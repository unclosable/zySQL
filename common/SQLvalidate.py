def hasQueryColunm(colunms):
    if colunms is None or len(colunms) == 0:
        return False
    for colunm in colunms:
        if not isinstance(colunm, str):
            raise Exception("非法的查询结果集")
    return True


def hasQueryCondition(conditions):
    if conditions is None:
        return False
    if not isinstance(conditions, dict):
        raise Exception("非法的查询条件")
    return True


def isStr(theStr, ex):
    if not isinstance(theStr, str):
        raise Exception(ex)
    return True
