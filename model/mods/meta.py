from typed.meta import DICT, TYPE

class MODEL(DICT):
    __cache__ = {}

    def __isterm__(typ, trm):
        from typed import every, check, prop

        if not check.isinstance(trm, dict) and not check.issub(prop.typeof(trm, level=2), DICT):
            return False

        fields = getattr(typ, "__fields__", None)
        if fields is not None:
            if not every(k in trm for k in fields):
                return False
            return every(check.isterm(trm[k], expected_type) for k, expected_type in fields.items())
        return True

    def __issub__(typ, other):
        from typed import check, every, get
        from model.mods.flags import flag

        if get(other, '__flags__.model.is_ordered', None):
            if not getattr(typ, '__flags__.model.is_ordered', False):
                return False

        if get(other, '__flags__', None) and getattr(other.__flags__, 'is_strict', False):
            if not getattr(typ.__flags__, 'is_strict', False):
                return False

        typ_fields = getattr(typ, '__fields__', None)
        other_fields = getattr(other, '__fields__', None)

        if isinstance(other, MODEL) and typ_fields is not None and other_fields is not None:
            if not every(k in typ_fields for k in other_fields):
                return False
            return every(issub(typ_fields[k], other_fields[k]) for k in other_fields)

        return super().__issub__(other)

    def __call__(met, typesystem=None, __check__: bool=None, **fields):
        from model.mods.resolve import resolve
        from model.mods.check import require

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        cache_key = (met, frozenset(fields.items()), id(typesystem), resolved_check)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            require.every.ismember(set(fields.values()), typesystem)

        display_name = f"Model({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "Model"

        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM
        types_set = set(fields.values()) if fields else set()
        from typed import Str

        class Model(met, metaclass=MODEL):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __fields__ = fields
            __types__ = types_set
            __key_type__ = Str
            __check__ = resolved_check

        Model.__name__ = display_name
        met.__cache__[cache_key] = Model
        return Model


class ORDERED_MODEL(MODEL):
    """
    The metatype of strictly ordered record/model types.
    """
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False

        fields = getattr(typ, "__fields__", None)
        if fields is not None:
            filtered_term_keys = [k for k in trm if k in fields]
            if filtered_term_keys != list(fields.keys()):
                return False
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub

        if isinstance(other, MODEL):
            typ_fields = getattr(typ, '__fields__', None)
            other_fields = getattr(other, '__fields__', None)

            if typ_fields is not None and other_fields is not None:
                if not super().__issub__(other):
                    return False
                if getattr(other, '__flags__', None) and getattr(other.__flags__, 'is_ordered_model', False):
                    filtered_typ_fields = [k for k in typ_fields if k in other_fields]
                    if filtered_typ_fields != list(other_fields.keys()):
                        return False
                return True
        return super(MODEL, typ).__issub__(other)

    def __call__(met, typesystem=None, __check__: bool = None, **fields):
        from model.mods.resolve import resolve
        from model.mods.check import check

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        cache_key = (met, tuple(fields.items()), id(typesystem), resolved_check)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            check.every.ismember(set(fields.values()), typesystem)

        display_name = f"OrderedModel({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "OrderedModel"

        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        types_set = set(fields.values()) if fields else set()

        class OrderedModel(met, metaclass=ORDERED_MODEL):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __flags__.is_ordered_model = True
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __fields__ = fields
            __types__ = types_set
            __key_type__ = Str
            __check__ = resolved_check

        OrderedModel.__name__ = display_name
        met.__cache__[cache_key] = OrderedModel
        return OrderedModel


class STRICT_MODEL(MODEL):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False

        fields = getattr(typ, "__fields__", None)
        if fields is not None and len(trm) != len(fields):
            return False
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        from typed.mods.init import every

        if isinstance(other, MODEL):
            typ_fields = getattr(typ, '__fields__', None)
            other_fields = getattr(other, '__fields__', None)

            if typ_fields is not None and other_fields is not None:
                if getattr(other, '__flags__', None) and getattr(other.__flags__, 'is_strict_model', False):
                    if set(typ_fields.keys()) != set(other_fields.keys()):
                        return False
                    return every(issub(typ_fields[k], other_fields[k]) for k in other_fields)
        return super(MODEL, typ).__issub__(other)

    def __call__(met, typesystem=None, __check__: bool = None, **fields):
        from model.mods.resolve import resolve
        from model.mods.check import check
        from typed.mods.types.atomic import Str

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        cache_key = (met, frozenset(fields.items()), id(typesystem), resolved_check)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            check.every.ismember(set(fields.values()), typesystem)

        display_name = f"StrictModel({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "StrictModel"

        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        types_set = set(fields.values()) if fields else set()

        class StrictModel(met, metaclass=STRICT_MODEL):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __flags__.is_strict_model = True
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __fields__ = fields
            __types__ = types_set
            __key_type__ = Str
            __check__ = resolved_check

        StrictModel.__name__ = display_name
        met.__cache__[cache_key] = StrictModel
        return StrictModel

class COMP_TYPE(TYPE):
    """
    Metatype for structured classes, validating static attributes.
    """
    __cache__ = {}

    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        if not isinstance(trm, type):
            return False

        fields = getattr(typ, "__fields__", {})
        for key, expected_type in fields.items():
            if not hasattr(trm, key):
                return False
            if not isterm(getattr(trm, key), expected_type):
                return False

        return True

    def __call__(met, **fields):
        cache_key = (met, frozenset(fields.items()))
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        display_name = f"CompType({', '.join(f'{k}={v}' for k, v in fields.items())})" if fields else "CompType"

        class CompType(met, metaclass=type(met)):
            __kind__ = "type"
            __display__ = display_name
            __fields__ = fields

        CompType.__name__ = display_name
        met.__cache__[cache_key] = CompType
        return CompType


class LAZY_COMP_TYPE(COMP_TYPE):
    """
    Lazy counterpart of COMP_TYPE.
    """
    def __call__(met, **fields):
        cache_key = (met, frozenset(fields.items()))
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        display_name = f"LazyCompType({', '.join(f'{k}={v}' for k, v in fields.items())})" if fields else "LazyCompType"

        class LazyCompType(met, metaclass=type(met)):
            __kind__ = "type"
            __display__ = display_name
            __fields__ = fields

        LazyCompType.__name__ = display_name
        met.__cache__[cache_key] = LazyCompType
        return LazyCompType
