create table parents as
  select "abraham" as parent, "barack" as child union
  select "abraham"          , "clinton"         union
  select "delano"           , "herbert"         union
  select "fillmore"         , "abraham"         union
  select "fillmore"         , "delano"          union
  select "fillmore"         , "grover"          union
  select "eisenhower"       , "fillmore";

create table dogs as
  select "abraham" as name, "long" as fur, 26 as height union
  select "barack"         , "short"      , 52           union
  select "clinton"        , "long"       , 47           union
  select "delano"         , "long"       , 46           union
  select "eisenhower"     , "short"      , 35           union
  select "fillmore"       , "curly"      , 32           union
  select "grover"         , "short"      , 28           union
  select "herbert"        , "curly"      , 31;

create table sizes as
  select "toy" as size, 24 as min, 28 as max union
  select "mini",        28,        35        union
  select "medium",      35,        45        union
  select "standard",    45,        60;

-------------------------------------------------------------
-- PLEASE DO NOT CHANGE ANY SQL STATEMENTS ABOVE THIS LINE --
-------------------------------------------------------------

-- The size of each dog
create table size_of_dogs as
  select name, size from dogs, sizes where min < height and height <= max;

-- All dogs with parents ordered by decreasing height of their parent
create table by_height as
  select child from dogs, parents where parent == name order by -height;

-- Sentences about siblings that are the same size
-- create table sized_parents as 
--   select *, size from parents, size_of_dogs where size_of_dogs.name = parents.child;
-- create table sentences as 
--   with siblings(first_name, second_name) as (select a.child, b.child from sized_parents as a, sized_parents as b where a.parent == b.parent and a.child != b.child and a.size = b.size and a.child < b.child order by b.size)
--   select distinct c.first_name || " and " || c.second_name || " are " || d.size || " siblings " from siblings as c, sized_parents as d where d.size = 'toy' or d.size = 'standard';

create table sentences as
  with siblings(first_name, second_name, sizer) as (select a.child, b.child, f.size from parents as a, parents as b, size_of_dogs as f where a.parent == b.parent and a.child != b.child and f.name == a.child and a.child < b.child order by size)
  select distinct c.first_name || " and " || c.second_name || " are " || c.sizer || " siblings " from siblings as c, size_of_dogs;

-- Ways to stack 4 dogs to a height of at least 170, ordered by total height
create table stacks as
  select "REPLACE THIS LINE WITH YOUR SOLUTION";

-- non_parents is an optional, but recommended question
-- All non-parent relations ordered by height difference
create table non_parents as
  select "REPLACE THIS LINE WITH YOUR SOLUTION";

create table ints as
    with i(n) as (
        select 1 union
        select n+1 from i limit 100
    )
    select n from i;

create table divisors as
    select "REPLACE THIS LINE WITH YOUR SOLUTION";

create table primes as
    select "REPLACE THIS LINE WITH YOUR SOLUTION";
