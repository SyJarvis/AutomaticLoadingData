# -*- coding: utf-8 -*-
# @FileName : ExcelUtils.py
# @Time     : 2023/5/13 21:23
# @Author   : Runke Zhong
import xlrd

class ExcelUtils(object):

    table = None
    sheet = None
    table_number = None
    nrows = None
    ncols = None
    sheet_names = []

    def __init__(self):
        pass

    def open_workbook(self, file_name):
        """打开一个excel表"""
        try:
            self.table = xlrd.open_workbook(file_name, 'rb')
        except Exception as e:
            print(e)
        self.sheet = self.table.sheets()[0]
        self.sheet_names = self.table.sheet_names()
        self.table_number = len(self.table.sheet_names())
        self.nrows = self.sheet.nrows
        self.ncols = self.sheet.ncols

    def check_workbook(self, file_name):
        """打开一个excel表"""
        try:
            self.table = xlrd.open_workbook(file_name, 'rb')
        except Exception as e:
            print(e)
            return False
        self.sheet = self.table.sheets()[0]
        self.sheet_names = self.table.sheet_names()
        self.table_number = len(self.table.sheet_names())
        self.nrows = self.sheet.nrows
        self.ncols = self.sheet.ncols
        self.close()
        return True

    def select_sheet(self, sheet_name):
        """选择某个sheet, 默认选择sheet1"""
        self.sheet = self.table.sheet_by_name(sheet_name)
        self.nrows = self.sheet.nrows
        self.ncols = self.sheet.ncols

    def get_all_sheet_data(self, IgnoreFirstLine=True):
        """获取所有sheet的data"""
        sheet_names = self.table.sheet_names()
        sheet_datas_list = []
        for sheet_name in sheet_names:
            sheet = self.table.sheet_by_name(sheet_name)
            nrows = sheet.nrows
            n = 1 if IgnoreFirstLine else 0
            sheet_datas_list.append(self._get_sheet_data(sheet, n, nrows))
        return sheet_datas_list

    def get_sheet_data_by_name(self, sheet_name, IgnoreFirstLine=True):
        """获取指定sheet_name的data"""
        sheet = self.table.sheet_by_name(sheet_name)
        nrows = sheet.nrows
        n = 1 if IgnoreFirstLine else 0
        return self._get_sheet_data(sheet, n, nrows)

    def get_sheet_names(self):
        """获取所有的sheets名字"""
        return self.sheet_names

    def get_current_sheet_info(self):
        """获取当前sheet的名字"""
        info = {}
        info['name'] = self.sheet.name
        info['nrows'] = self.nrows
        info['ncols'] = self.ncols
        return info

    def get_current_sheet_data(self, IgnoreFirstLine=True):
        """获取当前sheet的data"""
        n = 1 if IgnoreFirstLine else 0
        return self._get_sheet_data(self.sheet, n, self.nrows)

    def _get_sheet_data(self, sheet, n, nrows):
        datas_list = []
        for i in range(n, nrows):
            datas = []
            for data in sheet.row_values(i):
                if type(data) == int or type(data) == float:
                    data = int(data)
                datas.append(data)
            datas_list.append(datas)
        return datas_list

    def close(self):
        self.table.release_resources()

if __name__ == '__main__':
    excel_obj = ExcelUtils()
    excel_obj.open_workbook("D:\\coding\\PythonProjects\\auto_insert_data\\table\\test1.xlsx")
    print(excel_obj.get_all_sheet_data())
    print(excel_obj.get_sheet_data_by_name('test2'))