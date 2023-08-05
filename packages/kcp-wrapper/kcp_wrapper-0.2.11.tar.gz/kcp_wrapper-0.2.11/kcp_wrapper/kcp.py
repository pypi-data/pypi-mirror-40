# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_kcp')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_kcp')
    _kcp = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_kcp', [dirname(__file__)])
        except ImportError:
            import _kcp
            return _kcp
        try:
            _mod = imp.load_module('_kcp', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _kcp = swig_import_helper()
    del swig_import_helper
else:
    import _kcp
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

try:
    import weakref
    weakref_proxy = weakref.proxy
except __builtin__.Exception:
    weakref_proxy = lambda x: x


class KcpWrapper(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KcpWrapper, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KcpWrapper, name)
    __repr__ = _swig_repr

    def __init__(self, conv: 'unsigned int'):
        if self.__class__ == KcpWrapper:
            _self = None
        else:
            _self = self
        this = _kcp.new_KcpWrapper(_self, conv)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _kcp.delete_KcpWrapper
    __del__ = lambda self: None

    def setBindData(self, bindData: 'void *') -> "void":
        return _kcp.KcpWrapper_setBindData(self, bindData)

    def getBindData(self) -> "void *":
        return _kcp.KcpWrapper_getBindData(self)

    def setOutputListener(self, outputListener: 'OutputListener') -> "void":
        return _kcp.KcpWrapper_setOutputListener(self, outputListener)

    def recv(self) -> "std::string":
        return _kcp.KcpWrapper_recv(self)

    def send(self, buf: 'std::string const &') -> "int":
        return _kcp.KcpWrapper_send(self, buf)

    def update(self, current: 'unsigned int') -> "void":
        return _kcp.KcpWrapper_update(self, current)

    def check(self, current: 'unsigned int') -> "unsigned int":
        return _kcp.KcpWrapper_check(self, current)

    def input(self, buf: 'std::string const &') -> "int":
        return _kcp.KcpWrapper_input(self, buf)

    def flush(self) -> "void":
        return _kcp.KcpWrapper_flush(self)

    def setMtu(self, mtu: 'int') -> "int":
        return _kcp.KcpWrapper_setMtu(self, mtu)

    def setWndSize(self, sndwnd: 'int', rcvwnd: 'int') -> "int":
        return _kcp.KcpWrapper_setWndSize(self, sndwnd, rcvwnd)

    def setNoDelay(self, nodelay: 'int', interval: 'int', resend: 'int', nc: 'int') -> "int":
        return _kcp.KcpWrapper_setNoDelay(self, nodelay, interval, resend, nc)

    def getKcp(self) -> "ikcpcb *":
        return _kcp.KcpWrapper_getKcp(self)
    def __disown__(self):
        self.this.disown()
        _kcp.disown_KcpWrapper(self)
        return weakref_proxy(self)
KcpWrapper_swigregister = _kcp.KcpWrapper_swigregister
KcpWrapper_swigregister(KcpWrapper)

class OutputListener(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, OutputListener, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, OutputListener, name)
    __repr__ = _swig_repr

    def __init__(self):
        if self.__class__ == OutputListener:
            _self = None
        else:
            _self = self
        this = _kcp.new_OutputListener(_self, )
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _kcp.delete_OutputListener
    __del__ = lambda self: None

    def call(self, data: 'std::string const &', kcpWrapper: 'KcpWrapper') -> "int":
        return _kcp.OutputListener_call(self, data, kcpWrapper)
    def __disown__(self):
        self.this.disown()
        _kcp.disown_OutputListener(self)
        return weakref_proxy(self)
OutputListener_swigregister = _kcp.OutputListener_swigregister
OutputListener_swigregister(OutputListener)

# This file is compatible with both classic and new-style classes.


