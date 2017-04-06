import mysql.connector.pooling as pool


# import configparser, os


class connect_pool(object):
    __need_prop = {  # 链接需要的属性
        "user": None,
        "password": None,
        "host": None,
        "port": 3306,
        "database": None,
        "charset": "utf8"
    }

    def __check__(self):
        for key in self.__need_prop:
            if not self.__need_prop[key]:
                return key
        return False

    def __init_pool__(self, pool_size, pool_reset_session):
        self.__pool = pool.MySQLConnectionPool(pool_size=pool_size,
                                               pool_reset_session=pool_reset_session,
                                               **self.__need_prop)

    def __init__(self, pool_size=10, pool_reset_session=True, **agr):
        for key in self.__need_prop:
            if key in agr:
                self.__need_prop[key] = agr[key]
        if self.__check__():
            raise Exception('缺少参数:' + self.__check__())
        else:
            self.__init_pool__(pool_size, pool_reset_session)

    def __get_conn(self):
        return self.__pool.get_connection()

    def test(self):
        conn = self.__pool.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(1) FROM tablebase')
        re = cur.fetchall()
        print(re)
        cur.close()
        conn.close()

    def query(self, func):
        def wrapperFunc(*prop, **map):
            conn = self.__pool.get_connection()
            cur = conn.cursor()
            queryEnrty = func(*prop, **map)
            if type(queryEnrty) is str:
                cur.execute(queryEnrty)
            else:
                cur.execute(*queryEnrty)
            re = cur.fetchall()
            # print(re)
            cur.close()
            conn.close()
            return re

        return wrapperFunc

    def execute(self, func):
        def wrapperFunc(*prop, **map):
            conn = self.__pool.get_connection()
            cur = conn.cursor()
            queryEnrty = func(*prop, **map)
            if type(queryEnrty) is str:
                cur.execute(queryEnrty)
            else:
                cur.execute(*queryEnrty)
            conn.commit()
            cur.close()
            conn.close()

        return wrapperFunc

    def execute_many(self, func):
        def wrapperFunc(*prop, **map):
            conn = self.__pool.get_connection()
            cur = conn.cursor()
            queryEnrty = func(*prop, **map)
            cur.executemany(*queryEnrty)
            conn.commit()
            cur.close()
            conn.close()

        return wrapperFunc
