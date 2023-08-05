import unittest

from sakura.fields import BigIntField, VarcharField, DoubleField
from sakura.models import Model


class TestMysql(unittest.TestCase):

    def setUp(self):
        super().setUp()
        db = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'password',
            'db': 'arbhac'
        }
        from sakura.mysql import connect
        self.sakura = connect(**db)
        self.sakura.debug = True

        class Test(Model):
            id = BigIntField()
            f1 = BigIntField()
            f2 = VarcharField(50)
            f3 = DoubleField()

        self.test = Test

    def test_insert(self):
        sql = self.sakura.insert(self.test, {
            'id': 1,
            'f1': 2,
            'f2': 'qwe',
            'f3': 3.4
        })
        self.assertEqual(sql, f"INSERT INTO `{self.test.__table__}` (`id`, `f1`, `f2`, `f3`) VALUES (1, 2, 'qwe', 3.4)")

    def test_update(self):
        sql = self.sakura.update(self.test, {
            'id': 1,
            'f1': 2,
            'f2': 'qwe',
            'f3': 3.4
        }, [[['id', '=', 1]],[['id', '=', 2]]])
        self.assertEqual(sql, f"UPDATE `{self.test.__table__}` SET `id` = 1, `f1` = 2, `f2` = 'qwe', `f3` = 3.4 WHERE `id` = 1 OR `id` = 2")

    def test_delete(self):
        sql = self.sakura.delete(self.test, [[['id', '=', 1]], [['id', '=', 2]]])
        self.assertEqual(sql, f"DELETE FROM `{self.test.__table__}` WHERE `id` = 1 OR `id` = 2")

    def test_select(self):
        sql = self.sakura.select(self.test, [[['id', '=', 1]], [['id', '=', 2]]], ['f1', 'f2'], ['id'], 5, ['id', 'f1'])
        self.assertEqual(sql, f"SELECT `id`, `f1` FROM `{self.test.__table__}` WHERE `id` = 1 OR `id` = 2 GROUP BY `f1`, `f2` ORDER BY `id` LIMIT 5")
        sql = self.sakura.select(self.test, [[['id', '=', 1], ['id', '=', 2]], [['id', '=', 3]]], ['f1', 'f2'], ['id'], 5, ['id', 'f1'])
        self.assertEqual(sql, f"SELECT `id`, `f1` FROM `{self.test.__table__}` WHERE `id` = 1 AND `id` = 2 OR `id` = 3 GROUP BY `f1`, `f2` ORDER BY `id` LIMIT 5")


class TestSqlUtil(unittest.TestCase):
    def test_field_value(self):
        from sakura.util import SqlUtil
        _field_value = {
            'a': 1,
            'b': 2,
            'c': 'c'
        }
        field_value, args = SqlUtil.get_field_value(_field_value)
        self.assertEqual(field_value, '`a` = %s, `b` = %s, `c` = %s')
        self.assertEqual(args, [1, 2, 'c'])


if __name__ == '__main__':
    unittest.main()
