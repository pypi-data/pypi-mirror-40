import pytest
from types import ModuleType
from detector.WorkerDetector import WorkerDetector
from detector.ModuleAccessor import ModuleAccessor

@pytest.fixture
def worker_detector():
    return WorkerDetector()


def test_empty_initial_workers(worker_detector):
    workers = worker_detector.get_imported_workers()
    assert isinstance(workers, list)
    assert len(workers) == 0


def test_import_new_worker(worker_detector, monkeypatch):
    def mock_module_registration(first_mockparam, second_mockparam):
        return ModuleType('mocked')

    monkeypatch.setattr(
        ModuleAccessor,
        'load_unregistered_module_by_name',
        mock_module_registration
    )
    worker_detector.import_worker('mock')
    workers = worker_detector.get_imported_workers()
    assert len(workers) > 0


def test_get_unregistered_workers_empty(worker_detector, monkeypatch):
    def mock_module_registration(mockparam):
        return []


    monkeypatch.setattr(
        ModuleAccessor,
        'get_unregistered_module_names',
        mock_module_registration
    )
    workers = worker_detector.get_unregistered_workers()
    assert isinstance(workers, list)
    assert len(workers) == 0
