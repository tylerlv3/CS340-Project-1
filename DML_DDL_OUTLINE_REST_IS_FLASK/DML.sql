--Will be using % to show data passed from Jinja Templates which is then executed in backend
--When a variable is given from an dropdown or input it will be labeled as so, if it is left as %s, it is a built in form within the table and the input is automatically assigned at row creation, essentially a prefilled form waiting for submission.


-- Insert a new party into the serversTables table.
-- This represents a new guest being seated at a table.
-- The status is initially set to 'open'.
-- Parameters: employeeID, tableID, status
INSERT INTO serversTables (employeeID, tableID, status)
VALUES (%employeeID_dropdown, %tableID_dropdown, 'open');

-- Update the status of a table to 'taken'.
-- This happens when a new party is seated at the table.
-- Parameters: tableID
UPDATE tables SET status = 'taken' WHERE tableID = %s;

-- Select all data from the serversTables table, along with the server's name.
-- This retrieves the current seating information.
-- It joins the serversTables table with the servers table to get the server's name.
SELECT st.*, s.name AS server_name
FROM serversTables st
JOIN servers s ON st.employeeID = s.employeeID;

-- Select employeeID and name from the servers table.
-- This retrieves the list of employees for the dropdown menu in the form.
SELECT employeeID, name FROM servers;

-- Select tableID from the tables table where the status is 'avail'.
-- This retrieves the available tables for the dropdown menu in the form.
SELECT tableID FROM tables WHERE status = 'avail';

-- Select customerID and name from the customers table.
-- This retrieves the list of customers for the dropdown menu in the form.
SELECT customerID, name FROM customers;

-- Select all data from the reservations table, along with the server's and customer's names.
-- This retrieves the reservation information.
-- It joins the reservations table with the servers and customers tables to get the names.
SELECT r.*, s.name as server_name, c.name as customer_name 
FROM reservations r 
JOIN servers s ON r.employeeID = s.employeeID 
JOIN customers c ON r.customerID = c.customerID;

-- Select all data from the tables table.
-- This retrieves the table information.
SELECT * FROM tables;

-- Select all data from the servers table.
-- This retrieves the employee (server) information.
SELECT * FROM servers;

-- Select all data from the customers table.
-- This retrieves the customer information.
SELECT * FROM customers;


-- Update the status of a party in the serversTables table.
-- This is used to change the status of a party (e.g., from 'open' to 'closed').
-- Parameters: new_status, currentID
UPDATE serversTables SET status = %s WHERE currentID = %s;

-- Select the tableID from the serversTables table for a given currentID.
-- This is used to get the tableID associated with a party.
-- Parameters: currentID
SELECT tableID FROM serversTables WHERE currentID = %s;

-- Update the status of a table in the tables table.
-- This is used to change the status of a table (e.g., from 'taken' to 'avail').
-- Parameters: table_status, tableID
UPDATE tables SET status = %s WHERE tableID = %s;

-- Delete a party from the serversTables table.
-- This is used when a party leaves.
-- Parameters: currentID
DELETE FROM serversTables WHERE currentID = %s;

-- Insert a new employee into the servers table.
-- Parameters: name
INSERT INTO servers (name)
VALUES (%name_input);

-- Delete an employee from the servers table.
-- Parameters: employeeID
DELETE FROM servers WHERE employeeID = %s;

-- Insert a new table into the tables table.
-- Parameters: seatsAvail
INSERT INTO tables (seatsAvail)
VALUES (%seatsAvail_input);

-- Update a table's status in the tables table.
-- Parameters: status, tableID
--Form is directly in table, so variables are passed automatically, no input needed
UPDATE tables SET status = %s WHERE tableID = %s;

-- Delete a table from the tables table.
-- Parameters: tableID
DELETE FROM tables WHERE tableID = %s;

-- Select all data from the tabs table.
-- This retrieves the tab information.
SELECT * FROM tabs;

-- Select tableID and status from the tables table.
-- This retrieves the table information for the dropdown in tabs page.
SELECT tableID, status FROM tables;

-- Insert a new tab into the tabs table.
-- Parameters: tableID, total
INSERT INTO tabs (tableID, total)
VALUES (%tableID_dropdown, %total_input);

-- Insert a new customer into the customers table.
-- Parameters: name, customerEmail, customerPhone
INSERT INTO customers (name, customerEmail, customerPhone)
VALUES (%name_input, %email_input, %phone_input);

-- Insert a new reservation into the reservations table.
-- Parameters: customerID, employeeID, tableID, reservationDateTime, status
INSERT INTO reservations (customerID, employeeID, tableID, reservationDateTime, status)
VALUES (%customerID_dropdown, %employeeID_dropdown, %tableID_dropdown, %date_input, %status_input);


-- Instert a new row into serversTables for a server:table assignment
INSERT INTO serversTables (employeeID, tableID, status)
VALUES (%employeeID_dropdown, %preset_interface, 'open');

-- Delete a row from serversTables for a server:table assignment when it is selected as deleted in the current table
DELETE FROM serversTables WHERE employeeID = %s AND tableID = %s;


-- Select the status of a table from the tables table, then update it to opposite of what it currently is, also updates table table.
SELECT status FROM tables WHERE tableID = %s
UPDATE tables SET status = %s WHERE tableID = %s"