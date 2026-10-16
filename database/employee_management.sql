-- Employee Management & HR Analytics System
-- MySQL Database Setup

CREATE DATABASE IF NOT EXISTS employee_management;

USE employee_management;

CREATE TABLE IF NOT EXISTS employees (
    Employee_ID VARCHAR(10) NOT NULL,
    Name VARCHAR(100) NOT NULL,
    DOB DATE DEFAULT NULL,
    DOJ DATE DEFAULT NULL,
    Gender VARCHAR(10) DEFAULT NULL,
    Department VARCHAR(50) DEFAULT NULL,
    Designation VARCHAR(100) DEFAULT NULL,
    Salary DECIMAL(10,2) DEFAULT NULL,
    Contact VARCHAR(15) DEFAULT NULL,
    Email VARCHAR(100) DEFAULT NULL,
    Address VARCHAR(200) DEFAULT NULL,
    PRIMARY KEY (Employee_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS employee_login (
    Employee_ID VARCHAR(10) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    PRIMARY KEY (Employee_ID),
    CONSTRAINT employee_login_ibfk_1
        FOREIGN KEY (Employee_ID)
        REFERENCES employees (Employee_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Verify database tables
SHOW TABLES;
