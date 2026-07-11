from typing import TypeVar, Type, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from model.mods.types import Model, Schema

T = TypeVar('T')

class model:
    def __new__(cls, __cls__: Type[T] = None, *, check: bool = None, lazy: bool = None, strict: bool = None, ordered: bool = None):

        def decorator(c: Type[T]) -> 'Union[Type[T], Type[Model]]':
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
    from typed.mods.func import hints
    from typed.err import NotDefined
    import functools

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

    @functools.wraps(func)
    def getter(self):
        value = func(self)
        from typed.mods.check import check

        if not check.bind.cod(func, sig, value):
            from model.mods.err import FieldErr
            from model.mods.check import _safe_term

            raise FieldErr(
                message=f"Field returned invalid type.",
                key=func,
                field=_safe_term(value),
                expected=(sig.cod,),
                received=type(value)
            )
        return value

    return property(getter)

def schema(obj) -> 'Type[Schema]':
    from model.mods.check import check
    def _traverse(val):
        if check.model.ismodel(val):
            return schema(val)
        elif check.model.ismodel(type(val)):
            return schema(val)
        elif isinstance(val, list):
            return [_traverse(v) for v in val]
        elif isinstance(val, dict):
            return {k: _traverse(v) for k, v in val.items()}
        elif isinstance(val, tuple):
            return tuple(_traverse(v) for v in val)
        return val

    if check.model.ismodel(obj):
        from model.mods.types import Schema, OrderedSchema, StrictSchema
        from typed.mods.func import hints
        from typed import get

        raw_fields = dict(getattr(obj, "__fields__", {}))
        schema_fields = {}

        for k, v in raw_fields.items():
            schema_fields[k] = _traverse(v)
        for key in dir(obj):
            attr = getattr(obj, key, None)
            if isinstance(attr, property):
                h = hints(attr.fget)
                if 'return' in h:
                    schema_fields[key] = _traverse(h['return'])
        is_strict = get(obj, "__flags__.model.is_strict", False)
        is_ordered = get(obj, "__flags__.model.is_ordered", False)
        if is_strict:
            return StrictSchema(**schema_fields)
        if is_ordered:
            return OrderedSchema(**schema_fields)
        return Schema(**schema_fields)

    meta = type(obj)
    fields = getattr(meta, "__fields__", {})
    out = {}
    for key in fields:
        if hasattr(obj, key):
            out[key] = _traverse(getattr(obj, key))

    for key in dir(meta):
        attr = getattr(meta, key, None)
        if isinstance(attr, property):
            out[key] = _traverse(getattr(obj, key))

    return out

from typed.poly import Poly

fields = Poly("__fields__")

def unwrap(obj):
    fields = getattr(obj, "__fields__", None)
    if fields is not None:
        return {k: unwrap(v) for k, v in fields.items()}

    if isinstance(obj, dict):
        return {k: unwrap(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [unwrap(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(unwrap(v) for v in obj)

    return obj
