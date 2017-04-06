# zySQL

一个基于mysql-connector的简单封装（也许需要自己安装）

## example 实例

    import zySQL

    # insert single
    zySQL.queries.insert('newtest',id='id',f1='f1',f2='f2').do({'id':1,'f1':'str column','f2':'str column'})

    # insert list
    zySQL.queries.insert('newtest',id='id',f1='f1',f2='f2').do([{'id':1,'f1':'str column1','f2':'str column2'},
    {'id':2,'f1':'str column1','f2':'str column2'}])

    # select
    re = zySQL.queries.select('id', 'f1', 'f2').from_('testtable').where(f1='search condition').query()
    print(re)

    # update
    common.update('testtable').set(f1='up date test hh').where(id=1).execute()

    # delete
    common.delete('testtable').where(id=1).execute()

## usage 使用
在main方法同级或者上级目录中创建database.conf:

    [DB]
    host = 127.0.0.1
    port = 3306
    database = test_base
    user = root
    password = root
若一直找不到会一直找到‘／’为止并抛出异常
在import的时候会自动读取‘DB’下的配置信息

## other 另
当然有很多不易用啦，看心情吧……自己用的，看心情改吧

计划中的改进
* 省略列映射的insert方法
* 更灵活的数据库链接配置加载方式
* pip安装
* 异常处理
