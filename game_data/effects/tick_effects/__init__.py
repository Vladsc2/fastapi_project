import importlib
import pkgutil

__all__ = []


def _auto_import_modules(max_depth=2):

    for finder, name, is_pkg in pkgutil.walk_packages(__path__, prefix=__name__ + '.'):

        relative = name[len(__name__) + 1:]
        depth = relative.count('.') + 1

        if depth > max_depth:
            continue

        importlib.import_module(name)




_auto_import_modules(max_depth=2)