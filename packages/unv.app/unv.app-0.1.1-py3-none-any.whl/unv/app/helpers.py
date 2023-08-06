import importlib
import pathlib

from .settings import SETTINGS


def get_app_components():
    for component in SETTINGS['components']:
        component = '{}.app'.format(component)
        yield importlib.import_module(component)


def get_project_root(app_module: str = 'app.settings') -> pathlib.Path:
    """Return project root path, outside "src" directory."""
    return pathlib.Path(SETTINGS['root'])
