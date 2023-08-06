import importlib

__version__ = '0.1.0'

def dynamic_import(module):
    return importlib.import_module(module)

class OKEx3(object):
    """docstring for OKEx3"""
    config = {}

    def __init__(self, *args, **kwargs):
        self.config = kwargs

    def __getattr__(self, name): 
        if name not in self.__dict__: 
            self.__dict__[name] = self.create(name)
        return self.__dict__[name]

    def create(self, name='account'):
        module = dynamic_import("okex3.api.{}".format(name.lower()))
        method = getattr(module, "{}API".format(name.lower().capitalize()))
        return method(**self.config)