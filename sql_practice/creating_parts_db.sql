--manufacturers
INSERT INTO manufacturers (id, name) VALUES
(11, 'Pip-NNC Industrial'),
(3, 'Acme Components'),
(4, 'Bright Electronics'),
(5, 'Transistor Corp'),
(6, 'DiodeWorks'),
(7, 'Potentiometer Inc'),
(8, 'Microchip Ltd'),
(9, 'Crystal Co'),
(10, 'SwitchMasters');

--parts
INSERT INTO parts (id, description, code, quantity, manufacturer_id) VALUES
(1, '5V resistor', 'R-001', 100, 11),
(2, '3V resistor', 'R-002', 150, 11),
(3, 'Capacitor 10uF', 'C-003', 200, 3),
(4, 'LED Red', 'LED-004', 500, 4),
(5, 'Transistor NPN', 'T-005', 300, 5),
(6, 'Diode 1N4001', 'D-006', 250, 6),
(7, 'Potentiometer 10k', 'P-007', 120, 7),
(8, 'Microcontroller', 'MCU-008', 80, 8),
(9, 'Crystal 16MHz', 'X-009', 60, 9),
(10, 'Switch SPST', 'S-010', 400, 10),
(54, 'unavailable', 'V1-009', 9, 11);

--part_descriptions
INSERT INTO part_descriptions (id, description) VALUES
(1, '5V resistor'),
(2, '3V resistor');

--reorder options
INSERT INTO part_descriptions (id, description) VALUES
(1, '5V resistor'),
(2, '3V resistor');

--locations
INSERT INTO locations (part_id, location, qty) VALUES
(1, 'Warehouse A', 50),
(2, 'Warehouse B', 60),
(3, 'Warehouse A', 80),
(4, 'Warehouse C', 120),
(5, 'Warehouse B', 70);

-- Retrieve the first 10 rows from the 'parts' table
select *
from parts
limit 10;

-- Modify the 'code' column in 'parts' to disallow NULL values
alter table parts
alter column code set not null;

-- Ensure that each value in the 'code' column is unique across the table
alter table parts
add unique(code);

-- Create a new table 'part_descriptions' with two columns: id and description
CREATE TABLE part_descriptions (
    id int PRIMARY KEY,       -- Primary key to uniquely identify each row
    description text          -- Text description of the part
);

-- Insert two rows into 'part_descriptions'
INSERT INTO part_descriptions VALUES 
    (1, '5V resistor'), 
    (2, '3V resistor');

-- Update 'parts' table to set the description from 'part_descriptions' where the description is currently NULL
UPDATE parts
SET description = part_descriptions.description
FROM part_descriptions
WHERE part_descriptions.id = parts.id
  AND parts.description IS NULL;

-- Ensure that the 'description' column in 'parts' cannot be NULL
alter table parts
alter column description set not null;

-- Insert a new row into 'parts' table
-- (id = 54, description = 'unavailable', code = 'V1-009', quantity = 9)
insert into parts values(54, 'unavailable', 'V1-009', 9);

-- Enforce that 'price_usd' in 'reorder_options' cannot be NULL
alter table reorder_options
alter column price_usd set not null;

-- Enforce that 'quantity' in 'reorder_options' cannot be NULL
alter table reorder_options
alter column quantity set not null;

-- Add a constraint to ensure both 'price_usd' and 'quantity' are greater than 0
alter table reorder_options
add check (price_usd > 0 and quantity > 0);

-- Add a constraint to ensure the price per unit is reasonable
alter table reorder_options
add check (price_usd/quantity > 0.02 and price_usd/quantity < 25);

-- Set the 'id' column in 'parts' as the primary key
alter table parts
add primary key (id);

-- Add a foreign key from 'reorder_options.part_id' to 'parts.id'
alter table reorder_options
add foreign key (part_id) references parts(id);

-- Add a constraint to ensure quantity in 'locations' is positive
alter table locations
add check (qty > 0);

-- Ensure that each combination of part_id and location is unique
alter table locations
add unique (part_id, location);

-- Add a foreign key from 'locations.part_id' to 'parts.id'
alter table locations
add foreign key (part_id) references parts(id);

-- Insert a new manufacturer into 'manufacturers' table
insert into manufacturers values (11, 'Pip-NNC Industrial');

-- Retrieve all rows from the 'manufacturers' table
select *
from manufacturers;

-- Update parts to assign manufacturer_id = 11 where it was previously 1 or 2
update parts
set manufacturer_id = 11
where manufacturer_id in (1, 2);

-- Retrieve all rows from 'parts' table
select *
from parts;
