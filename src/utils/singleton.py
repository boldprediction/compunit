class MetaSingleton(type):

    def __init__(cls, *args, **kwargs):
        cls.__singleton__ = cls.Singleton()

    def __call__(cls, *args, **kwargs):
        raise RuntimeError("This class should not be instantiated!")

    def __getattr__(cls, key):
        return getattr(cls.__singleton__, key)