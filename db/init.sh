#!/bin/bash

ROOT_PATH=/Users/lishunyang/workspace/tianchi-monster/db
table_item=train_item
csv_item=$ROOT_PATH/$table_item.csv
table_user=train_user
csv_user=$ROOT_PATH/$table_user.csv

psql -d tianchi -f init_tables.sql
psql -d tianchi -c "COPY $table_item from '$csv_item' with delimiter ',';"
psql -d tianchi -c "COPY $table_user from '$csv_user' with delimiter ',';"
