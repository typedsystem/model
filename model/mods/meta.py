from typed.meta import DICT, TYPE

class TYPED_DICT(DICT):
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
        from model.mods.resolve import resolve
        from model.mods.check import require

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        cache_key = (met, frozenset(fields.items()), id(typesystem), resolved_check)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            require.every.ismember(set(fields.values()), typesystem)

        display_name = f"TypedDict({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "TypedDict"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(fields.values()) if fields else set()
        from typed import Str

        class TypedDict(met, metaclass=TYPED_DICT):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_typed_dict=True))
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __fields__ = fields
            __types__ = types_set
            __key_type__ = Str
            __check__ = resolved_check

        TypedDict.__name__ = display_name
        met.__cache__[cache_key] = TypedDict
        return TypedDict


class TYPED_DICT_ORDERED(TYPED_DICT):
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
        return super(TYPED_DICT, typ).__issub__(other)

    def __call__(met, typesystem=None, __check__: bool = None, **fields):
        from model.mods.resolve import resolve
        from model.mods.check import check
        from typed.mods.types.atomic import Str

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        cache_key = (met, tuple(fields.items()), id(typesystem), resolved_check)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            check.every.ismember(set(fields.values()), typesystem)

        display_name = f"TypedDictOrdered({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "TypedDictOrdered"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(fields.values()) if fields else set()

        class TypedDictOrdered(met, metaclass=TYPED_DICT_ORDERED):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_typed_dict=True, is_ordered=True))
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __fields__ = fields
            __types__ = types_set
            __key_type__ = Str
            __check__ = resolved_check

        TypedDictOrdered.__name__ = display_name
        met.__cache__[cache_key] = TypedDictOrdered
        return TypedDictOrdered


class TYPED_DICT_STRICT(TYPED_DICT):
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
        return super(TYPED_DICT, typ).__issub__(other)

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

        display_name = f"StrictTypedDict({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in fields.items())})" if fields else "StrictTypedDict"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(fields.values()) if fields else set()

        class StrictTypedDict(met, metaclass=TYPED_DICT_STRICT):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_typed_dict=True, is_strict=True))
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __fields__ = fields
            __types__ = types_set
            __key_type__ = Str
            __check__ = resolved_check

        StrictTypedDict.__name__ = display_name
        met.__cache__[cache_key] = StrictTypedDict
        return StrictTypedDict

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

    def __call__(met, **fields):
        cache_key = (met, frozenset(fields.items()))
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        display_name = f"Model({', '.join(f'{k}={v}' for k, v in fields.items())})" if fields else "Model"

        class Model(met, metaclass=type(met)):
            __kind__ = "type"
            __display__ = display_name
            __fields__ = fields

        Model.__name__ = display_name
        met.__cache__[cache_key] = Model
        return Model

class MODEL_ORDERED(MODEL):
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

    def __call__(met, **fields):
        cache_key = (met, tuple(fields.items()))
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        display_name = f"ModelOrdered({', '.join(f'{k}={v}' for k, v in fields.items())})" if fields else "ModelOrdered"

        class ModelOrdered(met, metaclass=type(met)):
            __kind__ = "type"
            __display__ = display_name
            __fields__ = fields

        ModelOrdered.__name__ = display_name
        met.__cache__[cache_key] = ModelOrdered
        return ModelOrdered

class MODEL_STRICT(MODEL):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        fields = getattr(typ, "__fields__", None)
        if fields is not None:
            trm_fields = getattr(trm, "__fields__", {})
            if len(trm_fields) != len(fields):
                return False
        return True

    def __call__(met, **fields):
        cache_key = (met, frozenset(fields.items()))
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        display_name = f"ModelStrict({', '.join(f'{k}={v}' for k, v in fields.items())})" if fields else "ModelStrict"

        class ModelStrict(met, metaclass=type(met)):
            __kind__ = "type"
            __display__ = display_name
            __fields__ = fields

        ModelStrict.__name__ = display_name
        met.__cache__[cache_key] = ModelStrict
        return ModelStrict

class LAZY_MODEL(MODEL):
    def __call__(met, **fields):
        cache_key = (met, frozenset(fields.items()))
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        display_name = f"LazyModel({', '.join(f'{k}={v}' for k, v in fields.items())})" if fields else "LazyModel"

        class LazyModel(met, metaclass=type(met)):
            __kind__ = "type"
            __display__ = display_name
            __fields__ = fields

        LazyModel.__name__ = display_name
        met.__cache__[cache_key] = LazyModel
        return LazyModel

class LAZY_MODEL_ORDERED(MODEL_ORDERED):
    def __call__(met, **fields):
        cache_key = (met, tuple(fields.items()))
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        display_name = f"LazyModelOrdered({', '.join(f'{k}={v}' for k, v in fields.items())})" if fields else "LazyModelOrdered"

        class LazyModelOrdered(met, metaclass=type(met)):
            __kind__ = "type"
            __display__ = display_name
            __fields__ = fields

        LazyModelOrdered.__name__ = display_name
        met.__cache__[cache_key] = LazyModelOrdered
        return LazyModelOrdered

class LAZY_MODEL_STRICT(MODEL_STRICT):
    def __call__(met, **fields):
        cache_key = (met, frozenset(fields.items()))
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        display_name = f"LazyModelStrict({', '.join(f'{k}={v}' for k, v in fields.items())})" if fields else "LazyModelStrict"

        class LazyModelStrict(met, metaclass=type(met)):
            __kind__ = "type"
            __display__ = display_name
            __fields__ = fields

        LazyModelStrict.__name__ = display_name
        met.__cache__[cache_key] = LazyModelStrict
        return LazyModelStrict
