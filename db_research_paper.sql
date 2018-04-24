-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: paper_research
-- ------------------------------------------------------
-- Server version	5.7.19-log

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

--
-- Table structure for table `admin_comment`
--

DROP TABLE IF EXISTS `admin_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_comment` (
  `comment_message` varchar(150) DEFAULT NULL,
  `admin_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  `submission_id` int(11) NOT NULL,
  KEY `idx_admin_comment` (`admin_id`),
  KEY `idx_admin_comment_0` (`paper_id`),
  KEY `idx_admin_comment_1` (`submission_id`),
  CONSTRAINT `admin_comment_id` FOREIGN KEY (`admin_id`) REFERENCES `admin_information` (`admin_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `admin_paper_comment_id` FOREIGN KEY (`paper_id`) REFERENCES `paper_creation` (`paper_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `admin_submission_comment_id` FOREIGN KEY (`submission_id`) REFERENCES `submission_of_paper` (`submission_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_comment`
--

LOCK TABLES `admin_comment` WRITE;
/*!40000 ALTER TABLE `admin_comment` DISABLE KEYS */;
INSERT INTO `admin_comment` VALUES ('Good Content',9,16,20),('Great paper',9,18,22),('Do changes',9,20,24),('do  as expert said',9,21,25),('Good',9,20,32);
/*!40000 ALTER TABLE `admin_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_information`
--

DROP TABLE IF EXISTS `admin_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_information` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `mobile_no` varchar(10) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `password` varchar(40) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `skills` varchar(100) NOT NULL,
  `profile_pic` varchar(100) NOT NULL,
  `date_of_birth` varchar(12) NOT NULL,
  `date_registration` date NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_information`
--

LOCK TABLES `admin_information` WRITE;
/*!40000 ALTER TABLE `admin_information` DISABLE KEYS */;
INSERT INTO `admin_information` VALUES (9,'Dattesh','L','Jain','8798789565','dd@gmail.com','1234','Male','skillskill','Default.jpg','2000-02-20','2017-09-10');
/*!40000 ALTER TABLE `admin_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_notification`
--

DROP TABLE IF EXISTS `admin_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_notification` (
  `index_no` int(11) NOT NULL AUTO_INCREMENT,
  `n_id` int(11) NOT NULL,
  PRIMARY KEY (`index_no`),
  KEY `idx_admin_notification` (`n_id`),
  CONSTRAINT `fk_admin_notification` FOREIGN KEY (`n_id`) REFERENCES `notification` (`n_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_notification`
--

LOCK TABLES `admin_notification` WRITE;
/*!40000 ALTER TABLE `admin_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcement`
--

DROP TABLE IF EXISTS `announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `announcement` (
  `announcement_id` int(11) NOT NULL AUTO_INCREMENT,
  `announcement_details` varchar(500) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `related_to` varchar(15) NOT NULL,
  `announcements_date` date NOT NULL,
  PRIMARY KEY (`announcement_id`),
  KEY `idx_announcement` (`admin_id`),
  CONSTRAINT `admin_announcement_id` FOREIGN KEY (`admin_id`) REFERENCES `admin_information` (`admin_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcement`
--

LOCK TABLES `announcement` WRITE;
/*!40000 ALTER TABLE `announcement` DISABLE KEYS */;
INSERT INTO `announcement` VALUES (3,'You have to submit Paper on or before 28/10',9,'USER','2017-10-18'),(4,'Check papers as fast as you can',9,'EXPERT','2017-10-18'),(6,'Thank You for joining us',9,'USER and EXPERT','2017-10-18'),(8,'ashjasd',9,'Reviewer','2017-11-12');
/*!40000 ALTER TABLE `announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author` (
  `author_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `designation` varchar(300) NOT NULL,
  `city` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `department` varchar(100) NOT NULL,
  `institute` varchar(150) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `university` varchar(100) DEFAULT NULL,
  `area_of_interset` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`author_id`),
  KEY `idx_author` (`user_id`),
  CONSTRAINT `user_author_id_1` FOREIGN KEY (`user_id`) REFERENCES `user_information` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
INSERT INTO `author` VALUES (2,'Sathwara','sathwara@ymail.com','BSc in chemistry','Ahmedabad','India','Chemical','LDCE',NULL,NULL,NULL),(3,'Sathwara','sathwara@ymail.com','BSc in chemistry','Ahmedabad','India','Chemical','LDCE',32,NULL,NULL),(4,'Shailesh','ssha@gmail.com','Bsc in Maths','Ahmedabad','India','Maths','LDCE',32,NULL,NULL);
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contactus`
--

DROP TABLE IF EXISTS `contactus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contactus` (
  `c_id` int(11) NOT NULL AUTO_INCREMENT,
  `mobile` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `message` varchar(300) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactus`
--

LOCK TABLES `contactus` WRITE;
/*!40000 ALTER TABLE `contactus` DISABLE KEYS */;
INSERT INTO `contactus` VALUES (3,'7878787878','herin@gmail.com','asjkhasjkdhsakjdhsjakhdjsakdhksjhdsajkdhasjkshds','Herin'),(4,'8511218967','prince@gmail.com','ashkdjhsadkjhsjkdhasjkhdjkshjkdhsajdhsjakdhjksahdkjashdjkashkdsajkdhkasdkssdsadhsakjdhsajdjksdhkhsdsdksdkjhsdjkshajkadhsjkdhshdsakjds','Prince');
/*!40000 ALTER TABLE `contactus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `countries` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `countryName` varchar(45) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=251 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countries`
--

LOCK TABLES `countries` WRITE;
/*!40000 ALTER TABLE `countries` DISABLE KEYS */;
INSERT INTO `countries` VALUES (1,'Andorra'),(2,'United Arab Emirates'),(3,'Afghanistan'),(4,'Antigua and Barbuda'),(5,'Anguilla'),(6,'Albania'),(7,'Armenia'),(8,'Angola'),(9,'Antarctica'),(10,'Argentina'),(11,'American Samoa'),(12,'Austria'),(13,'Australia'),(14,'Aruba'),(15,'Åland'),(16,'Azerbaijan'),(17,'Bosnia and Herzegovina'),(18,'Barbados'),(19,'Bangladesh'),(20,'Belgium'),(21,'Burkina Faso'),(22,'Bulgaria'),(23,'Bahrain'),(24,'Burundi'),(25,'Benin'),(26,'Saint Barthélemy'),(27,'Bermuda'),(28,'Brunei'),(29,'Bolivia'),(30,'Bonaire'),(31,'Brazil'),(32,'Bahamas'),(33,'Bhutan'),(34,'Bouvet Island'),(35,'Botswana'),(36,'Belarus'),(37,'Belize'),(38,'Canada'),(39,'Cocos [Keeling] Islands'),(40,'Democratic Republic of the Congo'),(41,'Central African Republic'),(42,'Republic of the Congo'),(43,'Switzerland'),(44,'Ivory Coast'),(45,'Cook Islands'),(46,'Chile'),(47,'Cameroon'),(48,'China'),(49,'Colombia'),(50,'Costa Rica'),(51,'Cuba'),(52,'Cape Verde'),(53,'Curacao'),(54,'Christmas Island'),(55,'Cyprus'),(56,'Czechia'),(57,'Germany'),(58,'Djibouti'),(59,'Denmark'),(60,'Dominica'),(61,'Dominican Republic'),(62,'Algeria'),(63,'Ecuador'),(64,'Estonia'),(65,'Egypt'),(66,'Western Sahara'),(67,'Eritrea'),(68,'Spain'),(69,'Ethiopia'),(70,'Finland'),(71,'Fiji'),(72,'Falkland Islands'),(73,'Micronesia'),(74,'Faroe Islands'),(75,'France'),(76,'Gabon'),(77,'United Kingdom'),(78,'Grenada'),(79,'Georgia'),(80,'French Guiana'),(81,'Guernsey'),(82,'Ghana'),(83,'Gibraltar'),(84,'Greenland'),(85,'Gambia'),(86,'Guinea'),(87,'Guadeloupe'),(88,'Equatorial Guinea'),(89,'Greece'),(90,'South Georgia and the South Sandwich Islands'),(91,'Guatemala'),(92,'Guam'),(93,'Guinea-Bissau'),(94,'Guyana'),(95,'Hong Kong'),(96,'Heard Island and McDonald Islands'),(97,'Honduras'),(98,'Croatia'),(99,'Haiti'),(100,'Hungary'),(101,'Indonesia'),(102,'Ireland'),(103,'Israel'),(104,'Isle of Man'),(105,'India'),(106,'British Indian Ocean Territory'),(107,'Iraq'),(108,'Iran'),(109,'Iceland'),(110,'Italy'),(111,'Jersey'),(112,'Jamaica'),(113,'Jordan'),(114,'Japan'),(115,'Kenya'),(116,'Kyrgyzstan'),(117,'Cambodia'),(118,'Kiribati'),(119,'Comoros'),(120,'Saint Kitts and Nevis'),(121,'North Korea'),(122,'South Korea'),(123,'Kuwait'),(124,'Cayman Islands'),(125,'Kazakhstan'),(126,'Laos'),(127,'Lebanon'),(128,'Saint Lucia'),(129,'Liechtenstein'),(130,'Sri Lanka'),(131,'Liberia'),(132,'Lesotho'),(133,'Lithuania'),(134,'Luxembourg'),(135,'Latvia'),(136,'Libya'),(137,'Morocco'),(138,'Monaco'),(139,'Moldova'),(140,'Montenegro'),(141,'Saint Martin'),(142,'Madagascar'),(143,'Marshall Islands'),(144,'Macedonia'),(145,'Mali'),(146,'Myanmar [Burma]'),(147,'Mongolia'),(148,'Macao'),(149,'Northern Mariana Islands'),(150,'Martinique'),(151,'Mauritania'),(152,'Montserrat'),(153,'Malta'),(154,'Mauritius'),(155,'Maldives'),(156,'Malawi'),(157,'Mexico'),(158,'Malaysia'),(159,'Mozambique'),(160,'Namibia'),(161,'New Caledonia'),(162,'Niger'),(163,'Norfolk Island'),(164,'Nigeria'),(165,'Nicaragua'),(166,'Netherlands'),(167,'Norway'),(168,'Nepal'),(169,'Nauru'),(170,'Niue'),(171,'New Zealand'),(172,'Oman'),(173,'Panama'),(174,'Peru'),(175,'French Polynesia'),(176,'Papua New Guinea'),(177,'Philippines'),(178,'Pakistan'),(179,'Poland'),(180,'Saint Pierre and Miquelon'),(181,'Pitcairn Islands'),(182,'Puerto Rico'),(183,'Palestine'),(184,'Portugal'),(185,'Palau'),(186,'Paraguay'),(187,'Qatar'),(188,'Réunion'),(189,'Romania'),(190,'Serbia'),(191,'Russia'),(192,'Rwanda'),(193,'Saudi Arabia'),(194,'Solomon Islands'),(195,'Seychelles'),(196,'Sudan'),(197,'Sweden'),(198,'Singapore'),(199,'Saint Helena'),(200,'Slovenia'),(201,'Svalbard and Jan Mayen'),(202,'Slovakia'),(203,'Sierra Leone'),(204,'San Marino'),(205,'Senegal'),(206,'Somalia'),(207,'Suriname'),(208,'South Sudan'),(209,'São Tomé and Príncipe'),(210,'El Salvador'),(211,'Sint Maarten'),(212,'Syria'),(213,'Swaziland'),(214,'Turks and Caicos Islands'),(215,'Chad'),(216,'French Southern Territories'),(217,'Togo'),(218,'Thailand'),(219,'Tajikistan'),(220,'Tokelau'),(221,'East Timor'),(222,'Turkmenistan'),(223,'Tunisia'),(224,'Tonga'),(225,'Turkey'),(226,'Trinidad and Tobago'),(227,'Tuvalu'),(228,'Taiwan'),(229,'Tanzania'),(230,'Ukraine'),(231,'Uganda'),(232,'U.S. Minor Outlying Islands'),(233,'United States'),(234,'Uruguay'),(235,'Uzbekistan'),(236,'Vatican City'),(237,'Saint Vincent and the Grenadines'),(238,'Venezuela'),(239,'British Virgin Islands'),(240,'U.S. Virgin Islands'),(241,'Vietnam'),(242,'Vanuatu'),(243,'Wallis and Futuna'),(244,'Samoa'),(245,'Kosovo'),(246,'Yemen'),(247,'Mayotte'),(248,'South Africa'),(249,'Zambia'),(250,'Zimbabwe');
/*!40000 ALTER TABLE `countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `editorial_board`
--

DROP TABLE IF EXISTS `editorial_board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `editorial_board` (
  `guest_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `description` varchar(500) NOT NULL,
  `profile` varchar(150) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`guest_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `editorial_board`
--

LOCK TABLES `editorial_board` WRITE;
/*!40000 ALTER TABLE `editorial_board` DISABLE KEYS */;
INSERT INTO `editorial_board` VALUES (7,'Rohan','M','Garg','ME from IIT Bombay PhD from IISC Banglore','Default.jpg','ProfessorAtICE'),(11,'Sathwara','M','Gaurang','adskjsadasjdjskahdas','Default.jpg','Chemistry');
/*!40000 ALTER TABLE `editorial_board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expert_comment`
--

DROP TABLE IF EXISTS `expert_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `expert_comment` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_message` varchar(500) DEFAULT NULL,
  `date_of_comment` date NOT NULL,
  `expert_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `submission_id` int(11) NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `idx_expert_comment` (`expert_id`),
  KEY `idx_expert_comment_1` (`paper_id`),
  KEY `idx_expert_comment_2` (`status_id`),
  KEY `idx_expert_comment_0` (`submission_id`),
  CONSTRAINT `expert_comment_id` FOREIGN KEY (`expert_id`) REFERENCES `expert_information` (`expert_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `paper_commnet_id` FOREIGN KEY (`paper_id`) REFERENCES `paper_creation` (`paper_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `status_comment_id` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `submission_expert_id` FOREIGN KEY (`submission_id`) REFERENCES `submission_of_paper` (`submission_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expert_comment`
--

LOCK TABLES `expert_comment` WRITE;
/*!40000 ALTER TABLE `expert_comment` DISABLE KEYS */;
INSERT INTO `expert_comment` VALUES (1,'This paper is absolutely perfect just add some more keyword..','2017-10-18',17,14,4,18),(2,NULL,'2017-10-18',17,15,2,19),(3,NULL,'2017-10-18',18,14,2,18),(4,'Perfect','2017-10-18',18,15,4,19),(5,NULL,'2017-10-18',19,14,3,18),(6,NULL,'2017-10-18',19,15,3,19),(7,NULL,'2017-10-18',17,16,2,20),(8,NULL,'2017-10-18',17,17,2,21),(9,NULL,'2017-10-18',17,18,2,22),(10,NULL,'2017-10-18',17,19,2,23),(11,NULL,'2017-10-18',18,16,2,20),(12,NULL,'2017-10-18',18,17,2,21),(13,NULL,'2017-10-18',18,18,2,22),(14,NULL,'2017-10-18',18,19,2,23),(15,'This is insane','2017-10-18',19,16,5,20),(16,'akhdaskhaskhds','2017-10-18',19,17,6,21),(17,NULL,'2017-10-18',19,18,2,22),(18,'change your abstract','2017-10-18',19,19,6,23),(19,'Do some changes','2017-10-18',17,20,6,24),(20,'Do some changes','2017-10-18',17,21,6,25),(21,'Add some more content do more research ','2017-10-18',18,20,6,24),(22,'less content','2017-10-18',18,21,6,25),(23,'add more content and make proper introduction','2017-10-18',19,20,6,24),(24,'remove content which are not relevant to the topic','2017-10-18',19,21,6,25),(25,'perfect','2017-10-19',17,20,4,32),(26,'still some changes need to do','2017-10-19',18,20,6,32),(27,'Nice ','2017-10-19',19,20,4,32),(28,'Good','2017-10-20',17,24,4,27),(29,'Nice content','2017-10-20',19,24,4,27),(30,NULL,'2017-10-20',18,24,2,27);
/*!40000 ALTER TABLE `expert_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expert_information`
--

DROP TABLE IF EXISTS `expert_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `expert_information` (
  `expert_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `mobile_no` varchar(10) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `date_of_birth` varchar(12) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `skills` varchar(100) NOT NULL,
  `total_experience` int(11) NOT NULL,
  `experience_in_words` varchar(150) NOT NULL,
  `profile_pic` varchar(100) NOT NULL,
  `date_registration` date NOT NULL,
  `expert_cv` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`expert_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expert_information`
--

LOCK TABLES `expert_information` WRITE;
/*!40000 ALTER TABLE `expert_information` DISABLE KEYS */;
INSERT INTO `expert_information` VALUES (17,'Tushar','A','Chapanery','7878787878','tac@ldce.ac.in','1234','2017-09-12','Male','IOT and MCWC',5,'Assistant Professor at LD College Of Engineering','Default.jpg','2017-09-19',''),(18,'Bhavesh','A','Oza','7878787878','bao@ldce.ac.in','1234','2017-10-09','Male','Data Structure,Data Minning,DBMS',5,'Assistant Professor at LD College Of Engineering','Default.jpg','2017-10-18','GateSyllabus.pdf'),(19,'Aakansha','S','Saxsena','8798789565','aakansha@gmail.com','1234','2017-10-14','Male','Digital Electronics',1,'Assistant Professor at LD College Of Engineering','Apple_3d.jpg','2017-10-18','');
/*!40000 ALTER TABLE `expert_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expert_notification`
--

DROP TABLE IF EXISTS `expert_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `expert_notification` (
  `index_no` int(11) NOT NULL AUTO_INCREMENT,
  `n_id` int(11) NOT NULL,
  `expert_id` int(11) NOT NULL,
  PRIMARY KEY (`index_no`),
  KEY `idx_expert_notification` (`n_id`),
  KEY `idx_expert_notification_0` (`expert_id`),
  CONSTRAINT `fk_expert_notification` FOREIGN KEY (`n_id`) REFERENCES `notification` (`n_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_expert_notification_0` FOREIGN KEY (`expert_id`) REFERENCES `expert_information` (`expert_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expert_notification`
--

LOCK TABLES `expert_notification` WRITE;
/*!40000 ALTER TABLE `expert_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `expert_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issue`
--

DROP TABLE IF EXISTS `issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `issue` (
  `issue_id` int(11) NOT NULL AUTO_INCREMENT,
  `issue_name` varchar(30) NOT NULL,
  `volume_id` int(11) NOT NULL,
  `issue_no` int(11) NOT NULL,
  PRIMARY KEY (`issue_id`),
  KEY `idx_issue` (`volume_id`),
  CONSTRAINT `volume_issue_id` FOREIGN KEY (`volume_id`) REFERENCES `volume` (`volume_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue`
--

LOCK TABLES `issue` WRITE;
/*!40000 ALTER TABLE `issue` DISABLE KEYS */;
INSERT INTO `issue` VALUES (5,'January to April',5,1),(6,'May to August',5,2),(7,'September to Decemeber',5,3),(8,'January to April',6,1),(9,'May to August',6,2),(10,'September to Decemeber',6,3),(11,'January to April',7,1),(12,'May to August',7,2);
/*!40000 ALTER TABLE `issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification` (
  `n_id` int(11) NOT NULL AUTO_INCREMENT,
  `n_message` varchar(150) NOT NULL,
  PRIMARY KEY (`n_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (1,'Admin has allocated new papers to you.'),(2,'User has resubmitted Paper.'),(3,'Reviewer has commented on a Paper.'),(4,'User has uploaded new paper.'),(5,'User has submitted CRC Copy'),(6,'Admin has published your paper');
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper_comment`
--

DROP TABLE IF EXISTS `paper_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paper_comment` (
  `comment_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  `submission_id` int(11) NOT NULL,
  KEY `idx_paper_comment` (`comment_id`),
  KEY `idx_paper_comment_0` (`paper_id`),
  KEY `idx_paper_comment_1` (`submission_id`),
  CONSTRAINT `comment_paper_id` FOREIGN KEY (`comment_id`) REFERENCES `expert_comment` (`comment_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `paper_comment_admin_id` FOREIGN KEY (`paper_id`) REFERENCES `paper_creation` (`paper_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `paper_comment_submission_id` FOREIGN KEY (`submission_id`) REFERENCES `submission_of_paper` (`submission_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper_comment`
--

LOCK TABLES `paper_comment` WRITE;
/*!40000 ALTER TABLE `paper_comment` DISABLE KEYS */;
INSERT INTO `paper_comment` VALUES (1,14,18),(7,16,20),(19,20,24),(21,20,24),(23,20,24),(20,21,25),(22,21,25),(24,21,25),(25,20,32),(27,20,32),(28,24,27),(29,24,27);
/*!40000 ALTER TABLE `paper_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper_creation`
--

DROP TABLE IF EXISTS `paper_creation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paper_creation` (
  `paper_id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` date NOT NULL,
  `path` varchar(100) NOT NULL,
  `status_allocation` varchar(10) NOT NULL,
  `user_id` int(11) NOT NULL,
  `issue_id` int(11) DEFAULT NULL,
  `status_id` int(11) NOT NULL,
  PRIMARY KEY (`paper_id`),
  KEY `idx_paper_creation` (`user_id`),
  KEY `idx_paper_creation_0` (`issue_id`),
  KEY `idx_paper_creation_1` (`status_id`),
  CONSTRAINT `issue_paper_id` FOREIGN KEY (`issue_id`) REFERENCES `issue` (`issue_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `status_paper_id` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `user_paper_id` FOREIGN KEY (`user_id`) REFERENCES `user_information` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper_creation`
--

LOCK TABLES `paper_creation` WRITE;
/*!40000 ALTER TABLE `paper_creation` DISABLE KEYS */;
INSERT INTO `paper_creation` VALUES (14,'2017-10-18','integration_formulas.pdf','true',32,12,9),(15,'2017-10-18','GateSyllabus.pdf','true',32,12,9),(16,'2017-10-18','An Innovative Solution for Cloud Computing Authentication- Grids of EAP-TLS Smart Cards.pdf','true',32,NULL,4),(17,'2017-10-18','cloud-computing-identity-management.pdf','true',32,NULL,8),(18,'2017-10-18','Security and Cloud Computing InterCloud Identity Management Infrastructure.pdf','true',32,NULL,8),(19,'2017-10-18','Three-Phase Cross-Cloud Federation Model The Cloud SSO Authentication.pdf','true',32,NULL,8),(20,'2017-10-18','Efficient Resource Management for Cloud Computing Environments.pdf','true',32,NULL,4),(21,'2017-10-18','Energy Aware Consolidation for Cloud Computing.pdf','true',32,NULL,6),(23,'2017-10-18','Energy-Aware-CloudResourceAllocation-FGCS2011.pdf','false',32,NULL,1),(24,'2017-10-18','Green Cloud Computing.pdf','true',32,12,9),(25,'2017-10-18','GreenCloud-EuroPar2011.pdf','true',32,NULL,7),(26,'2017-10-18','PowerNap Eliminating Server Idle Power.pdf','false',32,NULL,1),(27,'2017-11-12','ICSI-Admit-Card.pdf','false',32,NULL,1);
/*!40000 ALTER TABLE `paper_creation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper_keyword`
--

DROP TABLE IF EXISTS `paper_keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paper_keyword` (
  `submission_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  `keyword_name` varchar(100) DEFAULT NULL,
  KEY `idx_paper_keyword_0` (`submission_id`),
  KEY `idx_paper_keyword_1` (`paper_id`),
  CONSTRAINT `paper_keyword_id` FOREIGN KEY (`paper_id`) REFERENCES `paper_creation` (`paper_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `submission_keyword_id` FOREIGN KEY (`submission_id`) REFERENCES `submission_of_paper` (`submission_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper_keyword`
--

LOCK TABLES `paper_keyword` WRITE;
/*!40000 ALTER TABLE `paper_keyword` DISABLE KEYS */;
INSERT INTO `paper_keyword` VALUES (18,14,NULL),(18,14,NULL),(18,14,NULL),(19,15,NULL),(19,15,NULL),(19,15,NULL),(20,16,NULL),(20,16,NULL),(20,16,NULL),(21,17,NULL),(21,17,NULL),(21,17,NULL),(22,18,NULL),(22,18,NULL),(22,18,NULL),(23,19,NULL),(23,19,NULL),(23,19,NULL),(23,19,NULL),(24,20,NULL),(24,20,NULL),(24,20,NULL),(24,20,NULL),(24,20,NULL),(25,21,NULL),(25,21,NULL),(25,21,NULL),(25,21,NULL),(26,23,NULL),(26,23,NULL),(26,23,NULL),(26,23,NULL),(27,24,NULL),(27,24,NULL),(27,24,NULL),(27,24,NULL),(27,24,NULL),(28,25,NULL),(28,25,NULL),(28,25,NULL),(29,26,NULL),(29,26,NULL),(29,26,NULL),(32,20,NULL),(32,20,NULL),(32,20,NULL),(34,27,NULL),(34,27,NULL),(34,27,NULL),(34,27,NULL);
/*!40000 ALTER TABLE `paper_keyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper_of_expert`
--

DROP TABLE IF EXISTS `paper_of_expert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paper_of_expert` (
  `expert_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  KEY `idx_paper_of_expert` (`expert_id`),
  KEY `idx_paper_of_expert_0` (`paper_id`),
  KEY `idx_paper_of_expert_1` (`status_id`),
  CONSTRAINT `expert_paper_id` FOREIGN KEY (`expert_id`) REFERENCES `expert_information` (`expert_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `paper_expert_id` FOREIGN KEY (`paper_id`) REFERENCES `paper_creation` (`paper_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `status_expert_id` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper_of_expert`
--

LOCK TABLES `paper_of_expert` WRITE;
/*!40000 ALTER TABLE `paper_of_expert` DISABLE KEYS */;
INSERT INTO `paper_of_expert` VALUES (17,14,4),(18,14,2),(19,14,3),(17,15,2),(18,15,4),(19,15,3),(17,16,2),(18,16,2),(19,16,5),(17,17,2),(18,17,2),(19,17,6),(17,18,2),(18,18,2),(19,18,2),(17,19,2),(18,19,2),(19,19,6),(17,20,4),(18,20,6),(19,20,4),(17,21,6),(18,21,6),(19,21,6),(17,24,4),(18,24,2),(19,24,4),(17,25,7),(18,25,7),(19,25,7);
/*!40000 ALTER TABLE `paper_of_expert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site_wide_announcement`
--

DROP TABLE IF EXISTS `site_wide_announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `site_wide_announcement` (
  `an_id` int(11) NOT NULL AUTO_INCREMENT,
  `date_announcement` date NOT NULL,
  `description` varchar(500) NOT NULL,
  PRIMARY KEY (`an_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_wide_announcement`
--

LOCK TABLES `site_wide_announcement` WRITE;
/*!40000 ALTER TABLE `site_wide_announcement` DISABLE KEYS */;
INSERT INTO `site_wide_announcement` VALUES (7,'2017-10-18','News1 and News2'),(8,'2017-10-18','News3 and News4'),(9,'2017-10-18','News5 and News6'),(10,'2017-10-18','News7 and News8'),(11,'2017-10-18','News9 and News10'),(12,'2017-10-18','News11 and News12'),(14,'2017-10-18','News13 and News14'),(15,'2017-10-18','News15 and News16'),(16,'2017-10-18','News17 and News18');
/*!40000 ALTER TABLE `site_wide_announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `status_id` int(11) NOT NULL AUTO_INCREMENT,
  `status_name` varchar(50) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (1,'WithAuthor'),(2,'Accept'),(3,'Reject'),(4,'AcceptWithComment'),(5,'RejectWithComment'),(6,'WithReviewer'),(7,'WithEditor'),(8,'CRC'),(9,'Published');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subject` (
  `subject_id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(100) NOT NULL,
  `track_id` int(11) NOT NULL,
  PRIMARY KEY (`subject_id`),
  KEY `idx_subject` (`track_id`),
  CONSTRAINT `track_subject_id` FOREIGN KEY (`track_id`) REFERENCES `track` (`track_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (15,'CloudAuthentication',20),(16,'CloudComputing',20),(17,'CloudDataStorage',20),(18,'CloudEnergy',20),(19,'CloudLoadBalancing',20),(20,'CloudScheduling',20);
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submission_of_paper`
--

DROP TABLE IF EXISTS `submission_of_paper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `submission_of_paper` (
  `submission_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `abstract` varchar(2000) NOT NULL,
  `last_modified_date` date NOT NULL,
  `path` varchar(100) NOT NULL,
  `track_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  PRIMARY KEY (`submission_id`),
  KEY `idx_submission_of_paper` (`track_id`),
  KEY `idx_submission_of_paper_0` (`paper_id`),
  KEY `idx_submission_of_paper_1` (`subject_id`),
  CONSTRAINT `paper_submission_id` FOREIGN KEY (`paper_id`) REFERENCES `paper_creation` (`paper_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `subject_submission_id` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `track_submission_id` FOREIGN KEY (`track_id`) REFERENCES `track` (`track_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission_of_paper`
--

LOCK TABLES `submission_of_paper` WRITE;
/*!40000 ALTER TABLE `submission_of_paper` DISABLE KEYS */;
INSERT INTO `submission_of_paper` VALUES (18,'A Layered Security Approach for Cloud Computing Infrastructure','This paper introduces a practical security model\r\nbased on key security considerations by looking at a number\r\nof infrastructure aspects of Cloud Computing such as SaaS,\r\nUtility, Web, Platform and Managed Services, Service\r\ncommerce platforms and Internet Integration which was\r\nintroduced with a concise literature review. The purpose of\r\nthis paper is to offer a macro level solution for identified\r\ncommon infrastructure security requirements. This model\r\nwith a number of emerged patterns can be applied to\r\ninfrastructure aspect of Cloud Computing as a proposed\r\nshared security approach in system development life cycle\r\nfocusing on the plan-built-run scope.','2017-10-18','integration_formulas.pdf',20,14,15),(19,'An Identity-Based Security Infrastructure for Cloud Environments','This paper presents a novel security infrastructure\r\nfor deploying and using service-oriented Cloud applications\r\nsecurely without having to face the complexity associated with\r\ncertificate management. The proposal is based on an identitybased\r\ncryptographic approach that offers an independent setup\r\nof security domains and does not require a trust hierarchy\r\ncompared to other identity-based cryptographic systems. The\r\nservice URLs can be used as public keys, such that creating\r\na secure connection to a service is very simple. A comparison\r\nbetween traditional approaches and identity-based cryptography\r\nwith respect to data transfer requirements is presented.','2017-10-18','GateSyllabus.pdf',20,15,15),(20,'An Innovative Solution for Cloud Computing Authentication: Grids of EAP-TLS Smart Cards','The increase of authenticating solutions based on\r\nRADIUS servers questions the complexity of their\r\nadministration whose security and confidentiality are often at\r\nfault especially within Cloud Computing architectures. More\r\nspecifically, it raises the concern of server administration in a\r\nsecure environment for both the granting access’ company and\r\nits clients. This paper aims to solve this issue by proposing an\r\ninnovative paradigm based on a grid of smart cards built on a\r\ncontext of SSL smart cards. We believe that EAP-TLS server\r\nsmart cards offer the security and the simplicity required for\r\nan administration based on distributed servers. We specify the\r\ndesign of a RADIUS server in which EAP messages are fully\r\nprocessed by SSL smart cards. We present the scalability of\r\nthis server linked to smart card grids whose distributed\r\ncomputation manages the concurrence of numerous\r\nauthenticating sessions. Lastly, we relate the details of the first\r\nexperimental results obtained with the RADIUS server and an\r\narray composed of 32 Java cards, and demonstrate the\r\nfeasibility and prospective scalability of this architecture.','2017-10-18','An Innovative Solution for Cloud Computing Authentication- Grids of EAP-TLS Smart Cards.pdf',20,16,15),(21,'Cloud Computing Identity Management','Most cloud vendors have a simplified\r\nproprietary IDM solution with shortcomings\r\nthat have to be understood. The challenge in\r\nthis area is that there are considerable efforts\r\ntowards outsourcing the IDM that gave birth\r\nto the concept of identity-as-a-service (IaaS)\r\n[1]. IaaS vendors focus on comprehensive,\r\ninteroperable and quick-to-deploy solutions.','2017-10-18','cloud-computing-identity-management.pdf',20,17,15),(22,'Security and Cloud Computing: InterCloud Identity Management Infrastructure','Cloud Computing is becoming one of the most\r\nimportant topics in the IT world. Several challenges are being\r\nraised from the adoption of this computational paradigm\r\nincluding security, privacy, and federation. This paper aims\r\nto introduce new concepts in cloud computing and security,\r\nfocusing on heterogeneous and federated scenarios.We present a\r\nreference architecture able to address the Identity Management\r\n(IdM) problem in the InterCloud context and show how it can\r\nbe successfully applied to manage the authentication needed\r\namong clouds for the federation establishment.','2017-10-18','Security and Cloud Computing InterCloud Identity Management Infrastructure.pdf',20,18,16),(23,'Three-Phase Cross-Cloud Federation Model: The Cloud SSO Authentication','Cloud federation aims to cost-effective assets and\r\nresources optimization among heterogeneous environments\r\nwhere clouds can cooperate together with the goal of obtaining\r\n“unbounded” computation resources, hence new business opportunities.\r\nThis paper describes an architecture for the federation\r\nestablishment, where clouds that need external resources\r\nask to federated clouds the renting of extra physical resources.\r\nOur architecture introduces a new module named Cross-Cloud\r\nFederation Manager including three agents (Discovery, Matchmaking\r\nand Authentication). In this work, we specifically focus\r\non the authentication agent, which is responsible for a secure\r\nfederation. To address such problem we propose a technical\r\nsolution based on the IdP/SP model along with the SAML\r\ntechnology.','2017-10-18','Three-Phase Cross-Cloud Federation Model The Cloud SSO Authentication.pdf',20,19,15),(24,'Efficient Resource Management for Cloud Computing Environments','Cloud becomes popular, the dependence on power also\r\nincreases. In 2005, the data centers consume 1.2% of\r\nthe U.S. total electricity usage. And it’s projected to\r\ndouble every 5 years.','2017-10-18','Efficient Resource Management for Cloud Computing Environments.pdf',20,20,18),(25,'Energy Aware Consolidation for Cloud Computing','Consolidation of applications in cloud computing environments\r\npresents a significant opportunity for energy\r\noptimization. As a first step toward enabling energy efficient\r\nconsolidation, we study the inter-relationships between\r\nenergy consumption, resource utilization, and performance\r\nof consolidated workloads. The study reveals\r\nthe energy performance trade-offs for consolidation and\r\nshows that optimal operating points exist. We model the\r\nconsolidation problem as a modified bin packing problem\r\nand illustrate it with an example. Finally, we outline\r\nthe challenges in finding effective solutions to the consolidation\r\nproblem.','2017-10-18','Energy Aware Consolidation for Cloud Computing.pdf',20,21,18),(26,'Energy-Aware Resource Allocation Heuristics for Efficient Management of Data Centers for Cloud Computing','Cloud computing oers utility-oriented IT services to users worldwide. Based on a pay-as-you-go model, it enables\r\nhosting of pervasive applications from consumer, scientic, and business domains. However, data centers hosting Cloud\r\napplications consume huge amounts of electrical energy, contributing to high operational costs and carbon footprints to\r\nthe environment. Therefore, we need Green Cloud computing solutions that can not only save energy for the environment\r\nbut also reduce operational costs. In this paper, we dene an architectural framework and principles for energy-ecient\r\nCloud computing. Based on this architecture, we present a vision, challenges, and resource provisioning and allocation\r\nalgorithms for energy-ecient management of Cloud computing environments. The proposed energy-aware allocation\r\nheuristics provision data center resources to client applications in a way that improves energy eciency of the data center,\r\nwhile delivering the negotiated Quality of Service (QoS). ','2017-10-18','Energy-Aware-CloudResourceAllocation-FGCS2011.pdf',20,23,18),(27,'Green Cloud Computing: Balancing Energy in Processing, Storage and Transport','Network-based cloud computing is rapidly\r\nexpanding as an alternative to conventional office-based\r\ncomputing. As cloud computing becomes more widespread,\r\nthe energy consumption of the network and computing\r\nresources that underpin the cloud will grow. This is happening\r\nat a time when there is increasing attention being paid to the\r\nneed to manage energy consumption across the entire\r\ninformation and communications technology (ICT) sector.\r\nWhile data center energy use has received much attention\r\nrecently, there has been less attention paid to the energy\r\nconsumption of the transmission and switching networks that\r\nare key to connecting users to the cloud. In this paper, we\r\npresent an analysis of energy consumption in cloud computing.\r\nThe analysis considers both public and private clouds, and\r\nincludes energy consumption in switching and transmission as\r\nwell as data processing and data storage. We show that energy\r\nconsumption in transport and switching can be a significant\r\npercentage of total energy consumption in cloud computing.\r\nCloud computing can enable more energy-efficient use of\r\ncomputing power, especially when the computing tasks are of\r\nlow intensity or infrequent. However, under some circumstances\r\ncloud computing can consume more energy than\r\nconventional computing where each user performs all computing\r\non their own personal computer (PC).','2017-10-18','Green Cloud Computing.pdf',20,24,18),(28,'Green Cloud Framework For Improving Carbon Eciency of Clouds','The energy eciency of ICT has become a major issue with\r\nthe growing demand of Cloud Computing. More and more companies\r\nare investing in building large datacenters to host Cloud services. These\r\ndatacenters not only consume huge amount of energy but are also very\r\ncomplex in the infrastructure itself. Many studies have been proposed to\r\nmake these datacenter energy ecient using technologies such as virtual-\r\nization and consolidation. Still, these solutions are mostly cost driven and\r\nthus, do not directly address the critical impact on the environmental\r\nsustainability in terms of CO2 emissions. Hence, in this work, we propose\r\na user-oriented Cloud architectural framework, i.e. Carbon Aware Green\r\nCloud Architecture, which addresses this environmental problem from\r\nthe overall usage of Cloud Computing resources. We also present a case\r\nstudy on IaaS providers. Finally, we present future research directions to\r\nenable the wholesome carbon eciency of Cloud Computing.','2017-10-18','GreenCloud-EuroPar2011.pdf',20,25,18),(29,'PowerNap: Eliminating Server Idle Power','Data center power consumption is growing to unprecedented\r\nlevels: the EPA estimates U.S. data centers will consume\r\n100 billion kilowatt hours annually by 2011. Much of\r\nthis energy is wasted in idle systems: in typical deployments,\r\nserver utilization is below 30%, but idle servers still consume\r\n60% of their peak power draw. Typical idle periods—\r\nthough frequent—last seconds or less, confounding simple\r\nenergy-conservation approaches.\r\nIn this paper, we propose PowerNap, an energy-conservation\r\napproach where the entire system transitions rapidly between\r\na high-performance active state and a near-zeropower\r\nidle state in response to instantaneous load. Rather\r\nthan requiring fine-grained power-performance states and\r\ncomplex load-proportional operation from each system component,\r\nPowerNap instead calls for minimizing idle power\r\nand transition time, which are simpler optimization goals.\r\nBased on the PowerNap concept, we develop requirements\r\nand outline mechanisms to eliminate idle power waste in enterprise\r\nblade servers. Because PowerNap operates in lowefficiency\r\nregions of current blade center power supplies, we\r\nintroduce the Redundant Array for Inexpensive Load Sharing\r\n(RAILS), a power provisioning approach that provides\r\nhigh conversion efficiency across the entire range of Power-\r\nNap’s power demands. Using utilization traces collected\r\nfrom enterprise-scale commercial deployments, we demonstrate\r\nthat, together, PowerNap and RAILS reduce average\r\nserver power consumption by 74%.','2017-10-18','PowerNap Eliminating Server Idle Power.pdf',20,26,18),(30,'A Layered Security Approach for Cloud Computing Infrastructure','This paper introduces a practical security model\r\nbased on key security considerations by looking at a number\r\nof infrastructure aspects of Cloud Computing such as SaaS,\r\nUtility, Web, Platform and Managed Services, Service\r\ncommerce platforms and Internet Integration which was\r\nintroduced with a concise literature review. The purpose of\r\nthis paper is to offer a macro level solution for identified\r\ncommon infrastructure security requirements. This model\r\nwith a number of emerged patterns can be applied to\r\ninfrastructure aspect of Cloud Computing as a proposed\r\nshared security approach in system development life cycle\r\nfocusing on the plan-built-run scope.','2017-10-18','A Layered Security Approach for Cloud Computing Infrastructure.pdf',20,14,15),(31,'An Identity-Based Security Infrastructure for Cloud Environments','This paper presents a novel security infrastructure\r\nfor deploying and using service-oriented Cloud applications\r\nsecurely without having to face the complexity associated with\r\ncertificate management. The proposal is based on an identitybased\r\ncryptographic approach that offers an independent setup\r\nof security domains and does not require a trust hierarchy\r\ncompared to other identity-based cryptographic systems. The\r\nservice URLs can be used as public keys, such that creating\r\na secure connection to a service is very simple. A comparison\r\nbetween traditional approaches and identity-based cryptography\r\nwith respect to data transfer requirements is presented.','2017-10-18','An Identity-Based Security Infrastructure for Cloud Environments.pdf',20,15,15),(32,'Efficient Resource Management for Cloud Computing Environments','Cloud becomes popular, the dependence on power also\r\nincreases. In 2005, the data centers consume 1.2% of\r\nthe U.S. total electricity usage. And it’s projected to\r\ndouble every 5 years.','2017-10-19','Efficient Resource Management for Cloud Computing Environments.pdf',20,20,16),(33,'Green Cloud Computing: Balancing Energy in Processing, Storage and Transport','Network-based cloud computing is rapidly\r\nexpanding as an alternative to conventional office-based\r\ncomputing. As cloud computing becomes more widespread,\r\nthe energy consumption of the network and computing\r\nresources that underpin the cloud will grow. This is happening\r\nat a time when there is increasing attention being paid to the\r\nneed to manage energy consumption across the entire\r\ninformation and communications technology (ICT) sector.\r\nWhile data center energy use has received much attention\r\nrecently, there has been less attention paid to the energy\r\nconsumption of the transmission and switching networks that\r\nare key to connecting users to the cloud. In this paper, we\r\npresent an analysis of energy consumption in cloud computing.\r\nThe analysis considers both public and private clouds, and\r\nincludes energy consumption in switching and transmission as\r\nwell as data processing and data storage. We show that energy\r\nconsumption in transport and switching can be a significant\r\npercentage of total energy consumption in cloud computing.\r\nCloud computing can enable more energy-efficient use of\r\ncomputing power, especially when the computing tasks are of\r\nlow intensity or infrequent. However, under some circumstances\r\ncloud computing can consume more energy than\r\nconventional computing where each user performs all computing\r\non their own personal computer (PC).','2017-10-18','Green Cloud Computing.pdf',20,24,18),(34,'DEMO','askjdhsjkahkasdhkjahsdjkhas','2017-11-12','ICSI-Admit-Card.pdf',20,27,18);
/*!40000 ALTER TABLE `submission_of_paper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `track`
--

DROP TABLE IF EXISTS `track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `track` (
  `track_id` int(11) NOT NULL AUTO_INCREMENT,
  `track_name` varchar(30) NOT NULL,
  PRIMARY KEY (`track_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `track`
--

LOCK TABLES `track` WRITE;
/*!40000 ALTER TABLE `track` DISABLE KEYS */;
INSERT INTO `track` VALUES (20,'Cloud');
/*!40000 ALTER TABLE `track` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_author`
--

DROP TABLE IF EXISTS `user_author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_author` (
  `author_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `primary_author` varchar(10) DEFAULT NULL,
  KEY `idx_user_author` (`author_id`),
  KEY `idx_user_author_0` (`paper_id`),
  KEY `idx_user_author_1` (`user_id`),
  CONSTRAINT `fk_user_author` FOREIGN KEY (`author_id`) REFERENCES `author` (`author_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_author_0` FOREIGN KEY (`paper_id`) REFERENCES `paper_creation` (`paper_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_author_1` FOREIGN KEY (`user_id`) REFERENCES `user_information` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_author`
--

LOCK TABLES `user_author` WRITE;
/*!40000 ALTER TABLE `user_author` DISABLE KEYS */;
INSERT INTO `user_author` VALUES (4,27,32,NULL);
/*!40000 ALTER TABLE `user_author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_briefcase`
--

DROP TABLE IF EXISTS `user_briefcase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_briefcase` (
  `user_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  KEY `idx_user_briefcase` (`user_id`),
  KEY `idx_user_briefcase_0` (`paper_id`),
  CONSTRAINT `paper_briefcase_id` FOREIGN KEY (`paper_id`) REFERENCES `paper_creation` (`paper_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `user_briefcase_id` FOREIGN KEY (`user_id`) REFERENCES `user_information` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_briefcase`
--

LOCK TABLES `user_briefcase` WRITE;
/*!40000 ALTER TABLE `user_briefcase` DISABLE KEYS */;
INSERT INTO `user_briefcase` VALUES (32,14);
/*!40000 ALTER TABLE `user_briefcase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_information`
--

DROP TABLE IF EXISTS `user_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_information` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) DEFAULT NULL,
  `middle_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `mobile_no` varchar(10) DEFAULT NULL,
  `email_id` varchar(50) NOT NULL,
  `password` varchar(30) DEFAULT NULL,
  `date_of_birth` varchar(12) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `biodata` varchar(150) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `profile_pic` varchar(100) DEFAULT NULL,
  `date_registration` date NOT NULL,
  `address_1` varchar(100) DEFAULT NULL,
  `address_2` varchar(100) DEFAULT NULL,
  `address_3` varchar(100) DEFAULT NULL,
  `pincode` int(11) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `salution` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_information`
--

LOCK TABLES `user_information` WRITE;
/*!40000 ALTER TABLE `user_information` DISABLE KEYS */;
INSERT INTO `user_information` VALUES (32,'Vatsal','Rajeshkumar','Soni','8511218967','sonivatsal111@gmail.com','1234','2017-01-17','Male','','Student','https://lh6.googleusercontent.com/-rDklrNz19Ww/AAAAAAAAAAI/AAAAAAAAAJI/vZvccxNc5UQ/photo.jpg','2017-10-18','G-301 Swaminarayan Park-2 Flat','','',380007,'India',NULL),(33,'Harsh','','Shah','9099499731','harsh@gmail.com','1234','','Male','','Student','Default.jpg','2018-04-17','','','',0,'Italy','Mr.');
/*!40000 ALTER TABLE `user_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_notification`
--

DROP TABLE IF EXISTS `user_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_notification` (
  `index_no` int(11) NOT NULL AUTO_INCREMENT,
  `n_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`index_no`),
  KEY `idx_user_notification` (`n_id`),
  KEY `idx_user_notification_0` (`user_id`),
  CONSTRAINT `fk_user_notification` FOREIGN KEY (`n_id`) REFERENCES `notification` (`n_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_notification_0` FOREIGN KEY (`user_id`) REFERENCES `user_information` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_notification`
--

LOCK TABLES `user_notification` WRITE;
/*!40000 ALTER TABLE `user_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volume`
--

DROP TABLE IF EXISTS `volume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `volume` (
  `volume_id` int(11) NOT NULL AUTO_INCREMENT,
  `volume_name` varchar(30) NOT NULL,
  PRIMARY KEY (`volume_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volume`
--

LOCK TABLES `volume` WRITE;
/*!40000 ALTER TABLE `volume` DISABLE KEYS */;
INSERT INTO `volume` VALUES (5,'2015'),(6,'2016'),(7,'2017');
/*!40000 ALTER TABLE `volume` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'paper_research'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-24 17:05:56
