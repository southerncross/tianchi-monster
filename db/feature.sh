#!/bin/bash

# 使用方法
# 1. 修改ROOT_PATH为导出的csv文件的路径
# 2. 修改csv_name为导出的csv文件名
# 3. 修改sql为自定义的查询语句

ROOT_PATH=/Users/dengshihong/workspace/tianchi-monster/db

#提取每个人对每种商品的统计
#csv_name=feature31_5.csv
#target=31
#span=5
#sql="select user_id, item_id, coalesce(type1, 0) as type1, coalesce(type2, 0) as type2, coalesce(type3, 0) as type3, coalesce(type4, 0) as type4 from (select user_id, item_id, coalesce(type1, 0) as type1, coalesce(type2, 0) as type2, coalesce(type3, 0) as type3 from (select user_id, item_id, coalesce(type1, 0) as type1, coalesce(type2, 0) as type2 from (select user_id, item_id, count(*) as type1 from train_user where behavior_type=1 and hours <= 24 * ($target - 1) and hours >= 24 * ($target - 1 - $span) group by user_id, item_id) A full outer join (select user_id, item_id, count(*) as type2 from train_user where behavior_type=2 and hours <= 24 * ($target - 1) and hours >= 24 * ($target - 1 - $span) group by user_id, item_id) B  using(user_id, item_id)) AB full outer join (select user_id, item_id, count(*) as type3 from train_user where behavior_type=3 and hours <= 24 * ($target - 1) and hours >= 24 * ($target - 1 - $span) group by user_id, item_id) C using (user_id, item_id)) ABC full outer join (select user_id, item_id, count(*) as type4 from train_user where behavior_type=4 and hours <= 24 * ($target - 1) and hours >= 24 * ($target - 1 - $span) group by user_id, item_id) D using (user_id, item_id)"
#sql="select user_id, item_id, count(*) as type4 from train_user where behavior_type=4 and hours <= 24 * ($target - 1) and hours >= 24 * ($target - 1 - $span) group by user_id, item_id"


#csv_name=feature_item_hotness.csv
#sql="select item_id, alltype, coalesce(type1, 0) as type1, coalesce(type2, 0) as type2, coalesce(type3, 0) as type3, coalesce(type4, 0) as type4 from (((((select item_id, count(*) as alltype from train_user group by item_id) A left join (select item_id, count(*) as type1 from train_user where behavior_type=1 group by item_id) B using(item_id)) AB left join (select item_id, count(*) as type2 from train_user where behavior_type=2 group by item_id) C using(item_id)) ABC left join (select item_id, count(*) as type3 from train_user where behavior_type=3 group by item_id) D using(item_id)) ABCD left join (select item_id, count(*) as type4 from train_user where behavior_type=4 group by item_id) E using(item_id))" 


#csv_name=feature_user_behavior.csv
#sql="select user_id, alltype, coalesce(type1, 0) as type1, coalesce(type2, 0) as type2, coalesce(type3, 0) as type3, coalesce(type4, 0) as type4 from (((((select user_id, count(*) as alltype from train_user group by user_id) A left join (select user_id, count(*) as type1 from train_user where behavior_type=1 group by user_id) B using(user_id)) AB left join (select user_id, count(*) as type2 from train_user where behavior_type=2 group by user_id) C using(user_id)) ABC left join (select user_id, count(*) as type3 from train_user where behavior_type=3 group by user_id) D using(user_id)) ABCD left join (select user_id, count(*) as type4 from train_user where behavior_type=4 group by user_id) E using(user_id))" 

csv_name=feature_item_category_hotness.csv
sql="select item_category, alltype, coalesce(type1, 0) as type1, coalesce(type2, 0) as type2, coalesce(type3, 0) as type3, coalesce(type4, 0) as type4 from (((((select item_category, count(*) as alltype from train_user group by item_category) A left join (select item_category, count(*) as type1 from train_user where behavior_type=1 group by item_category) B using(item_category)) AB left join (select item_category, count(*) as type2 from train_user where behavior_type=2 group by item_category) C using(item_category)) ABC left join (select item_category, count(*) as type3 from train_user where behavior_type=3 group by item_category) D using(item_category)) ABCD left join (select item_category, count(*) as type4 from train_user where behavior_type=4 group by item_category) E using(item_category))"

psql -d tianchi -c "COPY ($sql) to '$ROOT_PATH/$csv_name' with delimiter ',';"