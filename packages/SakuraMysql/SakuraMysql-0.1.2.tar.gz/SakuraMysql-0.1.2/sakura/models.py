from .exception import SakuraException
from .meta import ModelMetaclass


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.modify = False

    def __getattr__(self, key):
        try:
            if key in self.__mappings__:
                return self.__mappings__[key].convert(self[key])  # .value()
            else:
                return self.__dict__[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        if key in self.__mappings__:
            self.modify = True
            self[key] = value
        else:
            self.__dict__[key]=value

    def Create(self):
        field_value = dict(self)
        id = self.connection.insert(self.__class__, field_value)
        self[self.__primary__] = id

    def Update(self):
        if not self.modify:
            return
        if self.__primary__ not in self:
            raise SakuraException('primary key is empty')
        cond = [[
            [self.__primary__, '=', self[self.__primary__]]
        ]]
        field_value = dict(self)
        field_value.pop(self.__primary__)
        return self.connection.update(self.__class__, field_value, cond)

    def Delete(self):
        if self.__primary__ not in self:
            raise SakuraException('primary key is empty')
        cond = [[
            [self.__primary__, '=', self[self.__primary__]]
        ]]
        return self.connection.delete(self.__class__, cond)

    def Get(self):
        cond = [[
            [k, '=', v] for k, v in self.items()
        ]]
        info = self.connection.select_one(self.__class__, cond)
        self.update(info)

    @classmethod
    def Fetch(cls, cond=None):
        return cls.connection.select(cls, cond)
