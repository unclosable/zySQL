

class lalala(object):
    def __init__(self):
        print("init")
        # print(func(2))

    def __exclud_sql(self, sql):
        print("执行了SQL:" + sql)
        return "结果集"

    def act(self, func):
        print(2)

        def wrapper(sql, excul=self.__exclud_sql, func=func):
            print('得到CONNECTION')
            sql = func(sql)
            print(sql)
            re = excul(sql)
            print('释放CONNECTION')
            return re

        return wrapper


def f1(a, aaa):
    print(1)
    print(aaa)
    re = a(aaa)
    print(re)
    return 4


lalala = lalala()


# @test.act
# def f2(s):
#     print(s)
#     return 3

@lalala.act
def do_sql(sql):
    print(1)
    return sql


re = do_sql("the sql")
print(re)
