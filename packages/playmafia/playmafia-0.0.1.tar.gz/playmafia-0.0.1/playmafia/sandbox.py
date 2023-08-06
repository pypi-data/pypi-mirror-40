"""
Allows executing a python module in a reasonably secure sandbox.
"""
import importlib

banned_builtins = [
    'breakpoint',
    'compile',
    'delattr',
    'dir',
    'eval',
    'exec',
    'globals',
    'help',
    'input',
    'memoryview',
    'open',
    'print',
    'setattr'
]

def get_builtin_dict():
    """
    Retrieves the implementation dependent builtin dictionary.
    """
    try:
        return get_builtin_dict.cached_dict
    except AttributeError:
        if isinstance(__builtins__, dict):
            get_builtin_dict.cached_dict = __builtins__
        else:
            get_builtin_dict.cached_dict = __builtins__.__dict__
        return get_builtin_dict.cached_dict

class SandboxError(Exception):
    """
    Is raised if a module cannot run in the sandbox.
    """
    def __init__(self, module, imported):
        super().__init__(f'Import of {imported} failed in module {module}')

class SandboxRunner:
    """
    Defines a sandbox runner that removes all imported modules and environment variables. It
    restores them after the sandbox finished executing code.
    """
    def __init__(self, import_function, allowed_builtins = []):
        """
        Initializes the sandbox runner with a secure import function.

        :param import_function: The import function to use.
        :param allowed_builtins: List of allowed builtins.
        :type import_function: module function(name, globals, locals, from_list, level)
        """
        self._import_function = import_function
        self._allowed_builtins = allowed_builtins
        self._old_builtins = dict()

    def __enter__(self):
        self._old_builtins['__import__'] = get_builtin_dict()['__import__']
        get_builtin_dict()['__import__'] = self._import_function
        for builtin in banned_builtins:
            if builtin in get_builtin_dict() and builtin not in self._allowed_builtins:
                self._old_builtins[builtin] = get_builtin_dict()[builtin]
                del get_builtin_dict()[builtin]
        return self

    def __exit__(self, type, value, traceback):
        get_builtin_dict().update(self._old_builtins)

class Sandbox:
    """
    Provides a sandbox for python modules. Before importing the module, it modifies the environment
    to use a custom import function in order to catch dangerous import statements.
    """
    def __init__(self, module_path, white_list = []):
        """
        Creates a new sandbox with the given module and white listed imports.

        :param module_path: The module path (e.g. A.B.C) to sandbox.
        :param white_list: The modules to white list for import.
        """
        self._module_path = module_path
        self._white_list = white_list
        self._module = None
        if not self._module_path:
            raise RuntimeError('Sandbox: Module path must not be empty')

    def run(self):
        """
        Returns a context manager to run sandboxed code inside.
        """
        if self._module is None:
            with SandboxRunner(self._secure_import, ['exec', 'setattr', 'compile', 'print']):
                self._module = importlib.import_module(self._module_path)
        return SandboxRunner(self._secure_import)

    def get_attribute(self, name):
        """
        Retrieves the attribute with the given name from the loaded module.
        """
        return getattr(self._module, name)

    def _secure_import(self, name, global_dict, local_dict, from_list = [], level = 0):
        if name not in self._white_list:
            raise SandboxError(self._module, name)
        local_from_enum = from_list if from_list and self._white_list else []
        for item in local_from_enum:
            full_name = f'{name}.{item}'
            if not full_name in self._white_list:
                raise SandboxError(self._module_path, full_name)
        return importlib.__import__(name, global_dict, local_dict, from_list, level)
