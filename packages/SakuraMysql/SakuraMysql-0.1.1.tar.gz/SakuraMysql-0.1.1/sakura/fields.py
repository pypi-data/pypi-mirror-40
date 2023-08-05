class Field(object):
    def __init__(self, column_type, convert, *, primary_key=False):
        self.column_type = column_type
        self.convert = convert
        self.primary_key = primary_key

    @classmethod
    def default_value(cls):
        raise NotImplementedError


class BaseStringField(Field):
    @classmethod
    def default_value(cls):
        return ''


class VarcharField(BaseStringField):
    def __init__(self, length, *args, **kwargs):
        super().__init__(f'varchar({length})', str, *args, **kwargs)


class BaseIntField(Field):
    @classmethod
    def default_value(cls):
        return 0


class BigIntField(BaseIntField):
    def __init__(self, *args, **kwargs):
        super().__init__('bigint', int, *args, **kwargs)


class TinyIntField(BaseIntField):
    def __init__(self, *args, **kwargs):
        super().__init__('tinyint', int, *args, **kwargs)


class BaseFloatField(Field):
    @classmethod
    def default_value(cls):
        return .0


class FloatField(BaseFloatField):
    def __init__(self, *args, **kwargs):
        super().__init__('float', float, *args, **kwargs)


class DoubleField(BaseFloatField):
    def __init__(self, *args, **kwargs):
        super().__init__('double', float, *args, **kwargs)
