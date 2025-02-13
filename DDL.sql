-- MariaDB dump 10.19  Distrib 10.5.22-MariaDB, for Linux (x86_64)
--
-- Host: classmysql.engr.oregonstate.edu    Database: cs340_vincenty
-- ------------------------------------------------------
-- Server version	10.11.10-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS `customers`; /*Creates or replaces the customers table. This table keeps a record of all customers and is used in conjunction with the reservations table to track reservations.  */
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `customerID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `customerEmail` varchar(100) NOT NULL,
  `customerPhone` varchar(20) NOT NULL,
  PRIMARY KEY (`customerID`),
  UNIQUE KEY `customerPhone_UNIQUE` (`customerPhone`),
  UNIQUE KEY `customerEmail_UNIQUE` (`customerEmail`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--
/*Inserts a few rows of example customer data that includes the neccesary columns such as phone, email, and name. A customerID is automatically generated for each customer record added.  */
LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Emily Davis','emily.davis@email.com','555-123-4567'),(2,'Benjamin Lee','benjamin.lee@email.com','555-234-5678'),(3,'Chloe Scott','chloe.scott@email.com','555-345-6789'),(4,'Noah Harris','noah.harris@email.com','555-456-7890');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservations` ( /*Creates or replaces the reservations table. This table holds all reservations past and present, being tracked with a status enumeration. This table has a foreign key of customerID, employeeID, and tableID.  */
  `reservationID` int(11) NOT NULL AUTO_INCREMENT,
  `reservationDateTime` datetime NOT NULL,
  `customerID` int(11) NOT NULL,
  `employeeID` int(11) DEFAULT NULL,
  `tableID` int(11) DEFAULT NULL,
  `status` enum('pending','cancelled','active') DEFAULT NULL,
  PRIMARY KEY (`reservationID`),
  KEY `customerID_idx` (`customerID`),
  KEY `employeeID_idx` (`employeeID`),
  KEY `tableID_idx` (`tableID`),
  CONSTRAINT `fkReservationCustomerID` FOREIGN KEY (`customerID`) REFERENCES `customers` (`customerID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fkReservationEmployeeID` FOREIGN KEY (`employeeID`) REFERENCES `servers` (`employeeID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fkReservationTableID` FOREIGN KEY (`tableID`) REFERENCES `tables` (`tableID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE; /*Inserts a few rows of example reservations that includes the neccesary columns such as time, customerID, employeeID, tableID, and status. A reservationID is automatically generated for each reservation added.  */
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` VALUES (1,'2025-02-07 18:00:00',1,1,1,'active'),(2,'2025-02-08 19:30:00',2,2,2,'pending'),(3,'2025-02-12 20:00:00',3,3,3,'cancelled'),(4,'2025-02-13 21:00:00',4,4,4,'active');
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servers`
--

DROP TABLE IF EXISTS `servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servers` ( /*Holds records for all employees at backwoods burgers. Includes a generated employeeID and name. These columns are used in multiple other tables. */
  `employeeID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`employeeID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servers`
--

LOCK TABLES `servers` WRITE; /*Adds a few employees to the employee table. */
/*!40000 ALTER TABLE `servers` DISABLE KEYS */;
INSERT INTO `servers` VALUES (1,'John Porker'),(2,'Michael Chen'),(3,'Emily Rodriguez'),(4,'David Kim');
/*!40000 ALTER TABLE `servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serversTables`
--

DROP TABLE IF EXISTS `serversTables`; /*This table handles all currently and previously seated tables. It aligns servers with tables and carries the time the table was seated and a status for if it is still open(party still present) or closed(interaction has ended,) */
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serversTables` (
  `tableID` int(11) NOT NULL,
  `serverID` int(11) NOT NULL,
  `dateTime` datetime NOT NULL DEFAULT current_timestamp(),
  `status` enum('open','closed') DEFAULT NULL,
  PRIMARY KEY (`serverID`,`tableID`),
  KEY `serverID_idx` (`serverID`),
  KEY `fkInterSecTableID` (`tableID`),
  CONSTRAINT `fkInterSecServerID` FOREIGN KEY (`serverID`) REFERENCES `servers` (`employeeID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fkInterSecTableID` FOREIGN KEY (`tableID`) REFERENCES `tables` (`tableID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serversTables`
--

LOCK TABLES `serversTables` WRITE;
/*!40000 ALTER TABLE `serversTables` DISABLE KEYS */; /*Some example tables all being seated at the same time, thus they are all open. */
INSERT INTO `serversTables` VALUES (1,1,'2025-02-05 16:55:44','open'),(2,2,'2025-02-05 16:55:44','open'),(3,3,'2025-02-05 16:55:44','open'),(4,4,'2025-02-05 16:55:44','open');
/*!40000 ALTER TABLE `serversTables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tables`
--

DROP TABLE IF EXISTS `tables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tables` ( /*Simple table to keep track of the resturants tables. Used to assign servers to and maintain a tables status(if it is ready to be used again, if it needs to be cleaned, or if a party is still there. Status is currently boolean, but going to switch to enumerate soon.) */
  `tableID` int(11) NOT NULL AUTO_INCREMENT,
  `seatsAvail` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`tableID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tables`
--

LOCK TABLES `tables` WRITE; /*Defines the tables in the resturant and that all are currently available*/
/*!40000 ALTER TABLE `tables` DISABLE KEYS */;
INSERT INTO `tables` VALUES (1,4,1),(2,2,1),(3,6,0),(4,8,1);
/*!40000 ALTER TABLE `tables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabs`
--

DROP TABLE IF EXISTS `tabs`; /*All of the tabs for the resturant current and past. These reference the table they originate from and carry a total. */
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabs` (
  `tabID` int(11) NOT NULL AUTO_INCREMENT,
  `total` decimal(10,2) DEFAULT NULL,
  `tableID` int(11) NOT NULL,
  PRIMARY KEY (`tabID`),
  KEY `tableID_idx` (`tableID`),
  CONSTRAINT `fkTabsTableID` FOREIGN KEY (`tableID`) REFERENCES `tables` (`tableID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabs`
--

LOCK TABLES `tabs` WRITE; /*Some sample tabs belonging to various tables. */
/*!40000 ALTER TABLE `tabs` DISABLE KEYS */;
INSERT INTO `tabs` VALUES (1,45.99,1),(2,127.50,2),(3,89.75,3),(4,156.80,1);
/*!40000 ALTER TABLE `tabs` ENABLE KEYS */;
UNLOCK TABLES;


SET FOREIGN_KEY_CHECKS=1;
COMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-05 16:57:30
