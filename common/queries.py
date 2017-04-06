from . import SQLvalidate as va
from .pool import connect_pool
from .condition_handler import handler
from .sqls import *
import configparser, os
import sys


def initConfig():
    conf = configparser.ConfigParser()
    path = __getUperPath()
    confPath = path + '/database.conf'
    while not os.path.exists(confPath):
        if path == '/':
            raise Exception("未找到配置文件")
        path = __getUperPath(path)
        confPath = path + '/database.conf'
    conf.read(confPath)
    prop = {}
    for key, value in conf.items('DB'):
        prop[key] = value
    conn = connect_pool(**prop)
    return conn


def __getUperPath(path=None):
    if path:
        return os.path.dirname(path)
    else:
        return os.path.abspath(sys.path[0])


conn = initConfig()


class baseQuery(object):
    _tables = []
    _colunms = []
    _conditions = {}
    _updates = {}
    _colunmMap = {}
    _orderby = ''
    _groupby = ''


class select(baseQuery):
    def __init__(self, *colunms):
        self._colunms.extend(colunms)

    def from_(self, table):
        from_(self, table)
        return self

    def where(self, **conditions):
        where(self, **conditions)
        return self

    @conn.query
    def query(self):
        SQL = 'SELECT '
        conditions = []

        # select colunm
        if va.hasQueryColunm(self._colunms):
            for index, column in enumerate(self._colunms):
                if index != len(self._colunms) - 1:
                    SQL += column + ','
                else:
                    SQL += column + ' '
        else:
            SQL += '* '
        # select table
        if va.isStr(self._tables[0], "非法表名"):
            SQL += 'FROM ' + self._tables[0]
        # select condition
        if va.hasQueryCondition(self._conditions):
            SQL += ' WHERE '
            first = True
            for key, value in self._conditions.items():
                if not first:
                    SQL += ' AND '
                else:
                    first = False
                transRe = handler(key, value)
                SQL += transRe[0]
                conditions.extend(transRe[1])
        return (SQL, tuple(conditions))


class update(baseQuery):
    def __init__(self, table):
        self._tables.append(table)

    def set(self, **update):
        self._updates = dict(self._updates, **update)
        return self

    def where(self, **conditions):
        where(self, **conditions)
        return self

    @conn.execute
    def execute(self):
        SQL = 'UPDATE '
        conditions = []

        # select table
        if va.isStr(self._tables[0], "非法表名"):
            SQL += self._tables[0]
        # update set condition
        if va.validateUpdateCondition(self._updates, '更新条件非法'):
            SQL += ' SET '
            first = True
            for key, value in self._updates.items():
                if not first:
                    SQL += ' , '
                else:
                    first = False
                SQL += key + '=%s '
                conditions.append(value)

        # select condition
        if va.hasQueryCondition(self._conditions):
            SQL += ' WHERE '
            first = True
            for key, value in self._conditions.items():
                if not first:
                    SQL += ' AND '
                else:
                    first = False
                transRe = handler(key, value)
                SQL += transRe[0]
                conditions.extend(transRe[1])
        return (SQL, tuple(conditions))


class insert(baseQuery):
    def __init__(self, tableName, **colunmKeyMap):
        self._tables.append(tableName)
        self._colunmMap = dict(self._colunmMap, **colunmKeyMap)
        self._colunms = self.__colunms__()

    def __colunms__(self):
        re = []
        for key in self._colunmMap.keys():
            re.append(key)
        return re

    def __colunmsStr__(self):
        re = ''
        for index, key in enumerate(self._colunmMap.keys()):
            if index != 0:
                re += ','
            re += key
        return re

    def __check__(self, data):
        for key in self._colunms:
            if self._colunmMap[key] not in data:
                raise Exception('key:' + self._colunmMap[key] + "未定义")
        return True

    def __baseInsert__(self):
        SQL = 'INSERT INTO ' + self._tables[0] + '('
        for index, key in enumerate(self.__colunms__()):
            if index != 0:
                SQL += ','
            SQL += key
        return SQL + ") VALUES"

    def __insertSQL__(self):
        SQL = self.__baseInsert__()
        for index, colunm in enumerate(self._colunms):
            if index != 0:
                SQL += ','
            else:
                SQL += '('
            SQL += '%s'
        SQL += ')'
        return SQL

    def do(self, data):
        if isinstance(data, list):
            return self.__list__(data)
        else:
            return self.__singel__(data)

    @conn.execute
    def __singel__(self, data):
        conditions = []
        if self.__check__(data):
            for index, colunm in enumerate(self._colunms):
                conditions.append(data[self._colunmMap[colunm]])
        return (self.__insertSQL__(), tuple(conditions))

    @conn.execute_many
    def __list__(self, list):
        conditions = []
        for dataindex, data in enumerate(list):
            thisCondition = []
            if self.__check__(data):
                for index, colunm in enumerate(self._colunms):
                    thisCondition.append(data[self._colunmMap[colunm]])
            conditions.append(tuple(thisCondition))
        return (self.__insertSQL__(), conditions)


class delete(baseQuery):
    def __init__(self, table):
        self._tables.append(table)

    def where(self, **conditions):
        where(self, **conditions)
        return self

    @conn.execute
    def execute(self):
        SQL = 'DELETE FROM '
        conditions = []

        # select table
        if va.isStr(self._tables[0], "非法表名"):
            SQL += self._tables[0]
        # select condition
        if va.hasQueryCondition(self._conditions):
            SQL += ' WHERE '
            first = True
            for key, value in self._conditions.items():
                if not first:
                    SQL += ' AND '
                else:
                    first = False
                transRe = handler(key, value)
                SQL += transRe[0]
                conditions.extend(transRe[1])
        return (SQL, tuple(conditions))
