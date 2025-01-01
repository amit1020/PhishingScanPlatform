-- Check if the database exists, create it if it doesn't
CREATE DATABASE IF NOT EXISTS `Phishing_Database`;

-- Switch to the newly created or existing database
USE `Phishing_Database`;


-- Phishing_Database.Phishing_Database definition

CREATE TABLE IF NOT EXISTS `Links_Table` (
  `Serial_Number` int NOT NULL AUTO_INCREMENT,
  `purpose` varchar(20) NOT NULL,
  `website_name` varchar(50) NOT NULL,
  `link` varchar(100) NOT NULL,
  `request_type` varchar(10) NOT NULL,
  `description` text,
  `headers` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  ,
  PRIMARY KEY (`Serial_Number`),
  UNIQUE KEY `Phishing_Database_link_IDX` (`link`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;