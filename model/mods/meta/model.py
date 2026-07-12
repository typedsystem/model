from typed.meta import TYPE
from model.helper.meta import _resolve

class MODEL(TYPE):
    __cache__ = {}

    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm

        if getattr(typ, '__is_base_model__', False):
            return isinstance(trm, type)

        if isinstance(trm, typ):
            return True

        fields = getattr(typ, "__fields__", {})
        for key, expected_type in fields.items():
            if not hasattr(trm, key):
                return False
            if not isterm(getattr(trm, key), expected_type):
                return False
        return True

    def __issub__(typ, other):
        from typed import prop
        from model.mods.check import check

        if not check.every.isterm(
            (prop.typeof(typ, level=2), prop.typeof(other, level=2)),
            MODEL
        ):
            return False

        return check.issub(typ.schema(), other.schema())

    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, frozenset(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"Model({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "Model"

        _display_name = display_name

        class Model(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(Model, k, v)

        Model.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
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

    def __issub__(typ, other):
        from typed import prop
        from model.mods.check import check

        if not check.every.isterm(
            (prop.typeof(typ, level=2), prop.typeof(other, level=2)),
            ORDERED_MODEL
        ):
            return False

        return super(ORDERED_MODEL, typ).__issub__(other)

    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, tuple(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"OrderedModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "OrderedModel"

        _display_name = display_name

        class OrderedModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(OrderedModel, k, v)

        OrderedModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
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

    def __issub__(typ, other):
        from typed import prop
        from model.mods.check import check

        if not check.every.isterm(
            (prop.typeof(typ, level=2), prop.typeof(other, level=2)),
            STRICT_MODEL
        ):
            return False

        return super(STRICT_MODEL, typ).__issub__(other)

    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, frozenset(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"StrictModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "StrictModel"

        _display_name = display_name

        class StrictModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(StrictModel, k, v)

        StrictModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = StrictModel
        return StrictModel

class LAZY_MODEL(MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, frozenset(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "LazyModel"

        _display_name = display_name

        class LazyModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyModel, k, v)

        LazyModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = LazyModel
        return LazyModel


class LAZY_ORDERED_MODEL(LAZY_MODEL, ORDERED_MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, tuple(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyOrderedModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "LazyOrderedModel"

        _display_name = display_name

        class LazyOrderedModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyOrderedModel, k, v)

        LazyOrderedModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = LazyOrderedModel
        return LazyOrderedModel


class LAZY_STRICT_MODEL(LAZY_MODEL, STRICT_MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, frozenset(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyStrictModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "LazyStrictModel"

        _display_name = display_name

        class LazyStrictModel(*bases, metaclass=type(met)):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyStrictModel, k, v)

        LazyStrictModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = LazyStrictModel
        return LazyStrictModel
