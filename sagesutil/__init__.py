
# This function taken from <http://docs.python.org/lib/built-in-funcs.html>:
def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def export(description = "[No Description Entered]", args = [], ret = None):
    """ Export a function via the Sages API """
    def wrap_fn(fn):
        fn.description = description
        fn.args = args
        fn.ret = ret
        fn.sages_exported = True
        return fn
    return wrap_fn

def listExportedModules(module):
    """ List the exported functions in a module """
    from types import ModuleType
    
    if type(module) != ModuleType: # This function accepts either an
        module = my_import(module) # actual Python module, or the string name
                                   # of a module

    module_directory = ( getattr(module, x) for x in dir(module) )
    
    for module_attr in module_directory:
        if hasattr(module_attr, 'sages_exported') and module_attr.sages_exported == True:
           yield module_attr

           
def listExports(module):
    """ Return a dictionary describing each exported function in the specified module """
    return ( { "function": module_attr,                    
               "description": module_attr.description,
               "docstring": module_attr.__doc__,
               "args": module_attr.args,
               "ret": module_attr.ret }
             for module_attr in listExportedModules(module) )
