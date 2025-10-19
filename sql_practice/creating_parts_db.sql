/* sample dataset and schema constraints 
    for showcasing sql and analytics engineering skills */

-- manufacturers
insert into manufacturers (id, name) values
(11, 'Pip-NNC Industrial'),
(3, 'Acme Components'),
(4, 'Bright Electronics'),
(5, 'Transistor Corp'),
(6, 'DiodeWorks'),
(7, 'Potentiometer Inc'),
(8, 'Microchip Ltd'),
(9, 'Crystal Co'),
(10, 'SwitchMasters');

-- parts
insert into parts (id, description, code, quantity, manufacturer_id) values
(1, '5v resistor', 'r-001', 100, 11),
(2, '3v resistor', 'r-002', 150, 11),
(3, 'capacitor 10uf', 'c-003', 200, 3),
(4, 'led red', 'led-004', 500, 4),
(5, 'transistor npn', 't-005', 300, 5),
(6, 'diode 1n4001', 'd-006', 250, 6),
(7, 'potentiometer 10k', 'p-007', 120, 7),
(8, 'microcontroller', 'mcu-008', 80, 8),
(9, 'crystal 16mhz', 'x-009', 60, 9),
(10, 'switch spst', 's-010', 400, 10),
(54, 'unavailable', 'v1-009', 9, 11);

-- reorder options
insert into reorder_options (id, part_id, quantity, price_usd) values
(1, 1, 100, 0.10),
(2, 2, 150, 0.15);

-- locations
insert into locations (part_id, location, qty) values
(1, 'warehouse a', 50),
(2, 'warehouse b', 60),
(3, 'warehouse a', 80),
(4, 'warehouse c', 120),
(5, 'warehouse b', 70);

-- create part_descriptions table
create table part_descriptions (
    id int primary key,
    description text
);

-- example data for part_descriptions
insert into part_descriptions (id, description) values
(1, '5v resistor'),
(2, '3v resistor');

-- retrieve the first 10 rows from parts
select *
from parts
limit 10;

-- make 'code' column in parts not null
alter table parts
alter column code set not null;

-- ensure each value in 'code' is unique
alter table parts
add unique (code);

-- update parts descriptions where null using part_descriptions
update parts
set description = part_descriptions.description
from part_descriptions
where part_descriptions.id = parts.id
  and parts.description is null;

-- ensure description column in parts cannot be null
alter table parts
alter column description set not null;

-- enforce not null constraints on reorder_options
alter table reorder_options
alter column price_usd set not null,
alter column quantity set not null;

-- add valid range and ratio checks for reorder_options
alter table reorder_options
add check (price_usd > 0 and quantity > 0),
add check (price_usd/quantity > 0.02 and price_usd/quantity < 25);

-- set id as primary key for parts
alter table parts
add primary key (id);

-- add foreign key from reorder_options.part_id to parts.id
alter table reorder_options
add foreign key (part_id) references parts(id);

-- add positive quantity check for locations
alter table locations
add check (qty > 0);

-- ensure each (part_id, location) pair is unique
alter table locations
add unique (part_id, location);

-- add foreign key from locations.part_id to parts.id
alter table locations
add foreign key (part_id) references parts(id);

-- retrieve all rows from manufacturers
select *
from manufacturers;

-- update parts to assign manufacturer_id = 11 where it was 1 or 2
update parts
set manufacturer_id = 11
where manufacturer_id in (1, 2);

-- retrieve all rows from parts
select *
from parts;

