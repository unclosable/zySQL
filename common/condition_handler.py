def handler(key, value):
    if value is None:
        return __nullHandler(value)
    elif isinstance(value, str):  # 字符
        return __baseHandler(key, value)
    elif isinstance(value, int):  # 数字
        return __baseHandler(key, value)
    elif isinstance(value, list):  # list
        return __arrayHandler(key, value)
    elif isinstance(value, tuple):
        if value[0]:
            return handler(key, value[1])
        else:
            return __handler_anti(key, value[1])

    else:
        raise Exception('解析不能')


def __handler_anti(key, value):
    if value is None:
        return __nullHandler_anti(value)
    elif isinstance(value, str):  # 字符
        return __baseHandler_anti(key, value)
    elif isinstance(value, int):  # 数字
        return __baseHandler_anti(key, value)
    elif isinstance(value, list):  # list
        return __arrayHandler_anti(key, value)
    else:
        raise Exception('解析不能')


def __baseHandler(key, value):
    sql = key + " = %s "
    return (sql, (value,))


def __baseHandler_anti(key, value):
    sql = key + " != %s "
    return (sql, (value,))


def __nullHandler(key):
    sql = key + " IS NULL "
    return (sql, ())


def __nullHandler_anti(key):
    sql = key + " IS NOT NULL "
    return (sql, ())


def __arrayHandler(key, array):
    reList = []
    sql = key + " IN("
    for index, iterm in enumerate(array):
        if index != len(array) - 1:
            sql += '%s,'
        else:
            sql += '%s'
        reList.append(iterm)
    sql += ") "
    return (sql, tuple(reList))


def __arrayHandler_anti(key, array):
    reList = []
    sql = key + " NOT IN("
    for index, iterm in enumerate(array):
        if index != len(array) - 1:
            sql += '%s,'
        else:
            sql += '%s'
        reList.append(iterm)
    sql += ") "
    return (sql, tuple(reList))
