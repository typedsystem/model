from model.mods.meta import MODEL

class Model(metaclass=MODEL):
    """
    The constructor type of models (typed dicts).

    : kindof(Model)    is  type
    : typeof(Model)    is  MODEL
    : isterm(x, Model) iff isinstance(x, dict) and matches field specs
    : nullof(Model)    is  {}
    : builtin(Model)   is  dict
    : flags(Model)     is  is_constructor
    """
    __flags__   = Flags(is_constructor=True)
    __null__    = {}
    __builtin__ = dict

    def __size__(trm):
        return len(trm)

    def __getitem__(trm, key):
        return trm.__dict__[key]

    def __setitem__(trm, key, value):
        from typed.mods.typesystem import typeof
        from typed.mods.check import check

        fields = getattr(typeof(trm), '__fields__', {})

        if key in fields:
            check.isterm(value, fields[key])

        trm.__dict__[key] = value

    def __contains__(trm, key):
        return key in trm.__dict__


