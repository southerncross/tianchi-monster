#!/bin/bash

# 使用说明
# 不能使用原始的CSV文件灌数据，必须用trans_csv.sh脚本格式化后的文件
# 把ROOT_PATH修改为格式化后的CSV数据文件所在目录
# 不要改table_item和table_user

ROOT_PATH=/Users/lishunyang/workspace/tianchi-monster/db

table_item=train_item
csv_item=$ROOT_PATH/${table_item}.csv
table_user=train_user
csv_user=$ROOT_PATH/${table_user}.csv

psql -d tianchi -f init_tables.sql
#psql -d tianchi -c "COPY $table_item from '$csv_item' with delimiter ',';"
#psql -d tianchi -c "COPY $table_user from '$csv_user' with delimiter ',';"
