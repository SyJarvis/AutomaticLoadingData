# -*- coding: utf-8 -*-
# @FileName : DBUtils.py
# @Time     : 2023/5/12 19:03
# @Author   : Runke Zhong
import pymysql

from utils.ExcelUtils import ExcelUtils
from utils.op_yaml import get_yaml_data

class DBUtils(object):

    conn = None
    DB = None
    MYSQL_CONFIG = None
    TABLE_CONFIG = None
    DB_CONFIG = None
    DATABASE_EXISTS = None

    def __init__(self, config):
        self.MYSQL_CONFIG = config['mysql']
        self.TABLE_CONFIG = config['table']
        self.DB_CONFIG = config['db']

    def create_connect(self):
        mysql_config = self.MYSQL_CONFIG
        self.conn = pymysql.connect(host=mysql_config['host'],
                                    port=mysql_config['port'],
                                    user=mysql_config['username'],
                                    password=mysql_config['password'],
                                    charset=mysql_config['charset'])
        if self.check_db_exists(mysql_config['db']):
            self.select_db(mysql_config['db'])
            self.DATABASE_EXISTS = True
        else:
            self.DATABASE_EXISTS = False

    def check_db_exists(self, db_name=None):
        if db_name is None:
            db_name = self.DB_CONFIG['db']
        if self.conn is None:
            raise Exception("please create connect")
        cursor = self.conn.cursor()
        sql = "show databases"
        try:
            result = cursor.execute(sql)  # 返回值数字
            databases_tuple = cursor.fetchall()
            for i in range(0, len(databases_tuple)):
                if db_name == databases_tuple[i][0]:
                    self.DATABASE_EXISTS = True
                    return True
        except Exception as e:
            print(e)  # 打印数据库已经存在的信息
        finally:
            cursor.close()
        return False

    def select_db(self, db_name):
        try:
            self.conn.select_db(db_name)
        except Exception as e:
            raise Exception(e)

    def get_data(self,tb_name=None, filed_list=None):
        if not self.DATABASE_EXISTS:
            raise Exception("please create database")
        if self.conn is None:
            raise Exception("please create connect")
        cursor = self.conn.cursor()
        if filed_list is None:
            sql = "select * from {}".format(tb_name)
        else:
            sql = "select "
            for filed in filed_list:
                sql = sql + filed + ","
            sql = sql + " from {}".format(tb_name)
        cursor.execute(sql)
        print(cursor.fetchall())
        cursor.close()

    def create_table(self, tb_name, datas_list=None, table_config=None, charset=None):
        if not self.DATABASE_EXISTS:
            raise Exception("please create database")
        if self.conn is None:
            raise Exception("please create connect")
        if table_config is None:
            table_config = self.TABLE_CONFIG
        if len(datas_list[0]) != len(table_config['heads']):
            raise Exception("length is error")

        cursor = self.conn.cursor()
        sql = "create table if not exists `" + tb_name + "` ("
        filed_list = table_config['heads']
        for n, row_data in enumerate(datas_list):
            # 这里有这个是为了跳过表头
            # if n == 0:
            #     continue
            print("filed_list:", filed_list)
            print("row_data", row_data)
            l = self._fix_data(filed_list, table_config, row_data)
            sql = sql + l
            if n != len(datas_list) - 1:
                sql = sql + ","
        sql = sql + ")"
        print(sql)
        try:
            result = cursor.execute(sql)  # 返回值数字
            result2 = self.conn.commit()  # 返回值None
        except Exception as e:
            print(e)  # 打印数据库已经存在的信息
        finally:
            cursor.close()

    def insert_data(self, tb_name=None, filed_list=None, data_list=None):
        if not self.DATABASE_EXISTS:
            raise Exception("please create database")
        if self.conn is None:
            raise Exception("please create connect")
        cursor = self.conn.cursor()
        sql = "insert into {}".format(tb_name)
        if filed_list is None:
            sql = sql + " values"
        else:
            if (len(filed_list) != len(data_list)):
                raise Exception("filed_list length and data_list length not equal")
            sql = sql + "("
            for filed in filed_list:
                sql = sql + filed + ","
            sql = sql + ") values"

        if data_list is None:
            raise Exception("insert error")
        else:
            sql = sql + "("
            for i, data in enumerate(data_list):
                if type(data) == int:
                    flag = "," if i + 1 != len(data_list) else ""
                    sql = sql + str(data) + flag
                elif type(data) == str:
                    flag = "," if i + 1 != len(data_list) else ""
                    sql = sql + "\'" + data + "\'" + flag
                else:
                    print("error")
            sql = sql + ")"
        # sql.encode("latin-1", errors="ignore").decode("gbk", errors="ignore")
        print(sql)
        cursor.execute(sql)
        # print(cursor.fetchall())
        result = self.conn.commit()
        print(result)
        cursor.close()

    def create_database(self, db_name, charset=None):
        if self.DATABASE_EXISTS:
            raise Exception("database is create")
        if self.conn is None:
            raise Exception("please create connect")
        cursor = self.conn.cursor()
        sql = "create database if not exists " + db_name
        if charset is not None:
            try:
                if str(charset).lower() in ['utf-8', 'utf8mb4']:
                    sql = sql + " charset=" + charset
            except Exception as e:
                print(e)
        try:
            result = cursor.execute(sql)  # 返回值数字
            result2 = self.conn.commit()  # 返回值None
            self.DATABASE_EXISTS = True
        except Exception as e:
            self.DATABASE_EXISTS = False
            print(e)  # 打印数据库已经存在的信息
        finally:
            cursor.close()

    def _fix_data(self, filed_list, table_config, row_data):
        if table_config is None:
            table_config = self.TABLE_CONFIG
        if len(row_data) != len(filed_list):
            raise Exception("length is error")
        if len(filed_list) != len(table_config['heads']):
            raise Exception("length is error")
        i = 0
        sql = ""
        flag = False
        for filed, data in zip(filed_list, row_data):
            if filed in table_config['heads'][i]:
                if type(table_config['rule'][i]) == dict:
                    data = str(data) if (type(data) == int) else data
                    sql = sql + table_config['rule'][i][data]
                elif (data == 0):
                    sql = sql + " "
                elif (filed == "decimal"):
                    flag = True
                    sql = sql + str(table_config['rule'][i]).format(data)
                elif flag:
                    data = str(data)
                    d_l = data.split()
                    sql = sql + "({},{})".format(d_l[0], d_l[1])
                    flag = False
                else:
                    sql = sql + str(table_config['rule'][i]).format(data)
            i += 1
        return sql

if __name__ == '__main__':
    excel_obj = ExcelUtils()
    excel_obj.open_workbook("D:\\coding\\PythonProjects\\auto_insert_data\\table\\test1.xlsx")
    print(excel_obj.get_all_sheet_data())
    print(excel_obj.get_sheet_data_by_name('test2'))
    datas_list = excel_obj.get_sheet_data_by_name('test2')
    config = get_yaml_data("../db_config/testdb.yaml")
    db_obj = DBUtils(config)
    db_obj.create_connect()
    print(db_obj.check_db_exists("test1"))
    # db_obj.create_database("testdb")
    print(datas_list)
    db_obj.create_table("test2", datas_list)