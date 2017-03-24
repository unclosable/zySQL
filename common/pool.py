import mysql.connector.pooling as pool


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

    def get_conn(self):
        return self.__pool.get_connection()
