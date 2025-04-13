-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.6.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for robertodb
CREATE DATABASE IF NOT EXISTS `robertodb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `robertodb`;

-- Dumping structure for table robertodb.all_batches_tab
CREATE TABLE IF NOT EXISTS `all_batches_tab` (
  `Batch_ID` varchar(100) NOT NULL,
  `Sample_ID` varchar(100) NOT NULL,
  `Batch_date` date NOT NULL,
  `Batch_process_time` time DEFAULT NULL,
  PRIMARY KEY (`Batch_ID`),
  KEY `fk_sample_id` (`Sample_ID`),
  CONSTRAINT `fk_sample_id` FOREIGN KEY (`Sample_ID`) REFERENCES `fullbatch_tab` (`Sample_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table robertodb.all_batches_tab: ~0 rows (approximately)

-- Dumping structure for table robertodb.fullbatch_tab
CREATE TABLE IF NOT EXISTS `fullbatch_tab` (
  `Sample_ID` varchar(100) NOT NULL,
  `Nugget_Count` int(10) unsigned NOT NULL,
  `Batch_weight` float NOT NULL,
  `Batch_validity` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Sample_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table robertodb.fullbatch_tab: ~1 rows (approximately)
INSERT INTO `fullbatch_tab` (`Sample_ID`, `Nugget_Count`, `Batch_weight`, `Batch_validity`) VALUES
	('BATCH_001', 3, 1.95, INVALID);

-- Dumping structure for table robertodb.nugget_tab
CREATE TABLE IF NOT EXISTS `nugget_tab` (
  `Nugget_ID` varchar(100) NOT NULL,
  `Sample_ID` varchar(100) NOT NULL,
  `Nugget_weight` float NOT NULL,
  `Nugget_size` float NOT NULL,
  `Nugget_condition` tinyint(1) NOT NULL,
  PRIMARY KEY (`Nugget_ID`),
  KEY `fk_sample` (`Sample_ID`),
  CONSTRAINT `fk_sample` FOREIGN KEY (`Sample_ID`) REFERENCES `fullbatch_tab` (`Sample_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table robertodb.nugget_tab: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
