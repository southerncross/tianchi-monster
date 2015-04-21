-- 创建俩表，因为表明都指定好了，所以其他的shell脚本里的名字都不要改

/*
DROP TABLE train_item;
CREATE TABLE train_item(
  item_id int8,
  item_geohash character(16),
  item_category integer
);

DROP TABLE train_user;
CREATE TABLE train_user(
  user_id int8,
  item_id int8,
  behavior_type integer,
  user_geohash character(16),
  item_category integer,
  hours integer
);
*/

/*
-- DROP TABLE train_user_limit;
CREATE TABLE train_user_limit(
  user_id int8,
  item_id int8,
  behavior_type integer,
  user_geohash character(16),
  item_category integer,
  hours integer
);
*/

/*
DROP TABLE user_type;
CREATE TABLE user_type(
  user_id int8,
  behavior_type integer,
  max_itv int8,
  min_itv int8,
  average_itv int8,
  variance_itv int8
);
*/

DROP TABLE user_foremost_itv;
CREATE TABLE user_foremost_itv(
  user_id int8,
  behavior_type integer,
  max_itv int8,
  min_itv int8,
  average_itv int8,
  variance_itv int8
);

