from typed import lazy

__imports__ = {
    "model.types": [
        "Model", "OrderedModel", "StrictModel",
        "Schema", "OrderedSchema", "StrictSchema",
        "LazyModel", "LazyOrderedModel", "LazyStrictModel"
    ],
    "model.wrap": [
        "model"
    ],
    "model.checker": [
        "check", "require"
    ],
    "model.resolve": [
        "resolve"
    ]
}

if lazy(__imports__):
    from model.types import (
        Model, OrderedModel, StrictModel,
        Schema, OrderedSchema, StrictSchema,
        LazyModel, LazyOrderedModel, LazyStrictModel
    )
    from model.wrap import model
    from model.checker import check, require
    from model.resolve import resolve
