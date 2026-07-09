from typed.check import (
    Checker as TypedChecker,
    check as typed_check,
    require as typed_require
)

class ModelChecker(TypedChecker):
    def ismodel(self, objs) -> bool:
        from model.mods.meta import MODEL
        from typed.mods.typesystem import isterm
        q = self.quantifier

        if q is None:
            res = isterm(objs, MODEL)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="ismodel",
                        term=objs,
                        expected=(MODEL,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(isterm(obj, MODEL) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="ismodel",
                    term=objs,
                    expected=(MODEL,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def isordered(self, objs) -> bool:
        from model.mods.meta import ORDERED_MODEL
        from typed.mods.typesystem import isterm
        q = self.quantifier

        if q is None:
            res = isterm(objs, ORDERED_MODEL)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isordered",
                        term=objs,
                        expected=(ORDERED_MODEL,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(isterm(obj, ORDERED_MODEL) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isordered",
                    term=objs,
                    expected=(ORDERED_MODEL,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def isstrict(self, objs) -> bool:
        from model.mods.meta import STRICT_MODEL
        from typed.mods.typesystem import isterm
        q = self.quantifier

        if q is None:
            res = isterm(objs, STRICT_MODEL)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isstrict",
                        term=objs,
                        expected=(STRICT_MODEL,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(isterm(obj, STRICT_MODEL) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isstrict",
                    term=objs,
                    expected=(STRICT_MODEL,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
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

class require(typed_require):
    class model:
        ismodel = __require__.ismodel
        isordered = __require__.isordered
        isstrict = __require__.isstrict
