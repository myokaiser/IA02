import importlib

def load_map(name):

    try:
        module = importlib.import_module(
            f"maps.{name}"
        )

        return module.WORLD

    except Exception:

        raise ValueError(
            f"Unknown map '{name}'"
        )