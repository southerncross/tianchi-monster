#!/bin/bash

# 效果
# 1. 删除CSV文件首行
# 2. 在user表的最后补全时间00:00
# 3. 在原始CSV文件目录下生成新的两个CSV文件

# 使用说明
# 把ROOT_PATH修改为原始CSV文件所在目录
# 其他变量不要改动
# 不要多次执行这个脚本，因为每次都会删掉首行！

ROOT_PATH=/Users/dengshihong/workspace/tianchi-monster/db
csv_user=$ROOT_PATH/tianchi_mobile_recommend_train_user.csv
csv_user_new=$ROOT_PATH/train_user.csv
csv_item=$ROOT_PATH/tianchi_mobile_recommend_train_item.csv
csv_item_new=$ROOT_PATH/train_item.csv

tail +2 $csv_user | sed 's/$/&:00:00/' > $csv_user_new
tail +2 $csv_item > $csv_item_new
