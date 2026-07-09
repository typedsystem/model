def _single_field_inner_type_and_key(mcls):
    try:
        req_tuple = getattr(mcls, '_required_attributes_and_types', ())
        req = dict(req_tuple)
        opt = getattr(mcls, '_optional_attributes_and_defaults', {})
        if len(req) == 1 and len(opt) == 0:
            key, inner_type = next(iter(req.items()))
            return inner_type, key
    except Exception:
        pass
    return None, None

def _issubmodel(subclass, cls):
    if not isinstance(subclass, type):
        return False

    if cls in getattr(subclass, '__mro__', []):
        return True

    visited = set()
    stack = [subclass]

    while stack:
        cur = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)

        bases = getattr(cur, '__bases__', ())
        for base in bases:
            if base is cls:
                return True
            stack.append(base)

    meta_attrs = [
        '_required_attributes_and_types',
        '_required_attribute_keys',
        '_optional_attributes_and_defaults',
    ]
    if not all(hasattr(subclass, attr) for attr in meta_attrs):
        return False

    cls_req_attrs = getattr(cls, '_defined_required_attributes', {})
    sub_req_attrs = getattr(subclass, '_defined_required_attributes', {})
    cls_opt_attrs = getattr(cls, '_defined_optional_attributes', {})
    sub_opt_attrs = getattr(subclass, '_defined_optional_attributes', {})

    sub_all_keys = set(sub_req_attrs.keys()) | set(sub_opt_attrs.keys())

    if not set(cls_req_attrs.keys()).issubset(sub_all_keys):
        return False
    if not set(cls_opt_attrs.keys()).issubset(sub_all_keys):
        return False

    for name, p_type in cls_req_attrs.items():
        if name in sub_req_attrs:
            if not issubclass(sub_req_attrs[name], p_type):
                return False
        elif name in sub_opt_attrs:
            if not issubclass(sub_opt_attrs[name].type, p_type):
                return False

    for name, p_wrapper in cls_opt_attrs.items():
        p_type = p_wrapper.type
        if name in sub_req_attrs:
            if not issubclass(sub_req_attrs[name], p_type):
                return False
        elif name in sub_opt_attrs:
            s_wrapper = sub_opt_attrs[name]
            if not issubclass(s_wrapper.type, p_type):
                return False
            if not isinstance(s_wrapper.default_value, p_type):
                return False

    if not set(getattr(cls, '__conditions_list', [])).issubset(
        set(getattr(subclass, '__conditions_list', []))
    ):
        return False

    return True

