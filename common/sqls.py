class where(object):
    def writeCreateConditions(self, **conditions):
        self.__creater._conditions = dict(self.__creater._conditions, **conditions)

    def __init__(self, creater, **conditions):
        self.__creater = creater
        self.writeCreateConditions(**conditions)


class from_(object):
    def writeCreateTables(self, *tables):
        self.__creater._tables.extend(tables)

    def __init__(self, creater, *tables):
        self.__creater = creater
        self.writeCreateTables(*tables)
