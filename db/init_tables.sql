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
  time timestamp
);
