from model.mods.meta import (
    SCHEMA, ORDERED_SCHEMA, STRICT_SCHEMA,
    MODEL, ORDERED_MODEL, STRICT_MODEL,
    LAZY_MODEL, LAZY_ORDERED_MODEL, LAZY_STRICT_MODEL
)
from model.mods.flags import Flags, ModelFlags

# ==========================================
# SCHEMAS 
# ==========================================

class Schema(metaclass=SCHEMA):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_schema=True))
    __is_base_schema__ = True
    __null__    = {}
    __builtin__ = dict

    def __size__(trm):
        return len(trm)

    def __getitem__(trm, key):
        return trm.__dict__[key]

    def __setitem__(trm, key, value):
        from typed import check, prop
        fields = getattr(prop.typeof(trm), '__fields__', {})
        if key in fields:
            check.isterm(value, fields[key])
        trm.__dict__[key] = value

    def __contains__(trm, key):
        return key in trm.__dict__


class OrderedSchema(Schema, metaclass=ORDERED_SCHEMA):
    """The constructor type of strictly ordered schemas."""
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_schema=True, is_ordered=True))
    __is_base_schema__ = True
    __null__    = {}
    __builtin__ = dict


class StrictSchema(Schema, metaclass=STRICT_SCHEMA):
    """The constructor type of strictly typed schemas."""
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_schema=True, is_strict=True))
    __is_base_schema__ = True
    __null__    = {}
    __builtin__ = dict


# ==========================================
# MODELS
# ==========================================

class Model(metaclass=MODEL):
    """The constructor type of structured classes (Models)."""
    __flags__ = Flags(is_constructor=True, model=ModelFlags(is_model=True))
    __is_base_model__ = True

    def schema(trm) -> dict:
        from model.mods.func import schema as _schema
        return _schema(trm)


class OrderedModel(Model, metaclass=ORDERED_MODEL):
    """The constructor type of strictly ordered models."""
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_ordered=True))
    __is_base_model__ = True


class StrictModel(Model, metaclass=STRICT_MODEL):
    """The constructor type of strictly defined models."""
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_strict=True))
    __is_base_model__ = True


# ==========================================
# LAZY MODELS
# ==========================================

class LazyModel(Model, metaclass=LAZY_MODEL):
    """The constructor type of lazy models."""
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True))
    __is_base_model__ = True


class LazyOrderedModel(LazyModel, OrderedModel, metaclass=LAZY_ORDERED_MODEL):
    """The constructor type of lazy ordered models."""
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True, is_ordered=True))
    __is_base_model__ = True


class LazyStrictModel(LazyModel, StrictModel, metaclass=LAZY_STRICT_MODEL):
    """The constructor type of lazy strict models."""
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True, is_strict=True))
    __is_base_model__ = True
