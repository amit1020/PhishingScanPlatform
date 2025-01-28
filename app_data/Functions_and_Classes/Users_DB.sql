-- Check if the database exists, create it if it doesn't
CREATE DATABASE IF NOT EXISTS `Phishing_Database`;

-- Switch to the newly created or existing database
USE `Phishing_Database`;

-- Phishing_Database.Links_Table definition
CREATE TABLE IF NOT EXISTS `Links_Table` (
  `Serial_Number` int NOT NULL AUTO_INCREMENT,
  `purpose` varchar(20) NOT NULL,
  `website_name` varchar(50) NOT NULL,
  `link` varchar(100) NOT NULL,
  `request_type` varchar(10) NOT NULL,
  `description` text,
  `headers` varchar(200) NOT NULL,
  PRIMARY KEY (`Serial_Number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- Phishing_Database.Users_Technical_Data_Table definition

CREATE TABLE IF NOT EXISTS `Users_Technical_Data_Table` (
  `userID` varchar(18) DEFAULT NULL,
  `2FA_key` varchar(32) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `2FA_enabled` tinyint(1) NOT NULL,
  `last_login` timestamp NULL DEFAULT NULL,
  `status` enum('active','inactive','banned') NOT NULL DEFAULT 'active',
  UNIQUE KEY `Users_Technical_Data_Table_UNIQUE` (`2FA_key`),
  KEY `Users_Technical_Data_Table_Users_FK` (`userID`),
  CONSTRAINT `Users_Technical_Data_Table_Users_FK` FOREIGN KEY (`userID`) REFERENCES `Users_Table` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




-- Phishing_Database.Users_Table definition
CREATE TABLE IF NOT EXISTS `Users_Table` (
  `userID` varchar(18) NOT NULL,
  `name` varchar(20) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `organization` varchar(100) DEFAULT NULL,
  `country` varchar(39) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `phone_number` varchar(18) NOT NULL,
  `street_address` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `postal_code` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `Users_UNIQUE` (`email`),
  UNIQUE KEY `Users_UNIQUE_1` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


