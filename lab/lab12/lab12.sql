.read fa16data.sql
.read sp17data.sql

CREATE TABLE obedience AS
  select seven, hilfinger from STUDENTS;

CREATE TABLE smallest_int AS
  select time, smallest from STUDENTS where smallest > 16 order by smallest limit 20;

CREATE TABLE greatstudents AS
  select a.date, a.color, a.pet, a.number, b.number FROM STUDENTS AS a, fa16students AS b where a.date = b.date AND a.color = b.color AND a.pet = b.pet;


CREATE TABLE sevens AS
  select a.seven from STUDENTS AS a, CHECKBOXES AS b where a.number is 7 and b.'7' is 'True' and a.time = b.time;

CREATE TABLE matchmaker AS
  select a.pet, a.song, a.color, b.color FROM STUDENTS AS a, STUDENTS AS b where a.time < b.time and a.pet = b.pet and a.song = b.song;
