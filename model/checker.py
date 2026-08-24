from typed import lazy

__imports__ = {
    "model.mods.check": [
        "check", "require"
    ]
}

if lazy(__imports__):
    from model.mods.check import (
        check, require
    )
