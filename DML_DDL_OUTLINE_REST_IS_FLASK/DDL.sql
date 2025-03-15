-- This DDL creates the database schema for the Backwoods Burgers system.
-- It includes tables for customers, reservations, servers, tables, and tabs.

-- Set the character set to utf8mb4 for proper Unicode support
SET NAMES utf8mb4;

-- Advised to set these in Canvas, then set back to 1 at end of the DDL
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0; 


-- ------------------------------------------------------
-- Create the `customers` table
-- ------------------------------------------------------

CREATE TABLE `customers` (
    `customerID` INT AUTO_INCREMENT, -- Unique identifier for each customer
    `name` VARCHAR(50) NOT NULL, -- Customer's full name
    `customerEmail` VARCHAR(100), -- Customer's email address (optional)
    `customerPhone` VARCHAR(20) NOT NULL, -- Customer's phone number
    PRIMARY KEY (`customerID`), -- Primary key constraint on customerID
    UNIQUE KEY `customerPhone_UNIQUE` (`customerPhone`), -- Unique constraint on customerPhone
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------
-- Insert data into the `customers` table
-- ------------------------------------------------------

INSERT INTO `customers` (`customerID`, `name`, `customerEmail`, `customerPhone`) VALUES 
    (1,'Emily Davis','emily.davis@email.com','555-123-4567'),
    (2,'Benjamin Lee','benjamin.lee@email.com','555-234-5678'),
    (3,'Chloe Scott','chloe.scott@email.com','555-345-6789'),
    (4,'Noah Harris','noah.harris@email.com','555-456-7890'),
    (21,'Leon Bridges','leon1234@gmail.com','904-555-0168'),
    (22,'Billy Chao','chaodown2004@gmail.com','915-556-6666');

-- ------------------------------------------------------
-- Create the `servers` table
-- ------------------------------------------------------

CREATE TABLE `servers` (
    `employeeID` INT AUTO_INCREMENT, -- Unique identifier for each server
    `name` VARCHAR(45) NOT NULL, -- Server's full name
    PRIMARY KEY (`employeeID`) -- Primary key constraint on employeeID
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------
-- Insert data into the `servers` table
-- ------------------------------------------------------

INSERT INTO `servers` (`employeeID`, `name`) VALUES 
    (1,'John Porker'),
    (2,'Michael Chen'),
    (3,'Emily Rodriguez'),
    (4,'David Kim'),
    (22,'Jim Jon'),
    (23,'Big Al'),
    (24,'Bob Fletcher'),
    (28,'Donald Duck');

-- ------------------------------------------------------
-- Create the `tables` table
-- ------------------------------------------------------

CREATE TABLE `tables` (
    `tableID` INT AUTO_INCREMENT, -- Unique identifier for each table
    `seatsAvail` INT NOT NULL, -- Number of seats available at the table
    `status` ENUM('avail','taken') DEFAULT 'avail', -- Status of the table (available or taken)
    PRIMARY KEY (`tableID`) -- Primary key constraint on tableID
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------
-- Insert data into the `tables` table
-- ------------------------------------------------------

INSERT INTO `tables` (`tableID`, `seatsAvail`, `status`) VALUES 
    (2,2,'taken'),
    (3,6,'taken'),
    (4,8,'taken'),
    (23,15,'taken'),
    (24,4,'taken'),
    (25,2,'avail'),
    (26,9,'avail');

-- ------------------------------------------------------
-- Create the `reservations` table
-- ------------------------------------------------------

CREATE TABLE `reservations` (
    `reservationID` INT AUTO_INCREMENT, -- Unique identifier for each reservation
    `reservationDateTime` DATETIME NOT NULL, -- Date and time of the reservation
    `customerID` INT NOT NULL, -- Foreign key referencing the `customers` table
    `employeeID` INT, -- Foreign key referencing the `servers` table (optional)
    `tableID` INT, -- Foreign key referencing the `tables` table (optional)
    `status` ENUM('pending','cancelled','active'), -- Status of the reservation
    PRIMARY KEY (`reservationID`), -- Primary key constraint on reservationID
    KEY `customerID_idx` (`customerID`), -- Index on customerID for faster lookups
    KEY `employeeID_idx` (`employeeID`), -- Index on employeeID for faster lookups
    KEY `tableID_idx` (`tableID`), -- Index on tableID for faster lookups
    CONSTRAINT `fkReservationCustomerID` FOREIGN KEY (`customerID`) REFERENCES `customers` (`customerID`) ON DELETE CASCADE, -- Foreign key constraint referencing `customers` table
    CONSTRAINT `fkReservationEmployeeID` FOREIGN KEY (`employeeID`) REFERENCES `servers` (`employeeID`) ON DELETE CASCADE, -- Foreign key constraint referencing `servers` table
    CONSTRAINT `fkReservationTableID` FOREIGN KEY (`tableID`) REFERENCES `tables` (`tableID`) ON DELETE CASCADE -- Foreign key constraint referencing `tables` table
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------
-- Insert data into the `reservations` table
-- ------------------------------------------------------

INSERT INTO `reservations` (`reservationID`, `reservationDateTime`, `customerID`, `employeeID`, `tableID`, `status`) VALUES 
    (2,'2025-02-08 19:30:00',2,2,2,'pending'),
    (3,'2025-02-12 20:00:00',3,3,3,'cancelled'),
    (4,'2025-02-13 21:00:00',4,4,4,'active'),
    (21,'2025-12-21 12:39:00',1,1,3,'active'),
    (22,'2055-01-23 08:00:00',21,23,4,'pending');

-- ------------------------------------------------------
-- Create the `serversTables` table
-- ------------------------------------------------------

CREATE TABLE `serversTables` (
    `tableID` INT NOT NULL, -- Foreign key referencing the `tables` table
    `employeeID` INT NOT NULL, -- Foreign key referencing the `servers` table
    `dateTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Date and time of the record creation
    `status` ENUM('open','closed'), -- Status of the server-table assignment
    `currentID` INT AUTO_INCREMENT, -- Unique identifier for each record
    PRIMARY KEY (`currentID`), -- Primary key constraint on currentID
    UNIQUE KEY `unique_server_table` (`employeeID`,`tableID`), -- Unique constraint on the combination of employeeID and tableID
    KEY `employeeID_idx` (`employeeID`), -- Index on employeeID for faster lookups
    KEY `fkInterSecTableID` (`tableID`), -- Index on tableID for faster lookups
    CONSTRAINT `fkInterSecemployeeID` FOREIGN KEY (`employeeID`) REFERENCES `servers` (`employeeID`) ON DELETE CASCADE, -- Foreign key constraint referencing `servers` table
    CONSTRAINT `fkInterSecTableID` FOREIGN KEY (`tableID`) REFERENCES `tables` (`tableID`) ON DELETE CASCADE -- Foreign key constraint referencing `tables` table
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------
-- Insert data into the `serversTables` table
-- ------------------------------------------------------

INSERT INTO `serversTables` (`tableID`, `employeeID`, `dateTime`, `status`, `currentID`) VALUES 
    (3,1,'2025-02-20 01:58:18','open',41),
    (3,23,'2025-02-20 01:58:23','open',42),
    (24,1,'2025-02-20 01:58:26','open',43),
    (23,23,'2025-02-20 01:58:30','open',44),
    (23,3,'2025-02-20 01:58:34','open',45),
    (4,3,'2025-02-20 02:05:11','open',46),
    (2,22,'2025-02-20 23:36:25','open',48);

-- ------------------------------------------------------
-- Create the `tabs` table
-- ------------------------------------------------------

CREATE TABLE `tabs` (
    `tabID` INT AUTO_INCREMENT, -- Unique identifier for each tab
    `total` DECIMAL(10,2), -- Total amount due on the tab
    `tableID` INT NOT NULL, -- Foreign key referencing the `tables` table
    PRIMARY KEY (`tabID`), -- Primary key constraint on tabID
    KEY `tableID_idx` (`tableID`), -- Index on tableID for faster lookups
    CONSTRAINT `fkTabsTableID` FOREIGN KEY (`tableID`) REFERENCES `tables` (`tableID`) ON DELETE CASCADE -- Foreign key constraint referencing `tables` table
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------
-- Insert data into the `tabs` table
-- ------------------------------------------------------

INSERT INTO `tabs` (`tabID`, `total`, `tableID`) VALUES 
    (2,'127.50',2),
    (3,'89.75',3);


--Turning foreign key checks back on after table creation
SET FOREIGN_KEY_CHECKS=1;
SET AUTOCOMMIT = 1;
COMMIT; 