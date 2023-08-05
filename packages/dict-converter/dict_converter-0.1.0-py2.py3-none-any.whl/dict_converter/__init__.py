from collections.abc import Callable


class DictConverter:
    def __init__(self, obj: dict):
        self.obj = obj.copy()
        self.converters: list = []

    def add(self, key, func: Callable):
        self.converters.append((key, func))
        return self

    def result(self):
        for key, func in self.converters:
            if isinstance(key, list):
                for sub_key in key:
                    self.convert_once(sub_key, func)
            else:
                self.convert_once(key, func)
        return self.obj

    def convert_once(self, key, func: Callable):
        self.obj[key] = func(self.obj[key])
