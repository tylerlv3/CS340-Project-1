-- Insert sample data for tables
-- status: 0 = unavailable, 1 = available
INSERT INTO `cs340_vincenty`.`tables` (`seatsAvail`, `status`) VALUES 
(4, 1),
(2, 1),
(6, 0),
(8, 1);

-- Insert sample data for tabs
INSERT INTO `cs340_vincenty`.`tabs` (`total`, `tableID`) VALUES 
(45.99, 1),
(127.50, 2),
(89.75, 3),
(156.80, 1);

-- Insert sample data for servers
INSERT INTO `cs340_vincenty`.`servers` (`name`) VALUES 
('John Porker'),
('Michael Chen'),
('Emily Rodriguez'),
('David Kim');

-- Insert sample data for customers
INSERT INTO `cs340_vincenty`.`customers` (`name`, `customerEmail`, `customerPhone`) VALUES 
('John Smith', 'john.smith@email.com', '503-555-0123'),
('Maria Garcia', 'mgarcia@email.com', '971-555-0456'),
('Alex Wong', 'awong@email.com', '503-555-0789'),
('Lisa Brown', 'lbrown@email.com', '971-555-4321');

-- Insert sample data for reservations
INSERT INTO `cs340_vincenty`.`reservations` (`reservationDateTime`, `customerID`, `employeeID`, `tableID`, `status`) VALUES 
('2025-02-10 18:30:00', 1, 1, 1, 'active'),
('2025-02-11 19:00:00', 2, 2, 2, 'pending'),
('2025-02-12 20:00:00', 3, 3, 3, 'cancelled'),
('2025-02-13 21:00:00', 4, 4, 4, 'active');

-- Insert sample data for serversTables
INSERT INTO `cs340_vincenty`.`serversTables` (`tableID`, `serverID`) VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4);

