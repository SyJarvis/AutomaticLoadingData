# AutomaticLoadingData

一个使用python编写的数据库工具脚本，可以基于excel表创建数据库、数据表、批量插入数据。



### 开发环境

* Pycharm
* Python3.9.13

```
pip install -r requirement.txt
```



### 配置文件

db_config下的配置文件格式 testdb.yaml

```yaml
mysql:
  host: localhost
  port: 3306
  username: root
  password: 123456
  db: testdb
  charset: utf8mb4

db:
  db_name: testdb
  table_file: table/test1.xlsx
  data_file: data/test1.xlsx
  tb_name_list: ["test1", "test2"]
  is_createdDB: true        # 创建数据库
  is_createdTable: true     # 创建数据表
  is_insertData: false      # 不插入数据

table:
  heads: ["字段名", "类型", "长度", "是否为空", "是否唯一", "是否为主键", "是否自增", "说明"]
  rule: ["{} ", "{}", "({}) ", {"1":"not null ", "0":""}, {"1":"unique ", "0":""}, {"1": "primary key ", "0":""}, {"1":"auto_increment ", "0":""}, "comment '{}'"]
```

注：数据库信息需要修改为本机的。



### 运行

```
python .\run.py --config ./db_config/testdb.yaml
```



