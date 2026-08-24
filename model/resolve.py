from typed import lazy

__imports__ = {
    "model.mods.resolve": [
        "resolve"
    ]
}

if lazy(__imports__):
    from model.mods.resolve import (
        resolve
    )
