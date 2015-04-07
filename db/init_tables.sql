-- 创建俩表，因为表明都指定好了，所以其他的shell脚本里的名字都不要改

DROP TABLE train_item;
CREATE TABLE train_item(
  item_id int8 PRIMARY KEY,
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
  hours integer,
  PRIMARY KEY (user_id, item_id)
);
