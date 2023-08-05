import abc
import argparse
import importlib
import inspect as ins
import logging
import os
import pathlib
import sys
from collections import namedtuple, defaultdict
from operator import itemgetter

import toml

from . import util


class NotConfiguredError(Exception):
    pass


class ParseError(Exception):
    pass


class NoWorkspaceError(Exception):
    pass


app = defaultdict(dict)


def get_app(path='.'):
    p = pathlib.Path(path).absolute()
    while p != pathlib.Path(p.root):
        if (p / 'fret.toml').exists():
            break
        p = p.parent

    sys.path.append(str(p))
    app['path'] = str(p)

    config = toml.load((p / 'fret.toml').open())
    app.update(config)

    m = importlib.import_module(config['appname'])
    for m in ins.getmembers(m, _sub_class_checker(Command)):
        register_command(m[1], m[0].lower())
    for m in ins.getmembers(m, _sub_class_checker(Module)):
        register_module(m[1], m[0])

    try:
        mc = importlib.import_module(config['appname'] + '.command')
        for m in ins.getmembers(mc, _sub_class_checker(Command)):
            register_command(m[1], m[0].lower())
    except ImportError as e:
        if (config['appname'] + '.command') in str(e):
            pass
        else:
            raise

    try:
        mm = importlib.import_module(config['appname'] + '.module')
        for m in ins.getmembers(mm, _sub_class_checker(Module)):
            register_module(m[1], m[0])
    except ImportError:
        pass

    try:
        _ = importlib.import_module(config['appname'] + '.plugin')
    except ImportError:
        pass


def register_command(cls, name=None):
    if name is None:
        name = cls.__name__.lower()
    app['commands'][name] = cls


def register_module(cls, name=None):
    if name is None:
        name = cls.__name__
    app['modules'][name] = cls


def register_ws_mixin(cls, name=None):
    if name is None:
        name = cls.__name__.lower()
    app['ws_mixins'][name] = cls


class Workspace:
    """Workspace utilities. One can save/load configurations, build models
    with specific configuration, save checkpoints, open results, etc., using
    workspace objects."""

    def __init__(self, path):
        if not path:
            if str(os.getcwd()) == app['path']:
                path = 'ws/test'
            else:
                path = '.'

        if 'path' in app:
            # record relative path to
            path = os.path.relpath(path, app['path'])
            os.chdir(app['path'])

        self._path = pathlib.Path(path)
        self._log_path = self._path / 'log'
        self._checkpoint_path = self._path / 'checkpoint'
        self._result_path = self._path / 'result'
        self._config_path = self._path / 'config.toml'
        self._modules = None

    def load(self):
        """Load configuration."""
        self._modules = {}
        config = toml.load(self.config_path.open())
        for name, cfg in config.items():
            cls_name = cfg['module']
            del cfg['module']
            self.add_module(name, cls_name, cfg)

    def save(self):
        """Save configuration."""
        f = self.config_path.open('w')
        cfg = {name: dict({'module': cls_name}, **cfg)
               for name, (cls_name, cfg) in self._modules.items()}
        toml.dump(cfg, f)
        f.close()

    @property
    def path(self):
        if not self._path.exists():
            self._path.mkdir(parents=True)
        return self._path

    @property
    def result_path(self):
        if not self._result_path.exists():
            self._result_path.mkdir(parents=True)
        return self._result_path

    @property
    def checkpoint_path(self):
        if not self._checkpoint_path.exists():
            self._checkpoint_path.mkdir(parents=True)
        return self._checkpoint_path

    @property
    def log_path(self):
        if not self._log_path.exists():
            self._log_path.mkdir(parents=True)
        return self._log_path

    @property
    def config_path(self):
        if not self._config_path.exists():
            _ = self.path
            self._config_path.open('w').close()
        return self._config_path

    def add_module(self, name, module, config=None):
        if self._modules is None:
            self.load()
        if config is None:
            self._modules[name] = (module.__class__.__name__,
                                   module.config._asdict())
        else:
            self._modules[name] = (module, config)

    def get_module(self, name='main'):
        if self._modules is None:
            self.load()
        if name in self._modules:
            return self._modules[name]
        else:
            raise NotConfiguredError('module %s not configured' % name)

    def build_module(self, name='main'):
        """Build module according to the configurations in current
        workspace."""
        cls_name, cfg = self.get_module(name)
        cfg = cfg.copy()
        try:
            cls = app['modules'][cls_name]
        except KeyError:
            raise KeyError('definition of module %s not found', cls_name)

        for sub in cls.submodules:
            if sub in cfg and isinstance(cfg[sub], str):
                cfg[sub] = self.build_module(sub)

        for k, v in cfg.items():
            if isinstance(v, str) and v.startswith('ref('):
                cfg[k] = self.deref(v[4:-1])  # remove 'ref()'

        # noinspection PyCallingNonCallable
        obj = cls(**cfg)
        obj.ws = self
        return obj

    def deref(self, r):
        *modules, attr = r.split('.')
        name = 'main'
        cfg = self.get_module(name)[1]
        for m in modules:
            name = cfg[m]
            cfg = self.get_module(name)[1]
        return cfg[attr]

    def logger(self, name: str):
        """Get a logger that logs to a file.

        Notice that same logger instance is returned for same names.

        Args:
            name(str): logger name
        """
        logger = logging.getLogger(name)
        if logger.handlers:
            # previously configured, remain unchanged
            return logger
        file_formatter = logging.Formatter('%(levelname)s [%(name)s] '
                                           '%(asctime)s %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(
            str(self.log_path / (name + '.log')))
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        return logger

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return 'Workspace(path=' + str(self.path) + ')'


