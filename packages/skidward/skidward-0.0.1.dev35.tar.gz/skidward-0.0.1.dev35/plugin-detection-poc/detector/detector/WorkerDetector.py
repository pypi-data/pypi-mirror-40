"""Contains calls to demonstrate dynamic detection and registration of modules"""
from types import ModuleType
from typing import List

import detector.ModuleAccessor


class WorkerDetector(object):
    def __init__(self):
        self.imported_workers: List[ModuleType] = []
        self.module_accessor = detector.ModuleAccessor.ModuleAccessor()

    def get_imported_workers(self) -> List[ModuleType]:
        return self.imported_workers

    def import_worker(self, name: str):
        try:
            worker = self.module_accessor.load_unregistered_module_by_name(name)
            self.imported_workers.append(worker)
        except ValueError:
            print(f'No module could be loaded by the name {name}')

    def trigger_message_from_imported_workers(self):
        for worker in self.imported_workers:
            worker.print_worker_message()

    def get_unregistered_workers(self) -> List[str]:
        return self.module_accessor.get_unregistered_module_names()
