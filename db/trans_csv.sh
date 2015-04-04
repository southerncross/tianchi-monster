#!/bin/bash

ROOT_PATH=/Users/lishunyang/workspace/tianchi-monster/db
csv_user=$ROOT_PATH/tianchi_mobile_recommend_train_user.csv
csv_user_new=$ROOT_PATH/train_user.csv
csv_item=$ROOT_PATH/tianchi_mobile_recommend_train_item.csv
csv_item_new=$ROOT_PATH/train_item.csv

tail +2 $csv_user | sed 's/$/&:00:00/' > $csv_user_new
tail +2 $csv_item > $csv_item_new
