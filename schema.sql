drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  address text not null,
  x_coord double precision not null,
  y_coord double precision not null,
  rent integer not null
);