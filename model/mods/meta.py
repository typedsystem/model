from typed.meta import DICT, TYPE

class SCHEMA(DICT):
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
        from typed import every
        from model.mods.check import check
        from typed.mods.typesystem import issub

        if check.model.isordered(other):
            if not check.model.isordered(typ):
                return False
        if check.model.isstrict(other):
            if not check.model.isstrict(typ):
                return False

        typ_fields = getattr(typ, '__fields__', None)
        other_fields = getattr(other, '__fields__', None)

        if check.model.ismodel(other) and typ_fields is not None and other_fields is not None:
            if not every(k in typ_fields for k in other_fields):
                return False
            return every(issub(typ_fields[k], other_fields[k]) for k in other_fields)
        return super().__issub__(other)

    def __call__(met, typesystem=None, __check__: bool=None, **fields):
        if not getattr(met, '__is_base_schema__', False):
            from model.mods.check import require
            require.model.validate(met, fields)
            return dict(**fields)

        from model.mods.resolve import resolve
        from model.mods.check import require

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        cache_key = (met, frozenset(fields.items()), id(typesystem), resolved_check)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            require.every.ismember(set(fields.values()), typesystem)

        display_name = f"Schema({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "Schema"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(fields.values()) if fields else set()
        from typed import Str

        _fields = fields
        _types_set = types_set
        _display_name = display_name
        _resolved_check = resolved_check
        _typesystems = {TYPESYSTEM, typesystem}

        class Schema(met, metaclass=SCHEMA):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_schema=True))
            __typesystems__ = _typesystems
            __display__ = _display_name
            __fields__ = _fields
            __types__ = _types_set
            __key_type__ = Str
            __check__ = _resolved_check
            __is_base_schema__ = False

        for k, v in fields.items():
            type.__setattr__(Schema, k, v)

        Schema.__name__ = display_name
        met.__cache__[cache_key] = Schema
        return Schema


class ORDERED_SCHEMA(SCHEMA):
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
        from model.mods.check import check
        if check.model.ismodel(other):
            typ_fields = getattr(typ, '__fields__', None)
            other_fields = getattr(other, '__fields__', None)
            if typ_fields is not None and other_fields is not None:
                if not super().__issub__(other):
                    return False
                if check.model.isordered(other):
                    filtered_typ_fields = [k for k in typ_fields if k in other_fields]
                    if filtered_typ_fields != list(other_fields.keys()):
                        return False
                return True
        return super(SCHEMA, typ).__issub__(other)

    def __call__(met, typesystem=None, __check__: bool = None, **fields):
        if not getattr(met, '__is_base_schema__', False):
            from model.mods.check import require
            require.model.validate(met, fields)
            return dict(**fields)

        from model.mods.resolve import resolve
        from model.mods.check import check
        from typed import Str

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        cache_key = (met, tuple(fields.items()), id(typesystem), resolved_check)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            check.every.ismember(set(fields.values()), typesystem)

        display_name = f"OrderedSchema({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "OrderedSchema"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(fields.values()) if fields else set()

        _fields = fields
        _types_set = types_set
        _display_name = display_name
        _resolved_check = resolved_check
        _typesystems = {TYPESYSTEM, typesystem}

        class OrderedSchema(met, metaclass=type(met)):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_schema=True, is_ordered=True))
            __typesystems__ = _typesystems
            __display__ = _display_name
            __fields__ = _fields
            __types__ = _types_set
            __key_type__ = Str
            __check__ = _resolved_check
            __is_base_schema__ = False

        for k, v in fields.items():
            type.__setattr__(OrderedSchema, k, v)

        OrderedSchema.__name__ = display_name
        met.__cache__[cache_key] = OrderedSchema
        return OrderedSchema


class STRICT_SCHEMA(SCHEMA):
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
        from model.mods.check import check

        if check.model.ismodel(other):
            typ_fields = getattr(typ, '__fields__', None)
            other_fields = getattr(other, '__fields__', None)
            if typ_fields is not None and other_fields is not None:
                if check.model.isstrict(other):
                    if set(typ_fields.keys()) != set(other_fields.keys()):
                        return False
                    return every(issub(typ_fields[k], other_fields[k]) for k in other_fields)
        return super(SCHEMA, typ).__issub__(other)

    def __call__(met, typesystem=None, __check__: bool=None, **fields):
        if not getattr(met, '__is_base_schema__', False):
            from model.mods.check import require
            require.model.validate(met, fields)
            return dict(**fields)

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

        display_name = f"StrictSchema({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "StrictSchema"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(fields.values()) if fields else set()

        _fields = fields
        _types_set = types_set
        _display_name = display_name
        _resolved_check = resolved_check
        _typesystems = {TYPESYSTEM, typesystem}

        class StrictSchema(met, metaclass=type(met)):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_schema=True, is_strict=True))
            __typesystems__ = _typesystems
            __display__ = _display_name
            __fields__ = _fields
            __types__ = _types_set
            __key_type__ = Str
            __check__ = _resolved_check
            __is_base_schema__ = False

        for k, v in fields.items():
            type.__setattr__(StrictSchema, k, v)

        StrictSchema.__name__ = display_name
        met.__cache__[cache_key] = StrictSchema
        return StrictSchema

