import pymysql

from .util import SqlUtil
from .exception import SakuraException
from .log import logger

class SakuraMysql:
    def __init__(self, *args, **kwargs) -> None:
        self.conn =  pymysql.connect(*args, **kwargs)
        self.debug = False

    def _sql(self, query, args):
        """获取sql语句"""
        cur = self.conn.cursor()
        return cur.mogrify(query, args)

    def insert(self, model, field_value):
        fields, _args = list(field_value.keys()), list(field_value.values())
        _fields = SqlUtil.get_fields(fields)

        _sql = SqlUtil.format_sql(
            [
                'INSERT INTO',
                f'`{model.__table__}`',
                f'({_fields})',
                f'VALUES ({", ".join(["%s"]*len(_args))})'
            ]
        )
        if self.debug:
            print('insert')
            return self._sql(_sql, _args)
        try:
            cur = self.execute(_sql, _args,True)
            if cur:
                return cur.lastrowid
            else:
                return False
        except Exception as e:
            raise SakuraException(e)

    def update(self, model, field_value, cond=None):
        _field_value, _args1 = SqlUtil.get_field_value(field_value)
        _where, _args2 = SqlUtil.get_where(cond)
        _args = _args1 + _args2
        _sql = SqlUtil.format_sql(
            [
                'UPDATE',
                f'`{model.__table__}`',
                'SET',
                _field_value,
                _where]
        )
        if self.debug:
            print('update')
            return self._sql(_sql, _args)
        try:
            if self.execute(_sql, _args,True):
                return True
            else:
                return False
        except Exception as e:
            raise SakuraException(e)

    def delete(self, model, cond=None):
        _where, _args = SqlUtil.get_where(cond)
        _sql = SqlUtil.format_sql(
            [
                'DELETE FROM',
                f'`{model.__table__}`',
                _where,
            ]
        )
        if self.debug:
            print('delete')
            return self._sql(_sql, _args)
        try:
            cur = self.execute(_sql, _args,True)
            if cur:
                return True
            else:
                return False
        except Exception as e:
            raise SakuraException(e)

    def select(self, model, cond=None, group_by=None, order_by=None, limit=100, fields=None):
        _fields = SqlUtil.get_fields(fields)
        if not fields:
            fields = model.__mappings__
        _where, _args = SqlUtil.get_where(cond)
        _group_by = SqlUtil.get_groupby(group_by)
        _order_by = SqlUtil.get_orderby(order_by)
        _limit = SqlUtil.get_limit(limit)
        _sql = SqlUtil.format_sql(
            [
                'SELECT',
                _fields,
                'FROM',
                f'`{model.__table__}`',
                _where,
                _group_by,
                _order_by,
                _limit
            ]
        )
        if self.debug:
            print('select')

            return self._sql(_sql, _args)
        try:
            l = self.execute(_sql, _args)
            models = []
            for i in l:
                models.append(model(**dict(zip(fields, i))))
            return models
        except Exception as e:
            raise SakuraException(e)

    def select_one(self, model, cond=None, group_by=None, order_by=None, fields=None):
        if self.debug:
            print('select_one')
        models = self.select(model, cond, group_by, order_by, 1, fields)
        if models:
            return models[0]
        return {}

    def execute(self, query, args=None,commit=False):
        if self.debug:
            print('execute')
            return self._sql(query, args)
        try:
            cur = self.conn.cursor()
            cur.execute(query, args)
            logger.debug('sql:%s',self._sql(query, args))
            if commit:
                self.conn.commit()
                return cur
            return cur.fetchall()
        except Exception as e:
            raise SakuraException(e)

    def execute_many(self, query, args=None):
        if self.debug:
            print('execute_many')
            return self._sql(query, args)
        try:
            cur = self.conn.cursor()
            cur.executemany(query, args)
            logger.debug('sql:%s',self._sql(query, args))
            self.conn.commit()
            return cur.fetchall()
        except Exception as e:
            raise SakuraException(e)


def connect(*args, **kwargs):
    return SakuraMysql(*args, **kwargs)
