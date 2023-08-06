import os
import copy
import importlib

import jsonschema

from unv.utils.collections import update_dict_recur


def create_component_settings(
        key: str, default_settings: dict, schema: dict) -> dict:
    """Create and validate application component settings."""
    try:
        module = importlib.import_module('app.settings')
        app_settings = module.SETTINGS
    except (ImportError, AttributeError):
        app_settings = {}

    settings = copy.deepcopy(default_settings)

    if key in app_settings:
        settings = update_dict_recur(settings, app_settings[key])

    validator = jsonschema.Draft4Validator(schema)
    validator.validate(settings)

    return settings


def load_settings(module_path: str = 'app.settings.development') -> dict:
    """Load settings from provided module_path."""
    module_path = os.environ.get('SETTINGS', module_path)
    module = importlib.import_module(module_path)

    settings = module.SETTINGS
    settings['env'] = module_path.split('.')[-1]

    for key, value in os.environ.items():
        if 'OVERRIDE_SETTINGS_' not in key:
            continue
        current_settings = settings
        parts = [
            part.lower()
            for part in key.replace('OVERRIDE_SETTINGS_', '').split('_')
        ]
        last_index = len(parts) - 1
        for index, part in enumerate(parts):
            if index == last_index:
                if value == 'False':
                    value = False
                elif value == 'True':
                    value = True
                elif value.isdigit():
                    value = int(value)
                current_settings[part] = value
            else:
                current_settings = current_settings.setdefault(part, {})

    return settings
