from . import SQLvalidate as va
from .pool import connect_pool
import configparser, os

__conn = None


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
    # print(confPath)
    return conn


def __getUperPath(path=None):
    if path:
        return os.path.dirname(path)
    else:
        return os.path.dirname(os.path.abspath(__file__))


conn = initConfig()


class select(object):
    @conn.query
    def query(self, tableName, *queryColumn, **queryConditions):
        SQL = 'SELECT '
        conditions = []

        # select colunm
        if va.hasQueryColunm(queryColumn):
            for index, column in enumerate(queryColumn):
                if index != len(queryColumn) - 1:
                    SQL += column + ','
                else:
                    SQL += column + ' '
        else:
            SQL += '* '
        # select table
        if va.isStr(tableName, "非法表名"):
            SQL += 'FROM ' + tableName
        # select condition
        if va.hasQueryCondition(queryConditions):
            SQL += ' WHERE '
            first = True
            for key, value in queryConditions.items():
                if not first:
                    SQL += 'AND '
                else:
                    first = False
                SQL += key + ' =%s '
                conditions.append(value)
        return (SQL, tuple(conditions))
