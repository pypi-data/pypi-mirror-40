from .core import create_component_settings

SCHEMA = {
    "type": "object",
    "properties": {
        "debug": {
            "type": "boolean",
            "required": True
        },
        "components": {
            "type": "array",
            "items": {"type": "string"},
            "required": True
        }
    }
}

DEFAULTS = {
    'debug': False,
    'components': [],
}

SETTINGS = create_component_settings('app', DEFAULTS, SCHEMA)
