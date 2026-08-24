from typed import lazy

__imports__ = {
    "model.mods.wrap": [
        "model"
    ]
}

if lazy(__imports__):
    from model.mods.wrap import model
