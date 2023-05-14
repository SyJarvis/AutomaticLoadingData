# -*- coding: utf-8 -*-
# @FileName : run.py
# @Time     : 2023/5/13 21:27
# @Author   : Runke Zhong
import sys
from utils.op_yaml import get_yaml_data
from utils.AutomaticWarrior import AutoWarrior
import os
# python run.py --config ./db_config/chain_market.yaml
argvs = sys.argv
config_path = argvs[argvs.index('--config') + 1] if '--config' in argvs else False
print(config_path)


def main():
    if config_path:
        config = get_yaml_data(config_path)
        config['root_path'] = os.getcwd()
        autoManage = AutoWarrior(config)
        autoManage.run()
    else:
        raise Exception("not config file")


if __name__ == '__main__':
    main()