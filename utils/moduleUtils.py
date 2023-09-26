import os
from types import ModuleType


def module_to_dict(module) -> dict:
    context = {}
    for setting in dir(module):
        if setting.islower() and setting.isalpha():
            context[setting] = getattr(module, setting)
    return context


# TODO Generic
def module_to_list(module, get=None, exclude=None) -> list[ModuleType]:
    ret = []
    for item in os.scandir(os.path.dirname(module.__file__)):
        name = item.name.split(".")[0]
        if name not in ["__init__", "__pycache__"]:
            if hasattr(module, name):
                submodule = getattr(module, name)
                ret.append(submodule)
    if get:
        ret = list(filter(lambda x: hasattr(x, get), ret))

    ret.sort(key=lambda x: x.order)

    if get:
        ret = list(map(lambda x: getattr(x, get), ret))

    return ret


def collect_module_name(root, prefix=None) -> list[str]:
    ret = []
    for module in os.scandir(os.path.dirname(root)):
        if module.is_dir() and module.name != "__pycache__":
            ret.append(f"{prefix}.{module.name}") if prefix else ret.append(module.name)
    return ret
