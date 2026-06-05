
CREATE DATABASE StudentDashboard;
USE StudentDashboard;

CREATE TABLE Students (
 StudentID INT PRIMARY KEY,
 Name VARCHAR(50),
 Department VARCHAR(50),
 Marks INT
);
ALTER TABLE Students
ADD sex VARCHAR(10);

UPDATE Students 
SET sex=Department;
SELECT * FROM Students;