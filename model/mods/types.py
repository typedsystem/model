from model.mods.meta import (
    TYPED_DICT, TYPED_DICT_ORDERED, TYPED_DICT_STRICT,
    MODEL, MODEL_ORDERED, MODEL_STRICT,
    LAZY_MODEL, LAZY_MODEL_ORDERED, LAZY_MODEL_STRICT
)
from model.mods.flags import Flags, ModelFlags

class TypedDict(metaclass=TYPED_DICT):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_typed_dict=True))
    __null__    = {}
    __builtin__ = dict

    def __size__(trm):
        return len(trm)

    def __getitem__(trm, key):
        return trm.__dict__[key]

    def __setitem__(trm, key, value):
        from typed.mods.typesystem import typeof
        from typed.mods.check import check

        fields = getattr(typeof(trm), '__fields__', {})
        if key in fields:
            check.isterm(value, fields[key])

        trm.__dict__[key] = value

    def __contains__(trm, key):
        return key in trm.__dict__

class TypedDictOrdered(TypedDict, metaclass=TYPED_DICT_ORDERED):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_typed_dict=True, is_ordered=True))
    __null__    = {}
    __builtin__ = dict


class TypedDictStrict(TypedDict, metaclass=TYPED_DICT_STRICT):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_typed_dict=True, is_strict=True))
    __null__    = {}
    __builtin__ = dict

class Model(metaclass=MODEL):
    __flags__ = Flags(is_constructor=True, model=ModelFlags(is_model=True))

class ModelOrdered(Model, metaclass=MODEL_ORDERED):
    __flags__ = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_ordered=True))

class ModelStrict(Model, metaclass=MODEL_STRICT):
    __flags__ = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_strict=True))

class LazyModel(Model, metaclass=LAZY_MODEL):
    __flags__ = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True))

class LazyModelOrdered(LazyModel, metaclass=LAZY_MODEL_ORDERED):
    __flags__ = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True, is_ordered=True))

class LazyModelStrict(LazyModel, metaclass=LAZY_MODEL_STRICT):
    __flags__ = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True, is_strict=True))
