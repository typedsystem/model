from typed.check import (
    Checker as TypedChecker,
    check as typed_check,
    require as typed_require
)

def _safe_term(val):
    """
    Wraps unhashable terms in a dynamic hashable object with the same class name.
    """
    try:
        hash(val)
        return val
    except TypeError:
        return type(type(val).__name__, (), {})()

class ModelChecker(TypedChecker):
    def ismodel(self, objs) -> bool:
        from model.mods.meta import MODEL
        from model.mods.check import check
        q = self.quantifier

        if q is None:
            res = check.isterm(objs, MODEL)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="ismodel",
                        term=_safe_term(objs),
                        expected=(MODEL,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(check.isterm(obj, MODEL) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="ismodel",
                    term=_safe_term(objs),
                    expected=(MODEL,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def isordered(self, objs) -> bool:
        from model.mods.meta import ORDERED_MODEL
        from model.mods.check import check
        q = self.quantifier

        if q is None:
            res = check.isterm(objs, ORDERED_MODEL)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isordered",
                        term=_safe_term(objs),
                        expected=(ORDERED_MODEL,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(check.isterm(obj, ORDERED_MODEL) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isordered",
                    term=_safe_term(objs),
                    expected=(ORDERED_MODEL,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def isstrict(self, objs) -> bool:
        from model.mods.meta import STRICT_MODEL
        from model.mods.check import check
        q = self.quantifier

        if q is None:
            res = check.isterm(objs, STRICT_MODEL)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isstrict",
                        term=_safe_term(objs),
                        expected=(STRICT_MODEL,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(check.isterm(obj, STRICT_MODEL) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isstrict",
                    term=_safe_term(objs),
                    expected=(STRICT_MODEL,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def validate(self, met, fields) -> bool:
        from typed import get
        from model.mods.check import check

        if not getattr(met, '__check__', True):
            return True

        from model.mods.err import ModelErr, FieldErr

        schema_fields = getattr(met, '__fields__', {})
        defaults = getattr(met, '__defaults__', {})
        is_strict = get(met, "__flags__.model.is_strict", False)
        is_ordered = get(met, "__flags__.model.is_ordered", False)

        for k, default_val in defaults.items():
            if k not in fields:
                fields[k] = default_val

        if is_strict:
            extra = [k for k in fields if k not in schema_fields]
            if extra:
                if self.explode:
                    raise FieldErr(
                        message=f"Strict schema/model received extra keys: {extra}", 
                        keys=extra, 
                        term=_safe_term(fields),
                        expected=(met,)
                    )
                return False

        if is_ordered:
            expected_order = [k for k in schema_fields if k in fields]
            provided_order = list(fields.keys())
            if expected_order != provided_order:
                if self.explode:
                    raise FieldErr(
                        message="Keys are not in the expected order.", 
                        term=_safe_term(fields),
                        expected=(met,)
                    )
                return False

        for k, expected_type in schema_fields.items():
            if k not in fields:
                if self.explode:
                    raise FieldErr(
                        message=f"Missing required key: '{k}'", 
                        key=k, 
                        term=_safe_term(fields),
                        expected=(met,)
                    )
                return False

            val = fields[k]
            if not check.isterm(val, expected_type):
                if self.explode:
                    from typed.mods.typesystem import nameof
                    raise ModelErr(
                        message=f"Invalid type for field '{k}'. Expected {nameof(expected_type)}, got {nameof(type(val))}.",
                        term=_safe_term(val),
                        expected=(expected_type,),
                        received=type(val)
                    )
                return False

        return True

__check__ = ModelChecker(quantifier=None, explode=False)
__require__ = ModelChecker(quantifier=None, explode=True)

class check(typed_check):
    class model:
        ismodel = __check__.ismodel
        isordered = __check__.isordered
        isstrict = __check__.isstrict
        validate = __check__.validate

class require(typed_require):
    class model:
        ismodel = __require__.ismodel
        isordered = __require__.isordered
        isstrict = __require__.isstrict
        validate = __require__.validate
