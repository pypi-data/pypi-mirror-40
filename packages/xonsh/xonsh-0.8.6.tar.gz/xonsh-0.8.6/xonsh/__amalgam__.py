"""Amalgamation of xonsh package, made up of the following modules, in order:

* completer
* contexts
* lazyasd
* lazyjson
* platform
* pretty
* codecache
* lazyimps
* parser
* tokenize
* tools
* ast
* color_tools
* commands_cache
* diff_history
* events
* foreign_shells
* jobs
* jsonutils
* lexer
* openpy
* xontribs
* ansi_colors
* dirstack
* proc
* shell
* style_tools
* timings
* xonfig
* base_shell
* environ
* inspectors
* readline_shell
* replay
* tracer
* aliases
* dumb_shell
* built_ins
* execer
* imphooks
* main

"""

from sys import modules as _modules
from types import ModuleType as _ModuleType
from importlib import import_module as _import_module


class _LazyModule(_ModuleType):

    def __init__(self, pkg, mod, asname=None):
        '''Lazy module 'pkg.mod' in package 'pkg'.'''
        self.__dct__ = {
            'loaded': False,
            'pkg': pkg,  # pkg
            'mod': mod,  # pkg.mod
            'asname': asname,  # alias
            }

    @classmethod
    def load(cls, pkg, mod, asname=None):
        if mod in _modules:
            key = pkg if asname is None else mod
            return _modules[key]
        else:
            return cls(pkg, mod, asname)

    def __getattribute__(self, name):
        if name == '__dct__':
            return super(_LazyModule, self).__getattribute__(name)
        dct = self.__dct__
        mod = dct['mod']
        if dct['loaded']:
            m = _modules[mod]
        else:
            m = _import_module(mod)
            glbs = globals()
            pkg = dct['pkg']
            asname = dct['asname']
            if asname is None:
                glbs[pkg] = m = _modules[pkg]
            else:
                glbs[asname] = m
            dct['loaded'] = True
        return getattr(m, name)

#
# completer
#
# -*- coding: utf-8 -*-
"""A (tab-)completer for xonsh."""
builtins = _LazyModule.load('builtins', 'builtins')
cabc = _LazyModule.load('collections', 'collections.abc', 'cabc')
class Completer(object):
    """This provides a list of optional completions for the xonsh shell."""

    def complete(self, prefix, line, begidx, endidx, ctx=None):
        """Complete the string, given a possible execution context.

        Parameters
        ----------
        prefix : str
            The string to match
        line : str
            The line that prefix appears on.
        begidx : int
            The index in line that prefix starts on.
        endidx : int
            The index in line that prefix ends on.
        ctx : Iterable of str (ie dict, set, etc), optional
            Names in the current execution context.

        Returns
        -------
        rtn : list of str
            Possible completions of prefix, sorted alphabetically.
        lprefix : int
            Length of the prefix to be replaced in the completion.
        """
        ctx = ctx or {}
        for func in builtins.__xonsh__.completers.values():
            try:
                out = func(prefix, line, begidx, endidx, ctx)
            except StopIteration:
                return set(), len(prefix)
            if isinstance(out, cabc.Sequence):
                res, lprefix = out
            else:
                res = out
                lprefix = len(prefix)
            if res is not None and len(res) != 0:

                def sortkey(s):
                    return s.lstrip(''''"''').lower()

                return tuple(sorted(res, key=sortkey)), lprefix
        return set(), lprefix

#
# contexts
#
"""Context management tools for xonsh."""
sys = _LazyModule.load('sys', 'sys')
textwrap = _LazyModule.load('textwrap', 'textwrap')
# amalgamated builtins
from collections.abc import Mapping


class Block(object):
    """This is a context manager for obtaining a block of lines without actually
    executing the block. The lines are accessible as the 'lines' attribute.
    This must be used as a macro.
    """

    __xonsh_block__ = str

    def __init__(self):
        """
        Attributes
        ----------
        lines : list of str or None
            Block lines as if split by str.splitlines(), if available.
        glbs : Mapping or None
            Global execution context, ie globals().
        locs : Mapping or None
            Local execution context, ie locals().
        """
        self.lines = self.glbs = self.locs = None

    def __enter__(self):
        if not hasattr(self, "macro_block"):
            raise XonshError(self.__class__.__name__ + " must be entered as a macro!")
        self.lines = self.macro_block.splitlines()
        self.glbs = self.macro_globals
        if self.macro_locals is not self.macro_globals:
            # leave locals as None when it is the same as globals
            self.locs = self.macro_locals
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Functor(Block):
    """This is a context manager that turns the block into a callable
    object, bound to the execution context it was created in.
    """

    def __init__(self, args=(), kwargs=None, rtn=""):
        """
        Parameters
        ----------
        args : Sequence of str, optional
            A tuple of argument names for the functor.
        kwargs : Mapping of str to values or list of item tuples, optional
            Keyword argument names and values, if available.
        rtn : str, optional
            Name of object to return, if available.

        Attributes
        ----------
        func : function
            The underlying function object. This defaults to none and is set
            after the the block is exited.
        """
        super().__init__()
        self.func = None
        self.args = args
        if kwargs is None:
            self.kwargs = []
        elif isinstance(kwargs, Mapping):
            self.kwargs = sorted(kwargs.items())
        else:
            self.kwargs = kwargs
        self.rtn = rtn

    def __enter__(self):
        super().__enter__()
        body = textwrap.indent(self.macro_block, "    ")
        uid = hash(body) + sys.maxsize  # should always be a positive int
        name = "__xonsh_functor_{uid}__".format(uid=uid)
        # construct signature string
        sig = rtn = ""
        sig = ", ".join(self.args)
        kwstr = ", ".join([k + "=None" for k, _ in self.kwargs])
        if len(kwstr) > 0:
            sig = kwstr if len(sig) == 0 else sig + ", " + kwstr
        # construct return string
        rtn = str(self.rtn)
        if len(rtn) > 0:
            rtn = "    return " + rtn + "\n"
        # construct function string
        fstr = "def {name}({sig}):\n{body}\n{rtn}"
        fstr = fstr.format(name=name, sig=sig, body=body, rtn=rtn)
        glbs = self.glbs
        locs = self.locs
        execer = builtins.__xonsh__.execer
        execer.exec(fstr, glbs=glbs, locs=locs)
        if locs is not None and name in locs:
            func = locs[name]
        elif name in glbs:
            func = glbs[name]
        else:
            raise ValueError("Functor block could not be found in context.")
        if len(self.kwargs) > 0:
            func.__defaults__ = tuple(v for _, v in self.kwargs)
        self.func = func
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __call__(self, *args, **kwargs):
        """Dispatches to func."""
        if self.func is None:
            msg = "{} block with 'None' func not callable"
            raise AttributeError(msg.formst(self.__class__.__name__))
        return self.func(*args, **kwargs)

#
# lazyasd
#
"""Lazy and self destructive containers for speeding up module import."""
# Copyright 2015-2016, the xonsh developers. All rights reserved.
os = _LazyModule.load('os', 'os')
# amalgamated sys
time = _LazyModule.load('time', 'time')
types = _LazyModule.load('types', 'types')
# amalgamated builtins
threading = _LazyModule.load('threading', 'threading')
importlib = _LazyModule.load('importlib', 'importlib')
importlib = _LazyModule.load('importlib', 'importlib.util')
# amalgamated collections.abc
__version__ = "0.1.3"


class LazyObject(object):
    def __init__(self, load, ctx, name):
        """Lazily loads an object via the load function the first time an
        attribute is accessed. Once loaded it will replace itself in the
        provided context (typically the globals of the call site) with the
        given name.

        For example, you can prevent the compilation of a regular expression
        until it is actually used::

            DOT = LazyObject((lambda: re.compile('.')), globals(), 'DOT')

        Parameters
        ----------
        load : function with no arguments
            A loader function that performs the actual object construction.
        ctx : Mapping
            Context to replace the LazyObject instance in
            with the object returned by load().
        name : str
            Name in the context to give the loaded object. This *should*
            be the name on the LHS of the assignment.
        """
        self._lasdo = {"loaded": False, "load": load, "ctx": ctx, "name": name}

    def _lazy_obj(self):
        d = self._lasdo
        if d["loaded"]:
            obj = d["obj"]
        else:
            obj = d["load"]()
            d["ctx"][d["name"]] = d["obj"] = obj
            d["loaded"] = True
        return obj

    def __getattribute__(self, name):
        if name == "_lasdo" or name == "_lazy_obj":
            return super().__getattribute__(name)
        obj = self._lazy_obj()
        return getattr(obj, name)

    def __bool__(self):
        obj = self._lazy_obj()
        return bool(obj)

    def __iter__(self):
        obj = self._lazy_obj()
        yield from obj

    def __getitem__(self, item):
        obj = self._lazy_obj()
        return obj[item]

    def __setitem__(self, key, value):
        obj = self._lazy_obj()
        obj[key] = value

    def __delitem__(self, item):
        obj = self._lazy_obj()
        del obj[item]

    def __call__(self, *args, **kwargs):
        obj = self._lazy_obj()
        return obj(*args, **kwargs)

    def __lt__(self, other):
        obj = self._lazy_obj()
        return obj < other

    def __le__(self, other):
        obj = self._lazy_obj()
        return obj <= other

    def __eq__(self, other):
        obj = self._lazy_obj()
        return obj == other

    def __ne__(self, other):
        obj = self._lazy_obj()
        return obj != other

    def __gt__(self, other):
        obj = self._lazy_obj()
        return obj > other

    def __ge__(self, other):
        obj = self._lazy_obj()
        return obj >= other

    def __hash__(self):
        obj = self._lazy_obj()
        return hash(obj)

    def __or__(self, other):
        obj = self._lazy_obj()
        return obj | other

    def __str__(self):
        return str(self._lazy_obj())

    def __repr__(self):
        return repr(self._lazy_obj())


def lazyobject(f):
    """Decorator for constructing lazy objects from a function."""
    return LazyObject(f, f.__globals__, f.__name__)


class LazyDict(cabc.MutableMapping):
    def __init__(self, loaders, ctx, name):
        """Dictionary like object that lazily loads its values from an initial
        dict of key-loader function pairs.  Each key is loaded when its value
        is first accessed. Once fully loaded, this object will replace itself
        in the provided context (typically the globals of the call site) with
        the given name.

        For example, you can prevent the compilation of a bunch of regular
        expressions until they are actually used::

            RES = LazyDict({
                    'dot': lambda: re.compile('.'),
                    'all': lambda: re.compile('.*'),
                    'two': lambda: re.compile('..'),
                    }, globals(), 'RES')

        Parameters
        ----------
        loaders : Mapping of keys to functions with no arguments
            A mapping of loader function that performs the actual value
            construction upon access.
        ctx : Mapping
            Context to replace the LazyDict instance in
            with the the fully loaded mapping.
        name : str
            Name in the context to give the loaded mapping. This *should*
            be the name on the LHS of the assignment.
        """
        self._loaders = loaders
        self._ctx = ctx
        self._name = name
        self._d = type(loaders)()  # make sure to return the same type

    def _destruct(self):
        if len(self._loaders) == 0:
            self._ctx[self._name] = self._d

    def __getitem__(self, key):
        d = self._d
        if key in d:
            val = d[key]
        else:
            # pop will raise a key error for us
            loader = self._loaders.pop(key)
            d[key] = val = loader()
            self._destruct()
        return val

    def __setitem__(self, key, value):
        self._d[key] = value
        if key in self._loaders:
            del self._loaders[key]
            self._destruct()

    def __delitem__(self, key):
        if key in self._d:
            del self._d[key]
        else:
            del self._loaders[key]
            self._destruct()

    def __iter__(self):
        yield from (set(self._d.keys()) | set(self._loaders.keys()))

    def __len__(self):
        return len(self._d) + len(self._loaders)


def lazydict(f):
    """Decorator for constructing lazy dicts from a function."""
    return LazyDict(f, f.__globals__, f.__name__)


class LazyBool(object):
    def __init__(self, load, ctx, name):
        """Boolean like object that lazily computes it boolean value when it is
        first asked. Once loaded, this result will replace itself
        in the provided context (typically the globals of the call site) with
        the given name.

        For example, you can prevent the complex boolean until it is actually
        used::

            ALIVE = LazyDict(lambda: not DEAD, globals(), 'ALIVE')

        Parameters
        ----------
        load : function with no arguments
            A loader function that performs the actual boolean evaluation.
        ctx : Mapping
            Context to replace the LazyBool instance in
            with the the fully loaded mapping.
        name : str
            Name in the context to give the loaded mapping. This *should*
            be the name on the LHS of the assignment.
        """
        self._load = load
        self._ctx = ctx
        self._name = name
        self._result = None

    def __bool__(self):
        if self._result is None:
            res = self._ctx[self._name] = self._result = self._load()
        else:
            res = self._result
        return res


def lazybool(f):
    """Decorator for constructing lazy booleans from a function."""
    return LazyBool(f, f.__globals__, f.__name__)


#
# Background module loaders
#


class BackgroundModuleProxy(types.ModuleType):
    """Proxy object for modules loaded in the background that block attribute
    access until the module is loaded..
    """

    def __init__(self, modname):
        self.__dct__ = {"loaded": False, "modname": modname}

    def __getattribute__(self, name):
        passthrough = frozenset({"__dct__", "__class__", "__spec__"})
        if name in passthrough:
            return super().__getattribute__(name)
        dct = self.__dct__
        modname = dct["modname"]
        if dct["loaded"]:
            mod = sys.modules[modname]
        else:
            delay_types = (BackgroundModuleProxy, type(None))
            while isinstance(sys.modules.get(modname, None), delay_types):
                time.sleep(0.001)
            mod = sys.modules[modname]
            dct["loaded"] = True
        # some modules may do construction after import, give them a second
        stall = 0
        while not hasattr(mod, name) and stall < 1000:
            stall += 1
            time.sleep(0.001)
        return getattr(mod, name)


class BackgroundModuleLoader(threading.Thread):
    """Thread to load modules in the background."""

    def __init__(self, name, package, replacements, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.name = name
        self.package = package
        self.replacements = replacements
        self.start()

    def run(self):
        # wait for other modules to stop being imported
        # We assume that module loading is finished when sys.modules doesn't
        # get longer in 5 consecutive 1ms waiting steps
        counter = 0
        last = -1
        while counter < 5:
            new = len(sys.modules)
            if new == last:
                counter += 1
            else:
                last = new
                counter = 0
            time.sleep(0.001)
        # now import module properly
        modname = importlib.util.resolve_name(self.name, self.package)
        if isinstance(sys.modules[modname], BackgroundModuleProxy):
            del sys.modules[modname]
        mod = importlib.import_module(self.name, package=self.package)
        for targname, varname in self.replacements.items():
            if targname in sys.modules:
                targmod = sys.modules[targname]
                setattr(targmod, varname, mod)


def load_module_in_background(
    name, package=None, debug="DEBUG", env=None, replacements=None
):
    """Entry point for loading modules in background thread.

    Parameters
    ----------
    name : str
        Module name to load in background thread.
    package : str or None, optional
        Package name, has the same meaning as in importlib.import_module().
    debug : str, optional
        Debugging symbol name to look up in the environment.
    env : Mapping or None, optional
        Environment this will default to __xonsh__.env, if available, and
        os.environ otherwise.
    replacements : Mapping or None, optional
        Dictionary mapping fully qualified module names (eg foo.bar.baz) that
        import the lazily loaded module, with the variable name in that
        module. For example, suppose that foo.bar imports module a as b,
        this dict is then {'foo.bar': 'b'}.

    Returns
    -------
    module : ModuleType
        This is either the original module that is found in sys.modules or
        a proxy module that will block until delay attribute access until the
        module is fully loaded.
    """
    modname = importlib.util.resolve_name(name, package)
    if modname in sys.modules:
        return sys.modules[modname]
    if env is None:
        xonsh_obj = getattr(builtins, "__xonsh__", None)
        env = os.environ if xonsh_obj is None else getattr(xonsh_obj, "env", os.environ)
    if env.get(debug, None):
        mod = importlib.import_module(name, package=package)
        return mod
    proxy = sys.modules[modname] = BackgroundModuleProxy(modname)
    BackgroundModuleLoader(name, package, replacements or {})
    return proxy

#
# lazyjson
#
# -*- coding: utf-8 -*-
"""Implements a lazy JSON file class that wraps around json data."""
io = _LazyModule.load('io', 'io')
json = _LazyModule.load('json', 'json')
weakref = _LazyModule.load('weakref', 'weakref')
contextlib = _LazyModule.load('contextlib', 'contextlib')
# amalgamated collections.abc
def _to_json_with_size(obj, offset=0, sort_keys=False):
    if isinstance(obj, str):
        s = json.dumps(obj)
        o = offset
        n = size = len(s.encode())  # size in bytes
    elif isinstance(obj, cabc.Mapping):
        s = "{"
        j = offset + 1
        o = {}
        size = {}
        items = sorted(obj.items()) if sort_keys else obj.items()
        for key, val in items:
            s_k, o_k, n_k, size_k = _to_json_with_size(
                key, offset=j, sort_keys=sort_keys
            )
            s += s_k + ": "
            j += n_k + 2
            s_v, o_v, n_v, size_v = _to_json_with_size(
                val, offset=j, sort_keys=sort_keys
            )
            o[key] = o_v
            size[key] = size_v
            s += s_v + ", "
            j += n_v + 2
        if s.endswith(", "):
            s = s[:-2]
        s += "}\n"
        n = len(s)
        o["__total__"] = offset
        size["__total__"] = n
    elif isinstance(obj, cabc.Sequence):
        s = "["
        j = offset + 1
        o = []
        size = []
        for x in obj:
            s_x, o_x, n_x, size_x = _to_json_with_size(x, offset=j, sort_keys=sort_keys)
            o.append(o_x)
            size.append(size_x)
            s += s_x + ", "
            j += n_x + 2
        if s.endswith(", "):
            s = s[:-2]
        s += "]\n"
        n = len(s)
        o.append(offset)
        size.append(n)
    else:
        s = json.dumps(obj, sort_keys=sort_keys)
        o = offset
        n = size = len(s)
    return s, o, n, size


def index(obj, sort_keys=False):
    """Creates an index for a JSON file."""
    idx = {}
    json_obj = _to_json_with_size(obj, sort_keys=sort_keys)
    s, idx["offsets"], _, idx["sizes"] = json_obj
    return s, idx


JSON_FORMAT = """{{"locs": [{iloc:>10}, {ilen:>10}, {dloc:>10}, {dlen:>10}],
 "index": {index},
 "data": {data}
}}
"""


def dumps(obj, sort_keys=False):
    """Dumps an object to JSON with an index."""
    data, idx = index(obj, sort_keys=sort_keys)
    jdx = json.dumps(idx, sort_keys=sort_keys)
    iloc = 69
    ilen = len(jdx)
    dloc = iloc + ilen + 11
    dlen = len(data)
    s = JSON_FORMAT.format(
        index=jdx, data=data, iloc=iloc, ilen=ilen, dloc=dloc, dlen=dlen
    )
    return s


def ljdump(obj, fp, sort_keys=False):
    """Dumps an object to JSON file."""
    s = dumps(obj, sort_keys=sort_keys)
    fp.write(s)


class LJNode(cabc.Mapping, cabc.Sequence):
    """A proxy node for JSON nodes. Acts as both sequence and mapping."""

    def __init__(self, offsets, sizes, root):
        """Parameters
        ----------
        offsets : dict, list, or int
            offsets of corresponding data structure, in bytes
        sizes : dict, list, or int
            sizes of corresponding data structure, in bytes
        root : weakref.proxy of LazyJSON
            weakref back to root node, which should be a LazyJSON object.
        """
        self.offsets = offsets
        self.sizes = sizes
        self.root = root
        self.is_mapping = isinstance(self.offsets, cabc.Mapping)
        self.is_sequence = isinstance(self.offsets, cabc.Sequence)

    def __len__(self):
        # recall that for maps, the '__total__' key is added and for
        # sequences the last element represents the total size/offset.
        return len(self.sizes) - 1

    def load(self):
        """Returns the Python data structure represented by the node."""
        if self.is_mapping:
            offset = self.offsets["__total__"]
            size = self.sizes["__total__"]
        elif self.is_sequence:
            offset = self.offsets[-1]
            size = self.sizes[-1]
        elif isinstance(self.offsets, int):
            offset = self.offsets
            size = self.sizes
        return self._load_or_node(offset, size)

    def _load_or_node(self, offset, size):
        if isinstance(offset, int):
            with self.root._open(newline="\n") as f:
                f.seek(self.root.dloc + offset)
                s = f.read(size)
            val = json.loads(s)
        elif isinstance(offset, (cabc.Mapping, cabc.Sequence)):
            val = LJNode(offset, size, self.root)
        else:
            raise TypeError("incorrect types for offset node")
        return val

    def _getitem_mapping(self, key):
        if key == "__total__":
            raise KeyError('"__total__" is a special LazyJSON key!')
        offset = self.offsets[key]
        size = self.sizes[key]
        return self._load_or_node(offset, size)

    def _getitem_sequence(self, key):
        if isinstance(key, int):
            rtn = self._load_or_node(self.offsets[key], self.sizes[key])
        elif isinstance(key, slice):
            key = slice(*key.indices(len(self)))
            rtn = list(map(self._load_or_node, self.offsets[key], self.sizes[key]))
        else:
            raise TypeError("only integer indexing available")
        return rtn

    def __getitem__(self, key):
        if self.is_mapping:
            rtn = self._getitem_mapping(key)
        elif self.is_sequence:
            rtn = self._getitem_sequence(key)
        else:
            raise NotImplementedError
        return rtn

    def __iter__(self):
        if self.is_mapping:
            keys = set(self.offsets.keys())
            keys.discard("__total__")
            yield from iter(keys)
        elif self.is_sequence:
            i = 0
            n = len(self)
            while i < n:
                yield self._load_or_node(self.offsets[i], self.sizes[i])
                i += 1
        else:
            raise NotImplementedError


class LazyJSON(LJNode):
    """Represents a lazy json file. Can be used like a normal Python
    dict or list.
    """

    def __init__(self, f, reopen=True):
        """Parameters
        ----------
        f : file handle or str
            JSON file to open.
        reopen : bool, optional
            Whether new file handle should be opened for each load.
        """
        self._f = f
        self.reopen = reopen
        if not reopen and isinstance(f, str):
            self._f = open(f, "r", newline="\n")
        self._load_index()
        self.root = weakref.proxy(self)
        self.is_mapping = isinstance(self.offsets, cabc.Mapping)
        self.is_sequence = isinstance(self.offsets, cabc.Sequence)

    def __del__(self):
        self.close()

    def close(self):
        """Close the file handle, if appropriate."""
        if not self.reopen and isinstance(self._f, io.IOBase):
            try:
                self._f.close()
            except OSError:
                pass

    @contextlib.contextmanager
    def _open(self, *args, **kwargs):
        if self.reopen and isinstance(self._f, str):
            f = open(self._f, *args, **kwargs)
            yield f
            f.close()
        else:
            yield self._f

    def _load_index(self):
        """Loads the index from the start of the file."""
        with self._open(newline="\n") as f:
            # read in the location data
            f.seek(9)
            locs = f.read(48)
            locs = json.loads(locs)
            self.iloc, self.ilen, self.dloc, self.dlen = locs
            # read in the index
            f.seek(self.iloc)
            idx = f.read(self.ilen)
            idx = json.loads(idx)
        self.offsets = idx["offsets"]
        self.sizes = idx["sizes"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

#
# platform
#
"""Module for platform-specific constants and implementations, as well as
compatibility layers to make use of the 'best' implementation available
on a platform.
"""
# amalgamated os
# amalgamated sys
ctypes = _LazyModule.load('ctypes', 'ctypes')
signal = _LazyModule.load('signal', 'signal')
pathlib = _LazyModule.load('pathlib', 'pathlib')
# amalgamated builtins
platform = _LazyModule.load('platform', 'platform')
functools = _LazyModule.load('functools', 'functools')
subprocess = _LazyModule.load('subprocess', 'subprocess')
collections = _LazyModule.load('collections', 'collections')
# amalgamated collections.abc
# amalgamated importlib.util
# amalgamated xonsh.lazyasd
FD_STDIN = 0
FD_STDOUT = 1
FD_STDERR = 2


@lazyobject
def distro():
    try:
        import distro as d
    except ImportError:
        d = None
    except Exception:
        raise
    return d


#
# OS
#
ON_DARWIN = LazyBool(lambda: platform.system() == "Darwin", globals(), "ON_DARWIN")
"""``True`` if executed on a Darwin platform, else ``False``. """
ON_LINUX = LazyBool(lambda: platform.system() == "Linux", globals(), "ON_LINUX")
"""``True`` if executed on a Linux platform, else ``False``. """
ON_WINDOWS = LazyBool(lambda: platform.system() == "Windows", globals(), "ON_WINDOWS")
"""``True`` if executed on a native Windows platform, else ``False``. """
ON_CYGWIN = LazyBool(lambda: sys.platform == "cygwin", globals(), "ON_CYGWIN")
"""``True`` if executed on a Cygwin Windows platform, else ``False``. """
ON_MSYS = LazyBool(lambda: sys.platform == "msys", globals(), "ON_MSYS")
"""``True`` if executed on a MSYS Windows platform, else ``False``. """
ON_POSIX = LazyBool(lambda: (os.name == "posix"), globals(), "ON_POSIX")
"""``True`` if executed on a POSIX-compliant platform, else ``False``. """
ON_FREEBSD = LazyBool(
    lambda: (sys.platform.startswith("freebsd")), globals(), "ON_FREEBSD"
)
"""``True`` if on a FreeBSD operating system, else ``False``."""
ON_DRAGONFLY = LazyBool(
    lambda: (sys.platform.startswith("dragonfly")), globals(), "ON_DRAGONFLY"
)
"""``True`` if on a DragonFly BSD operating system, else ``False``."""
ON_NETBSD = LazyBool(
    lambda: (sys.platform.startswith("netbsd")), globals(), "ON_NETBSD"
)
"""``True`` if on a NetBSD operating system, else ``False``."""


@lazybool
def ON_BSD():
    """``True`` if on a BSD operating system, else ``False``."""
    return bool(ON_FREEBSD) or bool(ON_NETBSD) or bool(ON_DRAGONFLY)


@lazybool
def ON_BEOS():
    """True if we are on BeOS or Haiku."""
    return sys.platform == "beos5" or sys.platform == "haiku1"


#
# Python & packages
#

PYTHON_VERSION_INFO = sys.version_info[:3]
""" Version of Python interpreter as three-value tuple. """


@lazyobject
def PYTHON_VERSION_INFO_BYTES():
    """The python version info tuple in a canonical bytes form."""
    return ".".join(map(str, sys.version_info)).encode()


ON_ANACONDA = LazyBool(
    lambda: any(s in sys.version for s in {"Anaconda", "Continuum", "conda-forge"}),
    globals(),
    "ON_ANACONDA",
)
""" ``True`` if executed in an Anaconda instance, else ``False``. """
CAN_RESIZE_WINDOW = LazyBool(
    lambda: hasattr(signal, "SIGWINCH"), globals(), "CAN_RESIZE_WINDOW"
)
"""``True`` if we can resize terminal window, as provided by the presense of
signal.SIGWINCH, else ``False``.
"""


@lazybool
def HAS_PYGMENTS():
    """``True`` if `pygments` is available, else ``False``."""
    spec = importlib.util.find_spec("pygments")
    return spec is not None


@functools.lru_cache(1)
def pygments_version():
    """pygments.__version__ version if available, else None."""
    if HAS_PYGMENTS:
        import pygments

        v = pygments.__version__
    else:
        v = None
    return v


@functools.lru_cache(1)
def pygments_version_info():
    """ Returns `pygments`'s version as tuple of integers. """
    if HAS_PYGMENTS:
        return tuple(int(x) for x in pygments_version().strip("<>+-=.").split("."))
    else:
        return None


@functools.lru_cache(1)
def has_prompt_toolkit():
    """Tests if the `prompt_toolkit` is available."""
    spec = importlib.util.find_spec("prompt_toolkit")
    return spec is not None


@functools.lru_cache(1)
def ptk_version():
    """Returns `prompt_toolkit.__version__` if available, else ``None``."""
    if has_prompt_toolkit():
        import prompt_toolkit

        return getattr(prompt_toolkit, "__version__", "<0.57")
    else:
        return None


@functools.lru_cache(1)
def ptk_version_info():
    """ Returns `prompt_toolkit`'s version as tuple of integers. """
    if has_prompt_toolkit():
        return tuple(int(x) for x in ptk_version().strip("<>+-=.").split("."))
    else:
        return None


@functools.lru_cache(1)
def ptk_above_min_supported():
    minimum_required_ptk_version = (1, 0)
    return ptk_version_info()[:2] >= minimum_required_ptk_version


@functools.lru_cache(1)
def ptk_shell_type():
    """Returns the prompt_toolkit shell type based on the installed version."""
    if ptk_version_info()[:2] < (2, 0):
        return "prompt_toolkit1"
    else:
        return "prompt_toolkit2"


@functools.lru_cache(1)
def win_ansi_support():
    if ON_WINDOWS:
        try:
            from prompt_toolkit.utils import is_windows_vt100_supported, is_conemu_ansi
        except ImportError:
            return False
        return is_conemu_ansi() or is_windows_vt100_supported()
    else:
        return False


@functools.lru_cache(1)
def ptk_below_max_supported():
    ptk_max_version_cutoff = (2, 0)
    return ptk_version_info()[:2] < ptk_max_version_cutoff


@functools.lru_cache(1)
def best_shell_type():
    if builtins.__xonsh__.env.get("TERM", "") == "dumb":
        return "dumb"
    elif ON_WINDOWS or has_prompt_toolkit():
        return "prompt_toolkit"
    else:
        return "readline"


@functools.lru_cache(1)
def is_readline_available():
    """Checks if readline is available to import."""
    spec = importlib.util.find_spec("readline")
    return spec is not None


@lazyobject
def seps():
    """String of all path separators."""
    s = os.path.sep
    if os.path.altsep is not None:
        s += os.path.altsep
    return s


def pathsplit(p):
    """This is a safe version of os.path.split(), which does not work on input
    without a drive.
    """
    n = len(p)
    while n and p[n - 1] not in seps:
        n -= 1
    pre = p[:n]
    pre = pre.rstrip(seps) or pre
    post = p[n:]
    return pre, post


def pathbasename(p):
    """This is a safe version of os.path.basename(), which does not work on
    input without a drive.  This version does.
    """
    return pathsplit(p)[-1]


@lazyobject
def expanduser():
    """Dispatches to the correct platform-dependent expanduser() function."""
    if ON_WINDOWS:
        return windows_expanduser
    else:
        return os.path.expanduser


def windows_expanduser(path):
    """A Windows-specific expanduser() function for xonsh. This is needed
    since os.path.expanduser() does not check on Windows if the user actually
    exists. This restricts expanding the '~' if it is not followed by a
    separator. That is only '~/' and '~\' are expanded.
    """
    if not path.startswith("~"):
        return path
    elif len(path) < 2 or path[1] in seps:
        return os.path.expanduser(path)
    else:
        return path


# termios tc(get|set)attr indexes.
IFLAG = 0
OFLAG = 1
CFLAG = 2
LFLAG = 3
ISPEED = 4
OSPEED = 5
CC = 6


#
# Dev release info
#


@functools.lru_cache(1)
def githash():
    """Returns a tuple contains two strings: the hash and the date."""
    install_base = os.path.dirname(__file__)
    githash_file = "{}/dev.githash".format(install_base)
    if not os.path.exists(githash_file):
        return None, None
    sha = None
    date_ = None
    try:
        with open(githash_file) as f:
            sha, date_ = f.read().strip().split("|")
    except ValueError:
        pass
    return sha, date_


#
# Encoding
#

DEFAULT_ENCODING = sys.getdefaultencoding()
""" Default string encoding. """


if PYTHON_VERSION_INFO < (3, 5, 0):

    class DirEntry:
        def __init__(self, directory, name):
            self.__path__ = pathlib.Path(directory) / name
            self.name = name
            self.path = str(self.__path__)
            self.is_symlink = self.__path__.is_symlink

        def inode(self):
            return os.stat(self.path, follow_symlinks=False).st_ino

        def is_dir(self, *, follow_symlinks=True):
            if follow_symlinks:
                return self.__path__.is_dir()
            else:
                return not self.__path__.is_symlink() and self.__path__.is_dir()

        def is_file(self, *, follow_symlinks=True):
            if follow_symlinks:
                return self.__path__.is_file()
            else:
                return not self.__path__.is_symlink() and self.__path__.is_file()

        def stat(self, *, follow_symlinks=True):
            return os.stat(self.path, follow_symlinks=follow_symlinks)

    def scandir(path):
        """ Compatibility layer for  `os.scandir` from Python 3.5+. """
        return (DirEntry(path, x) for x in os.listdir(path))


else:
    scandir = os.scandir


#
# Linux distro
#


@functools.lru_cache(1)
def linux_distro():
    """The id of the Linux distribution running on, possibly 'unknown'.
    None on non-Linux platforms.
    """
    if ON_LINUX:
        if distro:
            ld = distro.id()
        elif PYTHON_VERSION_INFO < (3, 6, 6):
            ld = platform.linux_distribution()[0] or "unknown"
        elif "-ARCH-" in platform.platform():
            ld = "arch"  # that's the only one we need to know for now
        else:
            ld = "unknown"
    else:
        ld = None
    return ld


#
# Windows
#


@functools.lru_cache(1)
def git_for_windows_path():
    """Returns the path to git for windows, if available and None otherwise."""
    import winreg

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\GitForWindows")
        gfwp, _ = winreg.QueryValueEx(key, "InstallPath")
    except FileNotFoundError:
        gfwp = None
    return gfwp


@functools.lru_cache(1)
def windows_bash_command():
    """Determines the command for Bash on windows."""
    # Check that bash is on path otherwise try the default directory
    # used by Git for windows
    wbc = "bash"
    cmd_cache = builtins.__xonsh__.commands_cache
    bash_on_path = cmd_cache.lazy_locate_binary("bash", ignore_alias=True)
    if bash_on_path:
        try:
            out = subprocess.check_output(
                [bash_on_path, "--version"],
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError:
            bash_works = False
        else:
            # Check if Bash is from the "Windows Subsystem for Linux" (WSL)
            # which can't be used by xonsh foreign-shell/completer
            bash_works = out and "pc-linux-gnu" not in out.splitlines()[0]

        if bash_works:
            wbc = bash_on_path
        else:
            gfwp = git_for_windows_path()
            if gfwp:
                bashcmd = os.path.join(gfwp, "bin\\bash.exe")
                if os.path.isfile(bashcmd):
                    wbc = bashcmd
    return wbc


#
# Environment variables defaults
#

if ON_WINDOWS:

    class OSEnvironCasePreserving(cabc.MutableMapping):
        """ Case-preserving wrapper for os.environ on Windows.
            It uses nt.environ to get the correct cased keys on
            initialization. It also preserves the case of any variables
            add after initialization.
        """

        def __init__(self):
            import nt

            self._upperkeys = dict((k.upper(), k) for k in nt.environ)

        def _sync(self):
            """ Ensure that the case sensitive map of the keys are
                in sync with os.environ
            """
            envkeys = set(os.environ.keys())
            for key in envkeys.difference(self._upperkeys):
                self._upperkeys[key] = key.upper()
            for key in set(self._upperkeys).difference(envkeys):
                del self._upperkeys[key]

        def __contains__(self, k):
            self._sync()
            return k.upper() in self._upperkeys

        def __len__(self):
            self._sync()
            return len(self._upperkeys)

        def __iter__(self):
            self._sync()
            return iter(self._upperkeys.values())

        def __getitem__(self, k):
            self._sync()
            return os.environ[k]

        def __setitem__(self, k, v):
            self._sync()
            self._upperkeys[k.upper()] = k
            os.environ[k] = v

        def __delitem__(self, k):
            self._sync()
            if k.upper() in self._upperkeys:
                del self._upperkeys[k.upper()]
                del os.environ[k]

        def getkey_actual_case(self, k):
            self._sync()
            return self._upperkeys.get(k.upper())


@lazyobject
def os_environ():
    """This dispatches to the correct, case-sensitive version of os.environ.
    This is mainly a problem for Windows. See #2024 for more details.
    This can probably go away once support for Python v3.5 or v3.6 is
    dropped.
    """
    if ON_WINDOWS:
        return OSEnvironCasePreserving()
    else:
        return os.environ


@functools.lru_cache(1)
def bash_command():
    """Determines the command for Bash on the current platform."""
    if ON_WINDOWS:
        bc = windows_bash_command()
    else:
        bc = "bash"
    return bc


@lazyobject
def BASH_COMPLETIONS_DEFAULT():
    """A possibly empty tuple with default paths to Bash completions known for
    the current platform.
    """
    if ON_LINUX or ON_CYGWIN or ON_MSYS:
        bcd = ("/usr/share/bash-completion/bash_completion",)
    elif ON_DARWIN:
        bcd = (
            "/usr/local/share/bash-completion/bash_completion",  # v2.x
            "/usr/local/etc/bash_completion",
        )  # v1.x
    elif ON_WINDOWS and git_for_windows_path():
        bcd = (
            os.path.join(
                git_for_windows_path(), "usr\\share\\bash-completion\\bash_completion"
            ),
            os.path.join(
                git_for_windows_path(),
                "mingw64\\share\\git\\completion\\" "git-completion.bash",
            ),
        )
    else:
        bcd = ()
    return bcd


@lazyobject
def PATH_DEFAULT():
    if ON_LINUX or ON_CYGWIN or ON_MSYS:
        if linux_distro() == "arch":
            pd = (
                "/usr/local/sbin",
                "/usr/local/bin",
                "/usr/bin",
                "/usr/bin/site_perl",
                "/usr/bin/vendor_perl",
                "/usr/bin/core_perl",
            )
        else:
            pd = (
                os.path.expanduser("~/bin"),
                "/usr/local/sbin",
                "/usr/local/bin",
                "/usr/sbin",
                "/usr/bin",
                "/sbin",
                "/bin",
                "/usr/games",
                "/usr/local/games",
            )
    elif ON_DARWIN:
        pd = ("/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin")
    elif ON_WINDOWS:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        )
        pd = tuple(winreg.QueryValueEx(key, "Path")[0].split(os.pathsep))
    else:
        pd = ()
    return pd


#
# libc
#
@lazyobject
def LIBC():
    """The platform dependent libc implementation."""
    global ctypes
    if ON_DARWIN:
        import ctypes.util

        libc = ctypes.CDLL(ctypes.util.find_library("c"))
    elif ON_CYGWIN:
        libc = ctypes.CDLL("cygwin1.dll")
    elif ON_MSYS:
        libc = ctypes.CDLL("msys-2.0.dll")
    elif ON_BSD:
        try:
            libc = ctypes.CDLL("libc.so")
        except AttributeError:
            libc = None
        except OSError:
            # OS X; can't use ctypes.util.find_library because that creates
            # a new process on Linux, which is undesirable.
            try:
                libc = ctypes.CDLL("libc.dylib")
            except OSError:
                libc = None
    elif ON_POSIX:
        try:
            libc = ctypes.CDLL("libc.so")
        except AttributeError:
            libc = None
        except OSError:
            # Debian and derivatives do the wrong thing because /usr/lib/libc.so
            # is a GNU ld script rather than an ELF object. To get around this, we
            # have to be more specific.
            # We don't want to use ctypes.util.find_library because that creates a
            # new process on Linux. We also don't want to try too hard because at
            # this point we're already pretty sure this isn't Linux.
            try:
                libc = ctypes.CDLL("libc.so.6")
            except OSError:
                libc = None
        if not hasattr(libc, "sysinfo"):
            # Not Linux.
            libc = None
    elif ON_WINDOWS:
        if hasattr(ctypes, "windll") and hasattr(ctypes.windll, "kernel32"):
            libc = ctypes.windll.kernel32
        else:
            try:
                # Windows CE uses the cdecl calling convention.
                libc = ctypes.CDLL("coredll.lib")
            except (AttributeError, OSError):
                libc = None
    elif ON_BEOS:
        libc = ctypes.CDLL("libroot.so")
    else:
        libc = None
    return libc

#
# pretty
#
# -*- coding: utf-8 -*-
"""
Python advanced pretty printer.  This pretty printer is intended to
replace the old `pprint` python module which does not allow developers
to provide their own pretty print callbacks.

This module is based on ruby's `prettyprint.rb` library by `Tanaka Akira`.

The following implementations were forked from the IPython project:
* Copyright (c) 2008-2014, IPython Development Team
* Copyright (C) 2001-2007 Fernando Perez <fperez@colorado.edu>
* Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
* Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>

Example Usage
-------------

To directly print the representation of an object use `pprint`::

    from pretty import pretty_print
    pretty_pprint(complex_object)

To get a string of the output use `pretty`::

    from pretty import pretty
    string = pretty(complex_object)


Extending
---------

The pretty library allows developers to add pretty printing rules for their
own objects.  This process is straightforward.  All you have to do is to
add a `_repr_pretty_` method to your object and call the methods on the
pretty printer passed::

    class MyObject(object):

        def _repr_pretty_(self, p, cycle):
            ...

Here is an example implementation of a `_repr_pretty_` method for a list
subclass::

    class MyList(list):

        def _repr_pretty_(self, p, cycle):
            if cycle:
                p.text('MyList(...)')
            else:
                with p.group(8, 'MyList([', '])'):
                    for idx, item in enumerate(self):
                        if idx:
                            p.text(',')
                            p.breakable()
                        p.pretty(item)

The `cycle` parameter is `True` if pretty detected a cycle.  You *have* to
react to that or the result is an infinite loop.  `p.text()` just adds
non breaking text to the output, `p.breakable()` either adds a whitespace
or breaks here.  If you pass it an argument it's used instead of the
default space.  `p.pretty` prettyprints another object using the pretty print
method.

The first parameter to the `group` function specifies the extra indentation
of the next line.  In this example the next item will either be on the same
line (if the items are short enough) or aligned with the right edge of the
opening bracket of `MyList`.

If you just want to indent something you can use the group function
without open / close parameters.  You can also use this code::

    with p.indent(2):
        ...


:copyright: 2007 by Armin Ronacher.
            Portions (c) 2009 by Robert Kern.
:license: BSD License.
"""
# amalgamated io
re = _LazyModule.load('re', 're')
# amalgamated sys
# amalgamated types
datetime = _LazyModule.load('datetime', 'datetime')
# amalgamated contextlib
# amalgamated collections
# amalgamated xonsh.lazyasd
__all__ = [
    "pretty",
    "pretty_print",
    "PrettyPrinter",
    "RepresentationPrinter",
    "for_type",
    "for_type_by_name",
]


MAX_SEQ_LENGTH = 1000


def _safe_getattr(obj, attr, default=None):
    """Safe version of getattr.

    Same as getattr, but will return ``default`` on any Exception,
    rather than raising.
    """
    try:
        return getattr(obj, attr, default)
    except Exception:
        return default


CUnicodeIO = io.StringIO


def pretty(
    obj, verbose=False, max_width=79, newline="\n", max_seq_length=MAX_SEQ_LENGTH
):
    """
    Pretty print the object's representation.
    """
    if hasattr(obj, "xonsh_display"):
        return obj.xonsh_display()

    stream = CUnicodeIO()
    printer = RepresentationPrinter(
        stream, verbose, max_width, newline, max_seq_length=max_seq_length
    )
    printer.pretty(obj)
    printer.flush()
    return stream.getvalue()


def pretty_print(
    obj, verbose=False, max_width=79, newline="\n", max_seq_length=MAX_SEQ_LENGTH
):
    """
    Like pretty() but print to stdout.
    """
    printer = RepresentationPrinter(
        sys.stdout, verbose, max_width, newline, max_seq_length=max_seq_length
    )
    printer.pretty(obj)
    printer.flush()
    sys.stdout.write(newline)
    sys.stdout.flush()


class _PrettyPrinterBase(object):
    @contextlib.contextmanager
    def indent(self, indent):
        """with statement support for indenting/dedenting."""
        self.indentation += indent
        try:
            yield
        finally:
            self.indentation -= indent

    @contextlib.contextmanager
    def group(self, indent=0, open="", close=""):
        """like begin_group / end_group but for the with statement."""
        self.begin_group(indent, open)
        try:
            yield
        finally:
            self.end_group(indent, close)


class PrettyPrinter(_PrettyPrinterBase):
    """
    Baseclass for the `RepresentationPrinter` prettyprinter that is used to
    generate pretty reprs of objects.  Contrary to the `RepresentationPrinter`
    this printer knows nothing about the default pprinters or the `_repr_pretty_`
    callback method.
    """

    def __init__(
        self, output, max_width=79, newline="\n", max_seq_length=MAX_SEQ_LENGTH
    ):
        self.output = output
        self.max_width = max_width
        self.newline = newline
        self.max_seq_length = max_seq_length
        self.output_width = 0
        self.buffer_width = 0
        self.buffer = collections.deque()

        root_group = Group(0)
        self.group_stack = [root_group]
        self.group_queue = GroupQueue(root_group)
        self.indentation = 0

    def _break_outer_groups(self):
        while self.max_width < self.output_width + self.buffer_width:
            group = self.group_queue.deq()
            if not group:
                return
            while group.breakables:
                x = self.buffer.popleft()
                self.output_width = x.output(self.output, self.output_width)
                self.buffer_width -= x.width
            while self.buffer and isinstance(self.buffer[0], Text):
                x = self.buffer.popleft()
                self.output_width = x.output(self.output, self.output_width)
                self.buffer_width -= x.width

    def text(self, obj):
        """Add literal text to the output."""
        width = len(obj)
        if self.buffer:
            text = self.buffer[-1]
            if not isinstance(text, Text):
                text = Text()
                self.buffer.append(text)
            text.add(obj, width)
            self.buffer_width += width
            self._break_outer_groups()
        else:
            self.output.write(obj)
            self.output_width += width

    def breakable(self, sep=" "):
        """
        Add a breakable separator to the output.  This does not mean that it
        will automatically break here.  If no breaking on this position takes
        place the `sep` is inserted which default to one space.
        """
        width = len(sep)
        group = self.group_stack[-1]
        if group.want_break:
            self.flush()
            self.output.write(self.newline)
            self.output.write(" " * self.indentation)
            self.output_width = self.indentation
            self.buffer_width = 0
        else:
            self.buffer.append(Breakable(sep, width, self))
            self.buffer_width += width
            self._break_outer_groups()

    def break_(self):
        """
        Explicitly insert a newline into the output, maintaining correct indentation.
        """
        self.flush()
        self.output.write(self.newline)
        self.output.write(" " * self.indentation)
        self.output_width = self.indentation
        self.buffer_width = 0

    def begin_group(self, indent=0, open=""):
        """
        Begin a group.  If you want support for python < 2.5 which doesn't has
        the with statement this is the preferred way:

            p.begin_group(1, '{')
            ...
            p.end_group(1, '}')

        The python 2.5 expression would be this:

            with p.group(1, '{', '}'):
                ...

        The first parameter specifies the indentation for the next line (usually
        the width of the opening text), the second the opening text.  All
        parameters are optional.
        """
        if open:
            self.text(open)
        group = Group(self.group_stack[-1].depth + 1)
        self.group_stack.append(group)
        self.group_queue.enq(group)
        self.indentation += indent

    def _enumerate(self, seq):
        """like enumerate, but with an upper limit on the number of items"""
        for idx, x in enumerate(seq):
            if self.max_seq_length and idx >= self.max_seq_length:
                self.text(",")
                self.breakable()
                self.text("...")
                return
            yield idx, x

    def end_group(self, dedent=0, close=""):
        """End a group. See `begin_group` for more details."""
        self.indentation -= dedent
        group = self.group_stack.pop()
        if not group.breakables:
            self.group_queue.remove(group)
        if close:
            self.text(close)

    def flush(self):
        """Flush data that is left in the buffer."""
        for data in self.buffer:
            self.output_width += data.output(self.output, self.output_width)
        self.buffer.clear()
        self.buffer_width = 0


def _get_mro(obj_class):
    """ Get a reasonable method resolution order of a class and its superclasses
    for both old-style and new-style classes.
    """
    if not hasattr(obj_class, "__mro__"):
        # Old-style class. Mix in object to make a fake new-style class.
        try:
            obj_class = type(obj_class.__name__, (obj_class, object), {})
        except TypeError:
            # Old-style extension type that does not descend from object.
            # FIXME: try to construct a more thorough MRO.
            mro = [obj_class]
        else:
            mro = obj_class.__mro__[1:-1]
    else:
        mro = obj_class.__mro__
    return mro


class RepresentationPrinter(PrettyPrinter):
    """
    Special pretty printer that has a `pretty` method that calls the pretty
    printer for a python object.

    This class stores processing data on `self` so you must *never* use
    this class in a threaded environment.  Always lock it or reinstantiate
    it.

    Instances also have a verbose flag callbacks can access to control their
    output.  For example the default instance repr prints all attributes and
    methods that are not prefixed by an underscore if the printer is in
    verbose mode.
    """

    def __init__(
        self,
        output,
        verbose=False,
        max_width=79,
        newline="\n",
        singleton_pprinters=None,
        type_pprinters=None,
        deferred_pprinters=None,
        max_seq_length=MAX_SEQ_LENGTH,
    ):

        PrettyPrinter.__init__(
            self, output, max_width, newline, max_seq_length=max_seq_length
        )
        self.verbose = verbose
        self.stack = []
        if singleton_pprinters is None:
            singleton_pprinters = _singleton_pprinters.copy()
        self.singleton_pprinters = singleton_pprinters
        if type_pprinters is None:
            type_pprinters = _type_pprinters.copy()
        self.type_pprinters = type_pprinters
        if deferred_pprinters is None:
            deferred_pprinters = _deferred_type_pprinters.copy()
        self.deferred_pprinters = deferred_pprinters

    def pretty(self, obj):
        """Pretty print the given object."""
        obj_id = id(obj)
        cycle = obj_id in self.stack
        self.stack.append(obj_id)
        self.begin_group()
        try:
            obj_class = _safe_getattr(obj, "__class__", None) or type(obj)
            # First try to find registered singleton printers for the type.
            try:
                printer = self.singleton_pprinters[obj_id]
            except (TypeError, KeyError):
                pass
            else:
                return printer(obj, self, cycle)
            # Next walk the mro and check for either:
            #   1) a registered printer
            #   2) a _repr_pretty_ method
            for cls in _get_mro(obj_class):
                if cls in self.type_pprinters:
                    # printer registered in self.type_pprinters
                    return self.type_pprinters[cls](obj, self, cycle)
                else:
                    # deferred printer
                    printer = self._in_deferred_types(cls)
                    if printer is not None:
                        return printer(obj, self, cycle)
                    else:
                        # Finally look for special method names.
                        # Some objects automatically create any requested
                        # attribute. Try to ignore most of them by checking for
                        # callability.
                        if "_repr_pretty_" in cls.__dict__:
                            meth = cls._repr_pretty_
                            if callable(meth):
                                return meth(obj, self, cycle)
            return _default_pprint(obj, self, cycle)
        finally:
            self.end_group()
            self.stack.pop()

    def _in_deferred_types(self, cls):
        """
        Check if the given class is specified in the deferred type registry.

        Returns the printer from the registry if it exists, and None if the
        class is not in the registry. Successful matches will be moved to the
        regular type registry for future use.
        """
        mod = _safe_getattr(cls, "__module__", None)
        name = _safe_getattr(cls, "__name__", None)
        key = (mod, name)
        printer = None
        if key in self.deferred_pprinters:
            # Move the printer over to the regular registry.
            printer = self.deferred_pprinters.pop(key)
            self.type_pprinters[cls] = printer
        return printer


class Printable(object):
    def output(self, stream, output_width):
        return output_width


class Text(Printable):
    def __init__(self):
        self.objs = []
        self.width = 0

    def output(self, stream, output_width):
        for obj in self.objs:
            stream.write(obj)
        return output_width + self.width

    def add(self, obj, width):
        self.objs.append(obj)
        self.width += width


class Breakable(Printable):
    def __init__(self, seq, width, pretty):
        self.obj = seq
        self.width = width
        self.pretty = pretty
        self.indentation = pretty.indentation
        self.group = pretty.group_stack[-1]
        self.group.breakables.append(self)

    def output(self, stream, output_width):
        self.group.breakables.popleft()
        if self.group.want_break:
            stream.write(self.pretty.newline)
            stream.write(" " * self.indentation)
            return self.indentation
        if not self.group.breakables:
            self.pretty.group_queue.remove(self.group)
        stream.write(self.obj)
        return output_width + self.width


class Group(Printable):
    def __init__(self, depth):
        self.depth = depth
        self.breakables = collections.deque()
        self.want_break = False


class GroupQueue(object):
    def __init__(self, *groups):
        self.queue = []
        for group in groups:
            self.enq(group)

    def enq(self, group):
        depth = group.depth
        while depth > len(self.queue) - 1:
            self.queue.append([])
        self.queue[depth].append(group)

    def deq(self):
        for stack in self.queue:
            for idx, group in enumerate(reversed(stack)):
                if group.breakables:
                    del stack[idx]
                    group.want_break = True
                    return group
            for group in stack:
                group.want_break = True
            del stack[:]

    def remove(self, group):
        try:
            self.queue[group.depth].remove(group)
        except ValueError:
            pass


@lazyobject
def _baseclass_reprs():
    try:
        br = (object.__repr__, types.InstanceType.__repr__)
    except AttributeError:  # Python 3
        br = (object.__repr__,)
    return br


def _default_pprint(obj, p, cycle):
    """
    The default print function.  Used if an object does not provide one and
    it's none of the builtin objects.
    """
    klass = _safe_getattr(obj, "__class__", None) or type(obj)
    if _safe_getattr(klass, "__repr__", None) not in _baseclass_reprs:
        # A user-provided repr. Find newlines and replace them with p.break_()
        _repr_pprint(obj, p, cycle)
        return
    p.begin_group(1, "<")
    p.pretty(klass)
    p.text(" at 0x%x" % id(obj))
    if cycle:
        p.text(" ...")
    elif p.verbose:
        first = True
        for key in dir(obj):
            if not key.startswith("_"):
                try:
                    value = getattr(obj, key)
                except AttributeError:
                    continue
                if isinstance(value, types.MethodType):
                    continue
                if not first:
                    p.text(",")
                p.breakable()
                p.text(key)
                p.text("=")
                step = len(key) + 1
                p.indentation += step
                p.pretty(value)
                p.indentation -= step
                first = False
    p.end_group(1, ">")


def _seq_pprinter_factory(start, end, basetype):
    """
    Factory that returns a pprint function useful for sequences.  Used by
    the default pprint for tuples, dicts, and lists.
    """

    def inner(obj, p, cycle):
        typ = type(obj)
        if (
            basetype is not None
            and typ is not basetype
            and typ.__repr__ != basetype.__repr__
        ):
            # If the subclass provides its own repr, use it instead.
            return p.text(typ.__repr__(obj))

        if cycle:
            return p.text(start + "..." + end)
        step = len(start)
        p.begin_group(step, start)
        for idx, x in p._enumerate(obj):
            if idx:
                p.text(",")
                p.breakable()
            p.pretty(x)
        if len(obj) == 1 and type(obj) is tuple:
            # Special case for 1-item tuples.
            p.text(",")
        p.end_group(step, end)

    return inner


def _set_pprinter_factory(start, end, basetype):
    """
    Factory that returns a pprint function useful for sets and frozensets.
    """

    def inner(obj, p, cycle):
        typ = type(obj)
        if (
            basetype is not None
            and typ is not basetype
            and typ.__repr__ != basetype.__repr__
        ):
            # If the subclass provides its own repr, use it instead.
            return p.text(typ.__repr__(obj))

        if cycle:
            return p.text(start + "..." + end)
        if len(obj) == 0:
            # Special case.
            p.text(basetype.__name__ + "()")
        else:
            step = len(start)
            p.begin_group(step, start)
            # Like dictionary keys, we will try to sort the items if there aren't too many
            items = obj
            if not (p.max_seq_length and len(obj) >= p.max_seq_length):
                try:
                    items = sorted(obj)
                except Exception:
                    # Sometimes the items don't sort.
                    pass
            for idx, x in p._enumerate(items):
                if idx:
                    p.text(",")
                    p.breakable()
                p.pretty(x)
            p.end_group(step, end)

    return inner


def _dict_pprinter_factory(start, end, basetype=None):
    """
    Factory that returns a pprint function used by the default pprint of
    dicts and dict proxies.
    """

    def inner(obj, p, cycle):
        typ = type(obj)
        if (
            basetype is not None
            and typ is not basetype
            and typ.__repr__ != basetype.__repr__
        ):
            # If the subclass provides its own repr, use it instead.
            return p.text(typ.__repr__(obj))

        if cycle:
            return p.text("{...}")
        p.begin_group(1, start)
        keys = obj.keys()
        # if dict isn't large enough to be truncated, sort keys before displaying
        if not (p.max_seq_length and len(obj) >= p.max_seq_length):
            try:
                keys = sorted(keys)
            except Exception:
                # Sometimes the keys don't sort.
                pass
        for idx, key in p._enumerate(keys):
            if idx:
                p.text(",")
                p.breakable()
            p.pretty(key)
            p.text(": ")
            p.pretty(obj[key])
        p.end_group(1, end)

    return inner


def _super_pprint(obj, p, cycle):
    """The pprint for the super type."""
    p.begin_group(8, "<super: ")
    p.pretty(obj.__thisclass__)
    p.text(",")
    p.breakable()
    p.pretty(obj.__self__)
    p.end_group(8, ">")


def _re_pattern_pprint(obj, p, cycle):
    """The pprint function for regular expression patterns."""
    p.text("re.compile(")
    pattern = repr(obj.pattern)
    if pattern[:1] in "uU":
        pattern = pattern[1:]
        prefix = "ur"
    else:
        prefix = "r"
    pattern = prefix + pattern.replace("\\\\", "\\")
    p.text(pattern)
    if obj.flags:
        p.text(",")
        p.breakable()
        done_one = False
        for flag in (
            "TEMPLATE",
            "IGNORECASE",
            "LOCALE",
            "MULTILINE",
            "DOTALL",
            "UNICODE",
            "VERBOSE",
            "DEBUG",
        ):
            if obj.flags & getattr(re, flag):
                if done_one:
                    p.text("|")
                p.text("re." + flag)
                done_one = True
    p.text(")")


def _type_pprint(obj, p, cycle):
    """The pprint for classes and types."""
    # Heap allocated types might not have the module attribute,
    # and others may set it to None.

    # Checks for a __repr__ override in the metaclass
    if type(obj).__repr__ is not type.__repr__:
        _repr_pprint(obj, p, cycle)
        return

    mod = _safe_getattr(obj, "__module__", None)
    try:
        name = obj.__qualname__
        if not isinstance(name, str):
            # This can happen if the type implements __qualname__ as a property
            # or other descriptor in Python 2.
            raise Exception("Try __name__")
    except Exception:
        name = obj.__name__
        if not isinstance(name, str):
            name = "<unknown type>"

    if mod in (None, "__builtin__", "builtins", "exceptions"):
        p.text(name)
    else:
        p.text(mod + "." + name)


def _repr_pprint(obj, p, cycle):
    """A pprint that just redirects to the normal repr function."""
    # Find newlines and replace them with p.break_()
    output = repr(obj)
    for idx, output_line in enumerate(output.splitlines()):
        if idx:
            p.break_()
        p.text(output_line)


def _function_pprint(obj, p, cycle):
    """Base pprint for all functions and builtin functions."""
    name = _safe_getattr(obj, "__qualname__", obj.__name__)
    mod = obj.__module__
    if mod and mod not in ("__builtin__", "builtins", "exceptions"):
        name = mod + "." + name
    p.text("<function %s>" % name)


def _exception_pprint(obj, p, cycle):
    """Base pprint for all exceptions."""
    name = getattr(obj.__class__, "__qualname__", obj.__class__.__name__)
    if obj.__class__.__module__ not in ("exceptions", "builtins"):
        name = "%s.%s" % (obj.__class__.__module__, name)
    step = len(name) + 1
    p.begin_group(step, name + "(")
    for idx, arg in enumerate(getattr(obj, "args", ())):
        if idx:
            p.text(",")
            p.breakable()
        p.pretty(arg)
    p.end_group(step, ")")


@lazyobject
def _type_pprinters():
    #: printers for builtin types
    tp = {
        int: _repr_pprint,
        float: _repr_pprint,
        str: _repr_pprint,
        tuple: _seq_pprinter_factory("(", ")", tuple),
        list: _seq_pprinter_factory("[", "]", list),
        dict: _dict_pprinter_factory("{", "}", dict),
        set: _set_pprinter_factory("{", "}", set),
        frozenset: _set_pprinter_factory("frozenset({", "})", frozenset),
        super: _super_pprint,
        type(re.compile("")): _re_pattern_pprint,
        type: _type_pprint,
        types.FunctionType: _function_pprint,
        types.BuiltinFunctionType: _function_pprint,
        types.MethodType: _repr_pprint,
        datetime.datetime: _repr_pprint,
        datetime.timedelta: _repr_pprint,
    }
    #: the exception base
    try:
        _exception_base = BaseException
    except NameError:
        _exception_base = Exception
    tp[_exception_base] = _exception_pprint
    try:
        tp[types.DictProxyType] = _dict_pprinter_factory("<dictproxy {", "}>")
        tp[types.ClassType] = _type_pprint
        tp[types.SliceType] = _repr_pprint
    except AttributeError:  # Python 3
        tp[slice] = _repr_pprint
    try:
        tp[xrange] = _repr_pprint
        tp[long] = _repr_pprint
        tp[unicode] = _repr_pprint
    except NameError:
        tp[range] = _repr_pprint
        tp[bytes] = _repr_pprint
    return tp


#: printers for types specified by name
@lazyobject
def _deferred_type_pprinters():
    dtp = {}
    for_type_by_name("collections", "defaultdict", _defaultdict_pprint, dtp=dtp)
    for_type_by_name("collections", "OrderedDict", _ordereddict_pprint, dtp=dtp)
    for_type_by_name("collections", "deque", _deque_pprint, dtp=dtp)
    for_type_by_name("collections", "Counter", _counter_pprint, dtp=dtp)
    return dtp


def for_type(typ, func):
    """
    Add a pretty printer for a given type.
    """
    oldfunc = _type_pprinters.get(typ, None)
    if func is not None:
        # To support easy restoration of old pprinters, we need to ignore Nones.
        _type_pprinters[typ] = func
    return oldfunc


def for_type_by_name(type_module, type_name, func, dtp=None):
    """
    Add a pretty printer for a type specified by the module and name of a type
    rather than the type object itself.
    """
    if dtp is None:
        dtp = _deferred_type_pprinters
    key = (type_module, type_name)
    oldfunc = dtp.get(key, None)
    if func is not None:
        # To support easy restoration of old pprinters, we need to ignore Nones.
        dtp[key] = func
    return oldfunc


#: printers for the default singletons
_singleton_pprinters = LazyObject(
    lambda: dict.fromkeys(
        map(id, [None, True, False, Ellipsis, NotImplemented]), _repr_pprint
    ),
    globals(),
    "_singleton_pprinters",
)


def _defaultdict_pprint(obj, p, cycle):
    name = obj.__class__.__name__
    with p.group(len(name) + 1, name + "(", ")"):
        if cycle:
            p.text("...")
        else:
            p.pretty(obj.default_factory)
            p.text(",")
            p.breakable()
            p.pretty(dict(obj))


def _ordereddict_pprint(obj, p, cycle):
    name = obj.__class__.__name__
    with p.group(len(name) + 1, name + "(", ")"):
        if cycle:
            p.text("...")
        elif len(obj):
            p.pretty(list(obj.items()))


def _deque_pprint(obj, p, cycle):
    name = obj.__class__.__name__
    with p.group(len(name) + 1, name + "(", ")"):
        if cycle:
            p.text("...")
        else:
            p.pretty(list(obj))


def _counter_pprint(obj, p, cycle):
    name = obj.__class__.__name__
    with p.group(len(name) + 1, name + "(", ")"):
        if cycle:
            p.text("...")
        elif len(obj):
            p.pretty(dict(obj))

#
# codecache
#
"""Tools for caching xonsh code."""
# amalgamated os
# amalgamated sys
hashlib = _LazyModule.load('hashlib', 'hashlib')
marshal = _LazyModule.load('marshal', 'marshal')
# amalgamated builtins
from xonsh import __version__ as XONSH_VERSION
# amalgamated xonsh.lazyasd
# amalgamated xonsh.platform
def _splitpath(path, sofar=[]):
    folder, path = os.path.split(path)
    if path == "":
        return sofar[::-1]
    elif folder == "":
        return (sofar + [path])[::-1]
    else:
        return _splitpath(folder, sofar + [path])


@lazyobject
def _CHARACTER_MAP():
    cmap = {chr(o): "_%s" % chr(o + 32) for o in range(65, 91)}
    cmap.update({".": "_.", "_": "__"})
    return cmap


def _cache_renamer(path, code=False):
    if not code:
        path = os.path.realpath(path)
    o = ["".join(_CHARACTER_MAP.get(i, i) for i in w) for w in _splitpath(path)]
    o[-1] = "{}.{}".format(o[-1], sys.implementation.cache_tag)
    return o


def _make_if_not_exists(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def should_use_cache(execer, mode):
    """
    Return ``True`` if caching has been enabled for this mode (through command
    line flags or environment variables)
    """
    if mode == "exec":
        return (execer.scriptcache or execer.cacheall) and (
            builtins.__xonsh__.env["XONSH_CACHE_SCRIPTS"]
            or builtins.__xonsh__.env["XONSH_CACHE_EVERYTHING"]
        )
    else:
        return execer.cacheall or builtins.__xonsh__.env["XONSH_CACHE_EVERYTHING"]


def run_compiled_code(code, glb, loc, mode):
    """
    Helper to run code in a given mode and context
    """
    if code is None:
        return
    if mode in {"exec", "single"}:
        func = exec
    else:
        func = eval
    func(code, glb, loc)


def get_cache_filename(fname, code=True):
    """
    Return the filename of the cache for the given filename.

    Cache filenames are similar to those used by the Mercurial DVCS for its
    internal store.

    The ``code`` switch should be true if we should use the code store rather
    than the script store.
    """
    datadir = builtins.__xonsh__.env["XONSH_DATA_DIR"]
    cachedir = os.path.join(
        datadir, "xonsh_code_cache" if code else "xonsh_script_cache"
    )
    cachefname = os.path.join(cachedir, *_cache_renamer(fname, code=code))
    return cachefname


def update_cache(ccode, cache_file_name):
    """
    Update the cache at ``cache_file_name`` to contain the compiled code
    represented by ``ccode``.
    """
    if cache_file_name is not None:
        _make_if_not_exists(os.path.dirname(cache_file_name))
        with open(cache_file_name, "wb") as cfile:
            cfile.write(XONSH_VERSION.encode() + b"\n")
            cfile.write(bytes(PYTHON_VERSION_INFO_BYTES) + b"\n")
            marshal.dump(ccode, cfile)


def _check_cache_versions(cfile):
    # version data should be < 1 kb
    ver = cfile.readline(1024).strip()
    if ver != XONSH_VERSION.encode():
        return False
    ver = cfile.readline(1024).strip()
    return ver == PYTHON_VERSION_INFO_BYTES


def compile_code(filename, code, execer, glb, loc, mode):
    """
    Wrapper for ``execer.compile`` to compile the given code
    """
    try:
        if not code.endswith("\n"):
            code += "\n"
        old_filename = execer.filename
        execer.filename = filename
        ccode = execer.compile(code, glbs=glb, locs=loc, mode=mode, filename=filename)
    except Exception:
        raise
    finally:
        execer.filename = old_filename
    return ccode


def script_cache_check(filename, cachefname):
    """
    Check whether the script cache for a particular file is valid.

    Returns a tuple containing: a boolean representing whether the cached code
    should be used, and the cached code (or ``None`` if the cache should not be
    used).
    """
    ccode = None
    run_cached = False
    if os.path.isfile(cachefname):
        if os.stat(cachefname).st_mtime >= os.stat(filename).st_mtime:
            with open(cachefname, "rb") as cfile:
                if not _check_cache_versions(cfile):
                    return False, None
                ccode = marshal.load(cfile)
                run_cached = True
    return run_cached, ccode


def run_script_with_cache(filename, execer, glb=None, loc=None, mode="exec"):
    """
    Run a script, using a cached version if it exists (and the source has not
    changed), and updating the cache as necessary.
    """
    run_cached = False
    use_cache = should_use_cache(execer, mode)
    cachefname = get_cache_filename(filename, code=False)
    if use_cache:
        run_cached, ccode = script_cache_check(filename, cachefname)
    if not run_cached:
        with open(filename, "r") as f:
            code = f.read()
        ccode = compile_code(filename, code, execer, glb, loc, mode)
        update_cache(ccode, cachefname)
    run_compiled_code(ccode, glb, loc, mode)


def code_cache_name(code):
    """
    Return an appropriate spoofed filename for the given code.
    """
    if isinstance(code, str):
        _code = code.encode()
    else:
        _code = code
    return hashlib.md5(_code).hexdigest()


def code_cache_check(cachefname):
    """
    Check whether the code cache for a particular piece of code is valid.

    Returns a tuple containing: a boolean representing whether the cached code
    should be used, and the cached code (or ``None`` if the cache should not be
    used).
    """
    ccode = None
    run_cached = False
    if os.path.isfile(cachefname):
        with open(cachefname, "rb") as cfile:
            if not _check_cache_versions(cfile):
                return False, None
            ccode = marshal.load(cfile)
            run_cached = True
    return run_cached, ccode


def run_code_with_cache(code, execer, glb=None, loc=None, mode="exec"):
    """
    Run a piece of code, using a cached version if it exists, and updating the
    cache as necessary.
    """
    use_cache = should_use_cache(execer, mode)
    filename = code_cache_name(code)
    cachefname = get_cache_filename(filename, code=True)
    run_cached = False
    if use_cache:
        run_cached, ccode = code_cache_check(cachefname)
    if not run_cached:
        ccode = compile_code(filename, code, execer, glb, loc, mode)
        update_cache(ccode, cachefname)
    run_compiled_code(ccode, glb, loc, mode)

#
# lazyimps
#
"""Lazy imports that may apply across the xonsh package."""
# amalgamated importlib
# amalgamated xonsh.platform
# amalgamated xonsh.lazyasd
pygments = LazyObject(
    lambda: importlib.import_module("pygments"), globals(), "pygments"
)
pyghooks = LazyObject(
    lambda: importlib.import_module("xonsh.pyghooks"), globals(), "pyghooks"
)


@lazyobject
def pty():
    if ON_WINDOWS:
        return
    else:
        return importlib.import_module("pty")


@lazyobject
def termios():
    if ON_WINDOWS:
        return
    else:
        return importlib.import_module("termios")


@lazyobject
def fcntl():
    if ON_WINDOWS:
        return
    else:
        return importlib.import_module("fcntl")


@lazyobject
def tty():
    if ON_WINDOWS:
        return
    else:
        return importlib.import_module("tty")


@lazyobject
def _winapi():
    if ON_WINDOWS:
        import _winapi as m
    else:
        m = None
    return m


@lazyobject
def msvcrt():
    if ON_WINDOWS:
        import msvcrt as m
    else:
        m = None
    return m


@lazyobject
def winutils():
    if ON_WINDOWS:
        import xonsh.winutils as m
    else:
        m = None
    return m


@lazyobject
def macutils():
    if ON_DARWIN:
        import xonsh.macutils as m
    else:
        m = None
    return m


@lazyobject
def terminal256():
    return importlib.import_module("pygments.formatters.terminal256")

#
# parser
#
# -*- coding: utf-8 -*-
"""Implements the xonsh parser."""
# amalgamated xonsh.lazyasd
# amalgamated xonsh.platform
@lazyobject
def Parser():
    if PYTHON_VERSION_INFO > (3, 6):
        from xonsh.parsers.v36 import Parser as p
    elif PYTHON_VERSION_INFO > (3, 5):
        from xonsh.parsers.v35 import Parser as p
    else:
        from xonsh.parsers.v34 import Parser as p
    return p

#
# tokenize
#
"""Tokenization help for xonsh programs.

This file is a modified version of tokenize.py form the Python 3.4 and 3.5
standard libraries (licensed under the Python Software Foundation License,
version 2), which provides tokenization help for Python programs.

It is modified to properly tokenize xonsh code, including backtick regex
path and several xonsh-specific operators.

A few pieces of this file are specific to the version of Python being used.
To find these pieces, search the PY35.

Original file credits:
   __author__ = 'Ka-Ping Yee <ping@lfw.org>'
   __credits__ = ('GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, '
                  'Skip Montanaro, Raymond Hettinger, Trent Nelson, '
                  'Michael Foord')
"""

# amalgamated re
# amalgamated io
# amalgamated sys
codecs = _LazyModule.load('codecs', 'codecs')
# amalgamated builtins
itertools = _LazyModule.load('itertools', 'itertools')
# amalgamated collections
token = _LazyModule.load('token', 'token')
from token import (
    AMPER,
    AMPEREQUAL,
    AT,
    CIRCUMFLEX,
    CIRCUMFLEXEQUAL,
    COLON,
    COMMA,
    DEDENT,
    DOT,
    DOUBLESLASH,
    DOUBLESLASHEQUAL,
    DOUBLESTAR,
    DOUBLESTAREQUAL,
    ENDMARKER,
    EQEQUAL,
    EQUAL,
    ERRORTOKEN,
    GREATER,
    GREATEREQUAL,
    INDENT,
    LBRACE,
    LEFTSHIFT,
    LEFTSHIFTEQUAL,
    LESS,
    LESSEQUAL,
    LPAR,
    LSQB,
    MINEQUAL,
    MINUS,
    NAME,
    NEWLINE,
    NOTEQUAL,
    NUMBER,
    N_TOKENS,
    OP,
    PERCENT,
    PERCENTEQUAL,
    PLUS,
    PLUSEQUAL,
    RBRACE,
    RIGHTSHIFT,
    RIGHTSHIFTEQUAL,
    RPAR,
    RSQB,
    SEMI,
    SLASH,
    SLASHEQUAL,
    STAR,
    STAREQUAL,
    STRING,
    TILDE,
    VBAR,
    VBAREQUAL,
    tok_name,
)

# amalgamated xonsh.lazyasd
# amalgamated xonsh.platform
cookie_re = LazyObject(
    lambda: re.compile(r"^[ \t\f]*#.*coding[:=][ \t]*([-\w.]+)", re.ASCII),
    globals(),
    "cookie_re",
)
blank_re = LazyObject(
    lambda: re.compile(br"^[ \t\f]*(?:[#\r\n]|$)", re.ASCII), globals(), "blank_re"
)

#
# token modifications
#
tok_name = tok_name.copy()
__all__ = token.__all__ + [
    "COMMENT",
    "tokenize",
    "detect_encoding",
    "NL",
    "untokenize",
    "ENCODING",
    "TokenInfo",
    "TokenError",
    "SEARCHPATH",
    "ATDOLLAR",
    "ATEQUAL",
    "DOLLARNAME",
    "IOREDIRECT",
]
HAS_ASYNC = (3, 5, 0) <= PYTHON_VERSION_INFO < (3, 7, 0)
if HAS_ASYNC:
    ASYNC = token.ASYNC
    AWAIT = token.AWAIT
    ADDSPACE_TOKS = (NAME, NUMBER, ASYNC, AWAIT)
else:
    ADDSPACE_TOKS = (NAME, NUMBER)
del token  # must clean up token
PY35 = (3, 5, 0) <= PYTHON_VERSION_INFO
AUGASSIGN_OPS = r"[+\-*/%&@|^=<>]=?"
if not PY35:
    AUGASSIGN_OPS = AUGASSIGN_OPS.replace("@", "")


COMMENT = N_TOKENS
tok_name[COMMENT] = "COMMENT"
NL = N_TOKENS + 1
tok_name[NL] = "NL"
ENCODING = N_TOKENS + 2
tok_name[ENCODING] = "ENCODING"
N_TOKENS += 3
SEARCHPATH = N_TOKENS
tok_name[N_TOKENS] = "SEARCHPATH"
N_TOKENS += 1
IOREDIRECT = N_TOKENS
tok_name[N_TOKENS] = "IOREDIRECT"
N_TOKENS += 1
DOLLARNAME = N_TOKENS
tok_name[N_TOKENS] = "DOLLARNAME"
N_TOKENS += 1
ATDOLLAR = N_TOKENS
tok_name[N_TOKENS] = "ATDOLLAR"
N_TOKENS += 1
ATEQUAL = N_TOKENS
tok_name[N_TOKENS] = "ATEQUAL"
N_TOKENS += 1
_xonsh_tokens = {
    "?": "QUESTION",
    "@=": "ATEQUAL",
    "@$": "ATDOLLAR",
    "||": "DOUBLEPIPE",
    "&&": "DOUBLEAMPER",
    "@(": "ATLPAREN",
    "!(": "BANGLPAREN",
    "![": "BANGLBRACKET",
    "$(": "DOLLARLPAREN",
    "$[": "DOLLARLBRACKET",
    "${": "DOLLARLBRACE",
    "??": "DOUBLEQUESTION",
    "@$(": "ATDOLLARLPAREN",
}

additional_parenlevs = frozenset({"@(", "!(", "![", "$(", "$[", "${", "@$("})

_glbs = globals()
for v in _xonsh_tokens.values():
    _glbs[v] = N_TOKENS
    tok_name[N_TOKENS] = v
    N_TOKENS += 1
    __all__.append(v)
del _glbs, v

EXACT_TOKEN_TYPES = {
    "(": LPAR,
    ")": RPAR,
    "[": LSQB,
    "]": RSQB,
    ":": COLON,
    ",": COMMA,
    ";": SEMI,
    "+": PLUS,
    "-": MINUS,
    "*": STAR,
    "/": SLASH,
    "|": VBAR,
    "&": AMPER,
    "<": LESS,
    ">": GREATER,
    "=": EQUAL,
    ".": DOT,
    "%": PERCENT,
    "{": LBRACE,
    "}": RBRACE,
    "==": EQEQUAL,
    "!=": NOTEQUAL,
    "<=": LESSEQUAL,
    ">=": GREATEREQUAL,
    "~": TILDE,
    "^": CIRCUMFLEX,
    "<<": LEFTSHIFT,
    ">>": RIGHTSHIFT,
    "**": DOUBLESTAR,
    "+=": PLUSEQUAL,
    "-=": MINEQUAL,
    "*=": STAREQUAL,
    "/=": SLASHEQUAL,
    "%=": PERCENTEQUAL,
    "&=": AMPEREQUAL,
    "|=": VBAREQUAL,
    "^=": CIRCUMFLEXEQUAL,
    "<<=": LEFTSHIFTEQUAL,
    ">>=": RIGHTSHIFTEQUAL,
    "**=": DOUBLESTAREQUAL,
    "//": DOUBLESLASH,
    "//=": DOUBLESLASHEQUAL,
    "@": AT,
}

EXACT_TOKEN_TYPES.update(_xonsh_tokens)


class TokenInfo(collections.namedtuple("TokenInfo", "type string start end line")):
    def __repr__(self):
        annotated_type = "%d (%s)" % (self.type, tok_name[self.type])
        return (
            "TokenInfo(type=%s, string=%r, start=%r, end=%r, line=%r)"
            % self._replace(type=annotated_type)
        )

    @property
    def exact_type(self):
        if self.type == OP and self.string in EXACT_TOKEN_TYPES:
            return EXACT_TOKEN_TYPES[self.string]
        else:
            return self.type


def group(*choices):
    return "(" + "|".join(choices) + ")"


def tokany(*choices):
    return group(*choices) + "*"


def maybe(*choices):
    return group(*choices) + "?"


# Note: we use unicode matching for names ("\w") but ascii matching for
# number literals.
Whitespace = r"[ \f\t]*"
Comment = r"#[^\r\n]*"
Ignore = Whitespace + tokany(r"\\\r?\n" + Whitespace) + maybe(Comment)
Name_RE = r"\$?\w+"

Hexnumber = r"0[xX](?:_?[0-9a-fA-F])+"
Binnumber = r"0[bB](?:_?[01])+"
Octnumber = r"0[oO](?:_?[0-7])+"
Decnumber = r"(?:0(?:_?0)*|[1-9](?:_?[0-9])*)"
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = r"[eE][-+]?[0-9](?:_?[0-9])*"
Pointfloat = group(
    r"[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?", r"\.[0-9](?:_?[0-9])*"
) + maybe(Exponent)
Expfloat = r"[0-9](?:_?[0-9])*" + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group(r"[0-9](?:_?[0-9])*[jJ]", Floatnumber + r"[jJ]")
Number = group(Imagnumber, Floatnumber, Intnumber)

StringPrefix = r"(?:[bBp][rR]?|[rR][bBpfF]?|[uU]|[fF][rR]?)?"

# Tail end of ' string.
Single = r"[^'\\]*(?:\\.[^'\\]*)*'"
# Tail end of " string.
Double = r'[^"\\]*(?:\\.[^"\\]*)*"'
# Tail end of ''' string.
Single3 = r"[^'\\]*(?:(?:\\.|'(?!''))[^'\\]*)*'''"
# Tail end of """ string.
Double3 = r'[^"\\]*(?:(?:\\.|"(?!""))[^"\\]*)*"""'
Triple = group(StringPrefix + "'''", StringPrefix + '"""')
# Single-line ' or " string.
String = group(
    StringPrefix + r"'[^\n'\\]*(?:\\.[^\n'\\]*)*'",
    StringPrefix + r'"[^\n"\\]*(?:\\.[^\n"\\]*)*"',
)

# Xonsh-specific Syntax
SearchPath = r"((?:[rgp]+|@\w*)?)`([^\n`\\]*(?:\\.[^\n`\\]*)*)`"

# Because of leftmost-then-longest match semantics, be sure to put the
# longest operators first (e.g., if = came before ==, == would get
# recognized as two instances of =).
_redir_names = ("out", "all", "err", "e", "2", "a", "&", "1", "o")
_redir_map = (
    # stderr to stdout
    "err>out",
    "err>&1",
    "2>out",
    "err>o",
    "err>1",
    "e>out",
    "e>&1",
    "2>&1",
    "e>o",
    "2>o",
    "e>1",
    "2>1",
    # stdout to stderr
    "out>err",
    "out>&2",
    "1>err",
    "out>e",
    "out>2",
    "o>err",
    "o>&2",
    "1>&2",
    "o>e",
    "1>e",
    "o>2",
    "1>2",
)
IORedirect = group(group(*_redir_map), "{}>>?".format(group(*_redir_names)))
_redir_check = set(_redir_map)
_redir_check = {"{}>".format(i) for i in _redir_names}.union(_redir_check)
_redir_check = {"{}>>".format(i) for i in _redir_names}.union(_redir_check)
_redir_check = frozenset(_redir_check)
Operator = group(
    r"\*\*=?",
    r">>=?",
    r"<<=?",
    r"!=",
    r"//=?",
    r"->",
    r"@\$\(?",
    r"\|\|",
    "&&",
    r"@\(",
    r"!\(",
    r"!\[",
    r"\$\(",
    r"\$\[",
    r"\${",
    r"\?\?",
    r"\?",
    AUGASSIGN_OPS,
    r"~",
)

Bracket = "[][(){}]"
Special = group(r"\r?\n", r"\.\.\.", r"[:;.,@]")
Funny = group(Operator, Bracket, Special)

PlainToken = group(IORedirect, Number, Funny, String, Name_RE, SearchPath)

# First (or only) line of ' or " string.
ContStr = group(
    StringPrefix + r"'[^\n'\\]*(?:\\.[^\n'\\]*)*" + group("'", r"\\\r?\n"),
    StringPrefix + r'"[^\n"\\]*(?:\\.[^\n"\\]*)*' + group('"', r"\\\r?\n"),
)
PseudoExtras = group(r"\\\r?\n|\Z", Comment, Triple, SearchPath)
PseudoToken = Whitespace + group(
    PseudoExtras, IORedirect, Number, Funny, ContStr, Name_RE
)


def _compile(expr):
    return re.compile(expr, re.UNICODE)


endpats = {
    "'": Single,
    '"': Double,
    "'''": Single3,
    '"""': Double3,
    "r'''": Single3,
    'r"""': Double3,
    "b'''": Single3,
    'b"""': Double3,
    "f'''": Single3,
    'f"""': Double3,
    "R'''": Single3,
    'R"""': Double3,
    "B'''": Single3,
    'B"""': Double3,
    "F'''": Single3,
    'F"""': Double3,
    "br'''": Single3,
    'br"""': Double3,
    "fr'''": Single3,
    'fr"""': Double3,
    "bR'''": Single3,
    'bR"""': Double3,
    "Br'''": Single3,
    'Br"""': Double3,
    "BR'''": Single3,
    'BR"""': Double3,
    "rb'''": Single3,
    'rb"""': Double3,
    "rf'''": Single3,
    'rf"""': Double3,
    "Rb'''": Single3,
    'Rb"""': Double3,
    "Fr'''": Single3,
    'Fr"""': Double3,
    "rB'''": Single3,
    'rB"""': Double3,
    "rF'''": Single3,
    'rF"""': Double3,
    "RB'''": Single3,
    'RB"""': Double3,
    "RF'''": Single3,
    'RF"""': Double3,
    "u'''": Single3,
    'u"""': Double3,
    "U'''": Single3,
    'U"""': Double3,
    "p'''": Single3,
    'p"""': Double3,
    "pr'''": Single3,
    'pr"""': Double3,
    "pR'''": Single3,
    'pR"""': Double3,
    "rp'''": Single3,
    'rp"""': Double3,
    "Rp'''": Single3,
    'Rp"""': Double3,
    "r": None,
    "R": None,
    "b": None,
    "B": None,
    "u": None,
    "U": None,
    "p": None,
    "f": None,
    "F": None,
}

triple_quoted = {}
for t in (
    "'''",
    '"""',
    "r'''",
    'r"""',
    "R'''",
    'R"""',
    "b'''",
    'b"""',
    "B'''",
    'B"""',
    "f'''",
    'f"""',
    "F'''",
    'F"""',
    "br'''",
    'br"""',
    "Br'''",
    'Br"""',
    "bR'''",
    'bR"""',
    "BR'''",
    'BR"""',
    "rb'''",
    'rb"""',
    "rB'''",
    'rB"""',
    "Rb'''",
    'Rb"""',
    "RB'''",
    'RB"""',
    "fr'''",
    'fr"""',
    "Fr'''",
    'Fr"""',
    "fR'''",
    'fR"""',
    "FR'''",
    'FR"""',
    "rf'''",
    'rf"""',
    "rF'''",
    'rF"""',
    "Rf'''",
    'Rf"""',
    "RF'''",
    'RF"""',
    "u'''",
    'u"""',
    "U'''",
    'U"""',
    "p'''",
    'p""""',
    "pr'''",
    'pr""""',
    "pR'''",
    'pR""""',
    "rp'''",
    'rp""""',
    "Rp'''",
    'Rp""""',
):
    triple_quoted[t] = t
single_quoted = {}
for t in (
    "'",
    '"',
    "r'",
    'r"',
    "R'",
    'R"',
    "b'",
    'b"',
    "B'",
    'B"',
    "f'",
    'f"',
    "F'",
    'F"',
    "br'",
    'br"',
    "Br'",
    'Br"',
    "bR'",
    'bR"',
    "BR'",
    'BR"',
    "rb'",
    'rb"',
    "rB'",
    'rB"',
    "Rb'",
    'Rb"',
    "RB'",
    'RB"',
    "fr'",
    'fr"',
    "Fr'",
    'Fr"',
    "fR'",
    'fR"',
    "FR'",
    'FR"',
    "rf'",
    'rf"',
    "rF'",
    'rF"',
    "Rf'",
    'Rf"',
    "RF'",
    'RF"',
    "u'",
    'u"',
    "U'",
    'U"',
    "p'",
    'p"',
    "pr'",
    'pr"',
    "pR'",
    'pR"',
    "rp'",
    'rp"',
    "Rp'",
    'Rp"',
):
    single_quoted[t] = t

tabsize = 8


class TokenError(Exception):
    pass


class StopTokenizing(Exception):
    pass


class Untokenizer:
    def __init__(self):
        self.tokens = []
        self.prev_row = 1
        self.prev_col = 0
        self.encoding = None

    def add_whitespace(self, start):
        row, col = start
        if row < self.prev_row or row == self.prev_row and col < self.prev_col:
            raise ValueError(
                "start ({},{}) precedes previous end ({},{})".format(
                    row, col, self.prev_row, self.prev_col
                )
            )
        row_offset = row - self.prev_row
        if row_offset:
            self.tokens.append("\\\n" * row_offset)
            self.prev_col = 0
        col_offset = col - self.prev_col
        if col_offset:
            self.tokens.append(" " * col_offset)

    def untokenize(self, iterable):
        it = iter(iterable)
        indents = []
        startline = False
        for t in it:
            if len(t) == 2:
                self.compat(t, it)
                break
            tok_type, token, start, end, line = t
            if tok_type == ENCODING:
                self.encoding = token
                continue
            if tok_type == ENDMARKER:
                break
            if tok_type == INDENT:
                indents.append(token)
                continue
            elif tok_type == DEDENT:
                indents.pop()
                self.prev_row, self.prev_col = end
                continue
            elif tok_type in (NEWLINE, NL):
                startline = True
            elif startline and indents:
                indent = indents[-1]
                if start[1] >= len(indent):
                    self.tokens.append(indent)
                    self.prev_col = len(indent)
                startline = False
            self.add_whitespace(start)
            self.tokens.append(token)
            self.prev_row, self.prev_col = end
            if tok_type in (NEWLINE, NL):
                self.prev_row += 1
                self.prev_col = 0
        return "".join(self.tokens)

    def compat(self, token, iterable):
        indents = []
        toks_append = self.tokens.append
        startline = token[0] in (NEWLINE, NL)
        prevstring = False

        for tok in itertools.chain([token], iterable):
            toknum, tokval = tok[:2]
            if toknum == ENCODING:
                self.encoding = tokval
                continue

            if toknum in ADDSPACE_TOKS:
                tokval += " "

            # Insert a space between two consecutive strings
            if toknum == STRING:
                if prevstring:
                    tokval = " " + tokval
                prevstring = True
            else:
                prevstring = False

            if toknum == INDENT:
                indents.append(tokval)
                continue
            elif toknum == DEDENT:
                indents.pop()
                continue
            elif toknum in (NEWLINE, NL):
                startline = True
            elif startline and indents:
                toks_append(indents[-1])
                startline = False
            toks_append(tokval)


def untokenize(iterable):
    """Transform tokens back into Python source code.
    It returns a bytes object, encoded using the ENCODING
    token, which is the first token sequence output by tokenize.

    Each element returned by the iterable must be a token sequence
    with at least two elements, a token number and token value.  If
    only two tokens are passed, the resulting output is poor.

    Round-trip invariant for full input:
        Untokenized source will match input source exactly

    Round-trip invariant for limited intput:
        # Output bytes will tokenize the back to the input
        t1 = [tok[:2] for tok in tokenize(f.readline)]
        newcode = untokenize(t1)
        readline = BytesIO(newcode).readline
        t2 = [tok[:2] for tok in tokenize(readline)]
        assert t1 == t2
    """
    ut = Untokenizer()
    out = ut.untokenize(iterable)
    if ut.encoding is not None:
        out = out.encode(ut.encoding)
    return out


def _get_normal_name(orig_enc):
    """Imitates get_normal_name in tokenizer.c."""
    # Only care about the first 12 characters.
    enc = orig_enc[:12].lower().replace("_", "-")
    if enc == "utf-8" or enc.startswith("utf-8-"):
        return "utf-8"
    if enc in ("latin-1", "iso-8859-1", "iso-latin-1") or enc.startswith(
        ("latin-1-", "iso-8859-1-", "iso-latin-1-")
    ):
        return "iso-8859-1"
    return orig_enc


def detect_encoding(readline):
    """
    The detect_encoding() function is used to detect the encoding that should
    be used to decode a Python source file.  It requires one argument, readline,
    in the same way as the tokenize() generator.

    It will call readline a maximum of twice, and return the encoding used
    (as a string) and a list of any lines (left as bytes) it has read in.

    It detects the encoding from the presence of a utf-8 bom or an encoding
    cookie as specified in pep-0263.  If both a bom and a cookie are present,
    but disagree, a SyntaxError will be raised.  If the encoding cookie is an
    invalid charset, raise a SyntaxError.  Note that if a utf-8 bom is found,
    'utf-8-sig' is returned.

    If no encoding is specified, then the default of 'utf-8' will be returned.
    """
    try:
        filename = readline.__self__.name
    except AttributeError:
        filename = None
    bom_found = False
    encoding = None
    default = "utf-8"

    def read_or_stop():
        try:
            return readline()
        except StopIteration:
            return b""

    def find_cookie(line):
        try:
            # Decode as UTF-8. Either the line is an encoding declaration,
            # in which case it should be pure ASCII, or it must be UTF-8
            # per default encoding.
            line_string = line.decode("utf-8")
        except UnicodeDecodeError:
            msg = "invalid or missing encoding declaration"
            if filename is not None:
                msg = "{} for {!r}".format(msg, filename)
            raise SyntaxError(msg)

        match = cookie_re.match(line_string)
        if not match:
            return None
        encoding = _get_normal_name(match.group(1))
        try:
            codecs.lookup(encoding)
        except LookupError:
            # This behaviour mimics the Python interpreter
            if filename is None:
                msg = "unknown encoding: " + encoding
            else:
                msg = "unknown encoding for {!r}: {}".format(filename, encoding)
            raise SyntaxError(msg)

        if bom_found:
            if encoding != "utf-8":
                # This behaviour mimics the Python interpreter
                if filename is None:
                    msg = "encoding problem: utf-8"
                else:
                    msg = "encoding problem for {!r}: utf-8".format(filename)
                raise SyntaxError(msg)
            encoding += "-sig"
        return encoding

    first = read_or_stop()
    if first.startswith(codecs.BOM_UTF8):
        bom_found = True
        first = first[3:]
        default = "utf-8-sig"
    if not first:
        return default, []

    encoding = find_cookie(first)
    if encoding:
        return encoding, [first]
    if not blank_re.match(first):
        return default, [first]

    second = read_or_stop()
    if not second:
        return default, [first]

    encoding = find_cookie(second)
    if encoding:
        return encoding, [first, second]

    return default, [first, second]


def tokopen(filename):
    """Open a file in read only mode using the encoding detected by
    detect_encoding().
    """
    buffer = builtins.open(filename, "rb")
    try:
        encoding, lines = detect_encoding(buffer.readline)
        buffer.seek(0)
        text = io.TextIOWrapper(buffer, encoding, line_buffering=True)
        text.mode = "r"
        return text
    except Exception:
        buffer.close()
        raise


def _tokenize(readline, encoding):
    lnum = parenlev = continued = 0
    numchars = "0123456789"
    contstr, needcont = "", 0
    contline = None
    indents = [0]

    # 'stashed' and 'async_*' are used for async/await parsing
    stashed = None
    async_def = False
    async_def_indent = 0
    async_def_nl = False

    if encoding is not None:
        if encoding == "utf-8-sig":
            # BOM will already have been stripped.
            encoding = "utf-8"
        yield TokenInfo(ENCODING, encoding, (0, 0), (0, 0), "")
    while True:  # loop over lines in stream
        try:
            line = readline()
        except StopIteration:
            line = b""

        if encoding is not None:
            line = line.decode(encoding)
        lnum += 1
        pos, max = 0, len(line)

        if contstr:  # continued string
            if not line:
                raise TokenError("EOF in multi-line string", strstart)
            endmatch = endprog.match(line)
            if endmatch:
                pos = end = endmatch.end(0)
                yield TokenInfo(
                    STRING, contstr + line[:end], strstart, (lnum, end), contline + line
                )
                contstr, needcont = "", 0
                contline = None
            elif needcont and line[-2:] != "\\\n" and line[-3:] != "\\\r\n":
                yield TokenInfo(
                    ERRORTOKEN, contstr + line, strstart, (lnum, len(line)), contline
                )
                contstr = ""
                contline = None
                continue
            else:
                contstr = contstr + line
                contline = contline + line
                continue

        elif parenlev == 0 and not continued:  # new statement
            if not line:
                break
            column = 0
            while pos < max:  # measure leading whitespace
                if line[pos] == " ":
                    column += 1
                elif line[pos] == "\t":
                    column = (column // tabsize + 1) * tabsize
                elif line[pos] == "\f":
                    column = 0
                else:
                    break
                pos += 1
            if pos == max:
                break

            if line[pos] in "#\r\n":  # skip comments or blank lines
                if line[pos] == "#":
                    comment_token = line[pos:].rstrip("\r\n")
                    nl_pos = pos + len(comment_token)
                    yield TokenInfo(
                        COMMENT,
                        comment_token,
                        (lnum, pos),
                        (lnum, pos + len(comment_token)),
                        line,
                    )
                    yield TokenInfo(
                        NL, line[nl_pos:], (lnum, nl_pos), (lnum, len(line)), line
                    )
                else:
                    yield TokenInfo(
                        (NL, COMMENT)[line[pos] == "#"],
                        line[pos:],
                        (lnum, pos),
                        (lnum, len(line)),
                        line,
                    )
                continue

            if column > indents[-1]:  # count indents or dedents
                indents.append(column)
                yield TokenInfo(INDENT, line[:pos], (lnum, 0), (lnum, pos), line)
            while column < indents[-1]:
                if column not in indents:
                    raise IndentationError(
                        "unindent does not match any outer indentation level",
                        ("<tokenize>", lnum, pos, line),
                    )
                indents = indents[:-1]

                if async_def and async_def_indent >= indents[-1]:
                    async_def = False
                    async_def_nl = False
                    async_def_indent = 0

                yield TokenInfo(DEDENT, "", (lnum, pos), (lnum, pos), line)

            if async_def and async_def_nl and async_def_indent >= indents[-1]:
                async_def = False
                async_def_nl = False
                async_def_indent = 0

        else:  # continued statement
            if not line:
                raise TokenError("EOF in multi-line statement", (lnum, 0))
            continued = 0

        while pos < max:
            pseudomatch = _compile(PseudoToken).match(line, pos)
            if pseudomatch:  # scan for tokens
                start, end = pseudomatch.span(1)
                spos, epos, pos = (lnum, start), (lnum, end), end
                if start == end:
                    continue
                token, initial = line[start:end], line[start]

                if token in _redir_check:
                    yield TokenInfo(IOREDIRECT, token, spos, epos, line)
                elif initial in numchars or (  # ordinary number
                    initial == "." and token != "." and token != "..."
                ):
                    yield TokenInfo(NUMBER, token, spos, epos, line)
                elif initial in "\r\n":
                    if stashed:
                        yield stashed
                        stashed = None
                    if parenlev > 0:
                        yield TokenInfo(NL, token, spos, epos, line)
                    else:
                        yield TokenInfo(NEWLINE, token, spos, epos, line)
                        if async_def:
                            async_def_nl = True

                elif initial == "#":
                    assert not token.endswith("\n")
                    if stashed:
                        yield stashed
                        stashed = None
                    yield TokenInfo(COMMENT, token, spos, epos, line)
                # Xonsh-specific Regex Globbing
                elif re.match(SearchPath, token):
                    yield TokenInfo(SEARCHPATH, token, spos, epos, line)
                elif token in triple_quoted:
                    endprog = _compile(endpats[token])
                    endmatch = endprog.match(line, pos)
                    if endmatch:  # all on one line
                        pos = endmatch.end(0)
                        token = line[start:pos]
                        yield TokenInfo(STRING, token, spos, (lnum, pos), line)
                    else:
                        strstart = (lnum, start)  # multiple lines
                        contstr = line[start:]
                        contline = line
                        break
                elif (
                    initial in single_quoted
                    or token[:2] in single_quoted
                    or token[:3] in single_quoted
                ):
                    if token[-1] == "\n":  # continued string
                        strstart = (lnum, start)
                        endprog = _compile(
                            endpats[initial] or endpats[token[1]] or endpats[token[2]]
                        )
                        contstr, needcont = line[start:], 1
                        contline = line
                        break
                    else:  # ordinary string
                        yield TokenInfo(STRING, token, spos, epos, line)
                elif token.startswith("$") and token[1:].isidentifier():
                    yield TokenInfo(DOLLARNAME, token, spos, epos, line)
                elif initial.isidentifier():  # ordinary name
                    if token in ("async", "await"):
                        if async_def:
                            yield TokenInfo(
                                ASYNC if token == "async" else AWAIT,
                                token,
                                spos,
                                epos,
                                line,
                            )
                            continue

                    tok = TokenInfo(NAME, token, spos, epos, line)
                    if token == "async" and not stashed:
                        stashed = tok
                        continue

                    if (
                        HAS_ASYNC
                        and token == "def"
                        and (
                            stashed
                            and stashed.type == NAME
                            and stashed.string == "async"
                        )
                    ):
                        async_def = True
                        async_def_indent = indents[-1]

                        yield TokenInfo(
                            ASYNC,
                            stashed.string,
                            stashed.start,
                            stashed.end,
                            stashed.line,
                        )
                        stashed = None

                    if stashed:
                        yield stashed
                        stashed = None

                    yield tok
                elif token == "\\\n" or token == "\\\r\n":  # continued stmt
                    continued = 1
                    yield TokenInfo(ERRORTOKEN, token, spos, epos, line)
                elif initial == "\\":  # continued stmt
                    # for cases like C:\\path\\to\\file
                    continued = 1
                else:
                    if initial in "([{":
                        parenlev += 1
                    elif initial in ")]}":
                        parenlev -= 1
                    elif token in additional_parenlevs:
                        parenlev += 1
                    if stashed:
                        yield stashed
                        stashed = None
                    yield TokenInfo(OP, token, spos, epos, line)
            else:
                yield TokenInfo(
                    ERRORTOKEN, line[pos], (lnum, pos), (lnum, pos + 1), line
                )
                pos += 1

    if stashed:
        yield stashed
        stashed = None

    for indent in indents[1:]:  # pop remaining indent levels
        yield TokenInfo(DEDENT, "", (lnum, 0), (lnum, 0), "")
    yield TokenInfo(ENDMARKER, "", (lnum, 0), (lnum, 0), "")


def tokenize(readline):
    """
    The tokenize() generator requires one argument, readline, which
    must be a callable object which provides the same interface as the
    readline() method of built-in file objects.  Each call to the function
    should return one line of input as bytes.  Alternately, readline
    can be a callable function terminating with StopIteration:
        readline = open(myfile, 'rb').__next__  # Example of alternate readline

    The generator produces 5-tuples with these members: the token type; the
    token string; a 2-tuple (srow, scol) of ints specifying the row and
    column where the token begins in the source; a 2-tuple (erow, ecol) of
    ints specifying the row and column where the token ends in the source;
    and the line on which the token was found.  The line passed is the
    logical line; continuation lines are included.

    The first token sequence will always be an ENCODING token
    which tells you which encoding was used to decode the bytes stream.
    """
    encoding, consumed = detect_encoding(readline)
    rl_gen = iter(readline, b"")
    empty = itertools.repeat(b"")
    return _tokenize(itertools.chain(consumed, rl_gen, empty).__next__, encoding)


# An undocumented, backwards compatible, API for all the places in the standard
# library that expect to be able to use tokenize with strings
def generate_tokens(readline):
    return _tokenize(readline, None)


def tokenize_main():
    import argparse

    # Helper error handling routines
    def perror(message):
        print(message, file=sys.stderr)

    def error(message, filename=None, location=None):
        if location:
            args = (filename,) + location + (message,)
            perror("%s:%d:%d: error: %s" % args)
        elif filename:
            perror("%s: error: %s" % (filename, message))
        else:
            perror("error: %s" % message)
        sys.exit(1)

    # Parse the arguments and options
    parser = argparse.ArgumentParser(prog="python -m tokenize")
    parser.add_argument(
        dest="filename",
        nargs="?",
        metavar="filename.py",
        help="the file to tokenize; defaults to stdin",
    )
    parser.add_argument(
        "-e",
        "--exact",
        dest="exact",
        action="store_true",
        help="display token names using the exact type",
    )
    args = parser.parse_args()

    try:
        # Tokenize the input
        if args.filename:
            filename = args.filename
            with builtins.open(filename, "rb") as f:
                tokens = list(tokenize(f.readline))
        else:
            filename = "<stdin>"
            tokens = _tokenize(sys.stdin.readline, None)

        # Output the tokenization
        for token in tokens:
            token_type = token.type
            if args.exact:
                token_type = token.exact_type
            token_range = "%d,%d-%d,%d:" % (token.start + token.end)
            print("%-20s%-15s%-15r" % (token_range, tok_name[token_type], token.string))
    except IndentationError as err:
        line, column = err.args[1][1:3]
        error(err.args[0], filename, (line, column))
    except TokenError as err:
        line, column = err.args[1]
        error(err.args[0], filename, (line, column))
    except SyntaxError as err:
        error(err, filename)
    except OSError as err:
        error(err)
    except KeyboardInterrupt:
        print("interrupted\n")
    except Exception as err:
        perror("unexpected error: %s" % err)
        raise

#
# tools
#
# -*- coding: utf-8 -*-
"""Misc. xonsh tools.

The following implementations were forked from the IPython project:

* Copyright (c) 2008-2014, IPython Development Team
* Copyright (C) 2001-2007 Fernando Perez <fperez@colorado.edu>
* Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
* Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>

Implementations:

* decode()
* encode()
* cast_unicode()
* safe_hasattr()
* indent()

"""
# amalgamated builtins
# amalgamated collections
# amalgamated collections.abc
# amalgamated contextlib
# amalgamated ctypes
# amalgamated datetime
from distutils.version import LooseVersion
# amalgamated functools
glob = _LazyModule.load('glob', 'glob')
# amalgamated itertools
# amalgamated os
# amalgamated pathlib
# amalgamated re
# amalgamated subprocess
# amalgamated sys
# amalgamated threading
traceback = _LazyModule.load('traceback', 'traceback')
warnings = _LazyModule.load('warnings', 'warnings')
operator = _LazyModule.load('operator', 'operator')
ast = _LazyModule.load('ast', 'ast')
string = _LazyModule.load('string', 'string')
from xonsh import __version__
# amalgamated xonsh.lazyasd
# amalgamated xonsh.platform
@functools.lru_cache(1)
def is_superuser():
    if ON_WINDOWS:
        rtn = ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        rtn = os.getuid() == 0
    return rtn


class XonshError(Exception):
    pass


class XonshCalledProcessError(XonshError, subprocess.CalledProcessError):
    """Raised when there's an error with a called process

    Inherits from XonshError and subprocess.CalledProcessError, catching
    either will also catch this error.

    Raised *after* iterating over stdout of a captured command, if the
    returncode of the command is nonzero.

    Example:
        try:
            for line in !(ls):
                print(line)
        except subprocess.CalledProcessError as error:
            print("Error in process: {}.format(error.completed_command.pid))

    This also handles differences between Python3.4 and 3.5 where
    CalledProcessError is concerned.
    """

    def __init__(
        self, returncode, command, output=None, stderr=None, completed_command=None
    ):
        super().__init__(returncode, command, output)
        self.stderr = stderr
        self.completed_command = completed_command


def expand_path(s, expand_user=True):
    """Takes a string path and expands ~ to home if expand_user is set
    and environment vars if EXPAND_ENV_VARS is set."""
    session = getattr(builtins, "__xonsh__", None)
    env = os_environ if session is None else getattr(session, "env", os_environ)
    if env.get("EXPAND_ENV_VARS", False):
        s = expandvars(s)
    if expand_user:
        # expand ~ according to Bash unquoted rules "Each variable assignment is
        # checked for unquoted tilde-prefixes immediately following a ':' or the
        # first '='". See the following for more details.
        # https://www.gnu.org/software/bash/manual/html_node/Tilde-Expansion.html
        pre, char, post = s.partition("=")
        if char:
            s = expanduser(pre) + char
            s += os.pathsep.join(map(expanduser, post.split(os.pathsep)))
        else:
            s = expanduser(s)
    return s


def _expandpath(path):
    """Performs environment variable / user expansion on a given path
    if EXPAND_ENV_VARS is set.
    """
    session = getattr(builtins, "__xonsh__", None)
    env = os_environ if session is None else getattr(session, "env", os_environ)
    expand_user = env.get("EXPAND_ENV_VARS", False)
    return expand_path(path, expand_user=expand_user)


def decode_bytes(b):
    """Tries to decode the bytes using XONSH_ENCODING if available,
    otherwise using sys.getdefaultencoding().
    """
    session = getattr(builtins, "__xonsh__", None)
    env = os_environ if session is None else getattr(session, "env", os_environ)
    enc = env.get("XONSH_ENCODING") or DEFAULT_ENCODING
    err = env.get("XONSH_ENCODING_ERRORS") or "strict"
    return b.decode(encoding=enc, errors=err)


def findfirst(s, substrs):
    """Finds whichever of the given substrings occurs first in the given string
    and returns that substring, or returns None if no such strings occur.
    """
    i = len(s)
    result = None
    for substr in substrs:
        pos = s.find(substr)
        if -1 < pos < i:
            i = pos
            result = substr
    return i, result


class EnvPath(cabc.MutableSequence):
    """A class that implements an environment path, which is a list of
    strings. Provides a custom method that expands all paths if the
    relevant env variable has been set.
    """

    def __init__(self, args=None):
        if not args:
            self._l = []
        else:
            if isinstance(args, str):
                self._l = args.split(os.pathsep)
            elif isinstance(args, pathlib.Path):
                self._l = [args]
            elif isinstance(args, bytes):
                # decode bytes to a string and then split based on
                # the default path separator
                self._l = decode_bytes(args).split(os.pathsep)
            elif isinstance(args, cabc.Iterable):
                # put everything in a list -before- performing the type check
                # in order to be able to retrieve it later, for cases such as
                # when a generator expression was passed as an argument
                args = list(args)
                if not all(isinstance(i, (str, bytes, pathlib.Path)) for i in args):
                    # make TypeError's message as informative as possible
                    # when given an invalid initialization sequence
                    raise TypeError(
                        "EnvPath's initialization sequence should only "
                        "contain str, bytes and pathlib.Path entries"
                    )
                self._l = args
            else:
                raise TypeError(
                    "EnvPath cannot be initialized with items "
                    "of type %s" % type(args)
                )

    def __getitem__(self, item):
        # handle slices separately
        if isinstance(item, slice):
            return [_expandpath(i) for i in self._l[item]]
        else:
            return _expandpath(self._l[item])

    def __setitem__(self, index, item):
        self._l.__setitem__(index, item)

    def __len__(self):
        return len(self._l)

    def __delitem__(self, key):
        self._l.__delitem__(key)

    def insert(self, index, value):
        self._l.insert(index, value)

    @property
    def paths(self):
        """
        Returns the list of directories that this EnvPath contains.
        """
        return list(self)

    def __repr__(self):
        return repr(self._l)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        return all(map(operator.eq, self, other))

    def _repr_pretty_(self, p, cycle):
        """ Pretty print path list """
        if cycle:
            p.text("EnvPath(...)")
        else:
            with p.group(1, "EnvPath(\n[", "]\n)"):
                for idx, item in enumerate(self):
                    if idx:
                        p.text(",")
                        p.breakable()
                    p.pretty(item)

    def __add__(self, other):
        if isinstance(other, EnvPath):
            other = other._l
        return EnvPath(self._l + other)

    def __radd__(self, other):
        if isinstance(other, EnvPath):
            other = other._l
        return EnvPath(other + self._l)

    def add(self, data, front=False, replace=False):
        """Add a value to this EnvPath,

        path.add(data, front=bool, replace=bool) -> ensures that path contains data, with position determined by kwargs

        Parameters
        ----------
        data : string or bytes or pathlib.Path
            value to be added
        front : bool
            whether the value should be added to the front, will be
            ignored if the data already exists in this EnvPath and
            replace is False
            Default : False
        replace : bool
            If True, the value will be removed and added to the
            start or end(depending on the value of front)
            Default : False

        Returns
        -------
        None

        """
        if data not in self._l:
            self._l.insert(0 if front else len(self._l), data)
        elif replace:
            self._l.remove(data)
            self._l.insert(0 if front else len(self._l), data)


@lazyobject
def FORMATTER():
    return string.Formatter()


class DefaultNotGivenType(object):
    """Singleton for representing when no default value is given."""

    __inst = None

    def __new__(cls):
        if DefaultNotGivenType.__inst is None:
            DefaultNotGivenType.__inst = object.__new__(cls)
        return DefaultNotGivenType.__inst


DefaultNotGiven = DefaultNotGivenType()

BEG_TOK_SKIPS = LazyObject(
    lambda: frozenset(["WS", "INDENT", "NOT", "LPAREN"]), globals(), "BEG_TOK_SKIPS"
)
END_TOK_TYPES = LazyObject(
    lambda: frozenset(["SEMI", "AND", "OR", "RPAREN"]), globals(), "END_TOK_TYPES"
)
RE_END_TOKS = LazyObject(
    lambda: re.compile(r"(;|and|\&\&|or|\|\||\))"), globals(), "RE_END_TOKS"
)
LPARENS = LazyObject(
    lambda: frozenset(
        ["LPAREN", "AT_LPAREN", "BANG_LPAREN", "DOLLAR_LPAREN", "ATDOLLAR_LPAREN"]
    ),
    globals(),
    "LPARENS",
)


def _is_not_lparen_and_rparen(lparens, rtok):
    """Tests if an RPAREN token is matched with something other than a plain old
    LPAREN type.
    """
    # note that any([]) is False, so this covers len(lparens) == 0
    return rtok.type == "RPAREN" and any(x != "LPAREN" for x in lparens)


def balanced_parens(line, mincol=0, maxcol=None, lexer=None):
    """Determines if parentheses are balanced in an expression."""
    line = line[mincol:maxcol]
    if lexer is None:
        lexer = builtins.__xonsh__.execer.parser.lexer
    if "(" not in line and ")" not in line:
        return True
    cnt = 0
    lexer.input(line)
    for tok in lexer:
        if tok.type in LPARENS:
            cnt += 1
        elif tok.type == "RPAREN":
            cnt -= 1
        elif tok.type == "ERRORTOKEN" and ")" in tok.value:
            cnt -= 1
    return cnt == 0


def find_next_break(line, mincol=0, lexer=None):
    """Returns the column number of the next logical break in subproc mode.
    This function may be useful in finding the maxcol argument of
    subproc_toks().
    """
    if mincol >= 1:
        line = line[mincol:]
    if lexer is None:
        lexer = builtins.__xonsh__.execer.parser.lexer
    if RE_END_TOKS.search(line) is None:
        return None
    maxcol = None
    lparens = []
    lexer.input(line)
    for tok in lexer:
        if tok.type in LPARENS:
            lparens.append(tok.type)
        elif tok.type in END_TOK_TYPES:
            if _is_not_lparen_and_rparen(lparens, tok):
                lparens.pop()
            else:
                maxcol = tok.lexpos + mincol + 1
                break
        elif tok.type == "ERRORTOKEN" and ")" in tok.value:
            maxcol = tok.lexpos + mincol + 1
            break
        elif tok.type == "BANG":
            maxcol = mincol + len(line) + 1
            break
    return maxcol


def _offset_from_prev_lines(line, last):
    lines = line.splitlines(keepends=True)[:last]
    return sum(map(len, lines))


def subproc_toks(
    line, mincol=-1, maxcol=None, lexer=None, returnline=False, greedy=False
):
    """Encapsulates tokens in a source code line in a uncaptured
    subprocess ![] starting at a minimum column. If there are no tokens
    (ie in a comment line) this returns None. If greedy is True, it will encapsulate
    normal parentheses. Greedy is False by default.
    """
    if lexer is None:
        lexer = builtins.__xonsh__.execer.parser.lexer
    if maxcol is None:
        maxcol = len(line) + 1
    lexer.reset()
    lexer.input(line)
    toks = []
    lparens = []
    saw_macro = False
    end_offset = 0
    for tok in lexer:
        pos = tok.lexpos
        if tok.type not in END_TOK_TYPES and pos >= maxcol:
            break
        if tok.type == "BANG":
            saw_macro = True
        if saw_macro and tok.type not in ("NEWLINE", "DEDENT"):
            toks.append(tok)
            continue
        if tok.type in LPARENS:
            lparens.append(tok.type)
        if greedy and len(lparens) > 0 and "LPAREN" in lparens:
            toks.append(tok)
            if tok.type == "RPAREN":
                lparens.pop()
            continue
        if len(toks) == 0 and tok.type in BEG_TOK_SKIPS:
            continue  # handle indentation
        elif len(toks) > 0 and toks[-1].type in END_TOK_TYPES:
            if _is_not_lparen_and_rparen(lparens, toks[-1]):
                lparens.pop()  # don't continue or break
            elif pos < maxcol and tok.type not in ("NEWLINE", "DEDENT", "WS"):
                if not greedy:
                    toks.clear()
                if tok.type in BEG_TOK_SKIPS:
                    continue
            else:
                break
        if pos < mincol:
            continue
        toks.append(tok)
        if tok.type == "WS" and tok.value == "\\":
            pass  # line continuation
        elif tok.type == "NEWLINE":
            break
        elif tok.type == "DEDENT":
            # fake a newline when dedenting without a newline
            tok.type = "NEWLINE"
            tok.value = "\n"
            tok.lineno -= 1
            if len(toks) >= 2:
                prev_tok_end = toks[-2].lexpos + len(toks[-2].value)
            else:
                prev_tok_end = len(line)
            if "#" in line[prev_tok_end:]:
                tok.lexpos = prev_tok_end  # prevents wrapping comments
            else:
                tok.lexpos = len(line)
            break
        elif check_bad_str_token(tok):
            return
    else:
        if len(toks) > 0 and toks[-1].type in END_TOK_TYPES:
            if _is_not_lparen_and_rparen(lparens, toks[-1]):
                pass
            elif greedy and toks[-1].type == "RPAREN":
                pass
            else:
                toks.pop()
        if len(toks) == 0:
            return  # handle comment lines
        tok = toks[-1]
        pos = tok.lexpos
        if isinstance(tok.value, str):
            end_offset = len(tok.value.rstrip())
        else:
            el = line[pos:].split("#")[0].rstrip()
            end_offset = len(el)
    if len(toks) == 0:
        return  # handle comment lines
    elif saw_macro or greedy:
        end_offset = len(toks[-1].value.rstrip()) + 1
    if toks[0].lineno != toks[-1].lineno:
        # handle multiline cases
        end_offset += _offset_from_prev_lines(line, toks[-1].lineno)
    beg, end = toks[0].lexpos, (toks[-1].lexpos + end_offset)
    end = len(line[:end].rstrip())
    rtn = "![" + line[beg:end] + "]"
    if returnline:
        rtn = line[:beg] + rtn + line[end:]
    return rtn


def check_bad_str_token(tok):
    """Checks if a token is a bad string."""
    if tok.type == "ERRORTOKEN" and tok.value == "EOF in multi-line string":
        return True
    elif isinstance(tok.value, str) and not check_quotes(tok.value):
        return True
    else:
        return False


def check_quotes(s):
    """Checks a string to make sure that if it starts with quotes, it also
    ends with quotes.
    """
    starts_as_str = RE_BEGIN_STRING.match(s) is not None
    ends_as_str = s.endswith('"') or s.endswith("'")
    if not starts_as_str and not ends_as_str:
        ok = True
    elif starts_as_str and not ends_as_str:
        ok = False
    elif not starts_as_str and ends_as_str:
        ok = False
    else:
        m = RE_COMPLETE_STRING.match(s)
        ok = m is not None
    return ok


def _have_open_triple_quotes(s):
    if s.count('"""') % 2 == 1:
        open_triple = '"""'
    elif s.count("'''") % 2 == 1:
        open_triple = "'''"
    else:
        open_triple = False
    return open_triple


def get_line_continuation():
    """ The line continuation characters used in subproc mode. In interactive
         mode on Windows the backslash must be preceded by a space. This is because
         paths on Windows may end in a backslash.
    """
    if (
        ON_WINDOWS
        and hasattr(builtins.__xonsh__, "env")
        and builtins.__xonsh__.env.get("XONSH_INTERACTIVE", False)
    ):
        return " \\"
    else:
        return "\\"


def get_logical_line(lines, idx):
    """Returns a single logical line (i.e. one without line continuations)
    from a list of lines.  This line should begin at index idx. This also
    returns the number of physical lines the logical line spans. The lines
    should not contain newlines
    """
    n = 1
    nlines = len(lines)
    linecont = get_line_continuation()
    while idx > 0 and lines[idx - 1].endswith(linecont):
        idx -= 1
    start = idx
    line = lines[idx]
    open_triple = _have_open_triple_quotes(line)
    while (line.endswith(linecont) or open_triple) and idx < nlines - 1:
        n += 1
        idx += 1
        if line.endswith(linecont):
            line = line[:-1] + lines[idx]
        else:
            line = line + "\n" + lines[idx]
        open_triple = _have_open_triple_quotes(line)
    return line, n, start


def replace_logical_line(lines, logical, idx, n):
    """Replaces lines at idx that may end in line continuation with a logical
    line that spans n lines.
    """
    linecont = get_line_continuation()
    if n == 1:
        lines[idx] = logical
        return
    space = " "
    for i in range(idx, idx + n - 1):
        a = len(lines[i])
        b = logical.find(space, a - 1)
        if b < 0:
            # no space found
            lines[i] = logical
            logical = ""
        else:
            # found space to split on
            lines[i] = logical[:b] + linecont
            logical = logical[b:]
    lines[idx + n - 1] = logical


def is_balanced(expr, ltok, rtok):
    """Determines whether an expression has unbalanced opening and closing tokens."""
    lcnt = expr.count(ltok)
    if lcnt == 0:
        return True
    rcnt = expr.count(rtok)
    if lcnt == rcnt:
        return True
    else:
        return False


def subexpr_from_unbalanced(expr, ltok, rtok):
    """Attempts to pull out a valid subexpression for unbalanced grouping,
    based on opening tokens, eg. '(', and closing tokens, eg. ')'.  This
    does not do full tokenization, but should be good enough for tab
    completion.
    """
    if is_balanced(expr, ltok, rtok):
        return expr
    subexpr = expr.rsplit(ltok, 1)[-1]
    subexpr = subexpr.rsplit(",", 1)[-1]
    subexpr = subexpr.rsplit(":", 1)[-1]
    return subexpr


def subexpr_before_unbalanced(expr, ltok, rtok):
    """Obtains the expression prior to last unbalanced left token."""
    subexpr, _, post = expr.rpartition(ltok)
    nrtoks_in_post = post.count(rtok)
    while nrtoks_in_post != 0:
        for i in range(nrtoks_in_post):
            subexpr, _, post = subexpr.rpartition(ltok)
        nrtoks_in_post = post.count(rtok)
    _, _, subexpr = subexpr.rpartition(rtok)
    _, _, subexpr = subexpr.rpartition(ltok)
    return subexpr


def decode(s, encoding=None):
    encoding = encoding or DEFAULT_ENCODING
    return s.decode(encoding, "replace")


def encode(u, encoding=None):
    encoding = encoding or DEFAULT_ENCODING
    return u.encode(encoding, "replace")


def cast_unicode(s, encoding=None):
    if isinstance(s, bytes):
        return decode(s, encoding)
    return s


def safe_hasattr(obj, attr):
    """In recent versions of Python, hasattr() only catches AttributeError.
    This catches all errors.
    """
    try:
        getattr(obj, attr)
        return True
    except Exception:  # pylint:disable=bare-except
        return False


def indent(instr, nspaces=4, ntabs=0, flatten=False):
    """Indent a string a given number of spaces or tabstops.

    indent(str,nspaces=4,ntabs=0) -> indent str by ntabs+nspaces.

    Parameters
    ----------
    instr : basestring
        The string to be indented.
    nspaces : int (default: 4)
        The number of spaces to be indented.
    ntabs : int (default: 0)
        The number of tabs to be indented.
    flatten : bool (default: False)
        Whether to scrub existing indentation.  If True, all lines will be
        aligned to the same indentation.  If False, existing indentation will
        be strictly increased.

    Returns
    -------
    outstr : string indented by ntabs and nspaces.

    """
    if instr is None:
        return
    ind = "\t" * ntabs + " " * nspaces
    if flatten:
        pat = re.compile(r"^\s*", re.MULTILINE)
    else:
        pat = re.compile(r"^", re.MULTILINE)
    outstr = re.sub(pat, ind, instr)
    if outstr.endswith(os.linesep + ind):
        return outstr[: -len(ind)]
    else:
        return outstr


def get_sep():
    """ Returns the appropriate filepath separator char depending on OS and
    xonsh options set
    """
    if ON_WINDOWS and builtins.__xonsh__.env.get("FORCE_POSIX_PATHS"):
        return os.altsep
    else:
        return os.sep


def fallback(cond, backup):
    """Decorator for returning the object if cond is true and a backup if cond
    is false.
    """

    def dec(obj):
        return obj if cond else backup

    return dec


# The following redirect classes were taken directly from Python 3.5's source
# code (from the contextlib module). This can be removed when 3.5 is released,
# although redirect_stdout exists in 3.4, redirect_stderr does not.
# See the Python software license: https://docs.python.org/3/license.html
# Copyright (c) Python Software Foundation. All rights reserved.
class _RedirectStream:

    _stream = None

    def __init__(self, new_target):
        self._new_target = new_target
        # We use a list of old targets to make this CM re-entrant
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(getattr(sys, self._stream))
        setattr(sys, self._stream, self._new_target)
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        setattr(sys, self._stream, self._old_targets.pop())


class redirect_stdout(_RedirectStream):
    """Context manager for temporarily redirecting stdout to another file::

        # How to send help() to stderr
        with redirect_stdout(sys.stderr):
            help(dir)

        # How to write help() to a file
        with open('help.txt', 'w') as f:
            with redirect_stdout(f):
                help(pow)

    Mostly for backwards compatibility.
    """

    _stream = "stdout"


class redirect_stderr(_RedirectStream):
    """Context manager for temporarily redirecting stderr to another file."""

    _stream = "stderr"


def _yield_accessible_unix_file_names(path):
    """yield file names of executable files in path."""
    if not os.path.exists(path):
        return
    for file_ in scandir(path):
        try:
            if file_.is_file() and os.access(file_.path, os.X_OK):
                yield file_.name
        except OSError:
            # broken Symlink are neither dir not files
            pass


def _executables_in_posix(path):
    if not os.path.exists(path):
        return
    elif PYTHON_VERSION_INFO < (3, 5, 0):
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)
            if (
                os.path.exists(fpath)
                and os.access(fpath, os.X_OK)
                and (not os.path.isdir(fpath))
            ):
                yield fname
    else:
        yield from _yield_accessible_unix_file_names(path)


def _executables_in_windows(path):
    if not os.path.isdir(path):
        return
    extensions = builtins.__xonsh__.env["PATHEXT"]
    if PYTHON_VERSION_INFO < (3, 5, 0):
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)
            if os.path.exists(fpath) and not os.path.isdir(fpath):
                base_name, ext = os.path.splitext(fname)
                if ext.upper() in extensions:
                    yield fname
    else:
        for x in scandir(path):
            if x.is_file():
                fname = x.name
            else:
                continue
            base_name, ext = os.path.splitext(fname)
            if ext.upper() in extensions:
                yield fname


def executables_in(path):
    """Returns a generator of files in path that the user could execute. """
    if ON_WINDOWS:
        func = _executables_in_windows
    else:
        func = _executables_in_posix
    try:
        yield from func(path)
    except PermissionError:
        return


def command_not_found(cmd):
    """Uses the debian/ubuntu command-not-found utility to suggest packages for a
    command that cannot currently be found.
    """
    if not ON_LINUX:
        return ""
    elif not os.path.isfile("/usr/lib/command-not-found"):
        # utility is not on PATH
        return ""
    c = "/usr/lib/command-not-found {0}; exit 0"
    s = subprocess.check_output(
        c.format(cmd), universal_newlines=True, stderr=subprocess.STDOUT, shell=True
    )
    s = "\n".join(s.rstrip().splitlines()).strip()
    return s


def suggest_commands(cmd, env, aliases):
    """Suggests alternative commands given an environment and aliases."""
    if not env.get("SUGGEST_COMMANDS"):
        return ""
    thresh = env.get("SUGGEST_THRESHOLD")
    max_sugg = env.get("SUGGEST_MAX_NUM")
    if max_sugg < 0:
        max_sugg = float("inf")
    cmd = cmd.lower()
    suggested = {}

    for alias in builtins.aliases:
        if alias not in suggested:
            if levenshtein(alias.lower(), cmd, thresh) < thresh:
                suggested[alias] = "Alias"

    for path in filter(os.path.isdir, env.get("PATH")):
        for _file in executables_in(path):
            if (
                _file not in suggested
                and levenshtein(_file.lower(), cmd, thresh) < thresh
            ):
                suggested[_file] = "Command ({0})".format(os.path.join(path, _file))

    suggested = collections.OrderedDict(
        sorted(
            suggested.items(), key=lambda x: suggestion_sort_helper(x[0].lower(), cmd)
        )
    )
    num = min(len(suggested), max_sugg)

    if num == 0:
        rtn = command_not_found(cmd)
    else:
        oneof = "" if num == 1 else "one of "
        tips = "Did you mean {}the following?".format(oneof)
        items = list(suggested.popitem(False) for _ in range(num))
        length = max(len(key) for key, _ in items) + 2
        alternatives = "\n".join(
            "    {: <{}} {}".format(key + ":", length, val) for key, val in items
        )
        rtn = "{}\n{}".format(tips, alternatives)
        c = command_not_found(cmd)
        rtn += ("\n\n" + c) if len(c) > 0 else ""
    return rtn


def print_exception(msg=None):
    """Print exceptions with/without traceback."""
    env = getattr(builtins.__xonsh__, "env", None)
    # flags indicating whether the traceback options have been manually set
    if env is None:
        env = os_environ
        manually_set_trace = "XONSH_SHOW_TRACEBACK" in env
        manually_set_logfile = "XONSH_TRACEBACK_LOGFILE" in env
    else:
        manually_set_trace = env.is_manually_set("XONSH_SHOW_TRACEBACK")
        manually_set_logfile = env.is_manually_set("XONSH_TRACEBACK_LOGFILE")
    if (not manually_set_trace) and (not manually_set_logfile):
        # Notify about the traceback output possibility if neither of
        # the two options have been manually set
        sys.stderr.write(
            "xonsh: For full traceback set: " "$XONSH_SHOW_TRACEBACK = True\n"
        )
    # get env option for traceback and convert it if necessary
    show_trace = env.get("XONSH_SHOW_TRACEBACK", False)
    if not is_bool(show_trace):
        show_trace = to_bool(show_trace)
    # if the trace option has been set, print all traceback info to stderr
    if show_trace:
        # notify user about XONSH_TRACEBACK_LOGFILE if it has
        # not been set manually
        if not manually_set_logfile:
            sys.stderr.write(
                "xonsh: To log full traceback to a file set: "
                "$XONSH_TRACEBACK_LOGFILE = <filename>\n"
            )
        traceback.print_exc()
    # additionally, check if a file for traceback logging has been
    # specified and convert to a proper option if needed
    log_file = env.get("XONSH_TRACEBACK_LOGFILE", None)
    log_file = to_logfile_opt(log_file)
    if log_file:
        # if log_file <> '' or log_file <> None, append
        # traceback log there as well
        with open(os.path.abspath(log_file), "a") as f:
            traceback.print_exc(file=f)

    if not show_trace:
        # if traceback output is disabled, print the exception's
        # error message on stderr.
        display_error_message()
    if msg:
        msg = msg if msg.endswith("\n") else msg + "\n"
        sys.stderr.write(msg)


def display_error_message(strip_xonsh_error_types=True):
    """
    Prints the error message of the current exception on stderr.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    exception_only = traceback.format_exception_only(exc_type, exc_value)
    if exc_type is XonshError and strip_xonsh_error_types:
        exception_only[0] = exception_only[0].partition(": ")[-1]
    sys.stderr.write("".join(exception_only))


def is_writable_file(filepath):
    """
    Checks if a filepath is valid for writing.
    """
    filepath = expand_path(filepath)
    # convert to absolute path if needed
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)
    # cannot write to directories
    if os.path.isdir(filepath):
        return False
    # if the file exists and is writable, we're fine
    if os.path.exists(filepath):
        return True if os.access(filepath, os.W_OK) else False
    # if the path doesn't exist, isolate its directory component
    # and ensure that directory is writable instead
    return os.access(os.path.dirname(filepath), os.W_OK)


# Modified from Public Domain code, by Magnus Lie Hetland
# from http://hetland.org/coding/python/levenshtein.py
def levenshtein(a, b, max_dist=float("inf")):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if abs(n - m) > max_dist:
        return float("inf")
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n
    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]


def suggestion_sort_helper(x, y):
    """Returns a score (lower is better) for x based on how similar
    it is to y.  Used to rank suggestions."""
    x = x.lower()
    y = y.lower()
    lendiff = len(x) + len(y)
    inx = len([i for i in x if i not in y])
    iny = len([i for i in y if i not in x])
    return lendiff + inx + iny


def escape_windows_cmd_string(s):
    """Returns a string that is usable by the Windows cmd.exe.
    The escaping is based on details here and empirical testing:
    http://www.robvanderwoude.com/escapechars.php
    """
    for c in '^()%!<>&|"':
        s = s.replace(c, "^" + c)
    return s


def argvquote(arg, force=False):
    """ Returns an argument quoted in such a way that that CommandLineToArgvW
    on Windows will return the argument string unchanged.
    This is the same thing Popen does when supplied with an list of arguments.
    Arguments in a command line should be separated by spaces; this
    function does not add these spaces. This implementation follows the
    suggestions outlined here:
    https://blogs.msdn.microsoft.com/twistylittlepassagesallalike/2011/04/23/everyone-quotes-command-line-arguments-the-wrong-way/
    """
    if not force and len(arg) != 0 and not any([c in arg for c in ' \t\n\v"']):
        return arg
    else:
        n_backslashes = 0
        cmdline = '"'
        for c in arg:
            if c == "\\":
                # first count the number of current backslashes
                n_backslashes += 1
                continue
            if c == '"':
                # Escape all backslashes and the following double quotation mark
                cmdline += (n_backslashes * 2 + 1) * "\\"
            else:
                # backslashes are not special here
                cmdline += n_backslashes * "\\"
            n_backslashes = 0
            cmdline += c
        # Escape all backslashes, but let the terminating
        # double quotation mark we add below be interpreted
        # as a metacharacter
        cmdline += +n_backslashes * 2 * "\\" + '"'
        return cmdline


def on_main_thread():
    """Checks if we are on the main thread or not."""
    return threading.current_thread() is threading.main_thread()


_DEFAULT_SENTINEL = object()


@contextlib.contextmanager
def swap(namespace, name, value, default=_DEFAULT_SENTINEL):
    """Swaps a current variable name in a namespace for another value, and then
    replaces it when the context is exited.
    """
    old = getattr(namespace, name, default)
    setattr(namespace, name, value)
    yield value
    if old is default:
        delattr(namespace, name)
    else:
        setattr(namespace, name, old)


@contextlib.contextmanager
def swap_values(d, updates, default=_DEFAULT_SENTINEL):
    """Updates a dictionary (or other mapping) with values from another mapping,
    and then restores the original mapping when the context is exited.
    """
    old = {k: d.get(k, default) for k in updates}
    d.update(updates)
    yield
    for k, v in old.items():
        if v is default and k in d:
            del d[k]
        else:
            d[k] = v


#
# Validators and converters
#


def is_int(x):
    """Tests if something is an integer"""
    return isinstance(x, int)


def is_float(x):
    """Tests if something is a float"""
    return isinstance(x, float)


def is_string(x):
    """Tests if something is a string"""
    return isinstance(x, str)


def is_slice(x):
    """Tests if something is a slice"""
    return isinstance(x, slice)


def is_callable(x):
    """Tests if something is callable"""
    return callable(x)


def is_string_or_callable(x):
    """Tests if something is a string or callable"""
    return is_string(x) or is_callable(x)


def is_class(x):
    """Tests if something is a class"""
    return isinstance(x, type)


def always_true(x):
    """Returns True"""
    return True


def always_false(x):
    """Returns False"""
    return False


def ensure_string(x):
    """Returns a string if x is not a string, and x if it already is."""
    return str(x)


def is_env_path(x):
    """This tests if something is an environment path, ie a list of strings."""
    return isinstance(x, EnvPath)


def str_to_env_path(x):
    """Converts a string to an environment path, ie a list of strings,
    splitting on the OS separator.
    """
    # splitting will be done implicitly in EnvPath's __init__
    return EnvPath(x)


def env_path_to_str(x):
    """Converts an environment path to a string by joining on the OS
    separator.
    """
    return os.pathsep.join(x)


def is_bool(x):
    """Tests if something is a boolean."""
    return isinstance(x, bool)


def is_logfile_opt(x):
    """
    Checks if x is a valid $XONSH_TRACEBACK_LOGFILE option. Returns False
    if x is not a writable/creatable file or an empty string or None.
    """
    if x is None:
        return True
    if not isinstance(x, str):
        return False
    else:
        return is_writable_file(x) or x == ""


def to_logfile_opt(x):
    """
    Converts a $XONSH_TRACEBACK_LOGFILE option to either a str containing
    the filepath if it is a writable file or None if the filepath is not
    valid, informing the user on stderr about the invalid choice.
    """
    superclass = pathlib.PurePath
    if PYTHON_VERSION_INFO >= (3, 6, 0):
        superclass = os.PathLike
    if isinstance(x, superclass):
        x = str(x)
    if is_logfile_opt(x):
        return x
    else:
        # if option is not valid, return a proper
        # option and inform the user on stderr
        sys.stderr.write(
            "xonsh: $XONSH_TRACEBACK_LOGFILE must be a "
            "filepath pointing to a file that either exists "
            "and is writable or that can be created.\n"
        )
        return None


def logfile_opt_to_str(x):
    """
    Detypes a $XONSH_TRACEBACK_LOGFILE option.
    """
    if x is None:
        # None should not be detyped to 'None', as 'None' constitutes
        # a perfectly valid filename and retyping it would introduce
        # ambiguity. Detype to the empty string instead.
        return ""
    return str(x)


_FALSES = LazyObject(
    lambda: frozenset(["", "0", "n", "f", "no", "none", "false", "off"]),
    globals(),
    "_FALSES",
)


def to_bool(x):
    """"Converts to a boolean in a semantically meaningful way."""
    if isinstance(x, bool):
        return x
    elif isinstance(x, str):
        return False if x.lower() in _FALSES else True
    else:
        return bool(x)


def to_itself(x):
    """No conversion, returns itself."""
    return x


def bool_to_str(x):
    """Converts a bool to an empty string if False and the string '1' if
    True.
    """
    return "1" if x else ""


_BREAKS = LazyObject(
    lambda: frozenset(["b", "break", "s", "skip", "q", "quit"]), globals(), "_BREAKS"
)


def to_bool_or_break(x):
    if isinstance(x, str) and x.lower() in _BREAKS:
        return "break"
    else:
        return to_bool(x)


def is_bool_or_int(x):
    """Returns whether a value is a boolean or integer."""
    return is_bool(x) or is_int(x)


def to_bool_or_int(x):
    """Converts a value to a boolean or an integer."""
    if isinstance(x, str):
        return int(x) if x.isdigit() else to_bool(x)
    elif is_int(x):  # bools are ints too!
        return x
    else:
        return bool(x)


def bool_or_int_to_str(x):
    """Converts a boolean or integer to a string."""
    return bool_to_str(x) if is_bool(x) else str(x)


@lazyobject
def SLICE_REG():
    return re.compile(
        r"(?P<start>(?:-\d)?\d*):(?P<end>(?:-\d)?\d*):?(?P<step>(?:-\d)?\d*)"
    )


def ensure_slice(x):
    """Try to convert an object into a slice, complain on failure"""
    if not x and x != 0:
        return slice(None)
    elif is_slice(x):
        return x
    try:
        x = int(x)
        if x != -1:
            s = slice(x, x + 1)
        else:
            s = slice(-1, None, None)
    except ValueError:
        x = x.strip("[]()")
        m = SLICE_REG.fullmatch(x)
        if m:
            groups = (int(i) if i else None for i in m.groups())
            s = slice(*groups)
        else:
            raise ValueError("cannot convert {!r} to slice".format(x))
    except TypeError:
        try:
            s = slice(*(int(i) for i in x))
        except (TypeError, ValueError):
            raise ValueError("cannot convert {!r} to slice".format(x))
    return s


def get_portions(it, slices):
    """Yield from portions of an iterable.

    Parameters
    ----------
    it: iterable
    slices: a slice or a list of slice objects
    """
    if is_slice(slices):
        slices = [slices]
    if len(slices) == 1:
        s = slices[0]
        try:
            yield from itertools.islice(it, s.start, s.stop, s.step)
            return
        except ValueError:  # islice failed
            pass
    it = list(it)
    for s in slices:
        yield from it[s]


def is_slice_as_str(x):
    """
    Test if string x is a slice. If not a string return False.
    """
    try:
        x = x.strip("[]()")
        m = SLICE_REG.fullmatch(x)
        if m:
            return True
    except AttributeError:
        pass
    return False


def is_int_as_str(x):
    """
    Test if string x is an integer. If not a string return False.
    """
    try:
        return x.isdecimal()
    except AttributeError:
        return False


def is_string_set(x):
    """Tests if something is a set of strings"""
    return isinstance(x, cabc.Set) and all(isinstance(a, str) for a in x)


def csv_to_set(x):
    """Convert a comma-separated list of strings to a set of strings."""
    if not x:
        return set()
    else:
        return set(x.split(","))


def set_to_csv(x):
    """Convert a set of strings to a comma-separated list of strings."""
    return ",".join(x)


def pathsep_to_set(x):
    """Converts a os.pathsep separated string to a set of strings."""
    if not x:
        return set()
    else:
        return set(x.split(os.pathsep))


def set_to_pathsep(x, sort=False):
    """Converts a set to an os.pathsep separated string. The sort kwarg
    specifies whether to sort the set prior to str conversion.
    """
    if sort:
        x = sorted(x)
    return os.pathsep.join(x)


def is_string_seq(x):
    """Tests if something is a sequence of strings"""
    return isinstance(x, cabc.Sequence) and all(isinstance(a, str) for a in x)


def is_nonstring_seq_of_strings(x):
    """Tests if something is a sequence of strings, where the top-level
    sequence is not a string itself.
    """
    return (
        isinstance(x, cabc.Sequence)
        and not isinstance(x, str)
        and all(isinstance(a, str) for a in x)
    )


def pathsep_to_seq(x):
    """Converts a os.pathsep separated string to a sequence of strings."""
    if not x:
        return []
    else:
        return x.split(os.pathsep)


def seq_to_pathsep(x):
    """Converts a sequence to an os.pathsep separated string."""
    return os.pathsep.join(x)


def pathsep_to_upper_seq(x):
    """Converts a os.pathsep separated string to a sequence of
    uppercase strings.
    """
    if not x:
        return []
    else:
        return x.upper().split(os.pathsep)


def seq_to_upper_pathsep(x):
    """Converts a sequence to an uppercase os.pathsep separated string."""
    return os.pathsep.join(x).upper()


def is_bool_seq(x):
    """Tests if an object is a sequence of bools."""
    return isinstance(x, cabc.Sequence) and all(isinstance(y, bool) for y in x)


def csv_to_bool_seq(x):
    """Takes a comma-separated string and converts it into a list of bools."""
    return [to_bool(y) for y in csv_to_set(x)]


def bool_seq_to_csv(x):
    """Converts a sequence of bools to a comma-separated string."""
    return ",".join(map(str, x))


def ptk2_color_depth_setter(x):
    """ Setter function for $PROMPT_TOOLKIT_COLOR_DEPTH. Also
        updates os.environ so prompt toolkit can pickup the value.
    """
    x = str(x)
    if x in {
        "DEPTH_1_BIT",
        "MONOCHROME",
        "DEPTH_4_BIT",
        "ANSI_COLORS_ONLY",
        "DEPTH_8_BIT",
        "DEFAULT",
        "DEPTH_24_BIT",
        "TRUE_COLOR",
    }:
        pass
    elif x in {"", None}:
        x = ""
    else:
        msg = '"{}" is not a valid value for $PROMPT_TOOLKIT_COLOR_DEPTH. '.format(x)
        warnings.warn(msg, RuntimeWarning)
        x = ""
    if x == "" and "PROMPT_TOOLKIT_COLOR_DEPTH" in os_environ:
        del os_environ["PROMPT_TOOLKIT_COLOR_DEPTH"]
    else:
        os_environ["PROMPT_TOOLKIT_COLOR_DEPTH"] = x
    return x


def is_completions_display_value(x):
    return x in {"none", "single", "multi"}


def to_completions_display_value(x):
    x = str(x).lower()
    if x in {"none", "false"}:
        x = "none"
    elif x in {"multi", "true"}:
        x = "multi"
    elif x in {"single", "readline"}:
        pass
    else:
        msg = '"{}" is not a valid value for $COMPLETIONS_DISPLAY. '.format(x)
        msg += 'Using "multi".'
        warnings.warn(msg, RuntimeWarning)
        x = "multi"
    return x


def is_str_str_dict(x):
    """Tests if something is a str:str dictionary"""
    return isinstance(x, dict) and all(
        isinstance(k, str) and isinstance(v, str) for k, v in x.items()
    )


def to_dict(x):
    """Converts a string to a dictionary"""
    if isinstance(x, dict):
        return x
    try:
        x = ast.literal_eval(x)
    except (ValueError, SyntaxError):
        msg = '"{}" can not be converted to Python dictionary.'.format(x)
        warnings.warn(msg, RuntimeWarning)
        x = dict()
    return x


def to_str_str_dict(x):
    """Converts a string to str:str dictionary"""
    if is_str_str_dict(x):
        return x
    x = to_dict(x)
    if not is_str_str_dict(x):
        msg = '"{}" can not be converted to str:str dictionary.'.format(x)
        warnings.warn(msg, RuntimeWarning)
        x = dict()
    return x


def dict_to_str(x):
    """Converts a dictionary to a string"""
    if not x or len(x) == 0:
        return ""
    return str(x)


def setup_win_unicode_console(enable):
    """"Enables or disables unicode display on windows."""
    try:
        import win_unicode_console
    except ImportError:
        win_unicode_console = False
    enable = to_bool(enable)
    if ON_WINDOWS and win_unicode_console:
        if enable:
            win_unicode_console.enable()
        else:
            win_unicode_console.disable()
    return enable


# history validation

_min_to_sec = lambda x: 60.0 * float(x)
_hour_to_sec = lambda x: 60.0 * _min_to_sec(x)
_day_to_sec = lambda x: 24.0 * _hour_to_sec(x)
_month_to_sec = lambda x: 30.4375 * _day_to_sec(x)
_year_to_sec = lambda x: 365.25 * _day_to_sec(x)
_kb_to_b = lambda x: 1024 * int(x)
_mb_to_b = lambda x: 1024 * _kb_to_b(x)
_gb_to_b = lambda x: 1024 * _mb_to_b(x)
_tb_to_b = lambda x: 1024 * _tb_to_b(x)

CANON_HISTORY_UNITS = LazyObject(
    lambda: frozenset(["commands", "files", "s", "b"]), globals(), "CANON_HISTORY_UNITS"
)

HISTORY_UNITS = LazyObject(
    lambda: {
        "": ("commands", int),
        "c": ("commands", int),
        "cmd": ("commands", int),
        "cmds": ("commands", int),
        "command": ("commands", int),
        "commands": ("commands", int),
        "f": ("files", int),
        "files": ("files", int),
        "s": ("s", float),
        "sec": ("s", float),
        "second": ("s", float),
        "seconds": ("s", float),
        "m": ("s", _min_to_sec),
        "min": ("s", _min_to_sec),
        "mins": ("s", _min_to_sec),
        "h": ("s", _hour_to_sec),
        "hr": ("s", _hour_to_sec),
        "hour": ("s", _hour_to_sec),
        "hours": ("s", _hour_to_sec),
        "d": ("s", _day_to_sec),
        "day": ("s", _day_to_sec),
        "days": ("s", _day_to_sec),
        "mon": ("s", _month_to_sec),
        "month": ("s", _month_to_sec),
        "months": ("s", _month_to_sec),
        "y": ("s", _year_to_sec),
        "yr": ("s", _year_to_sec),
        "yrs": ("s", _year_to_sec),
        "year": ("s", _year_to_sec),
        "years": ("s", _year_to_sec),
        "b": ("b", int),
        "byte": ("b", int),
        "bytes": ("b", int),
        "kb": ("b", _kb_to_b),
        "kilobyte": ("b", _kb_to_b),
        "kilobytes": ("b", _kb_to_b),
        "mb": ("b", _mb_to_b),
        "meg": ("b", _mb_to_b),
        "megs": ("b", _mb_to_b),
        "megabyte": ("b", _mb_to_b),
        "megabytes": ("b", _mb_to_b),
        "gb": ("b", _gb_to_b),
        "gig": ("b", _gb_to_b),
        "gigs": ("b", _gb_to_b),
        "gigabyte": ("b", _gb_to_b),
        "gigabytes": ("b", _gb_to_b),
        "tb": ("b", _tb_to_b),
        "terabyte": ("b", _tb_to_b),
        "terabytes": ("b", _tb_to_b),
    },
    globals(),
    "HISTORY_UNITS",
)
"""Maps lowercase unit names to canonical name and conversion utilities."""


def is_history_tuple(x):
    """Tests if something is a proper history value, units tuple."""
    if (
        isinstance(x, cabc.Sequence)
        and len(x) == 2
        and isinstance(x[0], (int, float))
        and x[1].lower() in CANON_HISTORY_UNITS
    ):
        return True
    return False


def is_history_backend(x):
    """Tests if something is a valid history backend."""
    return is_string(x) or is_class(x) or isinstance(x, object)


def is_dynamic_cwd_width(x):
    """ Determine if the input is a valid input for the DYNAMIC_CWD_WIDTH
    environment variable.
    """
    return (
        isinstance(x, tuple)
        and len(x) == 2
        and isinstance(x[0], float)
        and x[1] in set("c%")
    )


def to_dynamic_cwd_tuple(x):
    """Convert to a canonical cwd_width tuple."""
    unit = "c"
    if isinstance(x, str):
        if x[-1] == "%":
            x = x[:-1]
            unit = "%"
        else:
            unit = "c"
        return (float(x), unit)
    else:
        return (float(x[0]), x[1])


def dynamic_cwd_tuple_to_str(x):
    """Convert a canonical cwd_width tuple to a string."""
    if x[1] == "%":
        return str(x[0]) + "%"
    else:
        return str(x[0])


RE_HISTORY_TUPLE = LazyObject(
    lambda: re.compile(r"([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*([A-Za-z]*)"),
    globals(),
    "RE_HISTORY_TUPLE",
)


def to_history_tuple(x):
    """Converts to a canonical history tuple."""
    if not isinstance(x, (cabc.Sequence, float, int)):
        raise ValueError("history size must be given as a sequence or number")
    if isinstance(x, str):
        m = RE_HISTORY_TUPLE.match(x.strip().lower())
        return to_history_tuple((m.group(1), m.group(3)))
    elif isinstance(x, (float, int)):
        return to_history_tuple((x, "commands"))
    units, converter = HISTORY_UNITS[x[1]]
    value = converter(x[0])
    return (value, units)


def history_tuple_to_str(x):
    """Converts a valid history tuple to a canonical string."""
    return "{0} {1}".format(*x)


def format_color(string, **kwargs):
    """Formats strings that may contain colors. This simply dispatches to the
    shell instances method of the same name. The results of this function should
    be directly usable by print_color().
    """
    return builtins.__xonsh__.shell.shell.format_color(string, **kwargs)


def print_color(string, **kwargs):
    """Prints a string that may contain colors. This dispatched to the shell
    method of the same name. Colors will be formatted if they have not already
    been.
    """
    builtins.__xonsh__.shell.shell.print_color(string, **kwargs)


def color_style_names():
    """Returns an iterable of all available style names."""
    return builtins.__xonsh__.shell.shell.color_style_names()


def color_style():
    """Returns the current color map."""
    return builtins.__xonsh__.shell.shell.color_style()


def _token_attr_from_stylemap(stylemap):
    """yields tokens attr, and index from a stylemap """
    import prompt_toolkit as ptk

    if builtins.__xonsh__.shell.shell_type == "prompt_toolkit1":
        style = ptk.styles.style_from_dict(stylemap)
        for token in stylemap:
            yield token, style.token_to_attrs[token]
    else:
        style = ptk.styles.style_from_pygments_dict(stylemap)
        for token in stylemap:
            style_str = "class:{}".format(
                ptk.styles.pygments.pygments_token_to_classname(token)
            )
            yield (token, style.get_attrs_for_style_str(style_str))


def _get_color_lookup_table():
    """Returns the prompt_toolkit win32 ColorLookupTable """
    if builtins.__xonsh__.shell.shell_type == "prompt_toolkit1":
        from prompt_toolkit.terminal.win32_output import ColorLookupTable
    else:
        from prompt_toolkit.output.win32 import ColorLookupTable
    return ColorLookupTable()


def _get_color_indexes(style_map):
    """Generates the color and windows color index for a style """
    table = _get_color_lookup_table()
    for token, attr in _token_attr_from_stylemap(style_map):
        if attr.color:
            index = table.lookup_fg_color(attr.color)
            try:
                rgb = (
                    int(attr.color[0:2], 16),
                    int(attr.color[2:4], 16),
                    int(attr.color[4:6], 16),
                )
            except Exception:
                rgb = None
            yield token, index, rgb


# Map of new PTK2 color names to PTK1 variants
PTK_NEW_OLD_COLOR_MAP = LazyObject(
    lambda: {
        "black": "black",
        "red": "darkred",
        "green": "darkgreen",
        "yellow": "brown",
        "blue": "darkblue",
        "magenta": "purple",
        "cyan": "teal",
        "gray": "lightgray",
        "brightblack": "darkgray",
        "brightred": "red",
        "brightgreen": "green",
        "brightyellow": "yellow",
        "brightblue": "blue",
        "brightmagenta": "fuchsia",
        "brightcyan": "turquoise",
        "white": "white",
    },
    globals(),
    "PTK_NEW_OLD_COLOR_MAP",
)

# Map of new ansicolor names to old PTK1 names
ANSICOLOR_NAMES_MAP = LazyObject(
    lambda: {"ansi" + k: "#ansi" + v for k, v in PTK_NEW_OLD_COLOR_MAP.items()},
    globals(),
    "ANSICOLOR_NAMES_MAP",
)


def _win10_color_map():
    cmap = {
        "ansiblack": (12, 12, 12),
        "ansiblue": (0, 55, 218),
        "ansigreen": (19, 161, 14),
        "ansicyan": (58, 150, 221),
        "ansired": (197, 15, 31),
        "ansimagenta": (136, 23, 152),
        "ansiyellow": (193, 156, 0),
        "ansigray": (204, 204, 204),
        "ansibrightblack": (118, 118, 118),
        "ansibrightblue": (59, 120, 255),
        "ansibrightgreen": (22, 198, 12),
        "ansibrightcyan": (97, 214, 214),
        "ansibrightred": (231, 72, 86),
        "ansibrightmagenta": (180, 0, 158),
        "ansibrightyellow": (249, 241, 165),
        "ansiwhite": (242, 242, 242),
    }
    return {
        k: "#{0:02x}{1:02x}{2:02x}".format(r, g, b) for k, (r, g, b) in cmap.items()
    }


WIN10_COLOR_MAP = LazyObject(_win10_color_map, globals(), "WIN10_COLOR_MAP")


def _win_bold_color_map():
    """ Map dark ansi colors to lighter version. """
    return {
        "ansiblack": "ansibrightblack",
        "ansiblue": "ansibrightblue",
        "ansigreen": "ansibrightgreen",
        "ansicyan": "ansibrightcyan",
        "ansired": "ansibrightred",
        "ansimagenta": "ansibrightmagenta",
        "ansiyellow": "ansibrightyellow",
        "ansigray": "ansiwhite",
    }


WIN_BOLD_COLOR_MAP = LazyObject(_win_bold_color_map, globals(), "WIN_BOLD_COLOR_MAP")


def hardcode_colors_for_win10(style_map):
    """Replace all ansi colors with hardcoded colors to avoid unreadable defaults
       in conhost.exe
    """
    modified_style = {}
    if not builtins.__xonsh__.env["PROMPT_TOOLKIT_COLOR_DEPTH"]:
        builtins.__xonsh__.env["PROMPT_TOOLKIT_COLOR_DEPTH"] = "DEPTH_24_BIT"
    # Replace all ansi colors with hardcoded colors to avoid unreadable defaults
    # in conhost.exe
    for token, style_str in style_map.items():
        for ansicolor in WIN10_COLOR_MAP:
            if ansicolor in style_str:
                if "bold" in style_str and "nobold" not in style_str:
                    # Win10  doesn't yet handle bold colors. Instead dark
                    # colors are mapped to their lighter version. We simulate
                    # the same here.
                    style_str.replace("bold", "")
                    hexcolor = WIN10_COLOR_MAP[
                        WIN_BOLD_COLOR_MAP.get(ansicolor, ansicolor)
                    ]
                else:
                    hexcolor = WIN10_COLOR_MAP[ansicolor]
                style_str = style_str.replace(ansicolor, hexcolor)
        modified_style[token] = style_str
    return modified_style


def ansicolors_to_ptk1_names(stylemap):
    """Converts ansicolor names in a stylemap to old PTK1 color names
    """
    modified_stylemap = {}
    for token, style_str in stylemap.items():
        for color, ptk1_color in ANSICOLOR_NAMES_MAP.items():
            if "#" + color not in style_str:
                style_str = style_str.replace(color, ptk1_color)
        modified_stylemap[token] = style_str
    return modified_stylemap


def intensify_colors_for_cmd_exe(style_map):
    """Returns a modified style to where colors that maps to dark
       colors are replaced with brighter versions.
    """
    modified_style = {}
    replace_colors = {
        1: "ansibrightcyan",  # subst blue with bright cyan
        2: "ansibrightgreen",  # subst green with bright green
        4: "ansibrightred",  # subst red with bright red
        5: "ansibrightmagenta",  # subst magenta with bright magenta
        6: "ansibrightyellow",  # subst yellow with bright yellow
        9: "ansicyan",  # subst intense blue with dark cyan (more readable)
    }
    if builtins.__xonsh__.shell.shell_type == "prompt_toolkit1":
        replace_colors = ansicolors_to_ptk1_names(replace_colors)
    for token, idx, _ in _get_color_indexes(style_map):
        if idx in replace_colors:
            modified_style[token] = replace_colors[idx]
    return modified_style


def intensify_colors_on_win_setter(enable):
    """Resets the style when setting the INTENSIFY_COLORS_ON_WIN
    environment variable.
    """
    enable = to_bool(enable)
    if builtins.__xonsh__.shell is not None:
        if hasattr(builtins.__xonsh__.shell.shell.styler, "style_name"):
            delattr(builtins.__xonsh__.shell.shell.styler, "style_name")
    return enable


def format_std_prepost(template, env=None):
    """Formats a template prefix/postfix string for a standard buffer.
    Returns a string suitable for prepending or appending.
    """
    if not template:
        return ""
    env = builtins.__xonsh__.env if env is None else env
    shell = builtins.__xonsh__.shell.shell
    try:
        s = shell.prompt_formatter(template)
    except Exception:
        print_exception()
    # \001\002 is there to fool pygments into not returning an empty string
    # for potentially empty input. This happens when the template is just a
    # color code with no visible text.
    invis = "\001\002"
    s = shell.format_color(invis + s + invis, force_string=True)
    s = s.replace(invis, "")
    return s


_RE_STRING_START = "[bBprRuUf]*"
_RE_STRING_TRIPLE_DOUBLE = '"""'
_RE_STRING_TRIPLE_SINGLE = "'''"
_RE_STRING_DOUBLE = '"'
_RE_STRING_SINGLE = "'"
_STRINGS = (
    _RE_STRING_TRIPLE_DOUBLE,
    _RE_STRING_TRIPLE_SINGLE,
    _RE_STRING_DOUBLE,
    _RE_STRING_SINGLE,
)
RE_BEGIN_STRING = LazyObject(
    lambda: re.compile("(" + _RE_STRING_START + "(" + "|".join(_STRINGS) + "))"),
    globals(),
    "RE_BEGIN_STRING",
)
"""Regular expression matching the start of a string, including quotes and
leading characters (r, b, or u)"""

RE_STRING_START = LazyObject(
    lambda: re.compile(_RE_STRING_START), globals(), "RE_STRING_START"
)
"""Regular expression matching the characters before the quotes when starting a
string (r, b, or u, case insensitive)"""

RE_STRING_CONT = LazyDict(
    {
        '"': lambda: re.compile(r'((\\(.|\n))|([^"\\]))*'),
        "'": lambda: re.compile(r"((\\(.|\n))|([^'\\]))*"),
        '"""': lambda: re.compile(r'((\\(.|\n))|([^"\\])|("(?!""))|\n)*'),
        "'''": lambda: re.compile(r"((\\(.|\n))|([^'\\])|('(?!''))|\n)*"),
    },
    globals(),
    "RE_STRING_CONT",
)
"""Dictionary mapping starting quote sequences to regular expressions that
match the contents of a string beginning with those quotes (not including the
terminating quotes)"""


@lazyobject
def RE_COMPLETE_STRING():
    ptrn = (
        "^"
        + _RE_STRING_START
        + "(?P<quote>"
        + "|".join(_STRINGS)
        + ")"
        + ".*?(?P=quote)$"
    )
    return re.compile(ptrn, re.DOTALL)


def strip_simple_quotes(s):
    """Gets rid of single quotes, double quotes, single triple quotes, and
    single double quotes from a string, if present front and back of a string.
    Otherwiswe, does nothing.
    """
    starts_single = s.startswith("'")
    starts_double = s.startswith('"')
    if not starts_single and not starts_double:
        return s
    elif starts_single:
        ends_single = s.endswith("'")
        if not ends_single:
            return s
        elif s.startswith("'''") and s.endswith("'''") and len(s) >= 6:
            return s[3:-3]
        elif len(s) >= 2:
            return s[1:-1]
        else:
            return s
    else:
        # starts double
        ends_double = s.endswith('"')
        if not ends_double:
            return s
        elif s.startswith('"""') and s.endswith('"""') and len(s) >= 6:
            return s[3:-3]
        elif len(s) >= 2:
            return s[1:-1]
        else:
            return s


def check_for_partial_string(x):
    """Returns the starting index (inclusive), ending index (exclusive), and
    starting quote string of the most recent Python string found in the input.

    check_for_partial_string(x) -> (startix, endix, quote)

    Parameters
    ----------
    x : str
        The string to be checked (representing a line of terminal input)

    Returns
    -------
    startix : int (or None)
        The index where the most recent Python string found started
        (inclusive), or None if no strings exist in the input

    endix : int (or None)
        The index where the most recent Python string found ended (exclusive),
        or None if no strings exist in the input OR if the input ended in the
        middle of a Python string

    quote : str (or None)
        A string containing the quote used to start the string (e.g., b", ",
        '''), or None if no string was found.
    """
    string_indices = []
    starting_quote = []
    current_index = 0
    match = re.search(RE_BEGIN_STRING, x)
    while match is not None:
        # add the start in
        start = match.start()
        quote = match.group(0)
        lenquote = len(quote)
        current_index += start
        # store the starting index of the string, as well as the
        # characters in the starting quotes (e.g., ", ', """, r", etc)
        string_indices.append(current_index)
        starting_quote.append(quote)
        # determine the string that should terminate this string
        ender = re.sub(RE_STRING_START, "", quote)
        x = x[start + lenquote :]
        current_index += lenquote
        # figure out what is inside the string
        continuer = RE_STRING_CONT[ender]
        contents = re.match(continuer, x)
        inside = contents.group(0)
        leninside = len(inside)
        current_index += contents.start() + leninside + len(ender)
        # if we are not at the end of the input string, add the ending index of
        # the string to string_indices
        if contents.end() < len(x):
            string_indices.append(current_index)
        x = x[leninside + len(ender) :]
        # find the next match
        match = re.search(RE_BEGIN_STRING, x)
    numquotes = len(string_indices)
    if numquotes == 0:
        return (None, None, None)
    elif numquotes % 2:
        return (string_indices[-1], None, starting_quote[-1])
    else:
        return (string_indices[-2], string_indices[-1], starting_quote[-1])


# regular expressions for matching environment variables
# i.e $FOO, ${'FOO'}
@lazyobject
def POSIX_ENVVAR_REGEX():
    pat = r"""\$({(?P<quote>['"])|)(?P<envvar>\w+)((?P=quote)}|(?:\1\b))"""
    return re.compile(pat)


def expandvars(path):
    """Expand shell variables of the forms $var, ${var} and %var%.
    Unknown variables are left unchanged."""
    env = builtins.__xonsh__.env
    if isinstance(path, bytes):
        path = path.decode(
            encoding=env.get("XONSH_ENCODING"), errors=env.get("XONSH_ENCODING_ERRORS")
        )
    elif isinstance(path, pathlib.Path):
        # get the path's string representation
        path = str(path)
    if "$" in path:
        for match in POSIX_ENVVAR_REGEX.finditer(path):
            name = match.group("envvar")
            if name in env:
                ensurer = env.get_ensurer(name)
                value = ensurer.detype(env[name])
                path = POSIX_ENVVAR_REGEX.sub(value, path, count=1)
    return path


#
# File handling tools
#


def backup_file(fname):
    """Moves an existing file to a new name that has the current time right
    before the extension.
    """
    # lazy imports
    import shutil
    from datetime import datetime

    base, ext = os.path.splitext(fname)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    newfname = "%s.%s%s" % (base, timestamp, ext)
    shutil.move(fname, newfname)


def normabspath(p):
    """Returns as normalized absolute path, namely, normcase(abspath(p))"""
    return os.path.normcase(os.path.abspath(p))


def expanduser_abs_path(inp):
    """ Provides user expanded absolute path """
    return os.path.abspath(expanduser(inp))


WINDOWS_DRIVE_MATCHER = LazyObject(
    lambda: re.compile(r"^\w:"), globals(), "WINDOWS_DRIVE_MATCHER"
)


def expand_case_matching(s):
    """Expands a string to a case insensitive globable string."""
    t = []
    openers = {"[", "{"}
    closers = {"]", "}"}
    nesting = 0

    drive_part = WINDOWS_DRIVE_MATCHER.match(s) if ON_WINDOWS else None

    if drive_part:
        drive_part = drive_part.group(0)
        t.append(drive_part)
        s = s[len(drive_part) :]

    for c in s:
        if c in openers:
            nesting += 1
        elif c in closers:
            nesting -= 1
        elif nesting > 0:
            pass
        elif c.isalpha():
            folded = c.casefold()
            if len(folded) == 1:
                c = "[{0}{1}]".format(c.upper(), c.lower())
            else:
                newc = ["[{0}{1}]?".format(f.upper(), f.lower()) for f in folded[:-1]]
                newc = "".join(newc)
                newc += "[{0}{1}{2}]".format(folded[-1].upper(), folded[-1].lower(), c)
                c = newc
        t.append(c)
    return "".join(t)


def globpath(
    s, ignore_case=False, return_empty=False, sort_result=None, include_dotfiles=None
):
    """Simple wrapper around glob that also expands home and env vars."""
    o, s = _iglobpath(
        s,
        ignore_case=ignore_case,
        sort_result=sort_result,
        include_dotfiles=include_dotfiles,
    )
    o = list(o)
    no_match = [] if return_empty else [s]
    return o if len(o) != 0 else no_match


def _dotglobstr(s):
    modified = False
    dotted_s = s
    if "/*" in dotted_s:
        dotted_s = dotted_s.replace("/*", "/.*")
        dotted_s = dotted_s.replace("/.**/.*", "/**/.*")
        modified = True
    if dotted_s.startswith("*") and not dotted_s.startswith("**"):
        dotted_s = "." + dotted_s
        modified = True
    return dotted_s, modified


def _iglobpath(s, ignore_case=False, sort_result=None, include_dotfiles=None):
    s = builtins.__xonsh__.expand_path(s)
    if sort_result is None:
        sort_result = builtins.__xonsh__.env.get("GLOB_SORTED")
    if include_dotfiles is None:
        include_dotfiles = builtins.__xonsh__.env.get("DOTGLOB")
    if ignore_case:
        s = expand_case_matching(s)
    if sys.version_info > (3, 5):
        if "**" in s and "**/*" not in s:
            s = s.replace("**", "**/*")
        if include_dotfiles:
            dotted_s, dotmodified = _dotglobstr(s)
        # `recursive` is only a 3.5+ kwarg.
        if sort_result:
            paths = glob.glob(s, recursive=True)
            if include_dotfiles and dotmodified:
                paths.extend(glob.iglob(dotted_s, recursive=True))
            paths.sort()
            paths = iter(paths)
        else:
            paths = glob.iglob(s, recursive=True)
            if include_dotfiles and dotmodified:
                paths = itertools.chain(glob.iglob(dotted_s, recursive=True), paths)
        return paths, s
    else:
        if include_dotfiles:
            dotted_s, dotmodified = _dotglobstr(s)
        if sort_result:
            paths = glob.glob(s)
            if include_dotfiles and dotmodified:
                paths.extend(glob.iglob(dotted_s))
            paths.sort()
            paths = iter(paths)
        else:
            paths = glob.iglob(s)
            if include_dotfiles and dotmodified:
                paths = itertools.chain(glob.iglob(dotted_s), paths)
        return paths, s


def iglobpath(s, ignore_case=False, sort_result=None, include_dotfiles=None):
    """Simple wrapper around iglob that also expands home and env vars."""
    try:
        return _iglobpath(
            s,
            ignore_case=ignore_case,
            sort_result=sort_result,
            include_dotfiles=include_dotfiles,
        )[0]
    except IndexError:
        # something went wrong in the actual iglob() call
        return iter(())


def ensure_timestamp(t, datetime_format=None):
    if isinstance(t, (int, float)):
        return t
    try:
        return float(t)
    except (ValueError, TypeError):
        pass
    if datetime_format is None:
        datetime_format = builtins.__xonsh__.env["XONSH_DATETIME_FORMAT"]
    if isinstance(t, datetime.datetime):
        t = t.timestamp()
    else:
        t = datetime.datetime.strptime(t, datetime_format).timestamp()
    return t


def format_datetime(dt):
    """Format datetime object to string base on $XONSH_DATETIME_FORMAT Env."""
    format_ = builtins.__xonsh__.env["XONSH_DATETIME_FORMAT"]
    return dt.strftime(format_)


def columnize(elems, width=80, newline="\n"):
    """Takes an iterable of strings and returns a list of lines with the
    elements placed in columns. Each line will be at most *width* columns.
    The newline character will be appended to the end of each line.
    """
    sizes = [len(e) + 1 for e in elems]
    total = sum(sizes)
    nelem = len(elems)
    if total - 1 <= width:
        ncols = len(sizes)
        nrows = 1
        columns = [sizes]
        last_longest_row = total
        enter_loop = False
    else:
        ncols = 1
        nrows = len(sizes)
        columns = [sizes]
        last_longest_row = max(sizes)
        enter_loop = True
    while enter_loop:
        longest_row = sum(map(max, columns))
        if longest_row - 1 <= width:
            # we might be able to fit another column.
            ncols += 1
            nrows = nelem // ncols
            columns = [sizes[i * nrows : (i + 1) * nrows] for i in range(ncols)]
            last_longest_row = longest_row
        else:
            # we can't fit another column
            ncols -= 1
            nrows = nelem // ncols
            break
    pad = (width - last_longest_row + ncols) // ncols
    pad = pad if pad > 1 else 1
    data = [elems[i * nrows : (i + 1) * nrows] for i in range(ncols)]
    colwidths = [max(map(len, d)) + pad for d in data]
    colwidths[-1] -= pad
    row_t = "".join(["{{row[{i}]: <{{w[{i}]}}}}".format(i=i) for i in range(ncols)])
    row_t += newline
    lines = [
        row_t.format(row=row, w=colwidths)
        for row in itertools.zip_longest(*data, fillvalue="")
    ]
    return lines


def unthreadable(f):
    """Decorator that specifies that a callable alias should be run only
    on the main thread process. This is often needed for debuggers and
    profilers.
    """
    f.__xonsh_threadable__ = False
    return f


def uncapturable(f):
    """Decorator that specifies that a callable alias should not be run with
    any capturing. This is often needed if the alias call interactive
    subprocess, like pagers and text editors.
    """
    f.__xonsh_capturable__ = False
    return f


def carriage_return():
    """Writes a carriage return to stdout, and nothing else."""
    print("\r", flush=True, end="")


def deprecated(deprecated_in=None, removed_in=None):
    """Parametrized decorator that deprecates a function in a graceful manner.

    Updates the decorated function's docstring to mention the version
    that deprecation occurred in and the version it will be removed
    in if both of these values are passed.

    When removed_in is not a release equal to or less than the current
    release, call ``warnings.warn`` with details, while raising
    ``DeprecationWarning``.

    When removed_in is a release equal to or less than the current release,
    raise an ``AssertionError``.

    Parameters
    ----------
    deprecated_in : str
        The version number that deprecated this function.
    removed_in : str
        The version number that this function will be removed in.
    """
    message_suffix = _deprecated_message_suffix(deprecated_in, removed_in)
    if not message_suffix:
        message_suffix = ""

    def decorated(func):
        warning_message = "{} has been deprecated".format(func.__name__)
        warning_message += message_suffix

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            _deprecated_error_on_expiration(func.__name__, removed_in)
            func(*args, **kwargs)
            warnings.warn(warning_message, DeprecationWarning)

        wrapped.__doc__ = (
            "{}\n\n{}".format(wrapped.__doc__, warning_message)
            if wrapped.__doc__
            else warning_message
        )

        return wrapped

    return decorated


def _deprecated_message_suffix(deprecated_in, removed_in):
    if deprecated_in and removed_in:
        message_suffix = " in version {} and will be removed in version {}".format(
            deprecated_in, removed_in
        )
    elif deprecated_in and not removed_in:
        message_suffix = " in version {}".format(deprecated_in)
    elif not deprecated_in and removed_in:
        message_suffix = " and will be removed in version {}".format(removed_in)
    else:
        message_suffix = None

    return message_suffix


def _deprecated_error_on_expiration(name, removed_in):
    if not removed_in:
        return
    elif LooseVersion(__version__) >= LooseVersion(removed_in):
        raise AssertionError(
            "{} has passed its version {} expiry date!".format(name, removed_in)
        )

#
# ast
#
# -*- coding: utf-8 -*-
"""The xonsh abstract syntax tree node."""
# These are imported into our module namespace for the benefit of parser.py.
# pylint: disable=unused-import
# amalgamated sys
# amalgamated builtins
from ast import (
    Module,
    Num,
    Expr,
    Str,
    Bytes,
    UnaryOp,
    UAdd,
    USub,
    Invert,
    BinOp,
    Add,
    Sub,
    Mult,
    Div,
    FloorDiv,
    Mod,
    Pow,
    Compare,
    Lt,
    Gt,
    LtE,
    GtE,
    Eq,
    NotEq,
    In,
    NotIn,
    Is,
    IsNot,
    Not,
    BoolOp,
    Or,
    And,
    Subscript,
    Load,
    Slice,
    ExtSlice,
    List,
    Tuple,
    Set,
    Dict,
    AST,
    NameConstant,
    Name,
    GeneratorExp,
    Store,
    comprehension,
    ListComp,
    SetComp,
    DictComp,
    Assign,
    AugAssign,
    BitXor,
    BitAnd,
    BitOr,
    LShift,
    RShift,
    Assert,
    Delete,
    Del,
    Pass,
    Raise,
    Import,
    alias,
    ImportFrom,
    Continue,
    Break,
    Yield,
    YieldFrom,
    Return,
    IfExp,
    Lambda,
    arguments,
    arg,
    Call,
    keyword,
    Attribute,
    Global,
    Nonlocal,
    If,
    While,
    For,
    withitem,
    With,
    Try,
    ExceptHandler,
    FunctionDef,
    ClassDef,
    Starred,
    NodeTransformer,
    Interactive,
    Expression,
    Index,
    literal_eval,
    dump,
    walk,
    increment_lineno,
)
from ast import Ellipsis as EllipsisNode

# pylint: enable=unused-import
# amalgamated textwrap
# amalgamated itertools
# amalgamated xonsh.tools
# amalgamated xonsh.platform
if PYTHON_VERSION_INFO >= (3, 5, 0):
    # pylint: disable=unused-import
    # pylint: disable=no-name-in-module
    from ast import MatMult, AsyncFunctionDef, AsyncWith, AsyncFor, Await
else:
    MatMult = AsyncFunctionDef = AsyncWith = AsyncFor = Await = None

if PYTHON_VERSION_INFO >= (3, 6, 0):
    # pylint: disable=unused-import
    # pylint: disable=no-name-in-module
    from ast import JoinedStr, FormattedValue, AnnAssign
else:
    JoinedStr = FormattedValue = AnnAssign = None

STATEMENTS = (
    FunctionDef,
    ClassDef,
    Return,
    Delete,
    Assign,
    AugAssign,
    For,
    While,
    If,
    With,
    Raise,
    Try,
    Assert,
    Import,
    ImportFrom,
    Global,
    Nonlocal,
    Expr,
    Pass,
    Break,
    Continue,
)
if PYTHON_VERSION_INFO >= (3, 6, 0):
    STATEMENTS += (AnnAssign,)


def leftmostname(node):
    """Attempts to find the first name in the tree."""
    if isinstance(node, Name):
        rtn = node.id
    elif isinstance(node, (BinOp, Compare)):
        rtn = leftmostname(node.left)
    elif isinstance(node, (Attribute, Subscript, Starred, Expr)):
        rtn = leftmostname(node.value)
    elif isinstance(node, Call):
        rtn = leftmostname(node.func)
    elif isinstance(node, UnaryOp):
        rtn = leftmostname(node.operand)
    elif isinstance(node, BoolOp):
        rtn = leftmostname(node.values[0])
    elif isinstance(node, (Assign, AnnAssign)):
        rtn = leftmostname(node.targets[0])
    elif isinstance(node, (Str, Bytes, JoinedStr)):
        # handles case of "./my executable"
        rtn = leftmostname(node.s)
    elif isinstance(node, Tuple) and len(node.elts) > 0:
        # handles case of echo ,1,2,3
        rtn = leftmostname(node.elts[0])
    else:
        rtn = None
    return rtn


def get_lineno(node, default=0):
    """Gets the lineno of a node or returns the default."""
    return getattr(node, "lineno", default)


def min_line(node):
    """Computes the minimum lineno."""
    node_line = get_lineno(node)
    return min(map(get_lineno, walk(node), itertools.repeat(node_line)))


def max_line(node):
    """Computes the maximum lineno."""
    return max(map(get_lineno, walk(node)))


def get_col(node, default=-1):
    """Gets the col_offset of a node, or returns the default"""
    return getattr(node, "col_offset", default)


def min_col(node):
    """Computes the minimum col_offset."""
    return min(map(get_col, walk(node), itertools.repeat(node.col_offset)))


def max_col(node):
    """Returns the maximum col_offset of the node and all sub-nodes."""
    col = getattr(node, "max_col", None)
    if col is not None:
        return col
    highest = max(walk(node), key=get_col)
    col = highest.col_offset + node_len(highest)
    return col


def node_len(node):
    """The length of a node as a string"""
    val = 0
    for n in walk(node):
        if isinstance(n, Name):
            val += len(n.id)
        elif isinstance(n, Attribute):
            val += 1 + (len(n.attr) if isinstance(n.attr, str) else 0)
        # this may need to be added to for more nodes as more cases are found
    return val


def get_id(node, default=None):
    """Gets the id attribute of a node, or returns a default."""
    return getattr(node, "id", default)


def gather_names(node):
    """Returns the set of all names present in the node's tree."""
    rtn = set(map(get_id, walk(node)))
    rtn.discard(None)
    return rtn


def get_id_ctx(node):
    """Gets the id and attribute of a node, or returns a default."""
    nid = getattr(node, "id", None)
    if nid is None:
        return (None, None)
    return (nid, node.ctx)


def gather_load_store_names(node):
    """Returns the names present in the node's tree in a set of load nodes and
    a set of store nodes.
    """
    load = set()
    store = set()
    for nid, ctx in map(get_id_ctx, walk(node)):
        if nid is None:
            continue
        elif isinstance(ctx, Load):
            load.add(nid)
        else:
            store.add(nid)
    return (load, store)


def has_elts(x):
    """Tests if x is an AST node with elements."""
    return isinstance(x, AST) and hasattr(x, "elts")


def load_attribute_chain(name, lineno=None, col=None):
    """Creates an AST that loads variable name that may (or may not)
    have attribute chains. For example, "a.b.c"
    """
    names = name.split(".")
    node = Name(id=names.pop(0), ctx=Load(), lineno=lineno, col_offset=col)
    for attr in names:
        node = Attribute(
            value=node, attr=attr, ctx=Load(), lineno=lineno, col_offset=col
        )
    return node


def xonsh_call(name, args, lineno=None, col=None):
    """Creates the AST node for calling a function of a given name.
    Functions names may contain attribute access, e.g. __xonsh__.env.
    """
    return Call(
        func=load_attribute_chain(name, lineno=lineno, col=col),
        args=args,
        keywords=[],
        starargs=None,
        kwargs=None,
        lineno=lineno,
        col_offset=col,
    )


def isdescendable(node):
    """Determines whether or not a node is worth visiting. Currently only
    UnaryOp and BoolOp nodes are visited.
    """
    return isinstance(node, (UnaryOp, BoolOp))


def isexpression(node, ctx=None, *args, **kwargs):
    """Determines whether a node (or code string) is an expression, and
    does not contain any statements. The execution context (ctx) and
    other args and kwargs are passed down to the parser, as needed.
    """
    # parse string to AST
    if isinstance(node, str):
        node = node if node.endswith("\n") else node + "\n"
        ctx = builtins.__xonsh__.ctx if ctx is None else ctx
        node = builtins.__xonsh__.execer.parse(node, ctx, *args, **kwargs)
    # determin if expresission-like enough
    if isinstance(node, (Expr, Expression)):
        isexpr = True
    elif isinstance(node, Module) and len(node.body) == 1:
        isexpr = isinstance(node.body[0], (Expr, Expression))
    else:
        isexpr = False
    return isexpr


class CtxAwareTransformer(NodeTransformer):
    """Transforms a xonsh AST based to use subprocess calls when
    the first name in an expression statement is not known in the context.
    This assumes that the expression statement is instead parseable as
    a subprocess.
    """

    def __init__(self, parser):
        """Parameters
        ----------
        parser : xonsh.Parser
            A parse instance to try to parse subprocess statements with.
        """
        super(CtxAwareTransformer, self).__init__()
        self.parser = parser
        self.input = None
        self.contexts = []
        self.lines = None
        self.mode = None
        self._nwith = 0
        self.filename = "<xonsh-code>"
        self.debug_level = 0

    def ctxvisit(self, node, inp, ctx, mode="exec", filename=None, debug_level=0):
        """Transforms the node in a context-dependent way.

        Parameters
        ----------
        node : ast.AST
            A syntax tree to transform.
        input : str
            The input code in string format.
        ctx : dict
            The root context to use.
        filename : str, optional
            File we are to transform.
        debug_level : int, optional
            Debugging level to use in lexing and parsing.

        Returns
        -------
        node : ast.AST
            The transformed node.
        """
        self.filename = self.filename if filename is None else filename
        self.debug_level = debug_level
        self.lines = inp.splitlines()
        self.contexts = [ctx, set()]
        self.mode = mode
        self._nwith = 0
        node = self.visit(node)
        del self.lines, self.contexts, self.mode
        self._nwith = 0
        return node

    def ctxupdate(self, iterable):
        """Updated the most recent context."""
        self.contexts[-1].update(iterable)

    def ctxadd(self, value):
        """Adds a value the most recent context."""
        self.contexts[-1].add(value)

    def ctxremove(self, value):
        """Removes a value the most recent context."""
        for ctx in reversed(self.contexts):
            if value in ctx:
                ctx.remove(value)
                break

    def try_subproc_toks(self, node, strip_expr=False):
        """Tries to parse the line of the node as a subprocess."""
        line, nlogical, idx = get_logical_line(self.lines, node.lineno - 1)
        if self.mode == "eval":
            mincol = len(line) - len(line.lstrip())
            maxcol = None
        else:
            mincol = max(min_col(node) - 1, 0)
            maxcol = max_col(node)
            if mincol == maxcol:
                maxcol = find_next_break(line, mincol=mincol, lexer=self.parser.lexer)
            elif nlogical > 1:
                maxcol = None
            elif maxcol < len(line) and line[maxcol] == ";":
                pass
            else:
                maxcol += 1
        spline = subproc_toks(
            line,
            mincol=mincol,
            maxcol=maxcol,
            returnline=False,
            lexer=self.parser.lexer,
        )
        if spline is None or spline != "![{}]".format(line[mincol:maxcol].strip()):
            # failed to get something consistent, try greedy wrap
            spline = subproc_toks(
                line,
                mincol=mincol,
                maxcol=maxcol,
                returnline=False,
                lexer=self.parser.lexer,
                greedy=True,
            )
        if spline is None:
            return node
        try:
            newnode = self.parser.parse(
                spline,
                mode=self.mode,
                filename=self.filename,
                debug_level=(self.debug_level > 2),
            )
            newnode = newnode.body
            if not isinstance(newnode, AST):
                # take the first (and only) Expr
                newnode = newnode[0]
            increment_lineno(newnode, n=node.lineno - 1)
            newnode.col_offset = node.col_offset
            if self.debug_level > 1:
                msg = "{0}:{1}:{2}{3} - {4}\n" "{0}:{1}:{2}{3} + {5}"
                mstr = "" if maxcol is None else ":" + str(maxcol)
                msg = msg.format(self.filename, node.lineno, mincol, mstr, line, spline)
                print(msg, file=sys.stderr)
        except SyntaxError:
            newnode = node
        if strip_expr and isinstance(newnode, Expr):
            newnode = newnode.value
        return newnode

    def is_in_scope(self, node):
        """Determines whether or not the current node is in scope."""
        names, store = gather_load_store_names(node)
        names -= store
        if not names:
            return True
        inscope = False
        for ctx in reversed(self.contexts):
            names -= ctx
            if not names:
                inscope = True
                break
        return inscope

    #
    # Replacement visitors
    #

    def visit_Expression(self, node):
        """Handle visiting an expression body."""
        if isdescendable(node.body):
            node.body = self.visit(node.body)
        body = node.body
        inscope = self.is_in_scope(body)
        if not inscope:
            node.body = self.try_subproc_toks(body)
        return node

    def visit_Expr(self, node):
        """Handle visiting an expression."""
        if isdescendable(node.value):
            node.value = self.visit(node.value)  # this allows diving into BoolOps
        if self.is_in_scope(node) or isinstance(node.value, Lambda):
            return node
        else:
            newnode = self.try_subproc_toks(node)
            if not isinstance(newnode, Expr):
                newnode = Expr(
                    value=newnode, lineno=node.lineno, col_offset=node.col_offset
                )
                if hasattr(node, "max_lineno"):
                    newnode.max_lineno = node.max_lineno
                    newnode.max_col = node.max_col
            return newnode

    def visit_UnaryOp(self, node):
        """Handle visiting an unary operands, like not."""
        if isdescendable(node.operand):
            node.operand = self.visit(node.operand)
        operand = node.operand
        inscope = self.is_in_scope(operand)
        if not inscope:
            node.operand = self.try_subproc_toks(operand, strip_expr=True)
        return node

    def visit_BoolOp(self, node):
        """Handle visiting an boolean operands, like and/or."""
        for i in range(len(node.values)):
            val = node.values[i]
            if isdescendable(val):
                val = node.values[i] = self.visit(val)
            inscope = self.is_in_scope(val)
            if not inscope:
                node.values[i] = self.try_subproc_toks(val, strip_expr=True)
        return node

    #
    # Context aggregator visitors
    #

    def visit_Assign(self, node):
        """Handle visiting an assignment statement."""
        ups = set()
        for targ in node.targets:
            if isinstance(targ, (Tuple, List)):
                ups.update(leftmostname(elt) for elt in targ.elts)
            elif isinstance(targ, BinOp):
                newnode = self.try_subproc_toks(node)
                if newnode is node:
                    ups.add(leftmostname(targ))
                else:
                    return newnode
            else:
                ups.add(leftmostname(targ))
        self.ctxupdate(ups)
        return node

    visit_AnnAssign = visit_Assign

    def visit_Import(self, node):
        """Handle visiting a import statement."""
        for name in node.names:
            if name.asname is None:
                self.ctxadd(name.name)
            else:
                self.ctxadd(name.asname)
        return node

    def visit_ImportFrom(self, node):
        """Handle visiting a "from ... import ..." statement."""
        for name in node.names:
            if name.asname is None:
                self.ctxadd(name.name)
            else:
                self.ctxadd(name.asname)
        return node

    def visit_With(self, node):
        """Handle visiting a with statement."""
        for item in node.items:
            if item.optional_vars is not None:
                self.ctxupdate(gather_names(item.optional_vars))
        self._nwith += 1
        self.generic_visit(node)
        self._nwith -= 1
        return node

    def visit_For(self, node):
        """Handle visiting a for statement."""
        targ = node.target
        self.ctxupdate(gather_names(targ))
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        """Handle visiting a function definition."""
        self.ctxadd(node.name)
        self.contexts.append(set())
        args = node.args
        argchain = [args.args, args.kwonlyargs]
        if args.vararg is not None:
            argchain.append((args.vararg,))
        if args.kwarg is not None:
            argchain.append((args.kwarg,))
        self.ctxupdate(a.arg for a in itertools.chain.from_iterable(argchain))
        self.generic_visit(node)
        self.contexts.pop()
        return node

    def visit_ClassDef(self, node):
        """Handle visiting a class definition."""
        self.ctxadd(node.name)
        self.contexts.append(set())
        self.generic_visit(node)
        self.contexts.pop()
        return node

    def visit_Delete(self, node):
        """Handle visiting a del statement."""
        for targ in node.targets:
            if isinstance(targ, Name):
                self.ctxremove(targ.id)
        self.generic_visit(node)
        return node

    def visit_Try(self, node):
        """Handle visiting a try statement."""
        for handler in node.handlers:
            if handler.name is not None:
                self.ctxadd(handler.name)
        self.generic_visit(node)
        return node

    def visit_Global(self, node):
        """Handle visiting a global statement."""
        self.contexts[1].update(node.names)  # contexts[1] is the global ctx
        self.generic_visit(node)
        return node


def pdump(s, **kwargs):
    """performs a pretty dump of an AST node."""
    if isinstance(s, AST):
        s = dump(s, **kwargs).replace(",", ",\n")
    openers = "([{"
    closers = ")]}"
    lens = len(s) + 1
    if lens == 1:
        return s
    i = min([s.find(o) % lens for o in openers])
    if i == lens - 1:
        return s
    closer = closers[openers.find(s[i])]
    j = s.rfind(closer)
    if j == -1 or j <= i:
        return s[: i + 1] + "\n" + textwrap.indent(pdump(s[i + 1 :]), " ")
    pre = s[: i + 1] + "\n"
    mid = s[i + 1 : j]
    post = "\n" + s[j:]
    mid = textwrap.indent(pdump(mid), " ")
    if "(" in post or "[" in post or "{" in post:
        post = pdump(post)
    return pre + mid + post


def pprint_ast(s, *, sep=None, end=None, file=None, flush=False, **kwargs):
    """Performs a pretty print of the AST nodes."""
    print(pdump(s, **kwargs), sep=sep, end=end, file=file, flush=flush)


#
# Private helpers
#


def _getblockattr(name, lineno, col):
    """calls getattr(name, '__xonsh_block__', False)."""
    return xonsh_call(
        "getattr",
        args=[
            Name(id=name, ctx=Load(), lineno=lineno, col_offset=col),
            Str(s="__xonsh_block__", lineno=lineno, col_offset=col),
            NameConstant(value=False, lineno=lineno, col_offset=col),
        ],
        lineno=lineno,
        col=col,
    )

#
# color_tools
#
"""Tools for color handling in xonsh.

This includes Convert values between RGB hex codes and xterm-256
color codes. Parts of this file were originally forked from Micah Elliott
http://MicahElliott.com Copyright (C) 2011 Micah Elliott. All rights reserved.
WTFPL http://sam.zoy.org/wtfpl/
"""
# amalgamated re
math = _LazyModule.load('math', 'math')
# amalgamated xonsh.lazyasd
# amalgamated xonsh.tools
RE_BACKGROUND = LazyObject(
    lambda: re.compile("(BG#|BGHEX|BACKGROUND)"), globals(), "RE_BACKGROUND"
)


@lazyobject
def BASE_XONSH_COLORS():
    return {
        "BLACK": (0, 0, 0),
        "RED": (170, 0, 0),
        "GREEN": (0, 170, 0),
        "YELLOW": (170, 85, 0),
        "BLUE": (0, 0, 170),
        "PURPLE": (170, 0, 170),
        "CYAN": (0, 170, 170),
        "WHITE": (170, 170, 170),
        "INTENSE_BLACK": (85, 85, 85),
        "INTENSE_RED": (255, 85, 85),
        "INTENSE_GREEN": (85, 255, 85),
        "INTENSE_YELLOW": (255, 255, 85),
        "INTENSE_BLUE": (85, 85, 255),
        "INTENSE_PURPLE": (255, 85, 255),
        "INTENSE_CYAN": (85, 255, 255),
        "INTENSE_WHITE": (255, 255, 255),
    }


@lazyobject
def CLUT():
    """color look-up table"""
    return [
        #    8-bit, RGB hex
        # Primary 3-bit (8 colors). Unique representation!
        ("00", "000000"),
        ("01", "800000"),
        ("02", "008000"),
        ("03", "808000"),
        ("04", "000080"),
        ("05", "800080"),
        ("06", "008080"),
        ("07", "c0c0c0"),
        # Equivalent "bright" versions of original 8 colors.
        ("08", "808080"),
        ("09", "ff0000"),
        ("10", "00ff00"),
        ("11", "ffff00"),
        ("12", "0000ff"),
        ("13", "ff00ff"),
        ("14", "00ffff"),
        ("15", "ffffff"),
        # Strictly ascending.
        ("16", "000000"),
        ("17", "00005f"),
        ("18", "000087"),
        ("19", "0000af"),
        ("20", "0000d7"),
        ("21", "0000ff"),
        ("22", "005f00"),
        ("23", "005f5f"),
        ("24", "005f87"),
        ("25", "005faf"),
        ("26", "005fd7"),
        ("27", "005fff"),
        ("28", "008700"),
        ("29", "00875f"),
        ("30", "008787"),
        ("31", "0087af"),
        ("32", "0087d7"),
        ("33", "0087ff"),
        ("34", "00af00"),
        ("35", "00af5f"),
        ("36", "00af87"),
        ("37", "00afaf"),
        ("38", "00afd7"),
        ("39", "00afff"),
        ("40", "00d700"),
        ("41", "00d75f"),
        ("42", "00d787"),
        ("43", "00d7af"),
        ("44", "00d7d7"),
        ("45", "00d7ff"),
        ("46", "00ff00"),
        ("47", "00ff5f"),
        ("48", "00ff87"),
        ("49", "00ffaf"),
        ("50", "00ffd7"),
        ("51", "00ffff"),
        ("52", "5f0000"),
        ("53", "5f005f"),
        ("54", "5f0087"),
        ("55", "5f00af"),
        ("56", "5f00d7"),
        ("57", "5f00ff"),
        ("58", "5f5f00"),
        ("59", "5f5f5f"),
        ("60", "5f5f87"),
        ("61", "5f5faf"),
        ("62", "5f5fd7"),
        ("63", "5f5fff"),
        ("64", "5f8700"),
        ("65", "5f875f"),
        ("66", "5f8787"),
        ("67", "5f87af"),
        ("68", "5f87d7"),
        ("69", "5f87ff"),
        ("70", "5faf00"),
        ("71", "5faf5f"),
        ("72", "5faf87"),
        ("73", "5fafaf"),
        ("74", "5fafd7"),
        ("75", "5fafff"),
        ("76", "5fd700"),
        ("77", "5fd75f"),
        ("78", "5fd787"),
        ("79", "5fd7af"),
        ("80", "5fd7d7"),
        ("81", "5fd7ff"),
        ("82", "5fff00"),
        ("83", "5fff5f"),
        ("84", "5fff87"),
        ("85", "5fffaf"),
        ("86", "5fffd7"),
        ("87", "5fffff"),
        ("88", "870000"),
        ("89", "87005f"),
        ("90", "870087"),
        ("91", "8700af"),
        ("92", "8700d7"),
        ("93", "8700ff"),
        ("94", "875f00"),
        ("95", "875f5f"),
        ("96", "875f87"),
        ("97", "875faf"),
        ("98", "875fd7"),
        ("99", "875fff"),
        ("100", "878700"),
        ("101", "87875f"),
        ("102", "878787"),
        ("103", "8787af"),
        ("104", "8787d7"),
        ("105", "8787ff"),
        ("106", "87af00"),
        ("107", "87af5f"),
        ("108", "87af87"),
        ("109", "87afaf"),
        ("110", "87afd7"),
        ("111", "87afff"),
        ("112", "87d700"),
        ("113", "87d75f"),
        ("114", "87d787"),
        ("115", "87d7af"),
        ("116", "87d7d7"),
        ("117", "87d7ff"),
        ("118", "87ff00"),
        ("119", "87ff5f"),
        ("120", "87ff87"),
        ("121", "87ffaf"),
        ("122", "87ffd7"),
        ("123", "87ffff"),
        ("124", "af0000"),
        ("125", "af005f"),
        ("126", "af0087"),
        ("127", "af00af"),
        ("128", "af00d7"),
        ("129", "af00ff"),
        ("130", "af5f00"),
        ("131", "af5f5f"),
        ("132", "af5f87"),
        ("133", "af5faf"),
        ("134", "af5fd7"),
        ("135", "af5fff"),
        ("136", "af8700"),
        ("137", "af875f"),
        ("138", "af8787"),
        ("139", "af87af"),
        ("140", "af87d7"),
        ("141", "af87ff"),
        ("142", "afaf00"),
        ("143", "afaf5f"),
        ("144", "afaf87"),
        ("145", "afafaf"),
        ("146", "afafd7"),
        ("147", "afafff"),
        ("148", "afd700"),
        ("149", "afd75f"),
        ("150", "afd787"),
        ("151", "afd7af"),
        ("152", "afd7d7"),
        ("153", "afd7ff"),
        ("154", "afff00"),
        ("155", "afff5f"),
        ("156", "afff87"),
        ("157", "afffaf"),
        ("158", "afffd7"),
        ("159", "afffff"),
        ("160", "d70000"),
        ("161", "d7005f"),
        ("162", "d70087"),
        ("163", "d700af"),
        ("164", "d700d7"),
        ("165", "d700ff"),
        ("166", "d75f00"),
        ("167", "d75f5f"),
        ("168", "d75f87"),
        ("169", "d75faf"),
        ("170", "d75fd7"),
        ("171", "d75fff"),
        ("172", "d78700"),
        ("173", "d7875f"),
        ("174", "d78787"),
        ("175", "d787af"),
        ("176", "d787d7"),
        ("177", "d787ff"),
        ("178", "d7af00"),
        ("179", "d7af5f"),
        ("180", "d7af87"),
        ("181", "d7afaf"),
        ("182", "d7afd7"),
        ("183", "d7afff"),
        ("184", "d7d700"),
        ("185", "d7d75f"),
        ("186", "d7d787"),
        ("187", "d7d7af"),
        ("188", "d7d7d7"),
        ("189", "d7d7ff"),
        ("190", "d7ff00"),
        ("191", "d7ff5f"),
        ("192", "d7ff87"),
        ("193", "d7ffaf"),
        ("194", "d7ffd7"),
        ("195", "d7ffff"),
        ("196", "ff0000"),
        ("197", "ff005f"),
        ("198", "ff0087"),
        ("199", "ff00af"),
        ("200", "ff00d7"),
        ("201", "ff00ff"),
        ("202", "ff5f00"),
        ("203", "ff5f5f"),
        ("204", "ff5f87"),
        ("205", "ff5faf"),
        ("206", "ff5fd7"),
        ("207", "ff5fff"),
        ("208", "ff8700"),
        ("209", "ff875f"),
        ("210", "ff8787"),
        ("211", "ff87af"),
        ("212", "ff87d7"),
        ("213", "ff87ff"),
        ("214", "ffaf00"),
        ("215", "ffaf5f"),
        ("216", "ffaf87"),
        ("217", "ffafaf"),
        ("218", "ffafd7"),
        ("219", "ffafff"),
        ("220", "ffd700"),
        ("221", "ffd75f"),
        ("222", "ffd787"),
        ("223", "ffd7af"),
        ("224", "ffd7d7"),
        ("225", "ffd7ff"),
        ("226", "ffff00"),
        ("227", "ffff5f"),
        ("228", "ffff87"),
        ("229", "ffffaf"),
        ("230", "ffffd7"),
        ("231", "ffffff"),
        # Gray-scale range.
        ("232", "080808"),
        ("233", "121212"),
        ("234", "1c1c1c"),
        ("235", "262626"),
        ("236", "303030"),
        ("237", "3a3a3a"),
        ("238", "444444"),
        ("239", "4e4e4e"),
        ("240", "585858"),
        ("241", "626262"),
        ("242", "6c6c6c"),
        ("243", "767676"),
        ("244", "808080"),
        ("245", "8a8a8a"),
        ("246", "949494"),
        ("247", "9e9e9e"),
        ("248", "a8a8a8"),
        ("249", "b2b2b2"),
        ("250", "bcbcbc"),
        ("251", "c6c6c6"),
        ("252", "d0d0d0"),
        ("253", "dadada"),
        ("254", "e4e4e4"),
        ("255", "eeeeee"),
    ]


def _str2hex(hexstr):
    return int(hexstr, 16)


def _strip_hash(rgb):
    # Strip leading `#` if exists.
    if rgb.startswith("#"):
        rgb = rgb.lstrip("#")
    return rgb


@lazyobject
def SHORT_TO_RGB():
    return dict(CLUT)


@lazyobject
def RGB_TO_SHORT():
    return {v: k for k, v in SHORT_TO_RGB.items()}


def short2rgb(short):
    return SHORT_TO_RGB[short]


def rgb_to_256(rgb):
    """Find the closest ANSI 256 approximation to the given RGB value.

        >>> rgb2short('123456')
        ('23', '005f5f')
        >>> rgb2short('ffffff')
        ('231', 'ffffff')
        >>> rgb2short('0DADD6') # vimeo logo
        ('38', '00afd7')

    Parameters
    ----------
    rgb : Hex code representing an RGB value, eg, 'abcdef'

    Returns
    -------
    String between 0 and 255, compatible with xterm.
    """
    rgb = rgb.lstrip("#")
    if len(rgb) == 0:
        return "0", "000000"
    incs = (0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF)
    # Break 6-char RGB code into 3 integer vals.
    parts = rgb_to_ints(rgb)
    res = []
    for part in parts:
        i = 0
        while i < len(incs) - 1:
            s, b = incs[i], incs[i + 1]  # smaller, bigger
            if s <= part <= b:
                s1 = abs(s - part)
                b1 = abs(b - part)
                if s1 < b1:
                    closest = s
                else:
                    closest = b
                res.append(closest)
                break
            i += 1
    res = "".join([("%02.x" % i) for i in res])
    equiv = RGB_TO_SHORT[res]
    return equiv, res


rgb2short = rgb_to_256


@lazyobject
def RE_RGB3():
    return re.compile(r"(.)(.)(.)")


@lazyobject
def RE_RGB6():
    return re.compile(r"(..)(..)(..)")


def rgb_to_ints(rgb):
    if len(rgb) == 6:
        return tuple([int(h, 16) for h in RE_RGB6.split(rgb)[1:4]])
    else:
        return tuple([int(h * 2, 16) for h in RE_RGB3.split(rgb)[1:4]])


def color_dist(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2)


def find_closest_color(x, palette):
    return min(sorted(palette.keys())[::-1], key=lambda k: color_dist(x, palette[k]))


def make_palette(strings):
    """Makes a color palette from a collection of strings."""
    palette = {}
    for s in strings:
        while "#" in s:
            _, t = s.split("#", 1)
            t, _, s = t.partition(" ")
            palette[t] = rgb_to_ints(t)
    return palette


@deprecated(deprecated_in="0.5.10", removed_in="0.6.0")
def make_pallete(*args, **kwargs):
    make_palette(*args, **kwargs)

#
# commands_cache
#
# -*- coding: utf-8 -*-
"""Module for caching command & alias names as well as for predicting whether
a command will be able to be run in the background.

A background predictor is a function that accepts a single argument list
and returns whether or not the process can be run in the background (returns
True) or must be run the foreground (returns False).
"""
# amalgamated os
# amalgamated time
# amalgamated builtins
argparse = _LazyModule.load('argparse', 'argparse')
# amalgamated collections.abc
# amalgamated xonsh.platform
# amalgamated xonsh.tools
# amalgamated xonsh.lazyasd
class CommandsCache(cabc.Mapping):
    """A lazy cache representing the commands available on the file system.
    The keys are the command names and the values a tuple of (loc, has_alias)
    where loc is either a str pointing to the executable on the file system or
    None (if no executable exists) and has_alias is a boolean flag for whether
    the command has an alias.
    """

    def __init__(self):
        self._cmds_cache = {}
        self._path_checksum = None
        self._alias_checksum = None
        self._path_mtime = -1
        self.threadable_predictors = default_threadable_predictors()

    def __contains__(self, key):
        _ = self.all_commands
        return self.lazyin(key)

    def __iter__(self):
        for cmd, (path, is_alias) in self.all_commands.items():
            if ON_WINDOWS and path is not None:
                # All command keys are stored in uppercase on Windows.
                # This ensures the original command name is returned.
                cmd = pathbasename(path)
            yield cmd

    def __len__(self):
        return len(self.all_commands)

    def __getitem__(self, key):
        _ = self.all_commands
        return self.lazyget(key)

    def is_empty(self):
        """Returns whether the cache is populated or not."""
        return len(self._cmds_cache) == 0

    @staticmethod
    def get_possible_names(name):
        """Generates the possible `PATHEXT` extension variants of a given executable
         name on Windows as a list, conserving the ordering in `PATHEXT`.
         Returns a list as `name` being the only item in it on other platforms."""
        if ON_WINDOWS:
            pathext = builtins.__xonsh__.env.get("PATHEXT", [])
            name = name.upper()
            return [name + ext for ext in ([""] + pathext)]
        else:
            return [name]

    @staticmethod
    def remove_dups(p):
        ret = list()
        for e in p:
            if e not in ret:
                ret.append(e)
        return ret

    @property
    def all_commands(self):
        paths = builtins.__xonsh__.env.get("PATH", [])
        paths = CommandsCache.remove_dups(paths)
        path_immut = tuple(x for x in paths if os.path.isdir(x))
        # did PATH change?
        path_hash = hash(path_immut)
        cache_valid = path_hash == self._path_checksum
        self._path_checksum = path_hash
        # did aliases change?
        alss = getattr(builtins, "aliases", dict())
        al_hash = hash(frozenset(alss))
        cache_valid = cache_valid and al_hash == self._alias_checksum
        self._alias_checksum = al_hash
        # did the contents of any directory in PATH change?
        max_mtime = 0
        for path in path_immut:
            mtime = os.stat(path).st_mtime
            if mtime > max_mtime:
                max_mtime = mtime
        cache_valid = cache_valid and (max_mtime <= self._path_mtime)
        self._path_mtime = max_mtime
        if cache_valid:
            return self._cmds_cache
        allcmds = {}
        for path in reversed(path_immut):
            # iterate backwards so that entries at the front of PATH overwrite
            # entries at the back.
            for cmd in executables_in(path):
                key = cmd.upper() if ON_WINDOWS else cmd
                allcmds[key] = (os.path.join(path, cmd), alss.get(key, None))
        for cmd in alss:
            if cmd not in allcmds:
                key = cmd.upper() if ON_WINDOWS else cmd
                allcmds[key] = (cmd, True)
        self._cmds_cache = allcmds
        return allcmds

    def cached_name(self, name):
        """Returns the name that would appear in the cache, if it exists."""
        if name is None:
            return None
        cached = pathbasename(name)
        if ON_WINDOWS:
            keys = self.get_possible_names(cached)
            cached = next((k for k in keys if k in self._cmds_cache), None)
        return cached

    def lazyin(self, key):
        """Checks if the value is in the current cache without the potential to
        update the cache. It just says whether the value is known *now*. This
        may not reflect precisely what is on the $PATH.
        """
        return self.cached_name(key) in self._cmds_cache

    def lazyiter(self):
        """Returns an iterator over the current cache contents without the
        potential to update the cache. This may not reflect what is on the
        $PATH.
        """
        return iter(self._cmds_cache)

    def lazylen(self):
        """Returns the length of the current cache contents without the
        potential to update the cache. This may not reflect precisely
        what is on the $PATH.
        """
        return len(self._cmds_cache)

    def lazyget(self, key, default=None):
        """A lazy value getter."""
        return self._cmds_cache.get(self.cached_name(key), default)

    def locate_binary(self, name, ignore_alias=False):
        """Locates an executable on the file system using the cache.

        Arguments
        ---------
        name : str
                name of binary to search for
        ignore_alias : bool, optional
                Force return of binary path even if alias of ``name`` exists
                (default ``False``)
        """
        # make sure the cache is up to date by accessing the property
        _ = self.all_commands
        return self.lazy_locate_binary(name, ignore_alias)

    def lazy_locate_binary(self, name, ignore_alias=False):
        """Locates an executable in the cache, without checking its validity.

        Arguments
        ---------
        name : str
                name of binary to search for
        ignore_alias : bool, optional
                Force return of binary path even if alias of ``name`` exists
                (default ``False``)
        """
        possibilities = self.get_possible_names(name)
        if ON_WINDOWS:
            # Windows users expect to be able to execute files in the same
            # directory without `./`
            local_bin = next((fn for fn in possibilities if os.path.isfile(fn)), None)
            if local_bin:
                return os.path.abspath(local_bin)
        cached = next((cmd for cmd in possibilities if cmd in self._cmds_cache), None)
        if cached:
            (path, alias) = self._cmds_cache[cached]
            ispure = path == pathbasename(path)
            if alias and ignore_alias and ispure:
                # pure alias, which we are ignoring
                return None
            else:
                return path
        elif os.path.isfile(name) and name != pathbasename(name):
            return name

    def is_only_functional_alias(self, name):
        """Returns whether or not a command is only a functional alias, and has
        no underlying executable. For example, the "cd" command is only available
        as a functional alias.
        """
        _ = self.all_commands
        return self.lazy_is_only_functional_alias(name)

    def lazy_is_only_functional_alias(self, name):
        """Returns whether or not a command is only a functional alias, and has
        no underlying executable. For example, the "cd" command is only available
        as a functional alias. This search is performed lazily.
        """
        val = self._cmds_cache.get(name, None)
        if val is None:
            return False
        return (
            val == (name, True) and self.locate_binary(name, ignore_alias=True) is None
        )

    def predict_threadable(self, cmd):
        """Predicts whether a command list is able to be run on a background
        thread, rather than the main thread.
        """
        name = self.cached_name(cmd[0])
        predictors = self.threadable_predictors
        if ON_WINDOWS:
            # On all names (keys) are stored in upper case so instead
            # we get the original cmd or alias name
            path, _ = self.lazyget(name, (None, None))
            if path is None:
                return True
            else:
                name = pathbasename(path)
            if name not in predictors:
                pre, ext = os.path.splitext(name)
                if pre in predictors:
                    predictors[name] = predictors[pre]
        if name not in predictors:
            predictors[name] = self.default_predictor(name, cmd[0])
        predictor = predictors[name]
        return predictor(cmd[1:])

    #
    # Background Predictors (as methods)
    #

    def default_predictor(self, name, cmd0):
        if ON_POSIX:
            return self.default_predictor_readbin(
                name, cmd0, timeout=0.1, failure=predict_true
            )
        else:
            return predict_true

    def default_predictor_readbin(self, name, cmd0, timeout, failure):
        """Make a default predictor by
        analyzing the content of the binary. Should only works on POSIX.
        Return failure if the analysis fails.
        """
        fname = cmd0 if os.path.isabs(cmd0) else None
        fname = cmd0 if fname is None and os.sep in cmd0 else fname
        fname = self.lazy_locate_binary(name) if fname is None else fname

        if fname is None:
            return failure
        if not os.path.isfile(fname):
            return failure

        try:
            fd = os.open(fname, os.O_RDONLY | os.O_NONBLOCK)
        except Exception:
            return failure  # opening error

        search_for = {
            (b"ncurses",): [False],
            (b"libgpm",): [False],
            (b"isatty", b"tcgetattr", b"tcsetattr"): [False, False, False],
        }
        tstart = time.time()
        block = b""
        while time.time() < tstart + timeout:
            previous_block = block
            try:
                block = os.read(fd, 2048)
            except Exception:
                # should not occur, except e.g. if a file is deleted a a dir is
                # created with the same name between os.path.isfile and os.open
                os.close(fd)
                return failure
            if len(block) == 0:
                os.close(fd)
                return predict_true  # no keys of search_for found
            analyzed_block = previous_block + block
            for k, v in search_for.items():
                for i in range(len(k)):
                    if v[i]:
                        continue
                    if k[i] in analyzed_block:
                        v[i] = True
                if all(v):
                    os.close(fd)
                    return predict_false  # use one key of search_for
        os.close(fd)
        return failure  # timeout


#
# Background Predictors
#


def predict_true(args):
    """Always say the process is threadable."""
    return True


def predict_false(args):
    """Never say the process is threadable."""
    return False


@lazyobject
def SHELL_PREDICTOR_PARSER():
    p = argparse.ArgumentParser("shell", add_help=False)
    p.add_argument("-c", nargs="?", default=None)
    p.add_argument("filename", nargs="?", default=None)
    return p


def predict_shell(args):
    """Predict the backgroundability of the normal shell interface, which
    comes down to whether it is being run in subproc mode.
    """
    ns, _ = SHELL_PREDICTOR_PARSER.parse_known_args(args)
    if ns.c is None and ns.filename is None:
        pred = False
    else:
        pred = True
    return pred


@lazyobject
def HELP_VER_PREDICTOR_PARSER():
    p = argparse.ArgumentParser("cmd", add_help=False)
    p.add_argument("-h", "--help", dest="help", action="store_true", default=None)
    p.add_argument(
        "-v", "-V", "--version", dest="version", action="store_true", default=None
    )
    return p


def predict_help_ver(args):
    """Predict the backgroundability of commands that have help & version
    switches: -h, --help, -v, -V, --version. If either of these options is
    present, the command is assumed to print to stdout normally and is therefore
    threadable. Otherwise, the command is assumed to not be threadable.
    This is useful for commands, like top, that normally enter alternate mode
    but may not in certain circumstances.
    """
    ns, _ = HELP_VER_PREDICTOR_PARSER.parse_known_args(args)
    pred = ns.help is not None or ns.version is not None
    return pred


@lazyobject
def HG_PREDICTOR_PARSER():
    p = argparse.ArgumentParser("hg", add_help=False)
    p.add_argument("command")
    p.add_argument(
        "-i", "--interactive", action="store_true", default=False, dest="interactive"
    )
    return p


def predict_hg(args):
    """Predict if mercurial is about to be run in interactive mode.
    If it is interactive, predict False. If it isn't, predict True.
    Also predict False for certain commands, such as split.
    """
    ns, _ = HG_PREDICTOR_PARSER.parse_known_args(args)
    if ns.command == "split":
        return False
    else:
        return not ns.interactive


def default_threadable_predictors():
    """Generates a new defaultdict for known threadable predictors.
    The default is to predict true.
    """
    # alphabetical, for what it is worth.
    predictors = {
        "aurman": predict_false,
        "bash": predict_shell,
        "csh": predict_shell,
        "clear": predict_false,
        "cls": predict_false,
        "cmd": predict_shell,
        "cryptop": predict_false,
        "curl": predict_true,
        "ex": predict_false,
        "emacsclient": predict_false,
        "fish": predict_shell,
        "gvim": predict_help_ver,
        "hg": predict_hg,
        "htop": predict_help_ver,
        "ipython": predict_shell,
        "ksh": predict_shell,
        "less": predict_help_ver,
        "man": predict_help_ver,
        "more": predict_help_ver,
        "mvim": predict_help_ver,
        "mutt": predict_help_ver,
        "nano": predict_help_ver,
        "nvim": predict_false,
        "ponysay": predict_help_ver,
        "psql": predict_false,
        "python": predict_shell,
        "python2": predict_shell,
        "python3": predict_shell,
        "repo": predict_help_ver,
        "ranger": predict_help_ver,
        "rview": predict_false,
        "rvim": predict_false,
        "scp": predict_false,
        "sh": predict_shell,
        "ssh": predict_false,
        "startx": predict_false,
        "sudo": predict_help_ver,
        "tcsh": predict_shell,
        "telnet": predict_false,
        "top": predict_help_ver,
        "vi": predict_false,
        "view": predict_false,
        "vim": predict_false,
        "vimpager": predict_help_ver,
        "weechat": predict_help_ver,
        "xclip": predict_help_ver,
        "xo": predict_help_ver,
        "xonsh": predict_shell,
        "xon.sh": predict_shell,
        "zsh": predict_shell,
    }
    return predictors

#
# diff_history
#
# -*- coding: utf-8 -*-
"""Tools for diff'ing two xonsh history files in a meaningful fashion."""
difflib = _LazyModule.load('difflib', 'difflib')
# amalgamated datetime
# amalgamated itertools
# amalgamated argparse
# amalgamated xonsh.lazyjson
# amalgamated xonsh.tools
NO_COLOR_S = "{NO_COLOR}"
RED_S = "{RED}"
GREEN_S = "{GREEN}"
BOLD_RED_S = "{BOLD_RED}"
BOLD_GREEN_S = "{BOLD_GREEN}"

# intern some strings
REPLACE_S = "replace"
DELETE_S = "delete"
INSERT_S = "insert"
EQUAL_S = "equal"


def bold_str_diff(a, b, sm=None):
    if sm is None:
        sm = difflib.SequenceMatcher()
    aline = RED_S + "- "
    bline = GREEN_S + "+ "
    sm.set_seqs(a, b)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == REPLACE_S:
            aline += BOLD_RED_S + a[i1:i2] + RED_S
            bline += BOLD_GREEN_S + b[j1:j2] + GREEN_S
        elif tag == DELETE_S:
            aline += BOLD_RED_S + a[i1:i2] + RED_S
        elif tag == INSERT_S:
            bline += BOLD_GREEN_S + b[j1:j2] + GREEN_S
        elif tag == EQUAL_S:
            aline += a[i1:i2]
            bline += b[j1:j2]
        else:
            raise RuntimeError("tag not understood")
    return aline + NO_COLOR_S + "\n" + bline + NO_COLOR_S + "\n"


def redline(line):
    return "{red}- {line}{no_color}\n".format(red=RED_S, line=line, no_color=NO_COLOR_S)


def greenline(line):
    return "{green}+ {line}{no_color}\n".format(
        green=GREEN_S, line=line, no_color=NO_COLOR_S
    )


def highlighted_ndiff(a, b):
    """Returns a highlighted string, with bold characters where different."""
    s = ""
    sm = difflib.SequenceMatcher()
    sm.set_seqs(a, b)
    linesm = difflib.SequenceMatcher()
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == REPLACE_S:
            for aline, bline in itertools.zip_longest(a[i1:i2], b[j1:j2]):
                if bline is None:
                    s += redline(aline)
                elif aline is None:
                    s += greenline(bline)
                else:
                    s += bold_str_diff(aline, bline, sm=linesm)
        elif tag == DELETE_S:
            for aline in a[i1:i2]:
                s += redline(aline)
        elif tag == INSERT_S:
            for bline in b[j1:j2]:
                s += greenline(bline)
        elif tag == EQUAL_S:
            for aline in a[i1:i2]:
                s += "  " + aline + "\n"
        else:
            raise RuntimeError("tag not understood")
    return s


class HistoryDiffer(object):
    """This class helps diff two xonsh history files."""

    def __init__(self, afile, bfile, reopen=False, verbose=False):
        """
        Parameters
        ----------
        afile : file handle or str
            The first file to diff
        bfile : file handle or str
            The second file to diff
        reopen : bool, optional
            Whether or not to reopen the file handles each time. The default here is
            opposite from the LazyJSON default because we know that we will be doing
            a lot of reading so it is best to keep the handles open.
        verbose : bool, optional
            Whether to print a verbose amount of information.
        """
        self.a = LazyJSON(afile, reopen=reopen)
        self.b = LazyJSON(bfile, reopen=reopen)
        self.verbose = verbose
        self.sm = difflib.SequenceMatcher(autojunk=False)

    def __del__(self):
        self.a.close()
        self.b.close()

    def __str__(self):
        return self.format()

    def _header_line(self, lj):
        s = lj._f.name if hasattr(lj._f, "name") else ""
        s += " (" + lj["sessionid"] + ")"
        s += " [locked]" if lj["locked"] else " [unlocked]"
        ts = lj["ts"].load()
        ts0 = datetime.datetime.fromtimestamp(ts[0])
        s += " started: " + ts0.isoformat(" ")
        if ts[1] is not None:
            ts1 = datetime.datetime.fromtimestamp(ts[1])
            s += " stopped: " + ts1.isoformat(" ") + " runtime: " + str(ts1 - ts0)
        return s

    def header(self):
        """Computes a header string difference."""
        s = "{red}--- {aline}{no_color}\n" "{green}+++ {bline}{no_color}"
        s = s.format(
            aline=self._header_line(self.a),
            bline=self._header_line(self.b),
            red=RED_S,
            green=GREEN_S,
            no_color=NO_COLOR_S,
        )
        return s

    def _env_both_diff(self, in_both, aenv, benv):
        sm = self.sm
        s = ""
        for key in sorted(in_both):
            aval = aenv[key]
            bval = benv[key]
            if aval == bval:
                continue
            s += "{0!r} is in both, but differs\n".format(key)
            s += bold_str_diff(aval, bval, sm=sm) + "\n"
        return s

    def _env_in_one_diff(self, x, y, color, xid, xenv):
        only_x = sorted(x - y)
        if len(only_x) == 0:
            return ""
        if self.verbose:
            xstr = ",\n".join(
                ["    {0!r}: {1!r}".format(key, xenv[key]) for key in only_x]
            )
            xstr = "\n" + xstr
        else:
            xstr = ", ".join(["{0!r}".format(key) for key in only_x])
        in_x = "These vars are only in {color}{xid}{no_color}: {{{xstr}}}\n\n"
        return in_x.format(xid=xid, color=color, no_color=NO_COLOR_S, xstr=xstr)

    def envdiff(self):
        """Computes the difference between the environments."""
        aenv = self.a["env"].load()
        benv = self.b["env"].load()
        akeys = frozenset(aenv)
        bkeys = frozenset(benv)
        in_both = akeys & bkeys
        if len(in_both) == len(akeys) == len(bkeys):
            keydiff = self._env_both_diff(in_both, aenv, benv)
            if len(keydiff) == 0:
                return ""
            in_a = in_b = ""
        else:
            keydiff = self._env_both_diff(in_both, aenv, benv)
            in_a = self._env_in_one_diff(akeys, bkeys, RED_S, self.a["sessionid"], aenv)
            in_b = self._env_in_one_diff(
                bkeys, akeys, GREEN_S, self.b["sessionid"], benv
            )
        s = "Environment\n-----------\n" + in_a + keydiff + in_b
        return s

    def _cmd_in_one_diff(self, inp, i, xlj, xid, color):
        s = "cmd #{i} only in {color}{xid}{no_color}:\n"
        s = s.format(i=i, color=color, xid=xid, no_color=NO_COLOR_S)
        lines = inp.splitlines()
        lt = "{color}{pre}{no_color} {line}\n"
        s += lt.format(color=color, no_color=NO_COLOR_S, line=lines[0], pre=">>>")
        for line in lines[1:]:
            s += lt.format(color=color, no_color=NO_COLOR_S, line=line, pre="...")
        if not self.verbose:
            return s + "\n"
        out = xlj["cmds"][0].get("out", "Note: no output stored")
        s += out.rstrip() + "\n\n"
        return s

    def _cmd_out_and_rtn_diff(self, i, j):
        s = ""
        aout = self.a["cmds"][i].get("out", None)
        bout = self.b["cmds"][j].get("out", None)
        if aout is None and bout is None:
            # s += 'Note: neither output stored\n'
            pass
        elif bout is None:
            aid = self.a["sessionid"]
            s += "Note: only {red}{aid}{no_color} output stored\n".format(
                red=RED_S, aid=aid, no_color=NO_COLOR_S
            )
        elif aout is None:
            bid = self.b["sessionid"]
            s += "Note: only {green}{bid}{no_color} output stored\n".format(
                green=GREEN_S, bid=bid, no_color=NO_COLOR_S
            )
        elif aout != bout:
            s += "Outputs differ\n"
            s += highlighted_ndiff(aout.splitlines(), bout.splitlines())
        else:
            pass
        artn = self.a["cmds"][i]["rtn"]
        brtn = self.b["cmds"][j]["rtn"]
        if artn != brtn:
            s += (
                "Return vals {red}{artn}{no_color} & {green}{brtn}{no_color} differ\n"
            ).format(
                red=RED_S, green=GREEN_S, no_color=NO_COLOR_S, artn=artn, brtn=brtn
            )
        return s

    def _cmd_replace_diff(self, i, ainp, aid, j, binp, bid):
        s = (
            "cmd #{i} in {red}{aid}{no_color} is replaced by \n"
            "cmd #{j} in {green}{bid}{no_color}:\n"
        )
        s = s.format(
            i=i, aid=aid, j=j, bid=bid, red=RED_S, green=GREEN_S, no_color=NO_COLOR_S
        )
        s += highlighted_ndiff(ainp.splitlines(), binp.splitlines())
        if not self.verbose:
            return s + "\n"
        s += self._cmd_out_and_rtn_diff(i, j)
        return s + "\n"

    def cmdsdiff(self):
        """Computes the difference of the commands themselves."""
        aid = self.a["sessionid"]
        bid = self.b["sessionid"]
        ainps = [c["inp"] for c in self.a["cmds"]]
        binps = [c["inp"] for c in self.b["cmds"]]
        sm = self.sm
        sm.set_seqs(ainps, binps)
        s = ""
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == REPLACE_S:
                zipper = itertools.zip_longest
                for i, ainp, j, binp in zipper(
                    range(i1, i2), ainps[i1:i2], range(j1, j2), binps[j1:j2]
                ):
                    if j is None:
                        s += self._cmd_in_one_diff(ainp, i, self.a, aid, RED_S)
                    elif i is None:
                        s += self._cmd_in_one_diff(binp, j, self.b, bid, GREEN_S)
                    else:
                        self._cmd_replace_diff(i, ainp, aid, j, binp, bid)
            elif tag == DELETE_S:
                for i, inp in enumerate(ainps[i1:i2], i1):
                    s += self._cmd_in_one_diff(inp, i, self.a, aid, RED_S)
            elif tag == INSERT_S:
                for j, inp in enumerate(binps[j1:j2], j1):
                    s += self._cmd_in_one_diff(inp, j, self.b, bid, GREEN_S)
            elif tag == EQUAL_S:
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    odiff = self._cmd_out_and_rtn_diff(i, j)
                    if len(odiff) > 0:
                        h = (
                            "cmd #{i} in {red}{aid}{no_color} input is the same as \n"
                            "cmd #{j} in {green}{bid}{no_color}, but output differs:\n"
                        )
                        s += h.format(
                            i=i,
                            aid=aid,
                            j=j,
                            bid=bid,
                            red=RED_S,
                            green=GREEN_S,
                            no_color=NO_COLOR_S,
                        )
                        s += odiff + "\n"
            else:
                raise RuntimeError("tag not understood")
        if len(s) == 0:
            return s
        return "Commands\n--------\n" + s

    def format(self):
        """Formats the difference between the two history files."""
        s = self.header()
        ed = self.envdiff()
        if len(ed) > 0:
            s += "\n\n" + ed
        cd = self.cmdsdiff()
        if len(cd) > 0:
            s += "\n\n" + cd
        return s.rstrip()


_HD_PARSER = None


def dh_create_parser(p=None):
    global _HD_PARSER
    p_was_none = p is None
    if _HD_PARSER is not None and p_was_none:
        return _HD_PARSER
    if p_was_none:
        p = argparse.ArgumentParser(
            "diff-history", description="diffs two xonsh history files"
        )
    p.add_argument(
        "--reopen",
        dest="reopen",
        default=False,
        action="store_true",
        help="make lazy file loading reopen files each time",
    )
    p.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        default=False,
        action="store_true",
        help="whether to print even more information",
    )
    p.add_argument("a", help="first file in diff")
    p.add_argument("b", help="second file in diff")
    if p_was_none:
        _HD_PARSER = p
    return p


def dh_main_action(ns, hist=None, stdout=None, stderr=None):
    hd = HistoryDiffer(ns.a, ns.b, reopen=ns.reopen, verbose=ns.verbose)
    print_color(hd.format(), file=stdout)

#
# events
#
"""
Events for xonsh.

In all likelihood, you want builtins.events

The best way to "declare" an event is something like::

    events.doc('on_spam', "Comes with eggs")
"""
abc = _LazyModule.load('abc', 'abc')
# amalgamated builtins
collections = _LazyModule.load('collections', 'collections.abc')
inspect = _LazyModule.load('inspect', 'inspect')
# amalgamated xonsh.tools
def has_kwargs(func):
    return any(
        p.kind == p.VAR_KEYWORD for p in inspect.signature(func).parameters.values()
    )


def debug_level():
    if hasattr(builtins.__xonsh__, "env"):
        return builtins.__xonsh__.env.get("XONSH_DEBUG")
    # FIXME: Under py.test, return 1(?)
    else:
        return 0  # Optimize for speed, not guaranteed correctness


class AbstractEvent(collections.abc.MutableSet, abc.ABC):
    """
    A given event that handlers can register against.

    Acts as a ``MutableSet`` for registered handlers.

    Note that ordering is never guaranteed.
    """

    @property
    def species(self):
        """
        The species (basically, class) of the event
        """
        return type(self).__bases__[
            0
        ]  # events.on_chdir -> <class on_chdir> -> <class Event>

    def __call__(self, handler):
        """
        Registers a handler. It's suggested to use this as a decorator.

        A decorator method is added to the handler, validator(). If a validator
        function is added, it can filter if the handler will be considered. The
        validator takes the same arguments as the handler. If it returns False,
        the handler will not called or considered, as if it was not registered
        at all.

        Parameters
        ----------
        handler : callable
            The handler to register

        Returns
        -------
        rtn : callable
            The handler
        """
        #  Using Python's "private" munging to minimize hypothetical collisions
        handler.__validator = None
        if debug_level():
            if not has_kwargs(handler):
                raise ValueError("Event handlers need a **kwargs for future proofing")
        self.add(handler)

        def validator(vfunc):
            """
            Adds a validator function to a handler to limit when it is considered.
            """
            if debug_level():
                if not has_kwargs(handler):
                    raise ValueError(
                        "Event validators need a **kwargs for future proofing"
                    )
            handler.__validator = vfunc

        handler.validator = validator

        return handler

    def _filterhandlers(self, handlers, **kwargs):
        """
        Helper method for implementing classes. Generates the handlers that pass validation.
        """
        for handler in handlers:
            if handler.__validator is not None and not handler.__validator(**kwargs):
                continue
            yield handler

    @abc.abstractmethod
    def fire(self, **kwargs):
        """
        Fires an event, calling registered handlers with the given arguments.

        Parameters
        ----------
        **kwargs :
            Keyword arguments to pass to each handler
        """


class Event(AbstractEvent):
    """
    An event species for notify and scatter-gather events.
    """

    # Wish I could just pull from set...
    def __init__(self):
        self._handlers = set()

    def __len__(self):
        return len(self._handlers)

    def __contains__(self, item):
        return item in self._handlers

    def __iter__(self):
        yield from self._handlers

    def add(self, item):
        """
        Add an element to a set.

        This has no effect if the element is already present.
        """
        self._handlers.add(item)

    def discard(self, item):
        """
        Remove an element from a set if it is a member.

        If the element is not a member, do nothing.
        """
        self._handlers.discard(item)

    def fire(self, **kwargs):
        """
        Fires an event, calling registered handlers with the given arguments. A non-unique iterable
        of the results is returned.

        Each handler is called immediately. Exceptions are turned in to warnings.

        Parameters
        ----------
        **kwargs :
            Keyword arguments to pass to each handler

        Returns
        -------
        vals : iterable
            Return values of each handler. If multiple handlers return the same value, it will
            appear multiple times.
        """
        vals = []
        for handler in self._filterhandlers(self._handlers, **kwargs):
            try:
                rv = handler(**kwargs)
            except Exception:
                print_exception("Exception raised in event handler; ignored.")
            else:
                vals.append(rv)
        return vals


class LoadEvent(AbstractEvent):
    """
    An event species where each handler is called exactly once, shortly after either the event is
    fired or the handler is registered (whichever is later). Additional firings are ignored.

    Note: Does not support scatter/gather, due to never knowing when we have all the handlers.

    Note: Maintains a strong reference to pargs/kwargs in case of the addition of future handlers.

    Note: This is currently NOT thread safe.
    """

    def __init__(self):
        self._fired = set()
        self._unfired = set()
        self._hasfired = False

    def __len__(self):
        return len(self._fired) + len(self._unfired)

    def __contains__(self, item):
        return item in self._fired or item in self._unfired

    def __iter__(self):
        yield from self._fired
        yield from self._unfired

    def add(self, item):
        """
        Add an element to a set.

        This has no effect if the element is already present.
        """
        if self._hasfired:
            self._call(item)
            self._fired.add(item)
        else:
            self._unfired.add(item)

    def discard(self, item):
        """
        Remove an element from a set if it is a member.

        If the element is not a member, do nothing.
        """
        self._fired.discard(item)
        self._unfired.discard(item)

    def _call(self, handler):
        try:
            handler(**self._kwargs)
        except Exception:
            print_exception("Exception raised in event handler; ignored.")

    def fire(self, **kwargs):
        if self._hasfired:
            return
        self._kwargs = kwargs
        while self._unfired:
            handler = self._unfired.pop()
            self._call(handler)
        self._hasfired = True
        return ()  # Entirely for API compatibility


class EventManager:
    """
    Container for all events in a system.

    Meant to be a singleton, but doesn't enforce that itself.

    Each event is just an attribute. They're created dynamically on first use.
    """

    def doc(self, name, docstring):
        """
        Applies a docstring to an event.

        Parameters
        ----------
        name : str
            The name of the event, eg "on_precommand"
        docstring : str
            The docstring to apply to the event
        """
        type(getattr(self, name)).__doc__ = docstring

    @staticmethod
    def _mkevent(name, species=Event, doc=None):
        # NOTE: Also used in `xonsh_events` test fixture
        # (A little bit of magic to enable docstrings to work right)
        return type(
            name,
            (species,),
            {
                "__doc__": doc,
                "__module__": "xonsh.events",
                "__qualname__": "events." + name,
            },
        )()

    def transmogrify(self, name, species):
        """
        Converts an event from one species to another, preserving handlers and docstring.

        Please note: Some species maintain specialized state. This is lost on transmogrification.

        Parameters
        ----------
        name : str
            The name of the event, eg "on_precommand"
        species : subclass of AbstractEvent
            The type to turn the event in to.
        """
        if isinstance(species, str):
            species = globals()[species]

        if not issubclass(species, AbstractEvent):
            raise ValueError("Invalid event class; must be a subclass of AbstractEvent")

        oldevent = getattr(self, name)
        newevent = self._mkevent(name, species, type(oldevent).__doc__)
        setattr(self, name, newevent)

        for handler in oldevent:
            newevent.add(handler)

    def __getattr__(self, name):
        """Get an event, if it doesn't already exist."""
        if name.startswith("_"):
            raise AttributeError
        # This is only called if the attribute doesn't exist, so create the Event...
        e = self._mkevent(name)
        # ... and save it.
        setattr(self, name, e)
        # Now it exists, and we won't be called again.
        return e


# Not lazy because:
# 1. Initialization of EventManager can't be much cheaper
# 2. It's expected to be used at load time, negating any benefits of using lazy object
events = EventManager()

#
# foreign_shells
#
# -*- coding: utf-8 -*-
"""Tools to help interface with foreign shells, such as Bash."""
# amalgamated os
# amalgamated re
# amalgamated json
shlex = _LazyModule.load('shlex', 'shlex')
# amalgamated sys
tempfile = _LazyModule.load('tempfile', 'tempfile')
# amalgamated builtins
# amalgamated subprocess
# amalgamated warnings
# amalgamated functools
# amalgamated collections.abc
# amalgamated xonsh.lazyasd
# amalgamated xonsh.tools
# amalgamated xonsh.platform
COMMAND = """{seterrprevcmd}
{prevcmd}
echo __XONSH_ENV_BEG__
{envcmd}
echo __XONSH_ENV_END__
echo __XONSH_ALIAS_BEG__
{aliascmd}
echo __XONSH_ALIAS_END__
echo __XONSH_FUNCS_BEG__
{funcscmd}
echo __XONSH_FUNCS_END__
{postcmd}
{seterrpostcmd}"""

DEFAULT_BASH_FUNCSCMD = r"""# get function names from declare
declstr=$(declare -F)
read -r -a decls <<< $declstr
funcnames=""
for((n=0;n<${#decls[@]};n++)); do
  if (( $(($n % 3 )) == 2 )); then
    # get every 3rd entry
    funcnames="$funcnames ${decls[$n]}"
  fi
done

# get functions locations: funcname lineno filename
shopt -s extdebug
namelocfilestr=$(declare -F $funcnames)
shopt -u extdebug

# print just names and files as JSON object
read -r -a namelocfile <<< $namelocfilestr
sep=" "
namefile="{"
while IFS='' read -r line || [[ -n "$line" ]]; do
  name=${line%%"$sep"*}
  locfile=${line#*"$sep"}
  loc=${locfile%%"$sep"*}
  file=${locfile#*"$sep"}
  namefile="${namefile}\"${name}\":\"${file//\\/\\\\}\","
done <<< "$namelocfilestr"
if [[ "{" == "${namefile}" ]]; then
  namefile="${namefile}}"
else
  namefile="${namefile%?}}"
fi
echo $namefile"""

DEFAULT_ZSH_FUNCSCMD = """# get function names
autoload -U is-at-least  # We'll need to version check zsh
namefile="{"
for name in ${(ok)functions}; do
  # force zsh to load the func in order to get the filename,
  # but use +X so that it isn't executed.
  autoload +X $name || continue
  loc=$(whence -v $name)
  loc=${(z)loc}
  if is-at-least 5.2; then
    file=${loc[-1]}
  else
    file=${loc[7,-1]}
  fi
  namefile="${namefile}\\"${name}\\":\\"${(Q)file:A}\\","
done
if [[ "{" == "${namefile}" ]]; then
  namefile="${namefile}}"
else
  namefile="${namefile%?}}"
fi
echo ${namefile}"""


# mapping of shell name aliases to keys in other lookup dictionaries.
@lazyobject
def CANON_SHELL_NAMES():
    return {
        "bash": "bash",
        "/bin/bash": "bash",
        "zsh": "zsh",
        "/bin/zsh": "zsh",
        "/usr/bin/zsh": "zsh",
        "cmd": "cmd",
        "cmd.exe": "cmd",
    }


@lazyobject
def DEFAULT_ENVCMDS():
    return {"bash": "env", "zsh": "env", "cmd": "set"}


@lazyobject
def DEFAULT_ALIASCMDS():
    return {"bash": "alias", "zsh": "alias -L", "cmd": ""}


@lazyobject
def DEFAULT_FUNCSCMDS():
    return {"bash": DEFAULT_BASH_FUNCSCMD, "zsh": DEFAULT_ZSH_FUNCSCMD, "cmd": ""}


@lazyobject
def DEFAULT_SOURCERS():
    return {"bash": "source", "zsh": "source", "cmd": "call"}


@lazyobject
def DEFAULT_TMPFILE_EXT():
    return {"bash": ".sh", "zsh": ".zsh", "cmd": ".bat"}


@lazyobject
def DEFAULT_RUNCMD():
    return {"bash": "-c", "zsh": "-c", "cmd": "/C"}


@lazyobject
def DEFAULT_SETERRPREVCMD():
    return {"bash": "set -e", "zsh": "set -e", "cmd": "@echo off"}


@lazyobject
def DEFAULT_SETERRPOSTCMD():
    return {"bash": "", "zsh": "", "cmd": "if errorlevel 1 exit 1"}


@functools.lru_cache()
def foreign_shell_data(
    shell,
    interactive=True,
    login=False,
    envcmd=None,
    aliascmd=None,
    extra_args=(),
    currenv=None,
    safe=True,
    prevcmd="",
    postcmd="",
    funcscmd=None,
    sourcer=None,
    use_tmpfile=False,
    tmpfile_ext=None,
    runcmd=None,
    seterrprevcmd=None,
    seterrpostcmd=None,
    show=False,
    dryrun=False,
):
    """Extracts data from a foreign (non-xonsh) shells. Currently this gets
    the environment, aliases, and functions but may be extended in the future.

    Parameters
    ----------
    shell : str
        The name of the shell, such as 'bash' or '/bin/sh'.
    interactive : bool, optional
        Whether the shell should be run in interactive mode.
    login : bool, optional
        Whether the shell should be a login shell.
    envcmd : str or None, optional
        The command to generate environment output with.
    aliascmd : str or None, optional
        The command to generate alias output with.
    extra_args : tuple of str, optional
        Additional command line options to pass into the shell.
    currenv : tuple of items or None, optional
        Manual override for the current environment.
    safe : bool, optional
        Flag for whether or not to safely handle exceptions and other errors.
    prevcmd : str, optional
        A command to run in the shell before anything else, useful for
        sourcing and other commands that may require environment recovery.
    postcmd : str, optional
        A command to run after everything else, useful for cleaning up any
        damage that the prevcmd may have caused.
    funcscmd : str or None, optional
        This is a command or script that can be used to determine the names
        and locations of any functions that are native to the foreign shell.
        This command should print *only* a JSON object that maps
        function names to the filenames where the functions are defined.
        If this is None, then a default script will attempted to be looked
        up based on the shell name. Callable wrappers for these functions
        will be returned in the aliases dictionary.
    sourcer : str or None, optional
        How to source a foreign shell file for purposes of calling functions
        in that shell. If this is None, a default value will attempt to be
        looked up based on the shell name.
    use_tmpfile : bool, optional
        This specifies if the commands are written to a tmp file or just
        parsed directly to the shell
    tmpfile_ext : str or None, optional
        If tmpfile is True this sets specifies the extension used.
    runcmd : str or None, optional
        Command line switches to use when running the script, such as
        -c for Bash and /C for cmd.exe.
    seterrprevcmd : str or None, optional
        Command that enables exit-on-error for the shell that is run at the
        start of the script. For example, this is "set -e" in Bash. To disable
        exit-on-error behavior, simply pass in an empty string.
    seterrpostcmd : str or None, optional
        Command that enables exit-on-error for the shell that is run at the end
        of the script. For example, this is "if errorlevel 1 exit 1" in
        cmd.exe. To disable exit-on-error behavior, simply pass in an
        empty string.
    show : bool, optional
        Whether or not to display the script that will be run.
    dryrun : bool, optional
        Whether or not to actually run and process the command.


    Returns
    -------
    env : dict
        Dictionary of shell's environment. (None if the subproc command fails)
    aliases : dict
        Dictionary of shell's aliases, this includes foreign function
        wrappers.(None if the subproc command fails)
    """
    cmd = [shell]
    cmd.extend(extra_args)  # needs to come here for GNU long options
    if interactive:
        cmd.append("-i")
    if login:
        cmd.append("-l")
    shkey = CANON_SHELL_NAMES[shell]
    envcmd = DEFAULT_ENVCMDS.get(shkey, "env") if envcmd is None else envcmd
    aliascmd = DEFAULT_ALIASCMDS.get(shkey, "alias") if aliascmd is None else aliascmd
    funcscmd = DEFAULT_FUNCSCMDS.get(shkey, "echo {}") if funcscmd is None else funcscmd
    tmpfile_ext = (
        DEFAULT_TMPFILE_EXT.get(shkey, "sh") if tmpfile_ext is None else tmpfile_ext
    )
    runcmd = DEFAULT_RUNCMD.get(shkey, "-c") if runcmd is None else runcmd
    seterrprevcmd = (
        DEFAULT_SETERRPREVCMD.get(shkey, "") if seterrprevcmd is None else seterrprevcmd
    )
    seterrpostcmd = (
        DEFAULT_SETERRPOSTCMD.get(shkey, "") if seterrpostcmd is None else seterrpostcmd
    )
    command = COMMAND.format(
        envcmd=envcmd,
        aliascmd=aliascmd,
        prevcmd=prevcmd,
        postcmd=postcmd,
        funcscmd=funcscmd,
        seterrprevcmd=seterrprevcmd,
        seterrpostcmd=seterrpostcmd,
    ).strip()
    if show:
        print(command)
    if dryrun:
        return None, None
    cmd.append(runcmd)
    if not use_tmpfile:
        cmd.append(command)
    else:
        tmpfile = tempfile.NamedTemporaryFile(suffix=tmpfile_ext, delete=False)
        tmpfile.write(command.encode("utf8"))
        tmpfile.close()
        cmd.append(tmpfile.name)
    if currenv is None and hasattr(builtins.__xonsh__, "env"):
        currenv = builtins.__xonsh__.env.detype()
    elif currenv is not None:
        currenv = dict(currenv)
    try:
        s = subprocess.check_output(
            cmd,
            stderr=subprocess.PIPE,
            env=currenv,
            # start new session to avoid hangs
            # (doesn't work on Cygwin though)
            start_new_session=((not ON_CYGWIN) and (not ON_MSYS)),
            universal_newlines=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        if not safe:
            raise
        return None, None
    finally:
        if use_tmpfile:
            os.remove(tmpfile.name)
    env = parse_env(s)
    aliases = parse_aliases(s, shell=shell, sourcer=sourcer, extra_args=extra_args)
    funcs = parse_funcs(s, shell=shell, sourcer=sourcer, extra_args=extra_args)
    aliases.update(funcs)
    return env, aliases


@lazyobject
def ENV_RE():
    return re.compile("__XONSH_ENV_BEG__\n(.*)" "__XONSH_ENV_END__", flags=re.DOTALL)


@lazyobject
def ENV_SPLIT_RE():
    return re.compile("^([^=]+)=([^=]*|[^\n]*)$", flags=re.DOTALL | re.MULTILINE)


def parse_env(s):
    """Parses the environment portion of string into a dict."""
    m = ENV_RE.search(s)
    if m is None:
        return {}
    g1 = m.group(1)
    g1 = g1[:-1] if g1.endswith("\n") else g1
    env = dict(ENV_SPLIT_RE.findall(g1))
    return env


@lazyobject
def ALIAS_RE():
    return re.compile(
        "__XONSH_ALIAS_BEG__\n(.*)" "__XONSH_ALIAS_END__", flags=re.DOTALL
    )


@lazyobject
def FS_EXEC_ALIAS_RE():
    return re.compile(r";|`|\$\(")


def parse_aliases(s, shell, sourcer=None, extra_args=()):
    """Parses the aliases portion of string into a dict."""
    m = ALIAS_RE.search(s)
    if m is None:
        return {}
    g1 = m.group(1)
    items = [
        line.split("=", 1)
        for line in g1.splitlines()
        if line.startswith("alias ") and "=" in line
    ]
    aliases = {}
    for key, value in items:
        try:
            key = key[6:]  # lstrip 'alias '
            # undo bash's weird quoting of single quotes (sh_single_quote)
            value = value.replace("'\\''", "'")
            # strip one single quote at the start and end of value
            if value[0] == "'" and value[-1] == "'":
                value = value[1:-1]
            # now compute actual alias
            if FS_EXEC_ALIAS_RE.search(value) is None:
                # simple list of args alias
                value = shlex.split(value)
            else:
                # alias is more complex, use ExecAlias, but via shell
                filename = "<foreign-shell-exec-alias:" + key + ">"
                value = ForeignShellExecAlias(
                    src=value,
                    shell=shell,
                    filename=filename,
                    sourcer=sourcer,
                    extra_args=extra_args,
                )
        except ValueError as exc:
            warnings.warn(
                'could not parse alias "{0}": {1!r}'.format(key, exc), RuntimeWarning
            )
            continue
        aliases[key] = value
    return aliases


@lazyobject
def FUNCS_RE():
    return re.compile(
        "__XONSH_FUNCS_BEG__\n(.+)\n" "__XONSH_FUNCS_END__", flags=re.DOTALL
    )


def parse_funcs(s, shell, sourcer=None, extra_args=()):
    """Parses the funcs portion of a string into a dict of callable foreign
    function wrappers.
    """
    m = FUNCS_RE.search(s)
    if m is None:
        return {}
    g1 = m.group(1)
    if ON_WINDOWS:
        g1 = g1.replace(os.sep, os.altsep)
    try:
        namefiles = json.loads(g1.strip())
    except json.decoder.JSONDecodeError as exc:
        msg = (
            "{0!r}\n\ncould not parse {1} functions:\n"
            "  s  = {2!r}\n"
            "  g1 = {3!r}\n\n"
            "Note: you may be seeing this error if you use zsh with "
            "prezto. Prezto overwrites GNU coreutils functions (like echo) "
            "with its own zsh functions. Please try disabling prezto."
        )
        warnings.warn(msg.format(exc, shell, s, g1), RuntimeWarning)
        return {}
    sourcer = DEFAULT_SOURCERS.get(shell, "source") if sourcer is None else sourcer
    funcs = {}
    for funcname, filename in namefiles.items():
        if funcname.startswith("_") or not filename:
            continue  # skip private functions and invalid files
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
        wrapper = ForeignShellFunctionAlias(
            funcname=funcname,
            shell=shell,
            sourcer=sourcer,
            filename=filename,
            extra_args=extra_args,
        )
        funcs[funcname] = wrapper
    return funcs


class ForeignShellBaseAlias(object):
    """This class is responsible for calling foreign shell functions as if
    they were aliases. This does not currently support taking stdin.
    """

    INPUT = "echo ForeignShellBaseAlias {shell} {filename} {args}\n"

    def __init__(self, shell, filename, sourcer=None, extra_args=()):
        """
        Parameters
        ----------
        shell : str
            Name or path to shell
        filename : str
            Where the function is defined, path to source.
        sourcer : str or None, optional
            Command to source foreign files with.
        extra_args : tuple of str, optional
            Additional command line options to pass into the shell.
        """
        sourcer = DEFAULT_SOURCERS.get(shell, "source") if sourcer is None else sourcer
        self.shell = shell
        self.filename = filename
        self.sourcer = sourcer
        self.extra_args = extra_args

    def _input_kwargs(self):
        return {
            "shell": self.shell,
            "filename": self.filename,
            "sourcer": self.sourcer,
            "extra_args": self.extra_args,
        }

    def __eq__(self, other):
        if not hasattr(other, "_input_kwargs") or not callable(other._input_kwargs):
            return NotImplemented
        return self._input_kwargs() == other._input_kwargs()

    def __call__(
        self, args, stdin=None, stdout=None, stderr=None, spec=None, stack=None
    ):
        args, streaming = self._is_streaming(args)
        input = self.INPUT.format(args=" ".join(args), **self._input_kwargs())
        cmd = [self.shell] + list(self.extra_args) + ["-c", input]
        env = builtins.__xonsh__.env
        denv = env.detype()
        if streaming:
            subprocess.check_call(cmd, env=denv)
            out = None
        else:
            out = subprocess.check_output(cmd, env=denv, stderr=subprocess.STDOUT)
            out = out.decode(
                encoding=env.get("XONSH_ENCODING"),
                errors=env.get("XONSH_ENCODING_ERRORS"),
            )
            out = out.replace("\r\n", "\n")
        return out

    def __repr__(self):
        return (
            self.__class__.__name__
            + "("
            + ", ".join(
                [
                    "{k}={v!r}".format(k=k, v=v)
                    for k, v in sorted(self._input_kwargs().items())
                ]
            )
            + ")"
        )

    @staticmethod
    def _is_streaming(args):
        """Test and modify args if --xonsh-stream is present."""
        if "--xonsh-stream" not in args:
            return args, False
        args = list(args)
        args.remove("--xonsh-stream")
        return args, True


class ForeignShellFunctionAlias(ForeignShellBaseAlias):
    """This class is responsible for calling foreign shell functions as if
    they were aliases. This does not currently support taking stdin.
    """

    INPUT = '{sourcer} "{filename}"\n' "{funcname} {args}\n"

    def __init__(self, funcname, shell, filename, sourcer=None, extra_args=()):
        """
        Parameters
        ----------
        funcname : str
            function name
        shell : str
            Name or path to shell
        filename : str
            Where the function is defined, path to source.
        sourcer : str or None, optional
            Command to source foreign files with.
        extra_args : tuple of str, optional
            Additional command line options to pass into the shell.
        """
        super().__init__(
            shell=shell, filename=filename, sourcer=sourcer, extra_args=extra_args
        )
        self.funcname = funcname

    def _input_kwargs(self):
        inp = super()._input_kwargs()
        inp["funcname"] = self.funcname
        return inp


class ForeignShellExecAlias(ForeignShellBaseAlias):
    """Provides a callable alias for source code in a foreign shell."""

    INPUT = "{src} {args}\n"

    def __init__(
        self,
        src,
        shell,
        filename="<foreign-shell-exec-alias>",
        sourcer=None,
        extra_args=(),
    ):
        """
        Parameters
        ----------
        src : str
            Source code in the shell language
        shell : str
            Name or path to shell
        filename : str
            Where the function is defined, path to source.
        sourcer : str or None, optional
            Command to source foreign files with.
        extra_args : tuple of str, optional
            Additional command line options to pass into the shell.
        """
        super().__init__(
            shell=shell, filename=filename, sourcer=sourcer, extra_args=extra_args
        )
        self.src = src.strip()

    def _input_kwargs(self):
        inp = super()._input_kwargs()
        inp["src"] = self.src
        return inp


@lazyobject
def VALID_SHELL_PARAMS():
    return frozenset(
        [
            "shell",
            "interactive",
            "login",
            "envcmd",
            "aliascmd",
            "extra_args",
            "currenv",
            "safe",
            "prevcmd",
            "postcmd",
            "funcscmd",
            "sourcer",
        ]
    )


def ensure_shell(shell):
    """Ensures that a mapping follows the shell specification."""
    if not isinstance(shell, cabc.MutableMapping):
        shell = dict(shell)
    shell_keys = set(shell.keys())
    if not (shell_keys <= VALID_SHELL_PARAMS):
        msg = "unknown shell keys: {0}"
        raise KeyError(msg.format(shell_keys - VALID_SHELL_PARAMS))
    shell["shell"] = ensure_string(shell["shell"]).lower()
    if "interactive" in shell_keys:
        shell["interactive"] = to_bool(shell["interactive"])
    if "login" in shell_keys:
        shell["login"] = to_bool(shell["login"])
    if "envcmd" in shell_keys:
        shell["envcmd"] = (
            None if shell["envcmd"] is None else ensure_string(shell["envcmd"])
        )
    if "aliascmd" in shell_keys:
        shell["aliascmd"] = (
            None if shell["aliascmd"] is None else ensure_string(shell["aliascmd"])
        )
    if "extra_args" in shell_keys and not isinstance(shell["extra_args"], tuple):
        shell["extra_args"] = tuple(map(ensure_string, shell["extra_args"]))
    if "currenv" in shell_keys and not isinstance(shell["currenv"], tuple):
        ce = shell["currenv"]
        if isinstance(ce, cabc.Mapping):
            ce = tuple([(ensure_string(k), v) for k, v in ce.items()])
        elif isinstance(ce, cabc.Sequence):
            ce = tuple([(ensure_string(k), v) for k, v in ce])
        else:
            raise RuntimeError("unrecognized type for currenv")
        shell["currenv"] = ce
    if "safe" in shell_keys:
        shell["safe"] = to_bool(shell["safe"])
    if "prevcmd" in shell_keys:
        shell["prevcmd"] = ensure_string(shell["prevcmd"])
    if "postcmd" in shell_keys:
        shell["postcmd"] = ensure_string(shell["postcmd"])
    if "funcscmd" in shell_keys:
        shell["funcscmd"] = (
            None if shell["funcscmd"] is None else ensure_string(shell["funcscmd"])
        )
    if "sourcer" in shell_keys:
        shell["sourcer"] = (
            None if shell["sourcer"] is None else ensure_string(shell["sourcer"])
        )
    if "seterrprevcmd" in shell_keys:
        shell["seterrprevcmd"] = (
            None
            if shell["seterrprevcmd"] is None
            else ensure_string(shell["seterrprevcmd"])
        )
    if "seterrpostcmd" in shell_keys:
        shell["seterrpostcmd"] = (
            None
            if shell["seterrpostcmd"] is None
            else ensure_string(shell["seterrpostcmd"])
        )
    return shell


def load_foreign_envs(shells):
    """Loads environments from foreign shells.

    Parameters
    ----------
    shells : sequence of dicts
        An iterable of dicts that can be passed into foreign_shell_data() as
        keyword arguments.

    Returns
    -------
    env : dict
        A dictionary of the merged environments.
    """
    env = {}
    for shell in shells:
        shell = ensure_shell(shell)
        shenv, _ = foreign_shell_data(**shell)
        if shenv:
            env.update(shenv)
    return env


def load_foreign_aliases(shells):
    """Loads aliases from foreign shells.

    Parameters
    ----------
    shells : sequence of dicts
        An iterable of dicts that can be passed into foreign_shell_data() as
        keyword arguments.

    Returns
    -------
    aliases : dict
        A dictionary of the merged aliases.
    """
    aliases = {}
    xonsh_aliases = builtins.aliases
    for shell in shells:
        shell = ensure_shell(shell)
        _, shaliases = foreign_shell_data(**shell)
        if not builtins.__xonsh__.env.get("FOREIGN_ALIASES_OVERRIDE"):
            shaliases = {} if shaliases is None else shaliases
            for alias in set(shaliases) & set(xonsh_aliases):
                del shaliases[alias]
                if builtins.__xonsh__.env.get("XONSH_DEBUG") > 1:
                    print(
                        "aliases: ignoring alias {!r} of shell {!r} "
                        "which tries to override xonsh alias."
                        "".format(alias, shell["shell"]),
                        file=sys.stderr,
                    )
        aliases.update(shaliases)
    return aliases

#
# jobs
#
# -*- coding: utf-8 -*-
"""Job control for the xonsh shell."""
# amalgamated os
# amalgamated sys
# amalgamated time
# amalgamated ctypes
# amalgamated signal
# amalgamated builtins
# amalgamated subprocess
# amalgamated collections
# amalgamated xonsh.lazyasd
# amalgamated xonsh.platform
# amalgamated xonsh.tools
tasks = LazyObject(collections.deque, globals(), "tasks")
# Track time stamp of last exit command, so that two consecutive attempts to
# exit can kill all jobs and exit.
_last_exit_time = None


if ON_DARWIN:

    def _send_signal(job, signal):
        # On OS X, os.killpg() may cause PermissionError when there are
        # any zombie processes in the process group.
        # See github issue #1012 for details
        for pid in job["pids"]:
            if pid is None:  # the pid of an aliased proc is None
                continue
            try:
                os.kill(pid, signal)
            except ProcessLookupError:
                pass


elif ON_WINDOWS:
    pass
elif ON_CYGWIN or ON_MSYS:
    # Similar to what happened on OSX, more issues on Cygwin
    # (see Github issue #514).
    def _send_signal(job, signal):
        try:
            os.killpg(job["pgrp"], signal)
        except Exception:
            for pid in job["pids"]:
                try:
                    os.kill(pid, signal)
                except Exception:
                    pass


else:

    def _send_signal(job, signal):
        pgrp = job["pgrp"]
        if pgrp is None:
            for pid in job["pids"]:
                try:
                    os.kill(pid, signal)
                except Exception:
                    pass
        else:
            os.killpg(job["pgrp"], signal)


if ON_WINDOWS:

    def _continue(job):
        job["status"] = "running"

    def _kill(job):
        subprocess.check_output(["taskkill", "/F", "/T", "/PID", str(job["obj"].pid)])

    def ignore_sigtstp():
        pass

    def give_terminal_to(pgid):
        pass

    def wait_for_active_job(last_task=None, backgrounded=False):
        """
        Wait for the active job to finish, to be killed by SIGINT, or to be
        suspended by ctrl-z.
        """
        _clear_dead_jobs()
        active_task = get_next_task()
        # Return when there are no foreground active task
        if active_task is None:
            return last_task
        obj = active_task["obj"]
        _continue(active_task)
        while obj.returncode is None:
            try:
                obj.wait(0.01)
            except subprocess.TimeoutExpired:
                pass
            except KeyboardInterrupt:
                _kill(active_task)
        return wait_for_active_job(last_task=active_task)


else:

    def _continue(job):
        _send_signal(job, signal.SIGCONT)

    def _kill(job):
        _send_signal(job, signal.SIGKILL)

    def ignore_sigtstp():
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)

    _shell_pgrp = os.getpgrp()

    _block_when_giving = LazyObject(
        lambda: (signal.SIGTTOU, signal.SIGTTIN, signal.SIGTSTP, signal.SIGCHLD),
        globals(),
        "_block_when_giving",
    )

    if ON_CYGWIN or ON_MSYS:
        # on cygwin, signal.pthread_sigmask does not exist in Python, even
        # though pthread_sigmask is defined in the kernel.  thus, we use
        # ctypes to mimic the calls in the "normal" version below.
        LIBC.pthread_sigmask.restype = ctypes.c_int
        LIBC.pthread_sigmask.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
        ]

        def _pthread_sigmask(how, signals):
            mask = 0
            for sig in signals:
                mask |= 1 << sig
            oldmask = ctypes.c_ulong()
            mask = ctypes.c_ulong(mask)
            result = LIBC.pthread_sigmask(
                how, ctypes.byref(mask), ctypes.byref(oldmask)
            )
            if result:
                raise OSError(result, "Sigmask error.")

            return {
                sig
                for sig in getattr(signal, "Signals", range(0, 65))
                if (oldmask.value >> sig) & 1
            }

    else:
        _pthread_sigmask = signal.pthread_sigmask

    # give_terminal_to is a simplified version of:
    #    give_terminal_to from bash 4.3 source, jobs.c, line 4030
    # this will give the terminal to the process group pgid
    def give_terminal_to(pgid):
        if pgid is None:
            return False
        oldmask = _pthread_sigmask(signal.SIG_BLOCK, _block_when_giving)
        try:
            os.tcsetpgrp(FD_STDERR, pgid)
            return True
        except ProcessLookupError:
            # when the process finished before giving terminal to it,
            # see issue #2288
            return False
        except OSError as e:
            if e.errno == 22:  # [Errno 22] Invalid argument
                # there are cases that all the processes of pgid have
                # finished, then we don't need to do anything here, see
                # issue #2220
                return False
            elif e.errno == 25:  # [Errno 25] Inappropriate ioctl for device
                # There are also cases where we are not connected to a
                # real TTY, even though we may be run in interactive
                # mode. See issue #2267 for an example with emacs
                return False
            else:
                raise
        finally:
            _pthread_sigmask(signal.SIG_SETMASK, oldmask)

    def wait_for_active_job(last_task=None, backgrounded=False):
        """
        Wait for the active job to finish, to be killed by SIGINT, or to be
        suspended by ctrl-z.
        """
        _clear_dead_jobs()
        active_task = get_next_task()
        # Return when there are no foreground active task
        if active_task is None:
            return last_task
        obj = active_task["obj"]
        backgrounded = False
        try:
            _, wcode = os.waitpid(obj.pid, os.WUNTRACED)
        except ChildProcessError:  # No child processes
            return wait_for_active_job(last_task=active_task, backgrounded=backgrounded)
        if os.WIFSTOPPED(wcode):
            print("^Z")
            active_task["status"] = "stopped"
            backgrounded = True
        elif os.WIFSIGNALED(wcode):
            print()  # get a newline because ^C will have been printed
            obj.signal = (os.WTERMSIG(wcode), os.WCOREDUMP(wcode))
            obj.returncode = None
        else:
            obj.returncode = os.WEXITSTATUS(wcode)
            obj.signal = None
        return wait_for_active_job(last_task=active_task, backgrounded=backgrounded)


def get_next_task():
    """ Get the next active task and put it on top of the queue"""
    selected_task = None
    for tid in tasks:
        task = get_task(tid)
        if not task["bg"] and task["status"] == "running":
            selected_task = tid
            break
    if selected_task is None:
        return
    tasks.remove(selected_task)
    tasks.appendleft(selected_task)
    return get_task(selected_task)


def get_task(tid):
    return builtins.__xonsh__.all_jobs[tid]


def _clear_dead_jobs():
    to_remove = set()
    for tid in tasks:
        obj = get_task(tid)["obj"]
        if obj is None or obj.poll() is not None:
            to_remove.add(tid)
    for job in to_remove:
        tasks.remove(job)
        del builtins.__xonsh__.all_jobs[job]


def print_one_job(num, outfile=sys.stdout):
    """Print a line describing job number ``num``."""
    try:
        job = builtins.__xonsh__.all_jobs[num]
    except KeyError:
        return
    pos = "+" if tasks[0] == num else "-" if tasks[1] == num else " "
    status = job["status"]
    cmd = [" ".join(i) if isinstance(i, list) else i for i in job["cmds"]]
    cmd = " ".join(cmd)
    pid = job["pids"][-1]
    bg = " &" if job["bg"] else ""
    print("[{}]{} {}: {}{} ({})".format(num, pos, status, cmd, bg, pid), file=outfile)


def get_next_job_number():
    """Get the lowest available unique job number (for the next job created).
    """
    _clear_dead_jobs()
    i = 1
    while i in builtins.__xonsh__.all_jobs:
        i += 1
    return i


def add_job(info):
    """Add a new job to the jobs dictionary."""
    num = get_next_job_number()
    info["started"] = time.time()
    info["status"] = "running"
    tasks.appendleft(num)
    builtins.__xonsh__.all_jobs[num] = info
    if info["bg"] and builtins.__xonsh__.env.get("XONSH_INTERACTIVE"):
        print_one_job(num)


def clean_jobs():
    """Clean up jobs for exiting shell

    In non-interactive mode, kill all jobs.

    In interactive mode, check for suspended or background jobs, print a
    warning if any exist, and return False. Otherwise, return True.
    """
    jobs_clean = True
    if builtins.__xonsh__.env["XONSH_INTERACTIVE"]:
        _clear_dead_jobs()

        if builtins.__xonsh__.all_jobs:
            global _last_exit_time
            hist = builtins.__xonsh__.history
            if hist is not None and len(hist.tss) > 0:
                last_cmd_start = hist.tss[-1][0]
            else:
                last_cmd_start = None

            if _last_exit_time and last_cmd_start and _last_exit_time > last_cmd_start:
                # Exit occurred after last command started, so it was called as
                # part of the last command and is now being called again
                # immediately. Kill jobs and exit without reminder about
                # unfinished jobs in this case.
                kill_all_jobs()
            else:
                if len(builtins.__xonsh__.all_jobs) > 1:
                    msg = "there are unfinished jobs"
                else:
                    msg = "there is an unfinished job"

                if builtins.__xonsh__.env["SHELL_TYPE"] != "prompt_toolkit":
                    # The Ctrl+D binding for prompt_toolkit already inserts a
                    # newline
                    print()
                print("xonsh: {}".format(msg), file=sys.stderr)
                print("-" * 5, file=sys.stderr)
                jobs([], stdout=sys.stderr)
                print("-" * 5, file=sys.stderr)
                print(
                    'Type "exit" or press "ctrl-d" again to force quit.',
                    file=sys.stderr,
                )
                jobs_clean = False
                _last_exit_time = time.time()
    else:
        kill_all_jobs()

    return jobs_clean


def kill_all_jobs():
    """
    Send SIGKILL to all child processes (called when exiting xonsh).
    """
    _clear_dead_jobs()
    for job in builtins.__xonsh__.all_jobs.values():
        _kill(job)


def jobs(args, stdin=None, stdout=sys.stdout, stderr=None):
    """
    xonsh command: jobs

    Display a list of all current jobs.
    """
    _clear_dead_jobs()
    for j in tasks:
        print_one_job(j, outfile=stdout)
    return None, None


def resume_job(args, wording):
    """
    used by fg and bg to resume a job either in the foreground or in the background.
    """
    _clear_dead_jobs()
    if len(tasks) == 0:
        return "", "There are currently no suspended jobs"

    if len(args) == 0:
        tid = tasks[0]  # take the last manipulated task by default
    elif len(args) == 1:
        try:
            if args[0] == "+":  # take the last manipulated task
                tid = tasks[0]
            elif args[0] == "-":  # take the second to last manipulated task
                tid = tasks[1]
            else:
                tid = int(args[0])
        except (ValueError, IndexError):
            return "", "Invalid job: {}\n".format(args[0])

        if tid not in builtins.__xonsh__.all_jobs:
            return "", "Invalid job: {}\n".format(args[0])
    else:
        return "", "{} expects 0 or 1 arguments, not {}\n".format(wording, len(args))

    # Put this one on top of the queue
    tasks.remove(tid)
    tasks.appendleft(tid)

    job = get_task(tid)
    job["bg"] = False
    job["status"] = "running"
    if builtins.__xonsh__.env.get("XONSH_INTERACTIVE"):
        print_one_job(tid)
    pipeline = job["pipeline"]
    pipeline.resume(job)


@unthreadable
def fg(args, stdin=None):
    """
    xonsh command: fg

    Bring the currently active job to the foreground, or, if a single number is
    given as an argument, bring that job to the foreground. Additionally,
    specify "+" for the most recent job and "-" for the second most recent job.
    """
    return resume_job(args, wording="fg")


def bg(args, stdin=None):
    """xonsh command: bg

    Resume execution of the currently active job in the background, or, if a
    single number is given as an argument, resume that job in the background.
    """
    res = resume_job(args, wording="bg")
    if res is None:
        curtask = get_task(tasks[0])
        curtask["bg"] = True
        _continue(curtask)
    else:
        return res

#
# jsonutils
#
"""Custom tools for managing JSON serialization / deserialization of xonsh
objects.
"""
# amalgamated functools
# amalgamated xonsh.tools
@functools.singledispatch
def serialize_xonsh_json(val):
    """JSON serializer for xonsh custom data structures. This is only
    called when another normal JSON types are not found.
    """
    return str(val)


@serialize_xonsh_json.register(EnvPath)
def _serialize_xonsh_json_env_path(val):
    return val.paths

#
# lexer
#
# -*- coding: utf-8 -*-
"""Lexer for xonsh code.

Written using a hybrid of ``tokenize`` and PLY.
"""
# amalgamated io
# amalgamated re
kwmod = _LazyModule.load('keyword', 'keyword', 'kwmod')
try:
    from ply.lex import LexToken
except ImportError:
    from xonsh.ply.ply.lex import LexToken

# amalgamated xonsh.lazyasd
# amalgamated xonsh.platform
# amalgamated xonsh.tokenize
@lazyobject
def token_map():
    """Mapping from ``tokenize`` tokens (or token types) to PLY token types. If
    a simple one-to-one mapping from ``tokenize`` to PLY exists, the lexer will
    look it up here and generate a single PLY token of the given type.
    Otherwise, it will fall back to handling that token using one of the
    handlers in``special_handlers``.
    """
    tm = {}
    # operators
    _op_map = {
        # punctuation
        ",": "COMMA",
        ".": "PERIOD",
        ";": "SEMI",
        ":": "COLON",
        "...": "ELLIPSIS",
        # basic operators
        "+": "PLUS",
        "-": "MINUS",
        "*": "TIMES",
        "@": "AT",
        "/": "DIVIDE",
        "//": "DOUBLEDIV",
        "%": "MOD",
        "**": "POW",
        "|": "PIPE",
        "~": "TILDE",
        "^": "XOR",
        "<<": "LSHIFT",
        ">>": "RSHIFT",
        "<": "LT",
        "<=": "LE",
        ">": "GT",
        ">=": "GE",
        "==": "EQ",
        "!=": "NE",
        "->": "RARROW",
        # assignment operators
        "=": "EQUALS",
        "+=": "PLUSEQUAL",
        "-=": "MINUSEQUAL",
        "*=": "TIMESEQUAL",
        "@=": "ATEQUAL",
        "/=": "DIVEQUAL",
        "%=": "MODEQUAL",
        "**=": "POWEQUAL",
        "<<=": "LSHIFTEQUAL",
        ">>=": "RSHIFTEQUAL",
        "&=": "AMPERSANDEQUAL",
        "^=": "XOREQUAL",
        "|=": "PIPEEQUAL",
        "//=": "DOUBLEDIVEQUAL",
        # extra xonsh operators
        "?": "QUESTION",
        "??": "DOUBLE_QUESTION",
        "@$": "ATDOLLAR",
        "&": "AMPERSAND",
    }
    for (op, typ) in _op_map.items():
        tm[(OP, op)] = typ
    tm[IOREDIRECT] = "IOREDIRECT"
    tm[STRING] = "STRING"
    tm[DOLLARNAME] = "DOLLAR_NAME"
    tm[NUMBER] = "NUMBER"
    tm[SEARCHPATH] = "SEARCHPATH"
    tm[NEWLINE] = "NEWLINE"
    tm[INDENT] = "INDENT"
    tm[DEDENT] = "DEDENT"
    if (3, 5, 0) <= PYTHON_VERSION_INFO < (3, 7, 0):
        from xonsh.tokenize import ASYNC, AWAIT

        tm[ASYNC] = "ASYNC"
        tm[AWAIT] = "AWAIT"
    return tm


NEED_WHITESPACE = frozenset(["and", "or"])


@lazyobject
def RE_NEED_WHITESPACE():
    pattern = r"\s?(" + "|".join(NEED_WHITESPACE) + r")(\s|[\\]$)"
    return re.compile(pattern)


def handle_name(state, token):
    """Function for handling name tokens"""
    typ = "NAME"
    state["last"] = token
    needs_whitespace = token.string in NEED_WHITESPACE
    has_whitespace = needs_whitespace and RE_NEED_WHITESPACE.match(
        token.line[max(0, token.start[1] - 1) :]
    )
    if state["pymode"][-1][0]:
        if needs_whitespace and not has_whitespace:
            pass
        elif token.string in kwmod.kwlist:
            typ = token.string.upper()
        yield _new_token(typ, token.string, token.start)
    else:
        if has_whitespace and token.string == "and":
            yield _new_token("AND", token.string, token.start)
        elif has_whitespace and token.string == "or":
            yield _new_token("OR", token.string, token.start)
        else:
            yield _new_token("NAME", token.string, token.start)


def _end_delimiter(state, token):
    py = state["pymode"]
    s = token.string
    l, c = token.start
    if len(py) > 1:
        mode, orig, match, pos = py.pop()
        if s != match:
            e = '"{}" at {} ends "{}" at {} (expected "{}")'
            return e.format(s, (l, c), orig, pos, match)
    else:
        return 'Unmatched "{}" at line {}, column {}'.format(s, l, c)


def handle_rparen(state, token):
    """
    Function for handling ``)``
    """
    e = _end_delimiter(state, token)
    if e is None:
        state["last"] = token
        yield _new_token("RPAREN", ")", token.start)
    else:
        yield _new_token("ERRORTOKEN", e, token.start)


def handle_rbrace(state, token):
    """Function for handling ``}``"""
    e = _end_delimiter(state, token)
    if e is None:
        state["last"] = token
        yield _new_token("RBRACE", "}", token.start)
    else:
        yield _new_token("ERRORTOKEN", e, token.start)


def handle_rbracket(state, token):
    """
    Function for handling ``]``
    """
    e = _end_delimiter(state, token)
    if e is None:
        state["last"] = token
        yield _new_token("RBRACKET", "]", token.start)
    else:
        yield _new_token("ERRORTOKEN", e, token.start)


def handle_error_space(state, token):
    """
    Function for handling special whitespace characters in subprocess mode
    """
    if not state["pymode"][-1][0]:
        state["last"] = token
        yield _new_token("WS", token.string, token.start)
    else:
        yield from []


def handle_error_linecont(state, token):
    """Function for handling special line continuations as whitespace
    characters in subprocess mode.
    """
    if state["pymode"][-1][0]:
        return
    prev = state["last"]
    if prev.end != token.start:
        return  # previous token is separated by whitespace
    state["last"] = token
    yield _new_token("WS", "\\", token.start)


def handle_error_token(state, token):
    """
    Function for handling error tokens
    """
    state["last"] = token
    if token.string == "!":
        typ = "BANG"
    elif not state["pymode"][-1][0]:
        typ = "NAME"
    else:
        typ = "ERRORTOKEN"
    yield _new_token(typ, token.string, token.start)


def handle_ignore(state, token):
    """Function for handling tokens that should be ignored"""
    yield from []


def handle_double_amps(state, token):
    yield _new_token("AND", "and", token.start)


def handle_double_pipe(state, token):
    yield _new_token("OR", "or", token.start)


def handle_redirect(state, token):
    # The parser expects whitespace after a redirection in subproc mode.
    # If whitespace does not exist, we'll issue an empty whitespace
    # token before proceeding.
    state["last"] = token
    typ = token.type
    st = token.string
    key = (typ, st) if (typ, st) in token_map else typ
    yield _new_token(token_map[key], st, token.start)
    if state["pymode"][-1][0]:
        return
    # add a whitespace token after a redirection, if we need to
    next_tok = next(state["stream"])
    if next_tok.start == token.end:
        yield _new_token("WS", "", token.end)
    yield from handle_token(state, next_tok)


def _make_matcher_handler(tok, typ, pymode, ender, handlers):
    matcher = (
        ")"
        if tok.endswith("(")
        else "}"
        if tok.endswith("{")
        else "]"
        if tok.endswith("[")
        else None
    )

    def _inner_handler(state, token):
        state["pymode"].append((pymode, tok, matcher, token.start))
        state["last"] = token
        yield _new_token(typ, tok, token.start)

    handlers[(OP, tok)] = _inner_handler


@lazyobject
def special_handlers():
    """Mapping from ``tokenize`` tokens (or token types) to the proper
    function for generating PLY tokens from them.  In addition to
    yielding PLY tokens, these functions may manipulate the Lexer's state.
    """
    sh = {
        NL: handle_ignore,
        COMMENT: handle_ignore,
        ENCODING: handle_ignore,
        ENDMARKER: handle_ignore,
        NAME: handle_name,
        ERRORTOKEN: handle_error_token,
        LESS: handle_redirect,
        GREATER: handle_redirect,
        RIGHTSHIFT: handle_redirect,
        IOREDIRECT: handle_redirect,
        (OP, "<"): handle_redirect,
        (OP, ">"): handle_redirect,
        (OP, ">>"): handle_redirect,
        (OP, ")"): handle_rparen,
        (OP, "}"): handle_rbrace,
        (OP, "]"): handle_rbracket,
        (OP, "&&"): handle_double_amps,
        (OP, "||"): handle_double_pipe,
        (ERRORTOKEN, " "): handle_error_space,
        (ERRORTOKEN, "\\\n"): handle_error_linecont,
        (ERRORTOKEN, "\\\r\n"): handle_error_linecont,
    }
    _make_matcher_handler("(", "LPAREN", True, ")", sh)
    _make_matcher_handler("[", "LBRACKET", True, "]", sh)
    _make_matcher_handler("{", "LBRACE", True, "}", sh)
    _make_matcher_handler("$(", "DOLLAR_LPAREN", False, ")", sh)
    _make_matcher_handler("$[", "DOLLAR_LBRACKET", False, "]", sh)
    _make_matcher_handler("${", "DOLLAR_LBRACE", True, "}", sh)
    _make_matcher_handler("!(", "BANG_LPAREN", False, ")", sh)
    _make_matcher_handler("![", "BANG_LBRACKET", False, "]", sh)
    _make_matcher_handler("@(", "AT_LPAREN", True, ")", sh)
    _make_matcher_handler("@$(", "ATDOLLAR_LPAREN", False, ")", sh)
    return sh


def handle_token(state, token):
    """
    General-purpose token handler.  Makes use of ``token_map`` or
    ``special_map`` to yield one or more PLY tokens from the given input.

    Parameters
    ----------

    state :
        The current state of the lexer, including information about whether
        we are in Python mode or subprocess mode, which changes the lexer's
        behavior.  Also includes the stream of tokens yet to be considered.
    token :
        The token (from ``tokenize``) currently under consideration
    """
    typ = token.type
    st = token.string
    pymode = state["pymode"][-1][0]
    if not pymode:
        if state["last"] is not None and state["last"].end != token.start:
            cur = token.start
            old = state["last"].end
            if cur[0] == old[0] and cur[1] > old[1]:
                yield _new_token("WS", token.line[old[1] : cur[1]], old)
    if (typ, st) in special_handlers:
        yield from special_handlers[(typ, st)](state, token)
    elif (typ, st) in token_map:
        state["last"] = token
        yield _new_token(token_map[(typ, st)], st, token.start)
    elif typ in special_handlers:
        yield from special_handlers[typ](state, token)
    elif typ in token_map:
        state["last"] = token
        yield _new_token(token_map[typ], st, token.start)
    else:
        m = "Unexpected token: {0}".format(token)
        yield _new_token("ERRORTOKEN", m, token.start)


def get_tokens(s):
    """
    Given a string containing xonsh code, generates a stream of relevant PLY
    tokens using ``handle_token``.
    """
    state = {
        "indents": [0],
        "last": None,
        "pymode": [(True, "", "", (0, 0))],
        "stream": tokenize(io.BytesIO(s.encode("utf-8")).readline),
    }
    while True:
        try:
            token = next(state["stream"])
            yield from handle_token(state, token)
        except StopIteration:
            if len(state["pymode"]) > 1:
                pm, o, m, p = state["pymode"][-1]
                l, c = p
                e = 'Unmatched "{}" at line {}, column {}'
                yield _new_token("ERRORTOKEN", e.format(o, l, c), (0, 0))
            break
        except TokenError as e:
            # this is recoverable in single-line mode (from the shell)
            # (e.g., EOF while scanning string literal)
            yield _new_token("ERRORTOKEN", e.args[0], (0, 0))
            break
        except IndentationError as e:
            # this is never recoverable
            yield _new_token("ERRORTOKEN", e, (0, 0))
            break


# synthesize a new PLY token
def _new_token(type, value, pos):
    o = LexToken()
    o.type = type
    o.value = value
    o.lineno, o.lexpos = pos
    return o


class Lexer(object):
    """Implements a lexer for the xonsh language."""

    _tokens = None

    def __init__(self):
        """
        Attributes
        ----------
        fname : str
            Filename
        last : token
            The last token seen.
        lineno : int
            The last line number seen.

        """
        self.fname = ""
        self.last = None
        self.beforelast = None

    def build(self, **kwargs):
        """Part of the PLY lexer API."""
        pass

    def reset(self):
        pass

    def input(self, s):
        """Calls the lexer on the string s."""
        self.token_stream = get_tokens(s)

    def token(self):
        """Retrieves the next token."""
        self.beforelast = self.last
        self.last = next(self.token_stream, None)
        return self.last

    def __iter__(self):
        t = self.token()
        while t is not None:
            yield t
            t = self.token()

    def split(self, s):
        """Splits a string into a list of strings which are whitespace-separated
        tokens.
        """
        vals = []
        self.input(s)
        l = c = -1
        ws = "WS"
        nl = "\n"
        for t in self:
            if t.type == ws:
                continue
            elif l < t.lineno:
                vals.append(t.value)
            elif len(vals) > 0 and c == t.lexpos:
                vals[-1] = vals[-1] + t.value
            else:
                vals.append(t.value)
            nnl = t.value.count(nl)
            if nnl == 0:
                l = t.lineno
                c = t.lexpos + len(t.value)
            else:
                l = t.lineno + nnl
                c = len(t.value.rpartition(nl)[-1])
        return vals

    #
    # All the tokens recognized by the lexer
    #
    @property
    def tokens(self):
        if self._tokens is None:
            t = (
                tuple(token_map.values())
                + (
                    "NAME",  # name tokens
                    "BANG",  # ! tokens
                    "WS",  # whitespace in subprocess mode
                    "LPAREN",
                    "RPAREN",  # ( )
                    "LBRACKET",
                    "RBRACKET",  # [ ]
                    "LBRACE",
                    "RBRACE",  # { }
                    "AT_LPAREN",  # @(
                    "BANG_LPAREN",  # !(
                    "BANG_LBRACKET",  # ![
                    "DOLLAR_LPAREN",  # $(
                    "DOLLAR_LBRACE",  # ${
                    "DOLLAR_LBRACKET",  # $[
                    "ATDOLLAR_LPAREN",  # @$(
                    "ERRORTOKEN",  # whoops!
                )
                + tuple(i.upper() for i in kwmod.kwlist)
            )
            self._tokens = t
        return self._tokens

#
# openpy
#
# -*- coding: utf-8 -*-
"""Tools to open ``*.py`` files as Unicode.

Uses the encoding specified within the file, as per PEP 263.

Much of the code is taken from the tokenize module in Python 3.2.

This file was forked from the IPython project:

* Copyright (c) 2008-2014, IPython Development Team
* Copyright (C) 2001-2007 Fernando Perez <fperez@colorado.edu>
* Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
* Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>
"""
# amalgamated io
# amalgamated re
# amalgamated xonsh.lazyasd
# amalgamated xonsh.tokenize
cookie_comment_re = LazyObject(
    lambda: re.compile(r"^\s*#.*coding[:=]\s*([-\w.]+)", re.UNICODE),
    globals(),
    "cookie_comment_re",
)


def source_to_unicode(txt, errors="replace", skip_encoding_cookie=True):
    """Converts a bytes string with python source code to unicode.

    Unicode strings are passed through unchanged. Byte strings are checked
    for the python source file encoding cookie to determine encoding.
    txt can be either a bytes buffer or a string containing the source
    code.
    """
    if isinstance(txt, str):
        return txt
    if isinstance(txt, bytes):
        buf = io.BytesIO(txt)
    else:
        buf = txt
    try:
        encoding, _ = detect_encoding(buf.readline)
    except SyntaxError:
        encoding = "ascii"
    buf.seek(0)
    text = io.TextIOWrapper(buf, encoding, errors=errors, line_buffering=True)
    text.mode = "r"
    if skip_encoding_cookie:
        return u"".join(strip_encoding_cookie(text))
    else:
        return text.read()


def strip_encoding_cookie(filelike):
    """Generator to pull lines from a text-mode file, skipping the encoding
    cookie if it is found in the first two lines.
    """
    it = iter(filelike)
    try:
        first = next(it)
        if not cookie_comment_re.match(first):
            yield first
        second = next(it)
        if not cookie_comment_re.match(second):
            yield second
    except StopIteration:
        return
    for line in it:
        yield line


def read_py_file(filename, skip_encoding_cookie=True):
    """Read a Python file, using the encoding declared inside the file.

    Parameters
    ----------
    filename : str
      The path to the file to read.
    skip_encoding_cookie : bool
      If True (the default), and the encoding declaration is found in the first
      two lines, that line will be excluded from the output - compiling a
      unicode string with an encoding declaration is a SyntaxError in Python 2.

    Returns
    -------
    A unicode string containing the contents of the file.
    """
    with tokopen(filename) as f:  # the open function defined in this module.
        if skip_encoding_cookie:
            return "".join(strip_encoding_cookie(f))
        else:
            return f.read()


def read_py_url(url, errors="replace", skip_encoding_cookie=True):
    """Read a Python file from a URL, using the encoding declared inside the file.

    Parameters
    ----------
    url : str
      The URL from which to fetch the file.
    errors : str
      How to handle decoding errors in the file. Options are the same as for
      bytes.decode(), but here 'replace' is the default.
    skip_encoding_cookie : bool
      If True (the default), and the encoding declaration is found in the first
      two lines, that line will be excluded from the output - compiling a
      unicode string with an encoding declaration is a SyntaxError in Python 2.

    Returns
    -------
    A unicode string containing the contents of the file.
    """
    # Deferred import for faster start
    try:
        from urllib.request import urlopen  # Py 3
    except ImportError:
        from urllib import urlopen
    response = urlopen(url)
    buf = io.BytesIO(response.read())
    return source_to_unicode(buf, errors, skip_encoding_cookie)


def _list_readline(x):
    """Given a list, returns a readline() function that returns the next element
    with each call.
    """
    x = iter(x)

    def readline():
        return next(x)

    return readline

#
# xontribs
#
"""Tools for helping manage xontributions."""
# amalgamated os
# amalgamated sys
# amalgamated json
# amalgamated builtins
# amalgamated argparse
# amalgamated functools
# amalgamated importlib
# amalgamated importlib.util
# amalgamated xonsh.tools
@functools.lru_cache(1)
def xontribs_json():
    return os.path.join(os.path.dirname(__file__), "xontribs.json")


def find_xontrib(name):
    """Finds a xontribution from its name."""
    if name.startswith("."):
        spec = importlib.util.find_spec(name, package="xontrib")
    else:
        spec = importlib.util.find_spec("." + name, package="xontrib")
    return spec or importlib.util.find_spec(name)


def xontrib_context(name):
    """Return a context dictionary for a xontrib of a given name."""
    spec = find_xontrib(name)
    if spec is None:
        return None
    m = importlib.import_module(spec.name)
    pubnames = getattr(m, "__all__", None)
    if pubnames is not None:
        ctx = {k: getattr(m, k) for k in pubnames}
    else:
        ctx = {k: getattr(m, k) for k in dir(m) if not k.startswith("_")}
    return ctx


def prompt_xontrib_install(names):
    """Returns a formatted string with name of xontrib package to prompt user"""
    md = xontrib_metadata()
    packages = []
    for name in names:
        for xontrib in md["xontribs"]:
            if xontrib["name"] == name:
                packages.append(xontrib["package"])

    print(
        "The following xontribs are enabled but not installed: \n"
        "   {xontribs}\n"
        "To install them run \n"
        "    xpip install {packages}".format(
            xontribs=" ".join(names), packages=" ".join(packages)
        )
    )


def update_context(name, ctx=None):
    """Updates a context in place from a xontrib. If ctx is not provided,
    then __xonsh__.ctx is updated.
    """
    if ctx is None:
        ctx = builtins.__xonsh__.ctx
    if not hasattr(update_context, "bad_imports"):
        update_context.bad_imports = []
    modctx = xontrib_context(name)
    if modctx is None:
        update_context.bad_imports.append(name)
        return ctx
    return ctx.update(modctx)


@functools.lru_cache()
def xontrib_metadata():
    """Loads and returns the xontribs.json file."""
    with open(xontribs_json(), "r") as f:
        md = json.load(f)
    return md


def xontribs_load(names, verbose=False):
    """Load xontribs from a list of names"""
    ctx = builtins.__xonsh__.ctx
    for name in names:
        if verbose:
            print("loading xontrib {0!r}".format(name))
        update_context(name, ctx=ctx)
    if update_context.bad_imports:
        prompt_xontrib_install(update_context.bad_imports)
        del update_context.bad_imports


def _load(ns):
    """load xontribs"""
    xontribs_load(ns.names, verbose=ns.verbose)


def _list(ns):
    """Lists xontribs."""
    meta = xontrib_metadata()
    data = []
    nname = 6  # ensures some buffer space.
    names = None if len(ns.names) == 0 else set(ns.names)
    for md in meta["xontribs"]:
        name = md["name"]
        if names is not None and md["name"] not in names:
            continue
        nname = max(nname, len(name))
        spec = find_xontrib(name)
        if spec is None:
            installed = loaded = False
        else:
            installed = True
            loaded = spec.name in sys.modules
        d = {"name": name, "installed": installed, "loaded": loaded}
        data.append(d)
    if ns.json:
        jdata = {d.pop("name"): d for d in data}
        s = json.dumps(jdata)
        print(s)
    else:
        s = ""
        for d in data:
            name = d["name"]
            lname = len(name)
            s += "{PURPLE}" + name + "{NO_COLOR}  " + " " * (nname - lname)
            if d["installed"]:
                s += "{GREEN}installed{NO_COLOR}      "
            else:
                s += "{RED}not-installed{NO_COLOR}  "
            if d["loaded"]:
                s += "{GREEN}loaded{NO_COLOR}"
            else:
                s += "{RED}not-loaded{NO_COLOR}"
            s += "\n"
        print_color(s[:-1])


@functools.lru_cache()
def _create_xontrib_parser():
    # parse command line args
    parser = argparse.ArgumentParser(
        prog="xontrib", description="Manages xonsh extensions"
    )
    subp = parser.add_subparsers(title="action", dest="action")
    load = subp.add_parser("load", help="loads xontribs")
    load.add_argument(
        "-v", "--verbose", action="store_true", default=False, dest="verbose"
    )
    load.add_argument("names", nargs="+", default=(), help="names of xontribs")
    lyst = subp.add_parser(
        "list", help=("list xontribs, whether they are " "installed, and loaded.")
    )
    lyst.add_argument(
        "--json", action="store_true", default=False, help="reports results as json"
    )
    lyst.add_argument("names", nargs="*", default=(), help="names of xontribs")
    return parser


_MAIN_XONTRIB_ACTIONS = {"load": _load, "list": _list}


@unthreadable
def xontribs_main(args=None, stdin=None):
    """Alias that loads xontribs"""
    if not args or (
        args[0] not in _MAIN_XONTRIB_ACTIONS and args[0] not in {"-h", "--help"}
    ):
        args.insert(0, "load")
    parser = _create_xontrib_parser()
    ns = parser.parse_args(args)
    if ns.action is None:  # apply default action
        ns = parser.parse_args(["load"] + args)
    return _MAIN_XONTRIB_ACTIONS[ns.action](ns)

#
# ansi_colors
#
"""Tools for helping with ANSI color codes."""
# amalgamated sys
# amalgamated warnings
# amalgamated builtins
# amalgamated xonsh.platform
# amalgamated xonsh.lazyasd
# amalgamated xonsh.color_tools
# amalgamated xonsh.tools
def ansi_partial_color_format(template, style="default", cmap=None, hide=False):
    """Formats a template string but only with respect to the colors.
    Another template string is returned, with the color values filled in.

    Parameters
    ----------
    template : str
        The template string, potentially with color names.
    style : str, optional
        Style name to look up color map from.
    cmap : dict, optional
        A color map to use, this will prevent the color map from being
        looked up via the style name.
    hide : bool, optional
        Whether to wrap the color codes in the \\001 and \\002 escape
        codes, so that the color codes are not counted against line
        length.

    Returns
    -------
    A template string with the color values filled in.
    """
    try:
        return _ansi_partial_color_format_main(
            template, style=style, cmap=cmap, hide=hide
        )
    except Exception:
        return template


def _ansi_partial_color_format_main(template, style="default", cmap=None, hide=False):
    if cmap is not None:
        pass
    elif style in ANSI_STYLES:
        cmap = ANSI_STYLES[style]
    else:
        try:  # dynamically loading the style
            cmap = ansi_style_by_name(style)
        except Exception:
            msg = "Could not find color style {0!r}, using default."
            print(msg.format(style), file=sys.stderr)
            builtins.__xonsh__.env["XONSH_COLOR_STYLE"] = "default"
            cmap = ANSI_STYLES["default"]
    esc = ("\001" if hide else "") + "\033["
    m = "m" + ("\002" if hide else "")
    bopen = "{"
    bclose = "}"
    colon = ":"
    expl = "!"
    toks = []
    for literal, field, spec, conv in FORMATTER.parse(template):
        toks.append(literal)
        if field is None:
            pass
        elif field in cmap:
            toks.extend([esc, cmap[field], m])
        elif "#" in field:
            field = field.lower()
            pre, _, post = field.partition("#")
            f_or_b = "38" if RE_BACKGROUND.search(pre) is None else "48"
            rgb, _, post = post.partition("_")
            c256, _ = rgb_to_256(rgb)
            color = f_or_b + ";5;" + c256
            mods = pre + "_" + post
            if "underline" in mods:
                color = "4;" + color
            if "bold" in mods:
                color = "1;" + color
            toks.extend([esc, color, m])
        elif field is not None:
            toks.append(bopen)
            toks.append(field)
            if conv is not None and len(conv) > 0:
                toks.append(expl)
                toks.append(conv)
            if spec is not None and len(spec) > 0:
                toks.append(colon)
                toks.append(spec)
            toks.append(bclose)
    return "".join(toks)


def ansi_color_style_names():
    """Returns an iterable of all ANSI color style names."""
    return ANSI_STYLES.keys()


def ansi_color_style(style="default"):
    """Returns the current color map."""
    if style in ANSI_STYLES:
        cmap = ANSI_STYLES[style]
    else:
        msg = "Could not find color style {0!r}, using default.".format(style)
        warnings.warn(msg, RuntimeWarning)
        cmap = ANSI_STYLES["default"]
    return cmap


def _ansi_expand_style(cmap):
    """Expands a style in order to more quickly make color map changes."""
    for key, val in list(cmap.items()):
        if key == "NO_COLOR":
            continue
        elif len(val) == 0:
            cmap["BOLD_" + key] = "1"
            cmap["UNDERLINE_" + key] = "4"
            cmap["BOLD_UNDERLINE_" + key] = "1;4"
            cmap["BACKGROUND_" + key] = val
        else:
            cmap["BOLD_" + key] = "1;" + val
            cmap["UNDERLINE_" + key] = "4;" + val
            cmap["BOLD_UNDERLINE_" + key] = "1;4;" + val
            cmap["BACKGROUND_" + key] = val.replace("38", "48", 1)


def _bw_style():
    style = {
        "BLACK": "",
        "BLUE": "",
        "CYAN": "",
        "GREEN": "",
        "INTENSE_BLACK": "",
        "INTENSE_BLUE": "",
        "INTENSE_CYAN": "",
        "INTENSE_GREEN": "",
        "INTENSE_PURPLE": "",
        "INTENSE_RED": "",
        "INTENSE_WHITE": "",
        "INTENSE_YELLOW": "",
        "NO_COLOR": "0",
        "PURPLE": "",
        "RED": "",
        "WHITE": "",
        "YELLOW": "",
    }
    _ansi_expand_style(style)
    return style


def _default_style():
    style = {
        # Reset
        "NO_COLOR": "0",  # Text Reset
        # Regular Colors
        "BLACK": "0;30",  # BLACK
        "RED": "0;31",  # RED
        "GREEN": "0;32",  # GREEN
        "YELLOW": "0;33",  # YELLOW
        "BLUE": "0;34",  # BLUE
        "PURPLE": "0;35",  # PURPLE
        "CYAN": "0;36",  # CYAN
        "WHITE": "0;37",  # WHITE
        # Bold
        "BOLD_BLACK": "1;30",  # BLACK
        "BOLD_RED": "1;31",  # RED
        "BOLD_GREEN": "1;32",  # GREEN
        "BOLD_YELLOW": "1;33",  # YELLOW
        "BOLD_BLUE": "1;34",  # BLUE
        "BOLD_PURPLE": "1;35",  # PURPLE
        "BOLD_CYAN": "1;36",  # CYAN
        "BOLD_WHITE": "1;37",  # WHITE
        # Underline
        "UNDERLINE_BLACK": "4;30",  # BLACK
        "UNDERLINE_RED": "4;31",  # RED
        "UNDERLINE_GREEN": "4;32",  # GREEN
        "UNDERLINE_YELLOW": "4;33",  # YELLOW
        "UNDERLINE_BLUE": "4;34",  # BLUE
        "UNDERLINE_PURPLE": "4;35",  # PURPLE
        "UNDERLINE_CYAN": "4;36",  # CYAN
        "UNDERLINE_WHITE": "4;37",  # WHITE
        # Bold, Underline
        "BOLD_UNDERLINE_BLACK": "1;4;30",  # BLACK
        "BOLD_UNDERLINE_RED": "1;4;31",  # RED
        "BOLD_UNDERLINE_GREEN": "1;4;32",  # GREEN
        "BOLD_UNDERLINE_YELLOW": "1;4;33",  # YELLOW
        "BOLD_UNDERLINE_BLUE": "1;4;34",  # BLUE
        "BOLD_UNDERLINE_PURPLE": "1;4;35",  # PURPLE
        "BOLD_UNDERLINE_CYAN": "1;4;36",  # CYAN
        "BOLD_UNDERLINE_WHITE": "1;4;37",  # WHITE
        # Background
        "BACKGROUND_BLACK": "40",  # BLACK
        "BACKGROUND_RED": "41",  # RED
        "BACKGROUND_GREEN": "42",  # GREEN
        "BACKGROUND_YELLOW": "43",  # YELLOW
        "BACKGROUND_BLUE": "44",  # BLUE
        "BACKGROUND_PURPLE": "45",  # PURPLE
        "BACKGROUND_CYAN": "46",  # CYAN
        "BACKGROUND_WHITE": "47",  # WHITE
        # High Intensity
        "INTENSE_BLACK": "0;90",  # BLACK
        "INTENSE_RED": "0;91",  # RED
        "INTENSE_GREEN": "0;92",  # GREEN
        "INTENSE_YELLOW": "0;93",  # YELLOW
        "INTENSE_BLUE": "0;94",  # BLUE
        "INTENSE_PURPLE": "0;95",  # PURPLE
        "INTENSE_CYAN": "0;96",  # CYAN
        "INTENSE_WHITE": "0;97",  # WHITE
        # Bold High Intensity
        "BOLD_INTENSE_BLACK": "1;90",  # BLACK
        "BOLD_INTENSE_RED": "1;91",  # RED
        "BOLD_INTENSE_GREEN": "1;92",  # GREEN
        "BOLD_INTENSE_YELLOW": "1;93",  # YELLOW
        "BOLD_INTENSE_BLUE": "1;94",  # BLUE
        "BOLD_INTENSE_PURPLE": "1;95",  # PURPLE
        "BOLD_INTENSE_CYAN": "1;96",  # CYAN
        "BOLD_INTENSE_WHITE": "1;97",  # WHITE
        # Underline High Intensity
        "UNDERLINE_INTENSE_BLACK": "4;90",  # BLACK
        "UNDERLINE_INTENSE_RED": "4;91",  # RED
        "UNDERLINE_INTENSE_GREEN": "4;92",  # GREEN
        "UNDERLINE_INTENSE_YELLOW": "4;93",  # YELLOW
        "UNDERLINE_INTENSE_BLUE": "4;94",  # BLUE
        "UNDERLINE_INTENSE_PURPLE": "4;95",  # PURPLE
        "UNDERLINE_INTENSE_CYAN": "4;96",  # CYAN
        "UNDERLINE_INTENSE_WHITE": "4;97",  # WHITE
        # Bold Underline High Intensity
        "BOLD_UNDERLINE_INTENSE_BLACK": "1;4;90",  # BLACK
        "BOLD_UNDERLINE_INTENSE_RED": "1;4;91",  # RED
        "BOLD_UNDERLINE_INTENSE_GREEN": "1;4;92",  # GREEN
        "BOLD_UNDERLINE_INTENSE_YELLOW": "1;4;93",  # YELLOW
        "BOLD_UNDERLINE_INTENSE_BLUE": "1;4;94",  # BLUE
        "BOLD_UNDERLINE_INTENSE_PURPLE": "1;4;95",  # PURPLE
        "BOLD_UNDERLINE_INTENSE_CYAN": "1;4;96",  # CYAN
        "BOLD_UNDERLINE_INTENSE_WHITE": "1;4;97",  # WHITE
        # High Intensity backgrounds
        "BACKGROUND_INTENSE_BLACK": "0;100",  # BLACK
        "BACKGROUND_INTENSE_RED": "0;101",  # RED
        "BACKGROUND_INTENSE_GREEN": "0;102",  # GREEN
        "BACKGROUND_INTENSE_YELLOW": "0;103",  # YELLOW
        "BACKGROUND_INTENSE_BLUE": "0;104",  # BLUE
        "BACKGROUND_INTENSE_PURPLE": "0;105",  # PURPLE
        "BACKGROUND_INTENSE_CYAN": "0;106",  # CYAN
        "BACKGROUND_INTENSE_WHITE": "0;107",  # WHITE
    }
    return style


def _monokai_style():
    style = {
        "NO_COLOR": "0",
        "BLACK": "38;5;16",
        "BLUE": "38;5;63",
        "CYAN": "38;5;81",
        "GREEN": "38;5;40",
        "PURPLE": "38;5;89",
        "RED": "38;5;124",
        "WHITE": "38;5;188",
        "YELLOW": "38;5;184",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;20",
        "INTENSE_CYAN": "38;5;44",
        "INTENSE_GREEN": "38;5;148",
        "INTENSE_PURPLE": "38;5;141",
        "INTENSE_RED": "38;5;197",
        "INTENSE_WHITE": "38;5;15",
        "INTENSE_YELLOW": "38;5;186",
    }
    _ansi_expand_style(style)
    return style


####################################
# Auto-generated below this line   #
####################################


def _algol_style():
    style = {
        "BLACK": "38;5;59",
        "BLUE": "38;5;59",
        "CYAN": "38;5;59",
        "GREEN": "38;5;59",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;102",
        "INTENSE_CYAN": "38;5;102",
        "INTENSE_GREEN": "38;5;102",
        "INTENSE_PURPLE": "38;5;102",
        "INTENSE_RED": "38;5;09",
        "INTENSE_WHITE": "38;5;102",
        "INTENSE_YELLOW": "38;5;102",
        "NO_COLOR": "0",
        "PURPLE": "38;5;59",
        "RED": "38;5;09",
        "WHITE": "38;5;102",
        "YELLOW": "38;5;09",
    }
    _ansi_expand_style(style)
    return style


def _algol_nu_style():
    style = {
        "BLACK": "38;5;59",
        "BLUE": "38;5;59",
        "CYAN": "38;5;59",
        "GREEN": "38;5;59",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;102",
        "INTENSE_CYAN": "38;5;102",
        "INTENSE_GREEN": "38;5;102",
        "INTENSE_PURPLE": "38;5;102",
        "INTENSE_RED": "38;5;09",
        "INTENSE_WHITE": "38;5;102",
        "INTENSE_YELLOW": "38;5;102",
        "NO_COLOR": "0",
        "PURPLE": "38;5;59",
        "RED": "38;5;09",
        "WHITE": "38;5;102",
        "YELLOW": "38;5;09",
    }
    _ansi_expand_style(style)
    return style


def _autumn_style():
    style = {
        "BLACK": "38;5;18",
        "BLUE": "38;5;19",
        "CYAN": "38;5;37",
        "GREEN": "38;5;34",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;33",
        "INTENSE_CYAN": "38;5;33",
        "INTENSE_GREEN": "38;5;64",
        "INTENSE_PURPLE": "38;5;217",
        "INTENSE_RED": "38;5;130",
        "INTENSE_WHITE": "38;5;145",
        "INTENSE_YELLOW": "38;5;217",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;130",
    }
    _ansi_expand_style(style)
    return style


def _borland_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;18",
        "CYAN": "38;5;30",
        "GREEN": "38;5;28",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;21",
        "INTENSE_CYAN": "38;5;194",
        "INTENSE_GREEN": "38;5;102",
        "INTENSE_PURPLE": "38;5;188",
        "INTENSE_RED": "38;5;09",
        "INTENSE_WHITE": "38;5;224",
        "INTENSE_YELLOW": "38;5;188",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;124",
    }
    _ansi_expand_style(style)
    return style


def _colorful_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;20",
        "CYAN": "38;5;31",
        "GREEN": "38;5;34",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;61",
        "INTENSE_CYAN": "38;5;145",
        "INTENSE_GREEN": "38;5;102",
        "INTENSE_PURPLE": "38;5;217",
        "INTENSE_RED": "38;5;166",
        "INTENSE_WHITE": "38;5;15",
        "INTENSE_YELLOW": "38;5;217",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;130",
    }
    _ansi_expand_style(style)
    return style


def _emacs_style():
    style = {
        "BLACK": "38;5;28",
        "BLUE": "38;5;18",
        "CYAN": "38;5;26",
        "GREEN": "38;5;34",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;26",
        "INTENSE_CYAN": "38;5;145",
        "INTENSE_GREEN": "38;5;34",
        "INTENSE_PURPLE": "38;5;129",
        "INTENSE_RED": "38;5;167",
        "INTENSE_WHITE": "38;5;145",
        "INTENSE_YELLOW": "38;5;145",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;130",
    }
    _ansi_expand_style(style)
    return style


def _friendly_style():
    style = {
        "BLACK": "38;5;22",
        "BLUE": "38;5;18",
        "CYAN": "38;5;31",
        "GREEN": "38;5;34",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;74",
        "INTENSE_CYAN": "38;5;74",
        "INTENSE_GREEN": "38;5;71",
        "INTENSE_PURPLE": "38;5;134",
        "INTENSE_RED": "38;5;167",
        "INTENSE_WHITE": "38;5;15",
        "INTENSE_YELLOW": "38;5;145",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;166",
    }
    _ansi_expand_style(style)
    return style


def _fruity_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;32",
        "CYAN": "38;5;32",
        "GREEN": "38;5;28",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;33",
        "INTENSE_CYAN": "38;5;33",
        "INTENSE_GREEN": "38;5;102",
        "INTENSE_PURPLE": "38;5;198",
        "INTENSE_RED": "38;5;202",
        "INTENSE_WHITE": "38;5;15",
        "INTENSE_YELLOW": "38;5;187",
        "NO_COLOR": "0",
        "PURPLE": "38;5;198",
        "RED": "38;5;09",
        "WHITE": "38;5;187",
        "YELLOW": "38;5;202",
    }
    _ansi_expand_style(style)
    return style


def _igor_style():
    style = {
        "BLACK": "38;5;34",
        "BLUE": "38;5;21",
        "CYAN": "38;5;30",
        "GREEN": "38;5;34",
        "INTENSE_BLACK": "38;5;30",
        "INTENSE_BLUE": "38;5;21",
        "INTENSE_CYAN": "38;5;30",
        "INTENSE_GREEN": "38;5;34",
        "INTENSE_PURPLE": "38;5;163",
        "INTENSE_RED": "38;5;166",
        "INTENSE_WHITE": "38;5;163",
        "INTENSE_YELLOW": "38;5;166",
        "NO_COLOR": "0",
        "PURPLE": "38;5;163",
        "RED": "38;5;166",
        "WHITE": "38;5;163",
        "YELLOW": "38;5;166",
    }
    _ansi_expand_style(style)
    return style


def _lovelace_style():
    style = {
        "BLACK": "38;5;59",
        "BLUE": "38;5;25",
        "CYAN": "38;5;29",
        "GREEN": "38;5;65",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;25",
        "INTENSE_CYAN": "38;5;102",
        "INTENSE_GREEN": "38;5;29",
        "INTENSE_PURPLE": "38;5;133",
        "INTENSE_RED": "38;5;131",
        "INTENSE_WHITE": "38;5;102",
        "INTENSE_YELLOW": "38;5;136",
        "NO_COLOR": "0",
        "PURPLE": "38;5;133",
        "RED": "38;5;124",
        "WHITE": "38;5;102",
        "YELLOW": "38;5;130",
    }
    _ansi_expand_style(style)
    return style


def _manni_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;18",
        "CYAN": "38;5;30",
        "GREEN": "38;5;40",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;105",
        "INTENSE_CYAN": "38;5;45",
        "INTENSE_GREEN": "38;5;113",
        "INTENSE_PURPLE": "38;5;165",
        "INTENSE_RED": "38;5;202",
        "INTENSE_WHITE": "38;5;224",
        "INTENSE_YELLOW": "38;5;221",
        "NO_COLOR": "0",
        "PURPLE": "38;5;165",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;166",
    }
    _ansi_expand_style(style)
    return style


def _murphy_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;18",
        "CYAN": "38;5;31",
        "GREEN": "38;5;34",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;63",
        "INTENSE_CYAN": "38;5;86",
        "INTENSE_GREEN": "38;5;86",
        "INTENSE_PURPLE": "38;5;213",
        "INTENSE_RED": "38;5;209",
        "INTENSE_WHITE": "38;5;15",
        "INTENSE_YELLOW": "38;5;222",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;166",
    }
    _ansi_expand_style(style)
    return style


def _native_style():
    style = {
        "BLACK": "38;5;52",
        "BLUE": "38;5;67",
        "CYAN": "38;5;31",
        "GREEN": "38;5;64",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;68",
        "INTENSE_CYAN": "38;5;87",
        "INTENSE_GREEN": "38;5;70",
        "INTENSE_PURPLE": "38;5;188",
        "INTENSE_RED": "38;5;160",
        "INTENSE_WHITE": "38;5;15",
        "INTENSE_YELLOW": "38;5;214",
        "NO_COLOR": "0",
        "PURPLE": "38;5;59",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;124",
    }
    _ansi_expand_style(style)
    return style


def _paraiso_dark_style():
    style = {
        "BLACK": "38;5;95",
        "BLUE": "38;5;97",
        "CYAN": "38;5;39",
        "GREEN": "38;5;72",
        "INTENSE_BLACK": "38;5;95",
        "INTENSE_BLUE": "38;5;97",
        "INTENSE_CYAN": "38;5;79",
        "INTENSE_GREEN": "38;5;72",
        "INTENSE_PURPLE": "38;5;188",
        "INTENSE_RED": "38;5;203",
        "INTENSE_WHITE": "38;5;188",
        "INTENSE_YELLOW": "38;5;220",
        "NO_COLOR": "0",
        "PURPLE": "38;5;97",
        "RED": "38;5;203",
        "WHITE": "38;5;79",
        "YELLOW": "38;5;214",
    }
    _ansi_expand_style(style)
    return style


def _paraiso_light_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;16",
        "CYAN": "38;5;39",
        "GREEN": "38;5;72",
        "INTENSE_BLACK": "38;5;16",
        "INTENSE_BLUE": "38;5;97",
        "INTENSE_CYAN": "38;5;79",
        "INTENSE_GREEN": "38;5;72",
        "INTENSE_PURPLE": "38;5;97",
        "INTENSE_RED": "38;5;203",
        "INTENSE_WHITE": "38;5;79",
        "INTENSE_YELLOW": "38;5;220",
        "NO_COLOR": "0",
        "PURPLE": "38;5;97",
        "RED": "38;5;16",
        "WHITE": "38;5;102",
        "YELLOW": "38;5;214",
    }
    _ansi_expand_style(style)
    return style


def _pastie_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;20",
        "CYAN": "38;5;25",
        "GREEN": "38;5;28",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;61",
        "INTENSE_CYAN": "38;5;194",
        "INTENSE_GREEN": "38;5;34",
        "INTENSE_PURPLE": "38;5;188",
        "INTENSE_RED": "38;5;172",
        "INTENSE_WHITE": "38;5;15",
        "INTENSE_YELLOW": "38;5;188",
        "NO_COLOR": "0",
        "PURPLE": "38;5;125",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;130",
    }
    _ansi_expand_style(style)
    return style


def _perldoc_style():
    style = {
        "BLACK": "38;5;18",
        "BLUE": "38;5;18",
        "CYAN": "38;5;31",
        "GREEN": "38;5;34",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;134",
        "INTENSE_CYAN": "38;5;145",
        "INTENSE_GREEN": "38;5;28",
        "INTENSE_PURPLE": "38;5;134",
        "INTENSE_RED": "38;5;167",
        "INTENSE_WHITE": "38;5;188",
        "INTENSE_YELLOW": "38;5;188",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;166",
    }
    _ansi_expand_style(style)
    return style


def _rrt_style():
    style = {
        "BLACK": "38;5;09",
        "BLUE": "38;5;117",
        "CYAN": "38;5;117",
        "GREEN": "38;5;46",
        "INTENSE_BLACK": "38;5;117",
        "INTENSE_BLUE": "38;5;117",
        "INTENSE_CYAN": "38;5;122",
        "INTENSE_GREEN": "38;5;46",
        "INTENSE_PURPLE": "38;5;213",
        "INTENSE_RED": "38;5;09",
        "INTENSE_WHITE": "38;5;188",
        "INTENSE_YELLOW": "38;5;222",
        "NO_COLOR": "0",
        "PURPLE": "38;5;213",
        "RED": "38;5;09",
        "WHITE": "38;5;117",
        "YELLOW": "38;5;09",
    }
    _ansi_expand_style(style)
    return style


def _tango_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;20",
        "CYAN": "38;5;61",
        "GREEN": "38;5;34",
        "INTENSE_BLACK": "38;5;24",
        "INTENSE_BLUE": "38;5;62",
        "INTENSE_CYAN": "38;5;15",
        "INTENSE_GREEN": "38;5;64",
        "INTENSE_PURPLE": "38;5;15",
        "INTENSE_RED": "38;5;09",
        "INTENSE_WHITE": "38;5;15",
        "INTENSE_YELLOW": "38;5;178",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;15",
        "YELLOW": "38;5;94",
    }
    _ansi_expand_style(style)
    return style


def _trac_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;18",
        "CYAN": "38;5;30",
        "GREEN": "38;5;100",
        "INTENSE_BLACK": "38;5;59",
        "INTENSE_BLUE": "38;5;60",
        "INTENSE_CYAN": "38;5;194",
        "INTENSE_GREEN": "38;5;102",
        "INTENSE_PURPLE": "38;5;188",
        "INTENSE_RED": "38;5;137",
        "INTENSE_WHITE": "38;5;224",
        "INTENSE_YELLOW": "38;5;188",
        "NO_COLOR": "0",
        "PURPLE": "38;5;90",
        "RED": "38;5;124",
        "WHITE": "38;5;145",
        "YELLOW": "38;5;100",
    }
    _ansi_expand_style(style)
    return style


def _vim_style():
    style = {
        "BLACK": "38;5;18",
        "BLUE": "38;5;18",
        "CYAN": "38;5;44",
        "GREEN": "38;5;40",
        "INTENSE_BLACK": "38;5;60",
        "INTENSE_BLUE": "38;5;68",
        "INTENSE_CYAN": "38;5;44",
        "INTENSE_GREEN": "38;5;40",
        "INTENSE_PURPLE": "38;5;164",
        "INTENSE_RED": "38;5;09",
        "INTENSE_WHITE": "38;5;188",
        "INTENSE_YELLOW": "38;5;184",
        "NO_COLOR": "0",
        "PURPLE": "38;5;164",
        "RED": "38;5;160",
        "WHITE": "38;5;188",
        "YELLOW": "38;5;160",
    }
    _ansi_expand_style(style)
    return style


def _vs_style():
    style = {
        "BLACK": "38;5;28",
        "BLUE": "38;5;21",
        "CYAN": "38;5;31",
        "GREEN": "38;5;28",
        "INTENSE_BLACK": "38;5;31",
        "INTENSE_BLUE": "38;5;31",
        "INTENSE_CYAN": "38;5;31",
        "INTENSE_GREEN": "38;5;31",
        "INTENSE_PURPLE": "38;5;31",
        "INTENSE_RED": "38;5;09",
        "INTENSE_WHITE": "38;5;31",
        "INTENSE_YELLOW": "38;5;31",
        "NO_COLOR": "0",
        "PURPLE": "38;5;124",
        "RED": "38;5;124",
        "WHITE": "38;5;31",
        "YELLOW": "38;5;124",
    }
    _ansi_expand_style(style)
    return style


def _xcode_style():
    style = {
        "BLACK": "38;5;16",
        "BLUE": "38;5;20",
        "CYAN": "38;5;60",
        "GREEN": "38;5;28",
        "INTENSE_BLACK": "38;5;60",
        "INTENSE_BLUE": "38;5;20",
        "INTENSE_CYAN": "38;5;60",
        "INTENSE_GREEN": "38;5;60",
        "INTENSE_PURPLE": "38;5;126",
        "INTENSE_RED": "38;5;160",
        "INTENSE_WHITE": "38;5;60",
        "INTENSE_YELLOW": "38;5;94",
        "NO_COLOR": "0",
        "PURPLE": "38;5;126",
        "RED": "38;5;160",
        "WHITE": "38;5;60",
        "YELLOW": "38;5;94",
    }
    _ansi_expand_style(style)
    return style


ANSI_STYLES = LazyDict(
    {
        "algol": _algol_style,
        "algol_nu": _algol_nu_style,
        "autumn": _autumn_style,
        "borland": _borland_style,
        "bw": _bw_style,
        "colorful": _colorful_style,
        "default": _default_style,
        "emacs": _emacs_style,
        "friendly": _friendly_style,
        "fruity": _fruity_style,
        "igor": _igor_style,
        "lovelace": _lovelace_style,
        "manni": _manni_style,
        "monokai": _monokai_style,
        "murphy": _murphy_style,
        "native": _native_style,
        "paraiso-dark": _paraiso_dark_style,
        "paraiso-light": _paraiso_light_style,
        "pastie": _pastie_style,
        "perldoc": _perldoc_style,
        "rrt": _rrt_style,
        "tango": _tango_style,
        "trac": _trac_style,
        "vim": _vim_style,
        "vs": _vs_style,
        "xcode": _xcode_style,
    },
    globals(),
    "ANSI_STYLES",
)

del (
    _algol_style,
    _algol_nu_style,
    _autumn_style,
    _borland_style,
    _bw_style,
    _colorful_style,
    _default_style,
    _emacs_style,
    _friendly_style,
    _fruity_style,
    _igor_style,
    _lovelace_style,
    _manni_style,
    _monokai_style,
    _murphy_style,
    _native_style,
    _paraiso_dark_style,
    _paraiso_light_style,
    _pastie_style,
    _perldoc_style,
    _rrt_style,
    _tango_style,
    _trac_style,
    _vim_style,
    _vs_style,
    _xcode_style,
)


#
# Dynamically generated styles
#
def make_ansi_style(palette):
    """Makes an ANSI color style from a color palette"""
    style = {"NO_COLOR": "0"}
    for name, t in BASE_XONSH_COLORS.items():
        closest = find_closest_color(t, palette)
        if len(closest) == 3:
            closest = "".join([a * 2 for a in closest])
        short = rgb2short(closest)[0]
        style[name] = "38;5;" + short
        style["BOLD_" + name] = "1;38;5;" + short
        style["UNDERLINE_" + name] = "4;38;5;" + short
        style["BOLD_UNDERLINE_" + name] = "1;4;38;5;" + short
        style["BACKGROUND_" + name] = "48;5;" + short
    return style


def ansi_style_by_name(name):
    """Gets or makes an ANSI color style by name. If the styles does not
    exist, it will look for a style using the pygments name.
    """
    if name in ANSI_STYLES:
        return ANSI_STYLES[name]
    elif not HAS_PYGMENTS:
        raise KeyError("could not find style {0!r}".format(name))
    from xonsh.pygments_cache import get_style_by_name

    pstyle = get_style_by_name(name)
    palette = make_palette(pstyle.styles.values())
    astyle = make_ansi_style(palette)
    ANSI_STYLES[name] = astyle
    return astyle

#
# dirstack
#
# -*- coding: utf-8 -*-
"""Directory stack and associated utilities for the xonsh shell."""
# amalgamated os
# amalgamated glob
# amalgamated argparse
# amalgamated builtins
# amalgamated subprocess
# amalgamated xonsh.lazyasd
# amalgamated xonsh.tools
# amalgamated xonsh.events
# amalgamated xonsh.platform
DIRSTACK = []
"""A list containing the currently remembered directories."""
_unc_tempDrives = {}
""" drive: sharePath for temp drive letters we create for UNC mapping"""


def _unc_check_enabled() -> bool:
    r"""Check whether CMD.EXE is enforcing no-UNC-as-working-directory check.

    Check can be disabled by setting {HKCU, HKLM}/SOFTWARE\Microsoft\Command Processor\DisableUNCCheck:REG_DWORD=1

    Returns:
        True if `CMD.EXE` is enforcing the check (default Windows situation)
        False if check is explicitly disabled.
    """
    if not ON_WINDOWS:
        return

    import winreg

    wval = None

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"software\microsoft\command processor"
        )
        wval, wtype = winreg.QueryValueEx(key, "DisableUNCCheck")
        winreg.CloseKey(key)
    except OSError:
        pass

    if wval is None:
        try:
            key2 = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"software\microsoft\command processor"
            )
            wval, wtype = winreg.QueryValueEx(key2, "DisableUNCCheck")
            winreg.CloseKey(key2)
        except OSError as e:  # NOQA
            pass

    return False if wval else True


def _is_unc_path(some_path) -> bool:
    """True if path starts with 2 backward (or forward, due to python path hacking) slashes."""
    return (
        len(some_path) > 1
        and some_path[0] == some_path[1]
        and some_path[0] in (os.sep, os.altsep)
    )


def _unc_map_temp_drive(unc_path) -> str:
    r"""Map a new temporary drive letter for each distinct share,
    unless `CMD.EXE` is not insisting on non-UNC working directory.

    Emulating behavior of `CMD.EXE` `pushd`, create a new mapped drive (starting from Z: towards A:, skipping existing
     drive letters) for each new UNC path user selects.

    Args:
        unc_path: the path specified by user.  Assumed to be a UNC path of form \\<server>\share...

    Returns:
        a replacement for `unc_path` to be used as the actual new working directory.
        Note that the drive letter may be a the same as one already mapped if the server and share portion of `unc_path`
         is the same as one still active on the stack.
    """
    global _unc_tempDrives
    assert unc_path[1] in (os.sep, os.altsep), "unc_path is UNC form of path"

    if not _unc_check_enabled():
        return unc_path
    else:
        unc_share, rem_path = os.path.splitdrive(unc_path)
        unc_share = unc_share.casefold()
        for d in _unc_tempDrives:
            if _unc_tempDrives[d] == unc_share:
                return os.path.join(d, rem_path)

        for dord in range(ord("z"), ord("a"), -1):
            d = chr(dord) + ":"
            if not os.path.isdir(d):  # find unused drive letter starting from z:
                subprocess.check_output(
                    ["NET", "USE", d, unc_share], universal_newlines=True
                )
                _unc_tempDrives[d] = unc_share
                return os.path.join(d, rem_path)


def _unc_unmap_temp_drive(left_drive, cwd):
    """Unmap a temporary drive letter if it is no longer needed.
    Called after popping `DIRSTACK` and changing to new working directory, so we need stack *and*
    new current working directory to be sure drive letter no longer needed.

    Args:
        left_drive: driveletter (and colon) of working directory we just left
        cwd: full path of new current working directory
    """

    global _unc_tempDrives

    if left_drive not in _unc_tempDrives:  # if not one we've mapped, don't unmap it
        return

    for p in DIRSTACK + [cwd]:  # if still in use , don't unmap it.
        if p.casefold().startswith(left_drive):
            return

    _unc_tempDrives.pop(left_drive)
    subprocess.check_output(
        ["NET", "USE", left_drive, "/delete"], universal_newlines=True
    )


events.doc(
    "on_chdir",
    """
on_chdir(olddir: str, newdir: str) -> None

Fires when the current directory is changed for any reason.
""",
)


def _get_cwd():
    try:
        return os.getcwd()
    except (OSError, FileNotFoundError):
        return None


def _change_working_directory(newdir, follow_symlinks=False):
    env = builtins.__xonsh__.env
    old = env["PWD"]
    new = os.path.join(old, newdir)
    absnew = os.path.abspath(new)

    if follow_symlinks:
        absnew = os.path.realpath(absnew)

    try:
        os.chdir(absnew)
    except (OSError, FileNotFoundError):
        if new.endswith(get_sep()):
            new = new[:-1]
        if os.path.basename(new) == "..":
            env["PWD"] = new
    else:
        if old is not None:
            env["OLDPWD"] = old
        if new is not None:
            env["PWD"] = absnew

    # Fire event if the path actually changed
    if old != env["PWD"]:
        events.on_chdir.fire(olddir=old, newdir=env["PWD"])


def _try_cdpath(apath):
    # NOTE: this CDPATH implementation differs from the bash one.
    # In bash if a CDPATH is set, an unqualified local folder
    # is considered after all CDPATHs, example:
    # CDPATH=$HOME/src (with src/xonsh/ inside)
    # $ cd xonsh -> src/xonsh (with xonsh/xonsh)
    # a second $ cd xonsh has no effects, to move in the nested xonsh
    # in bash a full $ cd ./xonsh is needed.
    # In xonsh a relative folder is always preferred.
    env = builtins.__xonsh__.env
    cdpaths = env.get("CDPATH")
    for cdp in cdpaths:
        globber = builtins.__xonsh__.expand_path(os.path.join(cdp, apath))
        for cdpath_prefixed_path in glob.iglob(globber):
            return cdpath_prefixed_path
    return apath


def cd(args, stdin=None):
    """Changes the directory.

    If no directory is specified (i.e. if `args` is None) then this
    changes to the current user's home directory.
    """
    env = builtins.__xonsh__.env
    oldpwd = env.get("OLDPWD", None)
    cwd = env["PWD"]

    follow_symlinks = False
    if len(args) > 0 and args[0] == "-P":
        follow_symlinks = True
        del args[0]

    if len(args) == 0:
        d = os.path.expanduser("~")
    elif len(args) == 1:
        d = os.path.expanduser(args[0])
        if not os.path.isdir(d):
            if d == "-":
                if oldpwd is not None:
                    d = oldpwd
                else:
                    return "", "cd: no previous directory stored\n", 1
            elif d.startswith("-"):
                try:
                    num = int(d[1:])
                except ValueError:
                    return "", "cd: Invalid destination: {0}\n".format(d), 1
                if num == 0:
                    return None, None, 0
                elif num < 0:
                    return "", "cd: Invalid destination: {0}\n".format(d), 1
                elif num > len(DIRSTACK):
                    e = "cd: Too few elements in dirstack ({0} elements)\n"
                    return "", e.format(len(DIRSTACK)), 1
                else:
                    d = DIRSTACK[num - 1]
            else:
                d = _try_cdpath(d)
    else:
        return (
            "",
            (
                "cd takes 0 or 1 arguments, not {0}. An additional `-P` "
                "flag can be passed in first position to follow symlinks."
                "\n".format(len(args))
            ),
            1,
        )
    if not os.path.exists(d):
        return "", "cd: no such file or directory: {0}\n".format(d), 1
    if not os.path.isdir(d):
        return "", "cd: {0} is not a directory\n".format(d), 1
    if not os.access(d, os.X_OK):
        return "", "cd: permission denied: {0}\n".format(d), 1
    if (
        ON_WINDOWS
        and _is_unc_path(d)
        and _unc_check_enabled()
        and (not env.get("AUTO_PUSHD"))
    ):
        return (
            "",
            "cd: can't cd to UNC path on Windows, unless $AUTO_PUSHD set or reg entry "
            + r"HKCU\SOFTWARE\MICROSOFT\Command Processor\DisableUNCCheck:DWORD = 1"
            + "\n",
            1,
        )

    # now, push the directory onto the dirstack if AUTO_PUSHD is set
    if cwd is not None and env.get("AUTO_PUSHD"):
        pushd(["-n", "-q", cwd])
        if ON_WINDOWS and _is_unc_path(d):
            d = _unc_map_temp_drive(d)
    _change_working_directory(d, follow_symlinks)
    return None, None, 0


@lazyobject
def pushd_parser():
    parser = argparse.ArgumentParser(prog="pushd")
    parser.add_argument("dir", nargs="?")
    parser.add_argument(
        "-n",
        dest="cd",
        help="Suppresses the normal change of directory when"
        " adding directories to the stack, so that only the"
        " stack is manipulated.",
        action="store_false",
    )
    parser.add_argument(
        "-q",
        dest="quiet",
        help="Do not call dirs, regardless of $PUSHD_SILENT",
        action="store_true",
    )
    return parser


def pushd(args, stdin=None):
    r"""xonsh command: pushd

    Adds a directory to the top of the directory stack, or rotates the stack,
    making the new top of the stack the current working directory.

    On Windows, if the path is a UNC path (begins with `\\<server>\<share>`) and if the `DisableUNCCheck` registry
    value is not enabled, creates a temporary mapped drive letter and sets the working directory there, emulating
    behavior of `PUSHD` in `CMD.EXE`
    """
    global DIRSTACK

    try:
        args = pushd_parser.parse_args(args)
    except SystemExit:
        return None, None, 1

    env = builtins.__xonsh__.env

    pwd = env["PWD"]

    if env.get("PUSHD_MINUS", False):
        BACKWARD = "-"
        FORWARD = "+"
    else:
        BACKWARD = "+"
        FORWARD = "-"

    if args.dir is None:
        try:
            new_pwd = DIRSTACK.pop(0)
        except IndexError:
            e = "pushd: Directory stack is empty\n"
            return None, e, 1
    elif os.path.isdir(args.dir):
        new_pwd = args.dir
    else:
        try:
            num = int(args.dir[1:])
        except ValueError:
            e = "Invalid argument to pushd: {0}\n"
            return None, e.format(args.dir), 1

        if num < 0:
            e = "Invalid argument to pushd: {0}\n"
            return None, e.format(args.dir), 1

        if num > len(DIRSTACK):
            e = "Too few elements in dirstack ({0} elements)\n"
            return None, e.format(len(DIRSTACK)), 1
        elif args.dir.startswith(FORWARD):
            if num == len(DIRSTACK):
                new_pwd = None
            else:
                new_pwd = DIRSTACK.pop(len(DIRSTACK) - 1 - num)
        elif args.dir.startswith(BACKWARD):
            if num == 0:
                new_pwd = None
            else:
                new_pwd = DIRSTACK.pop(num - 1)
        else:
            e = "Invalid argument to pushd: {0}\n"
            return None, e.format(args.dir), 1
    if new_pwd is not None:
        if ON_WINDOWS and _is_unc_path(new_pwd):
            new_pwd = _unc_map_temp_drive(new_pwd)
        if args.cd:
            DIRSTACK.insert(0, os.path.expanduser(pwd))
            _change_working_directory(new_pwd)
        else:
            DIRSTACK.insert(0, os.path.expanduser(new_pwd))

    maxsize = env.get("DIRSTACK_SIZE")
    if len(DIRSTACK) > maxsize:
        DIRSTACK = DIRSTACK[:maxsize]

    if not args.quiet and not env.get("PUSHD_SILENT"):
        return dirs([], None)

    return None, None, 0


@lazyobject
def popd_parser():
    parser = argparse.ArgumentParser(prog="popd")
    parser.add_argument("dir", nargs="?")
    parser.add_argument(
        "-n",
        dest="cd",
        help="Suppresses the normal change of directory when"
        " adding directories to the stack, so that only the"
        " stack is manipulated.",
        action="store_false",
    )
    parser.add_argument(
        "-q",
        dest="quiet",
        help="Do not call dirs, regardless of $PUSHD_SILENT",
        action="store_true",
    )
    return parser


def popd(args, stdin=None):
    """
    xonsh command: popd

    Removes entries from the directory stack.
    """
    global DIRSTACK

    try:
        args = pushd_parser.parse_args(args)
    except SystemExit:
        return None, None, 1

    env = builtins.__xonsh__.env

    if env.get("PUSHD_MINUS"):
        BACKWARD = "-"
        FORWARD = "+"
    else:
        BACKWARD = "-"
        FORWARD = "+"

    if args.dir is None:
        try:
            new_pwd = DIRSTACK.pop(0)
        except IndexError:
            e = "popd: Directory stack is empty\n"
            return None, e, 1
    else:
        try:
            num = int(args.dir[1:])
        except ValueError:
            e = "Invalid argument to popd: {0}\n"
            return None, e.format(args.dir), 1

        if num < 0:
            e = "Invalid argument to popd: {0}\n"
            return None, e.format(args.dir), 1

        if num > len(DIRSTACK):
            e = "Too few elements in dirstack ({0} elements)\n"
            return None, e.format(len(DIRSTACK)), 1
        elif args.dir.startswith(FORWARD):
            if num == len(DIRSTACK):
                new_pwd = DIRSTACK.pop(0)
            else:
                new_pwd = None
                DIRSTACK.pop(len(DIRSTACK) - 1 - num)
        elif args.dir.startswith(BACKWARD):
            if num == 0:
                new_pwd = DIRSTACK.pop(0)
            else:
                new_pwd = None
                DIRSTACK.pop(num - 1)
        else:
            e = "Invalid argument to popd: {0}\n"
            return None, e.format(args.dir), 1

    if new_pwd is not None:
        e = None
        if args.cd:
            env = builtins.__xonsh__.env
            pwd = env["PWD"]

            _change_working_directory(new_pwd)

            if ON_WINDOWS:
                drive, rem_path = os.path.splitdrive(pwd)
                _unc_unmap_temp_drive(drive.casefold(), new_pwd)

    if not args.quiet and not env.get("PUSHD_SILENT"):
        return dirs([], None)

    return None, None, 0


@lazyobject
def dirs_parser():
    parser = argparse.ArgumentParser(prog="dirs")
    parser.add_argument("N", nargs="?")
    parser.add_argument(
        "-c",
        dest="clear",
        help="Clears the directory stack by deleting all of" " the entries.",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        dest="print_long",
        help="Print the directory stack with one entry per" " line.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        dest="verbose",
        help="Print the directory stack with one entry per"
        " line, prefixing each entry with its index in the"
        " stack.",
        action="store_true",
    )
    parser.add_argument(
        "-l",
        dest="long",
        help="Produces a longer listing; the default listing"
        " format uses a tilde to denote the home directory.",
        action="store_true",
    )
    return parser


def dirs(args, stdin=None):
    """xonsh command: dirs

    Displays the list of currently remembered directories.  Can also be used
    to clear the directory stack.
    """
    global DIRSTACK
    try:
        args = dirs_parser.parse_args(args)
    except SystemExit:
        return None, None

    env = builtins.__xonsh__.env
    dirstack = [os.path.expanduser(env["PWD"])] + DIRSTACK

    if env.get("PUSHD_MINUS"):
        BACKWARD = "-"
        FORWARD = "+"
    else:
        BACKWARD = "-"
        FORWARD = "+"

    if args.clear:
        DIRSTACK = []
        return None, None, 0

    if args.long:
        o = dirstack
    else:
        d = os.path.expanduser("~")
        o = [i.replace(d, "~") for i in dirstack]

    if args.verbose:
        out = ""
        pad = len(str(len(o) - 1))
        for (ix, e) in enumerate(o):
            blanks = " " * (pad - len(str(ix)))
            out += "\n{0}{1} {2}".format(blanks, ix, e)
        out = out[1:]
    elif args.print_long:
        out = "\n".join(o)
    else:
        out = " ".join(o)

    N = args.N
    if N is not None:
        try:
            num = int(N[1:])
        except ValueError:
            e = "Invalid argument to dirs: {0}\n"
            return None, e.format(N), 1

        if num < 0:
            e = "Invalid argument to dirs: {0}\n"
            return None, e.format(len(o)), 1

        if num >= len(o):
            e = "Too few elements in dirstack ({0} elements)\n"
            return None, e.format(len(o)), 1

        if N.startswith(BACKWARD):
            idx = num
        elif N.startswith(FORWARD):
            idx = len(o) - 1 - num
        else:
            e = "Invalid argument to dirs: {0}\n"
            return None, e.format(N), 1

        out = o[idx]

    return out + "\n", None, 0

#
# proc
#
# -*- coding: utf-8 -*-
"""Interface for running Python functions as subprocess-mode commands.

Code for several helper methods in the `ProcProxy` class have been reproduced
without modification from `subprocess.py` in the Python 3.4.2 standard library.
The contents of `subprocess.py` (and, thus, the reproduced methods) are
Copyright (c) 2003-2005 by Peter Astrand <astrand@lysator.liu.se> and were
licensed to the Python Software foundation under a Contributor Agreement.
"""
# amalgamated io
# amalgamated os
# amalgamated re
# amalgamated sys
# amalgamated time
queue = _LazyModule.load('queue', 'queue')
array = _LazyModule.load('array', 'array')
# amalgamated ctypes
# amalgamated signal
# amalgamated inspect
# amalgamated builtins
# amalgamated functools
# amalgamated threading
# amalgamated subprocess
# amalgamated collections.abc
# amalgamated xonsh.platform
# amalgamated xonsh.tools
# amalgamated xonsh.lazyasd
# amalgamated xonsh.jobs
# amalgamated xonsh.lazyimps
# amalgamated xonsh.tools
foreground = unthreadable


@lazyobject
def STDOUT_CAPTURE_KINDS():
    return frozenset(["stdout", "object"])


# The following escape codes are xterm codes.
# See http://rtfm.etla.org/xterm/ctlseq.html for more.
MODE_NUMS = ("1049", "47", "1047")
START_ALTERNATE_MODE = LazyObject(
    lambda: frozenset("\x1b[?{0}h".format(i).encode() for i in MODE_NUMS),
    globals(),
    "START_ALTERNATE_MODE",
)
END_ALTERNATE_MODE = LazyObject(
    lambda: frozenset("\x1b[?{0}l".format(i).encode() for i in MODE_NUMS),
    globals(),
    "END_ALTERNATE_MODE",
)
ALTERNATE_MODE_FLAGS = LazyObject(
    lambda: tuple(START_ALTERNATE_MODE) + tuple(END_ALTERNATE_MODE),
    globals(),
    "ALTERNATE_MODE_FLAGS",
)
RE_HIDDEN_BYTES = LazyObject(
    lambda: re.compile(b"(\001.*?\002)"), globals(), "RE_HIDDEN"
)


@lazyobject
def RE_VT100_ESCAPE():
    return re.compile(b"(\x9B|\x1B\\[)[0-?]*[ -\\/]*[@-~]")


@lazyobject
def RE_HIDE_ESCAPE():
    return re.compile(
        b"(" + RE_HIDDEN_BYTES.pattern + b"|" + RE_VT100_ESCAPE.pattern + b")"
    )


class QueueReader:
    """Provides a file-like interface to reading from a queue."""

    def __init__(self, fd, timeout=None):
        """
        Parameters
        ----------
        fd : int
            A file descriptor
        timeout : float or None, optional
            The queue reading timeout.
        """
        self.fd = fd
        self.timeout = timeout
        self.closed = False
        self.queue = queue.Queue()
        self.thread = None

    def close(self):
        """close the reader"""
        self.closed = True

    def is_fully_read(self):
        """Returns whether or not the queue is fully read and the reader is
        closed.
        """
        return (
            self.closed
            and (self.thread is None or not self.thread.is_alive())
            and self.queue.empty()
        )

    def read_queue(self):
        """Reads a single chunk from the queue. This is blocking if
        the timeout is None and non-blocking otherwise.
        """
        try:
            return self.queue.get(block=True, timeout=self.timeout)
        except queue.Empty:
            return b""

    def read(self, size=-1):
        """Reads bytes from the file."""
        i = 0
        buf = b""
        while size < 0 or i != size:
            line = self.read_queue()
            if line:
                buf += line
            else:
                break
            i += len(line)
        return buf

    def readline(self, size=-1):
        """Reads a line, or a partial line from the file descriptor."""
        i = 0
        nl = b"\n"
        buf = b""
        while size < 0 or i != size:
            line = self.read_queue()
            if line:
                buf += line
                if line.endswith(nl):
                    break
            else:
                break
            i += len(line)
        return buf

    def _read_all_lines(self):
        """This reads all remaining lines in a blocking fashion."""
        lines = []
        while not self.is_fully_read():
            chunk = self.read_queue()
            lines.extend(chunk.splitlines(keepends=True))
        return lines

    def readlines(self, hint=-1):
        """Reads lines from the file descriptor. This is blocking for negative
        hints (i.e. read all the remaining lines) and non-blocking otherwise.
        """
        if hint == -1:
            return self._read_all_lines()
        lines = []
        while len(lines) != hint:
            chunk = self.read_queue()
            if not chunk:
                break
            lines.extend(chunk.splitlines(keepends=True))
        return lines

    def fileno(self):
        """Returns the file descriptor number."""
        return self.fd

    @staticmethod
    def readable():
        """Returns true, because this object is always readable."""
        return True

    def iterqueue(self):
        """Iterates through all remaining chunks in a blocking fashion."""
        while not self.is_fully_read():
            chunk = self.read_queue()
            if not chunk:
                continue
            yield chunk


def populate_fd_queue(reader, fd, queue):
    """Reads 1 kb of data from a file descriptor into a queue.
    If this ends or fails, it flags the calling reader object as closed.
    """
    while True:
        try:
            c = os.read(fd, 1024)
        except OSError:
            reader.closed = True
            break
        if c:
            queue.put(c)
        else:
            reader.closed = True
            break


class NonBlockingFDReader(QueueReader):
    """A class for reading characters from a file descriptor on a background
    thread. This has the advantages that the calling thread can close the
    file and that the reading does not block the calling thread.
    """

    def __init__(self, fd, timeout=None):
        """
        Parameters
        ----------
        fd : int
            A file descriptor
        timeout : float or None, optional
            The queue reading timeout.
        """
        super().__init__(fd, timeout=timeout)
        # start reading from stream
        self.thread = threading.Thread(
            target=populate_fd_queue, args=(self, self.fd, self.queue)
        )
        self.thread.daemon = True
        self.thread.start()


def populate_buffer(reader, fd, buffer, chunksize):
    """Reads bytes from the file descriptor and copies them into a buffer.

    The reads happen in parallel using the pread() syscall; which is only
    available on POSIX systems. If the read fails for any reason, the reader is
    flagged as closed.
    """
    offset = 0
    while True:
        try:
            buf = os.pread(fd, chunksize, offset)
        except OSError:
            reader.closed = True
            break
        if buf:
            buffer.write(buf)
            offset += len(buf)
        else:
            reader.closed = True
            break


class BufferedFDParallelReader:
    """Buffered, parallel background thread reader."""

    def __init__(self, fd, buffer=None, chunksize=1024):
        """
        Parameters
        ----------
        fd : int
            File descriptor from which to read.
        buffer : binary file-like or None, optional
            A buffer to write bytes into. If None, a new BytesIO object
            is created.
        chunksize : int, optional
            The max size of the parallel reads, default 1 kb.
        """
        self.fd = fd
        self.buffer = io.BytesIO() if buffer is None else buffer
        self.chunksize = chunksize
        self.closed = False
        # start reading from stream
        self.thread = threading.Thread(
            target=populate_buffer, args=(self, fd, self.buffer, chunksize)
        )
        self.thread.daemon = True

        self.thread.start()


def _expand_console_buffer(cols, max_offset, expandsize, orig_posize, fd):
    # if we are getting close to the end of the console buffer,
    # expand it so that we can read from it successfully.
    if cols == 0:
        return orig_posize[-1], max_offset, orig_posize
    rows = ((max_offset + expandsize) // cols) + 1
    winutils.set_console_screen_buffer_size(cols, rows, fd=fd)
    orig_posize = orig_posize[:3] + (rows,)
    max_offset = (rows - 1) * cols
    return rows, max_offset, orig_posize


def populate_console(reader, fd, buffer, chunksize, queue, expandsize=None):
    """Reads bytes from the file descriptor and puts lines into the queue.
    The reads happened in parallel,
    using xonsh.winutils.read_console_output_character(),
    and is thus only available on windows. If the read fails for any reason,
    the reader is flagged as closed.
    """
    # OK, so this function is super annoying because Windows stores its
    # buffers as a 2D regular, dense array -- without trailing newlines.
    # Meanwhile, we want to add *lines* to the queue. Also, as is typical
    # with parallel reads, the entire buffer that you ask for may not be
    # filled. Thus we have to deal with the full generality.
    #   1. reads may end in the middle of a line
    #   2. excess whitespace at the end of a line may not be real, unless
    #   3. you haven't read to the end of the line yet!
    # So there are alignment issues everywhere.  Also, Windows will automatically
    # read past the current cursor position, even though there is presumably
    # nothing to see there.
    #
    # These chunked reads basically need to happen like this because,
    #   a. The default buffer size is HUGE for the console (90k lines x 120 cols)
    #      as so we can't just read in everything at the end and see what we
    #      care about without a noticeable performance hit.
    #   b. Even with this huge size, it is still possible to write more lines than
    #      this, so we should scroll along with the console.
    # Unfortunately, because we do not have control over the terminal emulator,
    # It is not possible to compute how far back we should set the beginning
    # read position because we don't know how many characters have been popped
    # off the top of the buffer. If we did somehow know this number we could do
    # something like the following:
    #
    #    new_offset = (y*cols) + x
    #    if new_offset == max_offset:
    #        new_offset -= scrolled_offset
    #        x = new_offset%cols
    #        y = new_offset//cols
    #        continue
    #
    # So this method is imperfect and only works as long as the screen has
    # room to expand to.  Thus the trick here is to expand the screen size
    # when we get close enough to the end of the screen. There remain some
    # async issues related to not being able to set the cursor position.
    # but they just affect the alignment / capture of the output of the
    # first command run after a screen resize.
    if expandsize is None:
        expandsize = 100 * chunksize
    x, y, cols, rows = posize = winutils.get_position_size(fd)
    pre_x = pre_y = -1
    orig_posize = posize
    offset = (cols * y) + x
    max_offset = (rows - 1) * cols
    # I believe that there is a bug in PTK that if we reset the
    # cursor position, the cursor on the next prompt is accidentally on
    # the next line.  If this is fixed, uncomment the following line.
    # if max_offset < offset + expandsize:
    #     rows, max_offset, orig_posize = _expand_console_buffer(
    #                                        cols, max_offset, expandsize,
    #                                        orig_posize, fd)
    #     winutils.set_console_cursor_position(x, y, fd=fd)
    while True:
        posize = winutils.get_position_size(fd)
        offset = (cols * y) + x
        if ((posize[1], posize[0]) <= (y, x) and posize[2:] == (cols, rows)) or (
            pre_x == x and pre_y == y
        ):
            # already at or ahead of the current cursor position.
            if reader.closed:
                break
            else:
                time.sleep(reader.timeout)
                continue
        elif max_offset <= offset + expandsize:
            ecb = _expand_console_buffer(cols, max_offset, expandsize, orig_posize, fd)
            rows, max_offset, orig_posize = ecb
            continue
        elif posize[2:] == (cols, rows):
            # cursor updated but screen size is the same.
            pass
        else:
            # screen size changed, which is offset preserving
            orig_posize = posize
            cols, rows = posize[2:]
            x = offset % cols
            y = offset // cols
            pre_x = pre_y = -1
            max_offset = (rows - 1) * cols
            continue
        try:
            buf = winutils.read_console_output_character(
                x=x, y=y, fd=fd, buf=buffer, bufsize=chunksize, raw=True
            )
        except (OSError, IOError):
            reader.closed = True
            break
        # cursor position and offset
        if not reader.closed:
            buf = buf.rstrip()
        nread = len(buf)
        if nread == 0:
            time.sleep(reader.timeout)
            continue
        cur_x, cur_y = posize[0], posize[1]
        cur_offset = (cols * cur_y) + cur_x
        beg_offset = (cols * y) + x
        end_offset = beg_offset + nread
        if end_offset > cur_offset and cur_offset != max_offset:
            buf = buf[: cur_offset - end_offset]
        # convert to lines
        xshift = cols - x
        yshift = (nread // cols) + (1 if nread % cols > 0 else 0)
        lines = [buf[:xshift]]
        lines += [
            buf[l * cols + xshift : (l + 1) * cols + xshift] for l in range(yshift)
        ]
        lines = [line for line in lines if line]
        if not lines:
            time.sleep(reader.timeout)
            continue
        # put lines in the queue
        nl = b"\n"
        for line in lines[:-1]:
            queue.put(line.rstrip() + nl)
        if len(lines[-1]) == xshift:
            queue.put(lines[-1].rstrip() + nl)
        else:
            queue.put(lines[-1])
        # update x and y locations
        if (beg_offset + len(buf)) % cols == 0:
            new_offset = beg_offset + len(buf)
        else:
            new_offset = beg_offset + len(buf.rstrip())
        pre_x = x
        pre_y = y
        x = new_offset % cols
        y = new_offset // cols
        time.sleep(reader.timeout)


class ConsoleParallelReader(QueueReader):
    """Parallel reader for consoles that runs in a background thread.
    This is only needed, available, and useful on Windows.
    """

    def __init__(self, fd, buffer=None, chunksize=1024, timeout=None):
        """
        Parameters
        ----------
        fd : int
            Standard buffer file descriptor, 0 for stdin, 1 for stdout (default),
            and 2 for stderr.
        buffer : ctypes.c_wchar_p, optional
            An existing buffer to (re-)use.
        chunksize : int, optional
            The max size of the parallel reads, default 1 kb.
        timeout : float, optional
            The queue reading timeout.
        """
        timeout = timeout or builtins.__xonsh__.env.get("XONSH_PROC_FREQUENCY")
        super().__init__(fd, timeout=timeout)
        self._buffer = buffer  # this cannot be public
        if buffer is None:
            self._buffer = ctypes.c_char_p(b" " * chunksize)
        self.chunksize = chunksize
        # start reading from stream
        self.thread = threading.Thread(
            target=populate_console,
            args=(self, fd, self._buffer, chunksize, self.queue),
        )
        self.thread.daemon = True
        self.thread.start()


def safe_fdclose(handle, cache=None):
    """Closes a file handle in the safest way possible, and potentially
    storing the result.
    """
    if cache is not None and cache.get(handle, False):
        return
    status = True
    if handle is None:
        pass
    elif isinstance(handle, int):
        if handle >= 3:
            # don't close stdin, stdout, stderr, -1
            try:
                os.close(handle)
            except OSError:
                status = False
    elif handle is sys.stdin or handle is sys.stdout or handle is sys.stderr:
        # don't close stdin, stdout, or stderr
        pass
    else:
        try:
            handle.close()
        except OSError:
            status = False
    if cache is not None:
        cache[handle] = status


def safe_flush(handle):
    """Attempts to safely flush a file handle, returns success bool."""
    status = True
    try:
        handle.flush()
    except OSError:
        status = False
    return status


def still_writable(fd):
    """Determines whether a file descriptor is still writable by trying to
    write an empty string and seeing if it fails.
    """
    try:
        os.write(fd, b"")
        status = True
    except OSError:
        status = False
    return status


class PopenThread(threading.Thread):
    """A thread for running and managing subprocess. This allows reading
    from the stdin, stdout, and stderr streams in a non-blocking fashion.

    This takes the same arguments and keyword arguments as regular Popen.
    This requires that the captured_stdout and captured_stderr attributes
    to be set following instantiation.
    """

    def __init__(self, *args, stdin=None, stdout=None, stderr=None, **kwargs):
        super().__init__()
        self.lock = threading.RLock()
        env = builtins.__xonsh__.env
        # stdin setup
        self.orig_stdin = stdin
        if stdin is None:
            self.stdin_fd = 0
        elif isinstance(stdin, int):
            self.stdin_fd = stdin
        else:
            self.stdin_fd = stdin.fileno()
        self.store_stdin = env.get("XONSH_STORE_STDIN")
        self.timeout = env.get("XONSH_PROC_FREQUENCY")
        self.in_alt_mode = False
        self.stdin_mode = None
        # stdout setup
        self.orig_stdout = stdout
        self.stdout_fd = 1 if stdout is None else stdout.fileno()
        self._set_pty_size()
        # stderr setup
        self.orig_stderr = stderr
        # Set some signal handles, if we can. Must come before process
        # is started to prevent deadlock on windows
        self.proc = None  # has to be here for closure for handles
        self.old_int_handler = self.old_winch_handler = None
        self.old_tstp_handler = self.old_quit_handler = None
        if on_main_thread():
            self.old_int_handler = signal.signal(signal.SIGINT, self._signal_int)
            if ON_POSIX:
                self.old_tstp_handler = signal.signal(signal.SIGTSTP, self._signal_tstp)
                self.old_quit_handler = signal.signal(signal.SIGQUIT, self._signal_quit)
            if CAN_RESIZE_WINDOW:
                self.old_winch_handler = signal.signal(
                    signal.SIGWINCH, self._signal_winch
                )
        # start up process
        if ON_WINDOWS and stdout is not None:
            os.set_inheritable(stdout.fileno(), False)

        try:
            self.proc = proc = subprocess.Popen(
                *args, stdin=stdin, stdout=stdout, stderr=stderr, **kwargs
            )
        except Exception:
            self._clean_up()
            raise

        self.pid = proc.pid
        self.universal_newlines = uninew = proc.universal_newlines
        if uninew:
            self.encoding = enc = env.get("XONSH_ENCODING")
            self.encoding_errors = err = env.get("XONSH_ENCODING_ERRORS")
            self.stdin = io.BytesIO()  # stdin is always bytes!
            self.stdout = io.TextIOWrapper(io.BytesIO(), encoding=enc, errors=err)
            self.stderr = io.TextIOWrapper(io.BytesIO(), encoding=enc, errors=err)
        else:
            self.encoding = self.encoding_errors = None
            self.stdin = io.BytesIO()
            self.stdout = io.BytesIO()
            self.stderr = io.BytesIO()
        self.suspended = False
        self.prevs_are_closed = False
        self.start()

    def run(self):
        """Runs the subprocess by performing a parallel read on stdin if allowed,
        and copying bytes from captured_stdout to stdout and bytes from
        captured_stderr to stderr.
        """
        proc = self.proc
        spec = self._wait_and_getattr("spec")
        # get stdin and apply parallel reader if needed.
        stdin = self.stdin
        if self.orig_stdin is None:
            origin = None
        elif ON_POSIX and self.store_stdin:
            origin = self.orig_stdin
            origfd = origin if isinstance(origin, int) else origin.fileno()
            origin = BufferedFDParallelReader(origfd, buffer=stdin)
        else:
            origin = None
        # get non-blocking stdout
        stdout = self.stdout.buffer if self.universal_newlines else self.stdout
        capout = spec.captured_stdout
        if capout is None:
            procout = None
        else:
            procout = NonBlockingFDReader(capout.fileno(), timeout=self.timeout)
        # get non-blocking stderr
        stderr = self.stderr.buffer if self.universal_newlines else self.stderr
        caperr = spec.captured_stderr
        if caperr is None:
            procerr = None
        else:
            procerr = NonBlockingFDReader(caperr.fileno(), timeout=self.timeout)
        # initial read from buffer
        self._read_write(procout, stdout, sys.__stdout__)
        self._read_write(procerr, stderr, sys.__stderr__)
        # loop over reads while process is running.
        i = j = cnt = 1
        while proc.poll() is None:
            # this is here for CPU performance reasons.
            if i + j == 0:
                cnt = min(cnt + 1, 1000)
                tout = self.timeout * cnt
                if procout is not None:
                    procout.timeout = tout
                if procerr is not None:
                    procerr.timeout = tout
            elif cnt == 1:
                pass
            else:
                cnt = 1
                if procout is not None:
                    procout.timeout = self.timeout
                if procerr is not None:
                    procerr.timeout = self.timeout
            # redirect some output!
            i = self._read_write(procout, stdout, sys.__stdout__)
            j = self._read_write(procerr, stderr, sys.__stderr__)
            if self.suspended:
                break
        if self.suspended:
            return
        # close files to send EOF to non-blocking reader.
        # capout & caperr seem to be needed only by Windows, while
        # orig_stdout & orig_stderr are need by posix and Windows.
        # Also, order seems to matter here,
        # with orig_* needed to be closed before cap*
        safe_fdclose(self.orig_stdout)
        safe_fdclose(self.orig_stderr)
        if ON_WINDOWS:
            safe_fdclose(capout)
            safe_fdclose(caperr)
        # read in the remaining data in a blocking fashion.
        while (procout is not None and not procout.is_fully_read()) or (
            procerr is not None and not procerr.is_fully_read()
        ):
            self._read_write(procout, stdout, sys.__stdout__)
            self._read_write(procerr, stderr, sys.__stderr__)
        # kill the process if it is still alive. Happens when piping.
        if proc.poll() is None:
            proc.terminate()

    def _wait_and_getattr(self, name):
        """make sure the instance has a certain attr, and return it."""
        while not hasattr(self, name):
            time.sleep(1e-7)
        return getattr(self, name)

    def _read_write(self, reader, writer, stdbuf):
        """Reads a chunk of bytes from a buffer and write into memory or back
        down to the standard buffer, as appropriate. Returns the number of
        successful reads.
        """
        if reader is None:
            return 0
        i = -1
        for i, chunk in enumerate(iter(reader.read_queue, b"")):
            self._alt_mode_switch(chunk, writer, stdbuf)
        if i >= 0:
            writer.flush()
            stdbuf.flush()
        return i + 1

    def _alt_mode_switch(self, chunk, membuf, stdbuf):
        """Enables recursively switching between normal capturing mode
        and 'alt' mode, which passes through values to the standard
        buffer. Pagers, text editors, curses applications, etc. use
        alternate mode.
        """
        i, flag = findfirst(chunk, ALTERNATE_MODE_FLAGS)
        if flag is None:
            self._alt_mode_writer(chunk, membuf, stdbuf)
        else:
            # This code is executed when the child process switches the
            # terminal into or out of alternate mode. The line below assumes
            # that the user has opened vim, less, or similar, and writes writes
            # to stdin.
            j = i + len(flag)
            # write the first part of the chunk in the current mode.
            self._alt_mode_writer(chunk[:i], membuf, stdbuf)
            # switch modes
            # write the flag itself the current mode where alt mode is on
            # so that it is streamed to the terminal ASAP.
            # this is needed for terminal emulators to find the correct
            # positions before and after alt mode.
            alt_mode = flag in START_ALTERNATE_MODE
            if alt_mode:
                self.in_alt_mode = alt_mode
                self._alt_mode_writer(flag, membuf, stdbuf)
                self._enable_cbreak_stdin()
            else:
                self._alt_mode_writer(flag, membuf, stdbuf)
                self.in_alt_mode = alt_mode
                self._disable_cbreak_stdin()
            # recurse this function, but without the current flag.
            self._alt_mode_switch(chunk[j:], membuf, stdbuf)

    def _alt_mode_writer(self, chunk, membuf, stdbuf):
        """Write bytes to the standard buffer if in alt mode or otherwise
        to the in-memory buffer.
        """
        if not chunk:
            pass  # don't write empty values
        elif self.in_alt_mode:
            stdbuf.buffer.write(chunk)
        else:
            with self.lock:
                p = membuf.tell()
                membuf.seek(0, io.SEEK_END)
                membuf.write(chunk)
                membuf.seek(p)

    #
    # Window resize handlers
    #

    def _signal_winch(self, signum, frame):
        """Signal handler for SIGWINCH - window size has changed."""
        self.send_signal(signal.SIGWINCH)
        self._set_pty_size()

    def _set_pty_size(self):
        """Sets the window size of the child pty based on the window size of
        our own controlling terminal.
        """
        if ON_WINDOWS or not os.isatty(self.stdout_fd):
            return
        # Get the terminal size of the real terminal, set it on the
        #       pseudoterminal.
        buf = array.array("h", [0, 0, 0, 0])
        # 1 = stdout here
        try:
            fcntl.ioctl(1, termios.TIOCGWINSZ, buf, True)
            fcntl.ioctl(self.stdout_fd, termios.TIOCSWINSZ, buf)
        except OSError:
            pass

    #
    # SIGINT handler
    #

    def _signal_int(self, signum, frame):
        """Signal handler for SIGINT - Ctrl+C may have been pressed."""
        self.send_signal(signum)
        if self.proc is not None and self.proc.poll() is not None:
            self._restore_sigint(frame=frame)
        if on_main_thread():
            signal.pthread_kill(threading.get_ident(), signal.SIGINT)

    def _restore_sigint(self, frame=None):
        old = self.old_int_handler
        if old is not None:
            if on_main_thread():
                signal.signal(signal.SIGINT, old)
            self.old_int_handler = None
        if frame is not None:
            self._disable_cbreak_stdin()
            if old is not None and old is not self._signal_int:
                old(signal.SIGINT, frame)

    #
    # SIGTSTP handler
    #

    def _signal_tstp(self, signum, frame):
        """Signal handler for suspending SIGTSTP - Ctrl+Z may have been pressed.
        """
        self.suspended = True
        self.send_signal(signum)
        self._restore_sigtstp(frame=frame)

    def _restore_sigtstp(self, frame=None):
        old = self.old_tstp_handler
        if old is not None:
            if on_main_thread():
                signal.signal(signal.SIGTSTP, old)
            self.old_tstp_handler = None
        if frame is not None:
            self._disable_cbreak_stdin()

    #
    # SIGQUIT handler
    #

    def _signal_quit(self, signum, frame):
        r"""Signal handler for quiting SIGQUIT - Ctrl+\ may have been pressed.
        """
        self.send_signal(signum)
        self._restore_sigquit(frame=frame)

    def _restore_sigquit(self, frame=None):
        old = self.old_quit_handler
        if old is not None:
            if on_main_thread():
                signal.signal(signal.SIGQUIT, old)
            self.old_quit_handler = None
        if frame is not None:
            self._disable_cbreak_stdin()

    #
    # cbreak mode handlers
    #

    def _enable_cbreak_stdin(self):
        if not ON_POSIX:
            return
        try:
            self.stdin_mode = termios.tcgetattr(self.stdin_fd)[:]
        except termios.error:
            # this can happen for cases where another process is controlling
            # xonsh's tty device, such as in testing.
            self.stdin_mode = None
            return
        new = self.stdin_mode[:]
        new[LFLAG] &= ~(termios.ECHO | termios.ICANON)
        new[CC][termios.VMIN] = 1
        new[CC][termios.VTIME] = 0
        try:
            # termios.TCSAFLUSH may be less reliable than termios.TCSANOW
            termios.tcsetattr(self.stdin_fd, termios.TCSANOW, new)
        except termios.error:
            self._disable_cbreak_stdin()

    def _disable_cbreak_stdin(self):
        if not ON_POSIX or self.stdin_mode is None:
            return
        new = self.stdin_mode[:]
        new[LFLAG] |= termios.ECHO | termios.ICANON
        new[CC][termios.VMIN] = 1
        new[CC][termios.VTIME] = 0
        try:
            termios.tcsetattr(self.stdin_fd, termios.TCSANOW, new)
        except termios.error:
            pass

    #
    # Dispatch methods
    #

    def poll(self):
        """Dispatches to Popen.returncode."""
        return self.proc.returncode

    def wait(self, timeout=None):
        """Dispatches to Popen.wait(), but also does process cleanup such as
        joining this thread and replacing the original window size signal
        handler.
        """
        self._disable_cbreak_stdin()
        rtn = self.proc.wait(timeout=timeout)
        self.join()
        # need to replace the old signal handlers somewhere...
        if self.old_winch_handler is not None and on_main_thread():
            signal.signal(signal.SIGWINCH, self.old_winch_handler)
            self.old_winch_handler = None
        self._clean_up()
        return rtn

    def _clean_up(self):
        self._restore_sigint()
        self._restore_sigtstp()
        self._restore_sigquit()

    @property
    def returncode(self):
        """Process return code."""
        return self.proc.returncode

    @returncode.setter
    def returncode(self, value):
        """Process return code."""
        self.proc.returncode = value

    @property
    def signal(self):
        """Process signal, or None."""
        s = getattr(self.proc, "signal", None)
        if s is None:
            rtn = self.returncode
            if rtn is not None and rtn != 0:
                s = (-1 * rtn, rtn < 0 if ON_WINDOWS else os.WCOREDUMP(rtn))
        return s

    @signal.setter
    def signal(self, value):
        """Process signal, or None."""
        self.proc.signal = value

    def send_signal(self, signal):
        """Dispatches to Popen.send_signal()."""
        dt = 0.0
        while self.proc is None and dt < self.timeout:
            time.sleep(1e-7)
            dt += 1e-7
        if self.proc is None:
            return
        try:
            rtn = self.proc.send_signal(signal)
        except ProcessLookupError:
            # This can happen in the case of !(cmd) when the command has ended
            rtn = None
        return rtn

    def terminate(self):
        """Dispatches to Popen.terminate()."""
        return self.proc.terminate()

    def kill(self):
        """Dispatches to Popen.kill()."""
        return self.proc.kill()


class Handle(int):
    closed = False

    def Close(self, CloseHandle=None):
        CloseHandle = CloseHandle or _winapi.CloseHandle
        if not self.closed:
            self.closed = True
            CloseHandle(self)

    def Detach(self):
        if not self.closed:
            self.closed = True
            return int(self)
        raise ValueError("already closed")

    def __repr__(self):
        return "Handle(%d)" % int(self)

    __del__ = Close
    __str__ = __repr__


class FileThreadDispatcher:
    """Dispatches to different file handles depending on the
    current thread. Useful if you want file operation to go to different
    places for different threads.
    """

    def __init__(self, default=None):
        """
        Parameters
        ----------
        default : file-like or None, optional
            The file handle to write to if a thread cannot be found in
            the registry. If None, a new in-memory instance.

        Attributes
        ----------
        registry : dict
            Maps thread idents to file handles.
        """
        if default is None:
            default = io.TextIOWrapper(io.BytesIO())
        self.default = default
        self.registry = {}

    def register(self, handle):
        """Registers a file handle for the current thread. Returns self so
        that this method can be used in a with-statement.
        """
        if handle is self:
            # prevent weird recurssion errors
            return self
        self.registry[threading.get_ident()] = handle
        return self

    def deregister(self):
        """Removes the current thread from the registry."""
        ident = threading.get_ident()
        if ident in self.registry:
            # don't remove if we have already been deregistered
            del self.registry[threading.get_ident()]

    @property
    def available(self):
        """True if the thread is available in the registry."""
        return threading.get_ident() in self.registry

    @property
    def handle(self):
        """Gets the current handle for the thread."""
        return self.registry.get(threading.get_ident(), self.default)

    def __enter__(self):
        pass

    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.deregister()

    #
    # io.TextIOBase interface
    #

    @property
    def encoding(self):
        """Gets the encoding for this thread's handle."""
        return self.handle.encoding

    @property
    def errors(self):
        """Gets the errors for this thread's handle."""
        return self.handle.errors

    @property
    def newlines(self):
        """Gets the newlines for this thread's handle."""
        return self.handle.newlines

    @property
    def buffer(self):
        """Gets the buffer for this thread's handle."""
        return self.handle.buffer

    def detach(self):
        """Detaches the buffer for the current thread."""
        return self.handle.detach()

    def read(self, size=None):
        """Reads from the handle for the current thread."""
        return self.handle.read(size)

    def readline(self, size=-1):
        """Reads a line from the handle for the current thread."""
        return self.handle.readline(size)

    def readlines(self, hint=-1):
        """Reads lines from the handle for the current thread."""
        return self.handle.readlines(hint)

    def seek(self, offset, whence=io.SEEK_SET):
        """Seeks the current file."""
        return self.handle.seek(offset, whence)

    def tell(self):
        """Reports the current position in the handle for the current thread."""
        return self.handle.tell()

    def write(self, s):
        """Writes to this thread's handle. This also flushes, just to be
        extra sure the string was written.
        """
        h = self.handle
        try:
            r = h.write(s)
            h.flush()
        except OSError:
            r = None
        return r

    @property
    def line_buffering(self):
        """Gets if line buffering for this thread's handle enabled."""
        return self.handle.line_buffering

    #
    # io.IOBase interface
    #

    def close(self):
        """Closes the current thread's handle."""
        return self.handle.close()

    @property
    def closed(self):
        """Is the thread's handle closed."""
        return self.handle.closed

    def fileno(self):
        """Returns the file descriptor for the current thread."""
        return self.handle.fileno()

    def flush(self):
        """Flushes the file descriptor for the current thread."""
        return safe_flush(self.handle)

    def isatty(self):
        """Returns if the file descriptor for the current thread is a tty."""
        return self.handle.isatty()

    def readable(self):
        """Returns if file descriptor for the current thread is readable."""
        return self.handle.readable()

    def seekable(self):
        """Returns if file descriptor for the current thread is seekable."""
        return self.handle.seekable()

    def truncate(self, size=None):
        """Truncates the file for for the current thread."""
        return self.handle.truncate()

    def writable(self, size=None):
        """Returns if file descriptor for the current thread is writable."""
        return self.handle.writable(size)

    def writelines(self):
        """Writes lines for the file descriptor for the current thread."""
        return self.handle.writelines()


# These should NOT be lazy since they *need* to get the true stdout from the
# main thread. Also their creation time should be negligible.
STDOUT_DISPATCHER = FileThreadDispatcher(default=sys.stdout)
STDERR_DISPATCHER = FileThreadDispatcher(default=sys.stderr)


def parse_proxy_return(r, stdout, stderr):
    """Proxies may return a variety of outputs. This handles them generally.

    Parameters
    ----------
    r : tuple, str, int, or None
        Return from proxy function
    stdout : file-like
        Current stdout stream
    stdout : file-like
        Current stderr stream

    Returns
    -------
    cmd_result : int
        The return code of the proxy
    """
    cmd_result = 0
    if isinstance(r, str):
        stdout.write(r)
        stdout.flush()
    elif isinstance(r, int):
        cmd_result = r
    elif isinstance(r, cabc.Sequence):
        rlen = len(r)
        if rlen > 0 and r[0] is not None:
            stdout.write(r[0])
            stdout.flush()
        if rlen > 1 and r[1] is not None:
            stderr.write(r[1])
            stderr.flush()
        if rlen > 2 and r[2] is not None:
            cmd_result = r[2]
    elif r is not None:
        # for the random object...
        stdout.write(str(r))
        stdout.flush()
    return cmd_result


def proxy_zero(f, args, stdin, stdout, stderr, spec, stack):
    """Calls a proxy function which takes no parameters."""
    return f()


def proxy_one(f, args, stdin, stdout, stderr, spec, stack):
    """Calls a proxy function which takes one parameter: args"""
    return f(args)


def proxy_two(f, args, stdin, stdout, stderr, spec, stack):
    """Calls a proxy function which takes two parameter: args and stdin."""
    return f(args, stdin)


def proxy_three(f, args, stdin, stdout, stderr, spec, stack):
    """Calls a proxy function which takes three parameter: args, stdin, stdout.
    """
    return f(args, stdin, stdout)


def proxy_four(f, args, stdin, stdout, stderr, spec, stack):
    """Calls a proxy function which takes four parameter: args, stdin, stdout,
    and stderr.
    """
    return f(args, stdin, stdout, stderr)


def proxy_five(f, args, stdin, stdout, stderr, spec, stack):
    """Calls a proxy function which takes four parameter: args, stdin, stdout,
    stderr, and spec.
    """
    return f(args, stdin, stdout, stderr, spec)


PROXIES = (proxy_zero, proxy_one, proxy_two, proxy_three, proxy_four, proxy_five)
PROXY_KWARG_NAMES = frozenset(["args", "stdin", "stdout", "stderr", "spec", "stack"])


def partial_proxy(f):
    """Dispatches the appropriate proxy function based on the number of args."""
    numargs = 0
    for name, param in inspect.signature(f).parameters.items():
        if (
            param.kind == param.POSITIONAL_ONLY
            or param.kind == param.POSITIONAL_OR_KEYWORD
        ):
            numargs += 1
        elif name in PROXY_KWARG_NAMES and param.kind == param.KEYWORD_ONLY:
            numargs += 1
    if numargs < 6:
        return functools.partial(PROXIES[numargs], f)
    elif numargs == 6:
        # don't need to partial.
        return f
    else:
        e = "Expected proxy with 6 or fewer arguments for {}, not {}"
        raise XonshError(e.format(", ".join(PROXY_KWARG_NAMES), numargs))


class ProcProxyThread(threading.Thread):
    """
    Class representing a function to be run as a subprocess-mode command.
    """

    def __init__(
        self,
        f,
        args,
        stdin=None,
        stdout=None,
        stderr=None,
        universal_newlines=False,
        env=None,
    ):
        """Parameters
        ----------
        f : function
            The function to be executed.
        args : list
            A (possibly empty) list containing the arguments that were given on
            the command line
        stdin : file-like, optional
            A file-like object representing stdin (input can be read from
            here).  If `stdin` is not provided or if it is explicitly set to
            `None`, then an instance of `io.StringIO` representing an empty
            file is used.
        stdout : file-like, optional
            A file-like object representing stdout (normal output can be
            written here).  If `stdout` is not provided or if it is explicitly
            set to `None`, then `sys.stdout` is used.
        stderr : file-like, optional
            A file-like object representing stderr (error output can be
            written here).  If `stderr` is not provided or if it is explicitly
            set to `None`, then `sys.stderr` is used.
        universal_newlines : bool, optional
            Whether or not to use universal newlines.
        env : Mapping, optional
            Environment mapping.
        """
        self.orig_f = f
        self.f = partial_proxy(f)
        self.args = args
        self.pid = None
        self.returncode = None
        self._closed_handle_cache = {}

        handles = self._get_handles(stdin, stdout, stderr)
        (
            self.p2cread,
            self.p2cwrite,
            self.c2pread,
            self.c2pwrite,
            self.errread,
            self.errwrite,
        ) = handles

        # default values
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.env = env or builtins.__xonsh__.env
        self._interrupted = False

        if ON_WINDOWS:
            if self.p2cwrite != -1:
                self.p2cwrite = msvcrt.open_osfhandle(self.p2cwrite.Detach(), 0)
            if self.c2pread != -1:
                self.c2pread = msvcrt.open_osfhandle(self.c2pread.Detach(), 0)
            if self.errread != -1:
                self.errread = msvcrt.open_osfhandle(self.errread.Detach(), 0)

        if self.p2cwrite != -1:
            self.stdin = io.open(self.p2cwrite, "wb", -1)
            if universal_newlines:
                self.stdin = io.TextIOWrapper(
                    self.stdin, write_through=True, line_buffering=False
                )
        elif isinstance(stdin, int) and stdin != 0:
            self.stdin = io.open(stdin, "wb", -1)

        if self.c2pread != -1:
            self.stdout = io.open(self.c2pread, "rb", -1)
            if universal_newlines:
                self.stdout = io.TextIOWrapper(self.stdout)

        if self.errread != -1:
            self.stderr = io.open(self.errread, "rb", -1)
            if universal_newlines:
                self.stderr = io.TextIOWrapper(self.stderr)

        # Set some signal handles, if we can. Must come before process
        # is started to prevent deadlock on windows
        self.old_int_handler = None
        if on_main_thread():
            self.old_int_handler = signal.signal(signal.SIGINT, self._signal_int)
        # start up the proc
        super().__init__()
        self.start()

    def __del__(self):
        self._restore_sigint()

    def run(self):
        """Set up input/output streams and execute the child function in a new
        thread.  This is part of the `threading.Thread` interface and should
        not be called directly.
        """
        if self.f is None:
            return
        spec = self._wait_and_getattr("spec")
        last_in_pipeline = spec.last_in_pipeline
        if last_in_pipeline:
            capout = spec.captured_stdout  # NOQA
            caperr = spec.captured_stderr  # NOQA
        env = builtins.__xonsh__.env
        enc = env.get("XONSH_ENCODING")
        err = env.get("XONSH_ENCODING_ERRORS")
        if ON_WINDOWS:
            if self.p2cread != -1:
                self.p2cread = msvcrt.open_osfhandle(self.p2cread.Detach(), 0)
            if self.c2pwrite != -1:
                self.c2pwrite = msvcrt.open_osfhandle(self.c2pwrite.Detach(), 0)
            if self.errwrite != -1:
                self.errwrite = msvcrt.open_osfhandle(self.errwrite.Detach(), 0)
        # get stdin
        if self.stdin is None:
            sp_stdin = None
        elif self.p2cread != -1:
            sp_stdin = io.TextIOWrapper(
                io.open(self.p2cread, "rb", -1), encoding=enc, errors=err
            )
        else:
            sp_stdin = sys.stdin
        # stdout
        if self.c2pwrite != -1:
            sp_stdout = io.TextIOWrapper(
                io.open(self.c2pwrite, "wb", -1), encoding=enc, errors=err
            )
        else:
            sp_stdout = sys.stdout
        # stderr
        if self.errwrite == self.c2pwrite:
            sp_stderr = sp_stdout
        elif self.errwrite != -1:
            sp_stderr = io.TextIOWrapper(
                io.open(self.errwrite, "wb", -1), encoding=enc, errors=err
            )
        else:
            sp_stderr = sys.stderr
        # run the function itself
        try:
            with STDOUT_DISPATCHER.register(sp_stdout), STDERR_DISPATCHER.register(
                sp_stderr
            ), redirect_stdout(STDOUT_DISPATCHER), redirect_stderr(STDERR_DISPATCHER):
                r = self.f(self.args, sp_stdin, sp_stdout, sp_stderr, spec, spec.stack)
        except SystemExit as e:
            r = e.code if isinstance(e.code, int) else int(bool(e.code))
        except OSError:
            status = still_writable(self.c2pwrite) and still_writable(self.errwrite)
            if status:
                # stdout and stderr are still writable, so error must
                # come from function itself.
                print_exception()
                r = 1
            else:
                # stdout and stderr are no longer writable, so error must
                # come from the fact that the next process in the pipeline
                # has closed the other side of the pipe. The function then
                # attempted to write to this side of the pipe anyway. This
                # is not truly an error and we should exit gracefully.
                r = 0
        except Exception:
            print_exception()
            r = 1
        safe_flush(sp_stdout)
        safe_flush(sp_stderr)
        self.returncode = parse_proxy_return(r, sp_stdout, sp_stderr)
        if not last_in_pipeline and not ON_WINDOWS:
            # mac requires us *not to* close the handles here while
            # windows requires us *to* close the handles here
            return
        # clean up
        # scopz: not sure why this is needed, but stdin cannot go here
        # and stdout & stderr must.
        handles = [self.stdout, self.stderr]
        for handle in handles:
            safe_fdclose(handle, cache=self._closed_handle_cache)

    def _wait_and_getattr(self, name):
        """make sure the instance has a certain attr, and return it."""
        while not hasattr(self, name):
            time.sleep(1e-7)
        return getattr(self, name)

    def poll(self):
        """Check if the function has completed.

        Returns
        -------
        None if the function is still executing, and the returncode otherwise
        """
        return self.returncode

    def wait(self, timeout=None):
        """Waits for the process to finish and returns the return code."""
        self.join()
        self._restore_sigint()
        return self.returncode

    #
    # SIGINT handler
    #

    def _signal_int(self, signum, frame):
        """Signal handler for SIGINT - Ctrl+C may have been pressed."""
        # Check if we have already been interrupted. This should prevent
        # the possibility of infinite recursion.
        if self._interrupted:
            return
        self._interrupted = True
        # close file handles here to stop an processes piped to us.
        handles = (
            self.p2cread,
            self.p2cwrite,
            self.c2pread,
            self.c2pwrite,
            self.errread,
            self.errwrite,
        )
        for handle in handles:
            safe_fdclose(handle)
        if self.poll() is not None:
            self._restore_sigint(frame=frame)
        if on_main_thread():
            signal.pthread_kill(threading.get_ident(), signal.SIGINT)

    def _restore_sigint(self, frame=None):
        old = self.old_int_handler
        if old is not None:
            if on_main_thread():
                signal.signal(signal.SIGINT, old)
            self.old_int_handler = None
        if frame is not None:
            if old is not None and old is not self._signal_int:
                old(signal.SIGINT, frame)
        if self._interrupted:
            self.returncode = 1

    # The code below (_get_devnull, _get_handles, and _make_inheritable) comes
    # from subprocess.py in the Python 3.4.2 Standard Library
    def _get_devnull(self):
        if not hasattr(self, "_devnull"):
            self._devnull = os.open(os.devnull, os.O_RDWR)
        return self._devnull

    if ON_WINDOWS:

        def _make_inheritable(self, handle):
            """Return a duplicate of handle, which is inheritable"""
            h = _winapi.DuplicateHandle(
                _winapi.GetCurrentProcess(),
                handle,
                _winapi.GetCurrentProcess(),
                0,
                1,
                _winapi.DUPLICATE_SAME_ACCESS,
            )
            return Handle(h)

        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tuple with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            if stdin is None and stdout is None and stderr is None:
                return (-1, -1, -1, -1, -1, -1)

            p2cread, p2cwrite = -1, -1
            c2pread, c2pwrite = -1, -1
            errread, errwrite = -1, -1

            if stdin is None:
                p2cread = _winapi.GetStdHandle(_winapi.STD_INPUT_HANDLE)
                if p2cread is None:
                    p2cread, _ = _winapi.CreatePipe(None, 0)
                    p2cread = Handle(p2cread)
                    _winapi.CloseHandle(_)
            elif stdin == subprocess.PIPE:
                p2cread, p2cwrite = Handle(p2cread), Handle(p2cwrite)
            elif stdin == subprocess.DEVNULL:
                p2cread = msvcrt.get_osfhandle(self._get_devnull())
            elif isinstance(stdin, int):
                p2cread = msvcrt.get_osfhandle(stdin)
            else:
                # Assuming file-like object
                p2cread = msvcrt.get_osfhandle(stdin.fileno())
            p2cread = self._make_inheritable(p2cread)

            if stdout is None:
                c2pwrite = _winapi.GetStdHandle(_winapi.STD_OUTPUT_HANDLE)
                if c2pwrite is None:
                    _, c2pwrite = _winapi.CreatePipe(None, 0)
                    c2pwrite = Handle(c2pwrite)
                    _winapi.CloseHandle(_)
            elif stdout == subprocess.PIPE:
                c2pread, c2pwrite = _winapi.CreatePipe(None, 0)
                c2pread, c2pwrite = Handle(c2pread), Handle(c2pwrite)
            elif stdout == subprocess.DEVNULL:
                c2pwrite = msvcrt.get_osfhandle(self._get_devnull())
            elif isinstance(stdout, int):
                c2pwrite = msvcrt.get_osfhandle(stdout)
            else:
                # Assuming file-like object
                c2pwrite = msvcrt.get_osfhandle(stdout.fileno())
            c2pwrite = self._make_inheritable(c2pwrite)

            if stderr is None:
                errwrite = _winapi.GetStdHandle(_winapi.STD_ERROR_HANDLE)
                if errwrite is None:
                    _, errwrite = _winapi.CreatePipe(None, 0)
                    errwrite = Handle(errwrite)
                    _winapi.CloseHandle(_)
            elif stderr == subprocess.PIPE:
                errread, errwrite = _winapi.CreatePipe(None, 0)
                errread, errwrite = Handle(errread), Handle(errwrite)
            elif stderr == subprocess.STDOUT:
                errwrite = c2pwrite
            elif stderr == subprocess.DEVNULL:
                errwrite = msvcrt.get_osfhandle(self._get_devnull())
            elif isinstance(stderr, int):
                errwrite = msvcrt.get_osfhandle(stderr)
            else:
                # Assuming file-like object
                errwrite = msvcrt.get_osfhandle(stderr.fileno())
            errwrite = self._make_inheritable(errwrite)

            return (p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)

    else:
        # POSIX versions
        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tuple with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            p2cread, p2cwrite = -1, -1
            c2pread, c2pwrite = -1, -1
            errread, errwrite = -1, -1

            if stdin is None:
                pass
            elif stdin == subprocess.PIPE:
                p2cread, p2cwrite = os.pipe()
            elif stdin == subprocess.DEVNULL:
                p2cread = self._get_devnull()
            elif isinstance(stdin, int):
                p2cread = stdin
            else:
                # Assuming file-like object
                p2cread = stdin.fileno()

            if stdout is None:
                pass
            elif stdout == subprocess.PIPE:
                c2pread, c2pwrite = os.pipe()
            elif stdout == subprocess.DEVNULL:
                c2pwrite = self._get_devnull()
            elif isinstance(stdout, int):
                c2pwrite = stdout
            else:
                # Assuming file-like object
                c2pwrite = stdout.fileno()

            if stderr is None:
                pass
            elif stderr == subprocess.PIPE:
                errread, errwrite = os.pipe()
            elif stderr == subprocess.STDOUT:
                errwrite = c2pwrite
            elif stderr == subprocess.DEVNULL:
                errwrite = self._get_devnull()
            elif isinstance(stderr, int):
                errwrite = stderr
            else:
                # Assuming file-like object
                errwrite = stderr.fileno()

            return (p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)


#
# Foreground Thread Process Proxies
#


class ProcProxy(object):
    """This is process proxy class that runs its alias functions on the
    same thread that it was called from, which is typically the main thread.
    This prevents the process from running on a background thread, but enables
    debugger and profiler tools (functions) be run on the same thread that they
    are attempting to debug.
    """

    def __init__(
        self,
        f,
        args,
        stdin=None,
        stdout=None,
        stderr=None,
        universal_newlines=False,
        env=None,
    ):
        self.orig_f = f
        self.f = partial_proxy(f)
        self.args = args
        self.pid = os.getpid()
        self.returncode = None
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.universal_newlines = universal_newlines
        self.env = env

    def poll(self):
        """Check if the function has completed via the returncode or None.
        """
        return self.returncode

    def wait(self, timeout=None):
        """Runs the function and returns the result. Timeout argument only
        present for API compatibility.
        """
        if self.f is None:
            return 0
        env = builtins.__xonsh__.env
        enc = env.get("XONSH_ENCODING")
        err = env.get("XONSH_ENCODING_ERRORS")
        spec = self._wait_and_getattr("spec")
        # set file handles
        if self.stdin is None:
            stdin = None
        else:
            if isinstance(self.stdin, int):
                inbuf = io.open(self.stdin, "rb", -1)
            else:
                inbuf = self.stdin
            stdin = io.TextIOWrapper(inbuf, encoding=enc, errors=err)
        stdout = self._pick_buf(self.stdout, sys.stdout, enc, err)
        stderr = self._pick_buf(self.stderr, sys.stderr, enc, err)
        # run the actual function
        try:
            r = self.f(self.args, stdin, stdout, stderr, spec, spec.stack)
        except Exception:
            print_exception()
            r = 1
        self.returncode = parse_proxy_return(r, stdout, stderr)
        safe_flush(stdout)
        safe_flush(stderr)
        return self.returncode

    @staticmethod
    def _pick_buf(handle, sysbuf, enc, err):
        if handle is None or handle is sysbuf:
            buf = sysbuf
        elif isinstance(handle, int):
            if handle < 3:
                buf = sysbuf
            else:
                buf = io.TextIOWrapper(
                    io.open(handle, "wb", -1), encoding=enc, errors=err
                )
        elif hasattr(handle, "encoding"):
            # must be a text stream, no need to wrap.
            buf = handle
        else:
            # must be a binary stream, should wrap it.
            buf = io.TextIOWrapper(handle, encoding=enc, errors=err)
        return buf

    def _wait_and_getattr(self, name):
        """make sure the instance has a certain attr, and return it."""
        while not hasattr(self, name):
            time.sleep(1e-7)
        return getattr(self, name)


@lazyobject
def SIGNAL_MESSAGES():
    sm = {
        signal.SIGABRT: "Aborted",
        signal.SIGFPE: "Floating point exception",
        signal.SIGILL: "Illegal instructions",
        signal.SIGTERM: "Terminated",
        signal.SIGSEGV: "Segmentation fault",
    }
    if ON_POSIX:
        sm.update(
            {signal.SIGQUIT: "Quit", signal.SIGHUP: "Hangup", signal.SIGKILL: "Killed"}
        )
    return sm


def safe_readlines(handle, hint=-1):
    """Attempts to read lines without throwing an error."""
    try:
        lines = handle.readlines(hint)
    except OSError:
        lines = []
    return lines


def safe_readable(handle):
    """Attempts to find if the handle is readable without throwing an error."""
    try:
        status = handle.readable()
    except (OSError, ValueError):
        status = False
    return status


def update_fg_process_group(pipeline_group, background):
    if background:
        return False
    if not ON_POSIX:
        return False
    env = builtins.__xonsh__.env
    if not env.get("XONSH_INTERACTIVE"):
        return False
    return give_terminal_to(pipeline_group)


class CommandPipeline:
    """Represents a subprocess-mode command pipeline."""

    attrnames = (
        "stdin",
        "stdout",
        "stderr",
        "pid",
        "returncode",
        "args",
        "alias",
        "stdin_redirect",
        "stdout_redirect",
        "stderr_redirect",
        "timestamps",
        "executed_cmd",
        "input",
        "output",
        "errors",
    )

    nonblocking = (io.BytesIO, NonBlockingFDReader, ConsoleParallelReader)

    def __init__(self, specs):
        """
        Parameters
        ----------
        specs : list of SubprocSpec
            Process specifications

        Attributes
        ----------
        spec : SubprocSpec
            The last specification in specs
        proc : Popen-like
            The process in procs
        ended : bool
            Boolean for if the command has stopped executing.
        input : str
            A string of the standard input.
        output : str
            A string of the standard output.
        errors : str
            A string of the standard error.
        lines : list of str
            The output lines
        starttime : floats or None
            Pipeline start timestamp.
        """
        self.starttime = None
        self.ended = False
        self.procs = []
        self.specs = specs
        self.spec = specs[-1]
        self.captured = specs[-1].captured
        self.input = self._output = self.errors = self.endtime = None
        self._closed_handle_cache = {}
        self.lines = []
        self._stderr_prefix = self._stderr_postfix = None
        self.term_pgid = None

        background = self.spec.background
        pipeline_group = None
        for spec in specs:
            if self.starttime is None:
                self.starttime = time.time()
            try:
                proc = spec.run(pipeline_group=pipeline_group)
            except Exception:
                print_exception()
                self._return_terminal()
                self.proc = None
                return
            if (
                proc.pid
                and pipeline_group is None
                and not spec.is_proxy
                and self.captured != "object"
            ):
                pipeline_group = proc.pid
                if update_fg_process_group(pipeline_group, background):
                    self.term_pgid = pipeline_group
            self.procs.append(proc)
        self.proc = self.procs[-1]

    def __repr__(self):
        s = self.__class__.__name__ + "("
        s += ", ".join(a + "=" + str(getattr(self, a)) for a in self.attrnames)
        s += ")"
        return s

    def __bool__(self):
        return self.returncode == 0

    def __len__(self):
        return len(self.procs)

    def __iter__(self):
        """Iterates through stdout and returns the lines, converting to
        strings and universal newlines if needed.
        """
        if self.ended:
            yield from iter(self.lines)
        else:
            yield from self.tee_stdout()

    def iterraw(self):
        """Iterates through the last stdout, and returns the lines
        exactly as found.
        """
        # get appropriate handles
        spec = self.spec
        proc = self.proc
        if proc is None:
            return
        timeout = builtins.__xonsh__.env.get("XONSH_PROC_FREQUENCY")
        # get the correct stdout
        stdout = proc.stdout
        if (
            stdout is None or spec.stdout is None or not safe_readable(stdout)
        ) and spec.captured_stdout is not None:
            stdout = spec.captured_stdout
        if hasattr(stdout, "buffer"):
            stdout = stdout.buffer
        if stdout is not None and not isinstance(stdout, self.nonblocking):
            stdout = NonBlockingFDReader(stdout.fileno(), timeout=timeout)
        if (
            not stdout
            or self.captured == "stdout"
            or not safe_readable(stdout)
            or not spec.threadable
        ):
            # we get here if the process is not threadable or the
            # class is the real Popen
            PrevProcCloser(pipeline=self)
            task = wait_for_active_job()
            if task is None or task["status"] != "stopped":
                proc.wait()
                self._endtime()
                if self.captured == "object":
                    self.end(tee_output=False)
                elif self.captured == "hiddenobject" and stdout:
                    b = stdout.read()
                    lines = b.splitlines(keepends=True)
                    yield from lines
                    self.end(tee_output=False)
                elif self.captured == "stdout":
                    b = stdout.read()
                    s = self._decode_uninew(b, universal_newlines=True)
                    self.lines = s.splitlines(keepends=True)
            return
        # get the correct stderr
        stderr = proc.stderr
        if (
            stderr is None or spec.stderr is None or not safe_readable(stderr)
        ) and spec.captured_stderr is not None:
            stderr = spec.captured_stderr
        if hasattr(stderr, "buffer"):
            stderr = stderr.buffer
        if stderr is not None and not isinstance(stderr, self.nonblocking):
            stderr = NonBlockingFDReader(stderr.fileno(), timeout=timeout)
        # read from process while it is running
        check_prev_done = len(self.procs) == 1
        prev_end_time = None
        i = j = cnt = 1
        while proc.poll() is None:
            if getattr(proc, "suspended", False):
                return
            elif getattr(proc, "in_alt_mode", False):
                time.sleep(0.1)  # probably not leaving any time soon
                continue
            elif not check_prev_done:
                # In the case of pipelines with more than one command
                # we should give the commands a little time
                # to start up fully. This is particularly true for
                # GNU Parallel, which has a long startup time.
                pass
            elif self._prev_procs_done():
                self._close_prev_procs()
                proc.prevs_are_closed = True
                break
            stdout_lines = safe_readlines(stdout, 1024)
            i = len(stdout_lines)
            if i != 0:
                yield from stdout_lines
            stderr_lines = safe_readlines(stderr, 1024)
            j = len(stderr_lines)
            if j != 0:
                self.stream_stderr(stderr_lines)
            if not check_prev_done:
                # if we are piping...
                if stdout_lines or stderr_lines:
                    # see if we have some output.
                    check_prev_done = True
                elif prev_end_time is None:
                    # or see if we already know that the next-to-last
                    # proc in the pipeline has ended.
                    if self._prev_procs_done():
                        # if it has, record the time
                        prev_end_time = time.time()
                elif time.time() - prev_end_time >= 0.1:
                    # if we still don't have any output, even though the
                    # next-to-last proc has finished, wait a bit to make
                    # sure we have fully started up, etc.
                    check_prev_done = True
            # this is for CPU usage
            if i + j == 0:
                cnt = min(cnt + 1, 1000)
            else:
                cnt = 1
            time.sleep(timeout * cnt)
        # read from process now that it is over
        yield from safe_readlines(stdout)
        self.stream_stderr(safe_readlines(stderr))
        proc.wait()
        self._endtime()
        yield from safe_readlines(stdout)
        self.stream_stderr(safe_readlines(stderr))
        if self.captured == "object":
            self.end(tee_output=False)

    def itercheck(self):
        """Iterates through the command lines and throws an error if the
        returncode is non-zero.
        """
        yield from self
        if self.returncode:
            # I included self, as providing access to stderr and other details
            # useful when instance isn't assigned to a variable in the shell.
            raise XonshCalledProcessError(
                self.returncode, self.executed_cmd, self.stdout, self.stderr, self
            )

    def tee_stdout(self):
        """Writes the process stdout to the output variable, line-by-line, and
        yields each line. This may optionally accept lines (in bytes) to iterate
        over, in which case it does not call iterraw().
        """
        env = builtins.__xonsh__.env
        enc = env.get("XONSH_ENCODING")
        err = env.get("XONSH_ENCODING_ERRORS")
        lines = self.lines
        stream = self.captured not in STDOUT_CAPTURE_KINDS
        if stream and not self.spec.stdout:
            stream = False
        stdout_has_buffer = hasattr(sys.stdout, "buffer")
        nl = b"\n"
        cr = b"\r"
        crnl = b"\r\n"
        for line in self.iterraw():
            # write to stdout line ASAP, if needed
            if stream:
                if stdout_has_buffer:
                    sys.stdout.buffer.write(line)
                else:
                    sys.stdout.write(line.decode(encoding=enc, errors=err))
                sys.stdout.flush()
            # do some munging of the line before we return it
            if line.endswith(crnl):
                line = line[:-2] + nl
            elif line.endswith(cr):
                line = line[:-1] + nl
            line = RE_HIDE_ESCAPE.sub(b"", line)
            line = line.decode(encoding=enc, errors=err)
            # tee it up!
            lines.append(line)
            yield line

    def stream_stderr(self, lines):
        """Streams lines to sys.stderr and the errors attribute."""
        if not lines:
            return
        env = builtins.__xonsh__.env
        enc = env.get("XONSH_ENCODING")
        err = env.get("XONSH_ENCODING_ERRORS")
        b = b"".join(lines)
        if self.stderr_prefix:
            b = self.stderr_prefix + b
        if self.stderr_postfix:
            b += self.stderr_postfix
        stderr_has_buffer = hasattr(sys.stderr, "buffer")
        # write bytes to std stream
        if stderr_has_buffer:
            sys.stderr.buffer.write(b)
        else:
            sys.stderr.write(b.decode(encoding=enc, errors=err))
        sys.stderr.flush()
        # do some munging of the line before we save it to the attr
        b = b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        b = RE_HIDE_ESCAPE.sub(b"", b)
        env = builtins.__xonsh__.env
        s = b.decode(
            encoding=env.get("XONSH_ENCODING"), errors=env.get("XONSH_ENCODING_ERRORS")
        )
        # set the errors
        if self.errors is None:
            self.errors = s
        else:
            self.errors += s

    def _decode_uninew(self, b, universal_newlines=None):
        """Decode bytes into a str and apply universal newlines as needed."""
        if not b:
            return ""
        if isinstance(b, bytes):
            env = builtins.__xonsh__.env
            s = b.decode(
                encoding=env.get("XONSH_ENCODING"),
                errors=env.get("XONSH_ENCODING_ERRORS"),
            )
        else:
            s = b
        if universal_newlines or self.spec.universal_newlines:
            s = s.replace("\r\n", "\n").replace("\r", "\n")
        return s

    #
    # Ending methods
    #

    def end(self, tee_output=True):
        """
        End the pipeline, return the controlling terminal if needed.

        Main things done in self._end().
        """
        if self.ended:
            return
        self._end(tee_output=tee_output)
        self._return_terminal()

    def _end(self, tee_output):
        """Waits for the command to complete and then runs any closing and
        cleanup procedures that need to be run.
        """
        if tee_output:
            for _ in self.tee_stdout():
                pass
        self._endtime()
        # since we are driven by getting output, input may not be available
        # until the command has completed.
        self._set_input()
        self._close_prev_procs()
        self._close_proc()
        self._check_signal()
        self._apply_to_history()
        self.ended = True
        self._raise_subproc_error()

    def _return_terminal(self):
        if ON_WINDOWS or not ON_POSIX:
            return
        pgid = os.getpgid(0)
        if self.term_pgid is None or pgid == self.term_pgid:
            return
        if give_terminal_to(pgid):  # if gave term succeed
            self.term_pgid = pgid
            if builtins.__xonsh__.shell is not None:
                # restoring sanity could probably be called whenever we return
                # control to the shell. But it only seems to matter after a
                # ^Z event. This *has* to be called after we give the terminal
                # back to the shell.
                builtins.__xonsh__.shell.shell.restore_tty_sanity()

    def resume(self, job, tee_output=True):
        self.ended = False
        if give_terminal_to(job["pgrp"]):
            self.term_pgid = job["pgrp"]
        _continue(job)
        self.end(tee_output=tee_output)

    def _endtime(self):
        """Sets the closing timestamp if it hasn't been already."""
        if self.endtime is None:
            self.endtime = time.time()

    def _safe_close(self, handle):
        safe_fdclose(handle, cache=self._closed_handle_cache)

    def _prev_procs_done(self):
        """Boolean for if all previous processes have completed. If there
        is only a single process in the pipeline, this returns False.
        """
        any_running = False
        for s, p in zip(self.specs[:-1], self.procs[:-1]):
            if p.poll() is None:
                any_running = True
                continue
            self._safe_close(s.stdin)
            self._safe_close(s.stdout)
            self._safe_close(s.stderr)
            if p is None:
                continue
            self._safe_close(p.stdin)
            self._safe_close(p.stdout)
            self._safe_close(p.stderr)
        return False if any_running else (len(self) > 1)

    def _close_prev_procs(self):
        """Closes all but the last proc's stdout."""
        for s, p in zip(self.specs[:-1], self.procs[:-1]):
            self._safe_close(s.stdin)
            self._safe_close(s.stdout)
            self._safe_close(s.stderr)
            if p is None:
                continue
            self._safe_close(p.stdin)
            self._safe_close(p.stdout)
            self._safe_close(p.stderr)

    def _close_proc(self):
        """Closes last proc's stdout."""
        s = self.spec
        p = self.proc
        self._safe_close(s.stdin)
        self._safe_close(s.stdout)
        self._safe_close(s.stderr)
        self._safe_close(s.captured_stdout)
        self._safe_close(s.captured_stderr)
        if p is None:
            return
        self._safe_close(p.stdin)
        self._safe_close(p.stdout)
        self._safe_close(p.stderr)

    def _set_input(self):
        """Sets the input variable."""
        if self.proc is None:
            return
        stdin = self.proc.stdin
        if (
            stdin is None
            or isinstance(stdin, int)
            or stdin.closed
            or not stdin.seekable()
            or not safe_readable(stdin)
        ):
            input = b""
        else:
            stdin.seek(0)
            input = stdin.read()
        self.input = self._decode_uninew(input)

    def _check_signal(self):
        """Checks if a signal was received and issues a message."""
        proc_signal = getattr(self.proc, "signal", None)
        if proc_signal is None:
            return
        sig, core = proc_signal
        sig_str = SIGNAL_MESSAGES.get(sig)
        if sig_str:
            if core:
                sig_str += " (core dumped)"
            print(sig_str, file=sys.stderr)
            if self.errors is not None:
                self.errors += sig_str + "\n"

    def _apply_to_history(self):
        """Applies the results to the current history object."""
        hist = builtins.__xonsh__.history
        if hist is not None:
            hist.last_cmd_rtn = 1 if self.proc is None else self.proc.returncode

    def _raise_subproc_error(self):
        """Raises a subprocess error, if we are supposed to."""
        spec = self.spec
        rtn = self.returncode
        if (
            rtn is not None
            and rtn > 0
            and builtins.__xonsh__.env.get("RAISE_SUBPROC_ERROR")
        ):
            try:
                raise subprocess.CalledProcessError(rtn, spec.args, output=self.output)
            finally:
                # this is need to get a working terminal in interactive mode
                self._return_terminal()

    #
    # Properties
    #

    @property
    def stdin(self):
        """Process stdin."""
        return self.proc.stdin

    @property
    def stdout(self):
        """Process stdout."""
        return self.proc.stdout

    @property
    def stderr(self):
        """Process stderr."""
        return self.proc.stderr

    @property
    def inp(self):
        """Creates normalized input string from args."""
        return " ".join(self.args)

    @property
    def output(self):
        """Non-blocking, lazy access to output"""
        if self.ended:
            if self._output is None:
                self._output = "".join(self.lines)
            return self._output
        else:
            return "".join(self.lines)

    @property
    def out(self):
        """Output value as a str."""
        self.end()
        return self.output

    @property
    def err(self):
        """Error messages as a string."""
        self.end()
        return self.errors

    @property
    def pid(self):
        """Process identifier."""
        return self.proc.pid

    @property
    def returncode(self):
        """Process return code, waits until command is completed."""
        self.end()
        if self.proc is None:
            return 1
        return self.proc.returncode

    rtn = returncode

    @property
    def args(self):
        """Arguments to the process."""
        return self.spec.args

    @property
    def rtn(self):
        """Alias to return code."""
        return self.returncode

    @property
    def alias(self):
        """Alias the process used."""
        return self.spec.alias

    @property
    def stdin_redirect(self):
        """Redirection used for stdin."""
        stdin = self.spec.stdin
        name = getattr(stdin, "name", "<stdin>")
        mode = getattr(stdin, "mode", "r")
        return [name, mode]

    @property
    def stdout_redirect(self):
        """Redirection used for stdout."""
        stdout = self.spec.stdout
        name = getattr(stdout, "name", "<stdout>")
        mode = getattr(stdout, "mode", "a")
        return [name, mode]

    @property
    def stderr_redirect(self):
        """Redirection used for stderr."""
        stderr = self.spec.stderr
        name = getattr(stderr, "name", "<stderr>")
        mode = getattr(stderr, "mode", "r")
        return [name, mode]

    @property
    def timestamps(self):
        """The start and end time stamps."""
        return [self.starttime, self.endtime]

    @property
    def executed_cmd(self):
        """The resolve and executed command."""
        return self.spec.cmd

    @property
    def stderr_prefix(self):
        """Prefix to print in front of stderr, as bytes."""
        p = self._stderr_prefix
        if p is None:
            env = builtins.__xonsh__.env
            t = env.get("XONSH_STDERR_PREFIX")
            s = format_std_prepost(t, env=env)
            p = s.encode(
                encoding=env.get("XONSH_ENCODING"),
                errors=env.get("XONSH_ENCODING_ERRORS"),
            )
            self._stderr_prefix = p
        return p

    @property
    def stderr_postfix(self):
        """Postfix to print after stderr, as bytes."""
        p = self._stderr_postfix
        if p is None:
            env = builtins.__xonsh__.env
            t = env.get("XONSH_STDERR_POSTFIX")
            s = format_std_prepost(t, env=env)
            p = s.encode(
                encoding=env.get("XONSH_ENCODING"),
                errors=env.get("XONSH_ENCODING_ERRORS"),
            )
            self._stderr_postfix = p
        return p


class HiddenCommandPipeline(CommandPipeline):
    def __repr__(self):
        return ""


def pause_call_resume(p, f, *args, **kwargs):
    """For a process p, this will call a function f with the remaining args and
    and kwargs. If the process cannot accept signals, the function will be called.

    Parameters
    ----------
    p : Popen object or similar
    f : callable
    args : remaining arguments
    kwargs : keyword arguments
    """
    can_send_signal = (
        hasattr(p, "send_signal") and ON_POSIX and not ON_MSYS and not ON_CYGWIN
    )
    if can_send_signal:
        try:
            p.send_signal(signal.SIGSTOP)
        except PermissionError:
            pass
    try:
        f(*args, **kwargs)
    except Exception:
        pass
    if can_send_signal:
        p.send_signal(signal.SIGCONT)


class PrevProcCloser(threading.Thread):
    """Previous process closer thread for pipelines whose last command
    is itself unthreadable. This makes sure that the pipeline is
    driven forward and does not deadlock.
    """

    def __init__(self, pipeline):
        """
        Parameters
        ----------
        pipeline : CommandPipeline
            The pipeline whose prev procs we should close.
        """
        self.pipeline = pipeline
        super().__init__()
        self.daemon = True
        self.start()

    def run(self):
        """Runs the closing algorithm."""
        pipeline = self.pipeline
        check_prev_done = len(pipeline.procs) == 1
        if check_prev_done:
            return
        proc = pipeline.proc
        prev_end_time = None
        timeout = builtins.__xonsh__.env.get("XONSH_PROC_FREQUENCY")
        sleeptime = min(timeout * 1000, 0.1)
        while proc.poll() is None:
            if not check_prev_done:
                # In the case of pipelines with more than one command
                # we should give the commands a little time
                # to start up fully. This is particularly true for
                # GNU Parallel, which has a long startup time.
                pass
            elif pipeline._prev_procs_done():
                pipeline._close_prev_procs()
                proc.prevs_are_closed = True
                break
            if not check_prev_done:
                # if we are piping...
                if prev_end_time is None:
                    # or see if we already know that the next-to-last
                    # proc in the pipeline has ended.
                    if pipeline._prev_procs_done():
                        # if it has, record the time
                        prev_end_time = time.time()
                elif time.time() - prev_end_time >= 0.1:
                    # if we still don't have any output, even though the
                    # next-to-last proc has finished, wait a bit to make
                    # sure we have fully started up, etc.
                    check_prev_done = True
            # this is for CPU usage
            time.sleep(sleeptime)

#
# shell
#
# -*- coding: utf-8 -*-
"""The xonsh shell"""
# amalgamated sys
random = _LazyModule.load('random', 'random')
# amalgamated time
# amalgamated difflib
# amalgamated builtins
# amalgamated warnings
# amalgamated xonsh.platform
# amalgamated xonsh.tools
# amalgamated xonsh.events
xhm = _LazyModule.load('xonsh', 'xonsh.history.main', 'xhm')
events.doc(
    "on_transform_command",
    """
on_transform_command(cmd: str) -> str

Fired to request xontribs to transform a command line. Return the transformed
command, or the same command if no transformation occurs. Only done for
interactive sessions.

This may be fired multiple times per command, with other transformers input or
output, so design any handlers for this carefully.
""",
)

events.doc(
    "on_precommand",
    """
on_precommand(cmd: str) -> None

Fires just before a command is executed.
""",
)

events.doc(
    "on_postcommand",
    """
on_postcommand(cmd: str, rtn: int, out: str or None, ts: list) -> None

Fires just after a command is executed. The arguments are the same as history.

Parameters:

* ``cmd``: The command that was executed (after transformation)
* ``rtn``: The result of the command executed (``0`` for success)
* ``out``: If xonsh stores command output, this is the output
* ``ts``: Timestamps, in the order of ``[starting, ending]``
""",
)

events.doc(
    "on_pre_prompt",
    """
on_first_prompt() -> None

Fires just before the prompt is shown
""",
)

events.doc(
    "on_post_prompt",
    """
on_first_prompt() -> None

Fires just after the prompt returns
""",
)


def transform_command(src, show_diff=True):
    """Returns the results of firing the precommand handles."""
    i = 0
    limit = sys.getrecursionlimit()
    lst = ""
    raw = src
    while src != lst:
        lst = src
        srcs = events.on_transform_command.fire(cmd=src)
        for s in srcs:
            if s != lst:
                src = s
                break
        i += 1
        if i == limit:
            print_exception(
                "Modifications to source input took more than "
                "the recursion limit number of iterations to "
                "converge."
            )
    debug_level = builtins.__xonsh__.env.get("XONSH_DEBUG")
    if show_diff and debug_level > 1 and src != raw:
        sys.stderr.writelines(
            difflib.unified_diff(
                raw.splitlines(keepends=True),
                src.splitlines(keepends=True),
                fromfile="before precommand event",
                tofile="after precommand event",
            )
        )
    return src


class Shell(object):
    """Main xonsh shell.

    Initializes execution environment and decides if prompt_toolkit or
    readline version of shell should be used.
    """

    shell_type_aliases = {
        "b": "best",
        "best": "best",
        "d": "dumb",
        "dumb": "dumb",
        "ptk": "prompt_toolkit",
        "ptk1": "prompt_toolkit1",
        "ptk2": "prompt_toolkit2",
        "prompt-toolkit": "prompt_toolkit",
        "prompt_toolkit": "prompt_toolkit",
        "prompt-toolkit1": "prompt_toolkit1",
        "prompt-toolkit2": "prompt_toolkit2",
        "rand": "random",
        "random": "random",
        "rl": "readline",
        "readline": "readline",
    }

    def __init__(self, execer, ctx=None, shell_type=None, **kwargs):
        """
        Parameters
        ----------
        execer : Execer
            An execer instance capable of running xonsh code.
        ctx : Mapping, optional
            The execution context for the shell (e.g. the globals namespace).
            If none, this is computed by loading the rc files. If not None,
            this no additional context is computed and this is used
            directly.
        shell_type : str, optional
            The shell type to start, such as 'readline', 'prompt_toolkit1',
            or 'random'.
        """
        self.execer = execer
        self.ctx = {} if ctx is None else ctx
        env = builtins.__xonsh__.env
        # build history backend before creating shell
        builtins.__xonsh__.history = hist = xhm.construct_history(
            env=env.detype(), ts=[time.time(), None], locked=True
        )

        # pick a valid shell -- if no shell is specified by the user,
        # shell type is pulled from env
        if shell_type is None:
            shell_type = env.get("SHELL_TYPE")
            if shell_type == "none":
                # This bricks interactive xonsh
                # Can happen from the use of .xinitrc, .xsession, etc
                shell_type = "best"
        shell_type = self.shell_type_aliases.get(shell_type, shell_type)
        if shell_type == "best" or shell_type is None:
            shell_type = best_shell_type()
        elif env.get("TERM", "") == "dumb":
            shell_type = "dumb"
        elif shell_type == "random":
            shell_type = random.choice(("readline", "prompt_toolkit"))
        if shell_type == "prompt_toolkit":
            if not has_prompt_toolkit():
                warnings.warn(
                    "prompt_toolkit is not available, using " "readline instead."
                )
                shell_type = "readline"
            elif not ptk_above_min_supported():
                warnings.warn(
                    "prompt-toolkit version < v1.0.0 is not "
                    "supported. Please update prompt-toolkit. Using "
                    "readline instead."
                )
                shell_type = "readline"
            else:
                shell_type = ptk_shell_type()
        self.shell_type = env["SHELL_TYPE"] = shell_type
        # actually make the shell
        if shell_type == "none":
            from xonsh.base_shell import BaseShell as shell_class
        elif shell_type == "prompt_toolkit2":
            from xonsh.ptk2.shell import PromptToolkit2Shell as shell_class
        elif shell_type == "prompt_toolkit1":
            from xonsh.ptk.shell import PromptToolkitShell as shell_class
        elif shell_type == "readline":
            from xonsh.readline_shell import ReadlineShell as shell_class
        elif shell_type == "jupyter":
            from xonsh.jupyter_shell import JupyterShell as shell_class
        elif shell_type == "dumb":
            from xonsh.dumb_shell import DumbShell as shell_class
        else:
            raise XonshError("{} is not recognized as a shell type".format(shell_type))
        self.shell = shell_class(execer=self.execer, ctx=self.ctx, **kwargs)
        # allows history garbage collector to start running
        if hist.gc is not None:
            hist.gc.wait_for_shell = False

    def __getattr__(self, attr):
        """Delegates calls to appropriate shell instance."""
        return getattr(self.shell, attr)

#
# style_tools
#
"""Xonsh color styling tools that simulate pygments, when it is unavailable."""
# amalgamated builtins
from collections import defaultdict

# amalgamated xonsh.platform
# amalgamated xonsh.lazyasd
# amalgamated xonsh.color_tools
# amalgamated xonsh.tools
class _TokenType(tuple):
    """
    Forked from the pygments project
    https://bitbucket.org/birkenfeld/pygments-main
    Copyright (c) 2006-2017 by the respective authors, All rights reserved.
    See https://bitbucket.org/birkenfeld/pygments-main/raw/05818a4ef9891d9ac22c851f7b3ea4b4fce460ab/AUTHORS
    """

    parent = None

    def split(self):
        buf = []
        node = self
        while node is not None:
            buf.append(node)
            node = node.parent
        buf.reverse()
        return buf

    def __init__(self, *args):
        # no need to call super.__init__
        self.subtypes = set()

    def __contains__(self, val):
        return self is val or (type(val) is self.__class__ and val[: len(self)] == self)

    def __getattr__(self, val):
        if not val or not val[0].isupper():
            return tuple.__getattribute__(self, val)
        new = _TokenType(self + (val,))
        setattr(self, val, new)
        self.subtypes.add(new)
        new.parent = self
        return new

    def __repr__(self):
        return "Token" + (self and "." or "") + ".".join(self)

    def __copy__(self):
        # These instances are supposed to be singletons
        return self

    def __deepcopy__(self, memo):
        # These instances are supposed to be singletons
        return self


Token = _TokenType()
Color = Token.Color


def partial_color_tokenize(template):
    """Tokenizes a template string containing colors. Will return a list
    of tuples mapping the token to the string which has that color.
    These sub-strings maybe templates themselves.
    """
    if HAS_PYGMENTS and builtins.__xonsh__.shell is not None:
        styles = __xonsh__.shell.shell.styler.styles
    elif builtins.__xonsh__.shell is not None:
        styles = DEFAULT_STYLE_DICT
    else:
        styles = None
    color = Color.NO_COLOR
    try:
        toks, color = _partial_color_tokenize_main(template, styles)
    except Exception:
        toks = [(Color.NO_COLOR, template)]
    if styles is not None:
        styles[color]  # ensure color is available
    return toks


def _partial_color_tokenize_main(template, styles):
    bopen = "{"
    bclose = "}"
    colon = ":"
    expl = "!"
    color = Color.NO_COLOR
    fg = bg = None
    value = ""
    toks = []
    for literal, field, spec, conv in FORMATTER.parse(template):
        if field is None:
            value += literal
        elif field in KNOWN_COLORS or "#" in field:
            value += literal
            next_color, fg, bg = color_by_name(field, fg, bg)
            if next_color is not color:
                if len(value) > 0:
                    toks.append((color, value))
                    if styles is not None:
                        styles[color]  # ensure color is available
                color = next_color
                value = ""
        elif field is not None:
            parts = [literal, bopen, field]
            if conv is not None and len(conv) > 0:
                parts.append(expl)
                parts.append(conv)
            if spec is not None and len(spec) > 0:
                parts.append(colon)
                parts.append(spec)
            parts.append(bclose)
            value += "".join(parts)
        else:
            value += literal
    toks.append((color, value))
    return toks, color


def color_by_name(name, fg=None, bg=None):
    """Converts a color name to a color token, foreground name,
    and background name.  Will take into consideration current foreground
    and background colors, if provided.

    Parameters
    ----------
    name : str
        Color name.
    fg : str, optional
        Foreground color name.
    bg : str, optional
        Background color name.

    Returns
    -------
    tok : Token
        Pygments Token.Color subclass
    fg : str or None
        New computed foreground color name.
    bg : str or None
        New computed background color name.
    """
    name = name.upper()
    if name == "NO_COLOR":
        return Color.NO_COLOR, None, None
    m = RE_BACKGROUND.search(name)
    if m is None:  # must be foreground color
        fg = norm_name(name)
    else:
        bg = norm_name(name)
    # assemble token
    if fg is None and bg is None:
        tokname = "NO_COLOR"
    elif fg is None:
        tokname = bg
    elif bg is None:
        tokname = fg
    else:
        tokname = fg + "__" + bg
    tok = getattr(Color, tokname)
    return tok, fg, bg


def norm_name(name):
    """Normalizes a color name."""
    return name.replace("#", "HEX").replace("BGHEX", "BACKGROUND_HEX")


KNOWN_COLORS = LazyObject(
    lambda: frozenset(
        [
            "BACKGROUND_BLACK",
            "BACKGROUND_BLUE",
            "BACKGROUND_CYAN",
            "BACKGROUND_GREEN",
            "BACKGROUND_INTENSE_BLACK",
            "BACKGROUND_INTENSE_BLUE",
            "BACKGROUND_INTENSE_CYAN",
            "BACKGROUND_INTENSE_GREEN",
            "BACKGROUND_INTENSE_PURPLE",
            "BACKGROUND_INTENSE_RED",
            "BACKGROUND_INTENSE_WHITE",
            "BACKGROUND_INTENSE_YELLOW",
            "BACKGROUND_PURPLE",
            "BACKGROUND_RED",
            "BACKGROUND_WHITE",
            "BACKGROUND_YELLOW",
            "BLACK",
            "BLUE",
            "BOLD_BLACK",
            "BOLD_BLUE",
            "BOLD_CYAN",
            "BOLD_GREEN",
            "BOLD_INTENSE_BLACK",
            "BOLD_INTENSE_BLUE",
            "BOLD_INTENSE_CYAN",
            "BOLD_INTENSE_GREEN",
            "BOLD_INTENSE_PURPLE",
            "BOLD_INTENSE_RED",
            "BOLD_INTENSE_WHITE",
            "BOLD_INTENSE_YELLOW",
            "BOLD_PURPLE",
            "BOLD_RED",
            "BOLD_UNDERLINE_BLACK",
            "BOLD_UNDERLINE_BLUE",
            "BOLD_UNDERLINE_CYAN",
            "BOLD_UNDERLINE_GREEN",
            "BOLD_UNDERLINE_INTENSE_BLACK",
            "BOLD_UNDERLINE_INTENSE_BLUE",
            "BOLD_UNDERLINE_INTENSE_CYAN",
            "BOLD_UNDERLINE_INTENSE_GREEN",
            "BOLD_UNDERLINE_INTENSE_PURPLE",
            "BOLD_UNDERLINE_INTENSE_RED",
            "BOLD_UNDERLINE_INTENSE_WHITE",
            "BOLD_UNDERLINE_INTENSE_YELLOW",
            "BOLD_UNDERLINE_PURPLE",
            "BOLD_UNDERLINE_RED",
            "BOLD_UNDERLINE_WHITE",
            "BOLD_UNDERLINE_YELLOW",
            "BOLD_WHITE",
            "BOLD_YELLOW",
            "CYAN",
            "GREEN",
            "INTENSE_BLACK",
            "INTENSE_BLUE",
            "INTENSE_CYAN",
            "INTENSE_GREEN",
            "INTENSE_PURPLE",
            "INTENSE_RED",
            "INTENSE_WHITE",
            "INTENSE_YELLOW",
            "NO_COLOR",
            "PURPLE",
            "RED",
            "UNDERLINE_BLACK",
            "UNDERLINE_BLUE",
            "UNDERLINE_CYAN",
            "UNDERLINE_GREEN",
            "UNDERLINE_INTENSE_BLACK",
            "UNDERLINE_INTENSE_BLUE",
            "UNDERLINE_INTENSE_CYAN",
            "UNDERLINE_INTENSE_GREEN",
            "UNDERLINE_INTENSE_PURPLE",
            "UNDERLINE_INTENSE_RED",
            "UNDERLINE_INTENSE_WHITE",
            "UNDERLINE_INTENSE_YELLOW",
            "UNDERLINE_PURPLE",
            "UNDERLINE_RED",
            "UNDERLINE_WHITE",
            "UNDERLINE_YELLOW",
            "WHITE",
            "YELLOW",
        ]
    ),
    globals(),
    "KNOWN_COLORS",
)

DEFAULT_STYLE_DICT = LazyObject(
    lambda: defaultdict(
        lambda: "",
        {
            Token: "",
            Token.Aborted: "ansibrightblack",
            Token.AutoSuggestion: "ansibrightblack",
            Token.Color.BACKGROUND_BLACK: "bg:ansiblack",
            Token.Color.BACKGROUND_BLUE: "bg:ansiblue",
            Token.Color.BACKGROUND_CYAN: "bg:ansicyan",
            Token.Color.BACKGROUND_GREEN: "bg:ansigreen",
            Token.Color.BACKGROUND_INTENSE_BLACK: "bg:ansibrightblack",
            Token.Color.BACKGROUND_INTENSE_BLUE: "bg:ansibrightblue",
            Token.Color.BACKGROUND_INTENSE_CYAN: "bg:ansibrightcyan",
            Token.Color.BACKGROUND_INTENSE_GREEN: "bg:ansibrightgreen",
            Token.Color.BACKGROUND_INTENSE_PURPLE: "bg:ansibrightmagenta",
            Token.Color.BACKGROUND_INTENSE_RED: "bg:ansibrightred",
            Token.Color.BACKGROUND_INTENSE_WHITE: "bg:ansiwhite",
            Token.Color.BACKGROUND_INTENSE_YELLOW: "bg:ansibrightyellow",
            Token.Color.BACKGROUND_PURPLE: "bg:ansimagenta",
            Token.Color.BACKGROUND_RED: "bg:ansired",
            Token.Color.BACKGROUND_WHITE: "bg:ansigray",
            Token.Color.BACKGROUND_YELLOW: "bg:ansiyellow",
            Token.Color.BLACK: "ansiblack",
            Token.Color.BLUE: "ansiblue",
            Token.Color.BOLD_BLACK: "bold ansiblack",
            Token.Color.BOLD_BLUE: "bold ansiblue",
            Token.Color.BOLD_CYAN: "bold ansicyan",
            Token.Color.BOLD_GREEN: "bold ansigreen",
            Token.Color.BOLD_INTENSE_BLACK: "bold ansibrightblack",
            Token.Color.BOLD_INTENSE_BLUE: "bold ansibrightblue",
            Token.Color.BOLD_INTENSE_CYAN: "bold ansibrightcyan",
            Token.Color.BOLD_INTENSE_GREEN: "bold ansibrightgreen",
            Token.Color.BOLD_INTENSE_PURPLE: "bold ansibrightmagenta",
            Token.Color.BOLD_INTENSE_RED: "bold ansibrightred",
            Token.Color.BOLD_INTENSE_WHITE: "bold ansiwhite",
            Token.Color.BOLD_INTENSE_YELLOW: "bold ansibrightyellow",
            Token.Color.BOLD_PURPLE: "bold ansimagenta",
            Token.Color.BOLD_RED: "bold ansired",
            Token.Color.BOLD_UNDERLINE_BLACK: "bold underline ansiblack",
            Token.Color.BOLD_UNDERLINE_BLUE: "bold underline ansiblue",
            Token.Color.BOLD_UNDERLINE_CYAN: "bold underline ansicyan",
            Token.Color.BOLD_UNDERLINE_GREEN: "bold underline ansigreen",
            Token.Color.BOLD_UNDERLINE_INTENSE_BLACK: "bold underline ansibrightblack",
            Token.Color.BOLD_UNDERLINE_INTENSE_BLUE: "bold underline ansibrightblue",
            Token.Color.BOLD_UNDERLINE_INTENSE_CYAN: "bold underline ansibrightcyan",
            Token.Color.BOLD_UNDERLINE_INTENSE_GREEN: "bold underline ansibrightgreen",
            Token.Color.BOLD_UNDERLINE_INTENSE_PURPLE: "bold underline ansibrightmagenta",
            Token.Color.BOLD_UNDERLINE_INTENSE_RED: "bold underline ansibrightred",
            Token.Color.BOLD_UNDERLINE_INTENSE_WHITE: "bold underline ansiwhite",
            Token.Color.BOLD_UNDERLINE_INTENSE_YELLOW: "bold underline ansibrightyellow",
            Token.Color.BOLD_UNDERLINE_PURPLE: "bold underline ansimagenta",
            Token.Color.BOLD_UNDERLINE_RED: "bold underline ansired",
            Token.Color.BOLD_UNDERLINE_WHITE: "bold underline ansigray",
            Token.Color.BOLD_UNDERLINE_YELLOW: "bold underline ansiyellow",
            Token.Color.BOLD_WHITE: "bold ansigray",
            Token.Color.BOLD_YELLOW: "bold ansiyellow",
            Token.Color.CYAN: "ansicyan",
            Token.Color.GREEN: "ansigreen",
            Token.Color.INTENSE_BLACK: "ansibrightblack",
            Token.Color.INTENSE_BLUE: "ansibrightblue",
            Token.Color.INTENSE_CYAN: "ansibrightcyan",
            Token.Color.INTENSE_GREEN: "ansibrightgreen",
            Token.Color.INTENSE_PURPLE: "ansibrightmagenta",
            Token.Color.INTENSE_RED: "ansibrightred",
            Token.Color.INTENSE_WHITE: "ansiwhite",
            Token.Color.INTENSE_YELLOW: "ansibrightyellow",
            Token.Color.NO_COLOR: "noinherit",
            Token.Color.PURPLE: "ansimagenta",
            Token.Color.RED: "ansired",
            Token.Color.UNDERLINE_BLACK: "underline ansiblack",
            Token.Color.UNDERLINE_BLUE: "underline ansiblue",
            Token.Color.UNDERLINE_CYAN: "underline ansicyan",
            Token.Color.UNDERLINE_GREEN: "underline ansigreen",
            Token.Color.UNDERLINE_INTENSE_BLACK: "underline ansibrightblack",
            Token.Color.UNDERLINE_INTENSE_BLUE: "underline ansibrightblue",
            Token.Color.UNDERLINE_INTENSE_CYAN: "underline ansibrightcyan",
            Token.Color.UNDERLINE_INTENSE_GREEN: "underline ansibrightgreen",
            Token.Color.UNDERLINE_INTENSE_PURPLE: "underline ansibrightmagenta",
            Token.Color.UNDERLINE_INTENSE_RED: "underline ansibrightred",
            Token.Color.UNDERLINE_INTENSE_WHITE: "underline ansiwhite",
            Token.Color.UNDERLINE_INTENSE_YELLOW: "underline ansibrightyellow",
            Token.Color.UNDERLINE_PURPLE: "underline ansimagenta",
            Token.Color.UNDERLINE_RED: "underline ansired",
            Token.Color.UNDERLINE_WHITE: "underline ansigray",
            Token.Color.UNDERLINE_YELLOW: "underline ansiyellow",
            Token.Color.WHITE: "ansigray",
            Token.Color.YELLOW: "ansiyellow",
            Token.Comment: "underline ansicyan",
            Token.Comment.Hashbang: "",
            Token.Comment.Multiline: "",
            Token.Comment.Preproc: "underline ansiyellow",
            Token.Comment.PreprocFile: "",
            Token.Comment.Single: "",
            Token.Comment.Special: "",
            Token.Error: "ansibrightred",
            Token.Escape: "",
            Token.Generic: "",
            Token.Generic.Deleted: "ansired",
            Token.Generic.Emph: "underline",
            Token.Generic.Error: "bold ansibrightred",
            Token.Generic.Heading: "bold ansiblue",
            Token.Generic.Inserted: "ansibrightgreen",
            Token.Generic.Output: "ansiblue",
            Token.Generic.Prompt: "bold ansiblue",
            Token.Generic.Strong: "",
            Token.Generic.Subheading: "bold ansimagenta",
            Token.Generic.Traceback: "ansiblue",
            Token.Keyword: "bold ansigreen",
            Token.Keyword.Constant: "",
            Token.Keyword.Declaration: "",
            Token.Keyword.Namespace: "",
            Token.Keyword.Pseudo: "nobold",
            Token.Keyword.Reserved: "",
            Token.Keyword.Type: "nobold ansired",
            Token.Literal: "",
            Token.Literal.Date: "",
            Token.Literal.Number: "ansibrightblack",
            Token.Literal.Number.Bin: "",
            Token.Literal.Number.Float: "",
            Token.Literal.Number.Hex: "",
            Token.Literal.Number.Integer: "",
            Token.Literal.Number.Integer.Long: "",
            Token.Literal.Number.Oct: "",
            Token.Literal.String: "ansibrightred",
            Token.Literal.String.Affix: "",
            Token.Literal.String.Backtick: "",
            Token.Literal.String.Char: "",
            Token.Literal.String.Delimiter: "",
            Token.Literal.String.Doc: "underline",
            Token.Literal.String.Double: "",
            Token.Literal.String.Escape: "bold ansiyellow",
            Token.Literal.String.Heredoc: "",
            Token.Literal.String.Interpol: "bold ansimagenta",
            Token.Literal.String.Other: "ansigreen",
            Token.Literal.String.Regex: "ansimagenta",
            Token.Literal.String.Single: "",
            Token.Literal.String.Symbol: "ansiyellow",
            Token.Menu.Completions: "bg:ansigray ansiblack",
            Token.Menu.Completions.Completion: "",
            Token.Menu.Completions.Completion.Current: "bg:ansibrightblack ansiwhite",
            Token.Name: "",
            Token.Name.Attribute: "ansibrightyellow",
            Token.Name.Builtin: "ansigreen",
            Token.Name.Builtin.Pseudo: "",
            Token.Name.Class: "bold ansibrightblue",
            Token.Name.Constant: "ansired",
            Token.Name.Decorator: "ansibrightmagenta",
            Token.Name.Entity: "bold ansigray",
            Token.Name.Exception: "bold ansibrightred",
            Token.Name.Function: "ansibrightblue",
            Token.Name.Function.Magic: "",
            Token.Name.Label: "ansibrightyellow",
            Token.Name.Namespace: "bold ansibrightblue",
            Token.Name.Other: "",
            Token.Name.Property: "",
            Token.Name.Tag: "bold ansigreen",
            Token.Name.Variable: "ansiblue",
            Token.Name.Variable.Class: "",
            Token.Name.Variable.Global: "",
            Token.Name.Variable.Instance: "",
            Token.Name.Variable.Magic: "",
            Token.Operator: "ansibrightblack",
            Token.Operator.Word: "bold ansimagenta",
            Token.Other: "",
            Token.Punctuation: "",
            Token.Scrollbar: "bg:ansibrightblack",
            Token.Scrollbar.Arrow: "bg:ansiblack ansiwhite bold",
            Token.Scrollbar.Button: "bg:ansiblack",
            Token.Text: "",
            Token.Text.Whitespace: "ansigray",
        },
    ),
    globals(),
    "DEFAULT_STYLE_DICT",
)

PTK2_STYLE = {
    "completion-menu": "bg:ansigray ansiblack",
    "completion-menu.completion": "",
    "completion-menu.completion.current": "bg:ansibrightblack ansiwhite",
    "scrollbar.background": "bg:ansibrightblack",
    "scrollbar.arrow": "bg:ansiblack ansiwhite bold",
    "scrollbar.button": "bg:ansiblack",
    "auto-suggestion": "ansibrightblack",
    "aborting": "ansibrightblack",
}

#
# timings
#
# -*- coding: utf-8 -*-
"""Timing related functionality for the xonsh shell.

The following time_it alias and Timer was forked from the IPython project:
* Copyright (c) 2008-2014, IPython Development Team
* Copyright (C) 2001-2007 Fernando Perez <fperez@colorado.edu>
* Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
* Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>
"""
# amalgamated os
gc = _LazyModule.load('gc', 'gc')
# amalgamated sys
# amalgamated math
# amalgamated time
timeit = _LazyModule.load('timeit', 'timeit')
# amalgamated builtins
# amalgamated itertools
# amalgamated xonsh.lazyasd
# amalgamated xonsh.events
# amalgamated xonsh.platform
@lazybool
def _HAVE_RESOURCE():
    try:
        import resource as r

        have = True
    except ImportError:
        # There is no distinction of user/system time under windows, so we
        # just use time.perf_counter() for everything...
        have = False
    return have


@lazyobject
def resource():
    import resource as r

    return r


@lazyobject
def clocku():
    if _HAVE_RESOURCE:

        def clocku():
            """clocku() -> floating point number
            Return the *USER* CPU time in seconds since the start of the
            process."""
            return resource.getrusage(resource.RUSAGE_SELF)[0]

    else:
        clocku = time.perf_counter
    return clocku


@lazyobject
def clocks():
    if _HAVE_RESOURCE:

        def clocks():
            """clocks() -> floating point number
            Return the *SYSTEM* CPU time in seconds since the start of the
            process."""
            return resource.getrusage(resource.RUSAGE_SELF)[1]

    else:
        clocks = time.perf_counter
    return clocks


@lazyobject
def clock():
    if _HAVE_RESOURCE:

        def clock():
            """clock() -> floating point number
            Return the *TOTAL USER+SYSTEM* CPU time in seconds since the
            start of the process."""
            u, s = resource.getrusage(resource.RUSAGE_SELF)[:2]
            return u + s

    else:
        clock = time.perf_counter
    return clock


@lazyobject
def clock2():
    if _HAVE_RESOURCE:

        def clock2():
            """clock2() -> (t_user,t_system)
            Similar to clock(), but return a tuple of user/system times."""
            return resource.getrusage(resource.RUSAGE_SELF)[:2]

    else:

        def clock2():
            """Under windows, system CPU time can't be measured.
            This just returns perf_counter() and zero."""
            return time.perf_counter(), 0.0

    return clock2


def format_time(timespan, precision=3):
    """Formats the timespan in a human readable form"""
    if timespan >= 60.0:
        # we have more than a minute, format that in a human readable form
        parts = [("d", 60 * 60 * 24), ("h", 60 * 60), ("min", 60), ("s", 1)]
        time = []
        leftover = timespan
        for suffix, length in parts:
            value = int(leftover / length)
            if value > 0:
                leftover = leftover % length
                time.append("{0}{1}".format(str(value), suffix))
            if leftover < 1:
                break
        return " ".join(time)
    # Unfortunately the unicode 'micro' symbol can cause problems in
    # certain terminals.
    # See bug: https://bugs.launchpad.net/ipython/+bug/348466
    # Try to prevent crashes by being more secure than it needs to
    # E.g. eclipse is able to print a mu, but has no sys.stdout.encoding set.
    units = ["s", "ms", "us", "ns"]  # the save value
    if hasattr(sys.stdout, "encoding") and sys.stdout.encoding:
        try:
            "\xb5".encode(sys.stdout.encoding)
            units = ["s", "ms", "\xb5s", "ns"]
        except Exception:
            pass
    scaling = [1, 1e3, 1e6, 1e9]

    if timespan > 0.0:
        order = min(-int(math.floor(math.log10(timespan)) // 3), 3)
    else:
        order = 3
    return "{1:.{0}g} {2}".format(precision, timespan * scaling[order], units[order])


class Timer(timeit.Timer):
    """Timer class that explicitly uses self.inner
    which is an undocumented implementation detail of CPython,
    not shared by PyPy.
    """

    # Timer.timeit copied from CPython 3.4.2
    def timeit(self, number=timeit.default_number):
        """Time 'number' executions of the main statement.
        To be precise, this executes the setup statement once, and
        then returns the time it takes to execute the main statement
        a number of times, as a float measured in seconds.  The
        argument is the number of times through the loop, defaulting
        to one million.  The main statement, the setup statement and
        the timer function to be used are passed to the constructor.
        """
        it = itertools.repeat(None, number)
        gcold = gc.isenabled()
        gc.disable()
        try:
            timing = self.inner(it, self.timer)
        finally:
            if gcold:
                gc.enable()
        return timing


INNER_TEMPLATE = """
def inner(_it, _timer):
    #setup
    _t0 = _timer()
    for _i in _it:
        {stmt}
    _t1 = _timer()
    return _t1 - _t0
"""


def timeit_alias(args, stdin=None):
    """Runs timing study on arguments."""
    # some real args
    number = 0
    quiet = False
    repeat = 3
    precision = 3
    # setup
    ctx = builtins.__xonsh__.ctx
    timer = Timer(timer=clock)
    stmt = " ".join(args)
    innerstr = INNER_TEMPLATE.format(stmt=stmt)
    # Track compilation time so it can be reported if too long
    # Minimum time above which compilation time will be reported
    tc_min = 0.1
    t0 = clock()
    innercode = builtins.compilex(
        innerstr, filename="<xonsh-timeit>", mode="exec", glbs=ctx
    )
    tc = clock() - t0
    # get inner func
    ns = {}
    builtins.execx(innercode, glbs=ctx, locs=ns, mode="exec")
    timer.inner = ns["inner"]
    # Check if there is a huge difference between the best and worst timings.
    worst_tuning = 0
    if number == 0:
        # determine number so that 0.2 <= total time < 2.0
        number = 1
        for _ in range(1, 10):
            time_number = timer.timeit(number)
            worst_tuning = max(worst_tuning, time_number / number)
            if time_number >= 0.2:
                break
            number *= 10
    all_runs = timer.repeat(repeat, number)
    best = min(all_runs) / number
    # print some debug info
    if not quiet:
        worst = max(all_runs) / number
        if worst_tuning:
            worst = max(worst, worst_tuning)
        # Check best timing is greater than zero to avoid a
        # ZeroDivisionError.
        # In cases where the slowest timing is less than 10 microseconds
        # we assume that it does not really matter if the fastest
        # timing is 4 times faster than the slowest timing or not.
        if worst > 4 * best and best > 0 and worst > 1e-5:
            print(
                (
                    "The slowest run took {0:0.2f} times longer than the "
                    "fastest. This could mean that an intermediate result "
                    "is being cached."
                ).format(worst / best)
            )
        print(
            "{0} loops, best of {1}: {2} per loop".format(
                number, repeat, format_time(best, precision)
            )
        )
        if tc > tc_min:
            print("Compiler time: {0:.2f} s".format(tc))
    return


_timings = {"start": clock()}


def setup_timings(argv):
    global _timings
    if "--timings" in argv:
        events.doc(
            "on_timingprobe",
            """
        on_timingprobe(name: str) -> None

        Fired to insert some timings into the startuptime list
        """,
        )

        @events.on_timingprobe
        def timing_on_timingprobe(name, **kw):
            global _timings
            _timings[name] = clock()

        @events.on_post_cmdloop
        def timing_on_post_cmdloop(**kw):
            global _timings
            _timings["on_post_cmdloop"] = clock()

        @events.on_post_init
        def timing_on_post_init(**kw):
            global _timings
            _timings["on_post_init"] = clock()

        @events.on_post_rc
        def timing_on_post_rc(**kw):
            global _timings
            _timings["on_post_rc"] = clock()

        @events.on_postcommand
        def timing_on_postcommand(**kw):
            global _timings
            _timings["on_postcommand"] = clock()

        @events.on_pre_cmdloop
        def timing_on_pre_cmdloop(**kw):
            global _timings
            _timings["on_pre_cmdloop"] = clock()

        @events.on_pre_rc
        def timing_on_pre_rc(**kw):
            global _timings
            _timings["on_pre_rc"] = clock()

        @events.on_precommand
        def timing_on_precommand(**kw):
            global _timings
            _timings["on_precommand"] = clock()

        @events.on_ptk_create
        def timing_on_ptk_create(**kw):
            global _timings
            _timings["on_ptk_create"] = clock()

        @events.on_chdir
        def timing_on_chdir(**kw):
            global _timings
            _timings["on_chdir"] = clock()

        @events.on_post_prompt
        def timing_on_post_prompt(**kw):
            global _timings
            _timings = {"on_post_prompt": clock()}

        @events.on_pre_prompt
        def timing_on_pre_prompt(**kw):
            global _timings
            _timings["on_pre_prompt"] = clock()
            times = list(_timings.items())
            times = sorted(times, key=lambda x: x[1])
            width = max(len(s) for s, _ in times) + 2
            header_format = "|{{:<{}}}|{{:^11}}|{{:^11}}|".format(width)
            entry_format = "|{{:<{}}}|{{:^11.3f}}|{{:^11.3f}}|".format(width)
            sepline = "|{}|{}|{}|".format("-" * width, "-" * 11, "-" * 11)
            # Print result table
            print(" Debug level: {}".format(os.getenv("XONSH_DEBUG", "Off")))
            print(sepline)
            print(header_format.format("Event name", "Time (s)", "Delta (s)"))
            print(sepline)
            prevtime = tstart = times[0][1]
            for name, ts in times:
                print(entry_format.format(name, ts - tstart, ts - prevtime))
                prevtime = ts
            print(sepline)

#
# xonfig
#
"""The xonsh configuration (xonfig) utility."""
# amalgamated os
# amalgamated re
# amalgamated ast
# amalgamated json
shutil = _LazyModule.load('shutil', 'shutil')
# amalgamated random
pprint = _LazyModule.load('pprint', 'pprint')
# amalgamated textwrap
# amalgamated builtins
# amalgamated argparse
# amalgamated functools
# amalgamated itertools
# amalgamated contextlib
# amalgamated collections
try:
    import ply
except ImportError:
    from xonsh.ply import ply

wiz = _LazyModule.load('xonsh', 'xonsh.wizard', 'wiz')
from xonsh import __version__ as XONSH_VERSION
from xonsh.prompt.base import is_template_string
# amalgamated xonsh.platform
# amalgamated xonsh.tools
# amalgamated xonsh.foreign_shells
# amalgamated xonsh.xontribs
# amalgamated xonsh.lazyasd
HR = "'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'"
WIZARD_HEAD = """
          {{BOLD_WHITE}}Welcome to the xonsh configuration wizard!{{NO_COLOR}}
          {{YELLOW}}------------------------------------------{{NO_COLOR}}
This will present a guided tour through setting up the xonsh static
config file. Xonsh will automatically ask you if you want to run this
wizard if the configuration file does not exist. However, you can
always rerun this wizard with the xonfig command:

    $ xonfig wizard

This wizard will load an existing configuration, if it is available.
Also never fear when this wizard saves its results! It will create
a backup of any existing configuration automatically.

This wizard has two main phases: foreign shell setup and environment
variable setup. Each phase may be skipped in its entirety.

For the configuration to take effect, you will need to restart xonsh.

{hr}
""".format(
    hr=HR
)

WIZARD_FS = """
{hr}

                      {{BOLD_WHITE}}Foreign Shell Setup{{NO_COLOR}}
                      {{YELLOW}}-------------------{{NO_COLOR}}
The xonsh shell has the ability to interface with foreign shells such
as Bash, or zsh (fish not yet implemented).

For configuration, this means that xonsh can load the environment,
aliases, and functions specified in the config files of these shells.
Naturally, these shells must be available on the system to work.
Being able to share configuration (and source) from foreign shells
makes it easier to transition to and from xonsh.
""".format(
    hr=HR
)

WIZARD_ENV = """
{hr}

                  {{BOLD_WHITE}}Environment Variable Setup{{NO_COLOR}}
                  {{YELLOW}}--------------------------{{NO_COLOR}}
The xonsh shell also allows you to setup environment variables from
the static configuration file. Any variables set in this way are
superseded by the definitions in the xonshrc or on the command line.
Still, setting environment variables in this way can help define
options that are global to the system or user.

The following lists the environment variable name, its documentation,
the default value, and the current value. The default and current
values are presented as pretty repr strings of their Python types.

{{BOLD_GREEN}}Note:{{NO_COLOR}} Simply hitting enter for any environment variable
will accept the default value for that entry.
""".format(
    hr=HR
)

WIZARD_ENV_QUESTION = "Would you like to set env vars now, " + wiz.YN

WIZARD_XONTRIB = """
{hr}

                           {{BOLD_WHITE}}Xontribs{{NO_COLOR}}
                           {{YELLOW}}--------{{NO_COLOR}}
No shell is complete without extensions, and xonsh is no exception. Xonsh
extensions are called {{BOLD_GREEN}}xontribs{{NO_COLOR}}, or xonsh contributions.
Xontribs are dynamically loadable, either by importing them directly or by
using the 'xontrib' command. However, you can also configure xonsh to load
xontribs automatically on startup prior to loading the run control files.
This allows the xontrib to be used immediately in your xonshrc files.

The following describes all xontribs that have been registered with xonsh.
These come from users, 3rd party developers, or xonsh itself!
""".format(
    hr=HR
)

WIZARD_XONTRIB_QUESTION = "Would you like to enable xontribs now, " + wiz.YN

WIZARD_TAIL = """
Thanks for using the xonsh configuration wizard!"""


_XONFIG_SOURCE_FOREIGN_SHELL_COMMAND = collections.defaultdict(
    lambda: "source-foreign", bash="source-bash", cmd="source-cmd", zsh="source-zsh"
)


def _dump_xonfig_foreign_shell(path, value):
    shell = value["shell"]
    shell = CANON_SHELL_NAMES.get(shell, shell)
    cmd = [_XONFIG_SOURCE_FOREIGN_SHELL_COMMAND[shell]]
    interactive = value.get("interactive", None)
    if interactive is not None:
        cmd.extend(["--interactive", str(interactive)])
    login = value.get("login", None)
    if login is not None:
        cmd.extend(["--login", str(login)])
    envcmd = value.get("envcmd", None)
    if envcmd is not None:
        cmd.extend(["--envcmd", envcmd])
    aliascmd = value.get("aliasmd", None)
    if aliascmd is not None:
        cmd.extend(["--aliascmd", aliascmd])
    extra_args = value.get("extra_args", None)
    if extra_args:
        cmd.extend(["--extra-args", repr(" ".join(extra_args))])
    safe = value.get("safe", None)
    if safe is not None:
        cmd.extend(["--safe", str(safe)])
    prevcmd = value.get("prevcmd", "")
    if prevcmd:
        cmd.extend(["--prevcmd", repr(prevcmd)])
    postcmd = value.get("postcmd", "")
    if postcmd:
        cmd.extend(["--postcmd", repr(postcmd)])
    funcscmd = value.get("funcscmd", None)
    if funcscmd:
        cmd.extend(["--funcscmd", repr(funcscmd)])
    sourcer = value.get("sourcer", None)
    if sourcer:
        cmd.extend(["--sourcer", sourcer])
    if cmd[0] == "source-foreign":
        cmd.append(shell)
    cmd.append('"echo loading xonsh foreign shell"')
    return " ".join(cmd)


def _dump_xonfig_env(path, value):
    name = os.path.basename(path.rstrip("/"))
    ensurer = builtins.__xonsh__.env.get_ensurer(name)
    dval = ensurer.detype(value)
    return "${name} = {val!r}".format(name=name, val=dval)


def _dump_xonfig_xontribs(path, value):
    return "xontrib load {0}".format(" ".join(value))


@lazyobject
def XONFIG_DUMP_RULES():
    return {
        "/": None,
        "/env/": None,
        "/foreign_shells/*/": _dump_xonfig_foreign_shell,
        "/env/*": _dump_xonfig_env,
        "/env/*/[0-9]*": None,
        "/xontribs/": _dump_xonfig_xontribs,
    }


def make_fs_wiz():
    """Makes the foreign shell part of the wizard."""
    cond = wiz.create_truefalse_cond(prompt="Add a new foreign shell, " + wiz.YN)
    fs = wiz.While(
        cond=cond,
        body=[
            wiz.Input("shell name (e.g. bash): ", path="/foreign_shells/{idx}/shell"),
            wiz.StoreNonEmpty(
                "interactive shell [bool, default=True]: ",
                converter=to_bool,
                show_conversion=True,
                path="/foreign_shells/{idx}/interactive",
            ),
            wiz.StoreNonEmpty(
                "login shell [bool, default=False]: ",
                converter=to_bool,
                show_conversion=True,
                path="/foreign_shells/{idx}/login",
            ),
            wiz.StoreNonEmpty(
                "env command [str, default='env']: ",
                path="/foreign_shells/{idx}/envcmd",
            ),
            wiz.StoreNonEmpty(
                "alias command [str, default='alias']: ",
                path="/foreign_shells/{idx}/aliascmd",
            ),
            wiz.StoreNonEmpty(
                ("extra command line arguments [list of str, " "default=[]]: "),
                converter=ast.literal_eval,
                show_conversion=True,
                path="/foreign_shells/{idx}/extra_args",
            ),
            wiz.StoreNonEmpty(
                "safely handle exceptions [bool, default=True]: ",
                converter=to_bool,
                show_conversion=True,
                path="/foreign_shells/{idx}/safe",
            ),
            wiz.StoreNonEmpty(
                "pre-command [str, default='']: ", path="/foreign_shells/{idx}/prevcmd"
            ),
            wiz.StoreNonEmpty(
                "post-command [str, default='']: ", path="/foreign_shells/{idx}/postcmd"
            ),
            wiz.StoreNonEmpty(
                "foreign function command [str, default=None]: ",
                path="/foreign_shells/{idx}/funcscmd",
            ),
            wiz.StoreNonEmpty(
                "source command [str, default=None]: ",
                path="/foreign_shells/{idx}/sourcer",
            ),
            wiz.Message(message="Foreign shell added.\n"),
        ],
    )
    return fs


def _wrap_paragraphs(text, width=70, **kwargs):
    """Wraps paragraphs instead."""
    pars = text.split("\n")
    pars = ["\n".join(textwrap.wrap(p, width=width, **kwargs)) for p in pars]
    s = "\n".join(pars)
    return s


ENVVAR_MESSAGE = """
{{BOLD_CYAN}}${name}{{NO_COLOR}}
{docstr}
{{RED}}default value:{{NO_COLOR}} {default}
{{RED}}current value:{{NO_COLOR}} {current}"""

ENVVAR_PROMPT = "{BOLD_GREEN}>>>{NO_COLOR} "


def make_exit_message():
    """Creates a message for how to exit the wizard."""
    shell_type = builtins.__xonsh__.shell.shell_type
    keyseq = "Ctrl-D" if shell_type == "readline" else "Ctrl-C"
    msg = "To exit the wizard at any time, press {BOLD_UNDERLINE_CYAN}"
    msg += keyseq + "{NO_COLOR}.\n"
    m = wiz.Message(message=msg)
    return m


def make_envvar(name):
    """Makes a StoreNonEmpty node for an environment variable."""
    env = builtins.__xonsh__.env
    vd = env.get_docs(name)
    if not vd.configurable:
        return
    default = vd.default
    if "\n" in default:
        default = "\n" + _wrap_paragraphs(default, width=69)
    curr = env.get(name)
    if is_string(curr) and is_template_string(curr):
        curr = curr.replace("{", "{{").replace("}", "}}")
    curr = pprint.pformat(curr, width=69)
    if "\n" in curr:
        curr = "\n" + curr
    msg = ENVVAR_MESSAGE.format(
        name=name,
        default=default,
        current=curr,
        docstr=_wrap_paragraphs(vd.docstr, width=69),
    )
    mnode = wiz.Message(message=msg)
    ens = env.get_ensurer(name)
    path = "/env/" + name
    pnode = wiz.StoreNonEmpty(
        ENVVAR_PROMPT,
        converter=ens.convert,
        show_conversion=True,
        path=path,
        retry=True,
        store_raw=vd.store_as_str,
    )
    return mnode, pnode


def _make_flat_wiz(kidfunc, *args):
    kids = map(kidfunc, *args)
    flatkids = []
    for k in kids:
        if k is None:
            continue
        flatkids.extend(k)
    wizard = wiz.Wizard(children=flatkids)
    return wizard


def make_env_wiz():
    """Makes an environment variable wizard."""
    w = _make_flat_wiz(make_envvar, sorted(builtins.__xonsh__.env._docs.keys()))
    return w


XONTRIB_PROMPT = "{BOLD_GREEN}Add this xontrib{NO_COLOR}, " + wiz.YN


def _xontrib_path(visitor=None, node=None, val=None):
    # need this to append only based on user-selected size
    return ("xontribs", len(visitor.state.get("xontribs", ())))


def make_xontrib(xontrib, package):
    """Makes a message and StoreNonEmpty node for a xontrib."""
    name = xontrib.get("name", "<unknown-xontrib-name>")
    msg = "\n{BOLD_CYAN}" + name + "{NO_COLOR}\n"
    if "url" in xontrib:
        msg += "{RED}url:{NO_COLOR} " + xontrib["url"] + "\n"
    if "package" in xontrib:
        msg += "{RED}package:{NO_COLOR} " + xontrib["package"] + "\n"
    if "url" in package:
        if "url" in xontrib and package["url"] != xontrib["url"]:
            msg += "{RED}package-url:{NO_COLOR} " + package["url"] + "\n"
    if "license" in package:
        msg += "{RED}license:{NO_COLOR} " + package["license"] + "\n"
    msg += "{PURPLE}installed?{NO_COLOR} "
    msg += ("no" if find_xontrib(name) is None else "yes") + "\n"
    desc = xontrib.get("description", "")
    if not isinstance(desc, str):
        desc = "".join(desc)
    msg += _wrap_paragraphs(desc, width=69)
    if msg.endswith("\n"):
        msg = msg[:-1]
    mnode = wiz.Message(message=msg)
    convert = lambda x: name if to_bool(x) else wiz.Unstorable
    pnode = wiz.StoreNonEmpty(XONTRIB_PROMPT, converter=convert, path=_xontrib_path)
    return mnode, pnode


def make_xontribs_wiz():
    """Makes a xontrib wizard."""
    md = xontrib_metadata()
    pkgs = [md["packages"].get(d.get("package", None), {}) for d in md["xontribs"]]
    w = _make_flat_wiz(make_xontrib, md["xontribs"], pkgs)
    return w


def make_xonfig_wizard(default_file=None, confirm=False, no_wizard_file=None):
    """Makes a configuration wizard for xonsh config file.

    Parameters
    ----------
    default_file : str, optional
        Default filename to save and load to. User will still be prompted.
    confirm : bool, optional
        Confirm that the main part of the wizard should be run.
    no_wizard_file : str, optional
        Filename for that will flag to future runs that the wizard should not be
        run again. If None (default), this defaults to default_file.
    """
    w = wiz.Wizard(
        children=[
            wiz.Message(message=WIZARD_HEAD),
            make_exit_message(),
            wiz.Message(message=WIZARD_FS),
            make_fs_wiz(),
            wiz.Message(message=WIZARD_ENV),
            wiz.YesNo(question=WIZARD_ENV_QUESTION, yes=make_env_wiz(), no=wiz.Pass()),
            wiz.Message(message=WIZARD_XONTRIB),
            wiz.YesNo(
                question=WIZARD_XONTRIB_QUESTION, yes=make_xontribs_wiz(), no=wiz.Pass()
            ),
            wiz.Message(message="\n" + HR + "\n"),
            wiz.FileInserter(
                prefix="# XONSH WIZARD START",
                suffix="# XONSH WIZARD END",
                dump_rules=XONFIG_DUMP_RULES,
                default_file=default_file,
                check=True,
            ),
            wiz.Message(message=WIZARD_TAIL),
        ]
    )
    if confirm:
        q = (
            "Would you like to run the xonsh configuration wizard now?\n\n"
            "1. Yes (You can abort at any time)\n"
            "2. No, but ask me next time.\n"
            "3. No, and don't ask me again.\n\n"
            "1, 2, or 3 [default: 2]? "
        )
        no_wizard_file = default_file if no_wizard_file is None else no_wizard_file
        passer = wiz.Pass()
        saver = wiz.SaveJSON(
            check=False, ask_filename=False, default_file=no_wizard_file
        )
        w = wiz.Question(
            q, {1: w, 2: passer, 3: saver}, converter=lambda x: int(x) if x != "" else 2
        )
    return w


def _wizard(ns):
    env = builtins.__xonsh__.env
    shell = builtins.__xonsh__.shell.shell
    fname = env.get("XONSHRC")[-1] if ns.file is None else ns.file
    no_wiz = os.path.join(env.get("XONSH_CONFIG_DIR"), "no-wizard")
    w = make_xonfig_wizard(
        default_file=fname, confirm=ns.confirm, no_wizard_file=no_wiz
    )
    tempenv = {"PROMPT": "", "XONSH_STORE_STDOUT": False}
    pv = wiz.PromptVisitor(w, store_in_history=False, multiline=False)

    @contextlib.contextmanager
    def force_hide():
        if env.get("XONSH_STORE_STDOUT") and hasattr(shell, "_force_hide"):
            orig, shell._force_hide = shell._force_hide, False
            yield
            shell._force_hide = orig
        else:
            yield

    with force_hide(), env.swap(tempenv):
        try:
            pv.visit()
        except (KeyboardInterrupt, Exception):
            print()
            print_exception()


def _xonfig_format_human(data):
    wcol1 = wcol2 = 0
    for key, val in data:
        wcol1 = max(wcol1, len(key))
        wcol2 = max(wcol2, len(str(val)))
    hr = "+" + ("-" * (wcol1 + 2)) + "+" + ("-" * (wcol2 + 2)) + "+\n"
    row = "| {key!s:<{wcol1}} | {val!s:<{wcol2}} |\n"
    s = hr
    for key, val in data:
        s += row.format(key=key, wcol1=wcol1, val=val, wcol2=wcol2)
    s += hr
    return s


def _xonfig_format_json(data):
    data = {k.replace(" ", "_"): v for k, v in data}
    s = json.dumps(data, sort_keys=True, indent=1) + "\n"
    return s


def _info(ns):
    env = builtins.__xonsh__.env
    try:
        ply.__version__ = ply.__version__
    except AttributeError:
        ply.__version__ = "3.8"
    data = [("xonsh", XONSH_VERSION)]
    hash_, date_ = githash()
    if hash_:
        data.append(("Git SHA", hash_))
        data.append(("Commit Date", date_))
    data.extend(
        [
            ("Python", "{}.{}.{}".format(*PYTHON_VERSION_INFO)),
            ("PLY", ply.__version__),
            ("have readline", is_readline_available()),
            ("prompt toolkit", ptk_version() or None),
            ("shell type", env.get("SHELL_TYPE")),
            ("pygments", pygments_version()),
            ("on posix", bool(ON_POSIX)),
            ("on linux", bool(ON_LINUX)),
        ]
    )
    if ON_LINUX:
        data.append(("distro", linux_distro()))
    data.extend(
        [
            ("on darwin", ON_DARWIN),
            ("on windows", ON_WINDOWS),
            ("on cygwin", ON_CYGWIN),
            ("on msys2", ON_MSYS),
            ("is superuser", is_superuser()),
            ("default encoding", DEFAULT_ENCODING),
            ("xonsh encoding", env.get("XONSH_ENCODING")),
            ("encoding errors", env.get("XONSH_ENCODING_ERRORS")),
        ]
    )
    formatter = _xonfig_format_json if ns.json else _xonfig_format_human
    s = formatter(data)
    return s


def _styles(ns):
    env = builtins.__xonsh__.env
    curr = env.get("XONSH_COLOR_STYLE")
    styles = sorted(color_style_names())
    if ns.json:
        s = json.dumps(styles, sort_keys=True, indent=1)
        print(s)
        return
    lines = []
    for style in styles:
        if style == curr:
            lines.append("* {GREEN}" + style + "{NO_COLOR}")
        else:
            lines.append("  " + style)
    s = "\n".join(lines)
    print_color(s)


def _str_colors(cmap, cols):
    color_names = sorted(cmap.keys(), key=(lambda s: (len(s), s)))
    grper = lambda s: min(cols // (len(s) + 1), 8)
    lines = []
    for n, group in itertools.groupby(color_names, key=grper):
        width = cols // n
        line = ""
        for i, name in enumerate(group):
            buf = " " * (width - len(name))
            line += "{" + name + "}" + name + "{NO_COLOR}" + buf
            if (i + 1) % n == 0:
                lines.append(line)
                line = ""
        if len(line) != 0:
            lines.append(line)
    return "\n".join(lines)


def _tok_colors(cmap, cols):
    from xonsh.style_tools import Color

    nc = Color.NO_COLOR
    names_toks = {}
    for t in cmap.keys():
        name = str(t)
        if name.startswith("Token.Color."):
            _, _, name = name.rpartition(".")
        names_toks[name] = t
    color_names = sorted(names_toks.keys(), key=(lambda s: (len(s), s)))
    grper = lambda s: min(cols // (len(s) + 1), 8)
    toks = []
    for n, group in itertools.groupby(color_names, key=grper):
        width = cols // n
        for i, name in enumerate(group):
            toks.append((names_toks[name], name))
            buf = " " * (width - len(name))
            if (i + 1) % n == 0:
                buf += "\n"
            toks.append((nc, buf))
        if not toks[-1][1].endswith("\n"):
            toks[-1] = (nc, toks[-1][1] + "\n")
    return toks


def _colors(args):
    columns, _ = shutil.get_terminal_size()
    columns -= int(ON_WINDOWS)
    style_stash = builtins.__xonsh__.env["XONSH_COLOR_STYLE"]

    if args.style is not None:
        if args.style not in color_style_names():
            print("Invalid style: {}".format(args.style))
            return
        builtins.__xonsh__.env["XONSH_COLOR_STYLE"] = args.style

    color_map = color_style()
    akey = next(iter(color_map))
    if isinstance(akey, str):
        s = _str_colors(color_map, columns)
    else:
        s = _tok_colors(color_map, columns)
    print_color(s)
    builtins.__xonsh__.env["XONSH_COLOR_STYLE"] = style_stash


def _tutorial(args):
    import webbrowser

    webbrowser.open("http://xon.sh/tutorial.html")


@functools.lru_cache(1)
def _xonfig_create_parser():
    p = argparse.ArgumentParser(
        prog="xonfig", description="Manages xonsh configuration."
    )
    subp = p.add_subparsers(title="action", dest="action")
    info = subp.add_parser(
        "info", help=("displays configuration information, " "default action")
    )
    info.add_argument(
        "--json", action="store_true", default=False, help="reports results as json"
    )
    wiz = subp.add_parser("wizard", help="displays configuration information")
    wiz.add_argument(
        "--file", default=None, help="config file location, default=$XONSHRC"
    )
    wiz.add_argument(
        "--confirm",
        action="store_true",
        default=False,
        help="confirm that the wizard should be run.",
    )
    sty = subp.add_parser("styles", help="prints available xonsh color styles")
    sty.add_argument(
        "--json", action="store_true", default=False, help="reports results as json"
    )
    colors = subp.add_parser("colors", help="preview color style")
    colors.add_argument(
        "style", nargs="?", default=None, help="style to preview, default: <current>"
    )
    subp.add_parser("tutorial", help="Launch tutorial in browser.")
    return p


_XONFIG_MAIN_ACTIONS = {
    "info": _info,
    "wizard": _wizard,
    "styles": _styles,
    "colors": _colors,
    "tutorial": _tutorial,
}


def xonfig_main(args=None):
    """Main xonfig entry point."""
    if not args or (
        args[0] not in _XONFIG_MAIN_ACTIONS and args[0] not in {"-h", "--help"}
    ):
        args.insert(0, "info")
    parser = _xonfig_create_parser()
    ns = parser.parse_args(args)
    if ns.action is None:  # apply default action
        ns = parser.parse_args(["info"] + args)
    return _XONFIG_MAIN_ACTIONS[ns.action](ns)


@lazyobject
def STRIP_COLOR_RE():
    return re.compile("{.*?}")


def _align_string(string, align="<", fill=" ", width=80):
    """ Align and pad a color formatted string """
    linelen = len(STRIP_COLOR_RE.sub("", string))
    padlen = max(width - linelen, 0)
    if align == "^":
        return fill * (padlen // 2) + string + fill * (padlen // 2 + padlen % 2)
    elif align == ">":
        return fill * padlen + string
    elif align == "<":
        return string + fill * padlen
    else:
        return string


@lazyobject
def TAGLINES():
    return [
        "Exofrills in the shell",
        "No frills in the shell",
        "Become the Lord of the Files",
        "Break out of your shell",
        "The only shell that is also a shell",
        "All that is and all that shell be",
        "It cannot be that hard",
        "Pass the xonsh, Piggy",
        "Piggy glanced nervously into hell and cradled the xonsh",
        "The xonsh is a symbol",
        "It is pronounced conch",
        "The shell, bourne again",
        "Snailed it",
        "Starfish loves you",
        "Come snail away",
        "This is Major Tom to Ground Xonshtrol",
        "Sally sells csh and keeps xonsh to herself",
        "Nice indeed. Everything's accounted for, except your old shell.",
        "I wanna thank you for putting me back in my snail shell",
        "Crustaceanly Yours",
        "With great shell comes great reproducibility",
        "None shell pass",
        "You shell not pass!",
        "The x-on shell",
        "Ever wonder why there isn't a Taco Shell? Because it is a corny idea.",
        "The carcolh will catch you!",
        "People xonshtantly mispronounce these things",
        "WHAT...is your favorite shell?",
        "Conches for the xonsh god!",
        "Python-powered, cross-platform, Unix-gazing shell",
        "Tab completion in Alderaan places",
        "This fix was trickier than expected",
        "The unholy cross of Bash/Python",
    ]


# list of strings or tuples (string, align, fill)
WELCOME_MSG = [
    "",
    ("{{INTENSE_WHITE}}Welcome to the xonsh shell ({version}){{NO_COLOR}}", "^", " "),
    "",
    ("{{INTENSE_RED}}~{{NO_COLOR}} {tagline} {{INTENSE_RED}}~{{NO_COLOR}}", "^", " "),
    "",
    ("{{INTENSE_BLACK}}", "<", "-"),
    "{{GREEN}}xonfig{{NO_COLOR}} tutorial    {{INTENSE_WHITE}}->    Launch the tutorial in "
    "the browser{{NO_COLOR}}",
    "{{GREEN}}xonfig{{NO_COLOR}} wizard      {{INTENSE_WHITE}}->    Run the configuration "
    "wizard and claim your shell {{NO_COLOR}}",
    "{{INTENSE_BLACK}}(Note: Run the Wizard or create a {{RED}}~/.xonshrc{{INTENSE_BLACK}} file "
    "to suppress the welcome screen)",
    "",
]


def print_welcome_screen():
    subst = dict(tagline=random.choice(list(TAGLINES)), version=XONSH_VERSION)
    for elem in WELCOME_MSG:
        if isinstance(elem, str):
            elem = (elem, "", "")
        line = elem[0].format(**subst)
        termwidth = os.get_terminal_size().columns
        line = _align_string(line, elem[1], elem[2], width=termwidth)
        print_color(line)

#
# base_shell
#
# -*- coding: utf-8 -*-
"""The base class for xonsh shell"""
# amalgamated io
# amalgamated os
# amalgamated sys
# amalgamated time
# amalgamated builtins
# amalgamated xonsh.tools
# amalgamated xonsh.platform
# amalgamated xonsh.codecache
# amalgamated xonsh.completer
from xonsh.prompt.base import multiline_prompt, PromptFormatter
# amalgamated xonsh.events
# amalgamated xonsh.shell
# amalgamated xonsh.lazyimps
# amalgamated xonsh.ansi_colors
if ON_WINDOWS:
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleTitleW.argtypes = [ctypes.c_wchar_p]


class _TeeStdBuf(io.RawIOBase):
    """A dispatcher for bytes to two buffers, as std stream buffer and an
    in memory buffer.
    """

    def __init__(
        self, stdbuf, membuf, encoding=None, errors=None, prestd=b"", poststd=b""
    ):
        """
        Parameters
        ----------
        stdbuf : BytesIO-like or StringIO-like
            The std stream buffer.
        membuf : BytesIO-like
            The in memory stream buffer.
        encoding : str or None, optional
            The encoding of the stream. Only used if stdbuf is a text stream,
            rather than a binary one. Defaults to $XONSH_ENCODING if None.
        errors : str or None, optional
            The error form for the encoding of the stream. Only used if stdbuf
            is a text stream, rather than a binary one. Deafults to
            $XONSH_ENCODING_ERRORS if None.
        prestd : bytes, optional
            The prefix to prepend to the standard buffer.
        poststd : bytes, optional
            The postfix to append to the standard buffer.
        """
        self.stdbuf = stdbuf
        self.membuf = membuf
        env = builtins.__xonsh__.env
        self.encoding = env.get("XONSH_ENCODING") if encoding is None else encoding
        self.errors = env.get("XONSH_ENCODING_ERRORS") if errors is None else errors
        self.prestd = prestd
        self.poststd = poststd
        self._std_is_binary = not hasattr(stdbuf, "encoding")

    def fileno(self):
        """Returns the file descriptor of the std buffer."""
        return self.stdbuf.fileno()

    def seek(self, offset, whence=io.SEEK_SET):
        """Sets the location in both the stdbuf and the membuf."""
        self.stdbuf.seek(offset, whence)
        self.membuf.seek(offset, whence)

    def truncate(self, size=None):
        """Truncate both buffers."""
        self.stdbuf.truncate(size)
        self.membuf.truncate(size)

    def readinto(self, b):
        """Read bytes into buffer from both streams."""
        if self._std_is_binary:
            self.stdbuf.readinto(b)
        return self.membuf.readinto(b)

    def write(self, b):
        """Write bytes into both buffers."""
        std_b = b
        if self.prestd:
            std_b = self.prestd + b
        if self.poststd:
            std_b += self.poststd
        # write to stdbuf
        if self._std_is_binary:
            self.stdbuf.write(std_b)
        else:
            self.stdbuf.write(std_b.decode(encoding=self.encoding, errors=self.errors))
        return self.membuf.write(b)


class _TeeStd(io.TextIOBase):
    """Tees a std stream into an in-memory container and the original stream."""

    def __init__(self, name, mem, prestd="", poststd=""):
        """
        Parameters
        ----------
        name : str
            The name of the buffer in the sys module, e.g. 'stdout'.
        mem : io.TextIOBase-like
            The in-memory text-based representation.
        prestd : str, optional
            The prefix to prepend to the standard stream.
        poststd : str, optional
            The postfix to append to the standard stream.
        """
        self._name = name
        self.std = std = getattr(sys, name)
        self.mem = mem
        self.prestd = prestd
        self.poststd = poststd
        preb = prestd.encode(encoding=mem.encoding, errors=mem.errors)
        postb = poststd.encode(encoding=mem.encoding, errors=mem.errors)
        if hasattr(std, "buffer"):
            buffer = _TeeStdBuf(std.buffer, mem.buffer, prestd=preb, poststd=postb)
        else:
            # TextIO does not have buffer as part of the API, so std streams
            # may not either.
            buffer = _TeeStdBuf(
                std,
                mem.buffer,
                encoding=mem.encoding,
                errors=mem.errors,
                prestd=preb,
                poststd=postb,
            )
        self.buffer = buffer
        setattr(sys, name, self)

    @property
    def encoding(self):
        """The encoding of the in-memory buffer."""
        return self.mem.encoding

    @property
    def errors(self):
        """The errors of the in-memory buffer."""
        return self.mem.errors

    @property
    def newlines(self):
        """The newlines of the in-memory buffer."""
        return self.mem.newlines

    def _replace_std(self):
        std = self.std
        if std is None:
            return
        setattr(sys, self._name, std)
        self.std = self._name = None

    def __del__(self):
        self._replace_std()

    def close(self):
        """Restores the original std stream."""
        self._replace_std()

    def write(self, s):
        """Writes data to the original std stream and the in-memory object."""
        self.mem.write(s)
        if self.std is None:
            return
        std_s = s
        if self.prestd:
            std_s = self.prestd + std_s
        if self.poststd:
            std_s += self.poststd
        self.std.write(std_s)

    def flush(self):
        """Flushes both the original stdout and the buffer."""
        self.std.flush()
        self.mem.flush()

    def fileno(self):
        """Tunnel fileno() calls to the std stream."""
        return self.std.fileno()

    def seek(self, offset, whence=io.SEEK_SET):
        """Seek to a location in both streams."""
        self.std.seek(offset, whence)
        self.mem.seek(offset, whence)

    def truncate(self, size=None):
        """Seek to a location in both streams."""
        self.std.truncate(size)
        self.mem.truncate(size)

    def detach(self):
        """This operation is not supported."""
        raise io.UnsupportedOperation

    def read(self, size=None):
        """Read from the in-memory stream and seek to a new location in the
        std stream.
        """
        s = self.mem.read(size)
        loc = self.std.tell()
        self.std.seek(loc + len(s))
        return s

    def readline(self, size=-1):
        """Read a line from the in-memory stream and seek to a new location
        in the std stream.
        """
        s = self.mem.readline(size)
        loc = self.std.tell()
        self.std.seek(loc + len(s))
        return s


class Tee:
    """Class that merges tee'd stdout and stderr into a single stream.

    This represents what a user would actually see on the command line.
    This class has the same interface as io.TextIOWrapper, except that
    the buffer is optional.
    """

    # pylint is a stupid about counting public methods when using inheritance.
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        buffer=None,
        encoding=None,
        errors=None,
        newline=None,
        line_buffering=False,
        write_through=False,
    ):
        self.buffer = io.BytesIO() if buffer is None else buffer
        self.memory = io.TextIOWrapper(
            self.buffer,
            encoding=encoding,
            errors=errors,
            newline=newline,
            line_buffering=line_buffering,
            write_through=write_through,
        )
        self.stdout = _TeeStd("stdout", self.memory)
        env = builtins.__xonsh__.env
        prestderr = format_std_prepost(env.get("XONSH_STDERR_PREFIX"))
        poststderr = format_std_prepost(env.get("XONSH_STDERR_POSTFIX"))
        self.stderr = _TeeStd(
            "stderr", self.memory, prestd=prestderr, poststd=poststderr
        )

    @property
    def line_buffering(self):
        return self.memory.line_buffering

    def __del__(self):
        del self.stdout, self.stderr
        self.stdout = self.stderr = None

    def close(self):
        """Closes the buffer as well as the stdout and stderr tees."""
        self.stdout.close()
        self.stderr.close()
        self.memory.close()

    def getvalue(self):
        """Gets the current contents of the in-memory buffer."""
        m = self.memory
        loc = m.tell()
        m.seek(0)
        s = m.read()
        m.seek(loc)
        return s


class BaseShell(object):
    """The xonsh shell."""

    def __init__(self, execer, ctx, **kwargs):
        super().__init__()
        self.execer = execer
        self.ctx = ctx
        self.completer = Completer() if kwargs.get("completer", True) else None
        self.buffer = []
        self.need_more_lines = False
        self.mlprompt = None
        self._styler = DefaultNotGiven
        self.prompt_formatter = PromptFormatter()
        self.accumulated_inputs = ""

    @property
    def styler(self):
        if self._styler is DefaultNotGiven:
            if HAS_PYGMENTS:
                from xonsh.pyghooks import XonshStyle

                env = builtins.__xonsh__.env
                self._styler = XonshStyle(env.get("XONSH_COLOR_STYLE"))
            else:
                self._styler = None
        return self._styler

    @styler.setter
    def styler(self, value):
        self._styler = value

    @styler.deleter
    def styler(self):
        self._styler = DefaultNotGiven

    def emptyline(self):
        """Called when an empty line has been entered."""
        self.need_more_lines = False
        self.default("")

    def singleline(self, **kwargs):
        """Reads a single line of input from the shell."""
        msg = "{0} has not implemented singleline()."
        raise RuntimeError(msg.format(self.__class__.__name__))

    def precmd(self, line):
        """Called just before execution of line."""
        return line if self.need_more_lines else line.lstrip()

    def default(self, line):
        """Implements code execution."""
        line = line if line.endswith("\n") else line + "\n"
        src, code = self.push(line)
        if code is None:
            return

        events.on_precommand.fire(cmd=src)

        env = builtins.__xonsh__.env
        hist = builtins.__xonsh__.history  # pylint: disable=no-member
        ts1 = None
        enc = env.get("XONSH_ENCODING")
        err = env.get("XONSH_ENCODING_ERRORS")
        tee = Tee(encoding=enc, errors=err)
        try:
            ts0 = time.time()
            run_compiled_code(code, self.ctx, None, "single")
            ts1 = time.time()
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 0  # returncode for success
        except XonshError as e:
            print(e.args[0], file=sys.stderr)
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 1  # return code for failure
        except Exception:  # pylint: disable=broad-except
            print_exception()
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 1  # return code for failure
        finally:
            ts1 = ts1 or time.time()
            tee_out = tee.getvalue()
            self._append_history(inp=src, ts=[ts0, ts1], tee_out=tee_out)
            self.accumulated_inputs += src
            if (
                tee_out
                and env.get("XONSH_APPEND_NEWLINE")
                and not tee_out.endswith(os.linesep)
            ):
                print(os.linesep, end="")
            tee.close()
            self._fix_cwd()
        if builtins.__xonsh__.exit:  # pylint: disable=no-member
            return True

    def _append_history(self, tee_out=None, **info):
        """Append information about the command to the history.

        This also handles on_postcommand because this is the place where all the
        information is available.
        """
        hist = builtins.__xonsh__.history  # pylint: disable=no-member
        info["rtn"] = hist.last_cmd_rtn if hist is not None else None
        tee_out = tee_out or None
        last_out = hist.last_cmd_out if hist is not None else None
        if last_out is None and tee_out is None:
            pass
        elif last_out is None and tee_out is not None:
            info["out"] = tee_out
        elif last_out is not None and tee_out is None:
            info["out"] = last_out
        else:
            info["out"] = tee_out + "\n" + last_out
        events.on_postcommand.fire(
            cmd=info["inp"], rtn=info["rtn"], out=info.get("out", None), ts=info["ts"]
        )
        if hist is not None:
            hist.append(info)
            hist.last_cmd_rtn = hist.last_cmd_out = None

    def _fix_cwd(self):
        """Check if the cwd changed out from under us."""
        env = builtins.__xonsh__.env
        try:
            cwd = os.getcwd()
        except (FileNotFoundError, OSError):
            cwd = None
        if cwd is None:
            # directory has been deleted out from under us, most likely
            pwd = env.get("PWD", None)
            if pwd is None:
                # we have no idea where we are
                env["PWD"] = "<invalid directory>"
            elif os.path.isdir(pwd):
                # unclear why os.getcwd() failed. do nothing.
                pass
            else:
                # OK PWD is really gone.
                msg = "{UNDERLINE_INTENSE_WHITE}{BACKGROUND_INTENSE_BLACK}"
                msg += "xonsh: working directory does not exist: " + pwd
                msg += "{NO_COLOR}"
                self.print_color(msg, file=sys.stderr)
        elif "PWD" not in env:
            # $PWD is missing from env, recreate it
            env["PWD"] = cwd
        elif os.path.realpath(cwd) != os.path.realpath(env["PWD"]):
            # The working directory has changed without updating $PWD, fix this
            old = env["PWD"]
            env["PWD"] = cwd
            env["OLDPWD"] = old
            events.on_chdir.fire(olddir=old, newdir=cwd)

    def push(self, line):
        """Pushes a line onto the buffer and compiles the code in a way that
        enables multiline input.
        """
        self.buffer.append(line)
        if self.need_more_lines:
            return None, None
        src = "".join(self.buffer)
        src = transform_command(src)
        return self.compile(src)

    def compile(self, src):
        """Compiles source code and returns the (possibly modified) source and
        a valid code object.
        """
        _cache = should_use_cache(self.execer, "single")
        if _cache:
            codefname = code_cache_name(src)
            cachefname = get_cache_filename(codefname, code=True)
            usecache, code = code_cache_check(cachefname)
            if usecache:
                self.reset_buffer()
                return src, code
        lincont = get_line_continuation()
        if src.endswith(lincont + "\n"):
            self.need_more_lines = True
            return src, None
        try:
            code = self.execer.compile(src, mode="single", glbs=self.ctx, locs=None)
            if _cache:
                update_cache(code, cachefname)
            self.reset_buffer()
        except SyntaxError:
            partial_string_info = check_for_partial_string(src)
            in_partial_string = (
                partial_string_info[0] is not None and partial_string_info[1] is None
            )
            if (src == "\n" or src.endswith("\n\n")) and not in_partial_string:
                self.reset_buffer()
                print_exception()
                return src, None
            self.need_more_lines = True
            code = None
        except Exception:  # pylint: disable=broad-except
            self.reset_buffer()
            print_exception()
            code = None
        return src, code

    def reset_buffer(self):
        """Resets the line buffer."""
        self.buffer.clear()
        self.need_more_lines = False
        self.mlprompt = None

    def settitle(self):
        """Sets terminal title."""
        env = builtins.__xonsh__.env  # pylint: disable=no-member
        term = env.get("TERM", None)
        # Shells running in emacs sets TERM to "dumb" or "eterm-color".
        # Do not set title for these to avoid garbled prompt.
        if (term is None and not ON_WINDOWS) or term in [
            "dumb",
            "eterm-color",
            "linux",
        ]:
            return
        t = env.get("TITLE")
        if t is None:
            return
        t = self.prompt_formatter(t)
        if ON_WINDOWS and "ANSICON" not in env:
            kernel32.SetConsoleTitleW(t)
        else:
            with open(1, "wb", closefd=False) as f:
                # prevent xonsh from answering interactive questions
                # on the next command by writing the title
                f.write("\x1b]0;{0}\x07".format(t).encode())
                f.flush()

    @property
    def prompt(self):
        """Obtains the current prompt string."""
        if self.need_more_lines:
            if self.mlprompt is None:
                try:
                    self.mlprompt = multiline_prompt()
                except Exception:  # pylint: disable=broad-except
                    print_exception()
                    self.mlprompt = "<multiline prompt error> "
            return self.mlprompt
        env = builtins.__xonsh__.env  # pylint: disable=no-member
        p = env.get("PROMPT")
        try:
            p = self.prompt_formatter(p)
        except Exception:  # pylint: disable=broad-except
            print_exception()
        self.settitle()
        return p

    def format_color(self, string, hide=False, force_string=False, **kwargs):
        """Formats the colors in a string. ``BaseShell``'s default implementation
        of this method uses colors based on ANSI color codes.
        """
        style = builtins.__xonsh__.env.get("XONSH_COLOR_STYLE")
        return ansi_partial_color_format(string, hide=hide, style=style)

    def print_color(self, string, hide=False, **kwargs):
        """Prints a string in color. This base implementation's colors are based
        on ANSI color codes if a string was given as input. If a list of token
        pairs is given, it will color based on pygments, if available. If
        pygments is not available, it will print a colorless string.
        """
        if isinstance(string, str):
            s = self.format_color(string, hide=hide)
        elif HAS_PYGMENTS:
            # assume this is a list of (Token, str) tuples and format it
            env = builtins.__xonsh__.env
            self.styler.style_name = env.get("XONSH_COLOR_STYLE")
            style_proxy = pyghooks.xonsh_style_proxy(self.styler)
            formatter = pyghooks.XonshTerminal256Formatter(style=style_proxy)
            s = pygments.format(string, formatter).rstrip()
        else:
            # assume this is a list of (Token, str) tuples and remove color
            s = "".join([x for _, x in string])
        print(s, **kwargs)

    def color_style_names(self):
        """Returns an iterable of all available style names."""
        return ()

    def color_style(self):
        """Returns the current color map."""
        return {}

    def restore_tty_sanity(self):
        """An interface for resetting the TTY stdin mode. This is highly
        dependent on the shell backend. Also it is mostly optional since
        it only affects ^Z backgrounding behaviour.
        """
        pass

#
# environ
#
# -*- coding: utf-8 -*-
"""Environment for the xonsh shell."""
# amalgamated os
# amalgamated re
# amalgamated sys
# amalgamated pprint
# amalgamated textwrap
locale = _LazyModule.load('locale', 'locale')
# amalgamated builtins
# amalgamated warnings
# amalgamated contextlib
# amalgamated collections
# amalgamated collections.abc
from xonsh import __version__ as XONSH_VERSION
# amalgamated xonsh.lazyasd
# amalgamated xonsh.codecache
# amalgamated xonsh.dirstack
# amalgamated xonsh.events
# amalgamated xonsh.platform
# amalgamated xonsh.style_tools
# amalgamated xonsh.tools
prompt = _LazyModule.load('xonsh', 'xonsh.prompt.base', 'prompt')
events.doc(
    "on_envvar_new",
    """
on_envvar_new(name: str, value: Any) -> None

Fires after a new environment variable is created.
Note: Setting envvars inside the handler might
cause a recursion until the limit.
""",
)


events.doc(
    "on_envvar_change",
    """
on_envvar_change(name: str, oldvalue: Any, newvalue: Any) -> None

Fires after an environment variable is changed.
Note: Setting envvars inside the handler might
cause a recursion until the limit.
""",
)


@lazyobject
def HELP_TEMPLATE():
    return (
        "{{INTENSE_RED}}{envvar}{{NO_COLOR}}:\n\n"
        "{{INTENSE_YELLOW}}{docstr}{{NO_COLOR}}\n\n"
        "default: {{CYAN}}{default}{{NO_COLOR}}\n"
        "configurable: {{CYAN}}{configurable}{{NO_COLOR}}"
    )


@lazyobject
def LOCALE_CATS():
    lc = {
        "LC_CTYPE": locale.LC_CTYPE,
        "LC_COLLATE": locale.LC_COLLATE,
        "LC_NUMERIC": locale.LC_NUMERIC,
        "LC_MONETARY": locale.LC_MONETARY,
        "LC_TIME": locale.LC_TIME,
    }
    if hasattr(locale, "LC_MESSAGES"):
        lc["LC_MESSAGES"] = locale.LC_MESSAGES
    return lc


def locale_convert(key):
    """Creates a converter for a locale key."""

    def lc_converter(val):
        try:
            locale.setlocale(LOCALE_CATS[key], val)
            val = locale.setlocale(LOCALE_CATS[key])
        except (locale.Error, KeyError):
            msg = "Failed to set locale {0!r} to {1!r}".format(key, val)
            warnings.warn(msg, RuntimeWarning)
        return val

    return lc_converter


def to_debug(x):
    """Converts value using to_bool_or_int() and sets this value on as the
    execer's debug level.
    """
    val = to_bool_or_int(x)
    if (
        hasattr(builtins, "__xonsh__")
        and hasattr(builtins.__xonsh__, "execer")
        and builtins.__xonsh__.execer is not None
    ):
        builtins.__xonsh__.execer.debug_level = val
    return val


Ensurer = collections.namedtuple("Ensurer", ["validate", "convert", "detype"])
Ensurer.__doc__ = """Named tuples whose elements are functions that
represent environment variable validation, conversion, detyping.
"""


@lazyobject
def DEFAULT_ENSURERS():
    return {
        "AUTO_CD": (is_bool, to_bool, bool_to_str),
        "AUTO_PUSHD": (is_bool, to_bool, bool_to_str),
        "AUTO_SUGGEST": (is_bool, to_bool, bool_to_str),
        "AUTO_SUGGEST_IN_COMPLETIONS": (is_bool, to_bool, bool_to_str),
        "BASH_COMPLETIONS": (is_env_path, str_to_env_path, env_path_to_str),
        "CASE_SENSITIVE_COMPLETIONS": (is_bool, to_bool, bool_to_str),
        re.compile(r"\w*DIRS$"): (is_env_path, str_to_env_path, env_path_to_str),
        "COLOR_INPUT": (is_bool, to_bool, bool_to_str),
        "COLOR_RESULTS": (is_bool, to_bool, bool_to_str),
        "COMPLETIONS_BRACKETS": (is_bool, to_bool, bool_to_str),
        "COMPLETIONS_CONFIRM": (is_bool, to_bool, bool_to_str),
        "COMPLETIONS_DISPLAY": (
            is_completions_display_value,
            to_completions_display_value,
            str,
        ),
        "COMPLETIONS_MENU_ROWS": (is_int, int, str),
        "COMPLETION_QUERY_LIMIT": (is_int, int, str),
        "DIRSTACK_SIZE": (is_int, int, str),
        "DOTGLOB": (is_bool, to_bool, bool_to_str),
        "DYNAMIC_CWD_WIDTH": (
            is_dynamic_cwd_width,
            to_dynamic_cwd_tuple,
            dynamic_cwd_tuple_to_str,
        ),
        "DYNAMIC_CWD_ELISION_CHAR": (is_string, ensure_string, ensure_string),
        "EXPAND_ENV_VARS": (is_bool, to_bool, bool_to_str),
        "FORCE_POSIX_PATHS": (is_bool, to_bool, bool_to_str),
        "FOREIGN_ALIASES_SUPPRESS_SKIP_MESSAGE": (is_bool, to_bool, bool_to_str),
        "FOREIGN_ALIASES_OVERRIDE": (is_bool, to_bool, bool_to_str),
        "FUZZY_PATH_COMPLETION": (is_bool, to_bool, bool_to_str),
        "GLOB_SORTED": (is_bool, to_bool, bool_to_str),
        "HISTCONTROL": (is_string_set, csv_to_set, set_to_csv),
        "IGNOREEOF": (is_bool, to_bool, bool_to_str),
        "INTENSIFY_COLORS_ON_WIN": (
            always_false,
            intensify_colors_on_win_setter,
            bool_to_str,
        ),
        "LANG": (is_string, ensure_string, ensure_string),
        "LC_COLLATE": (always_false, locale_convert("LC_COLLATE"), ensure_string),
        "LC_CTYPE": (always_false, locale_convert("LC_CTYPE"), ensure_string),
        "LC_MESSAGES": (always_false, locale_convert("LC_MESSAGES"), ensure_string),
        "LC_MONETARY": (always_false, locale_convert("LC_MONETARY"), ensure_string),
        "LC_NUMERIC": (always_false, locale_convert("LC_NUMERIC"), ensure_string),
        "LC_TIME": (always_false, locale_convert("LC_TIME"), ensure_string),
        "LOADED_RC_FILES": (is_bool_seq, csv_to_bool_seq, bool_seq_to_csv),
        "MOUSE_SUPPORT": (is_bool, to_bool, bool_to_str),
        "MULTILINE_PROMPT": (is_string_or_callable, ensure_string, ensure_string),
        re.compile(r"\w*PATH$"): (is_env_path, str_to_env_path, env_path_to_str),
        "PATHEXT": (
            is_nonstring_seq_of_strings,
            pathsep_to_upper_seq,
            seq_to_upper_pathsep,
        ),
        "PRETTY_PRINT_RESULTS": (is_bool, to_bool, bool_to_str),
        "PROMPT": (is_string_or_callable, ensure_string, ensure_string),
        "PROMPT_TOOLKIT_COLOR_DEPTH": (
            always_false,
            ptk2_color_depth_setter,
            ensure_string,
        ),
        "PUSHD_MINUS": (is_bool, to_bool, bool_to_str),
        "PUSHD_SILENT": (is_bool, to_bool, bool_to_str),
        "PTK_STYLE_OVERRIDES": (is_str_str_dict, to_str_str_dict, dict_to_str),
        "RAISE_SUBPROC_ERROR": (is_bool, to_bool, bool_to_str),
        "RIGHT_PROMPT": (is_string_or_callable, ensure_string, ensure_string),
        "BOTTOM_TOOLBAR": (is_string_or_callable, ensure_string, ensure_string),
        "SUBSEQUENCE_PATH_COMPLETION": (is_bool, to_bool, bool_to_str),
        "SUGGEST_COMMANDS": (is_bool, to_bool, bool_to_str),
        "SUGGEST_MAX_NUM": (is_int, int, str),
        "SUGGEST_THRESHOLD": (is_int, int, str),
        "SUPPRESS_BRANCH_TIMEOUT_MESSAGE": (is_bool, to_bool, bool_to_str),
        "UPDATE_COMPLETIONS_ON_KEYPRESS": (is_bool, to_bool, bool_to_str),
        "UPDATE_OS_ENVIRON": (is_bool, to_bool, bool_to_str),
        "UPDATE_PROMPT_ON_KEYPRESS": (is_bool, to_bool, bool_to_str),
        "VC_BRANCH_TIMEOUT": (is_float, float, str),
        "VC_HG_SHOW_BRANCH": (is_bool, to_bool, bool_to_str),
        "VI_MODE": (is_bool, to_bool, bool_to_str),
        "VIRTUAL_ENV": (is_string, ensure_string, ensure_string),
        "WIN_UNICODE_CONSOLE": (always_false, setup_win_unicode_console, bool_to_str),
        "XONSHRC": (is_env_path, str_to_env_path, env_path_to_str),
        "XONSH_APPEND_NEWLINE": (is_bool, to_bool, bool_to_str),
        "XONSH_AUTOPAIR": (is_bool, to_bool, bool_to_str),
        "XONSH_CACHE_SCRIPTS": (is_bool, to_bool, bool_to_str),
        "XONSH_CACHE_EVERYTHING": (is_bool, to_bool, bool_to_str),
        "XONSH_COLOR_STYLE": (is_string, ensure_string, ensure_string),
        "XONSH_DEBUG": (always_false, to_debug, bool_or_int_to_str),
        "XONSH_ENCODING": (is_string, ensure_string, ensure_string),
        "XONSH_ENCODING_ERRORS": (is_string, ensure_string, ensure_string),
        "XONSH_HISTORY_BACKEND": (is_history_backend, to_itself, ensure_string),
        "XONSH_HISTORY_FILE": (is_string, ensure_string, ensure_string),
        "XONSH_HISTORY_MATCH_ANYWHERE": (is_bool, to_bool, bool_to_str),
        "XONSH_HISTORY_SIZE": (
            is_history_tuple,
            to_history_tuple,
            history_tuple_to_str,
        ),
        "XONSH_LOGIN": (is_bool, to_bool, bool_to_str),
        "XONSH_PROC_FREQUENCY": (is_float, float, str),
        "XONSH_SHOW_TRACEBACK": (is_bool, to_bool, bool_to_str),
        "XONSH_STDERR_PREFIX": (is_string, ensure_string, ensure_string),
        "XONSH_STDERR_POSTFIX": (is_string, ensure_string, ensure_string),
        "XONSH_STORE_STDOUT": (is_bool, to_bool, bool_to_str),
        "XONSH_STORE_STDIN": (is_bool, to_bool, bool_to_str),
        "XONSH_TRACEBACK_LOGFILE": (is_logfile_opt, to_logfile_opt, logfile_opt_to_str),
        "XONSH_DATETIME_FORMAT": (is_string, ensure_string, ensure_string),
    }


#
# Defaults
#
def default_value(f):
    """Decorator for making callable default values."""
    f._xonsh_callable_default = True
    return f


def is_callable_default(x):
    """Checks if a value is a callable default."""
    return callable(x) and getattr(x, "_xonsh_callable_default", False)


DEFAULT_TITLE = "{current_job:{} | }{user}@{hostname}: {cwd} | xonsh"


@default_value
def xonsh_data_dir(env):
    """Ensures and returns the $XONSH_DATA_DIR"""
    xdd = os.path.expanduser(os.path.join(env.get("XDG_DATA_HOME"), "xonsh"))
    os.makedirs(xdd, exist_ok=True)
    return xdd


@default_value
def xonsh_config_dir(env):
    """Ensures and returns the $XONSH_CONFIG_DIR"""
    xcd = os.path.expanduser(os.path.join(env.get("XDG_CONFIG_HOME"), "xonsh"))
    os.makedirs(xcd, exist_ok=True)
    return xcd


def xonshconfig(env):
    """Ensures and returns the $XONSHCONFIG"""
    xcd = env.get("XONSH_CONFIG_DIR")
    xc = os.path.join(xcd, "config.json")
    return xc


@default_value
def default_xonshrc(env):
    """Creates a new instance of the default xonshrc tuple."""
    xcdrc = os.path.join(xonsh_config_dir(env), "rc.xsh")
    if ON_WINDOWS:
        dxrc = (
            os.path.join(os_environ["ALLUSERSPROFILE"], "xonsh", "xonshrc"),
            xcdrc,
            os.path.expanduser("~/.xonshrc"),
        )
    else:
        dxrc = ("/etc/xonshrc", xcdrc, os.path.expanduser("~/.xonshrc"))
    # Check if old config file exists and issue warning
    old_config_filename = xonshconfig(env)
    if os.path.isfile(old_config_filename):
        print(
            "WARNING! old style configuration ("
            + old_config_filename
            + ") is no longer supported. "
            + "Please migrate to xonshrc."
        )
    return dxrc


@default_value
def xonsh_append_newline(env):
    """Appends a newline if we are in interactive mode"""
    return env.get("XONSH_INTERACTIVE", False)


# Default values should generally be immutable, that way if a user wants
# to set them they have to do a copy and write them to the environment.
# try to keep this sorted.
@lazyobject
def DEFAULT_VALUES():
    dv = {
        "AUTO_CD": False,
        "AUTO_PUSHD": False,
        "AUTO_SUGGEST": True,
        "AUTO_SUGGEST_IN_COMPLETIONS": False,
        "BASH_COMPLETIONS": BASH_COMPLETIONS_DEFAULT,
        "CASE_SENSITIVE_COMPLETIONS": ON_LINUX,
        "CDPATH": (),
        "COLOR_INPUT": True,
        "COLOR_RESULTS": True,
        "COMPLETIONS_BRACKETS": True,
        "COMPLETIONS_CONFIRM": False,
        "COMPLETIONS_DISPLAY": "multi",
        "COMPLETIONS_MENU_ROWS": 5,
        "COMPLETION_QUERY_LIMIT": 100,
        "DIRSTACK_SIZE": 20,
        "DOTGLOB": False,
        "DYNAMIC_CWD_WIDTH": (float("inf"), "c"),
        "DYNAMIC_CWD_ELISION_CHAR": "",
        "EXPAND_ENV_VARS": True,
        "FORCE_POSIX_PATHS": False,
        "FOREIGN_ALIASES_SUPPRESS_SKIP_MESSAGE": False,
        "FOREIGN_ALIASES_OVERRIDE": False,
        "PROMPT_FIELDS": dict(prompt.PROMPT_FIELDS),
        "FUZZY_PATH_COMPLETION": True,
        "GLOB_SORTED": True,
        "HISTCONTROL": set(),
        "IGNOREEOF": False,
        "INDENT": "    ",
        "INTENSIFY_COLORS_ON_WIN": True,
        "LANG": "C.UTF-8",
        "LC_CTYPE": locale.setlocale(locale.LC_CTYPE),
        "LC_COLLATE": locale.setlocale(locale.LC_COLLATE),
        "LC_TIME": locale.setlocale(locale.LC_TIME),
        "LC_MONETARY": locale.setlocale(locale.LC_MONETARY),
        "LC_NUMERIC": locale.setlocale(locale.LC_NUMERIC),
        "LOADED_RC_FILES": (),
        "MOUSE_SUPPORT": False,
        "MULTILINE_PROMPT": ".",
        "PATH": PATH_DEFAULT,
        "PATHEXT": [".COM", ".EXE", ".BAT", ".CMD"] if ON_WINDOWS else [],
        "PRETTY_PRINT_RESULTS": True,
        "PROMPT": prompt.default_prompt(),
        "PROMPT_TOOLKIT_COLOR_DEPTH": "",
        "PTK_STYLE_OVERRIDES": dict(PTK2_STYLE),
        "PUSHD_MINUS": False,
        "PUSHD_SILENT": False,
        "RAISE_SUBPROC_ERROR": False,
        "RIGHT_PROMPT": "",
        "BOTTOM_TOOLBAR": "",
        "SHELL_TYPE": "best",
        "SUBSEQUENCE_PATH_COMPLETION": True,
        "SUPPRESS_BRANCH_TIMEOUT_MESSAGE": False,
        "SUGGEST_COMMANDS": True,
        "SUGGEST_MAX_NUM": 5,
        "SUGGEST_THRESHOLD": 3,
        "TITLE": DEFAULT_TITLE,
        "UPDATE_COMPLETIONS_ON_KEYPRESS": False,
        "UPDATE_OS_ENVIRON": False,
        "UPDATE_PROMPT_ON_KEYPRESS": False,
        "VC_BRANCH_TIMEOUT": 0.2 if ON_WINDOWS else 0.1,
        "VC_HG_SHOW_BRANCH": True,
        "VI_MODE": False,
        "WIN_UNICODE_CONSOLE": True,
        "XDG_CONFIG_HOME": os.path.expanduser(os.path.join("~", ".config")),
        "XDG_DATA_HOME": os.path.expanduser(os.path.join("~", ".local", "share")),
        "XONSHRC": default_xonshrc,
        "XONSH_APPEND_NEWLINE": xonsh_append_newline,
        "XONSH_AUTOPAIR": False,
        "XONSH_CACHE_SCRIPTS": True,
        "XONSH_CACHE_EVERYTHING": False,
        "XONSH_COLOR_STYLE": "default",
        "XONSH_CONFIG_DIR": xonsh_config_dir,
        "XONSH_DATA_DIR": xonsh_data_dir,
        "XONSH_DEBUG": 0,
        "XONSH_ENCODING": DEFAULT_ENCODING,
        "XONSH_ENCODING_ERRORS": "surrogateescape",
        "XONSH_HISTORY_BACKEND": "json",
        "XONSH_HISTORY_FILE": os.path.expanduser("~/.xonsh_history.json"),
        "XONSH_HISTORY_MATCH_ANYWHERE": False,
        "XONSH_HISTORY_SIZE": (8128, "commands"),
        "XONSH_LOGIN": False,
        "XONSH_PROC_FREQUENCY": 1e-4,
        "XONSH_SHOW_TRACEBACK": False,
        "XONSH_STDERR_PREFIX": "",
        "XONSH_STDERR_POSTFIX": "",
        "XONSH_STORE_STDIN": False,
        "XONSH_STORE_STDOUT": False,
        "XONSH_TRACEBACK_LOGFILE": None,
        "XONSH_DATETIME_FORMAT": "%Y-%m-%d %H:%M",
    }
    if hasattr(locale, "LC_MESSAGES"):
        dv["LC_MESSAGES"] = locale.setlocale(locale.LC_MESSAGES)
    return dv


VarDocs = collections.namedtuple(
    "VarDocs", ["docstr", "configurable", "default", "store_as_str"]
)
VarDocs.__doc__ = """Named tuple for environment variable documentation

Parameters
----------
docstr : str
   The environment variable docstring.
configurable : bool, optional
    Flag for whether the environment variable is configurable or not.
default : str, optional
    Custom docstring for the default value for complex defaults.
    Is this is DefaultNotGiven, then the default will be looked up
    from DEFAULT_VALUES and converted to a str.
store_as_str : bool, optional
    Flag for whether the environment variable should be stored as a
    string. This is used when persisting a variable that is not JSON
    serializable to the config file. For example, sets, frozensets, and
    potentially other non-trivial data types. default, False.
"""
# iterates from back
VarDocs.__new__.__defaults__ = (True, DefaultNotGiven, False)


# Please keep the following in alphabetic order - scopatz
@lazyobject
def DEFAULT_DOCS():
    return {
        "ANSICON": VarDocs(
            "This is used on Windows to set the title, " "if available.",
            configurable=False,
        ),
        "AUTO_CD": VarDocs(
            "Flag to enable changing to a directory by entering the dirname or "
            "full path only (without the cd command)."
        ),
        "AUTO_PUSHD": VarDocs(
            "Flag for automatically pushing directories onto the directory stack."
        ),
        "AUTO_SUGGEST": VarDocs(
            "Enable automatic command suggestions based on history, like in the fish "
            "shell.\n\nPressing the right arrow key inserts the currently "
            "displayed suggestion. Only usable with ``$SHELL_TYPE=prompt_toolkit.``"
        ),
        "AUTO_SUGGEST_IN_COMPLETIONS": VarDocs(
            "Places the auto-suggest result as the first option in the completions. "
            "This enables you to tab complete the auto-suggestion."
        ),
        "BASH_COMPLETIONS": VarDocs(
            "This is a list (or tuple) of strings that specifies where the "
            "``bash_completion`` script may be found. "
            "The first valid path will be used. For better performance, "
            "bash-completion v2.x is recommended since it lazy-loads individual "
            "completion scripts. "
            "For both bash-completion v1.x and v2.x, paths of individual completion "
            "scripts (like ``.../completes/ssh``) do not need to be included here. "
            "The default values are platform "
            "dependent, but sane. To specify an alternate list, do so in the run "
            "control file.",
            default=(
                "Normally this is:\n\n"
                "    ``('/usr/share/bash-completion/bash_completion', )``\n\n"
                "But, on Mac it is:\n\n"
                "    ``('/usr/local/share/bash-completion/bash_completion', "
                "'/usr/local/etc/bash_completion')``\n\n"
                "Other OS-specific defaults may be added in the future."
            ),
        ),
        "CASE_SENSITIVE_COMPLETIONS": VarDocs(
            "Sets whether completions should be case sensitive or case " "insensitive.",
            default="True on Linux, False otherwise.",
        ),
        "CDPATH": VarDocs(
            "A list of paths to be used as roots for a cd, breaking compatibility "
            "with Bash, xonsh always prefer an existing relative path."
        ),
        "COLOR_INPUT": VarDocs("Flag for syntax highlighting interactive input."),
        "COLOR_RESULTS": VarDocs("Flag for syntax highlighting return values."),
        "COMPLETIONS_BRACKETS": VarDocs(
            "Flag to enable/disable inclusion of square brackets and parentheses "
            "in Python attribute completions.",
            default="True",
        ),
        "COMPLETIONS_DISPLAY": VarDocs(
            "Configure if and how Python completions are displayed by the "
            "``prompt_toolkit`` shell.\n\nThis option does not affect Bash "
            "completions, auto-suggestions, etc.\n\nChanging it at runtime will "
            "take immediate effect, so you can quickly disable and enable "
            "completions during shell sessions.\n\n"
            "- If ``$COMPLETIONS_DISPLAY`` is ``none`` or ``false``, do not display\n"
            "  those completions.\n"
            "- If ``$COMPLETIONS_DISPLAY`` is ``single``, display completions in a\n"
            "  single column while typing.\n"
            "- If ``$COMPLETIONS_DISPLAY`` is ``multi`` or ``true``, display completions\n"
            "  in multiple columns while typing.\n\n"
            "- If ``$COMPLETIONS_DISPLAY`` is ``readline``, display completions\n"
            "  will emulate the behavior of readline.\n\n"
            "These option values are not case- or type-sensitive, so e.g."
            "writing ``$COMPLETIONS_DISPLAY = None`` "
            "and ``$COMPLETIONS_DISPLAY = 'none'`` are equivalent. Only usable with "
            "``$SHELL_TYPE=prompt_toolkit``"
        ),
        "COMPLETIONS_CONFIRM": VarDocs(
            "While tab-completions menu is displayed, press <Enter> to confirm "
            "completion instead of running command. This only affects the "
            "prompt-toolkit shell."
        ),
        "COMPLETIONS_MENU_ROWS": VarDocs(
            "Number of rows to reserve for tab-completions menu if "
            "``$COMPLETIONS_DISPLAY`` is ``single`` or ``multi``. This only affects the "
            "prompt-toolkit shell."
        ),
        "COMPLETION_QUERY_LIMIT": VarDocs(
            "The number of completions to display before the user is asked "
            "for confirmation."
        ),
        "DIRSTACK_SIZE": VarDocs("Maximum size of the directory stack."),
        "DOTGLOB": VarDocs(
            'Globbing files with "*" or "**" will also match '
            "dotfiles, or those 'hidden' files whose names "
            "begin with a literal '.'. Such files are filtered "
            "out by default."
        ),
        "DYNAMIC_CWD_WIDTH": VarDocs(
            "Maximum length in number of characters "
            "or as a percentage for the ``cwd`` prompt variable. For example, "
            '"20" is a twenty character width and "10%" is ten percent of the '
            "number of columns available."
        ),
        "DYNAMIC_CWD_ELISION_CHAR": VarDocs(
            "The string used to show a shortened directory in a shortened cwd, "
            "e.g. ``'…'``."
        ),
        "EXPAND_ENV_VARS": VarDocs(
            "Toggles whether environment variables are expanded inside of strings "
            "in subprocess mode."
        ),
        "FORCE_POSIX_PATHS": VarDocs(
            "Forces forward slashes (``/``) on Windows systems when using auto "
            "completion if set to anything truthy.",
            configurable=ON_WINDOWS,
        ),
        "FOREIGN_ALIASES_SUPPRESS_SKIP_MESSAGE": VarDocs(
            "Whether or not foreign aliases should suppress the message "
            "that informs the user when a foreign alias has been skipped "
            "because it already exists in xonsh.",
            configurable=True,
        ),
        "FOREIGN_ALIASES_OVERRIDE": VarDocs(
            "Whether or not foreign aliases should override xonsh aliases "
            "with the same name. Note that setting of this must happen in the "
            "environment that xonsh was started from. "
            "It cannot be set in the ``.xonshrc`` as loading of foreign aliases happens before"
            "``.xonshrc`` is parsed",
            configurable=True,
        ),
        "PROMPT_FIELDS": VarDocs(
            "Dictionary containing variables to be used when formatting $PROMPT "
            "and $TITLE. See 'Customizing the Prompt' "
            "http://xon.sh/tutorial.html#customizing-the-prompt",
            configurable=False,
            default="``xonsh.prompt.PROMPT_FIELDS``",
        ),
        "FUZZY_PATH_COMPLETION": VarDocs(
            "Toggles 'fuzzy' matching of paths for tab completion, which is only "
            "used as a fallback if no other completions succeed but can be used "
            "as a way to adjust for typographical errors. If ``True``, then, e.g.,"
            " ``xonhs`` will match ``xonsh``."
        ),
        "GLOB_SORTED": VarDocs(
            "Toggles whether globbing results are manually sorted. If ``False``, "
            "the results are returned in arbitrary order."
        ),
        "HISTCONTROL": VarDocs(
            "A set of strings (comma-separated list in string form) of options "
            "that determine what commands are saved to the history list. By "
            "default all commands are saved. The option ``ignoredups`` will not "
            "save the command if it matches the previous command. The option "
            "'ignoreerr' will cause any commands that fail (i.e. return non-zero "
            "exit status) to not be added to the history list.",
            store_as_str=True,
        ),
        "IGNOREEOF": VarDocs("Prevents Ctrl-D from exiting the shell."),
        "INDENT": VarDocs("Indentation string for multiline input"),
        "INTENSIFY_COLORS_ON_WIN": VarDocs(
            "Enhance style colors for readability "
            "when using the default terminal (``cmd.exe``) on Windows. Blue colors, "
            "which are hard to read, are replaced with cyan. Other colors are "
            "generally replaced by their bright counter parts.",
            configurable=ON_WINDOWS,
        ),
        "LANG": VarDocs("Fallback locale setting for systems where it matters"),
        "LOADED_RC_FILES": VarDocs(
            "Whether or not any of the xonsh run control files were loaded at "
            "startup. This is a sequence of bools in Python that is converted "
            "to a CSV list in string form, ie ``[True, False]`` becomes "
            "``'True,False'``.",
            configurable=False,
        ),
        "MOUSE_SUPPORT": VarDocs(
            "Enable mouse support in the ``prompt_toolkit`` shell. This allows "
            "clicking for positioning the cursor or selecting a completion. In "
            "some terminals however, this disables the ability to scroll back "
            "through the history of the terminal. Only usable with "
            "``$SHELL_TYPE=prompt_toolkit``"
        ),
        "MULTILINE_PROMPT": VarDocs(
            "Prompt text for 2nd+ lines of input, may be str or function which "
            "returns a str."
        ),
        "OLDPWD": VarDocs(
            "Used to represent a previous present working directory.",
            configurable=False,
        ),
        "PATH": VarDocs("List of strings representing where to look for executables."),
        "PATHEXT": VarDocs(
            "Sequence of extension strings (eg, ``.EXE``) for "
            "filtering valid executables by. Each element must be "
            "uppercase."
        ),
        "PRETTY_PRINT_RESULTS": VarDocs('Flag for "pretty printing" return values.'),
        "PROMPT": VarDocs(
            "The prompt text. May contain keyword arguments which are "
            "auto-formatted, see 'Customizing the Prompt' at "
            "http://xon.sh/tutorial.html#customizing-the-prompt. "
            "This value is never inherited from parent processes.",
            default="``xonsh.environ.DEFAULT_PROMPT``",
        ),
        "PROMPT_TOOLKIT_COLOR_DEPTH": VarDocs(
            "The color depth used by prompt toolkit 2. Possible values are: "
            "``DEPTH_1_BIT``, ``DEPTH_4_BIT``, ``DEPTH_8_BIT``, ``DEPTH_24_BIT`` "
            "colors. Default is an empty string which means that prompt toolkit decide."
        ),
        "PTK_STYLE_OVERRIDES": VarDocs(
            "A dictionary containing custom prompt_toolkit style definitions."
        ),
        "PUSHD_MINUS": VarDocs(
            "Flag for directory pushing functionality. False is the normal " "behavior."
        ),
        "PUSHD_SILENT": VarDocs(
            "Whether or not to suppress directory stack manipulation output."
        ),
        "RAISE_SUBPROC_ERROR": VarDocs(
            "Whether or not to raise an error if a subprocess (captured or "
            "uncaptured) returns a non-zero exit status, which indicates failure. "
            "This is most useful in xonsh scripts or modules where failures "
            "should cause an end to execution. This is less useful at a terminal. "
            "The error that is raised is a ``subprocess.CalledProcessError``."
        ),
        "RIGHT_PROMPT": VarDocs(
            "Template string for right-aligned text "
            "at the prompt. This may be parametrized in the same way as "
            "the ``$PROMPT`` variable. Currently, this is only available in the "
            "prompt-toolkit shell."
        ),
        "BOTTOM_TOOLBAR": VarDocs(
            "Template string for the bottom toolbar. "
            "This may be parametrized in the same way as "
            "the ``$PROMPT`` variable. Currently, this is only available in the "
            "prompt-toolkit shell."
        ),
        "SHELL_TYPE": VarDocs(
            "Which shell is used. Currently two base shell types are supported:\n\n"
            "    - ``readline`` that is backed by Python's readline module\n"
            "    - ``prompt_toolkit`` that uses external library of the same name\n"
            "    - ``random`` selects a random shell from the above on startup\n"
            "    - ``best`` selects the most feature-rich shell available on the\n"
            "       user's system\n\n"
            "To use the ``prompt_toolkit`` shell you need to have the "
            "`prompt_toolkit <https://github.com/jonathanslenders/python-prompt-toolkit>`_"
            " library installed. To specify which shell should be used, do so in "
            "the run control file.",
            default="``best``",
        ),
        "SUBSEQUENCE_PATH_COMPLETION": VarDocs(
            "Toggles subsequence matching of paths for tab completion. "
            "If ``True``, then, e.g., ``~/u/ro`` can match ``~/lou/carcolh``."
        ),
        "SUGGEST_COMMANDS": VarDocs(
            "When a user types an invalid command, xonsh will try to offer "
            "suggestions of similar valid commands if this is True."
        ),
        "SUGGEST_MAX_NUM": VarDocs(
            "xonsh will show at most this many suggestions in response to an "
            "invalid command. If negative, there is no limit to how many "
            "suggestions are shown."
        ),
        "SUGGEST_THRESHOLD": VarDocs(
            "An error threshold. If the Levenshtein distance between the entered "
            "command and a valid command is less than this value, the valid "
            'command will be offered as a suggestion.  Also used for "fuzzy" '
            "tab completion of paths."
        ),
        "SUPPRESS_BRANCH_TIMEOUT_MESSAGE": VarDocs(
            "Whether or not to suppress branch timeout warning messages."
        ),
        "TERM": VarDocs(
            "TERM is sometimes set by the terminal emulator. This is used (when "
            "valid) to determine whether or not to set the title. Users shouldn't "
            "need to set this themselves. Note that this variable should be set as "
            "early as possible in order to ensure it is effective. Here are a few "
            "options:\n\n"
            "* Set this from the program that launches xonsh. On POSIX systems, \n"
            "  this can be performed by using env, e.g. \n"
            "  ``/usr/bin/env TERM=xterm-color xonsh`` or similar.\n"
            "* From the xonsh command line, namely ``xonsh -DTERM=xterm-color``.\n"
            '* In the config file with ``{"env": {"TERM": "xterm-color"}}``.\n'
            "* Lastly, in xonshrc with ``$TERM``\n\n"
            "Ideally, your terminal emulator will set this correctly but that does "
            "not always happen.",
            configurable=False,
        ),
        "TITLE": VarDocs(
            "The title text for the window in which xonsh is running. Formatted "
            "in the same manner as ``$PROMPT``, see 'Customizing the Prompt' "
            "http://xon.sh/tutorial.html#customizing-the-prompt.",
            default="``xonsh.environ.DEFAULT_TITLE``",
        ),
        "UPDATE_COMPLETIONS_ON_KEYPRESS": VarDocs(
            "Completions display is evaluated and presented whenever a key is "
            "pressed. This avoids the need to press TAB, except to cycle through "
            "the possibilities. This currently only affects the prompt-toolkit shell."
        ),
        "UPDATE_OS_ENVIRON": VarDocs(
            "If True ``os_environ`` will always be updated "
            "when the xonsh environment changes. The environment can be reset to "
            "the default value by calling ``__xonsh__.env.undo_replace_env()``"
        ),
        "UPDATE_PROMPT_ON_KEYPRESS": VarDocs(
            "Disables caching the prompt between commands, "
            "so that it would be reevaluated on each keypress. "
            "Disabled by default because of the incurred performance penalty."
        ),
        "VC_BRANCH_TIMEOUT": VarDocs(
            "The timeout (in seconds) for version control "
            "branch computations. This is a timeout per subprocess call, so the "
            "total time to compute will be larger than this in many cases."
        ),
        "VC_HG_SHOW_BRANCH": VarDocs(
            "Whether or not to show the Mercurial branch in the prompt."
        ),
        "VI_MODE": VarDocs(
            "Flag to enable ``vi_mode`` in the ``prompt_toolkit`` shell."
        ),
        "VIRTUAL_ENV": VarDocs(
            "Path to the currently active Python environment.", configurable=False
        ),
        "WIN_UNICODE_CONSOLE": VarDocs(
            "Enables unicode support in windows terminals. Requires the external "
            "library ``win_unicode_console``.",
            configurable=ON_WINDOWS,
        ),
        "XDG_CONFIG_HOME": VarDocs(
            "Open desktop standard configuration home dir. This is the same "
            "default as used in the standard.",
            configurable=False,
            default="``~/.config``",
        ),
        "XDG_DATA_HOME": VarDocs(
            "Open desktop standard data home dir. This is the same default as "
            "used in the standard.",
            default="``~/.local/share``",
        ),
        "XONSHRC": VarDocs(
            "A list of the locations of run control files, if they exist.  User "
            "defined run control file will supersede values set in system-wide "
            "control file if there is a naming collision.",
            default=(
                "On Linux & Mac OSX: ``['/etc/xonshrc', '~/.config/xonsh/rc.xsh', '~/.xonshrc']``\n"
                "\nOn Windows: "
                "``['%ALLUSERSPROFILE%\\\\xonsh\\\\xonshrc', '~/.config/xonsh/rc.xsh', '~/.xonshrc']``"
            ),
        ),
        "XONSH_APPEND_NEWLINE": VarDocs(
            "Append new line when a partial line is preserved in output."
        ),
        "XONSH_AUTOPAIR": VarDocs(
            "Whether Xonsh will auto-insert matching parentheses, brackets, and "
            "quotes. Only available under the prompt-toolkit shell."
        ),
        "XONSH_CACHE_SCRIPTS": VarDocs(
            "Controls whether the code for scripts run from xonsh will be cached"
            " (``True``) or re-compiled each time (``False``)."
        ),
        "XONSH_CACHE_EVERYTHING": VarDocs(
            "Controls whether all code (including code entered at the interactive"
            " prompt) will be cached."
        ),
        "XONSH_COLOR_STYLE": VarDocs(
            "Sets the color style for xonsh colors. This is a style name, not "
            "a color map. Run ``xonfig styles`` to see the available styles."
        ),
        "XONSH_CONFIG_DIR": VarDocs(
            "This is the location where xonsh configuration information is stored.",
            configurable=False,
            default="``$XDG_CONFIG_HOME/xonsh``",
        ),
        "XONSH_DEBUG": VarDocs(
            "Sets the xonsh debugging level. This may be an integer or a boolean. "
            "Setting this variable prior to stating xonsh to ``1`` or ``True`` "
            "will suppress amalgamated imports. Setting it to ``2`` will get some "
            "basic information like input transformation, command replacement. "
            "With ``3`` or a higher number will make more debugging information "
            "presented, like PLY parsing messages.",
            configurable=False,
        ),
        "XONSH_DATA_DIR": VarDocs(
            "This is the location where xonsh data files are stored, such as "
            "history.",
            default="``$XDG_DATA_HOME/xonsh``",
        ),
        "XONSH_ENCODING": VarDocs(
            "This is the encoding that xonsh should use for subprocess operations.",
            default="``sys.getdefaultencoding()``",
        ),
        "XONSH_ENCODING_ERRORS": VarDocs(
            "The flag for how to handle encoding errors should they happen. "
            "Any string flag that has been previously registered with Python "
            "is allowed. See the 'Python codecs documentation' "
            "(https://docs.python.org/3/library/codecs.html#error-handlers) "
            "for more information and available options.",
            default="``surrogateescape``",
        ),
        "XONSH_GITSTATUS_*": VarDocs(
            "Symbols for gitstatus prompt. Default values are: \n\n"
            "* ``XONSH_GITSTATUS_HASH``: ``:``\n"
            "* ``XONSH_GITSTATUS_BRANCH``: ``{CYAN}``\n"
            "* ``XONSH_GITSTATUS_OPERATION``: ``{CYAN}``\n"
            "* ``XONSH_GITSTATUS_STAGED``: ``{RED}●``\n"
            "* ``XONSH_GITSTATUS_CONFLICTS``: ``{RED}×``\n"
            "* ``XONSH_GITSTATUS_CHANGED``: ``{BLUE}+``\n"
            "* ``XONSH_GITSTATUS_UNTRACKED``: ``…``\n"
            "* ``XONSH_GITSTATUS_STASHED``: ``⚑``\n"
            "* ``XONSH_GITSTATUS_CLEAN``: ``{BOLD_GREEN}✓``\n"
            "* ``XONSH_GITSTATUS_AHEAD``: ``↑·``\n"
            "* ``XONSH_GITSTATUS_BEHIND``: ``↓·``\n"
        ),
        "XONSH_HISTORY_BACKEND": VarDocs(
            "Set which history backend to use. Options are: 'json', "
            "'sqlite', and 'dummy'. The default is 'json'. "
            "``XONSH_HISTORY_BACKEND`` also accepts a class type that inherits "
            "from ``xonsh.history.base.History``, or its instance."
        ),
        "XONSH_HISTORY_FILE": VarDocs(
            "Location of history file (deprecated).",
            configurable=False,
            default="``~/.xonsh_history``",
        ),
        "XONSH_HISTORY_MATCH_ANYWHERE": VarDocs(
            "When searching history from a partial string (by pressing up arrow), "
            "match command history anywhere in a given line (not just the start)",
            default="False",
        ),
        "XONSH_HISTORY_SIZE": VarDocs(
            "Value and units tuple that sets the size of history after garbage "
            "collection. Canonical units are:\n\n"
            "- ``commands`` for the number of past commands executed,\n"
            "- ``files`` for the number of history files to keep,\n"
            "- ``s`` for the number of seconds in the past that are allowed, and\n"
            "- ``b`` for the number of bytes that history may consume.\n\n"
            "Common abbreviations, such as '6 months' or '1 GB' are also allowed.",
            default="``(8128, 'commands')`` or ``'8128 commands'``",
        ),
        "XONSH_INTERACTIVE": VarDocs(
            "``True`` if xonsh is running interactively, and ``False`` otherwise.",
            configurable=False,
        ),
        "XONSH_LOGIN": VarDocs(
            "``True`` if xonsh is running as a login shell, and ``False`` otherwise.",
            configurable=False,
        ),
        "XONSH_PROC_FREQUENCY": VarDocs(
            "The process frequency is the time that "
            "xonsh process threads sleep for while running command pipelines. "
            "The value has units of seconds [s]."
        ),
        "XONSH_SHOW_TRACEBACK": VarDocs(
            "Controls if a traceback is shown if exceptions occur in the shell. "
            "Set to ``True`` to always show traceback or ``False`` to always hide. "
            "If undefined then the traceback is hidden but a notice is shown on how "
            "to enable the full traceback."
        ),
        "XONSH_SOURCE": VarDocs(
            "When running a xonsh script, this variable contains the absolute path "
            "to the currently executing script's file.",
            configurable=False,
        ),
        "XONSH_STDERR_PREFIX": VarDocs(
            "A format string, using the same keys and colors as ``$PROMPT``, that "
            "is prepended whenever stderr is displayed. This may be used in "
            "conjunction with ``$XONSH_STDERR_POSTFIX`` to close out the block."
            "For example, to have stderr appear on a red background, the "
            'prefix & postfix pair would be "{BACKGROUND_RED}" & "{NO_COLOR}".'
        ),
        "XONSH_STDERR_POSTFIX": VarDocs(
            "A format string, using the same keys and colors as ``$PROMPT``, that "
            "is appended whenever stderr is displayed. This may be used in "
            "conjunction with ``$XONSH_STDERR_PREFIX`` to start the block."
            "For example, to have stderr appear on a red background, the "
            'prefix & postfix pair would be "{BACKGROUND_RED}" & "{NO_COLOR}".'
        ),
        "XONSH_STORE_STDIN": VarDocs(
            "Whether or not to store the stdin that is supplied to the "
            "``!()`` and ``![]`` operators."
        ),
        "XONSH_STORE_STDOUT": VarDocs(
            "Whether or not to store the ``stdout`` and ``stderr`` streams in the "
            "history files."
        ),
        "XONSH_TRACEBACK_LOGFILE": VarDocs(
            "Specifies a file to store the traceback log to, regardless of whether "
            "``XONSH_SHOW_TRACEBACK`` has been set. Its value must be a writable file "
            "or None / the empty string if traceback logging is not desired. "
            "Logging to a file is not enabled by default."
        ),
        "XONSH_DATETIME_FORMAT": VarDocs(
            "The format that is used for ``datetime.strptime()`` in various places"
            "i.e the history timestamp option"
        ),
    }


#
# actual environment
#


class Env(cabc.MutableMapping):
    """A xonsh environment, whose variables have limited typing
    (unlike BASH). Most variables are, by default, strings (like BASH).
    However, the following rules also apply based on variable-name:

    * PATH: any variable whose name ends in PATH is a list of strings.
    * XONSH_HISTORY_SIZE: this variable is an (int | float, str) tuple.
    * LC_* (locale categories): locale category names get/set the Python
      locale via locale.getlocale() and locale.setlocale() functions.

    An Env instance may be converted to an untyped version suitable for
    use in a subprocess.
    """

    _arg_regex = None

    def __init__(self, *args, **kwargs):
        """If no initial environment is given, os_environ is used."""
        self._d = {}
        # sentinel value for non existing envvars
        self._no_value = object()
        self._orig_env = None
        self._ensurers = {k: Ensurer(*v) for k, v in DEFAULT_ENSURERS.items()}
        self._defaults = DEFAULT_VALUES
        self._docs = DEFAULT_DOCS
        if len(args) == 0 and len(kwargs) == 0:
            args = (os_environ,)
        for key, val in dict(*args, **kwargs).items():
            self[key] = val
        if ON_WINDOWS:
            path_key = next((k for k in self._d if k.upper() == "PATH"), None)
            if path_key:
                self["PATH"] = self._d.pop(path_key)
        if "PATH" not in self._d:
            # this is here so the PATH is accessible to subprocs and so that
            # it can be modified in-place in the xonshrc file
            self._d["PATH"] = list(PATH_DEFAULT)
        self._detyped = None

    @staticmethod
    def detypeable(val):
        return not (callable(val) or isinstance(val, cabc.MutableMapping))

    def detype(self):
        if self._detyped is not None:
            return self._detyped
        ctx = {}
        for key, val in self._d.items():
            if not self.detypeable(val):
                continue
            if not isinstance(key, str):
                key = str(key)
            ensurer = self.get_ensurer(key)
            val = ensurer.detype(val)
            ctx[key] = val
        self._detyped = ctx
        return ctx

    def replace_env(self):
        """Replaces the contents of os_environ with a detyped version
        of the xonsh environment.
        """
        if self._orig_env is None:
            self._orig_env = dict(os_environ)
        os_environ.clear()
        os_environ.update(self.detype())

    def undo_replace_env(self):
        """Replaces the contents of os_environ with a detyped version
        of the xonsh environment.
        """
        if self._orig_env is not None:
            os_environ.clear()
            os_environ.update(self._orig_env)
            self._orig_env = None

    def get_ensurer(self, key, default=Ensurer(always_true, None, ensure_string)):
        """Gets an ensurer for the given key."""
        if key in self._ensurers:
            return self._ensurers[key]
        for k, ensurer in self._ensurers.items():
            if isinstance(k, str):
                continue
            if k.match(key) is not None:
                break
        else:
            ensurer = default
        self._ensurers[key] = ensurer
        return ensurer

    def get_docs(self, key, default=VarDocs("<no documentation>")):
        """Gets the documentation for the environment variable."""
        vd = self._docs.get(key, None)
        if vd is None:
            return default
        if vd.default is DefaultNotGiven:
            dval = pprint.pformat(self._defaults.get(key, "<default not set>"))
            vd = vd._replace(default=dval)
            self._docs[key] = vd
        return vd

    def help(self, key):
        """Get information about a specific environment variable."""
        vardocs = self.get_docs(key)
        width = min(79, os.get_terminal_size()[0])
        docstr = "\n".join(textwrap.wrap(vardocs.docstr, width=width))
        template = HELP_TEMPLATE.format(
            envvar=key,
            docstr=docstr,
            default=vardocs.default,
            configurable=vardocs.configurable,
        )
        print_color(template)

    def is_manually_set(self, varname):
        """
        Checks if an environment variable has been manually set.
        """
        return varname in self._d

    @contextlib.contextmanager
    def swap(self, other=None, **kwargs):
        """Provides a context manager for temporarily swapping out certain
        environment variables with other values. On exit from the context
        manager, the original values are restored.
        """
        old = {}
        # single positional argument should be a dict-like object
        if other is not None:
            for k, v in other.items():
                old[k] = self.get(k, NotImplemented)
                self[k] = v
        # kwargs could also have been sent in
        for k, v in kwargs.items():
            old[k] = self.get(k, NotImplemented)
            self[k] = v

        exception = None
        try:
            yield self
        except Exception as e:
            exception = e
        finally:
            # restore the values
            for k, v in old.items():
                if v is NotImplemented:
                    del self[k]
                else:
                    self[k] = v
            if exception is not None:
                raise exception from None

    #
    # Mutable mapping interface
    #

    def __getitem__(self, key):
        # remove this block on next release
        if key == "FORMATTER_DICT":
            print(
                "PendingDeprecationWarning: FORMATTER_DICT is an alias of "
                "PROMPT_FIELDS and will be removed in the next release",
                file=sys.stderr,
            )
            return self["PROMPT_FIELDS"]
        if key is Ellipsis:
            return self
        elif key in self._d:
            val = self._d[key]
        elif key in self._defaults:
            val = self._defaults[key]
            if is_callable_default(val):
                val = val(self)
        else:
            e = "Unknown environment variable: ${}"
            raise KeyError(e.format(key))
        if isinstance(
            val, (cabc.MutableSet, cabc.MutableSequence, cabc.MutableMapping)
        ):
            self._detyped = None
        return val

    def __setitem__(self, key, val):
        ensurer = self.get_ensurer(key)
        if not ensurer.validate(val):
            val = ensurer.convert(val)
        # existing envvars can have any value including None
        old_value = self._d[key] if key in self._d else self._no_value
        self._d[key] = val
        if self.detypeable(val):
            self._detyped = None
            if self.get("UPDATE_OS_ENVIRON"):
                if self._orig_env is None:
                    self.replace_env()
                else:
                    os_environ[key] = ensurer.detype(val)
        if old_value is self._no_value:
            events.on_envvar_new.fire(name=key, value=val)
        elif old_value != val:
            events.on_envvar_change.fire(name=key, oldvalue=old_value, newvalue=val)

    def __delitem__(self, key):
        val = self._d.pop(key)
        if self.detypeable(val):
            self._detyped = None
            if self.get("UPDATE_OS_ENVIRON") and key in os_environ:
                del os_environ[key]

    def get(self, key, default=None):
        """The environment will look up default values from its own defaults if a
        default is not given here.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self):
        yield from (set(self._d) | set(self._defaults))

    def __contains__(self, item):
        return item in self._d or item in self._defaults

    def __len__(self):
        return len(self._d)

    def __str__(self):
        return str(self._d)

    def __repr__(self):
        return "{0}.{1}(...)".format(
            self.__class__.__module__, self.__class__.__name__, self._d
        )

    def _repr_pretty_(self, p, cycle):
        name = "{0}.{1}".format(self.__class__.__module__, self.__class__.__name__)
        with p.group(0, name + "(", ")"):
            if cycle:
                p.text("...")
            elif len(self):
                p.break_()
                p.pretty(dict(self))


def _yield_executables(directory, name):
    if ON_WINDOWS:
        base_name, ext = os.path.splitext(name.lower())
        for fname in executables_in(directory):
            fbase, fext = os.path.splitext(fname.lower())
            if base_name == fbase and (len(ext) == 0 or ext == fext):
                yield os.path.join(directory, fname)
    else:
        for x in executables_in(directory):
            if x == name:
                yield os.path.join(directory, name)
                return


def locate_binary(name):
    """Locates an executable on the file system."""
    return builtins.__xonsh__.commands_cache.locate_binary(name)


BASE_ENV = LazyObject(
    lambda: {
        "BASH_COMPLETIONS": list(DEFAULT_VALUES["BASH_COMPLETIONS"]),
        "PROMPT_FIELDS": dict(DEFAULT_VALUES["PROMPT_FIELDS"]),
        "XONSH_VERSION": XONSH_VERSION,
    },
    globals(),
    "BASE_ENV",
)


def xonshrc_context(rcfiles=None, execer=None, ctx=None, env=None, login=True):
    """Attempts to read in all xonshrc files and return the context."""
    loaded = env["LOADED_RC_FILES"] = []
    ctx = {} if ctx is None else ctx
    if rcfiles is None:
        return env
    env["XONSHRC"] = tuple(rcfiles)
    for rcfile in rcfiles:
        if not os.path.isfile(rcfile):
            loaded.append(False)
            continue
        _, ext = os.path.splitext(rcfile)
        status = xonsh_script_run_control(rcfile, ctx, env, execer=execer, login=login)
        loaded.append(status)
    return ctx


def windows_foreign_env_fixes(ctx):
    """Environment fixes for Windows. Operates in-place."""
    # remove these bash variables which only cause problems.
    for ev in ["HOME", "OLDPWD"]:
        if ev in ctx:
            del ctx[ev]
    # Override path-related bash variables; on Windows bash uses
    # /c/Windows/System32 syntax instead of C:\\Windows\\System32
    # which messes up these environment variables for xonsh.
    for ev in ["PATH", "TEMP", "TMP"]:
        if ev in os_environ:
            ctx[ev] = os_environ[ev]
        elif ev in ctx:
            del ctx[ev]
    ctx["PWD"] = _get_cwd() or ""


def foreign_env_fixes(ctx):
    """Environment fixes for all operating systems"""
    if "PROMPT" in ctx:
        del ctx["PROMPT"]


def xonsh_script_run_control(filename, ctx, env, execer=None, login=True):
    """Loads a xonsh file and applies it as a run control."""
    if execer is None:
        return False
    updates = {"__file__": filename, "__name__": os.path.abspath(filename)}
    try:
        with swap_values(ctx, updates):
            run_script_with_cache(filename, execer, ctx)
        loaded = True
    except SyntaxError as err:
        msg = "syntax error in xonsh run control file {0!r}: {1!s}"
        print_exception(msg.format(filename, err))
        loaded = False
    except Exception as err:
        msg = "error running xonsh run control file {0!r}: {1!s}"
        print_exception(msg.format(filename, err))
        loaded = False
    return loaded


def default_env(env=None):
    """Constructs a default xonsh environment."""
    # in order of increasing precedence
    ctx = dict(BASE_ENV)
    ctx.update(os_environ)
    ctx["PWD"] = _get_cwd() or ""
    # These can cause problems for programs (#2543)
    ctx.pop("LINES", None)
    ctx.pop("COLUMNS", None)
    # other shells' PROMPT definitions generally don't work in XONSH:
    try:
        del ctx["PROMPT"]
    except KeyError:
        pass
    # finalize env
    if env is not None:
        ctx.update(env)
    return ctx


def make_args_env(args=None):
    """Makes a dictionary containing the $ARGS and $ARG<N> environment
    variables. If the supplied ARGS is None, then sys.argv is used.
    """
    if args is None:
        args = sys.argv
    env = {"ARG" + str(i): arg for i, arg in enumerate(args)}
    env["ARGS"] = list(args)  # make a copy so we don't interfere with original variable
    return env

#
# inspectors
#
# -*- coding: utf-8 -*-
"""Tools for inspecting Python objects.

This file was forked from the IPython project:

* Copyright (c) 2008-2014, IPython Development Team
* Copyright (C) 2001-2007 Fernando Perez <fperez@colorado.edu>
* Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
* Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>
"""
# amalgamated os
# amalgamated io
# amalgamated sys
# amalgamated types
# amalgamated inspect
# amalgamated itertools
linecache = _LazyModule.load('linecache', 'linecache')
# amalgamated collections
# amalgamated xonsh.lazyasd
# amalgamated xonsh.tokenize
# amalgamated xonsh.openpy
# amalgamated xonsh.tools
# amalgamated xonsh.platform
# amalgamated xonsh.lazyimps
# amalgamated xonsh.style_tools
_func_call_docstring = LazyObject(
    lambda: types.FunctionType.__call__.__doc__, globals(), "_func_call_docstring"
)
_object_init_docstring = LazyObject(
    lambda: object.__init__.__doc__, globals(), "_object_init_docstring"
)
_builtin_type_docstrings = LazyObject(
    lambda: {
        t.__doc__ for t in (types.ModuleType, types.MethodType, types.FunctionType)
    },
    globals(),
    "_builtin_type_docstrings",
)

_builtin_func_type = LazyObject(lambda: type(all), globals(), "_builtin_func_type")
# Bound methods have the same type as builtin functions
_builtin_meth_type = LazyObject(
    lambda: type(str.upper), globals(), "_builtin_meth_type"
)

info_fields = LazyObject(
    lambda: [
        "type_name",
        "base_class",
        "string_form",
        "namespace",
        "length",
        "file",
        "definition",
        "docstring",
        "source",
        "init_definition",
        "class_docstring",
        "init_docstring",
        "call_def",
        "call_docstring",
        # These won't be printed but will be used to determine how to
        # format the object
        "ismagic",
        "isalias",
        "isclass",
        "argspec",
        "found",
        "name",
    ],
    globals(),
    "info_fields",
)


def object_info(**kw):
    """Make an object info dict with all fields present."""
    infodict = dict(itertools.zip_longest(info_fields, [None]))
    infodict.update(kw)
    return infodict


def get_encoding(obj):
    """Get encoding for python source file defining obj

    Returns None if obj is not defined in a sourcefile.
    """
    ofile = find_file(obj)
    # run contents of file through pager starting at line where the object
    # is defined, as long as the file isn't binary and is actually on the
    # filesystem.
    if ofile is None:
        return None
    elif ofile.endswith((".so", ".dll", ".pyd")):
        return None
    elif not os.path.isfile(ofile):
        return None
    else:
        # Print only text files, not extension binaries.  Note that
        # getsourcelines returns lineno with 1-offset and page() uses
        # 0-offset, so we must adjust.
        with io.open(ofile, "rb") as buf:  # Tweaked to use io.open for Python 2
            encoding, _ = detect_encoding(buf.readline)
        return encoding


def getdoc(obj):
    """Stable wrapper around inspect.getdoc.

    This can't crash because of attribute problems.

    It also attempts to call a getdoc() method on the given object.  This
    allows objects which provide their docstrings via non-standard mechanisms
    (like Pyro proxies) to still be inspected by ipython's ? system."""
    # Allow objects to offer customized documentation via a getdoc method:
    try:
        ds = obj.getdoc()
    except Exception:  # pylint:disable=broad-except
        pass
    else:
        # if we get extra info, we add it to the normal docstring.
        if isinstance(ds, str):
            return inspect.cleandoc(ds)

    try:
        docstr = inspect.getdoc(obj)
        encoding = get_encoding(obj)
        return cast_unicode(docstr, encoding=encoding)
    except Exception:  # pylint:disable=broad-except
        # Harden against an inspect failure, which can occur with
        # SWIG-wrapped extensions.
        raise


def getsource(obj, is_binary=False):
    """Wrapper around inspect.getsource.

    This can be modified by other projects to provide customized source
    extraction.

    Inputs:

    - obj: an object whose source code we will attempt to extract.

    Optional inputs:

    - is_binary: whether the object is known to come from a binary source.
      This implementation will skip returning any output for binary objects,
      but custom extractors may know how to meaningfully process them."""

    if is_binary:
        return None
    else:
        # get source if obj was decorated with @decorator
        if hasattr(obj, "__wrapped__"):
            obj = obj.__wrapped__
        try:
            src = inspect.getsource(obj)
        except TypeError:
            if hasattr(obj, "__class__"):
                src = inspect.getsource(obj.__class__)
        encoding = get_encoding(obj)
        return cast_unicode(src, encoding=encoding)


def is_simple_callable(obj):
    """True if obj is a function ()"""
    return (
        inspect.isfunction(obj)
        or inspect.ismethod(obj)
        or isinstance(obj, _builtin_func_type)
        or isinstance(obj, _builtin_meth_type)
    )


def getargspec(obj):
    """Wrapper around :func:`inspect.getfullargspec` on Python 3, and
    :func:inspect.getargspec` on Python 2.

    In addition to functions and methods, this can also handle objects with a
    ``__call__`` attribute.
    """
    if safe_hasattr(obj, "__call__") and not is_simple_callable(obj):
        obj = obj.__call__

    return inspect.getfullargspec(obj)


def format_argspec(argspec):
    """Format argspect, convenience wrapper around inspect's.

    This takes a dict instead of ordered arguments and calls
    inspect.format_argspec with the arguments in the necessary order.
    """
    return inspect.formatargspec(
        argspec["args"], argspec["varargs"], argspec["varkw"], argspec["defaults"]
    )


def call_tip(oinfo, format_call=True):
    """Extract call tip data from an oinfo dict.

    Parameters
    ----------
    oinfo : dict

    format_call : bool, optional
      If True, the call line is formatted and returned as a string.  If not, a
      tuple of (name, argspec) is returned.

    Returns
    -------
    call_info : None, str or (str, dict) tuple.
      When format_call is True, the whole call information is formatted as a
      single string.  Otherwise, the object's name and its argspec dict are
      returned.  If no call information is available, None is returned.

    docstring : str or None
      The most relevant docstring for calling purposes is returned, if
      available.  The priority is: call docstring for callable instances, then
      constructor docstring for classes, then main object's docstring otherwise
      (regular functions).
    """
    # Get call definition
    argspec = oinfo.get("argspec")
    if argspec is None:
        call_line = None
    else:
        # Callable objects will have 'self' as their first argument, prune
        # it out if it's there for clarity (since users do *not* pass an
        # extra first argument explicitly).
        try:
            has_self = argspec["args"][0] == "self"
        except (KeyError, IndexError):
            pass
        else:
            if has_self:
                argspec["args"] = argspec["args"][1:]

        call_line = oinfo["name"] + format_argspec(argspec)

    # Now get docstring.
    # The priority is: call docstring, constructor docstring, main one.
    doc = oinfo.get("call_docstring")
    if doc is None:
        doc = oinfo.get("init_docstring")
    if doc is None:
        doc = oinfo.get("docstring", "")

    return call_line, doc


def find_file(obj):
    """Find the absolute path to the file where an object was defined.

    This is essentially a robust wrapper around `inspect.getabsfile`.

    Returns None if no file can be found.

    Parameters
    ----------
    obj : any Python object

    Returns
    -------
    fname : str
      The absolute path to the file where the object was defined.
    """
    # get source if obj was decorated with @decorator
    if safe_hasattr(obj, "__wrapped__"):
        obj = obj.__wrapped__

    fname = None
    try:
        fname = inspect.getabsfile(obj)
    except TypeError:
        # For an instance, the file that matters is where its class was
        # declared.
        if hasattr(obj, "__class__"):
            try:
                fname = inspect.getabsfile(obj.__class__)
            except TypeError:
                # Can happen for builtins
                pass
    except:  # pylint:disable=bare-except
        pass
    return cast_unicode(fname)


def find_source_lines(obj):
    """Find the line number in a file where an object was defined.

    This is essentially a robust wrapper around `inspect.getsourcelines`.

    Returns None if no file can be found.

    Parameters
    ----------
    obj : any Python object

    Returns
    -------
    lineno : int
      The line number where the object definition starts.
    """
    # get source if obj was decorated with @decorator
    if safe_hasattr(obj, "__wrapped__"):
        obj = obj.__wrapped__

    try:
        try:
            lineno = inspect.getsourcelines(obj)[1]
        except TypeError:
            # For instances, try the class object like getsource() does
            if hasattr(obj, "__class__"):
                lineno = inspect.getsourcelines(obj.__class__)[1]
            else:
                lineno = None
    except:  # pylint:disable=bare-except
        return None

    return lineno


if PYTHON_VERSION_INFO < (3, 5, 0):
    FrameInfo = collections.namedtuple(
        "FrameInfo",
        ["frame", "filename", "lineno", "function", "code_context", "index"],
    )

    def getouterframes(frame, context=1):
        """Wrapper for getouterframes so that it acts like the Python v3.5 version."""
        return [FrameInfo(*f) for f in inspect.getouterframes(frame, context=context)]


else:
    getouterframes = inspect.getouterframes


class Inspector(object):
    """Inspects objects."""

    def __init__(self, str_detail_level=0):
        self.str_detail_level = str_detail_level

    def _getdef(self, obj, oname=""):
        """Return the call signature for any callable object.

        If any exception is generated, None is returned instead and the
        exception is suppressed.
        """
        try:
            hdef = oname + inspect.signature(*getargspec(obj))
            return cast_unicode(hdef)
        except:  # pylint:disable=bare-except
            return None

    def noinfo(self, msg, oname):
        """Generic message when no information is found."""
        print("No %s found" % msg, end=" ")
        if oname:
            print("for %s" % oname)
        else:
            print()

    def pdef(self, obj, oname=""):
        """Print the call signature for any callable object.

        If the object is a class, print the constructor information.
        """

        if not callable(obj):
            print("Object is not callable.")
            return

        header = ""

        if inspect.isclass(obj):
            header = self.__head("Class constructor information:\n")
            obj = obj.__init__

        output = self._getdef(obj, oname)
        if output is None:
            self.noinfo("definition header", oname)
        else:
            print(header, output, end=" ", file=sys.stdout)

    def pdoc(self, obj, oname=""):
        """Print the docstring for any object.

        Optional

        -formatter: a function to run the docstring through for specially
        formatted docstrings.
        """

        head = self.__head  # For convenience
        lines = []
        ds = getdoc(obj)
        if ds:
            lines.append(head("Class docstring:"))
            lines.append(indent(ds))
        if inspect.isclass(obj) and hasattr(obj, "__init__"):
            init_ds = getdoc(obj.__init__)
            if init_ds is not None:
                lines.append(head("Init docstring:"))
                lines.append(indent(init_ds))
        elif hasattr(obj, "__call__"):
            call_ds = getdoc(obj.__call__)
            if call_ds:
                lines.append(head("Call docstring:"))
                lines.append(indent(call_ds))

        if not lines:
            self.noinfo("documentation", oname)
        else:
            print("\n".join(lines))

    def psource(self, obj, oname=""):
        """Print the source code for an object."""
        # Flush the source cache because inspect can return out-of-date source
        linecache.checkcache()
        try:
            src = getsource(obj)
        except:  # pylint:disable=bare-except
            self.noinfo("source", oname)
        else:
            print(src)

    def pfile(self, obj, oname=""):
        """Show the whole file where an object was defined."""
        lineno = find_source_lines(obj)
        if lineno is None:
            self.noinfo("file", oname)
            return

        ofile = find_file(obj)
        # run contents of file through pager starting at line where the object
        # is defined, as long as the file isn't binary and is actually on the
        # filesystem.
        if ofile.endswith((".so", ".dll", ".pyd")):
            print("File %r is binary, not printing." % ofile)
        elif not os.path.isfile(ofile):
            print("File %r does not exist, not printing." % ofile)
        else:
            # Print only text files, not extension binaries.  Note that
            # getsourcelines returns lineno with 1-offset and page() uses
            # 0-offset, so we must adjust.
            o = read_py_file(ofile, skip_encoding_cookie=False)
            print(o, lineno - 1)

    def _format_fields_str(self, fields, title_width=0):
        """Formats a list of fields for display using color strings.

        Parameters
        ----------
        fields : list
          A list of 2-tuples: (field_title, field_content)
        title_width : int
          How many characters to pad titles to. Default to longest title.
        """
        out = []
        if title_width == 0:
            title_width = max(len(title) + 2 for title, _ in fields)
        for title, content in fields:
            title_len = len(title)
            title = "{BOLD_RED}" + title + ":{NO_COLOR}"
            if len(content.splitlines()) > 1:
                title += "\n"
            else:
                title += " ".ljust(title_width - title_len)
            out.append(cast_unicode(title) + cast_unicode(content))
        return format_color("\n".join(out) + "\n")

    def _format_fields_tokens(self, fields, title_width=0):
        """Formats a list of fields for display using color tokens from
        pygments.

        Parameters
        ----------
        fields : list
          A list of 2-tuples: (field_title, field_content)
        title_width : int
          How many characters to pad titles to. Default to longest title.
        """
        out = []
        if title_width == 0:
            title_width = max(len(title) + 2 for title, _ in fields)
        for title, content in fields:
            title_len = len(title)
            title = "{BOLD_RED}" + title + ":{NO_COLOR}"
            if not isinstance(content, str) or len(content.splitlines()) > 1:
                title += "\n"
            else:
                title += " ".ljust(title_width - title_len)
            out += partial_color_tokenize(title)
            if isinstance(content, str):
                out[-1] = (out[-1][0], out[-1][1] + content + "\n")
            else:
                out += content
                out[-1] = (out[-1][0], out[-1][1] + "\n")
        out[-1] = (out[-1][0], out[-1][1] + "\n")
        return out

    def _format_fields(self, fields, title_width=0):
        """Formats a list of fields for display using color tokens from
        pygments.

        Parameters
        ----------
        fields : list
          A list of 2-tuples: (field_title, field_content)
        title_width : int
          How many characters to pad titles to. Default to longest title.
        """
        if HAS_PYGMENTS:
            rtn = self._format_fields_tokens(fields, title_width=title_width)
        else:
            rtn = self._format_fields_str(fields, title_width=title_width)
        return rtn

    # The fields to be displayed by pinfo: (fancy_name, key_in_info_dict)
    pinfo_fields1 = [("Type", "type_name")]

    pinfo_fields2 = [("String form", "string_form")]

    pinfo_fields3 = [
        ("Length", "length"),
        ("File", "file"),
        ("Definition", "definition"),
    ]

    pinfo_fields_obj = [
        ("Class docstring", "class_docstring"),
        ("Init docstring", "init_docstring"),
        ("Call def", "call_def"),
        ("Call docstring", "call_docstring"),
    ]

    def pinfo(self, obj, oname="", info=None, detail_level=0):
        """Show detailed information about an object.

        Parameters
        ----------
        obj : object
        oname : str, optional
            name of the variable pointing to the object.
        info : dict, optional
            a structure with some information fields which may have been
            precomputed already.
        detail_level : int, optional
            if set to 1, more information is given.
        """
        info = self.info(obj, oname=oname, info=info, detail_level=detail_level)
        displayfields = []

        def add_fields(fields):
            for title, key in fields:
                field = info[key]
                if field is not None:
                    displayfields.append((title, field.rstrip()))

        add_fields(self.pinfo_fields1)
        add_fields(self.pinfo_fields2)

        # Namespace
        if info["namespace"] is not None and info["namespace"] != "Interactive":
            displayfields.append(("Namespace", info["namespace"].rstrip()))

        add_fields(self.pinfo_fields3)
        if info["isclass"] and info["init_definition"]:
            displayfields.append(("Init definition", info["init_definition"].rstrip()))

        # Source or docstring, depending on detail level and whether
        # source found.
        if detail_level > 0 and info["source"] is not None:
            displayfields.append(("Source", cast_unicode(info["source"])))
        elif info["docstring"] is not None:
            displayfields.append(("Docstring", info["docstring"]))

        # Constructor info for classes
        if info["isclass"]:
            if info["init_docstring"] is not None:
                displayfields.append(("Init docstring", info["init_docstring"]))

        # Info for objects:
        else:
            add_fields(self.pinfo_fields_obj)

        # Finally send to printer/pager:
        if displayfields:
            print_color(self._format_fields(displayfields))

    def info(self, obj, oname="", info=None, detail_level=0):
        """Compute a dict with detailed information about an object.

        Optional arguments:

        - oname: name of the variable pointing to the object.

        - info: a structure with some information fields which may have been
          precomputed already.

        - detail_level: if set to 1, more information is given.
        """
        obj_type = type(obj)
        if info is None:
            ismagic = 0
            isalias = 0
            ospace = ""
        else:
            ismagic = info.ismagic
            isalias = info.isalias
            ospace = info.namespace
        # Get docstring, special-casing aliases:
        if isalias:
            if not callable(obj):
                if len(obj) >= 2 and isinstance(obj[1], str):
                    ds = "Alias to the system command:\n  {0}".format(obj[1])
                else:  # pylint:disable=bare-except
                    ds = "Alias: " + str(obj)
            else:
                ds = "Alias to " + str(obj)
                if obj.__doc__:
                    ds += "\nDocstring:\n" + obj.__doc__
        else:
            ds = getdoc(obj)
            if ds is None:
                ds = "<no docstring>"

        # store output in a dict, we initialize it here and fill it as we go
        out = dict(name=oname, found=True, isalias=isalias, ismagic=ismagic)

        string_max = 200  # max size of strings to show (snipped if longer)
        shalf = int((string_max - 5) / 2)

        if ismagic:
            obj_type_name = "Magic function"
        elif isalias:
            obj_type_name = "System alias"
        else:
            obj_type_name = obj_type.__name__
        out["type_name"] = obj_type_name

        try:
            bclass = obj.__class__
            out["base_class"] = str(bclass)
        except:  # pylint:disable=bare-except
            pass

        # String form, but snip if too long in ? form (full in ??)
        if detail_level >= self.str_detail_level:
            try:
                ostr = str(obj)
                str_head = "string_form"
                if not detail_level and len(ostr) > string_max:
                    ostr = ostr[:shalf] + " <...> " + ostr[-shalf:]
                    ostr = ("\n" + " " * len(str_head.expandtabs())).join(
                        q.strip() for q in ostr.split("\n")
                    )
                out[str_head] = ostr
            except:  # pylint:disable=bare-except
                pass

        if ospace:
            out["namespace"] = ospace

        # Length (for strings and lists)
        try:
            out["length"] = str(len(obj))
        except:  # pylint:disable=bare-except
            pass

        # Filename where object was defined
        binary_file = False
        fname = find_file(obj)
        if fname is None:
            # if anything goes wrong, we don't want to show source, so it's as
            # if the file was binary
            binary_file = True
        else:
            if fname.endswith((".so", ".dll", ".pyd")):
                binary_file = True
            elif fname.endswith("<string>"):
                fname = "Dynamically generated function. " "No source code available."
            out["file"] = fname

        # Docstrings only in detail 0 mode, since source contains them (we
        # avoid repetitions).  If source fails, we add them back, see below.
        if ds and detail_level == 0:
            out["docstring"] = ds

        # Original source code for any callable
        if detail_level:
            # Flush the source cache because inspect can return out-of-date
            # source
            linecache.checkcache()
            source = None
            try:
                try:
                    source = getsource(obj, binary_file)
                except TypeError:
                    if hasattr(obj, "__class__"):
                        source = getsource(obj.__class__, binary_file)
                if source is not None:
                    source = source.rstrip()
                    if HAS_PYGMENTS:
                        lexer = pyghooks.XonshLexer()
                        source = list(pygments.lex(source, lexer=lexer))
                    out["source"] = source
            except Exception:  # pylint:disable=broad-except
                pass

            if ds and source is None:
                out["docstring"] = ds

        # Constructor docstring for classes
        if inspect.isclass(obj):
            out["isclass"] = True
            # reconstruct the function definition and print it:
            try:
                obj_init = obj.__init__
            except AttributeError:
                init_def = init_ds = None
            else:
                init_def = self._getdef(obj_init, oname)
                init_ds = getdoc(obj_init)
                # Skip Python's auto-generated docstrings
                if init_ds == _object_init_docstring:
                    init_ds = None

            if init_def or init_ds:
                if init_def:
                    out["init_definition"] = init_def
                if init_ds:
                    out["init_docstring"] = init_ds

        # and class docstring for instances:
        else:
            # reconstruct the function definition and print it:
            defln = self._getdef(obj, oname)
            if defln:
                out["definition"] = defln

            # First, check whether the instance docstring is identical to the
            # class one, and print it separately if they don't coincide.  In
            # most cases they will, but it's nice to print all the info for
            # objects which use instance-customized docstrings.
            if ds:
                try:
                    cls = getattr(obj, "__class__")
                except:  # pylint:disable=bare-except
                    class_ds = None
                else:
                    class_ds = getdoc(cls)
                # Skip Python's auto-generated docstrings
                if class_ds in _builtin_type_docstrings:
                    class_ds = None
                if class_ds and ds != class_ds:
                    out["class_docstring"] = class_ds

            # Next, try to show constructor docstrings
            try:
                init_ds = getdoc(obj.__init__)
                # Skip Python's auto-generated docstrings
                if init_ds == _object_init_docstring:
                    init_ds = None
            except AttributeError:
                init_ds = None
            if init_ds:
                out["init_docstring"] = init_ds

            # Call form docstring for callable instances
            if safe_hasattr(obj, "__call__") and not is_simple_callable(obj):
                call_def = self._getdef(obj.__call__, oname)
                if call_def:
                    call_def = call_def
                    # it may never be the case that call def and definition
                    # differ, but don't include the same signature twice
                    if call_def != out.get("definition"):
                        out["call_def"] = call_def
                call_ds = getdoc(obj.__call__)
                # Skip Python's auto-generated docstrings
                if call_ds == _func_call_docstring:
                    call_ds = None
                if call_ds:
                    out["call_docstring"] = call_ds

        # Compute the object's argspec as a callable.  The key is to decide
        # whether to pull it from the object itself, from its __init__ or
        # from its __call__ method.

        if inspect.isclass(obj):
            # Old-style classes need not have an __init__
            callable_obj = getattr(obj, "__init__", None)
        elif callable(obj):
            callable_obj = obj
        else:
            callable_obj = None

        if callable_obj:
            try:
                argspec = getargspec(callable_obj)
            except (TypeError, AttributeError):
                # For extensions/builtins we can't retrieve the argspec
                pass
            else:
                # named tuples' _asdict() method returns an OrderedDict, but we
                # we want a normal
                out["argspec"] = argspec_dict = dict(argspec._asdict())
                # We called this varkw before argspec became a named tuple.
                # With getfullargspec it's also called varkw.
                if "varkw" not in argspec_dict:
                    argspec_dict["varkw"] = argspec_dict.pop("keywords")

        return object_info(**out)

#
# readline_shell
#
# -*- coding: utf-8 -*-
"""The readline based xonsh shell.

Portions of this code related to initializing the readline library
are included from the IPython project.  The IPython project is:

* Copyright (c) 2008-2014, IPython Development Team
* Copyright (c) 2001-2007, Fernando Perez <fernando.perez@colorado.edu>
* Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
* Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>

"""
# amalgamated os
# amalgamated sys
cmd = _LazyModule.load('cmd', 'cmd')
select = _LazyModule.load('select', 'select')
# amalgamated shutil
# amalgamated builtins
# amalgamated importlib
# amalgamated threading
# amalgamated subprocess
# amalgamated collections
# amalgamated xonsh.lazyasd
# amalgamated xonsh.base_shell
# amalgamated xonsh.ansi_colors
# amalgamated from xonsh.prompt.base import multiline_prompt
# amalgamated xonsh.tools
# amalgamated xonsh.platform
# amalgamated xonsh.lazyimps
# amalgamated xonsh.events
readline = None
RL_COMPLETION_SUPPRESS_APPEND = RL_LIB = RL_STATE = None
RL_COMPLETION_QUERY_ITEMS = None
RL_CAN_RESIZE = False
RL_DONE = None
RL_VARIABLE_VALUE = None
_RL_STATE_DONE = 0x1000000
_RL_STATE_ISEARCH = 0x0000080

_RL_PREV_CASE_SENSITIVE_COMPLETIONS = "to-be-set"


def setup_readline():
    """Sets up the readline module and completion suppression, if available."""
    global RL_COMPLETION_SUPPRESS_APPEND, RL_LIB, RL_CAN_RESIZE, RL_STATE, readline, RL_COMPLETION_QUERY_ITEMS
    if RL_COMPLETION_SUPPRESS_APPEND is not None:
        return
    for _rlmod_name in ("gnureadline", "readline"):
        try:
            readline = importlib.import_module(_rlmod_name)
            sys.modules["readline"] = readline
        except ImportError:
            pass
        else:
            break

    if readline is None:
        print(
            """Skipping setup. Because no `readline` implementation available.
            Please install a backend (`readline`, `prompt-toolkit`, etc) to use
            `xonsh` interactively.
            See https://github.com/xonsh/xonsh/issues/1170"""
        )
        return

    import ctypes
    import ctypes.util

    uses_libedit = readline.__doc__ and "libedit" in readline.__doc__
    readline.set_completer_delims(" \t\n")
    # Cygwin seems to hang indefinitely when querying the readline lib
    if (not ON_CYGWIN) and (not ON_MSYS) and (not readline.__file__.endswith(".py")):
        RL_LIB = lib = ctypes.cdll.LoadLibrary(readline.__file__)
        try:
            RL_COMPLETION_SUPPRESS_APPEND = ctypes.c_int.in_dll(
                lib, "rl_completion_suppress_append"
            )
        except ValueError:
            # not all versions of readline have this symbol, ie Macs sometimes
            RL_COMPLETION_SUPPRESS_APPEND = None
        try:
            RL_COMPLETION_QUERY_ITEMS = ctypes.c_int.in_dll(
                lib, "rl_completion_query_items"
            )
        except ValueError:
            # not all versions of readline have this symbol, ie Macs sometimes
            RL_COMPLETION_QUERY_ITEMS = None
        try:
            RL_STATE = ctypes.c_int.in_dll(lib, "rl_readline_state")
        except Exception:
            pass
        RL_CAN_RESIZE = hasattr(lib, "rl_reset_screen_size")
    env = builtins.__xonsh__.env
    # reads in history
    readline.set_history_length(-1)
    ReadlineHistoryAdder()
    # sets up IPython-like history matching with up and down
    readline.parse_and_bind('"\\e[B": history-search-forward')
    readline.parse_and_bind('"\\e[A": history-search-backward')
    # Setup Shift-Tab to indent
    readline.parse_and_bind('"\\e[Z": "{0}"'.format(env.get("INDENT")))

    # handle tab completion differences found in libedit readline compatibility
    # as discussed at http://stackoverflow.com/a/7116997
    if uses_libedit and ON_DARWIN:
        readline.parse_and_bind("bind ^I rl_complete")
        print(
            "\n".join(
                [
                    "",
                    "*" * 78,
                    "libedit detected - readline will not be well behaved, including but not limited to:",
                    "   * crashes on tab completion",
                    "   * incorrect history navigation",
                    "   * corrupting long-lines",
                    "   * failure to wrap or indent lines properly",
                    "",
                    "It is highly recommended that you install gnureadline, which is installable with:",
                    "     xpip install gnureadline",
                    "*" * 78,
                ]
            ),
            file=sys.stderr,
        )
    else:
        readline.parse_and_bind("tab: complete")
    # try to load custom user settings
    inputrc_name = os_environ.get("INPUTRC")
    if inputrc_name is None:
        if uses_libedit:
            inputrc_name = ".editrc"
        else:
            inputrc_name = ".inputrc"
        inputrc_name = os.path.join(os.path.expanduser("~"), inputrc_name)
    if (not ON_WINDOWS) and (not os.path.isfile(inputrc_name)):
        inputrc_name = "/etc/inputrc"
    if ON_WINDOWS:
        winutils.enable_virtual_terminal_processing()
    if os.path.isfile(inputrc_name):
        try:
            readline.read_init_file(inputrc_name)
        except Exception:
            # this seems to fail with libedit
            print_exception("xonsh: could not load readline default init file.")
    # properly reset input typed before the first prompt
    readline.set_startup_hook(carriage_return)


def teardown_readline():
    """Tears down up the readline module, if available."""
    try:
        import readline
    except (ImportError, TypeError):
        return


def _rebind_case_sensitive_completions():
    # handle case sensitive, see Github issue #1342 for details
    global _RL_PREV_CASE_SENSITIVE_COMPLETIONS
    env = builtins.__xonsh__.env
    case_sensitive = env.get("CASE_SENSITIVE_COMPLETIONS")
    if case_sensitive is _RL_PREV_CASE_SENSITIVE_COMPLETIONS:
        return
    if case_sensitive:
        readline.parse_and_bind("set completion-ignore-case off")
    else:
        readline.parse_and_bind("set completion-ignore-case on")
    _RL_PREV_CASE_SENSITIVE_COMPLETIONS = case_sensitive


def fix_readline_state_after_ctrl_c():
    """
    Fix to allow Ctrl-C to exit reverse-i-search.

    Based on code from:
        http://bugs.python.org/file39467/raw_input__workaround_demo.py
    """
    if ON_WINDOWS:
        # hack to make pyreadline mimic the desired behavior
        try:
            _q = readline.rl.mode.process_keyevent_queue
            if len(_q) > 1:
                _q.pop()
        except Exception:
            pass
    if RL_STATE is None:
        return
    if RL_STATE.value & _RL_STATE_ISEARCH:
        RL_STATE.value &= ~_RL_STATE_ISEARCH
    if not RL_STATE.value & _RL_STATE_DONE:
        RL_STATE.value |= _RL_STATE_DONE


def rl_completion_suppress_append(val=1):
    """Sets the rl_completion_suppress_append variable, if possible.
    A value of 1 (default) means to suppress, a value of 0 means to enable.
    """
    if RL_COMPLETION_SUPPRESS_APPEND is None:
        return
    RL_COMPLETION_SUPPRESS_APPEND.value = val


def rl_completion_query_items(val=None):
    """Sets the rl_completion_query_items variable, if possible.
    A None value will set this to $COMPLETION_QUERY_LIMIT, otherwise any integer
    is accepted.
    """
    if RL_COMPLETION_QUERY_ITEMS is None:
        return
    if val is None:
        val = builtins.__xonsh__.env.get("COMPLETION_QUERY_LIMIT")
    RL_COMPLETION_QUERY_ITEMS.value = val


def rl_variable_dumper(readable=True):
    """Dumps the currently set readline variables. If readable is True, then this
    output may be used in an inputrc file.
    """
    RL_LIB.rl_variable_dumper(int(readable))


def rl_variable_value(variable):
    """Returns the currently set value for a readline configuration variable."""
    global RL_VARIABLE_VALUE
    if RL_VARIABLE_VALUE is None:
        import ctypes

        RL_VARIABLE_VALUE = RL_LIB.rl_variable_value
        RL_VARIABLE_VALUE.restype = ctypes.c_char_p
    env = builtins.__xonsh__.env
    enc, errors = env.get("XONSH_ENCODING"), env.get("XONSH_ENCODING_ERRORS")
    if isinstance(variable, str):
        variable = variable.encode(encoding=enc, errors=errors)
    rtn = RL_VARIABLE_VALUE(variable)
    return rtn.decode(encoding=enc, errors=errors)


@lazyobject
def rl_on_new_line():
    """Grabs one of a few possible redisplay functions in readline."""
    names = ["rl_on_new_line", "rl_forced_update_display", "rl_redisplay"]
    for name in names:
        func = getattr(RL_LIB, name, None)
        if func is not None:
            break
    else:

        def print_for_newline():
            print()

        func = print_for_newline
    return func


def _insert_text_func(s, readline):
    """Creates a function to insert text via readline."""

    def inserter():
        readline.insert_text(s)
        readline.redisplay()

    return inserter


DEDENT_TOKENS = LazyObject(
    lambda: frozenset(["raise", "return", "pass", "break", "continue"]),
    globals(),
    "DEDENT_TOKENS",
)


class ReadlineShell(BaseShell, cmd.Cmd):
    """The readline based xonsh shell."""

    def __init__(self, completekey="tab", stdin=None, stdout=None, **kwargs):
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout, **kwargs)
        setup_readline()
        self._current_indent = ""
        self._current_prompt = ""
        self._force_hide = None
        self._complete_only_last_table = {
            # Truth table for completions, keys are:
            # (prefix_begs_quote, prefix_ends_quote, i_ends_quote,
            #  last_starts_with_prefix, i_has_space)
            (True, True, True, True, True): True,
            (True, True, True, True, False): True,
            (True, True, True, False, True): False,
            (True, True, True, False, False): True,
            (True, True, False, True, True): False,
            (True, True, False, True, False): False,
            (True, True, False, False, True): False,
            (True, True, False, False, False): False,
            (True, False, True, True, True): True,
            (True, False, True, True, False): False,
            (True, False, True, False, True): False,
            (True, False, True, False, False): True,
            (True, False, False, True, True): False,
            (True, False, False, True, False): False,
            (True, False, False, False, True): False,
            (True, False, False, False, False): False,
            (False, True, True, True, True): True,
            (False, True, True, True, False): True,
            (False, True, True, False, True): True,
            (False, True, True, False, False): True,
            (False, True, False, True, True): False,
            (False, True, False, True, False): False,
            (False, True, False, False, True): False,
            (False, True, False, False, False): False,
            (False, False, True, True, True): False,
            (False, False, True, True, False): False,
            (False, False, True, False, True): False,
            (False, False, True, False, False): True,
            (False, False, False, True, True): True,
            (False, False, False, True, False): False,
            (False, False, False, False, True): False,
            (False, False, False, False, False): False,
        }
        self.cmdqueue = collections.deque()

    def __del__(self):
        teardown_readline()

    def singleline(self, store_in_history=True, **kwargs):
        """Reads a single line of input. The store_in_history kwarg
        flags whether the input should be stored in readline's in-memory
        history.
        """
        if not store_in_history:  # store current position to remove it later
            try:
                import readline
            except ImportError:
                store_in_history = True
            pos = readline.get_current_history_length() - 1
        events.on_pre_prompt.fire()
        rtn = input(self.prompt)
        events.on_post_prompt.fire()
        if not store_in_history and pos >= 0:
            readline.remove_history_item(pos)
        return rtn

    def parseline(self, line):
        """Overridden to no-op."""
        return "", line, line

    def _querycompletions(self, completions, loc):
        """Returns whether or not we should show completions. 0 means that prefixes
        should not be shown, 1 means that there is a common prefix among all completions
        and they should be shown, while 2 means that there is no common prefix but
        we are under the query limit and they should be shown.
        """
        if os.path.commonprefix([c[loc:] for c in completions]):
            return 1
        elif len(completions) <= builtins.__xonsh__.env.get("COMPLETION_QUERY_LIMIT"):
            return 2
        msg = "\nDisplay all {} possibilities? ".format(len(completions))
        msg += "({GREEN}y{NO_COLOR} or {RED}n{NO_COLOR})"
        self.print_color(msg, end="", flush=True, file=sys.stderr)
        yn = "x"
        while yn not in "yn":
            yn = sys.stdin.read(1)
        show_completions = to_bool(yn)
        print()
        if not show_completions:
            rl_on_new_line()
            return 0
        w, h = shutil.get_terminal_size()
        lines = columnize(completions, width=w)
        more_msg = self.format_color(
            "{YELLOW}==={NO_COLOR} more or "
            "{PURPLE}({NO_COLOR}q{PURPLE}){NO_COLOR}uit "
            "{YELLOW}==={NO_COLOR}"
        )
        while len(lines) > h - 1:
            print("".join(lines[: h - 1]), end="", flush=True, file=sys.stderr)
            lines = lines[h - 1 :]
            print(more_msg, end="", flush=True, file=sys.stderr)
            q = sys.stdin.read(1).lower()
            print(flush=True, file=sys.stderr)
            if q == "q":
                rl_on_new_line()
                return 0
        print("".join(lines), end="", flush=True, file=sys.stderr)
        rl_on_new_line()
        return 0

    def completedefault(self, prefix, line, begidx, endidx):
        """Implements tab-completion for text."""
        if self.completer is None:
            return []
        rl_completion_suppress_append()  # this needs to be called each time
        _rebind_case_sensitive_completions()
        rl_completion_query_items(val=999999999)
        completions, l = self.completer.complete(
            prefix, line, begidx, endidx, ctx=self.ctx
        )
        chopped = prefix[:-l]
        if chopped:
            rtn_completions = [chopped + i for i in completions]
        else:
            rtn_completions = completions
        rtn = []
        prefix_begs_quote = prefix.startswith("'") or prefix.startswith('"')
        prefix_ends_quote = prefix.endswith("'") or prefix.endswith('"')
        for i in rtn_completions:
            i_ends_quote = i.endswith("'") or i.endswith('"')
            last = i.rsplit(" ", 1)[-1]
            last_starts_prefix = last.startswith(prefix)
            i_has_space = " " in i
            key = (
                prefix_begs_quote,
                prefix_ends_quote,
                i_ends_quote,
                last_starts_prefix,
                i_has_space,
            )
            rtn.append(last if self._complete_only_last_table[key] else i)
        # return based on show completions
        show_completions = self._querycompletions(completions, endidx - begidx)
        if show_completions == 0:
            return []
        elif show_completions == 1:
            return rtn
        elif show_completions == 2:
            return completions
        else:
            raise ValueError("query completions flag not understood.")

    # tab complete on first index too
    completenames = completedefault

    def _load_remaining_input_into_queue(self):
        buf = b""
        while True:
            r, w, x = select.select([self.stdin], [], [], 1e-6)
            if len(r) == 0:
                break
            buf += os.read(self.stdin.fileno(), 1024)
        if len(buf) > 0:
            buf = buf.decode().replace("\r\n", "\n").replace("\r", "\n")
            self.cmdqueue.extend(buf.splitlines(keepends=True))

    def postcmd(self, stop, line):
        """Called just before execution of line. For readline, this handles the
        automatic indentation of code blocks.
        """
        try:
            import readline
        except ImportError:
            return stop
        if self.need_more_lines:
            if len(line.strip()) == 0:
                readline.set_pre_input_hook(None)
                self._current_indent = ""
            elif line.rstrip()[-1] == ":":
                ind = line[: len(line) - len(line.lstrip())]
                ind += builtins.__xonsh__.env.get("INDENT")
                readline.set_pre_input_hook(_insert_text_func(ind, readline))
                self._current_indent = ind
            elif line.split(maxsplit=1)[0] in DEDENT_TOKENS:
                env = builtins.__xonsh__.env
                ind = self._current_indent[: -len(env.get("INDENT"))]
                readline.set_pre_input_hook(_insert_text_func(ind, readline))
                self._current_indent = ind
            else:
                ind = line[: len(line) - len(line.lstrip())]
                if ind != self._current_indent:
                    insert_func = _insert_text_func(ind, readline)
                    readline.set_pre_input_hook(insert_func)
                    self._current_indent = ind
        else:
            readline.set_pre_input_hook(None)
        return stop

    def _cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        This was forked from Lib/cmd.py from the Python standard library v3.4.3,
        (C) Python Software Foundation, 2015.
        """
        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline

                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey + ": complete")
                have_readline = True
            except ImportError:
                have_readline = False
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
            stop = None
            while not stop:
                line = None
                exec_now = False
                if len(self.cmdqueue) > 0:
                    line = self.cmdqueue.popleft()
                    exec_now = line.endswith("\n")
                if self.use_rawinput and not exec_now:
                    inserter = (
                        None if line is None else _insert_text_func(line, readline)
                    )
                    if inserter is not None:
                        readline.set_pre_input_hook(inserter)
                    try:
                        line = self.singleline()
                    except EOFError:
                        if builtins.__xonsh__.env.get("IGNOREEOF"):
                            self.stdout.write('Use "exit" to leave the shell.' "\n")
                            line = ""
                        else:
                            line = "EOF"
                    if inserter is not None:
                        readline.set_pre_input_hook(None)
                else:
                    self.print_color(self.prompt, file=self.stdout)
                    if line is not None:
                        os.write(self.stdin.fileno(), line.encode())
                    if not exec_now:
                        line = self.stdin.readline()
                    if len(line) == 0:
                        line = "EOF"
                    else:
                        line = line.rstrip("\r\n")
                    if have_readline and line != "EOF":
                        readline.add_history(line)
                if not ON_WINDOWS:
                    # select() is not fully functional on windows
                    self._load_remaining_input_into_queue()
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
                if ON_WINDOWS:
                    winutils.enable_virtual_terminal_processing()
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline

                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass

    def cmdloop(self, intro=None):
        while not builtins.__xonsh__.exit:
            try:
                self._cmdloop(intro=intro)
            except (KeyboardInterrupt, SystemExit):
                print()  # Gives a newline
                fix_readline_state_after_ctrl_c()
                self.reset_buffer()
                intro = None

    @property
    def prompt(self):
        """Obtains the current prompt string."""
        global RL_LIB, RL_CAN_RESIZE
        if RL_CAN_RESIZE:
            # This is needed to support some system where line-wrapping doesn't
            # work. This is a bug in upstream Python, or possibly readline.
            RL_LIB.rl_reset_screen_size()
        if self.need_more_lines:
            if self.mlprompt is None:
                try:
                    self.mlprompt = multiline_prompt(curr=self._current_prompt)
                except Exception:  # pylint: disable=broad-except
                    print_exception()
                    self.mlprompt = "<multiline prompt error> "
            return self.mlprompt
        env = builtins.__xonsh__.env  # pylint: disable=no-member
        p = env.get("PROMPT")
        try:
            p = self.prompt_formatter(p)
        except Exception:  # pylint: disable=broad-except
            print_exception()
        hide = True if self._force_hide is None else self._force_hide
        p = ansi_partial_color_format(p, style=env.get("XONSH_COLOR_STYLE"), hide=hide)
        self._current_prompt = p
        self.settitle()
        return p

    def format_color(self, string, hide=False, force_string=False, **kwargs):
        """Readline implementation of color formatting. This uses ANSI color
        codes.
        """
        hide = hide if self._force_hide is None else self._force_hide
        style = builtins.__xonsh__.env.get("XONSH_COLOR_STYLE")
        return ansi_partial_color_format(string, hide=hide, style=style)

    def print_color(self, string, hide=False, **kwargs):
        if isinstance(string, str):
            s = self.format_color(string, hide=hide)
        else:
            # assume this is a list of (Token, str) tuples and format it
            env = builtins.__xonsh__.env
            self.styler.style_name = env.get("XONSH_COLOR_STYLE")
            style_proxy = pyghooks.xonsh_style_proxy(self.styler)
            formatter = pyghooks.XonshTerminal256Formatter(style=style_proxy)
            s = pygments.format(string, formatter).rstrip()
        print(s, **kwargs)

    def color_style_names(self):
        """Returns an iterable of all available style names."""
        return ansi_color_style_names()

    def color_style(self):
        """Returns the current color map."""
        style = style = builtins.__xonsh__.env.get("XONSH_COLOR_STYLE")
        return ansi_color_style(style=style)

    def restore_tty_sanity(self):
        """An interface for resetting the TTY stdin mode. This is highly
        dependent on the shell backend. Also it is mostly optional since
        it only affects ^Z backgrounding behaviour.
        """
        if not ON_POSIX:
            return
        stty, _ = builtins.__xonsh__.commands_cache.lazyget("stty", None)
        if stty is None:
            return
        # If available, we should just call the stty utility. This call should
        # not throw even if stty fails. It should also be noted that subprocess
        # calls, like the following, seem to be ineffective:
        #       subprocess.call([stty, 'sane'], shell=True)
        # My guess is that this is because Popen does some crazy redirecting
        # under the covers. This effectively hides the true TTY stdin handle
        # from stty. To get around this we have to use the lower level
        # os.system() function.
        os.system(stty + " sane")


class ReadlineHistoryAdder(threading.Thread):
    def __init__(self, wait_for_gc=True, *args, **kwargs):
        """Thread responsible for adding inputs from history to the
        current readline instance. May wait for the history garbage
        collector to finish.
        """
        super(ReadlineHistoryAdder, self).__init__(*args, **kwargs)
        self.daemon = True
        self.wait_for_gc = wait_for_gc
        self.start()

    def run(self):
        try:
            import readline
        except ImportError:
            return
        hist = builtins.__xonsh__.history
        if hist is None:
            return
        i = 1
        for h in hist.all_items():
            line = h["inp"].rstrip()
            if i == 1:
                pass
            elif line == readline.get_history_item(i - 1):
                continue
            readline.add_history(line)
            if RL_LIB is not None:
                RL_LIB.history_set_pos(i)
            i += 1

#
# replay
#
# -*- coding: utf-8 -*-
"""Tools to replay xonsh history files."""
# amalgamated json
# amalgamated time
# amalgamated builtins
# amalgamated collections.abc
# amalgamated xonsh.tools
# amalgamated xonsh.lazyjson
# amalgamated xonsh.environ
# amalgamated xonsh.history.main
DEFAULT_MERGE_ENVS = ("replay", "native")


class Replayer(object):
    """Replays a xonsh history file."""

    def __init__(self, f, reopen=True):
        """
        Parameters
        ----------
        f : file handle or str
            Path to xonsh history file.
        reopen : bool, optional
            Whether new file handle should be opened for each load, passed directly into
            LazyJSON class.
        """
        self._lj = LazyJSON(f, reopen=reopen)

    def __del__(self):
        self._lj.close()

    def replay(self, merge_envs=DEFAULT_MERGE_ENVS, target=None):
        """Replays the history specified, returns the history object where the code
        was executed.

        Parameters
        ----------
        merge_env : tuple of str or Mappings, optional
            Describes how to merge the environments, in order of increasing precedence.
            Available strings are 'replay' and 'native'. The 'replay' env comes from the
            history file that we are replaying. The 'native' env comes from what this
            instance of xonsh was started up with. Instead of a string, a dict or other
            mapping may be passed in as well. Defaults to ('replay', 'native').
        target : str, optional
            Path to new history file.
        """
        shell = builtins.__xonsh__.shell
        re_env = self._lj["env"].load()
        new_env = self._merge_envs(merge_envs, re_env)
        new_hist = xhm.construct_history(
            env=new_env.detype(),
            locked=True,
            ts=[time.time(), None],
            gc=False,
            filename=target,
        )
        with swap(builtins.__xonsh__, "env", new_env), swap(
            builtins.__xonsh__, "history", new_hist
        ):
            for cmd in self._lj["cmds"]:
                inp = cmd["inp"]
                shell.default(inp)
                if builtins.__xonsh__.exit:  # prevent premature exit
                    builtins.__xonsh__.exit = False
        new_hist.flush(at_exit=True)
        return new_hist

    def _merge_envs(self, merge_envs, re_env):
        new_env = {}
        for e in merge_envs:
            if e == "replay":
                new_env.update(re_env)
            elif e == "native":
                new_env.update(builtins.__xonsh__.env)
            elif isinstance(e, cabc.Mapping):
                new_env.update(e)
            else:
                raise TypeError("Type of env not understood: {0!r}".format(e))
        new_env = Env(**new_env)
        return new_env


_REPLAY_PARSER = None


def replay_create_parser(p=None):
    global _REPLAY_PARSER
    p_was_none = p is None
    if _REPLAY_PARSER is not None and p_was_none:
        return _REPLAY_PARSER
    if p_was_none:
        from argparse import ArgumentParser

        p = ArgumentParser("replay", description="replays a xonsh history file")
    p.add_argument(
        "--merge-envs",
        dest="merge_envs",
        default=DEFAULT_MERGE_ENVS,
        nargs="+",
        help="Describes how to merge the environments, in order of "
        "increasing precedence. Available strings are 'replay' and "
        "'native'. The 'replay' env comes from the history file that we "
        "are replaying. The 'native' env comes from what this instance "
        "of xonsh was started up with. One or more of these options may "
        "be passed in. Defaults to '--merge-envs replay native'.",
    )
    p.add_argument(
        "--json",
        dest="json",
        default=False,
        action="store_true",
        help="print history info in JSON format",
    )
    p.add_argument(
        "-o", "--target", dest="target", default=None, help="path to new history file"
    )
    p.add_argument("path", help="path to replay history file")
    if p_was_none:
        _REPLAY_PARSER = p
    return p


def replay_main_action(h, ns, stdout=None, stderr=None):
    replayer = Replayer(ns.path)
    hist = replayer.replay(merge_envs=ns.merge_envs, target=ns.target)
    print("----------------------------------------------------------------")
    print("Just replayed history, new history has the following information")
    print("----------------------------------------------------------------")
    data = hist.info()
    if ns.json:
        s = json.dumps(data)
        print(s, file=stdout)
    else:
        lines = ["{0}: {1}".format(k, v) for k, v in data.items()]
        print("\n".join(lines), file=stdout)


def replay_main(args, stdin=None):
    """Acts as main function for replaying a xonsh history file."""
    parser = replay_create_parser()
    ns = parser.parse_args(args)
    replay_main_action(ns)

#
# tracer
#
"""Implements a xonsh tracer."""
# amalgamated os
# amalgamated re
# amalgamated sys
# amalgamated inspect
# amalgamated argparse
# amalgamated linecache
# amalgamated importlib
# amalgamated functools
# amalgamated xonsh.lazyasd
# amalgamated xonsh.platform
# amalgamated xonsh.tools
# amalgamated xonsh.inspectors
# amalgamated xonsh.lazyimps
# amalgamated xonsh.proc
prompt = _LazyModule.load('xonsh', 'xonsh.prompt.cwd', 'prompt')
terminal = LazyObject(
    lambda: importlib.import_module("pygments.formatters.terminal"),
    globals(),
    "terminal",
)


class TracerType(object):
    """Represents a xonsh tracer object, which keeps track of all tracing
    state. This is a singleton.
    """

    _inst = None
    valid_events = frozenset(["line", "call"])

    def __new__(cls, *args, **kwargs):
        if cls._inst is None:
            cls._inst = super(TracerType, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    def __init__(self):
        self.prev_tracer = DefaultNotGiven
        self.files = set()
        self.usecolor = True
        self.lexer = pyghooks.XonshLexer()
        self.formatter = terminal.TerminalFormatter()
        self._last = ("", -1)  # filename, lineno tuple

    def __del__(self):
        for f in set(self.files):
            self.stop(f)

    def color_output(self, usecolor):
        """Specify whether or not the tracer output should be colored."""
        # we have to use a function to set usecolor because of the way that
        # lazyasd works. Namely, it cannot dispatch setattr to the target
        # object without being unable to access its own __dict__. This makes
        # setting an attr look like getting a function.
        self.usecolor = usecolor

    def start(self, filename):
        """Starts tracing a file."""
        files = self.files
        if len(files) == 0:
            self.prev_tracer = sys.gettrace()
        files.add(normabspath(filename))
        sys.settrace(self.trace)
        curr = inspect.currentframe()
        for frame, fname, *_ in getouterframes(curr, context=0):
            if normabspath(fname) in files:
                frame.f_trace = self.trace

    def stop(self, filename):
        """Stops tracing a file."""
        filename = normabspath(filename)
        self.files.discard(filename)
        if len(self.files) == 0:
            sys.settrace(self.prev_tracer)
            curr = inspect.currentframe()
            for frame, fname, *_ in getouterframes(curr, context=0):
                if normabspath(fname) == filename:
                    frame.f_trace = self.prev_tracer
            self.prev_tracer = DefaultNotGiven

    def trace(self, frame, event, arg):
        """Implements a line tracing function."""
        if event not in self.valid_events:
            return self.trace
        fname = find_file(frame)
        if fname in self.files:
            lineno = frame.f_lineno
            curr = (fname, lineno)
            if curr != self._last:
                line = linecache.getline(fname, lineno).rstrip()
                s = tracer_format_line(
                    fname,
                    lineno,
                    line,
                    color=self.usecolor,
                    lexer=self.lexer,
                    formatter=self.formatter,
                )
                print_color(s)
                self._last = curr
        return self.trace


tracer = LazyObject(TracerType, globals(), "tracer")

COLORLESS_LINE = "{fname}:{lineno}:{line}"
COLOR_LINE = "{{PURPLE}}{fname}{{BLUE}}:" "{{GREEN}}{lineno}{{BLUE}}:" "{{NO_COLOR}}"


def tracer_format_line(fname, lineno, line, color=True, lexer=None, formatter=None):
    """Formats a trace line suitable for printing."""
    fname = min(fname, prompt._replace_home(fname), os.path.relpath(fname), key=len)
    if not color:
        return COLORLESS_LINE.format(fname=fname, lineno=lineno, line=line)
    cline = COLOR_LINE.format(fname=fname, lineno=lineno)
    if not HAS_PYGMENTS:
        return cline + line
    # OK, so we have pygments
    tokens = pyghooks.partial_color_tokenize(cline)
    lexer = lexer or pyghooks.XonshLexer()
    tokens += pygments.lex(line, lexer=lexer)
    if tokens[-1][1] == "\n":
        del tokens[-1]
    elif tokens[-1][1].endswith("\n"):
        tokens[-1] = (tokens[-1][0], tokens[-1][1].rstrip())
    return tokens


#
# Command line interface
#


def _find_caller(args):
    """Somewhat hacky method of finding the __file__ based on the line executed."""
    re_line = re.compile(r"[^;\s|&<>]+\s+" + r"\s+".join(args))
    curr = inspect.currentframe()
    for _, fname, lineno, _, lines, _ in getouterframes(curr, context=1)[3:]:
        if lines is not None and re_line.search(lines[0]) is not None:
            return fname
        elif (
            lineno == 1 and re_line.search(linecache.getline(fname, lineno)) is not None
        ):
            # There is a bug in CPython such that getouterframes(curr, context=1)
            # will actually return the 2nd line in the code_context field, even though
            # line number is itself correct. We manually fix that in this branch.
            return fname
    else:
        msg = (
            "xonsh: warning: __file__ name could not be found. You may be "
            "trying to trace interactively. Please pass in the file names "
            "you want to trace explicitly."
        )
        print(msg, file=sys.stderr)


def _on(ns, args):
    """Turns on tracing for files."""
    for f in ns.files:
        if f == "__file__":
            f = _find_caller(args)
        if f is None:
            continue
        tracer.start(f)


def _off(ns, args):
    """Turns off tracing for files."""
    for f in ns.files:
        if f == "__file__":
            f = _find_caller(args)
        if f is None:
            continue
        tracer.stop(f)


def _color(ns, args):
    """Manages color action for tracer CLI."""
    tracer.color_output(ns.toggle)


@functools.lru_cache(1)
def _tracer_create_parser():
    """Creates tracer argument parser"""
    p = argparse.ArgumentParser(
        prog="trace", description="tool for tracing xonsh code as it runs."
    )
    subp = p.add_subparsers(title="action", dest="action")
    onp = subp.add_parser(
        "on", aliases=["start", "add"], help="begins tracing selected files."
    )
    onp.add_argument(
        "files",
        nargs="*",
        default=["__file__"],
        help=(
            'file paths to watch, use "__file__" (default) to select '
            "the current file."
        ),
    )
    off = subp.add_parser(
        "off", aliases=["stop", "del", "rm"], help="removes selected files fom tracing."
    )
    off.add_argument(
        "files",
        nargs="*",
        default=["__file__"],
        help=(
            'file paths to stop watching, use "__file__" (default) to '
            "select the current file."
        ),
    )
    col = subp.add_parser("color", help="output color management for tracer.")
    col.add_argument(
        "toggle", type=to_bool, help="true/false, y/n, etc. to toggle color usage."
    )
    return p


_TRACER_MAIN_ACTIONS = {
    "on": _on,
    "add": _on,
    "start": _on,
    "rm": _off,
    "off": _off,
    "del": _off,
    "stop": _off,
    "color": _color,
}


def tracermain(args=None, stdin=None, stdout=None, stderr=None, spec=None):
    """Main function for tracer command-line interface."""
    parser = _tracer_create_parser()
    ns = parser.parse_args(args)
    usecolor = (spec.captured not in STDOUT_CAPTURE_KINDS) and sys.stdout.isatty()
    tracer.color_output(usecolor)
    return _TRACER_MAIN_ACTIONS[ns.action](ns, args)

#
# aliases
#
# -*- coding: utf-8 -*-
"""Aliases for the xonsh shell."""
# amalgamated os
# amalgamated re
# amalgamated sys
# amalgamated inspect
# amalgamated argparse
# amalgamated builtins
# amalgamated collections.abc
# amalgamated xonsh.lazyasd
# amalgamated xonsh.dirstack
# amalgamated xonsh.environ
# amalgamated xonsh.foreign_shells
# amalgamated xonsh.jobs
# amalgamated xonsh.platform
# amalgamated xonsh.tools
# amalgamated xonsh.replay
# amalgamated xonsh.timings
# amalgamated xonsh.tools
# amalgamated xonsh.xontribs
# amalgamated xonsh.ast
xca = _LazyModule.load('xonsh', 'xonsh.completers._aliases', 'xca')
# amalgamated xonsh.history.main
xxw = _LazyModule.load('xonsh', 'xonsh.xoreutils.which', 'xxw')
@lazyobject
def SUB_EXEC_ALIAS_RE():
    return re.compile(r"@\(|\$\(|!\(|\$\[|!\[")


class Aliases(cabc.MutableMapping):
    """Represents a location to hold and look up aliases."""

    def __init__(self, *args, **kwargs):
        self._raw = {}
        self.update(*args, **kwargs)

    def get(self, key, default=None):
        """Returns the (possibly modified) value. If the key is not present,
        then `default` is returned.
        If the value is callable, it is returned without modification. If it
        is an iterable of strings it will be evaluated recursively to expand
        other aliases, resulting in a new list or a "partially applied"
        callable.
        """
        val = self._raw.get(key)
        if val is None:
            return default
        elif isinstance(val, cabc.Iterable) or callable(val):
            return self.eval_alias(val, seen_tokens={key})
        else:
            msg = "alias of {!r} has an inappropriate type: {!r}"
            raise TypeError(msg.format(key, val))

    def eval_alias(self, value, seen_tokens=frozenset(), acc_args=()):
        """
        "Evaluates" the alias `value`, by recursively looking up the leftmost
        token and "expanding" if it's also an alias.

        A value like ["cmd", "arg"] might transform like this:
        > ["cmd", "arg"] -> ["ls", "-al", "arg"] -> callable()
        where `cmd=ls -al` and `ls` is an alias with its value being a
        callable.  The resulting callable will be "partially applied" with
        ["-al", "arg"].
        """
        # Beware of mutability: default values for keyword args are evaluated
        # only once.
        if callable(value):
            if acc_args:  # Partial application

                def _alias(args, stdin=None):
                    args = list(acc_args) + args
                    return value(args, stdin=stdin)

                return _alias
            else:
                return value
        else:
            expand_path = builtins.__xonsh__.expand_path
            token, *rest = map(expand_path, value)
            if token in seen_tokens or token not in self._raw:
                # ^ Making sure things like `egrep=egrep --color=auto` works,
                # and that `l` evals to `ls --color=auto -CF` if `l=ls -CF`
                # and `ls=ls --color=auto`
                rtn = [token]
                rtn.extend(rest)
                rtn.extend(acc_args)
                return rtn
            else:
                seen_tokens = seen_tokens | {token}
                acc_args = rest + list(acc_args)
                return self.eval_alias(self._raw[token], seen_tokens, acc_args)

    def expand_alias(self, line):
        """Expands any aliases present in line if alias does not point to a
        builtin function and if alias is only a single command.
        """
        word = line.split(" ", 1)[0]
        if word in builtins.aliases and isinstance(self.get(word), cabc.Sequence):
            word_idx = line.find(word)
            expansion = " ".join(self.get(word))
            line = line[:word_idx] + expansion + line[word_idx + len(word) :]
        return line

    #
    # Mutable mapping interface
    #

    def __getitem__(self, key):
        return self._raw[key]

    def __setitem__(self, key, val):
        if isinstance(val, str):
            f = "<exec-alias:" + key + ">"
            if SUB_EXEC_ALIAS_RE.search(val) is not None:
                # We have a sub-command, e.g. $(cmd), to evaluate
                self._raw[key] = ExecAlias(val, filename=f)
            elif isexpression(val):
                # expansion substitution
                lexer = builtins.__xonsh__.execer.parser.lexer
                self._raw[key] = list(map(strip_simple_quotes, lexer.split(val)))
            else:
                # need to exec alias
                self._raw[key] = ExecAlias(val, filename=f)
        else:
            self._raw[key] = val

    def __delitem__(self, key):
        del self._raw[key]

    def update(self, *args, **kwargs):
        for key, val in dict(*args, **kwargs).items():
            self[key] = val

    def __iter__(self):
        yield from self._raw

    def __len__(self):
        return len(self._raw)

    def __str__(self):
        return str(self._raw)

    def __repr__(self):
        return "{0}.{1}({2})".format(
            self.__class__.__module__, self.__class__.__name__, self._raw
        )

    def _repr_pretty_(self, p, cycle):
        name = "{0}.{1}".format(self.__class__.__module__, self.__class__.__name__)
        with p.group(0, name + "(", ")"):
            if cycle:
                p.text("...")
            elif len(self):
                p.break_()
                p.pretty(dict(self))


class ExecAlias:
    """Provides a callable alias for xonsh source code."""

    def __init__(self, src, filename="<exec-alias>"):
        """
        Parameters
        ----------
        src : str
            Source code that will be
        """
        self.src = src if src.endswith("\n") else src + "\n"
        self.filename = filename

    def __call__(
        self, args, stdin=None, stdout=None, stderr=None, spec=None, stack=None
    ):
        execer = builtins.__xonsh__.execer
        frame = stack[0][0]  # execute as though we are at the call site
        execer.exec(
            self.src, glbs=frame.f_globals, locs=frame.f_locals, filename=self.filename
        )

    def __repr__(self):
        return "ExecAlias({0!r}, filename={1!r})".format(self.src, self.filename)


#
# Actual aliases below
#


def xonsh_exit(args, stdin=None):
    """Sends signal to exit shell."""
    if not clean_jobs():
        # Do not exit if jobs not cleaned up
        return None, None
    builtins.__xonsh__.exit = True
    print()  # gimme a newline
    return None, None


def xonsh_reset(args, stdin=None):
    """ Clears __xonsh__.ctx"""
    builtins.__xonsh__.ctx.clear()


@lazyobject
def _SOURCE_FOREIGN_PARSER():
    desc = "Sources a file written in a foreign shell language."
    parser = argparse.ArgumentParser("source-foreign", description=desc)
    parser.add_argument("shell", help="Name or path to the foreign shell")
    parser.add_argument(
        "files_or_code",
        nargs="+",
        help="file paths to source or code in the target " "language.",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        type=to_bool,
        default=True,
        help="whether the sourced shell should be interactive",
        dest="interactive",
    )
    parser.add_argument(
        "-l",
        "--login",
        type=to_bool,
        default=False,
        help="whether the sourced shell should be login",
        dest="login",
    )
    parser.add_argument(
        "--envcmd", default=None, dest="envcmd", help="command to print environment"
    )
    parser.add_argument(
        "--aliascmd", default=None, dest="aliascmd", help="command to print aliases"
    )
    parser.add_argument(
        "--extra-args",
        default=(),
        dest="extra_args",
        type=(lambda s: tuple(s.split())),
        help="extra arguments needed to run the shell",
    )
    parser.add_argument(
        "-s",
        "--safe",
        type=to_bool,
        default=True,
        help="whether the source shell should be run safely, "
        "and not raise any errors, even if they occur.",
        dest="safe",
    )
    parser.add_argument(
        "-p",
        "--prevcmd",
        default=None,
        dest="prevcmd",
        help="command(s) to run before any other commands, "
        "replaces traditional source.",
    )
    parser.add_argument(
        "--postcmd",
        default="",
        dest="postcmd",
        help="command(s) to run after all other commands",
    )
    parser.add_argument(
        "--funcscmd",
        default=None,
        dest="funcscmd",
        help="code to find locations of all native functions " "in the shell language.",
    )
    parser.add_argument(
        "--sourcer",
        default=None,
        dest="sourcer",
        help="the source command in the target shell " "language, default: source.",
    )
    parser.add_argument(
        "--use-tmpfile",
        type=to_bool,
        default=False,
        help="whether the commands for source shell should be "
        "written to a temporary file.",
        dest="use_tmpfile",
    )
    parser.add_argument(
        "--seterrprevcmd",
        default=None,
        dest="seterrprevcmd",
        help="command(s) to set exit-on-error before any" "other commands.",
    )
    parser.add_argument(
        "--seterrpostcmd",
        default=None,
        dest="seterrpostcmd",
        help="command(s) to set exit-on-error after all" "other commands.",
    )
    parser.add_argument(
        "--overwrite-aliases",
        default=False,
        action="store_true",
        dest="overwrite_aliases",
        help="flag for whether or not sourced aliases should "
        "replace the current xonsh aliases.",
    )
    parser.add_argument(
        "--suppress-skip-message",
        default=None,
        action="store_true",
        dest="suppress_skip_message",
        help="flag for whether or not skip messages should be suppressed.",
    )
    parser.add_argument(
        "--show",
        default=False,
        action="store_true",
        dest="show",
        help="Will show the script output.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        default=False,
        action="store_true",
        dest="dryrun",
        help="Will not actually source the file.",
    )
    return parser


def source_foreign(args, stdin=None, stdout=None, stderr=None):
    """Sources a file written in a foreign shell language."""
    env = builtins.__xonsh__.env
    ns = _SOURCE_FOREIGN_PARSER.parse_args(args)
    ns.suppress_skip_message = (
        env.get("FOREIGN_ALIASES_SUPPRESS_SKIP_MESSAGE")
        if ns.suppress_skip_message is None
        else ns.suppress_skip_message
    )
    if ns.prevcmd is not None:
        pass  # don't change prevcmd if given explicitly
    elif os.path.isfile(ns.files_or_code[0]):
        # we have filename to source
        ns.prevcmd = '{} "{}"'.format(ns.sourcer, '" "'.join(ns.files_or_code))
    elif ns.prevcmd is None:
        ns.prevcmd = " ".join(ns.files_or_code)  # code to run, no files
    foreign_shell_data.cache_clear()  # make sure that we don't get prev src
    fsenv, fsaliases = foreign_shell_data(
        shell=ns.shell,
        login=ns.login,
        interactive=ns.interactive,
        envcmd=ns.envcmd,
        aliascmd=ns.aliascmd,
        extra_args=ns.extra_args,
        safe=ns.safe,
        prevcmd=ns.prevcmd,
        postcmd=ns.postcmd,
        funcscmd=ns.funcscmd,
        sourcer=ns.sourcer,
        use_tmpfile=ns.use_tmpfile,
        seterrprevcmd=ns.seterrprevcmd,
        seterrpostcmd=ns.seterrpostcmd,
        show=ns.show,
        dryrun=ns.dryrun,
    )
    if fsenv is None:
        if ns.dryrun:
            return
        else:
            msg = "xonsh: error: Source failed: {0!r}\n".format(ns.prevcmd)
            msg += "xonsh: error: Possible reasons: File not found or syntax error\n"
            return (None, msg, 1)
    # apply results
    denv = env.detype()
    for k, v in fsenv.items():
        if k in denv and v == denv[k]:
            continue  # no change from original
        env[k] = v
    # Remove any env-vars that were unset by the script.
    for k in denv:
        if k not in fsenv:
            env.pop(k, None)
    # Update aliases
    baliases = builtins.aliases
    for k, v in fsaliases.items():
        if k in baliases and v == baliases[k]:
            continue  # no change from original
        elif ns.overwrite_aliases or k not in baliases:
            baliases[k] = v
        elif ns.suppress_skip_message:
            pass
        else:
            msg = (
                "Skipping application of {0!r} alias from {1!r} "
                "since it shares a name with an existing xonsh alias. "
                'Use "--overwrite-alias" option to apply it anyway.'
                'You may prevent this message with "--suppress-skip-message" or '
                '"$FOREIGN_ALIASES_SUPPRESS_SKIP_MESSAGE = True".'
            )
            print(msg.format(k, ns.shell), file=stderr)


def source_alias(args, stdin=None):
    """Executes the contents of the provided files in the current context.
    If sourced file isn't found in cwd, search for file along $PATH to source
    instead.
    """
    env = builtins.__xonsh__.env
    encoding = env.get("XONSH_ENCODING")
    errors = env.get("XONSH_ENCODING_ERRORS")
    for i, fname in enumerate(args):
        fpath = fname
        if not os.path.isfile(fpath):
            fpath = locate_binary(fname)
            if fpath is None:
                if env.get("XONSH_DEBUG"):
                    print("source: {}: No such file".format(fname), file=sys.stderr)
                if i == 0:
                    raise RuntimeError(
                        "must source at least one file, " + fname + "does not exist."
                    )
                break
        _, fext = os.path.splitext(fpath)
        if fext and fext != ".xsh" and fext != ".py":
            raise RuntimeError(
                "attempting to source non-xonsh file! If you are "
                "trying to source a file in another language, "
                "then please use the appropriate source command. "
                "For example, source-bash script.sh"
            )
        with open(fpath, "r", encoding=encoding, errors=errors) as fp:
            src = fp.read()
        if not src.endswith("\n"):
            src += "\n"
        ctx = builtins.__xonsh__.ctx
        updates = {"__file__": fpath, "__name__": os.path.abspath(fpath)}
        with env.swap(**make_args_env(args[i + 1 :])), swap_values(ctx, updates):
            try:
                builtins.execx(src, "exec", ctx, filename=fpath)
            except Exception:
                print_color(
                    "{RED}You may be attempting to source non-xonsh file! "
                    "{NO_COLOR}If you are trying to source a file in "
                    "another language, then please use the appropriate "
                    "source command. For example, {GREEN}source-bash "
                    "script.sh{NO_COLOR}",
                    file=sys.stderr,
                )
                raise


def source_cmd(args, stdin=None):
    """Simple cmd.exe-specific wrapper around source-foreign."""
    args = list(args)
    fpath = locate_binary(args[0])
    args[0] = fpath if fpath else args[0]
    if not os.path.isfile(args[0]):
        return (None, "xonsh: error: File not found: {}\n".format(args[0]), 1)
    prevcmd = "call "
    prevcmd += " ".join([argvquote(arg, force=True) for arg in args])
    prevcmd = escape_windows_cmd_string(prevcmd)
    args.append("--prevcmd={}".format(prevcmd))
    args.insert(0, "cmd")
    args.append("--interactive=0")
    args.append("--sourcer=call")
    args.append("--envcmd=set")
    args.append("--seterrpostcmd=if errorlevel 1 exit 1")
    args.append("--use-tmpfile=1")
    with builtins.__xonsh__.env.swap(PROMPT="$P$G"):
        return source_foreign(args, stdin=stdin)


def xexec(args, stdin=None):
    """exec [-h|--help] command [args...]

    exec (also aliased as xexec) uses the os.execvpe() function to
    replace the xonsh process with the specified program. This provides
    the functionality of the bash 'exec' builtin::

        >>> exec bash -l -i
        bash $

    The '-h' and '--help' options print this message and exit.

    Notes
    -----
    This command **is not** the same as the Python builtin function
    exec(). That function is for running Python code. This command,
    which shares the same name as the sh-lang statement, is for launching
    a command directly in the same process. In the event of a name conflict,
    please use the xexec command directly or dive into subprocess mode
    explicitly with ![exec command]. For more details, please see
    http://xon.sh/faq.html#exec.
    """
    if len(args) == 0:
        return (None, "xonsh: exec: no args specified\n", 1)
    elif args[0] == "-h" or args[0] == "--help":
        return inspect.getdoc(xexec)
    else:
        denv = builtins.__xonsh__.env.detype()
        try:
            os.execvpe(args[0], args, denv)
        except FileNotFoundError as e:
            return (
                None,
                "xonsh: exec: file not found: {}: {}" "\n".format(e.args[1], args[0]),
                1,
            )


class AWitchAWitch(argparse.Action):
    SUPPRESS = "==SUPPRESS=="

    def __init__(
        self, option_strings, version=None, dest=SUPPRESS, default=SUPPRESS, **kwargs
    ):
        super().__init__(
            option_strings=option_strings, dest=dest, default=default, nargs=0, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        import webbrowser

        webbrowser.open("https://github.com/xonsh/xonsh/commit/f49b400")
        parser.exit()


def xonfig(args, stdin=None):
    """Runs the xonsh configuration utility."""
    from xonsh.xonfig import xonfig_main  # lazy import

    return xonfig_main(args)


@unthreadable
def trace(args, stdin=None, stdout=None, stderr=None, spec=None):
    """Runs the xonsh tracer utility."""
    from xonsh.tracer import tracermain  # lazy import

    try:
        return tracermain(args, stdin=stdin, stdout=stdout, stderr=stderr, spec=spec)
    except SystemExit:
        pass


def showcmd(args, stdin=None):
    """usage: showcmd [-h|--help|cmd args]

    Displays the command and arguments as a list of strings that xonsh would
    run in subprocess mode. This is useful for determining how xonsh evaluates
    your commands and arguments prior to running these commands.

    optional arguments:
      -h, --help            show this help message and exit

    example:
      >>> showcmd echo $USER can't hear "the sea"
      ['echo', 'I', "can't", 'hear', 'the sea']
    """
    if len(args) == 0 or (len(args) == 1 and args[0] in {"-h", "--help"}):
        print(showcmd.__doc__.rstrip().replace("\n    ", "\n"))
    else:
        sys.displayhook(args)


def detect_xpip_alias():
    """
    Determines the correct invocation to get xonsh's pip
    """
    if not getattr(sys, "executable", None):
        return lambda args, stdin=None: (
            "",
            "Sorry, unable to run pip on your system (missing sys.executable)",
            1,
        )

    basecmd = [sys.executable, "-m", "pip"]
    try:
        if ON_WINDOWS:
            # XXX: Does windows have an installation mode that requires UAC?
            return basecmd
        elif not os.access(os.path.dirname(sys.executable), os.W_OK):
            return ["sudo"] + basecmd
        else:
            return basecmd
    except Exception:
        # Something freaky happened, return something that'll probably work
        return basecmd


def make_default_aliases():
    """Creates a new default aliases dictionary."""
    default_aliases = {
        "cd": cd,
        "pushd": pushd,
        "popd": popd,
        "dirs": dirs,
        "jobs": jobs,
        "fg": fg,
        "bg": bg,
        "EOF": xonsh_exit,
        "exit": xonsh_exit,
        "quit": xonsh_exit,
        "exec": xexec,
        "xexec": xexec,
        "source": source_alias,
        "source-zsh": ["source-foreign", "zsh", "--sourcer=source"],
        "source-bash": ["source-foreign", "bash", "--sourcer=source"],
        "source-cmd": source_cmd,
        "source-foreign": source_foreign,
        "history": xhm.history_main,
        "replay": replay_main,
        "trace": trace,
        "timeit": timeit_alias,
        "xonfig": xonfig,
        "scp-resume": ["rsync", "--partial", "-h", "--progress", "--rsh=ssh"],
        "showcmd": showcmd,
        "ipynb": ["jupyter", "notebook", "--no-browser"],
        "which": xxw.which,
        "xontrib": xontribs_main,
        "completer": xca.completer_alias,
        "xpip": detect_xpip_alias(),
        "xonsh-reset": xonsh_reset,
    }
    if ON_WINDOWS:
        # Borrow builtin commands from cmd.exe.
        windows_cmd_aliases = {
            "cls",
            "copy",
            "del",
            "dir",
            "echo",
            "erase",
            "md",
            "mkdir",
            "mklink",
            "move",
            "rd",
            "ren",
            "rename",
            "rmdir",
            "time",
            "type",
            "vol",
        }
        for alias in windows_cmd_aliases:
            default_aliases[alias] = ["cmd", "/c", alias]
        default_aliases["call"] = ["source-cmd"]
        default_aliases["source-bat"] = ["source-cmd"]
        default_aliases["clear"] = "cls"
        if ON_ANACONDA:
            # Add aliases specific to the Anaconda python distribution.
            default_aliases["activate"] = ["source-cmd", "activate.bat"]
            default_aliases["deactivate"] = ["source-cmd", "deactivate.bat"]
        if not locate_binary("sudo"):
            import xonsh.winutils as winutils

            def sudo(args):
                if len(args) < 1:
                    print(
                        "You need to provide an executable to run as " "Administrator."
                    )
                    return
                cmd = args[0]
                if locate_binary(cmd):
                    return winutils.sudo(cmd, args[1:])
                elif cmd.lower() in windows_cmd_aliases:
                    args = ["/D", "/C", "CD", _get_cwd(), "&&"] + args
                    return winutils.sudo("cmd", args)
                else:
                    msg = 'Cannot find the path for executable "{0}".'
                    print(msg.format(cmd))

            default_aliases["sudo"] = sudo
    elif ON_DARWIN:
        default_aliases["ls"] = ["ls", "-G"]
    elif ON_FREEBSD or ON_DRAGONFLY:
        default_aliases["grep"] = ["grep", "--color=auto"]
        default_aliases["egrep"] = ["egrep", "--color=auto"]
        default_aliases["fgrep"] = ["fgrep", "--color=auto"]
        default_aliases["ls"] = ["ls", "-G"]
    elif ON_NETBSD:
        default_aliases["grep"] = ["grep", "--color=auto"]
        default_aliases["egrep"] = ["egrep", "--color=auto"]
        default_aliases["fgrep"] = ["fgrep", "--color=auto"]
    else:
        default_aliases["grep"] = ["grep", "--color=auto"]
        default_aliases["egrep"] = ["egrep", "--color=auto"]
        default_aliases["fgrep"] = ["fgrep", "--color=auto"]
        default_aliases["ls"] = ["ls", "--color=auto", "-v"]
    return default_aliases

#
# dumb_shell
#
"""A dumb shell for when $TERM == 'dumb', which usually happens in emacs."""
# amalgamated builtins
# amalgamated xonsh.readline_shell
class DumbShell(ReadlineShell):
    """A dumb shell for when $TERM == 'dumb', which usually happens in emacs."""

    def __init__(self, *args, **kwargs):
        builtins.__xonsh__.env["XONSH_COLOR_STYLE"] = "emacs"
        super().__init__(*args, **kwargs)

#
# built_ins
#
# -*- coding: utf-8 -*-
"""The xonsh built-ins.

Note that this module is named 'built_ins' so as not to be confused with the
special Python builtins module.
"""
# amalgamated io
# amalgamated os
# amalgamated re
# amalgamated sys
# amalgamated types
# amalgamated shlex
# amalgamated signal
atexit = _LazyModule.load('atexit', 'atexit')
# amalgamated pathlib
# amalgamated inspect
# amalgamated warnings
# amalgamated builtins
# amalgamated itertools
# amalgamated subprocess
# amalgamated contextlib
# amalgamated collections.abc
# amalgamated xonsh.ast
# amalgamated xonsh.lazyasd
# amalgamated xonsh.inspectors
# amalgamated xonsh.aliases
# amalgamated xonsh.environ
# amalgamated xonsh.jobs
# amalgamated xonsh.platform
# amalgamated xonsh.proc
# amalgamated xonsh.tools
# amalgamated xonsh.lazyimps
# amalgamated xonsh.commands_cache
# amalgamated xonsh.events
xonsh = _LazyModule.load('xonsh', 'xonsh.completers.init')
BUILTINS_LOADED = False
INSPECTOR = LazyObject(Inspector, globals(), "INSPECTOR")

warnings.filterwarnings("once", category=DeprecationWarning)


@lazyobject
def AT_EXIT_SIGNALS():
    sigs = (
        signal.SIGABRT,
        signal.SIGFPE,
        signal.SIGILL,
        signal.SIGSEGV,
        signal.SIGTERM,
    )
    if ON_POSIX:
        sigs += (signal.SIGTSTP, signal.SIGQUIT, signal.SIGHUP)
    return sigs


def resetting_signal_handle(sig, f):
    """Sets a new signal handle that will automatically restore the old value
    once the new handle is finished.
    """
    oldh = signal.getsignal(sig)

    def newh(s=None, frame=None):
        f(s, frame)
        signal.signal(sig, oldh)
        if sig != 0:
            sys.exit(sig)

    signal.signal(sig, newh)


def helper(x, name=""):
    """Prints help about, and then returns that variable."""
    INSPECTOR.pinfo(x, oname=name, detail_level=0)
    return x


def superhelper(x, name=""):
    """Prints help about, and then returns that variable."""
    INSPECTOR.pinfo(x, oname=name, detail_level=1)
    return x


def reglob(path, parts=None, i=None):
    """Regular expression-based globbing."""
    if parts is None:
        path = os.path.normpath(path)
        drive, tail = os.path.splitdrive(path)
        parts = tail.split(os.sep)
        d = os.sep if os.path.isabs(path) else "."
        d = os.path.join(drive, d)
        return reglob(d, parts, i=0)
    base = subdir = path
    if i == 0:
        if not os.path.isabs(base):
            base = ""
        elif len(parts) > 1:
            i += 1
    regex = os.path.join(base, parts[i])
    if ON_WINDOWS:
        # currently unable to access regex backslash sequences
        # on Windows due to paths using \.
        regex = regex.replace("\\", "\\\\")
    regex = re.compile(regex)
    files = os.listdir(subdir)
    files.sort()
    paths = []
    i1 = i + 1
    if i1 == len(parts):
        for f in files:
            p = os.path.join(base, f)
            if regex.fullmatch(p) is not None:
                paths.append(p)
    else:
        for f in files:
            p = os.path.join(base, f)
            if regex.fullmatch(p) is None or not os.path.isdir(p):
                continue
            paths += reglob(p, parts=parts, i=i1)
    return paths


def path_literal(s):
    s = expand_path(s)
    return pathlib.Path(s)


def regexsearch(s):
    s = expand_path(s)
    return reglob(s)


def globsearch(s):
    csc = builtins.__xonsh__.env.get("CASE_SENSITIVE_COMPLETIONS")
    glob_sorted = builtins.__xonsh__.env.get("GLOB_SORTED")
    dotglob = builtins.__xonsh__.env.get("DOTGLOB")
    return globpath(
        s,
        ignore_case=(not csc),
        return_empty=True,
        sort_result=glob_sorted,
        include_dotfiles=dotglob,
    )


def pathsearch(func, s, pymode=False, pathobj=False):
    """
    Takes a string and returns a list of file paths that match (regex, glob,
    or arbitrary search function). If pathobj=True, the return is a list of
    pathlib.Path objects instead of strings.
    """
    if not callable(func) or len(inspect.signature(func).parameters) != 1:
        error = "%r is not a known path search function"
        raise XonshError(error % func)
    o = func(s)
    if pathobj and pymode:
        o = list(map(pathlib.Path, o))
    no_match = [] if pymode else [s]
    return o if len(o) != 0 else no_match


RE_SHEBANG = LazyObject(lambda: re.compile(r"#![ \t]*(.+?)$"), globals(), "RE_SHEBANG")


def _is_binary(fname, limit=80):
    with open(fname, "rb") as f:
        for i in range(limit):
            char = f.read(1)
            if char == b"\0":
                return True
            if char == b"\n":
                return False
            if char == b"":
                return False
    return False


def _un_shebang(x):
    if x == "/usr/bin/env":
        return []
    elif any(x.startswith(i) for i in ["/usr/bin", "/usr/local/bin", "/bin"]):
        x = os.path.basename(x)
    elif x.endswith("python") or x.endswith("python.exe"):
        x = "python"
    if x == "xonsh":
        return ["python", "-m", "xonsh.main"]
    return [x]


def get_script_subproc_command(fname, args):
    """Given the name of a script outside the path, returns a list representing
    an appropriate subprocess command to execute the script.  Raises
    PermissionError if the script is not executable.
    """
    # make sure file is executable
    if not os.access(fname, os.X_OK):
        raise PermissionError
    if ON_POSIX and not os.access(fname, os.R_OK):
        # on some systems, some important programs (e.g. sudo) will have
        # execute permissions but not read/write permissions. This enables
        # things with the SUID set to be run. Needs to come before _is_binary()
        # is called, because that function tries to read the file.
        return [fname] + args
    elif _is_binary(fname):
        # if the file is a binary, we should call it directly
        return [fname] + args
    if ON_WINDOWS:
        # Windows can execute various filetypes directly
        # as given in PATHEXT
        _, ext = os.path.splitext(fname)
        if ext.upper() in builtins.__xonsh__.env.get("PATHEXT"):
            return [fname] + args
    # find interpreter
    with open(fname, "rb") as f:
        first_line = f.readline().decode().strip()
    m = RE_SHEBANG.match(first_line)
    # xonsh is the default interpreter
    if m is None:
        interp = ["xonsh"]
    else:
        interp = m.group(1).strip()
        if len(interp) > 0:
            interp = shlex.split(interp)
        else:
            interp = ["xonsh"]
    if ON_WINDOWS:
        o = []
        for i in interp:
            o.extend(_un_shebang(i))
        interp = o
    return interp + [fname] + args


@lazyobject
def _REDIR_REGEX():
    name = r"(o(?:ut)?|e(?:rr)?|a(?:ll)?|&?\d?)"
    return re.compile("{r}(>?>|<){r}$".format(r=name))


_MODES = LazyObject(lambda: {">>": "a", ">": "w", "<": "r"}, globals(), "_MODES")
_WRITE_MODES = LazyObject(lambda: frozenset({"w", "a"}), globals(), "_WRITE_MODES")
_REDIR_ALL = LazyObject(lambda: frozenset({"&", "a", "all"}), globals(), "_REDIR_ALL")
_REDIR_ERR = LazyObject(lambda: frozenset({"2", "e", "err"}), globals(), "_REDIR_ERR")
_REDIR_OUT = LazyObject(
    lambda: frozenset({"", "1", "o", "out"}), globals(), "_REDIR_OUT"
)
_E2O_MAP = LazyObject(
    lambda: frozenset(
        {"{}>{}".format(e, o) for e in _REDIR_ERR for o in _REDIR_OUT if o != ""}
    ),
    globals(),
    "_E2O_MAP",
)
_O2E_MAP = LazyObject(
    lambda: frozenset(
        {"{}>{}".format(o, e) for e in _REDIR_ERR for o in _REDIR_OUT if o != ""}
    ),
    globals(),
    "_O2E_MAP",
)


def _is_redirect(x):
    return isinstance(x, str) and _REDIR_REGEX.match(x)


def safe_open(fname, mode, buffering=-1):
    """Safely attempts to open a file in for xonsh subprocs."""
    # file descriptors
    try:
        return io.open(fname, mode, buffering=buffering)
    except PermissionError:
        raise XonshError("xonsh: {0}: permission denied".format(fname))
    except FileNotFoundError:
        raise XonshError("xonsh: {0}: no such file or directory".format(fname))
    except Exception:
        raise XonshError("xonsh: {0}: unable to open file".format(fname))


def safe_close(x):
    """Safely attempts to close an object."""
    if not isinstance(x, io.IOBase):
        return
    if x.closed:
        return
    try:
        x.close()
    except Exception:
        pass


def _parse_redirects(r, loc=None):
    """returns origin, mode, destination tuple"""
    orig, mode, dest = _REDIR_REGEX.match(r).groups()
    # redirect to fd
    if dest.startswith("&"):
        try:
            dest = int(dest[1:])
            if loc is None:
                loc, dest = dest, ""  # NOQA
            else:
                e = "Unrecognized redirection command: {}".format(r)
                raise XonshError(e)
        except (ValueError, XonshError):
            raise
        except Exception:
            pass
    mode = _MODES.get(mode, None)
    if mode == "r" and (len(orig) > 0 or len(dest) > 0):
        raise XonshError("Unrecognized redirection command: {}".format(r))
    elif mode in _WRITE_MODES and len(dest) > 0:
        raise XonshError("Unrecognized redirection command: {}".format(r))
    return orig, mode, dest


def _redirect_streams(r, loc=None):
    """Returns stdin, stdout, stderr tuple of redirections."""
    stdin = stdout = stderr = None
    no_ampersand = r.replace("&", "")
    # special case of redirecting stderr to stdout
    if no_ampersand in _E2O_MAP:
        stderr = subprocess.STDOUT
        return stdin, stdout, stderr
    elif no_ampersand in _O2E_MAP:
        stdout = 2  # using 2 as a flag, rather than using a file object
        return stdin, stdout, stderr
    # get streams
    orig, mode, dest = _parse_redirects(r)
    if mode == "r":
        stdin = safe_open(loc, mode)
    elif mode in _WRITE_MODES:
        if orig in _REDIR_ALL:
            stdout = stderr = safe_open(loc, mode)
        elif orig in _REDIR_OUT:
            stdout = safe_open(loc, mode)
        elif orig in _REDIR_ERR:
            stderr = safe_open(loc, mode)
        else:
            raise XonshError("Unrecognized redirection command: {}".format(r))
    else:
        raise XonshError("Unrecognized redirection command: {}".format(r))
    return stdin, stdout, stderr


def default_signal_pauser(n, f):
    """Pauses a signal, as needed."""
    signal.pause()


def no_pg_xonsh_preexec_fn():
    """Default subprocess preexec function for when there is no existing
    pipeline group.
    """
    os.setpgrp()
    signal.signal(signal.SIGTSTP, default_signal_pauser)


class SubprocSpec:
    """A container for specifying how a subprocess command should be
    executed.
    """

    kwnames = ("stdin", "stdout", "stderr", "universal_newlines")

    def __init__(
        self,
        cmd,
        *,
        cls=subprocess.Popen,
        stdin=None,
        stdout=None,
        stderr=None,
        universal_newlines=False,
        captured=False
    ):
        """
        Parameters
        ----------
        cmd : list of str
            Command to be run.
        cls : Popen-like
            Class to run the subprocess with.
        stdin : file-like
            Popen file descriptor or flag for stdin.
        stdout : file-like
            Popen file descriptor or flag for stdout.
        stderr : file-like
            Popen file descriptor or flag for stderr.
        universal_newlines : bool
            Whether or not to use universal newlines.
        captured : bool or str, optional
            The flag for if the subprocess is captured, may be one of:
            False for $[], 'stdout' for $(), 'hiddenobject' for ![], or
            'object' for !().

        Attributes
        ----------
        args : list of str
            Arguments as originally supplied.
        alias : list of str, callable, or None
            The alias that was resolved for this command, if any.
        binary_loc : str or None
            Path to binary to execute.
        is_proxy : bool
            Whether or not the subprocess is or should be run as a proxy.
        background : bool
            Whether or not the subprocess should be started in the background.
        threadable : bool
            Whether or not the subprocess is able to be run in a background
            thread, rather than the main thread.
        pipeline_index : int or None
            The index number of this sepc into the pipeline that is being setup.
        last_in_pipeline : bool
            Whether the subprocess is the last in the execution pipeline.
        captured_stdout : file-like
            Handle to captured stdin
        captured_stderr : file-like
            Handle to captured stderr
        stack : list of FrameInfo namedtuples or None
            The stack of the call-site of alias, if the alias requires it.
            None otherwise.
        """
        self._stdin = self._stdout = self._stderr = None
        # args
        self.cmd = list(cmd)
        self.cls = cls
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.universal_newlines = universal_newlines
        self.captured = captured
        # pure attrs
        self.args = list(cmd)
        self.alias = None
        self.binary_loc = None
        self.is_proxy = False
        self.background = False
        self.threadable = True
        self.pipeline_index = None
        self.last_in_pipeline = False
        self.captured_stdout = None
        self.captured_stderr = None
        self.stack = None

    def __str__(self):
        s = self.__class__.__name__ + "(" + str(self.cmd) + ", "
        s += self.cls.__name__ + ", "
        kws = [n + "=" + str(getattr(self, n)) for n in self.kwnames]
        s += ", ".join(kws) + ")"
        return s

    def __repr__(self):
        s = self.__class__.__name__ + "(" + repr(self.cmd) + ", "
        s += self.cls.__name__ + ", "
        kws = [n + "=" + repr(getattr(self, n)) for n in self.kwnames]
        s += ", ".join(kws) + ")"
        return s

    #
    # Properties
    #

    @property
    def stdin(self):
        return self._stdin

    @stdin.setter
    def stdin(self, value):
        if self._stdin is None:
            self._stdin = value
        elif value is None:
            pass
        else:
            safe_close(value)
            msg = "Multiple inputs for stdin for {0!r}"
            msg = msg.format(" ".join(self.args))
            raise XonshError(msg)

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, value):
        if self._stdout is None:
            self._stdout = value
        elif value is None:
            pass
        else:
            safe_close(value)
            msg = "Multiple redirections for stdout for {0!r}"
            msg = msg.format(" ".join(self.args))
            raise XonshError(msg)

    @property
    def stderr(self):
        return self._stderr

    @stderr.setter
    def stderr(self, value):
        if self._stderr is None:
            self._stderr = value
        elif value is None:
            pass
        else:
            safe_close(value)
            msg = "Multiple redirections for stderr for {0!r}"
            msg = msg.format(" ".join(self.args))
            raise XonshError(msg)

    #
    # Execution methods
    #

    def run(self, *, pipeline_group=None):
        """Launches the subprocess and returns the object."""
        kwargs = {n: getattr(self, n) for n in self.kwnames}
        self.prep_env(kwargs)
        self.prep_preexec_fn(kwargs, pipeline_group=pipeline_group)
        if callable(self.alias):
            if "preexec_fn" in kwargs:
                kwargs.pop("preexec_fn")
            p = self.cls(self.alias, self.cmd, **kwargs)
        else:
            self._fix_null_cmd_bytes()
            p = self._run_binary(kwargs)
        p.spec = self
        p.last_in_pipeline = self.last_in_pipeline
        p.captured_stdout = self.captured_stdout
        p.captured_stderr = self.captured_stderr
        return p

    def _run_binary(self, kwargs):
        try:
            bufsize = 1
            p = self.cls(self.cmd, bufsize=bufsize, **kwargs)
        except PermissionError:
            e = "xonsh: subprocess mode: permission denied: {0}"
            raise XonshError(e.format(self.cmd[0]))
        except FileNotFoundError:
            cmd0 = self.cmd[0]
            e = "xonsh: subprocess mode: command not found: {0}".format(cmd0)
            env = builtins.__xonsh__.env
            sug = suggest_commands(cmd0, env, builtins.aliases)
            if len(sug.strip()) > 0:
                e += "\n" + suggest_commands(cmd0, env, builtins.aliases)
            raise XonshError(e)
        return p

    def prep_env(self, kwargs):
        """Prepares the environment to use in the subprocess."""
        denv = builtins.__xonsh__.env.detype()
        if ON_WINDOWS:
            # Over write prompt variable as xonsh's $PROMPT does
            # not make much sense for other subprocs
            denv["PROMPT"] = "$P$G"
        kwargs["env"] = denv

    def prep_preexec_fn(self, kwargs, pipeline_group=None):
        """Prepares the 'preexec_fn' keyword argument"""
        if not ON_POSIX:
            return
        if not builtins.__xonsh__.env.get("XONSH_INTERACTIVE"):
            return
        if pipeline_group is None:
            xonsh_preexec_fn = no_pg_xonsh_preexec_fn
        else:

            def xonsh_preexec_fn():
                """Preexec function bound to a pipeline group."""
                os.setpgid(0, pipeline_group)
                signal.signal(signal.SIGTSTP, default_signal_pauser)

        kwargs["preexec_fn"] = xonsh_preexec_fn

    def _fix_null_cmd_bytes(self):
        # Popen does not accept null bytes in its input commands.
        # That doesn't stop some subprocesses from using them. Here we
        # escape them just in case.
        cmd = self.cmd
        for i in range(len(cmd)):
            cmd[i] = cmd[i].replace("\0", "\\0")

    #
    # Building methods
    #

    @classmethod
    def build(kls, cmd, *, cls=subprocess.Popen, **kwargs):
        """Creates an instance of the subprocess command, with any
        modifications and adjustments based on the actual cmd that
        was received.
        """
        # modifications that do not alter cmds may come before creating instance
        spec = kls(cmd, cls=cls, **kwargs)
        # modifications that alter cmds must come after creating instance
        # perform initial redirects
        spec.redirect_leading()
        spec.redirect_trailing()
        # apply aliases
        spec.resolve_alias()
        spec.resolve_binary_loc()
        spec.resolve_auto_cd()
        spec.resolve_executable_commands()
        spec.resolve_alias_cls()
        spec.resolve_stack()
        return spec

    def redirect_leading(self):
        """Manage leading redirects such as with '< input.txt COMMAND'. """
        while len(self.cmd) >= 3 and self.cmd[0] == "<":
            self.stdin = safe_open(self.cmd[1], "r")
            self.cmd = self.cmd[2:]

    def redirect_trailing(self):
        """Manages trailing redirects."""
        while True:
            cmd = self.cmd
            if len(cmd) >= 3 and _is_redirect(cmd[-2]):
                streams = _redirect_streams(cmd[-2], cmd[-1])
                self.stdin, self.stdout, self.stderr = streams
                self.cmd = cmd[:-2]
            elif len(cmd) >= 2 and _is_redirect(cmd[-1]):
                streams = _redirect_streams(cmd[-1])
                self.stdin, self.stdout, self.stderr = streams
                self.cmd = cmd[:-1]
            else:
                break

    def resolve_alias(self):
        """Sets alias in command, if applicable."""
        cmd0 = self.cmd[0]
        if callable(cmd0):
            alias = cmd0
        else:
            alias = builtins.aliases.get(cmd0, None)
        self.alias = alias

    def resolve_binary_loc(self):
        """Sets the binary location"""
        alias = self.alias
        if alias is None:
            binary_loc = locate_binary(self.cmd[0])
        elif callable(alias):
            binary_loc = None
        else:
            binary_loc = locate_binary(alias[0])
        self.binary_loc = binary_loc

    def resolve_auto_cd(self):
        """Implements AUTO_CD functionality."""
        if not (
            self.alias is None
            and self.binary_loc is None
            and len(self.cmd) == 1
            and builtins.__xonsh__.env.get("AUTO_CD")
            and os.path.isdir(self.cmd[0])
        ):
            return
        self.cmd.insert(0, "cd")
        self.alias = builtins.aliases.get("cd", None)

    def resolve_executable_commands(self):
        """Resolve command executables, if applicable."""
        alias = self.alias
        if alias is None:
            pass
        elif callable(alias):
            self.cmd.pop(0)
            return
        else:
            self.cmd = alias + self.cmd[1:]
            # resolve any redirects the aliases may have applied
            self.redirect_leading()
            self.redirect_trailing()
        if self.binary_loc is None:
            return
        try:
            self.cmd = get_script_subproc_command(self.binary_loc, self.cmd[1:])
        except PermissionError:
            e = "xonsh: subprocess mode: permission denied: {0}"
            raise XonshError(e.format(self.cmd[0]))

    def resolve_alias_cls(self):
        """Determine which proxy class to run an alias with."""
        alias = self.alias
        if not callable(alias):
            return
        self.is_proxy = True
        thable = getattr(alias, "__xonsh_threadable__", True)
        cls = ProcProxyThread if thable else ProcProxy
        self.cls = cls
        self.threadable = thable
        # also check capturability, while we are here
        cpable = getattr(alias, "__xonsh_capturable__", self.captured)
        self.captured = cpable

    def resolve_stack(self):
        """Computes the stack for a callable alias's call-site, if needed."""
        if not callable(self.alias):
            return
        # check that we actual need the stack
        sig = inspect.signature(self.alias)
        if len(sig.parameters) <= 5 and "stack" not in sig.parameters:
            return
        # compute the stack, and filter out these build methods
        # run_subproc() is the 4th command in the stack
        # we want to filter out one up, e.g. subproc_captured_hiddenobject()
        # after that the stack from the call site starts.
        stack = inspect.stack(context=0)
        assert stack[3][3] == "run_subproc", "xonsh stack has changed!"
        del stack[:5]
        self.stack = stack


def _safe_pipe_properties(fd, use_tty=False):
    """Makes sure that a pipe file descriptor properties are sane."""
    if not use_tty:
        return
    # due to some weird, long standing issue in Python, PTYs come out
    # replacing newline \n with \r\n. This causes issues for raw unix
    # protocols, like git and ssh, which expect unix line endings.
    # see https://mail.python.org/pipermail/python-list/2013-June/650460.html
    # for more details and the following solution.
    props = termios.tcgetattr(fd)
    props[1] = props[1] & (~termios.ONLCR) | termios.ONLRET
    termios.tcsetattr(fd, termios.TCSANOW, props)


def _update_last_spec(last):
    captured = last.captured
    last.last_in_pipeline = True
    if not captured:
        return
    callable_alias = callable(last.alias)
    if callable_alias:
        pass
    else:
        cmds_cache = builtins.__xonsh__.commands_cache
        thable = cmds_cache.predict_threadable(
            last.args
        ) and cmds_cache.predict_threadable(last.cmd)
        if captured and thable:
            last.cls = PopenThread
        elif not thable:
            # foreground processes should use Popen
            last.threadable = False
            if captured == "object" or captured == "hiddenobject":
                # CommandPipeline objects should not pipe stdout, stderr
                return
    # cannot used PTY pipes for aliases, for some dark reason,
    # and must use normal pipes instead.
    use_tty = ON_POSIX and not callable_alias
    # Do not set standard in! Popen is not a fan of redirections here
    # set standard out
    if last.stdout is not None:
        last.universal_newlines = True
    elif captured in STDOUT_CAPTURE_KINDS:
        last.universal_newlines = False
        r, w = os.pipe()
        last.stdout = safe_open(w, "wb")
        last.captured_stdout = safe_open(r, "rb")
    elif builtins.__xonsh__.stdout_uncaptured is not None:
        last.universal_newlines = True
        last.stdout = builtins.__xonsh__.stdout_uncaptured
        last.captured_stdout = last.stdout
    elif ON_WINDOWS and not callable_alias:
        last.universal_newlines = True
        last.stdout = None  # must truly stream on windows
        last.captured_stdout = ConsoleParallelReader(1)
    else:
        last.universal_newlines = True
        r, w = pty.openpty() if use_tty else os.pipe()
        _safe_pipe_properties(w, use_tty=use_tty)
        last.stdout = safe_open(w, "w")
        _safe_pipe_properties(r, use_tty=use_tty)
        last.captured_stdout = safe_open(r, "r")
    # set standard error
    if last.stderr is not None:
        pass
    elif captured == "object":
        r, w = os.pipe()
        last.stderr = safe_open(w, "w")
        last.captured_stderr = safe_open(r, "r")
    elif builtins.__xonsh__.stderr_uncaptured is not None:
        last.stderr = builtins.__xonsh__.stderr_uncaptured
        last.captured_stderr = last.stderr
    elif ON_WINDOWS and not callable_alias:
        last.universal_newlines = True
        last.stderr = None  # must truly stream on windows
    else:
        r, w = pty.openpty() if use_tty else os.pipe()
        _safe_pipe_properties(w, use_tty=use_tty)
        last.stderr = safe_open(w, "w")
        _safe_pipe_properties(r, use_tty=use_tty)
        last.captured_stderr = safe_open(r, "r")
    # redirect stdout to stderr, if we should
    if isinstance(last.stdout, int) and last.stdout == 2:
        # need to use private interface to avoid duplication.
        last._stdout = last.stderr
    # redirect stderr to stdout, if we should
    if callable_alias and last.stderr == subprocess.STDOUT:
        last._stderr = last.stdout
        last.captured_stderr = last.captured_stdout


def cmds_to_specs(cmds, captured=False):
    """Converts a list of cmds to a list of SubprocSpec objects that are
    ready to be executed.
    """
    # first build the subprocs independently and separate from the redirects
    i = 0
    specs = []
    redirects = []
    for cmd in cmds:
        if isinstance(cmd, str):
            redirects.append(cmd)
        else:
            if cmd[-1] == "&":
                cmd = cmd[:-1]
                redirects.append("&")
            spec = SubprocSpec.build(cmd, captured=captured)
            spec.pipeline_index = i
            specs.append(spec)
            i += 1
    # now modify the subprocs based on the redirects.
    for i, redirect in enumerate(redirects):
        if redirect == "|":
            # these should remain integer file descriptors, and not Python
            # file objects since they connect processes.
            r, w = os.pipe()
            specs[i].stdout = w
            specs[i + 1].stdin = r
        elif redirect == "&" and i == len(redirects) - 1:
            specs[-1].background = True
        else:
            raise XonshError("unrecognized redirect {0!r}".format(redirect))
    # Apply boundary conditions
    _update_last_spec(specs[-1])
    return specs


def _should_set_title(captured=False):
    env = builtins.__xonsh__.env
    return (
        env.get("XONSH_INTERACTIVE")
        and not env.get("XONSH_STORE_STDOUT")
        and captured not in STDOUT_CAPTURE_KINDS
        and builtins.__xonsh__.shell is not None
    )


def run_subproc(cmds, captured=False):
    """Runs a subprocess, in its many forms. This takes a list of 'commands,'
    which may be a list of command line arguments or a string, representing
    a special connecting character.  For example::

        $ ls | grep wakka

    is represented by the following cmds::

        [['ls'], '|', ['grep', 'wakka']]

    Lastly, the captured argument affects only the last real command.
    """
    specs = cmds_to_specs(cmds, captured=captured)
    captured = specs[-1].captured
    if captured == "hiddenobject":
        command = HiddenCommandPipeline(specs)
    else:
        command = CommandPipeline(specs)
    proc = command.proc
    background = command.spec.background
    if not all(x.is_proxy for x in specs):
        add_job(
            {
                "cmds": cmds,
                "pids": [i.pid for i in command.procs],
                "obj": proc,
                "bg": background,
                "pipeline": command,
                "pgrp": command.term_pgid,
            }
        )
    if _should_set_title(captured=captured):
        # set title here to get currently executing command
        pause_call_resume(proc, builtins.__xonsh__.shell.settitle)
    # create command or return if backgrounding.
    if background:
        return
    # now figure out what we should return.
    if captured == "stdout":
        command.end()
        return command.output
    elif captured == "object":
        return command
    elif captured == "hiddenobject":
        command.end()
        return command
    else:
        command.end()
        return


def subproc_captured_stdout(*cmds):
    """Runs a subprocess, capturing the output. Returns the stdout
    that was produced as a str.
    """
    return run_subproc(cmds, captured="stdout")


def subproc_captured_inject(*cmds):
    """Runs a subprocess, capturing the output. Returns a list of
    whitespace-separated strings of the stdout that was produced.
    The string is split using xonsh's lexer, rather than Python's str.split()
    or shlex.split().
    """
    s = run_subproc(cmds, captured="stdout")
    toks = builtins.__xonsh__.execer.parser.lexer.split(s.strip())
    return toks


def subproc_captured_object(*cmds):
    """
    Runs a subprocess, capturing the output. Returns an instance of
    CommandPipeline representing the completed command.
    """
    return run_subproc(cmds, captured="object")


def subproc_captured_hiddenobject(*cmds):
    """Runs a subprocess, capturing the output. Returns an instance of
    HiddenCommandPipeline representing the completed command.
    """
    return run_subproc(cmds, captured="hiddenobject")


def subproc_uncaptured(*cmds):
    """Runs a subprocess, without capturing the output. Returns the stdout
    that was produced as a str.
    """
    return run_subproc(cmds, captured=False)


def ensure_list_of_strs(x):
    """Ensures that x is a list of strings."""
    if isinstance(x, str):
        rtn = [x]
    elif isinstance(x, cabc.Sequence):
        rtn = [i if isinstance(i, str) else str(i) for i in x]
    else:
        rtn = [str(x)]
    return rtn


def list_of_strs_or_callables(x):
    """Ensures that x is a list of strings or functions"""
    if isinstance(x, str) or callable(x):
        rtn = [x]
    elif isinstance(x, cabc.Iterable):
        rtn = [i if isinstance(i, str) or callable(i) else str(i) for i in x]
    else:
        rtn = [str(x)]
    return rtn


def list_of_list_of_strs_outer_product(x):
    """Takes an outer product of a list of strings"""
    lolos = map(ensure_list_of_strs, x)
    rtn = []
    for los in itertools.product(*lolos):
        s = "".join(los)
        if "*" in s:
            rtn.extend(builtins.__xonsh__.glob(s))
        else:
            rtn.append(builtins.__xonsh__.expand_path(s))
    return rtn


@lazyobject
def MACRO_FLAG_KINDS():
    return {
        "s": str,
        "str": str,
        "string": str,
        "a": AST,
        "ast": AST,
        "c": types.CodeType,
        "code": types.CodeType,
        "compile": types.CodeType,
        "v": eval,
        "eval": eval,
        "x": exec,
        "exec": exec,
        "t": type,
        "type": type,
    }


def _convert_kind_flag(x):
    """Puts a kind flag (string) a canonical form."""
    x = x.lower()
    kind = MACRO_FLAG_KINDS.get(x, None)
    if kind is None:
        raise TypeError("{0!r} not a recognized macro type.".format(x))
    return kind


def convert_macro_arg(raw_arg, kind, glbs, locs, *, name="<arg>", macroname="<macro>"):
    """Converts a string macro argument based on the requested kind.

    Parameters
    ----------
    raw_arg : str
        The str representation of the macro argument.
    kind : object
        A flag or type representing how to convert the argument.
    glbs : Mapping
        The globals from the call site.
    locs : Mapping or None
        The locals from the call site.
    name : str, optional
        The macro argument name.
    macroname : str, optional
        The name of the macro itself.

    Returns
    -------
    The converted argument.
    """
    # munge kind and mode to start
    mode = None
    if isinstance(kind, cabc.Sequence) and not isinstance(kind, str):
        # have (kind, mode) tuple
        kind, mode = kind
    if isinstance(kind, str):
        kind = _convert_kind_flag(kind)
    if kind is str or kind is None:
        return raw_arg  # short circuit since there is nothing else to do
    # select from kind and convert
    execer = builtins.__xonsh__.execer
    filename = macroname + "(" + name + ")"
    if kind is AST:
        ctx = set(dir(builtins)) | set(glbs.keys())
        if locs is not None:
            ctx |= set(locs.keys())
        mode = mode or "eval"
        arg = execer.parse(raw_arg, ctx, mode=mode, filename=filename)
    elif kind is types.CodeType or kind is compile:  # NOQA
        mode = mode or "eval"
        arg = execer.compile(
            raw_arg, mode=mode, glbs=glbs, locs=locs, filename=filename
        )
    elif kind is eval:
        arg = execer.eval(raw_arg, glbs=glbs, locs=locs, filename=filename)
    elif kind is exec:
        mode = mode or "exec"
        if not raw_arg.endswith("\n"):
            raw_arg += "\n"
        arg = execer.exec(raw_arg, mode=mode, glbs=glbs, locs=locs, filename=filename)
    elif kind is type:
        arg = type(execer.eval(raw_arg, glbs=glbs, locs=locs, filename=filename))
    else:
        msg = "kind={0!r} and mode={1!r} was not recognized for macro " "argument {2!r}"
        raise TypeError(msg.format(kind, mode, name))
    return arg


@contextlib.contextmanager
def in_macro_call(f, glbs, locs):
    """Attaches macro globals and locals temporarily to function as a
    context manager.

    Parameters
    ----------
    f : callable object
        The function that is called as ``f(*args)``.
    glbs : Mapping
        The globals from the call site.
    locs : Mapping or None
        The locals from the call site.
    """
    prev_glbs = getattr(f, "macro_globals", None)
    prev_locs = getattr(f, "macro_locals", None)
    f.macro_globals = glbs
    f.macro_locals = locs
    yield
    if prev_glbs is None:
        del f.macro_globals
    else:
        f.macro_globals = prev_glbs
    if prev_locs is None:
        del f.macro_locals
    else:
        f.macro_locals = prev_locs


def call_macro(f, raw_args, glbs, locs):
    """Calls a function as a macro, returning its result.

    Parameters
    ----------
    f : callable object
        The function that is called as ``f(*args)``.
    raw_args : tuple of str
        The str representation of arguments of that were passed into the
        macro. These strings will be parsed, compiled, evaled, or left as
        a string depending on the annotations of f.
    glbs : Mapping
        The globals from the call site.
    locs : Mapping or None
        The locals from the call site.
    """
    sig = inspect.signature(f)
    empty = inspect.Parameter.empty
    macroname = f.__name__
    i = 0
    args = []
    for (key, param), raw_arg in zip(sig.parameters.items(), raw_args):
        i += 1
        if raw_arg == "*":
            break
        kind = param.annotation
        if kind is empty or kind is None:
            kind = str
        arg = convert_macro_arg(
            raw_arg, kind, glbs, locs, name=key, macroname=macroname
        )
        args.append(arg)
    reg_args, kwargs = _eval_regular_args(raw_args[i:], glbs, locs)
    args += reg_args
    with in_macro_call(f, glbs, locs):
        rtn = f(*args, **kwargs)
    return rtn


@lazyobject
def KWARG_RE():
    return re.compile(r"([A-Za-z_]\w*=|\*\*)")


def _starts_as_arg(s):
    """Tests if a string starts as a non-kwarg string would."""
    return KWARG_RE.match(s) is None


def _eval_regular_args(raw_args, glbs, locs):
    if not raw_args:
        return [], {}
    arglist = list(itertools.takewhile(_starts_as_arg, raw_args))
    kwarglist = raw_args[len(arglist) :]
    execer = builtins.__xonsh__.execer
    if not arglist:
        args = arglist
        kwargstr = "dict({})".format(", ".join(kwarglist))
        kwargs = execer.eval(kwargstr, glbs=glbs, locs=locs)
    elif not kwarglist:
        argstr = "({},)".format(", ".join(arglist))
        args = execer.eval(argstr, glbs=glbs, locs=locs)
        kwargs = {}
    else:
        argstr = "({},)".format(", ".join(arglist))
        kwargstr = "dict({})".format(", ".join(kwarglist))
        both = "({}, {})".format(argstr, kwargstr)
        args, kwargs = execer.eval(both, glbs=glbs, locs=locs)
    return args, kwargs


def enter_macro(obj, raw_block, glbs, locs):
    """Prepares to enter a context manager macro by attaching the contents
    of the macro block, globals, and locals to the object. These modifications
    are made in-place and the original object is returned.


    Parameters
    ----------
    obj : context manager
        The object that is about to be entered via a with-statement.
    raw_block : str
        The str of the block that is the context body.
        This string will be parsed, compiled, evaled, or left as
        a string depending on the return annotation of obj.__enter__.
    glbs : Mapping
        The globals from the context site.
    locs : Mapping or None
        The locals from the context site.

    Returns
    -------
    obj : context manager
        The same context manager but with the new macro information applied.
    """
    # recurse down sequences
    if isinstance(obj, cabc.Sequence):
        for x in obj:
            enter_macro(x, raw_block, glbs, locs)
        return obj
    # convert block as needed
    kind = getattr(obj, "__xonsh_block__", str)
    macroname = getattr(obj, "__name__", "<context>")
    block = convert_macro_arg(
        raw_block, kind, glbs, locs, name="<with!>", macroname=macroname
    )
    # attach attrs
    obj.macro_globals = glbs
    obj.macro_locals = locs
    obj.macro_block = block
    return obj


def load_builtins(execer=None, ctx=None):
    """Loads the xonsh builtins into the Python builtins. Sets the
    BUILTINS_LOADED variable to True.
    """
    global BUILTINS_LOADED
    if not hasattr(builtins, "__xonsh__"):
        builtins.__xonsh__ = XonshSession(execer=execer, ctx=ctx)
    builtins.__xonsh__.load(execer=execer, ctx=ctx)
    builtins.__xonsh__.link_builtins(execer=execer)
    BUILTINS_LOADED = True


def _lastflush(s=None, f=None):
    if hasattr(builtins, "__xonsh__"):
        if builtins.__xonsh__.history is not None:
            builtins.__xonsh__.history.flush(at_exit=True)


def unload_builtins():
    """Removes the xonsh builtins from the Python builtins, if the
    BUILTINS_LOADED is True, sets BUILTINS_LOADED to False, and returns.
    """
    global BUILTINS_LOADED
    if not hasattr(builtins, "__xonsh__"):
        BUILTINS_LOADED = False
        return
    env = getattr(builtins.__xonsh__, "env", None)
    if isinstance(env, Env):
        env.undo_replace_env()
    if hasattr(builtins.__xonsh__, "pyexit"):
        builtins.exit = builtins.__xonsh__.pyexit
    if hasattr(builtins.__xonsh__, "pyquit"):
        builtins.quit = builtins.__xonsh__.pyquit
    if not BUILTINS_LOADED:
        return
    builtins.__xonsh__.unlink_builtins()
    delattr(builtins, "__xonsh__")
    BUILTINS_LOADED = False


@contextlib.contextmanager
def xonsh_builtins(execer=None):
    """A context manager for using the xonsh builtins only in a limited
    scope. Likely useful in testing.
    """
    load_builtins(execer=execer)
    # temporary shims for old __xonsh_*__ builtins
    load_proxies()
    yield
    # temporary shims for old __xonsh_*__ builtins
    unload_proxies()
    unload_builtins()


class XonshSession:
    """All components defining a xonsh session.

    """

    def __init__(self, execer=None, ctx=None):
        """
        Parameters
        ---------
        execer : Execer, optional
            Xonsh execution object, may be None to start
        ctx : Mapping, optional
            Context to start xonsh session with.
        """
        self.execer = execer
        self.ctx = {} if ctx is None else ctx

    def load(self, execer=None, ctx=None):
        """Loads the session with default values.

        Parameters
        ---------
        execer : Execer, optional
            Xonsh execution object, may be None to start
        ctx : Mapping, optional
            Context to start xonsh session with.
        """
        if ctx is not None:
            self.ctx = ctx
        self.env = Env(default_env())
        self.help = helper
        self.superhelp = superhelper
        self.pathsearch = pathsearch
        self.globsearch = globsearch
        self.regexsearch = regexsearch
        self.glob = globpath
        self.expand_path = expand_path
        self.exit = False
        self.stdout_uncaptured = None
        self.stderr_uncaptured = None

        if hasattr(builtins, "exit"):
            self.pyexit = builtins.exit
            del builtins.exit

        if hasattr(builtins, "quit"):
            self.pyquit = builtins.quit
            del builtins.quit

        self.subproc_captured_stdout = subproc_captured_stdout
        self.subproc_captured_inject = subproc_captured_inject
        self.subproc_captured_object = subproc_captured_object
        self.subproc_captured_hiddenobject = subproc_captured_hiddenobject
        self.subproc_uncaptured = subproc_uncaptured
        self.execer = execer
        self.commands_cache = CommandsCache()
        self.all_jobs = {}
        self.ensure_list_of_strs = ensure_list_of_strs
        self.list_of_strs_or_callables = list_of_strs_or_callables

        self.list_of_list_of_strs_outer_product = list_of_list_of_strs_outer_product

        self.completers = xonsh.completers.init.default_completers()
        self.call_macro = call_macro
        self.enter_macro = enter_macro
        self.path_literal = path_literal

        self.builtins = _BuiltIns(execer)

        self.history = None
        self.shell = None

    def link_builtins(self, execer=None):
        # public built-ins
        builtins.XonshError = self.builtins.XonshError
        builtins.XonshCalledProcessError = self.builtins.XonshCalledProcessError
        builtins.evalx = None if execer is None else execer.eval
        builtins.execx = None if execer is None else execer.exec
        builtins.compilex = None if execer is None else execer.compile
        builtins.events = self.builtins.events

        # sneak the path search functions into the aliases
        # Need this inline/lazy import here since we use locate_binary that
        # relies on __xonsh__.env in default aliases
        builtins.default_aliases = builtins.aliases = Aliases(make_default_aliases())
        atexit.register(_lastflush)
        for sig in AT_EXIT_SIGNALS:
            resetting_signal_handle(sig, _lastflush)

    def unlink_builtins(self):
        names = [
            "XonshError",
            "XonshCalledProcessError",
            "evalx",
            "execx",
            "compilex",
            "default_aliases",
        ]

        for name in names:
            if hasattr(builtins, name):
                delattr(builtins, name)


class _BuiltIns:
    def __init__(self, execer=None):
        # public built-ins
        self.XonshError = XonshError
        self.XonshCalledProcessError = XonshCalledProcessError
        self.evalx = None if execer is None else execer.eval
        self.execx = None if execer is None else execer.exec
        self.compilex = None if execer is None else execer.compile
        self.events = events


class DynamicAccessProxy:
    """Proxies access dynamically."""

    def __init__(self, refname, objname):
        """
        Parameters
        ----------
        refname : str
            '.'-separated string that represents the new, reference name that
            the user will access.
        objname : str
            '.'-separated string that represents the name where the target
            object actually lives that refname points to.
        """
        super().__setattr__("refname", refname)
        super().__setattr__("objname", objname)

    @property
    def obj(self):
        """Dynamically grabs object"""
        names = self.objname.split(".")
        obj = builtins
        for name in names:
            obj = getattr(obj, name)
        return obj

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def __setattr__(self, name, value):
        return super().__setattr__(self.obj, name, value)

    def __delattr__(self, name):
        return delattr(self.obj, name)

    def __getitem__(self, item):
        return self.obj.__getitem__(item)

    def __setitem__(self, item, value):
        return self.obj.__setitem__(item, value)

    def __delitem__(self, item):
        del self.obj[item]

    def __call__(self, *args, **kwargs):
        return self.obj.__call__(*args, **kwargs)


class DeprecationWarningProxy:
    """Proxies access, but warns in the process."""

    def __init__(self, oldname, newname):
        super().__setattr__("oldname", oldname)
        super().__setattr__("newname", newname)

    @property
    def obj(self):
        """Dynamically grabs object"""
        names = self.newname.split(".")
        obj = builtins
        for name in names:
            obj = getattr(obj, name)
        return obj

    def warn(self):
        """Issues deprecation warning."""
        warnings.warn(
            "{} has been deprecated, please use {} instead.".format(
                self.oldname, self.newname
            ),
            DeprecationWarning,
            stacklevel=3,
        )

    def __getattr__(self, name):
        self.warn()
        return getattr(self.obj, name)

    def __setattr__(self, name, value):
        self.warn()
        return super().__setattr__(self.obj, name, value)

    def __delattr__(self, name):
        self.warn()
        return delattr(self.obj, name)

    def __getitem__(self, item):
        self.warn()
        return self.obj.__getitem__(item)

    def __setitem__(self, item, value):
        self.warn()
        return self.obj.__setitem__(item, value)

    def __delitem__(self, item):
        self.warn()
        del self.obj[item]

    def __call__(self, *args, **kwargs):
        self.warn()
        return self.obj.__call__(*args, **kwargs)


def load_proxies():
    """Loads builtin dynamic access proxies.
    Also puts temporary shims in place for `__xonsh_*__` builtins.
    """
    proxy_mapping = {
        "XonshError": "__xonsh__.builtins.XonshError",
        "XonshCalledProcessError": "__xonsh__.builtins.XonshCalledProcessError",
        "evalx": "__xonsh__.builtins.evalx",
        "execx": "__xonsh__.builtins.execx",
        "compilex": "__xonsh__.builtins.compilex",
        "events": "__xonsh__.builtins.events",
    }
    for refname, objname in proxy_mapping.items():
        proxy = DynamicAccessProxy(refname, objname)
        setattr(builtins, refname, proxy)

    deprecated_mapping = {
        "__xonsh_env__": "__xonsh__.env",
        "__xonsh_history__": "__xonsh__.history",
        "__xonsh_ctx__": "__xonsh__.ctx",
        "__xonsh_help__": "__xonsh__.help",
        "__xonsh_superhelp__": "__xonsh__.superhelp",
        "__xonsh_pathsearch__": "__xonsh__.pathsearch",
        "__xonsh_globsearch__": "__xonsh__.globsearch",
        "__xonsh_regexsearch__": "__xonsh__.regexsearch",
        "__xonsh_glob__": "__xonsh__.glob",
        "__xonsh_expand_path__": "__xonsh__.expand_path",
        "__xonsh_exit__": "__xonsh__.exit",
        "__xonsh_stdout_uncaptured__": "__xonsh__.stdout_uncaptured",
        "__xonsh_stderr_uncaptured__": "__xonsh__.stderr_uncaptured",
        "__xonsh_subproc_captured_stdout__": "__xonsh__.subproc_captured_stdout",
        "__xonsh_subproc_captured_inject__": "__xonsh__.subproc_captured_inject",
        "__xonsh_subproc_captured_object__": "__xonsh__.subproc_captured_object",
        "__xonsh_subproc_captured_hiddenobject__": "__xonsh__.subproc_captured_hiddenobject",
        "__xonsh_subproc_uncaptured__": "__xonsh__.subproc_uncaptured",
        "__xonsh_execer__": "__xonsh__.execer",
        "__xonsh_commands_cache__": "__xonsh__.commands_cache",
        "__xonsh_all_jobs__": "__xonsh__.all_jobs",
        "__xonsh_ensure_list_of_strs__": "__xonsh__.ensure_list_of_strs",
        "__xonsh_list_of_strs_or_callables__": "__xonsh__.list_of_strs_or_callables",
        "__xonsh_list_of_list_of_strs_outer_product__": "__xonsh__.list_of_list_of_strs_outer_product",
        "__xonsh_completers__": "__xonsh__.completers",
        "__xonsh_call_macro__": "__xonsh__.call_macro",
        "__xonsh_enter_macro__": "__xonsh__.enter_macro",
        "__xonsh_path_literal__": "__xonsh__.path_literal",
    }
    for badname, goodname in deprecated_mapping.items():
        proxy = DeprecationWarningProxy(badname, goodname)
        setattr(builtins, badname, proxy)

    if hasattr(builtins.__xonsh__, "pyexit"):
        builtins.__xonsh_pyexit__ = DeprecationWarningProxy(
            "builtins.__xonsh_pyexit__", "builtins.__xonsh__.pyexit"
        )
    if hasattr(builtins.__xonsh__, "quit"):
        builtins.__xonsh_pyquit__ = DeprecationWarningProxy(
            "builtins.__xonsh_pyquit__", "builtins.__xonsh__.pyquit"
        )


def unload_proxies():
    """Removes the xonsh builtins (proxies) from the Python builtins.
    """
    if hasattr(builtins, "__xonsh_pyexit__"):
        builtins.exit = builtins.__xonsh_pyexit__
    if hasattr(builtins, "__xonsh_pyquit__"):
        builtins.quit = builtins.__xonsh_pyquit__

    names = [
        "__xonsh_env__",
        "__xonsh_ctx__",
        "__xonsh_help__",
        "__xonsh_superhelp__",
        "__xonsh_pathsearch__",
        "__xonsh_globsearch__",
        "__xonsh_regexsearch__",
        "__xonsh_glob__",
        "__xonsh_expand_path__",
        "__xonsh_exit__",
        "__xonsh_stdout_uncaptured__",
        "__xonsh_stderr_uncaptured__",
        "__xonsh_pyexit__",
        "__xonsh_pyquit__",
        "__xonsh_subproc_captured_stdout__",
        "__xonsh_subproc_captured_inject__",
        "__xonsh_subproc_captured_object__",
        "__xonsh_subproc_captured_hiddenobject__",
        "__xonsh_subproc_uncaptured__",
        "__xonsh_execer__",
        "__xonsh_commands_cache__",
        "__xonsh_completers__",
        "__xonsh_call_macro__",
        "__xonsh_enter_macro__",
        "__xonsh_path_literal__",
        "XonshError",
        "XonshCalledProcessError",
        "evalx",
        "execx",
        "compilex",
        "default_aliases",
        "__xonsh_all_jobs__",
        "__xonsh_ensure_list_of_strs__",
        "__xonsh_list_of_strs_or_callables__",
        "__xonsh_list_of_list_of_strs_outer_product__",
        "__xonsh_history__",
    ]
    for name in names:
        if hasattr(builtins, name):
            delattr(builtins, name)

#
# execer
#
# -*- coding: utf-8 -*-
"""Implements the xonsh executer."""
# amalgamated sys
# amalgamated types
# amalgamated inspect
# amalgamated builtins
# amalgamated collections.abc
# amalgamated xonsh.ast
# amalgamated xonsh.parser
# amalgamated xonsh.tools
# amalgamated xonsh.built_ins
class Execer(object):
    """Executes xonsh code in a context."""

    def __init__(
        self,
        filename="<xonsh-code>",
        debug_level=0,
        parser_args=None,
        unload=True,
        xonsh_ctx=None,
        scriptcache=True,
        cacheall=False,
    ):
        """Parameters
        ----------
        filename : str, optional
            File we are to execute.
        debug_level : int, optional
            Debugging level to use in lexing and parsing.
        parser_args : dict, optional
            Arguments to pass down to the parser.
        unload : bool, optional
            Whether or not to unload xonsh builtins upon deletion.
        xonsh_ctx : dict or None, optional
            Xonsh xontext to load as builtins.__xonsh__.ctx
        scriptcache : bool, optional
            Whether or not to use a precompiled bytecode cache when execing
            code, default: True.
        cacheall : bool, optional
            Whether or not to cache all xonsh code, and not just files. If this
            is set to true, it will cache command line input too, default: False.
        """
        parser_args = parser_args or {}
        self.parser = Parser(**parser_args)
        self.filename = filename
        self.debug_level = debug_level
        self.unload = unload
        self.scriptcache = scriptcache
        self.cacheall = cacheall
        self.ctxtransformer = CtxAwareTransformer(self.parser)
        load_builtins(execer=self, ctx=xonsh_ctx)
        load_proxies()

    def __del__(self):
        if self.unload:
            unload_proxies()
            unload_builtins()

    def parse(self, input, ctx, mode="exec", filename=None, transform=True):
        """Parses xonsh code in a context-aware fashion. For context-free
        parsing, please use the Parser class directly or pass in
        transform=False.
        """
        if filename is None:
            filename = self.filename
        if not transform:
            return self.parser.parse(
                input, filename=filename, mode=mode, debug_level=(self.debug_level > 2)
            )

        # Parsing actually happens in a couple of phases. The first is a
        # shortcut for a context-free parser. Normally, all subprocess
        # lines should be wrapped in $(), to indicate that they are a
        # subproc. But that would be super annoying. Unfortunately, Python
        # mode - after indentation - is whitespace agnostic while, using
        # the Python token, subproc mode is whitespace aware. That is to say,
        # in Python mode "ls -l", "ls-l", and "ls - l" all parse to the
        # same AST because whitespace doesn't matter to the minus binary op.
        # However, these phases all have very different meaning in subproc
        # mode. The 'right' way to deal with this is to make the entire
        # grammar whitespace aware, and then ignore all of the whitespace
        # tokens for all of the Python rules. The lazy way implemented here
        # is to parse a line a second time with a $() wrapper if it fails
        # the first time. This is a context-free phase.
        tree, input = self._parse_ctx_free(input, mode=mode, filename=filename)
        if tree is None:
            return None

        # Now we need to perform context-aware AST transformation. This is
        # because the "ls -l" is valid Python. The only way that we know
        # it is not actually Python is by checking to see if the first token
        # (ls) is part of the execution context. If it isn't, then we will
        # assume that this line is supposed to be a subprocess line, assuming
        # it also is valid as a subprocess line.
        if ctx is None:
            ctx = set()
        elif isinstance(ctx, cabc.Mapping):
            ctx = set(ctx.keys())
        tree = self.ctxtransformer.ctxvisit(
            tree, input, ctx, mode=mode, debug_level=self.debug_level
        )
        return tree

    def compile(
        self,
        input,
        mode="exec",
        glbs=None,
        locs=None,
        stacklevel=2,
        filename=None,
        transform=True,
    ):
        """Compiles xonsh code into a Python code object, which may then
        be execed or evaled.
        """
        if filename is None:
            filename = self.filename
        if glbs is None or locs is None:
            frame = inspect.stack()[stacklevel][0]
            glbs = frame.f_globals if glbs is None else glbs
            locs = frame.f_locals if locs is None else locs
        ctx = set(dir(builtins)) | set(glbs.keys()) | set(locs.keys())
        tree = self.parse(input, ctx, mode=mode, filename=filename, transform=transform)
        if tree is None:
            return None  # handles comment only input
        code = compile(tree, filename, mode)
        return code

    def eval(
        self, input, glbs=None, locs=None, stacklevel=2, filename=None, transform=True
    ):
        """Evaluates (and returns) xonsh code."""
        if isinstance(input, types.CodeType):
            code = input
        else:
            if filename is None:
                filename = self.filename
            code = self.compile(
                input=input,
                glbs=glbs,
                locs=locs,
                mode="eval",
                stacklevel=stacklevel,
                filename=filename,
                transform=transform,
            )
        if code is None:
            return None  # handles comment only input
        return eval(code, glbs, locs)

    def exec(
        self,
        input,
        mode="exec",
        glbs=None,
        locs=None,
        stacklevel=2,
        filename=None,
        transform=True,
    ):
        """Execute xonsh code."""
        if isinstance(input, types.CodeType):
            code = input
        else:
            if filename is None:
                filename = self.filename
            code = self.compile(
                input=input,
                glbs=glbs,
                locs=locs,
                mode=mode,
                stacklevel=stacklevel,
                filename=filename,
                transform=transform,
            )
        if code is None:
            return None  # handles comment only input
        return exec(code, glbs, locs)

    def _print_debug_wrapping(
        self, line, sbpline, last_error_line, last_error_col, maxcol=None
    ):
        """print some debugging info if asked for."""
        if self.debug_level > 1:
            msg = "{0}:{1}:{2}{3} - {4}\n" "{0}:{1}:{2}{3} + {5}"
            mstr = "" if maxcol is None else ":" + str(maxcol)
            msg = msg.format(
                self.filename, last_error_line, last_error_col, mstr, line, sbpline
            )
            print(msg, file=sys.stderr)

    def _parse_ctx_free(self, input, mode="exec", filename=None, logical_input=False):
        last_error_line = last_error_col = -1
        parsed = False
        original_error = None
        greedy = False
        if filename is None:
            filename = self.filename
        while not parsed:
            try:
                tree = self.parser.parse(
                    input,
                    filename=filename,
                    mode=mode,
                    debug_level=(self.debug_level > 2),
                )
                parsed = True
            except IndentationError as e:
                if original_error is None:
                    raise e
                else:
                    raise original_error
            except SyntaxError as e:
                if original_error is None:
                    original_error = e
                if (e.loc is None) or (
                    last_error_line == e.loc.lineno
                    and last_error_col in (e.loc.column + 1, e.loc.column)
                ):
                    raise original_error from None
                elif last_error_line != e.loc.lineno:
                    original_error = e
                last_error_col = e.loc.column
                last_error_line = e.loc.lineno
                idx = last_error_line - 1
                lines = input.splitlines()
                line, nlogical, idx = get_logical_line(lines, idx)
                if nlogical > 1 and not logical_input:
                    _, sbpline = self._parse_ctx_free(
                        line, mode=mode, filename=filename, logical_input=True
                    )
                    self._print_debug_wrapping(
                        line, sbpline, last_error_line, last_error_col, maxcol=None
                    )
                    replace_logical_line(lines, sbpline, idx, nlogical)
                    last_error_col += 3
                    input = "\n".join(lines)
                    continue
                if input.endswith("\n"):
                    lines.append("")
                if len(line.strip()) == 0:
                    # whitespace only lines are not valid syntax in Python's
                    # interactive mode='single', who knew?! Just ignore them.
                    # this might cause actual syntax errors to have bad line
                    # numbers reported, but should only affect interactive mode
                    del lines[idx]
                    last_error_line = last_error_col = -1
                    input = "\n".join(lines)
                    continue

                if last_error_line > 1 and lines[idx - 1].rstrip()[-1:] == ":":
                    # catch non-indented blocks and raise error.
                    prev_indent = len(lines[idx - 1]) - len(lines[idx - 1].lstrip())
                    curr_indent = len(lines[idx]) - len(lines[idx].lstrip())
                    if prev_indent == curr_indent:
                        raise original_error
                lexer = self.parser.lexer
                maxcol = (
                    None
                    if greedy
                    else find_next_break(line, mincol=last_error_col, lexer=lexer)
                )
                if not greedy and maxcol in (e.loc.column + 1, e.loc.column):
                    # go greedy the first time if the syntax error was because
                    # we hit an end token out of place. This usually indicates
                    # a subshell or maybe a macro.
                    if not balanced_parens(line, maxcol=maxcol):
                        greedy = True
                        maxcol = None
                sbpline = subproc_toks(
                    line, returnline=True, greedy=greedy, maxcol=maxcol, lexer=lexer
                )
                if sbpline is None:
                    # subprocess line had no valid tokens,
                    if len(line.partition("#")[0].strip()) == 0:
                        # likely because it only contained a comment.
                        del lines[idx]
                        last_error_line = last_error_col = -1
                        input = "\n".join(lines)
                        continue
                    elif not greedy:
                        greedy = True
                        continue
                    else:
                        # or for some other syntax error
                        raise original_error
                elif sbpline[last_error_col:].startswith(
                    "![!["
                ) or sbpline.lstrip().startswith("![!["):
                    # if we have already wrapped this in subproc tokens
                    # and it still doesn't work, adding more won't help
                    # anything
                    if not greedy:
                        greedy = True
                        continue
                    else:
                        raise original_error
                # replace the line
                self._print_debug_wrapping(
                    line, sbpline, last_error_line, last_error_col, maxcol=maxcol
                )
                replace_logical_line(lines, sbpline, idx, nlogical)
                last_error_col += 3
                input = "\n".join(lines)
        return tree, input

#
# imphooks
#
# -*- coding: utf-8 -*-
"""Import hooks for importing xonsh source files.

This module registers the hooks it defines when it is imported.
"""
# amalgamated os
# amalgamated re
# amalgamated sys
# amalgamated types
# amalgamated builtins
# amalgamated contextlib
# amalgamated importlib
from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder, SourceLoader, Loader

# amalgamated xonsh.events
# amalgamated xonsh.execer
# amalgamated xonsh.platform
# amalgamated xonsh.lazyasd
@lazyobject
def ENCODING_LINE():
    # this regex comes from PEP 263
    # https://www.python.org/dev/peps/pep-0263/#defining-the-encoding
    return re.compile(b"^[ tv]*#.*?coding[:=][ t]*([-_.a-zA-Z0-9]+)")


def find_source_encoding(src):
    """Finds the source encoding given bytes representing a file. If
    no encoding is found, UTF-8 will be returned as per the docs
    https://docs.python.org/3/howto/unicode.html#unicode-literals-in-python-source-code
    """
    utf8 = "UTF-8"
    first, _, rest = src.partition(b"\n")
    m = ENCODING_LINE.match(first)
    if m is not None:
        return m.group(1).decode(utf8)
    second, _, _ = rest.partition(b"\n")
    m = ENCODING_LINE.match(second)
    if m is not None:
        return m.group(1).decode(utf8)
    return utf8


class XonshImportHook(MetaPathFinder, SourceLoader):
    """Implements the import hook for xonsh source files."""

    def __init__(self, *args, **kwargs):
        super(XonshImportHook, self).__init__(*args, **kwargs)
        self._filenames = {}
        self._execer = None

    @property
    def execer(self):
        if (
            hasattr(builtins, "__xonsh__")
            and hasattr(builtins.__xonsh__, "execer")
            and builtins.__xonsh__.execer is not None
        ):
            execer = builtins.__xonsh__.execer
            if self._execer is not None:
                self._execer = None
        elif self._execer is None:
            self._execer = execer = Execer(unload=False)
        else:
            execer = self._execer
        return execer

    #
    # MetaPathFinder methods
    #
    def find_spec(self, fullname, path, target=None):
        """Finds the spec for a xonsh module if it exists."""
        dot = "."
        spec = None
        path = sys.path if path is None else path
        if dot not in fullname and dot not in path:
            path = [dot] + path
        name = fullname.rsplit(dot, 1)[-1]
        fname = name + ".xsh"
        for p in path:
            if not isinstance(p, str):
                continue
            if not os.path.isdir(p) or not os.access(p, os.R_OK):
                continue
            if fname not in {x.name for x in scandir(p)}:
                continue
            spec = ModuleSpec(fullname, self)
            self._filenames[fullname] = os.path.join(p, fname)
            break
        return spec

    #
    # SourceLoader methods
    #
    def create_module(self, spec):
        """Create a xonsh module with the appropriate attributes."""
        mod = types.ModuleType(spec.name)
        mod.__file__ = self.get_filename(spec.name)
        mod.__loader__ = self
        mod.__package__ = spec.parent or ""
        return mod

    def get_filename(self, fullname):
        """Returns the filename for a module's fullname."""
        return self._filenames[fullname]

    def get_data(self, path):
        """Gets the bytes for a path."""
        raise NotImplementedError

    def get_code(self, fullname):
        """Gets the code object for a xonsh file."""
        filename = self.get_filename(fullname)
        if filename is None:
            msg = "xonsh file {0!r} could not be found".format(fullname)
            raise ImportError(msg)
        with open(filename, "rb") as f:
            src = f.read()
        enc = find_source_encoding(src)
        src = src.decode(encoding=enc)
        src = src if src.endswith("\n") else src + "\n"
        execer = self.execer
        execer.filename = filename
        ctx = {}  # dummy for modules
        code = execer.compile(src, glbs=ctx, locs=ctx)
        return code


#
# Import events
#
events.doc(
    "on_import_pre_find_spec",
    """
on_import_pre_find_spec(fullname: str, path: str, target: module or None) -> None

Fires before any import find_spec() calls have been executed. The parameters
here are the same as importlib.abc.MetaPathFinder.find_spec(). Namely,

:``fullname``: The full name of the module to import.
:``path``: None if a top-level import, otherwise the ``__path__`` of the parent
          package.
:``target``: Target module used to make a better guess about the package spec.
""",
)

events.doc(
    "on_import_post_find_spec",
    """
on_import_post_find_spec(spec, fullname, path, target) -> None

Fires after all import find_spec() calls have been executed. The parameters
here the spec and the arguments importlib.abc.MetaPathFinder.find_spec(). Namely,

:``spec``: A ModuleSpec object if the spec was found, or None if it was not.
:``fullname``: The full name of the module to import.
:``path``: None if a top-level import, otherwise the ``__path__`` of the parent
          package.
:``target``: Target module used to make a better guess about the package spec.
""",
)

events.doc(
    "on_import_pre_create_module",
    """
on_import_pre_create_module(spec: ModuleSpec) -> None

Fires right before a module is created by its loader. The only parameter
is the spec object. See importlib for more details.
""",
)

events.doc(
    "on_import_post_create_module",
    """
on_import_post_create_module(module: Module, spec: ModuleSpec) -> None

Fires after a module is created by its loader but before the loader returns it.
The parameters here are the module object itself and the spec object.
See importlib for more details.
""",
)

events.doc(
    "on_import_pre_exec_module",
    """
on_import_pre_exec_module(module: Module) -> None

Fires right before a module is executed by its loader. The only parameter
is the module itself. See importlib for more details.
""",
)

events.doc(
    "on_import_post_exec_module",
    """
on_import_post_create_module(module: Module) -> None

Fires after a module is executed by its loader but before the loader returns it.
The only parameter is the module itself. See importlib for more details.
""",
)


def _should_dispatch_xonsh_import_event_loader():
    """Figures out if we should dispatch to a load event"""
    return (
        len(events.on_import_pre_create_module) > 0
        or len(events.on_import_post_create_module) > 0
        or len(events.on_import_pre_exec_module) > 0
        or len(events.on_import_post_exec_module) > 0
    )


class XonshImportEventHook(MetaPathFinder):
    """Implements the import hook for firing xonsh events on import."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fullname_stack = []

    @contextlib.contextmanager
    def append_stack(self, fullname):
        """A context manager for appending and then removing a name from the
        fullname stack.
        """
        self._fullname_stack.append(fullname)
        yield
        del self._fullname_stack[-1]

    #
    # MetaPathFinder methods
    #
    def find_spec(self, fullname, path, target=None):
        """Finds the spec for a xonsh module if it exists."""
        if fullname in reversed(self._fullname_stack):
            # don't execute if we are already in the stack.
            return None
        npre = len(events.on_import_pre_find_spec)
        npost = len(events.on_import_post_find_spec)
        dispatch_load = _should_dispatch_xonsh_import_event_loader()
        if npre > 0:
            events.on_import_pre_find_spec.fire(
                fullname=fullname, path=path, target=target
            )
        elif npost == 0 and not dispatch_load:
            # no events to fire, proceed normally and prevent recursion
            return None
        # now find the spec
        with self.append_stack(fullname):
            spec = importlib.util.find_spec(fullname)
        # fire post event
        if npost > 0:
            events.on_import_post_find_spec.fire(
                spec=spec, fullname=fullname, path=path, target=target
            )
        if dispatch_load and spec is not None and hasattr(spec.loader, "create_module"):
            spec.loader = XonshImportEventLoader(spec.loader)
        return spec


class XonshImportEventLoader(Loader):
    """A class that dispatches loader calls to another loader and fires relevant
    xonsh events.
    """

    def __init__(self, loader):
        self.loader = loader

    #
    # Loader methods
    #
    def create_module(self, spec):
        """Creates and returns the module object."""
        events.on_import_pre_create_module.fire(spec=spec)
        mod = self.loader.create_module(spec)
        events.on_import_post_create_module.fire(module=mod, spec=spec)
        return mod

    def exec_module(self, module):
        """Executes the module in its own namespace."""
        events.on_import_pre_exec_module.fire(module=module)
        rtn = self.loader.exec_module(module)
        events.on_import_post_exec_module.fire(module=module)
        return rtn

    def load_module(self, fullname):
        """Legacy module loading, provided for backwards compatibility."""
        return self.loader.load_module(fullname)

    def module_repr(self, module):
        """Legacy module repr, provided for backwards compatibility."""
        return self.loader.module_repr(module)


def install_import_hooks():
    """
    Install Xonsh import hooks in ``sys.meta_path`` in order for ``.xsh`` files
    to be importable and import events to be fired.

    Can safely be called many times, will be no-op if xonsh import hooks are
    already present.
    """
    found_imp = found_event = False
    for hook in sys.meta_path:
        if isinstance(hook, XonshImportHook):
            found_imp = True
        elif isinstance(hook, XonshImportEventHook):
            found_event = True
    if not found_imp:
        sys.meta_path.append(XonshImportHook())
    if not found_event:
        sys.meta_path.insert(0, XonshImportEventHook())


# alias to deprecated name
install_hook = install_import_hooks

#
# main
#
# -*- coding: utf-8 -*-
"""The main xonsh script."""
# amalgamated os
# amalgamated sys
enum = _LazyModule.load('enum', 'enum')
# amalgamated argparse
# amalgamated builtins
# amalgamated contextlib
# amalgamated signal
# amalgamated traceback
from xonsh import __version__
# amalgamated xonsh.timings
# amalgamated xonsh.lazyasd
# amalgamated xonsh.shell
# amalgamated xonsh.pretty
# amalgamated xonsh.execer
# amalgamated xonsh.proc
# amalgamated xonsh.jobs
# amalgamated xonsh.tools
# amalgamated xonsh.platform
# amalgamated xonsh.codecache
# amalgamated xonsh.xonfig
# amalgamated xonsh.xontribs
# amalgamated xonsh.lazyimps
# amalgamated xonsh.imphooks
# amalgamated xonsh.events
# amalgamated xonsh.environ
# amalgamated xonsh.built_ins
events.transmogrify("on_post_init", "LoadEvent")
events.doc(
    "on_post_init",
    """
on_post_init() -> None

Fired after all initialization is finished and we're ready to do work.

NOTE: This is fired before the wizard is automatically started.
""",
)

events.transmogrify("on_exit", "LoadEvent")
events.doc(
    "on_exit",
    """
on_exit() -> None

Fired after all commands have been executed, before tear-down occurs.

NOTE: All the caveats of the ``atexit`` module also apply to this event.
""",
)


events.transmogrify("on_pre_cmdloop", "LoadEvent")
events.doc(
    "on_pre_cmdloop",
    """
on_pre_cmdloop() -> None

Fired just before the command loop is started, if it is.
""",
)

events.transmogrify("on_post_cmdloop", "LoadEvent")
events.doc(
    "on_post_cmdloop",
    """
on_post_cmdloop() -> None

Fired just after the command loop finishes, if it is.

NOTE: All the caveats of the ``atexit`` module also apply to this event.
""",
)

events.transmogrify("on_pre_rc", "LoadEvent")
events.doc(
    "on_pre_rc",
    """
on_pre_rc() -> None

Fired just before rc files are loaded, if they are.
""",
)

events.transmogrify("on_post_rc", "LoadEvent")
events.doc(
    "on_post_rc",
    """
on_post_rc() -> None

Fired just after rc files are loaded, if they are.
""",
)


def get_setproctitle():
    """Proxy function for loading process title"""
    try:
        from setproctitle import setproctitle as spt
    except ImportError:
        return
    return spt


def path_argument(s):
    """Return a path only if the path is actually legal

    This is very similar to argparse.FileType, except that it doesn't return
    an open file handle, but rather simply validates the path."""

    s = os.path.abspath(os.path.expanduser(s))
    if not os.path.isfile(s):
        msg = "{0!r} must be a valid path to a file".format(s)
        raise argparse.ArgumentTypeError(msg)
    return s


@lazyobject
def parser():
    p = argparse.ArgumentParser(description="xonsh", add_help=False)
    p.add_argument(
        "-h",
        "--help",
        dest="help",
        action="store_true",
        default=False,
        help="show help and exit",
    )
    p.add_argument(
        "-V",
        "--version",
        dest="version",
        action="store_true",
        default=False,
        help="show version information and exit",
    )
    p.add_argument(
        "-c",
        help="Run a single command and exit",
        dest="command",
        required=False,
        default=None,
    )
    p.add_argument(
        "-i",
        "--interactive",
        help="force running in interactive mode",
        dest="force_interactive",
        action="store_true",
        default=False,
    )
    p.add_argument(
        "-l",
        "--login",
        help="run as a login shell",
        dest="login",
        action="store_true",
        default=False,
    )
    p.add_argument(
        "--config-path",
        help="DEPRECATED: static configuration files may now be used "
        "in the XONSHRC file list, see the --rc option.",
        dest="config_path",
        default=None,
        type=path_argument,
    )
    p.add_argument(
        "--rc",
        help="The xonshrc files to load, these may be either xonsh "
        "files or JSON-based static configuration files.",
        dest="rc",
        nargs="+",
        type=path_argument,
        default=None,
    )
    p.add_argument(
        "--no-rc",
        help="Do not load the .xonshrc files",
        dest="norc",
        action="store_true",
        default=False,
    )
    p.add_argument(
        "--no-script-cache",
        help="Do not cache scripts as they are run",
        dest="scriptcache",
        action="store_false",
        default=True,
    )
    p.add_argument(
        "--cache-everything",
        help="Use a cache, even for interactive commands",
        dest="cacheall",
        action="store_true",
        default=False,
    )
    p.add_argument(
        "-D",
        dest="defines",
        help="define an environment variable, in the form of "
        "-DNAME=VAL. May be used many times.",
        metavar="ITEM",
        action="append",
        default=None,
    )
    p.add_argument(
        "--shell-type",
        help="What kind of shell should be used. "
        "Possible options: readline, prompt_toolkit, random. "
        "Warning! If set this overrides $SHELL_TYPE variable.",
        dest="shell_type",
        choices=tuple(Shell.shell_type_aliases.keys()),
        default=None,
    )
    p.add_argument(
        "--timings",
        help="Prints timing information before the prompt is shown. "
        "This is useful while tracking down performance issues "
        "and investigating startup times.",
        dest="timings",
        action="store_true",
        default=None,
    )
    p.add_argument(
        "file",
        metavar="script-file",
        help="If present, execute the script in script-file" " and exit",
        nargs="?",
        default=None,
    )
    p.add_argument(
        "args",
        metavar="args",
        help="Additional arguments to the script specified " "by script-file",
        nargs=argparse.REMAINDER,
        default=[],
    )
    return p


def _pprint_displayhook(value):
    if value is None:
        return
    builtins._ = None  # Set '_' to None to avoid recursion
    if isinstance(value, HiddenCommandPipeline):
        builtins._ = value
        return
    env = builtins.__xonsh__.env
    if env.get("PRETTY_PRINT_RESULTS"):
        printed_val = pretty(value)
    else:
        printed_val = repr(value)
    if HAS_PYGMENTS and env.get("COLOR_RESULTS"):
        tokens = list(pygments.lex(printed_val, lexer=pyghooks.XonshLexer()))
        end = "" if env.get("SHELL_TYPE") == "prompt_toolkit2" else "\n"
        print_color(tokens, end=end)
    else:
        print(printed_val)  # black & white case
    builtins._ = value


class XonshMode(enum.Enum):
    single_command = 0
    script_from_file = 1
    script_from_stdin = 2
    interactive = 3


def start_services(shell_kwargs, args):
    """Starts up the essential services in the proper order.
    This returns the environment instance as a convenience.
    """
    install_import_hooks()
    # create execer, which loads builtins
    ctx = shell_kwargs.get("ctx", {})
    debug = to_bool_or_int(os.getenv("XONSH_DEBUG", "0"))
    events.on_timingprobe.fire(name="pre_execer_init")
    execer = Execer(
        xonsh_ctx=ctx,
        debug_level=debug,
        scriptcache=shell_kwargs.get("scriptcache", True),
        cacheall=shell_kwargs.get("cacheall", False),
    )
    events.on_timingprobe.fire(name="post_execer_init")
    # load rc files
    login = shell_kwargs.get("login", True)
    env = builtins.__xonsh__.env
    rc = shell_kwargs.get("rc", None)
    rc = env.get("XONSHRC") if rc is None else rc
    if args.mode != XonshMode.interactive and not args.force_interactive:
        #  Don't load xonshrc if not interactive shell
        rc = None
    events.on_pre_rc.fire()
    xonshrc_context(rcfiles=rc, execer=execer, ctx=ctx, env=env, login=login)
    events.on_post_rc.fire()
    # create shell
    builtins.__xonsh__.shell = Shell(execer=execer, **shell_kwargs)
    ctx["__name__"] = "__main__"
    return env


def premain(argv=None):
    """Setup for main xonsh entry point. Returns parsed arguments."""
    if argv is None:
        argv = sys.argv[1:]
    builtins.__xonsh__ = XonshSession()
    setup_timings(argv)
    setproctitle = get_setproctitle()
    if setproctitle is not None:
        setproctitle(" ".join(["xonsh"] + argv))
    args = parser.parse_args(argv)
    if args.help:
        parser.print_help()
        parser.exit()
    if args.version:
        version = "/".join(("xonsh", __version__))
        print(version)
        parser.exit()
    shell_kwargs = {
        "shell_type": args.shell_type,
        "completer": False,
        "login": False,
        "scriptcache": args.scriptcache,
        "cacheall": args.cacheall,
        "ctx": builtins.__xonsh__.ctx,
    }
    if args.login:
        shell_kwargs["login"] = True
    if args.norc:
        shell_kwargs["rc"] = ()
    elif args.rc:
        shell_kwargs["rc"] = args.rc
    setattr(sys, "displayhook", _pprint_displayhook)
    if args.command is not None:
        args.mode = XonshMode.single_command
        shell_kwargs["shell_type"] = "none"
    elif args.file is not None:
        args.mode = XonshMode.script_from_file
        shell_kwargs["shell_type"] = "none"
    elif not sys.stdin.isatty() and not args.force_interactive:
        args.mode = XonshMode.script_from_stdin
        shell_kwargs["shell_type"] = "none"
    else:
        args.mode = XonshMode.interactive
        shell_kwargs["completer"] = True
        shell_kwargs["login"] = True
    env = start_services(shell_kwargs, args)
    env["XONSH_LOGIN"] = shell_kwargs["login"]
    if args.defines is not None:
        env.update([x.split("=", 1) for x in args.defines])
    env["XONSH_INTERACTIVE"] = args.force_interactive or (
        args.mode == XonshMode.interactive
    )
    if ON_WINDOWS:
        setup_win_unicode_console(env.get("WIN_UNICODE_CONSOLE", True))
    return args


def _failback_to_other_shells(args, err):
    # only failback for interactive shell; if we cannot tell, treat it
    # as an interactive one for safe.
    if hasattr(args, "mode") and args.mode != XonshMode.interactive:
        raise err
    foreign_shell = None
    shells_file = "/etc/shells"
    if not os.path.exists(shells_file):
        # right now, it will always break here on Windows
        raise err
    excluded_list = ["xonsh", "screen"]
    with open(shells_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "/" not in line:
                continue
            _, shell = line.rsplit("/", 1)
            if shell in excluded_list:
                continue
            if not os.path.exists(line):
                continue
            foreign_shell = line
            break
    if foreign_shell:
        traceback.print_exc()
        print("Xonsh encountered an issue during launch", file=sys.stderr)
        print("Failback to {}".format(foreign_shell), file=sys.stderr)
        os.execlp(foreign_shell, foreign_shell)
    else:
        raise err


def main(argv=None):
    args = None
    try:
        args = premain(argv)
        return main_xonsh(args)
    except Exception as err:
        _failback_to_other_shells(args, err)


def main_xonsh(args):
    """Main entry point for xonsh cli."""
    if not ON_WINDOWS:

        def func_sig_ttin_ttou(n, f):
            pass

        signal.signal(signal.SIGTTIN, func_sig_ttin_ttou)
        signal.signal(signal.SIGTTOU, func_sig_ttin_ttou)

    events.on_post_init.fire()
    env = builtins.__xonsh__.env
    shell = builtins.__xonsh__.shell
    try:
        if args.mode == XonshMode.interactive:
            # enter the shell
            env["XONSH_INTERACTIVE"] = True
            ignore_sigtstp()
            if env["XONSH_INTERACTIVE"] and not any(
                os.path.isfile(i) for i in env["XONSHRC"]
            ):
                print_welcome_screen()
            events.on_pre_cmdloop.fire()
            try:
                shell.shell.cmdloop()
            finally:
                events.on_post_cmdloop.fire()
        elif args.mode == XonshMode.single_command:
            # run a single command and exit
            run_code_with_cache(args.command.lstrip(), shell.execer, mode="single")
        elif args.mode == XonshMode.script_from_file:
            # run a script contained in a file
            path = os.path.abspath(os.path.expanduser(args.file))
            if os.path.isfile(path):
                sys.argv = [args.file] + args.args
                env.update(make_args_env())  # $ARGS is not sys.argv
                env["XONSH_SOURCE"] = path
                shell.ctx.update({"__file__": args.file, "__name__": "__main__"})
                run_script_with_cache(
                    args.file, shell.execer, glb=shell.ctx, loc=None, mode="exec"
                )
            else:
                print("xonsh: {0}: No such file or directory.".format(args.file))
        elif args.mode == XonshMode.script_from_stdin:
            # run a script given on stdin
            code = sys.stdin.read()
            run_code_with_cache(
                code, shell.execer, glb=shell.ctx, loc=None, mode="exec"
            )
    finally:
        events.on_exit.fire()
    postmain(args)


def postmain(args=None):
    """Teardown for main xonsh entry point, accepts parsed arguments."""
    if ON_WINDOWS:
        setup_win_unicode_console(enable=False)
    builtins.__xonsh__.shell = None


@contextlib.contextmanager
def main_context(argv=None):
    """Generator that runs pre- and post-main() functions. This has two iterations.
    The first yields the shell. The second returns None but cleans
    up the shell.
    """
    args = premain(argv)
    yield builtins.__xonsh__.shell
    postmain(args)


def setup(
    ctx=None,
    shell_type="none",
    env=(("RAISE_SUBPROC_ERROR", True),),
    aliases=(),
    xontribs=(),
    threadable_predictors=(),
):
    """Starts up a new xonsh shell. Calling this in function in another
    packages __init__.py will allow xonsh to be fully used in the
    package in headless or headed mode. This function is primarily indended to
    make starting up xonsh for 3rd party packages easier.

    Parameters
    ----------
    ctx : dict-like or None, optional
        The xonsh context to start with. If None, an empty dictionary
        is provided.
    shell_type : str, optional
        The type of shell to start. By default this is 'none', indicating
        we should start in headless mode.
    env : dict-like, optional
        Environment to update the current environment with after the shell
        has been initialized.
    aliases : dict-like, optional
        Aliases to add after the shell has been initialized.
    xontribs : iterable of str, optional
        Xontrib names to load.
    threadable_predictors : dict-like, optional
        Threadable predictors to start up with. These overide the defaults.
    """
    ctx = {} if ctx is None else ctx
    # setup xonsh ctx and execer
    if not hasattr(builtins, "__xonsh__"):
        execer = Execer(xonsh_ctx=ctx)
        builtins.__xonsh__ = XonshSession(ctx=ctx, execer=execer)
        load_builtins(ctx=ctx, execer=execer)
        load_proxies()
        builtins.__xonsh__.shell = Shell(execer, ctx=ctx, shell_type=shell_type)
    builtins.__xonsh__.env.update(env)
    install_import_hooks()
    builtins.aliases.update(aliases)
    if xontribs:
        xontribs_load(xontribs)
    tp = builtins.__xonsh__.commands_cache.threadable_predictors
    tp.update(threadable_predictors)

