from .fields import Field
from .mysql import SakuraMysql


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return type.__new__(mcs, name, bases, attrs)
        mappings = dict()
        pk = []
        obj = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                if v.primary_key:
                    pk = k
                mappings[k] = v
            elif k == 'connection' and isinstance(v, SakuraMysql):
                obj = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__connection__'] = obj
        attrs['__primary__'] = pk
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = name.lower()  # 假设表名和类名一致
        return type.__new__(mcs, name, bases, attrs)
