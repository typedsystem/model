from typed.err import TypeErr

class ModelErr(TypeErr):
    pass

class KeyErr(ModelErr):
    def __init__(self, message=None, key=None, keys=None, **kwargs):
        self.key = key
        self.keys = keys
        super().__init__(message=message, **kwargs)
