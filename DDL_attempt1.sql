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

DROP TABLE IF EXISTS `customers`;
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

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'John Smith','john.smith@email.com','503-555-0123'),(2,'Maria Garcia','mgarcia@email.com','971-555-0456'),(3,'Alex Wong','awong@email.com','503-555-0789'),(4,'Lisa Brown','lbrown@email.com','971-555-4321');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservations` (
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

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` VALUES (1,'2025-02-10 18:30:00',1,1,1,'active'),(2,'2025-02-11 19:00:00',2,2,2,'pending'),(3,'2025-02-12 20:00:00',3,3,3,'cancelled'),(4,'2025-02-13 21:00:00',4,4,4,'active'),(5,'2025-02-10 18:30:00',1,1,1,'active'),(6,'2025-02-11 19:00:00',2,2,2,'pending'),(7,'2025-02-12 20:00:00',3,3,3,'cancelled'),(8,'2025-02-13 21:00:00',4,4,4,'active'),(9,'2025-02-10 18:30:00',1,1,1,'active'),(10,'2025-02-11 19:00:00',2,2,2,'pending'),(11,'2025-02-12 20:00:00',3,3,3,'cancelled'),(12,'2025-02-13 21:00:00',4,4,4,'active'),(13,'2025-02-10 18:30:00',1,1,1,'active'),(14,'2025-02-11 19:00:00',2,2,2,'pending'),(15,'2025-02-12 20:00:00',3,3,3,'cancelled'),(16,'2025-02-13 21:00:00',4,4,4,'active'),(17,'2025-02-10 18:30:00',1,1,1,'active'),(18,'2025-02-11 19:00:00',2,2,2,'pending'),(19,'2025-02-12 20:00:00',3,3,3,'cancelled'),(20,'2025-02-13 21:00:00',4,4,4,'active');
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servers`
--

DROP TABLE IF EXISTS `servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servers` (
  `employeeID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`employeeID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servers`
--

LOCK TABLES `servers` WRITE;
/*!40000 ALTER TABLE `servers` DISABLE KEYS */;
INSERT INTO `servers` VALUES (1,'John Porker'),(2,'Michael Chen'),(3,'Emily Rodriguez'),(4,'David Kim'),(5,'John Porker'),(6,'Michael Chen'),(7,'Emily Rodriguez'),(8,'David Kim'),(9,'John Porker'),(10,'Michael Chen'),(11,'Emily Rodriguez'),(12,'David Kim'),(13,'John Porker'),(14,'Michael Chen'),(15,'Emily Rodriguez'),(16,'David Kim'),(17,'John Porker'),(18,'Michael Chen'),(19,'Emily Rodriguez'),(20,'David Kim');
/*!40000 ALTER TABLE `servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serversTables`
--

DROP TABLE IF EXISTS `serversTables`;
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
/*!40000 ALTER TABLE `serversTables` DISABLE KEYS */;
INSERT INTO `serversTables` VALUES (1,1,'2025-02-05 16:55:44','open'),(2,2,'2025-02-05 16:55:44','open'),(3,3,'2025-02-05 16:55:44','open'),(4,4,'2025-02-05 16:55:44','open');
/*!40000 ALTER TABLE `serversTables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tables`
--

DROP TABLE IF EXISTS `tables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tables` (
  `tableID` int(11) NOT NULL AUTO_INCREMENT,
  `seatsAvail` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`tableID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tables`
--

LOCK TABLES `tables` WRITE;
/*!40000 ALTER TABLE `tables` DISABLE KEYS */;
INSERT INTO `tables` VALUES (1,4,1),(2,2,1),(3,6,0),(4,8,1),(5,4,1),(6,2,1),(7,6,0),(8,8,1),(9,4,1),(10,2,1),(11,6,0),(12,8,1),(13,4,1),(14,2,1),(15,6,0),(16,8,1),(17,4,1),(18,2,1),(19,6,0),(20,8,1);
/*!40000 ALTER TABLE `tables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabs`
--

DROP TABLE IF EXISTS `tabs`;
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

LOCK TABLES `tabs` WRITE;
/*!40000 ALTER TABLE `tabs` DISABLE KEYS */;
INSERT INTO `tabs` VALUES (1,45.99,1),(2,127.50,2),(3,89.75,3),(4,156.80,1),(5,45.99,1),(6,127.50,2),(7,89.75,3),(8,156.80,1),(9,45.99,1),(10,127.50,2),(11,89.75,3),(12,156.80,1),(13,45.99,1),(14,127.50,2),(15,89.75,3),(16,156.80,1),(17,45.99,1),(18,127.50,2),(19,89.75,3),(20,156.80,1);
/*!40000 ALTER TABLE `tabs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-05 16:57:30
