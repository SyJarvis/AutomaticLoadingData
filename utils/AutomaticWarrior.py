# -*- coding: utf-8 -*-
# @FileName : AutomaticWarrior.py
# @Time     : 2023/5/14 13:30
# @Author   : Runke Zhong
from utils.DBUtils import DBUtils
from utils.ExcelUtils import ExcelUtils
import os


class AutoWarrior(object):
    """
    自动战士
    """
    config = None
    mysql_config= None
    db_config = None
    table_config = None
    db_obj = None
    excel_obj = None
    is_tb_all = False
    IS_createdDB = False
    IS_CreatedTable = False
    IS_InsertData = False
    ROOT_PATH = None

    def __init__(self, config):
        self.config = config
        self.db_config = config['db']
        self.table_config = config['table']
        self.db_obj = DBUtils(config)
        self.excel_obj = ExcelUtils()
        self.ROOT_PATH = config['root_path']

        # 检查配置文件
        print("检查配置文件")
        # 是否创建数据库
        if self.db_config['is_createdDB']:
            self.IS_createdDB = True
        else:
            self.IS_createdDB = False
        # 是否创建表
        if self.db_config['is_createdTable']:
            self.IS_CreatedTable = True
            if self.excel_obj.check_workbook(os.path.join(self.ROOT_PATH, self.db_config['table_file'])):
                print("{} is exists".format(self.db_config['table_file']))
            else:
                raise Exception("{} is not exists.".format(self.db_config['table_file']))
        else:
            self.IS_CreatedTable = False
        # 是否插入数据
        if self.db_config['is_insertData']:
            self.IS_InsertData = True
            self.excel_obj.check_workbook(os.path.join(self.ROOT_PATH, self.db_config['data_file']))
        else:
            self.IS_InsertData = False
        # 判断heades和rule的长度是否一致
        if len(self.table_config['heads']) != len(self.table_config['rule']):
            raise Exception("heads length and rule length must be equal")
        # 判断是否所有表
        if self.db_config['tb_name_list'] == '*':
            self.is_tb_all = True
        else:
            self.is_tb_all = False

    def run(self):
        # 判断是否需要创建数据库
        self.db_obj.create_connect()
        if self.IS_createdDB:
            self.db_obj.create_database(self.db_config['db_name'])
            self.IS_createdDB = False
            self.db_obj.select_db(self.db_config['db_name'])
        # 判断是否需要创建数据表
        if self.IS_CreatedTable:
            self.excel_obj.open_workbook(os.path.join(self.ROOT_PATH, self.db_config['table_file']))
            if self.is_tb_all:
                sheet_datas_list = self.excel_obj.get_all_sheet_data()
                sheet_names = self.excel_obj.get_sheet_names()
                if len(sheet_datas_list) != len(sheet_names):
                    raise Exception("sheet data error")
                for tb_name,datas_list in zip(sheet_names, sheet_datas_list):
                    self.db_obj.create_table(tb_name, datas_list)
            else:
                for tb_name in self.db_config['tb_name_list']:
                    datas_list = self.excel_obj.get_sheet_data_by_name(tb_name)
                    self.db_obj.create_table(tb_name, datas_list)
            self.IS_CreatedTable = False
            self.excel_obj.close()
        # 判断是否需要插入数据
        if self.IS_InsertData:
            self.excel_obj.open_workbook(os.path.join(self.ROOT_PATH, self.db_config['data_file']))
            self.db_obj.select_db(self.db_config['db_name'])
            if self.is_tb_all:
                sheet_datas_list = self.excel_obj.get_all_sheet_data()
                print("===============sheet_datas_list===================")
                filed_list = sheet_datas_list[0]
                sheet_datas_list = sheet_datas_list[1:]
                print(sheet_datas_list)
                # for tb_name, data_list in zip(self.excel_obj.get_sheet_names(), sheet_datas_list):
                #     self.db_obj.insert_data(tb_name, filed_list=None, data_list=data_list)
            else:
                try:
                    for tb_name in self.db_config['tb_name_list']:
                        datas_list = self.excel_obj.get_sheet_data_by_name(tb_name)
                        print(datas_list)
                        filed_list = datas_list[0]
                        for i in range(1, len(datas_list)):
                            self.db_obj.insert_data(tb_name, filed_list=None, data_list=datas_list[i])
                except Exception as e:
                    print(e)
                finally:
                    print("插入成功")


    def export_data(self):
        pass