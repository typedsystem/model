
def model(__cls__=None, *, check: bool = None, lazy: bool = None):
    def decorator(cls):
        from model.mods.resolve import resolve
        from model.mods.types import CompType, LazyCompType

        lz = resolve.model.lazy(lazy)

        if lz:
            return LazyCompType(cls, check=check)
        return CompType(cls, check=check)

    if __cls__ is None:
        return decorator
    return decorator(__cls__)
