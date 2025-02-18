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



-- Phishing_Database.Users_Table definition
CREATE TABLE IF NOT EXISTS `Users_Table` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `organization` varchar(100) DEFAULT NULL,
  `country` varchar(39) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `phone_number` varchar(18) NOT NULL,
  `street_address` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `postal_code` varchar(20) DEFAULT NULL,
  `2FA_key` varchar(32) NOT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `Users_UNIQUE` (`email`),
  UNIQUE KEY `Users_UNIQUE_1` (`phone_number`),
  UNIQUE KEY `Users_Table_UNIQUE` (`2FA_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




-- Phishing_Database.Users_Technical_Data_Table definition

CREATE TABLE IF NOT EXISTS `Users_Technical_Data_Table` (
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `2FA_enabled` tinyint(1) NOT NULL,
  `last_login` timestamp NULL DEFAULT NULL,
  `status` enum('active','inactive','banned') NOT NULL DEFAULT 'active',
  `userID` int DEFAULT NULL,
  KEY `Users_Technical_Data_Table_Users_Table_FK` (`userID`),
  CONSTRAINT `Users_Technical_Data_Table_Users_Table_FK` FOREIGN KEY (`userID`) REFERENCES `Users_Table` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE IF NOT EXISTS 'API_Table' (
	'api_id' INT auto_increment NOT NULL,
	'api_website_name' varchar(100) NOT NULL,
	'value' VARBINARY(512) NOT NULL,
  'description' TEXT NULL,
	CONSTRAINT API_Table_PK PRIMARY KEY ('api_id')
)ENGINE=InnoDB,DEFAULT CHARSET=utf8mb4,COLLATE=utf8mb4_0900_ai_ci;