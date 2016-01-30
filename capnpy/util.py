import imp

def extend(cls):
    def decorator(new_class):
        for key, value in new_class.__dict__.iteritems():
            if key not in ('__dict__', '__doc__', '__module__', '__weakref__'):
                setattr(cls, key, value)
        return cls
    return decorator

def exec_extended(modname, globals):
    try:
        f, filename, _ = imp.find_module(modname)
    except ImportError:
        return
    src = f.read()
    f.close()
    code = compile(src, filename, 'exec')
    exec code in globals


def text_repr(s):
    # abuse the python string repr algo: make sure that the string contains at
    # least one single quote and one double quote (which we will remove
    # later); this way python returns a repr inside single quotes, and escapes
    # non-ascii chars and single quotes. Then, we manually escape the double
    # quotes and put everything inside double quotes
    #
    s = s + "'" + '"'
    s = repr(s)[1:-4] # remove the single quotes around the string, plus the
                      # extra quotes we added above
    s = s.replace('"', r'\"')
    return '"%s"' % s

try:
    from capnpy.floatrepr import float32_repr, float64_repr
except ImportError:
    float32_repr = float64_repr = repr
