#!/bin/bash

ROOT_PATH=/Users/dengshihong/workspace/tianchi-monster/db

echo start
table=train_user_limit
for target in 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
do
	echo processing $target
	csv_name=tag_limit/tag_limit${target}.csv
	sql="select user_id, item_id, count(*) from $table where behavior_type=4 and hours < $target * 24 and hours >= ($target - 1) * 24 group by user_id, item_id"
	psql -d tianchi -c "COPY ($sql) to '$ROOT_PATH/$csv_name' with delimiter ',';"
done
echo end