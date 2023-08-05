class Field(object):
    def __init__(self, name, column_type, convert, *, primary_key=False):
        self.name = name
        self.column_type = column_type
        self.convert = convert
        self.primary_key = primary_key

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

    @classmethod
    def default_value(self):
        raise NotImplementedError


class BaseStringField(Field):
    @classmethod
    def default_value(self):
        return ''


class VarcharField(BaseStringField):
    def __init__(self, name, length, *args, **kwargs):
        super().__init__(name, f'varchar({length})', str, *args, **kwargs)


class BaseIntField(Field):
    def default_value(self):
        return 0


class BigIntField(BaseIntField):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 'bigint', int, *args, **kwargs)


class TinyIntField(BaseIntField):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 'tinyint', int, *args, **kwargs)


class BaseFloatField(Field):
    def default_value(self):
        return .0


class FloatField(BaseFloatField):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 'float', float, *args, **kwargs)


class DoubleField(BaseFloatField):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 'double', float, *args, **kwargs)
