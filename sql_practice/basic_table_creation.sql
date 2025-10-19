-- Create a table named "friends" with three columns: id, name, and birthday
create table friends
(
    id INTEGER,       -- Unique identifier for each friend
    name TEXT,        -- Friend's name
    birthday DATE     -- Friend's birthday
);

-- Insert three rows of data into the "friends" table
insert into friends (id, name, birthday)
values 
    (1, 'Ororo Monroe', '1940-05-30'),   -- Use ISO date format YYYY-MM-DD
    (2, 'Awesome Sauce', '1985-04-10'),
    (3, 'Too Awesome', '1990-12-25');

-- Update the "name" column to SQL NULL for the friend with id = 1
update friends
set name = NULL
where id = 1;

-- Add a new column called "email" to the "friends" table
alter table friends
add column email TEXT;

-- Set the "email" column only for rows where it is currently NULL
update friends
set email = 'storm@codecademy.com'
where email is NULL;

-- Delete the row from the "friends" table where id = 1
delete from friends
where id = 1;

-- Retrieve all remaining rows and columns from the "friends" table
select *
from friends;
