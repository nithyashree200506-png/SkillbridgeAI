-- SkillBridge AI Database Schema
-- Create Database
CREATE DATABASE IF NOT EXISTS skillbridge_db;
USE skillbridge_db;

-- Table 1: Student
CREATE TABLE IF NOT EXISTS student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    cgpa FLOAT NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Resume
CREATE TABLE IF NOT EXISTS resume (
    resume_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    resume_name VARCHAR(255) NOT NULL,
    resume_score FLOAT DEFAULT 0,
    placement_score FLOAT DEFAULT 0,
    skills TEXT,
    extracted_text LONGTEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE
);

-- Default Admin User (Password: admin123)
-- Password hash generated via Werkzeug scrypt/pbkdf2
INSERT IGNORE INTO student (id, name, email, password, department, year, cgpa, role) 
VALUES (1, 'System Admin', 'admin@skillbridge.ai', 'scrypt:32768:8:1$uJ8Tz2VpQ9xW$1d7a31eb24b07fbdfc6999a0e69b5fa4905caea24a2e5885c3453b52d9a33bb58c35bd28b76c8cbf6ea7d9bb6cfd15024ca0f9ecbfbfbd9ef6d787042a9b31d8', 'Administration', 4, 10.0, 'admin');
