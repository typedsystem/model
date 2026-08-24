from typed import lazy

__imports__ = {
    "model.mods.err": [
        "ModelErr", "FieldErr"
    ]
}

if lazy(__imports__):
    from model.mods.err import ModelErr, FieldErr
