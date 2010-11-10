# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.
# This file is compatible with both classic and new-style classes.

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_regulus', [dirname(__file__)])
        except ImportError:
            import _regulus
            return _regulus
        if fp is not None:
            try:
                _mod = imp.load_module('_regulus', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _regulus = swig_import_helper()
    del swig_import_helper
else:
    import _regulus
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _regulus.delete_SwigPyIterator
    __del__ = lambda self : None;
    def value(self): return _regulus.SwigPyIterator_value(self)
    def incr(self, n = 1): return _regulus.SwigPyIterator_incr(self, n)
    def decr(self, n = 1): return _regulus.SwigPyIterator_decr(self, n)
    def distance(self, *args): return _regulus.SwigPyIterator_distance(self, *args)
    def equal(self, *args): return _regulus.SwigPyIterator_equal(self, *args)
    def copy(self): return _regulus.SwigPyIterator_copy(self)
    def next(self): return _regulus.SwigPyIterator_next(self)
    def __next__(self): return _regulus.SwigPyIterator___next__(self)
    def previous(self): return _regulus.SwigPyIterator_previous(self)
    def advance(self, *args): return _regulus.SwigPyIterator_advance(self, *args)
    def __eq__(self, *args): return _regulus.SwigPyIterator___eq__(self, *args)
    def __ne__(self, *args): return _regulus.SwigPyIterator___ne__(self, *args)
    def __iadd__(self, *args): return _regulus.SwigPyIterator___iadd__(self, *args)
    def __isub__(self, *args): return _regulus.SwigPyIterator___isub__(self, *args)
    def __add__(self, *args): return _regulus.SwigPyIterator___add__(self, *args)
    def __sub__(self, *args): return _regulus.SwigPyIterator___sub__(self, *args)
    def __iter__(self): return self
SwigPyIterator_swigregister = _regulus.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class dictvector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dictvector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dictvector, name)
    __repr__ = _swig_repr
    def iterator(self): return _regulus.dictvector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _regulus.dictvector___nonzero__(self)
    def __bool__(self): return _regulus.dictvector___bool__(self)
    def __len__(self): return _regulus.dictvector___len__(self)
    def pop(self): return _regulus.dictvector_pop(self)
    def __getslice__(self, *args): return _regulus.dictvector___getslice__(self, *args)
    def __setslice__(self, *args): return _regulus.dictvector___setslice__(self, *args)
    def __delslice__(self, *args): return _regulus.dictvector___delslice__(self, *args)
    def __delitem__(self, *args): return _regulus.dictvector___delitem__(self, *args)
    def __getitem__(self, *args): return _regulus.dictvector___getitem__(self, *args)
    def __setitem__(self, *args): return _regulus.dictvector___setitem__(self, *args)
    def append(self, *args): return _regulus.dictvector_append(self, *args)
    def empty(self): return _regulus.dictvector_empty(self)
    def size(self): return _regulus.dictvector_size(self)
    def clear(self): return _regulus.dictvector_clear(self)
    def swap(self, *args): return _regulus.dictvector_swap(self, *args)
    def get_allocator(self): return _regulus.dictvector_get_allocator(self)
    def begin(self): return _regulus.dictvector_begin(self)
    def end(self): return _regulus.dictvector_end(self)
    def rbegin(self): return _regulus.dictvector_rbegin(self)
    def rend(self): return _regulus.dictvector_rend(self)
    def pop_back(self): return _regulus.dictvector_pop_back(self)
    def erase(self, *args): return _regulus.dictvector_erase(self, *args)
    def __init__(self, *args): 
        this = _regulus.new_dictvector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _regulus.dictvector_push_back(self, *args)
    def front(self): return _regulus.dictvector_front(self)
    def back(self): return _regulus.dictvector_back(self)
    def assign(self, *args): return _regulus.dictvector_assign(self, *args)
    def resize(self, *args): return _regulus.dictvector_resize(self, *args)
    def insert(self, *args): return _regulus.dictvector_insert(self, *args)
    def reserve(self, *args): return _regulus.dictvector_reserve(self, *args)
    def capacity(self): return _regulus.dictvector_capacity(self)
    __swig_destroy__ = _regulus.delete_dictvector
    __del__ = lambda self : None;
dictvector_swigregister = _regulus.dictvector_swigregister
dictvector_swigregister(dictvector)

class DictEntry(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DictEntry, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DictEntry, name)
    __repr__ = _swig_repr
    __swig_setmethods__["word"] = _regulus.DictEntry_word_set
    __swig_getmethods__["word"] = _regulus.DictEntry_word_get
    if _newclass:word = _swig_property(_regulus.DictEntry_word_get, _regulus.DictEntry_word_set)
    __swig_setmethods__["freq"] = _regulus.DictEntry_freq_set
    __swig_getmethods__["freq"] = _regulus.DictEntry_freq_get
    if _newclass:freq = _swig_property(_regulus.DictEntry_freq_get, _regulus.DictEntry_freq_set)
    def __init__(self, *args): 
        this = _regulus.new_DictEntry(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _regulus.delete_DictEntry
    __del__ = lambda self : None;
DictEntry_swigregister = _regulus.DictEntry_swigregister
DictEntry_swigregister(DictEntry)

class Dict(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Dict, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Dict, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _regulus.new_Dict(*args)
        try: self.this.append(this)
        except: self.this = this
    def read(self, *args): return _regulus.Dict_read(self, *args)
    def write(self, *args): return _regulus.Dict_write(self, *args)
    def grep(self, *args): return _regulus.Dict_grep(self, *args)
    def grep_freq_sorted(self, *args): return _regulus.Dict_grep_freq_sorted(self, *args)
    def total_freq(self, *args): return _regulus.Dict_total_freq(self, *args)
    def best_match(self, *args): return _regulus.Dict_best_match(self, *args)
    __swig_destroy__ = _regulus.delete_Dict
    __del__ = lambda self : None;
Dict_swigregister = _regulus.Dict_swigregister
Dict_swigregister(Dict)



