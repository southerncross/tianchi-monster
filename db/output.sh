#!/bin/bash

# 使用方法
# 1. 修改ROOT_PATH为导出的csv文件的路径
# 2. 修改csv_name为导出的csv文件名
# 3. 修改sql为自定义的查询语句

ROOT_PATH=/Users/lishunyang/workspace/tianchi-monster/db
csv_name=feature1.csv
sql="SELECT * FROM train_user limit 10"

psql -d tianchi -c "COPY ($sql) to '$ROOT_PATH/$csv_name' with delimiter ',';"
