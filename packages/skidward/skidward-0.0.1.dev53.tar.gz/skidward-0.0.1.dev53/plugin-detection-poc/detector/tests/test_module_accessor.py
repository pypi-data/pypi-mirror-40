import pytest
from types import ModuleType
import pkg_resources

from detector.ModuleAccessor import ModuleAccessor


@pytest.fixture
def module_accessor():
    return ModuleAccessor()


class MockEntryPoint(ModuleType):
    def __init__(self, name, module_name):
        self.name = name
        self.module_name = module_name

    def load(self) -> ModuleType:
        return ModuleType('name')


def mock_entry_points(namespace):
    return [
        MockEntryPoint('mock_first', 'mock_first'),
        MockEntryPoint('mock_second', 'mock_second')
    ]


def test_detect_unregistered_entry_points(module_accessor, monkeypatch):
    monkeypatch.setattr(
        pkg_resources,
        'iter_entry_points',
        mock_entry_points
    )

    entrypoints = module_accessor._get_unregistered_module_entrypoints()
    assert isinstance(entrypoints, list)
    assert len(entrypoints) == 2
    assert isinstance(entrypoints[0], MockEntryPoint)

    names = module_accessor.get_unregistered_module_names()
    assert isinstance(names, list)
    assert len(names) == 2
    assert isinstance(names[0], str)


def test_load_incorrect_entry_point(module_accessor, monkeypatch):
    monkeypatch.setattr(
        pkg_resources,
        'iter_entry_points',
        mock_entry_points
    )
    with pytest.raises(ValueError):
        module_accessor.load_unregistered_module_by_name('')


def test_load_unregistered_entry_point(module_accessor, monkeypatch):
    monkeypatch.setattr(
        pkg_resources,
        'iter_entry_points',
        mock_entry_points
    )
    module = module_accessor.load_unregistered_module_by_name('mock_first')

    assert module is not None
    assert isinstance(module, ModuleType)
