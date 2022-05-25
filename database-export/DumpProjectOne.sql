SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

-- MySQL dump 10.13  Distrib 5.7.37, for Win64 (x86_64)
--
-- Host: localhost    Database: Projectone
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.15-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP DATABASE IF EXISTS projectone;

CREATE DATABASE  IF NOT EXISTS `Projectone` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Projectone`;

CREATE USER IF NOT EXISTS 'Student'@'localhost' IDENTIFIED BY 'Student';
GRANT ALL PRIVILEGES ON * . * TO 'Student'@'192.168.168.169' WITH GRANT OPTION;
FLUSH PRIVILEGES;


--
-- Table structure for table `Device`
--

DROP TABLE IF EXISTS `Device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Device` (
  `DeviceId` int(11) NOT NULL AUTO_INCREMENT,
  `Naam` varchar(45) DEFAULT NULL,
  `Merk` varchar(45) DEFAULT NULL,
  `Beschrijving` varchar(100) DEFAULT NULL,
  `Type` varchar(45) DEFAULT NULL,
  `AankoopKost` float DEFAULT NULL,
  `Meeteenheid` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`DeviceId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Device`
--

LOCK TABLES `Device` WRITE;
/*!40000 ALTER TABLE `Device` DISABLE KEYS */;
INSERT INTO `Device` VALUES (1,'Water flow sensor','Otronic','Sensor om de water snelheid te meten','4013488820707',9,'liter/min'),(2,'Temperature sensor','Otronic','Sensor om de temperatuur te meten','DS18B20',4.95,'graden'),(3,'luchtvochtigheid sensor','Otronic','Sensor om de luchtvochtigheid te meten','3631225305938',3.39,'procent');
/*!40000 ALTER TABLE `Device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Gebruiker`
--

DROP TABLE IF EXISTS `Gebruiker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Gebruiker` (
  `GerbruikerId` int(11) NOT NULL,
  `Naam` varchar(45) DEFAULT NULL,
  `Voornaam` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`GerbruikerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gebruiker`
--

LOCK TABLES `Gebruiker` WRITE;
/*!40000 ALTER TABLE `Gebruiker` DISABLE KEYS */;
INSERT INTO `Gebruiker` VALUES (1,'Messiaen','Tibo'),(2,'Buyse','Tjorven'),(3,'Demortier','Ibe'),(4,'Depotter','Lander'),(5,'Delfosse','Doran'),(6,'Zwanepool','Sander'),(7,'Dedene','Xander'),(8,'Uitenhove','Thomas'),(9,'Devos','Milan'),(10,'Coninks','joergen'),(11,'Van den broeke','Niels'),(12,'Deblaere','michiel'),(13,'Depre','lars'),(14,'De jong','Noah'),(15,'Jansen','Arthur'),(16,'De Vries','Finn'),(17,'Van den Berg','jules'),(18,'van Dijk','liam'),(19,'Bakker','leon'),(20,'Janssen','Louis'),(21,'Visser','Lucas'),(22,'Smit','Adam'),(23,'Meijer','Matteo'),(24,'De Boer','Lewis'),(25,'Mulder','Otis'),(26,'de Groot','Vic'),(27,'Bos','Mathis'),(28,'Vos','Victor'),(29,'Peters','Oscar'),(30,'Hendriks','Emiel'),(31,'van Leeuwen','Elias'),(32,'Dekker','Felix'),(33,'Brouwer','jack'),(34,'de Wit','Vince'),(35,'Dijkstra','Lou'),(36,'Smits','Lowie'),(37,'de Graaf','Maurice'),(38,'van der Linden','Luca'),(39,'Kok','Alexander'),(40,'Jacobs','Marcel'),(41,'de Haan','Georges'),(42,'Vermeulen','léon'),(43,'van den Heuvel','Gust'),(44,'van der Veen','Rayan'),(45,'van den Broek','Amir'),(46,'de Bruijn','Oliver'),(47,'de Bruin','Lio'),(48,'van der Heijden','Mats'),(49,'Schouten','Tuur'),(50,'Maas','Milan');
/*!40000 ALTER TABLE `Gebruiker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Historiek`
--

DROP TABLE IF EXISTS `Historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Historiek` (
  `Volgnummer` int(11) NOT NULL,
  `DeviceId` int(11) NOT NULL,
  `GerbruikerId` int(11) NOT NULL,
  `ActieDatum` datetime DEFAULT NULL,
  `Waarde` float DEFAULT NULL,
  `Commentaar` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Volgnummer`,`DeviceId`,`GerbruikerId`),
  KEY `fk_Historiek_Device_idx` (`DeviceId`),
  KEY `fk_Historiek_Gebruiker1_idx` (`GerbruikerId`),
  CONSTRAINT `fk_Historiek_Device` FOREIGN KEY (`DeviceId`) REFERENCES `Device` (`DeviceId`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Historiek_Gebruiker1` FOREIGN KEY (`GerbruikerId`) REFERENCES `Gebruiker` (`GerbruikerId`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Historiek`
--

LOCK TABLES `Historiek` WRITE;
/*!40000 ALTER TABLE `Historiek` DISABLE KEYS */;
INSERT INTO `Historiek` VALUES (1,1,2,'2022-02-01 19:02:38',0.0957,'Douchen'),(2,3,13,'2022-01-07 02:08:02',8.9357,'Douchen'),(3,2,31,'2022-02-02 18:37:20',9.5671,'Douchen'),(4,2,40,'2022-03-24 00:19:56',2.4237,'Douchen'),(5,1,29,'2022-04-24 04:13:38',4.5343,'Douchen'),(6,3,33,'2022-01-20 23:50:22',5.2112,'Douchen'),(7,3,37,'2022-05-14 08:23:57',7.6515,'Douchen'),(8,2,22,'2022-01-14 18:29:59',8.824,'Douchen'),(9,2,43,'2022-05-17 14:12:12',4.4578,'Douchen'),(10,1,26,'2022-01-27 01:35:36',8.7508,'Douchen'),(11,1,14,'2022-04-10 06:27:56',4.8112,'Douchen'),(12,3,28,'2022-04-10 18:28:18',0.4536,'Douchen'),(13,3,45,'2022-03-05 13:16:18',7.7137,'Douchen'),(14,2,7,'2022-02-23 06:36:49',1.9398,'Douchen'),(15,1,32,'2022-04-12 03:45:04',6.4404,'Douchen'),(16,2,31,'2022-01-29 14:02:45',1.1244,'Douchen'),(17,3,34,'2022-01-20 13:15:55',9.8582,'Douchen'),(18,3,25,'2022-01-07 20:29:25',8.9329,'Douchen'),(19,1,23,'2022-01-28 19:51:15',8.0297,'Douchen'),(20,3,49,'2022-02-05 11:36:42',7.2758,'Douchen'),(21,2,34,'2022-02-11 07:18:07',3.0471,'Douchen'),(22,1,19,'2022-02-21 17:39:15',1.8294,'Douchen'),(23,2,36,'2022-04-20 10:24:43',7.9868,'Douchen'),(24,1,1,'2022-05-09 22:11:27',1.8174,'Douchen'),(25,3,39,'2022-03-07 00:23:55',9.3551,'Douchen'),(26,1,4,'2022-01-27 11:08:20',5.0202,'Douchen'),(27,3,47,'2022-03-07 22:24:14',2.6793,'Douchen'),(28,2,11,'2022-04-02 23:17:53',0.3784,'Douchen'),(29,1,10,'2022-04-25 14:41:52',2.7964,'Douchen'),(30,3,16,'2022-05-09 07:22:56',7.2407,'Douchen'),(31,3,42,'2022-02-03 11:30:52',0.3096,'Douchen'),(32,1,41,'2022-01-17 22:52:10',5.2843,'Douchen'),(33,3,30,'2022-04-05 03:21:41',7.1109,'Douchen'),(34,1,46,'2022-03-27 07:21:21',9.2292,'Douchen'),(35,2,5,'2022-04-21 21:46:00',5.6963,'Douchen'),(36,2,44,'2022-02-27 14:54:22',3.0085,'Douchen'),(37,3,48,'2022-01-28 08:57:36',2.6381,'Douchen'),(38,1,35,'2022-04-14 10:51:51',5.1534,'Douchen'),(39,1,9,'2022-05-14 05:05:28',5.4239,'Douchen'),(40,1,20,'2022-03-31 21:10:45',9.3193,'Douchen'),(41,3,17,'2022-04-05 01:16:36',9.7245,'Douchen'),(42,3,12,'2022-04-13 03:54:35',4.894,'Douchen'),(43,1,18,'2022-03-05 20:17:51',2.4647,'Douchen'),(44,3,8,'2022-01-14 03:59:49',0.7506,'Douchen'),(45,1,27,'2022-01-14 15:37:13',0.4103,'Douchen'),(46,2,15,'2022-05-10 21:52:42',6.2761,'Douchen'),(47,2,3,'2022-02-15 21:32:44',8.4452,'Douchen'),(48,1,50,'2022-03-10 20:51:00',0.7054,'Douchen'),(49,2,6,'2022-02-10 07:32:23',6.1901,'Douchen'),(50,1,21,'2022-04-12 16:41:45',6.8799,'Douchen');
/*!40000 ALTER TABLE `Historiek` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-24 10:57:34
