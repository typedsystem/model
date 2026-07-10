from typing import TypeVar, Type

T = TypeVar('T')

class model:
    def __new__(cls, __cls__: Type[T] = None, *, check: bool = None, lazy: bool = None, strict: bool = None, ordered: bool = None):
        def decorator(c: Type[T]) -> Type[T]:
            from model.mods.resolve import resolve
            from model.mods.types import (
                Model, OrderedModel, StrictModel,
                LazyModel, LazyOrderedModel, LazyStrictModel
            )

            lz = resolve.model.lazy(lazy)
            chk = resolve.model.check(check)
            st = resolve.model.strict(strict)
            od = resolve.model.ordered(ordered)

            try:
                from typed.mods.func import hints
                fields = hints(c)
            except Exception:
                fields = {}

            defaults = {k: getattr(c, k) for k in fields if hasattr(c, k)}

            if lz:
                if od:
                    return LazyOrderedModel(__origin_cls__=c, __defaults__=defaults, **fields)
                if st:
                    return LazyStrictModel(__origin_cls__=c, __defaults__=defaults, **fields)
                return LazyModel(__origin_cls__=c, __defaults__=defaults, **fields)
            else:
                if od:
                    return OrderedModel(__origin_cls__=c, __defaults__=defaults, **fields)
                if st:
                    return StrictModel(__origin_cls__=c, __defaults__=defaults, **fields)
                return Model(__origin_cls__=c, __defaults__=defaults, **fields)

        if __cls__ is None:
            return decorator
        return decorator(__cls__)

    @staticmethod
    def strict(__cls__: Type[T] = None, *, check: bool = None, lazy: bool = None) -> Type[T]:
        return model(__cls__, check=check, lazy=lazy, strict=True)

    @staticmethod
    def ordered(__cls__: Type[T] = None, *, check: bool = None, lazy: bool = None) -> Type[T]:
        return model(__cls__, check=check, lazy=lazy, ordered=True)


def field(func):
    from typed.func import hints
    from typed.err import NotDefined

    h = hints(func)
    if 'return' not in h:
        from model.mods.err import FieldErr
        raise FieldErr(
            message=f"Dynamic field has no codomain",
            field=func,
            expected="some type",
            received=NotDefined
        )

    from typed.mods.func import signature
    sig = signature(func)

    def getter(self):
        value = func(self)
        from typed.check import check

        if not check.bind.cod(func, sig, value):
            from model.mods.err import FieldErr
            from model.mods.check import _safe_term

            raise FieldErr(
                message=f"Field has invalid type",
                key=func.__name__,
                field=_safe_term(value),
                expected=(sig.cod,),
                received=type(value)
            )
        return value
    return property(getter)


def schema(obj) -> dict:
    meta = type(obj)

    fields = getattr(meta, "__fields__", {})
    out = {
        key: getattr(obj, key) 
        for key in fields 
        if hasattr(obj, key)
    }

    for key in dir(meta):
        attr = getattr(meta, key, None)
        if isinstance(attr, property):
            out[key] = getattr(obj, key)

    return out