class Module(abc.ABC):
    """Interface for configurable modules.

    Each module class should have an ``configure`` class method to define
    model arguments along with their types, default values, etc.
    """

    submodules = []

    @property
    def ws(self):
        if self._ws is not None:
            return self._ws
        raise NoWorkspaceError('should be run in a workspace')

    @ws.setter
    def ws(self, ws):
        self._ws = ws

    @util.classproperty
    def help(cls):
        return 'module ' + cls.__name__

    @classmethod
    def _add_arguments(cls, parser: argparse.ArgumentParser):
        for base_cls in cls.__bases__:
            if hasattr(base_cls, 'add_arguments'):
                base_cls.add_arguments(parser)
        cls.add_arguments(parser)
        for submodule in cls.submodules:
            parser.add_argument('-' + submodule, default=submodule,
                                help='submodule ' + submodule)

    @classmethod
    @abc.abstractmethod
    def add_arguments(cls, parser: argparse.ArgumentParser):
        """Add arguments to an argparse subparser."""
        raise NotImplementedError

    @classmethod
    def parse(cls, args):
        """Parse command-line options and build module."""

        class _ArgumentParser(argparse.ArgumentParser):
            def error(self, message):
                raise ParseError(message)

        parser = _ArgumentParser(prog='', add_help=False)
        cls._add_arguments(parser)
        args = parser.parse_args(args)
        config = dict(args._get_kwargs())
        return cls(**config)

    def __init__(self, **kwargs):
        """
        Args:
            config (namedtuple): module configuration
        """
        keys, values = zip(*sorted(list(kwargs.items()), key=itemgetter(0)))
        config = namedtuple(self.__class__.__name__, keys)(*values)
        self.config = config
        self._ws = None

    def __str__(self):
        return str(self.config)

    def __repr__(self):
        return str(self)


class Command(abc.ABC):
    """Command interface."""

    @util.classproperty
    def help(cls):
        return 'command ' + cls.__name__.lower()

    def __init__(self, parser):
        self.parser = parser

    def _run(self, args):
        ws = Workspace(args.workspace)
        cmd = args.command
        del args.command, args.func, args.workspace
        args = {name: value for (name, value) in args._get_kwargs()}
        args = namedtuple(cmd, args.keys())(*args.values())
        return self.run(ws, args)

    @abc.abstractmethod
    def run(self, ws, args):
        raise NotImplementedError


def configurable(cls):
    orig_init = cls.__init__
    submodules, config = _get_args(orig_init)
    submodules = submodules[1:]

    @classmethod
    def add_arguments(_, parser):
        _add_arguments_by_kwargs(parser, config)

    def new_init(self, *args, **kwargs):
        cfg = {k: v for k, v in config}
        cfg.update(kwargs)
        for k in cfg:
            v = cfg[k]
            if isinstance(v, tuple):
                cfg[k] = v[0]
            elif isinstance(v, dict):
                cfg[k] = v.get('default')
        if not hasattr(self, 'config'):
            Module.__init__(**ins.getcallargs(
                orig_init, self, *args, **cfg))
        orig_init(self, *args, **cfg)

    d = dict(cls.__dict__)
    d.update(Module.__dict__)
    d.update(dict(
        __init__=new_init,
        add_arguments=add_arguments,
        submodules=submodules))
    new_cls = type(cls.__name__, (cls.__base__,), d)
    register_module(new_cls)
    return new_cls


def command(f):
    _args, config = _get_args(f)

    class Cmd(Command):
        def __init__(self, parser):
            super().__init__(parser)
            for arg in _args[1:]:
                parser.add_argument('-' + arg)
            _add_arguments_by_kwargs(parser, config)

        def run(self, ws, args):
            f.args = args
            return f(ws, **args._asdict())

    Cmd.__name__ = f.__name__[0].upper() + f.__name__[1:]
    register_command(Cmd)
    return f


def _get_args(f):
    spec = ins.getfullargspec(f)
    n_config = len(spec.defaults) if spec.defaults else 0
    args = spec.args if n_config == 0 else spec.args[:-n_config]
    kwargs = [] if n_config == 0 else \
        [(k, v) for k, v in zip(spec.args[-n_config:], spec.defaults)]
    return args, kwargs


def _add_arguments_by_kwargs(parser, config):
    for k, v in config:
        # TODO: add arg style (java/gnu)
        if isinstance(v, ref):
            continue
        if isinstance(v, tuple):
            if len(v) > 0 and isinstance(v[0], tuple):
                # kwargs for parser.add_argument
                v = {x: y for x, y in v}
            else:
                # just default value and help
                nv = {
                    'default': v[0],
                    'type': type(v[0]),
                    'help': v[1]
                } if v[0] is not None else {
                    'help': v[1]
                }
                if len(v) > 2:
                    nv['choices'] = v[2]
                v = nv
            parser.add_argument('-' + k, **v)
        else:
            parser.add_argument('-' + k, default=v, type=type(v))


def _sub_class_checker(cls):
    def rv(obj):
        if ins.isclass(obj) and not ins.isabstract(obj) \
                and issubclass(obj, cls):
            return True
        else:
            return False

    return rv


class ref:
    def __init__(self, attr):
        self.attr = attr

    def __str__(self):
        return 'ref(%s)' % self.attr

    def __repr__(self):
        return str(self)
