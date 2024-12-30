IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'Phishing_Database')
BEGIN
	CREATE DATABASE Phishing_Database;
END;

USE Phishing_Database;



CREATE TABLE [APIs_Table] (
  [Serial_Number] int NOT NULL IDENTITY(1,1),
  [purpose] varchar(20) NOT NULL,
  [website_name] varchar(50) NOT NULL,
  [link] varchar(100) NOT NULL,
  [request_type] varchar(10) NOT NULL,
  [description] text,
  PRIMARY KEY ([Serial_Number]),
  UNIQUE ([link])
);