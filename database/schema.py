import mysql.connector
from mysql.connector import Error
from config import Config

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'analyst') NOT NULL DEFAULT 'analyst',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(100) NOT NULL,
    current_semester INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_student_name (name),
    INDEX idx_student_major (major),
    INDEX idx_student_semester (current_semester)
);

CREATE TABLE IF NOT EXISTS academic_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    semester INT NOT NULL,
    gpa DECIMAL(3,2) NOT NULL,
    attendance DECIMAL(5,2) NOT NULL,
    assignment_score DECIMAL(5,2) NOT NULL,
    midterm_score DECIMAL(5,2) NOT NULL,
    final_score DECIMAL(5,2) NOT NULL,
    study_hours DECIMAL(5,2) NOT NULL,
    academic_status VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_semester (student_id, semester),
    INDEX idx_semester (semester),
    INDEX idx_gpa (gpa)
);

CREATE TABLE IF NOT EXISTS risk_assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH') NOT NULL,
    gpa_risk DECIMAL(3,2),
    attendance_risk DECIMAL(3,2),
    score_trend_risk DECIMAL(3,2),
    study_hours_risk DECIMAL(3,2),
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    INDEX idx_risk_level (risk_level),
    INDEX idx_assessment_date (assessment_date)
);

CREATE TABLE IF NOT EXISTS prediction_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    semester INT NOT NULL,
    predicted_gpa DECIMAL(3,2) NOT NULL,
    actual_gpa DECIMAL(3,2),
    model_used VARCHAR(50) NOT NULL,
    mae DECIMAL(5,4),
    rmse DECIMAL(5,4),
    r_squared DECIMAL(5,4),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    INDEX idx_prediction_date (prediction_date)
);

CREATE TABLE IF NOT EXISTS datasets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_path VARCHAR(500),
    rows_count INT,
    columns_count INT,
    status ENUM('uploaded', 'processed', 'error') DEFAULT 'uploaded',
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_upload_date (upload_date)
);

CREATE TABLE IF NOT EXISTS dataset_cleaning_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dataset_id INT NOT NULL,
    action VARCHAR(100),
    rows_affected INT,
    columns_affected INT,
    details JSON,
    cleaning_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
    INDEX idx_cleaning_date (cleaning_date)
);
"""

def init_database():
    """Initialize database and create tables"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE}")
        cursor.execute(f"USE {Config.MYSQL_DATABASE}")
        
        # Create tables
        for statement in SCHEMA_SQL.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        connection.commit()
        print(f"[OK] Database '{Config.MYSQL_DATABASE}' initialized successfully")
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"[ERROR] Database initialization error: {e}")
        raise

if __name__ == '__main__':
    init_database()
