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

        # conf = configparser.ConfigParser()
        # path = os.path.split(os.path.realpath(__file__))[0] + '/database.conf'
        # conf.read(path)
        # prop = {}
        # for key, value in conf.items('DB'):
        #     prop[key] = value
        # conn = connect_pool(**prop)
        #
        #
        # @conn.query
        # def test(wwww, test=1):
        #     print(wwww)
        #     print(test)
        #     return ("select count(%s) from tablebase", (1,))
        # return "select count(1) from tablebase"

# if __name__ == "__main__":
#     list = ['1', '2', '3']
#     for i in list:
#         print(i)