class MODEL(TYPE):
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

    def __call__(met, __origin_cls__=None, __defaults__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        cache_key = (met, frozenset(fields.items()), __origin_cls__)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"Model({', '.join(f'{k}={nameof(v)}' for k, v in fields.items())})" if fields else "Model"
        bases = (met, __origin_cls__) if __origin_cls__ else (met,)

        _fields = fields
        _defaults = __defaults__ if __defaults__ is not None else {}
        _display_name = display_name

        class Model(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(Model, k, v)

        Model.__name__ = getattr(__origin_cls__, '__name__', display_name)
        met.__cache__[cache_key] = Model
        return Model


class ORDERED_MODEL(MODEL):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        fields = getattr(typ, "__fields__", None)
        if fields is not None:
            trm_fields = getattr(trm, "__fields__", {})
            filtered_term_keys = [k for k in trm_fields if k in fields]
            if filtered_term_keys != list(fields.keys()):
                return False
        return True

    def __call__(met, __origin_cls__=None, __defaults__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        cache_key = (met, tuple(fields.items()), __origin_cls__)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"OrderedModel({', '.join(f'{k}={nameof(v)}' for k, v in fields.items())})" if fields else "OrderedModel"
        bases = (met, __origin_cls__) if __origin_cls__ else (met,)

        _fields = fields
        _defaults = __defaults__ if __defaults__ is not None else {}
        _display_name = display_name

        class OrderedModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(OrderedModel, k, v)

        OrderedModel.__name__ = getattr(__origin_cls__, '__name__', display_name)
        met.__cache__[cache_key] = OrderedModel
        return OrderedModel


class STRICT_MODEL(MODEL):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        fields = getattr(typ, "__fields__", None)
        if fields is not None:
            trm_fields = getattr(trm, "__fields__", {})
            if len(trm_fields) != len(fields):
                return False
        return True

    def __call__(met, __origin_cls__=None, __defaults__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        cache_key = (met, frozenset(fields.items()), __origin_cls__)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"StrictModel({', '.join(f'{k}={nameof(v)}' for k, v in fields.items())})" if fields else "StrictModel"
        bases = (met, __origin_cls__) if __origin_cls__ else (met,)

        _fields = fields
        _defaults = __defaults__ if __defaults__ is not None else {}
        _display_name = display_name

        class StrictModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(StrictModel, k, v)

        StrictModel.__name__ = getattr(__origin_cls__, '__name__', display_name)
        met.__cache__[cache_key] = StrictModel
        return StrictModel


class LAZY_MODEL(MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        cache_key = (met, frozenset(fields.items()), __origin_cls__)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyModel({', '.join(f'{k}={nameof(v)}' for k, v in fields.items())})" if fields else "LazyModel"
        bases = (met, __origin_cls__) if __origin_cls__ else (met,)

        _fields = fields
        _defaults = __defaults__ if __defaults__ is not None else {}
        _display_name = display_name

        class LazyModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyModel, k, v)

        LazyModel.__name__ = getattr(__origin_cls__, '__name__', display_name)
        met.__cache__[cache_key] = LazyModel
        return LazyModel


class LAZY_ORDERED_MODEL(LAZY_MODEL, ORDERED_MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        cache_key = (met, tuple(fields.items()), __origin_cls__)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyOrderedModel({', '.join(f'{k}={nameof(v)}' for k, v in fields.items())})" if fields else "LazyOrderedModel"
        bases = (met, __origin_cls__) if __origin_cls__ else (met,)

        _fields = fields
        _defaults = __defaults__ if __defaults__ is not None else {}
        _display_name = display_name

        class LazyOrderedModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyOrderedModel, k, v)

        LazyOrderedModel.__name__ = getattr(__origin_cls__, '__name__', display_name)
        met.__cache__[cache_key] = LazyOrderedModel
        return LazyOrderedModel


class LAZY_STRICT_MODEL(LAZY_MODEL, STRICT_MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        cache_key = (met, frozenset(fields.items()), __origin_cls__)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyStrictModel({', '.join(f'{k}={nameof(v)}' for k, v in fields.items())})" if fields else "LazyStrictModel"
        bases = (met, __origin_cls__) if __origin_cls__ else (met,)

        _fields = fields
        _defaults = __defaults__ if __defaults__ is not None else {}
        _display_name = display_name

        class LazyStrictModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyStrictModel, k, v)

        LazyStrictModel.__name__ = getattr(__origin_cls__, '__name__', display_name)
        met.__cache__[cache_key] = LazyStrictModel
        return LazyStrictModel
