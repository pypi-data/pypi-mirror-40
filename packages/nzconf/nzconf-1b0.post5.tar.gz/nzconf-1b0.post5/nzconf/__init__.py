from .file import File

try:
    from .__version__ import VERSION
except:               # pragma: no cover
    VERSION='unknown'

_EXTENSION2CLASS = dict()

__all__ = ['File','register_extension','supports','AutoFile']

def register_extension(ext,cls):
    if not issubclass(cls,File):
        raise TypeError("Class '%s' must extend '%s'." % (cls.__name__,File.__name__))
    _EXTENSION2CLASS[ext] = cls

def supports(ext=None):
    if ext is None:
        return list(_EXTENSION2CLASS.keys())
    return ext in _EXTENSION2CLASS

def AutoFile(filename,*args,**kwargs):
    fn = str(filename)
    for ext,cls in _EXTENSION2CLASS.items():
        if fn.endswith(ext):
            break
    else:
        raise KeyError("Unsupported extension for '%s'." % fn)
    return cls(filename,*args,**kwargs)
