# -*- coding: utf-8 -*-
# @FileName : op_yaml.py
# @Time     : 2023/5/10 19:52
# @Author   : Runke Zhong
import yaml


def getConfig(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result


def get_yaml_data(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result


if __name__ == '__main__':
    getConfig()