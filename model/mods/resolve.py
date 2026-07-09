from typed.resolve import resolve as typed_resolve, resolved, resolver

class resolve(typed_resolve):
    class model:
        @resolver
        def check(__check__=None, conf=None):
            from typed.mods.err import NotDefined
            if __check__ is not None and __check__ is not NotDefined:
                return __check__

            if conf is None:
                try:
                    from model.mods.init import conf
                except ImportError:
                    pass

            default_val = getattr(conf.model, 'check', True) if conf and hasattr(conf, 'model') else True
            return resolved(provided=__check__, default=default_val)
