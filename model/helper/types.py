from threading import local

__state__ = local()

class STATE:
    def env():
        env = getattr(__state__, "env", None)
        if env is None:
            env = {}
            __state__.env = env
        return env

    def stack():
        stack = getattr(__state__, "stack", None)
        if stack is None:
            stack = []
            __state__.stack = stack
        return stack

    def data():
        stack = getattr(__state__, "stack", None)
        if not stack:
            return None, None
        model_cls = stack[-1]
        env = STATE.env()
        return model_cls, env.get(model_cls)

def _operation(op, left, right, callback):
    def fn():
        left = left() if callable(left) else left
        right = right() if callable(right) else right
        return op(left, right)
    return callback(fn)

def _eval(func, *args):
    def fn():
        resolved_args = [arg() if callable(arg) else arg for arg in args]
        value = func(*resolved_args)
        if callable(value):
            def wrapper(*args, **kwargs):
                return value(*args, **kwargs)
            return wrapper
        return value
    return fn()

def _resolve_path(self, entity):
    parts = self._attr.split(".")
    cur = entity
    for part in parts:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            cur = getattr(cur, part, None)
    return cur

def _resolve(self):
    model_cls, entity = STATE.data()
    if entity is None:
        return None
    return self._resolve_path(entity)
