"""Class providing an API for the new module detections"""
from types import ModuleType
from typing import List

import pkg_resources


class ModuleAccessor(object):
    namespace: str = 'skidward.workers'

    def __init__(self):
        pass

    def _get_unregistered_module_entrypoints(self) -> List[ModuleType]:
        modules = []

        for ep in pkg_resources.iter_entry_points(self.namespace):
            modules.append(ep)

        return modules

    def _register_module_entrypoint(self, module_name: str) -> ModuleType:
        module: ModuleType = None

        for entrypoint in self._get_unregistered_module_entrypoints():
            if entrypoint.module_name == module_name:
                module = entrypoint.load()

        if module is None:
            raise ValueError(f'No module found by name {module_name}.')

        return module

    def get_unregistered_module_names(self) -> List[str]:
        module_names = []

        for ep in self._get_unregistered_module_entrypoints():
            module_names.append(ep.module_name)

        return module_names

    def load_unregistered_module_by_name(self, name: str) -> ModuleType:
        return self._register_module_entrypoint(name)

