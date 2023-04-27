-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: pms
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `name` varchar(20) DEFAULT NULL,
  `password` varchar(15) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('Thota Visali','anisha','206156@siddharthamahila.ac.in'),('Thota Visali','anisha','thotavisali@gmail.com'),('Thota Visali','anisha','206116@siddharthamahila.ac.in');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patientname` varchar(20) DEFAULT NULL,
  `mobileno` varchar(15) NOT NULL,
  `age` int DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`mobileno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES ('nafiya','7730967557',20,'gandhinagar'),('sukanya','81068610',65,'hyderabad'),('fhg','8106861000',54,'gh'),('anisha','81068610548',54,'fgjmmk'),('visali','8106861060',19,'kathunivanipalem'),('oiioijo','810686106016',54,'jhui'),('fhg','8106861067',54,'gh'),('sukanya','8106861085',14,'jghjgyug'),('visali','8529333678',95,'vijayawada'),('sravani','9381499122',20,'vijayawada'),('kkhjkh','965412388',75,'jiuytyutty'),('kkhjkh','965412389',65,'jiuytyutty');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `records` (
  `rid` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `mobileno` varchar(15) DEFAULT NULL,
  `doctorname` varchar(30) DEFAULT NULL,
  `purposetovisit` varchar(30) DEFAULT NULL,
  `appointmenttime` varchar(40) DEFAULT NULL,
  `checkin` datetime DEFAULT NULL,
  `checkout` datetime DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`rid`),
  KEY `mobileno` (`mobileno`),
  CONSTRAINT `records_ibfk_1` FOREIGN KEY (`mobileno`) REFERENCES `patients` (`mobileno`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
INSERT INTO `records` VALUES (1,'sravani','9381499122','jhghjg','hjgyug','2.11','2023-04-25 19:35:29','2023-04-25 19:35:32','2023-04-24 18:03:58'),(2,'sukanya','8106861085','visali','stomach pain','9.00am','2023-04-27 15:21:07','2023-04-27 15:21:20','2023-04-24 18:03:58'),(3,'anisha','81068610548',NULL,NULL,NULL,NULL,NULL,'2023-04-24 18:03:58'),(4,'fhg','8106861067',NULL,NULL,NULL,NULL,NULL,'2023-04-25 19:35:42'),(5,'nafiya','7730967557',NULL,NULL,NULL,NULL,NULL,'2023-04-26 12:56:35'),(6,'visali','8106861060','Jaya Sri','mental issue','12:00pm','2023-04-27 13:19:39','2023-04-27 13:20:20','2023-04-27 13:15:21'),(7,'oiioijo','810686106016',NULL,NULL,NULL,NULL,NULL,'2023-04-27 15:23:54');
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test` (
  `mobileno` varchar(15) DEFAULT NULL,
  `testname` varchar(30) DEFAULT NULL,
  `testresult` varchar(40) DEFAULT NULL,
  KEY `mobileno` (`mobileno`),
  CONSTRAINT `test_ibfk_1` FOREIGN KEY (`mobileno`) REFERENCES `patients` (`mobileno`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES ('965412389','blood','postive'),('8106861000','ccf','kj0i'),('810686106016','ghjku','anisha'),('8106861085','thyroid test','positive'),('81068610548','thyroid test','iji');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-27 16:55:30
