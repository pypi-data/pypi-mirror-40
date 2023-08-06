# pylint: disable=W0612
import inspect
from datetime import datetime


def props(obj):
    pro = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not inspect.ismethod(value):
            pro[name] = value
    return pro


def change_value_to_sqlvalue(value):
    numtype = int, float
    datetimetype = datetime
    if(isinstance(value, numtype)):
        return str(value)
    elif(isinstance(value, datetimetype)):
        return "'"+value.strftime('%Y-%m-%d %H:%M:%S')+"'"
    return "'"+value+"'"


def build_sql_insert(table, obj):
    dic = obj
    if not isinstance(obj, dict):
        dic = props(obj)
    keys = []
    values = []
    for key, value in dic.items():
        keys.append(key)
        values.append(change_value_to_sqlvalue(value))
    sql = "INSERT INTO "+table + \
        "("+",".join(keys)+") VALUES ("+",".join(values)+")"
    print(sql)
    return sql


def build_sql_select(frompart, wherepart, selectpart='*',offset = 0,limit = 0):
    wherepart.append("1=1")
    sql = "SELECT "+selectpart+" from " + \
        frompart + " where "+" AND ".join(wherepart) +" OFFSET "+offset
    if limit > 0:
        sql = sql + " LIMIT "+limit
    print(sql)
    return sql


def build_sql_select_with_class(frompart, wherepart, targrt_class,offset = 0,limit = 0):
    obj = targrt_class()
    dic = props(obj)
    keys = []
    for key, value in dic.items():
        keys.append(key)
    selectpart = ",".join(keys)
    return build_sql_select(frompart, wherepart, selectpart,offset,limit), keys


def build_object_with_fetchone(rowtitle, row, targrt_class):
    obj = targrt_class()
    for tmp in rowtitle:
        index = rowtitle.index(tmp)
        setattr(obj, rowtitle[index], row[index])
    return obj


def build_object_with_fetchall(rowtitle, rows, targrt_class):
    objs = []
    for item in rows:
        objs.append(build_object_with_fetchone(rowtitle, item, targrt_class))
    return objs
