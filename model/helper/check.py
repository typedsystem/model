def _base_check(self, met, objs):
    from typed import check
    q = self.quantifier
    if q is None:
        res = check.isterm(objs, met)
        if not res:
            if self.explode:
                from typed.err import TypeErr
                from typed import prop
                raise TypeErr(
                    func="isschema",
                    term=objs,
                    expected=(met,),
                    received=prop.typeof(objs)
                )
            return False
        return True

    res = q(check.isterm(obj, met) for obj in objs)
    if not res:
        if self.explode:
            from typed.err import TypeErr
            from typed import prop
            raise TypeErr(
                func="isschema",
                term=objs,
                expected=(met,),
                quantifier=q,
                received=prop.typeof(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(prop.typeof(obj) for obj in objs)
            )
        return False
    return True

def _validate(self, met, typ, fields):
    from typed.mods.check import check
    if not check.isterm(typ, met):
        if self.explode:
            from typed.mods.err import TypeErr
            from model.mods.meta.schema import SCHEMA
            raise TypeErr(
                func="validate",
                term=typ,
                expected=(SCHEMA,)
            )
        return False
    if not fields or not getattr(typ, '__check__', True):
        return True

    _fields = getattr(typ, '__fields__', {})

    is_ordered = False
    is_strict = False
    if met.__name__ == 'Schema':
        from model.mods.types.schema import OrderedSchema, StrictSchema
        is_ordered = check.isterm(typ, OrderedSchema)
        is_strict = check.isterm(typ, StrictSchema)
    else:
        from model.mods.types.model_ import OrderedModel, StrictModel
        is_ordered = check.isterm(typ, OrderedModel)
        is_strict = check.isterm(typ, StrictModel)

    if is_ordered:
        extra = [k for k in fields if k not in _fields]
        if extra:
            if self.explode:
                from model.mods.err import FieldErr
                raise FieldErr(
                    message=f"Received extra keys",
                    keys=extra,
                    term=fields,
                    expected=(typ,)
                )
            return False

    if is_strict:
        expected_order = [k for k in fields if k in _fields]
        provided_order = list(fields.keys())
        if expected_order != provided_order:
            if self.explode:
                from model.mods.err import FieldErr
                raise FieldErr(
                    message="Keys are not in the expected order",
                    term=fields,
                    expected=(typ,)
                )
            return False

    for k, expected_type in _fields.items():
        if k not in fields:
            if self.explode:
                from model.mods.err import FieldErr
                raise FieldErr(
                    message=f"Missing required key",
                    key=k,
                    term=fields,
                    expected=(typ,)
                )
            return False
        val = fields[k]
        if not check.isterm(val, expected_type):
            if self.explode:
                from model.mods.err import ModelErr
                from typed.mods.prop import prop
                raise ModelErr(
                    message=f"Field has invalid type",
                    term=val,
                    field=k,
                    expected=(expected_type,),
                    received=prop.typeof(val)
                )
            return False

    return True
