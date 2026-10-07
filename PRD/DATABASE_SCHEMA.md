1. Tujuan

Database digunakan sebagai sumber data utama untuk Student Performance Analytics.

Struktur database harus mendukung:

Student Management
Academic History
Analytics
GPA Prediction
Risk Analysis
Dataset Management
Reports
Authentication

PRD menetapkan MySQL sebagai database dan membagi aplikasi menjadi Dashboard, Students, Analytics, Prediction, Risk Analysis, Dataset, Reports, dan Settings.

2. Arsitektur Database

Struktur utama:

users
  │
  │
  └── authentication

students
  │
  ├── academic_records
  │
  ├── risk_assessments
  │
  └── prediction_results

datasets
  │
  └── dataset_cleaning_logs

Secara konsep:

                    ┌──────────────┐
                    │    users     │
                    └──────────────┘


┌──────────────┐
│   students   │
└──────┬───────┘
       │
       ├───────────────┐
       │               │
       ▼               ▼
┌──────────────┐  ┌──────────────────┐
│   academic   │  │ risk_assessments │
│   records    │  └──────────────────┘
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ prediction_results│
└──────────────────┘


┌──────────────┐
│   datasets   │
└──────┬───────┘
       │
       ▼
┌────────────────────────┐
│ dataset_cleaning_logs  │
└────────────────────────┘
3. Tabel Database

Untuk tahap awal kita gunakan 7 tabel:

1. users
2. students
3. academic_records
4. risk_assessments
5. prediction_results
6. datasets
7. dataset_cleaning_logs

Catatan: tabel ini adalah rancangan implementasi dari kebutuhan PRD. PRD tidak memberikan schema SQL final, sehingga bagian relationship dan kolom teknis di bawah merupakan desain implementasi, bukan isi eksplisit dari PRD.

4. Table users

Digunakan untuk authentication.

PRD menetapkan dua role:

Admin
Analyst

Admin memiliki akses penuh, sedangkan Analyst dapat melakukan analisis tetapi tidak mengubah dataset utama.

Schema
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    email VARCHAR(100) UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    role ENUM('admin', 'analyst') NOT NULL DEFAULT 'analyst',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
Contoh
username	role
admin	admin
analyst01	analyst

Password tidak disimpan sebagai plaintext. Yang disimpan adalah password_hash.

5. Table students

Menyimpan informasi dasar mahasiswa.

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id VARCHAR(30) NOT NULL UNIQUE,

    name VARCHAR(100) NOT NULL,

    major VARCHAR(100) NOT NULL,

    current_semester INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_student_name (name),

    INDEX idx_student_major (major),

    INDEX idx_student_semester (current_semester)
);
Field
Field	Type	Fungsi
id	INT	Primary key internal
student_id	VARCHAR	ID mahasiswa
name	VARCHAR	Nama
major	VARCHAR	Jurusan
current_semester	INT	Semester aktif
created_at	TIMESTAMP	Waktu dibuat
updated_at	TIMESTAMP	Waktu diperbarui

student_id dibuat UNIQUE supaya satu mahasiswa tidak memiliki ID yang sama.

6. Table academic_records

Ini merupakan tabel yang sangat penting karena menyimpan performa akademik per semester.

Struktur ini memungkinkan kita membuat:

Semester 1 → GPA
Semester 2 → GPA
Semester 3 → GPA
Semester 4 → GPA

yang diperlukan untuk GPA Trend dan academic history. PRD memang meminta GPA history per semester serta faktor attendance, assignment, midterm, final, dan study hours.

Schema
CREATE TABLE academic_records (
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

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_academic_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_student_semester
        UNIQUE (student_id, semester),

    INDEX idx_academic_semester (semester),

    INDEX idx_academic_gpa (gpa)
);
Kenapa menggunakan student_id INT?

Di sini:

students.id
     ↓
academic_records.student_id

students.id adalah primary key internal.

Sedangkan:

students.student_id

adalah ID mahasiswa yang ditampilkan ke user.

Contoh:

students

id = 1
student_id = STD001
name = Muhammad Ihsan

Maka:

academic_records

student_id = 1
semester = 4
gpa = 3.72
7. Unique Semester

Kita menggunakan:

UNIQUE (student_id, semester)

Artinya satu mahasiswa tidak boleh memiliki dua record untuk semester yang sama.

Tidak boleh:

STD001 | Semester 4 | 3.72
STD001 | Semester 4 | 3.50

Tetapi boleh:

STD001 | Semester 1 | 3.20
STD001 | Semester 2 | 3.31
STD001 | Semester 3 | 3.45
STD001 | Semester 4 | 3.72

Ini penting untuk GPA Trend.

8. Table risk_assessments

Menyimpan hasil Risk Analysis.

PRD menetapkan:

LOW
MEDIUM
HIGH

serta faktor seperti GPA, attendance, score trend, study hours, previous GPA, assignment, midterm, dan final performance.

Schema
CREATE TABLE risk_assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    semester INT NOT NULL,

    risk_level ENUM('low', 'medium', 'high') NOT NULL,

    risk_score DECIMAL(5,2),

    main_factors TEXT,

    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_risk_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    INDEX idx_risk_level (risk_level),

    INDEX idx_risk_student (student_id),

    INDEX idx_risk_semester (semester)
);
9. Kenapa Ada risk_score?

PRD hanya menentukan level:

LOW
MEDIUM
HIGH

tetapi belum menentukan bagaimana level tersebut dihitung.

Karena itu kita menyediakan:

risk_score

sebagai tempat menyimpan skor numerik apabila nanti Risk Engine menggunakan scoring system.

Contoh belum menjadi aturan final:

Risk Score = 82.50
Risk Level = HIGH

Threshold-nya akan ditentukan dalam RISK_ENGINE_SPEC.md.

10. Table prediction_results

Digunakan untuk menyimpan hasil prediksi GPA.

PRD menentukan input prediction:

Semester
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours

dan output berupa predicted GPA serta model yang digunakan.

Schema
CREATE TABLE prediction_results (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NULL,

    semester INT NOT NULL,

    attendance DECIMAL(5,2) NOT NULL,

    assignment_score DECIMAL(5,2) NOT NULL,

    midterm_score DECIMAL(5,2) NOT NULL,

    final_score DECIMAL(5,2) NOT NULL,

    study_hours DECIMAL(5,2) NOT NULL,

    predicted_gpa DECIMAL(3,2) NOT NULL,

    performance_category VARCHAR(30),

    model_name VARCHAR(100) NOT NULL,

    mae DECIMAL(10,4),

    rmse DECIMAL(10,4),

    r2 DECIMAL(10,4),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prediction_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE SET NULL,

    INDEX idx_prediction_student (student_id),

    INDEX idx_prediction_model (model_name)
);
11. Kenapa student_id Boleh NULL?

Prediction bisa dilakukan untuk:

Mahasiswa yang sudah ada
Student:
STD001

Input:
Attendance
Assignment
Midterm
Final
Study Hours

atau untuk:

Simulasi mahasiswa baru

User hanya memasukkan:

Semester
Attendance
Assignment
Midterm
Final
Study Hours

tanpa memilih mahasiswa.

Karena itu:

student_id INT NULL

lebih fleksibel.

12. Model Information

Field:

model_name

menyimpan model yang digunakan.

Contoh:

Linear Regression
Random Forest Regressor
Gradient Boosting Regressor

PRD memang menetapkan minimal tiga model tersebut dan membandingkannya menggunakan MAE, RMSE, dan R².

13. Table datasets

Tabel ini digunakan untuk mencatat dataset yang di-upload.

PRD meminta Dataset Management dengan CSV upload, preview, jumlah rows/columns, missing values, duplicate, data types, dan cleaning.

Schema
CREATE TABLE datasets (
    id INT AUTO_INCREMENT PRIMARY KEY,

    dataset_name VARCHAR(150) NOT NULL,

    original_filename VARCHAR(255) NOT NULL,

    file_path VARCHAR(500),

    total_rows INT DEFAULT 0,

    total_columns INT DEFAULT 0,

    missing_values INT DEFAULT 0,

    duplicate_rows INT DEFAULT 0,

    status ENUM(
        'uploaded',
        'validated',
        'cleaned',
        'processed',
        'failed'
    ) DEFAULT 'uploaded',

    uploaded_by INT,

    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dataset_user
        FOREIGN KEY (uploaded_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);
14. Table dataset_cleaning_logs

Digunakan untuk menyimpan hasil proses cleaning.

PRD meminta cleaning report seperti:

Missing values
Duplicates
Invalid GPA
Invalid attendance
Invalid score
Total records cleaned

dan user dapat melihat perubahan sebelum menerapkan cleaning.

Schema
CREATE TABLE dataset_cleaning_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,

    dataset_id INT NOT NULL,

    missing_values_found INT DEFAULT 0,

    duplicates_found INT DEFAULT 0,

    invalid_gpa INT DEFAULT 0,

    invalid_attendance INT DEFAULT 0,

    invalid_scores INT DEFAULT 0,

    incorrect_data_types INT DEFAULT 0,

    outliers_found INT DEFAULT 0,

    total_records_cleaned INT DEFAULT 0,

    cleaning_method TEXT,

    applied_by INT,

    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cleaning_dataset
        FOREIGN KEY (dataset_id)
        REFERENCES datasets(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_cleaning_user
        FOREIGN KEY (applied_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);
15. ERD

Struktur finalnya:

┌────────────────────┐
│       users        │
├────────────────────┤
│ PK id              │
│ username           │
│ email              │
│ password_hash      │
│ role               │
└───────┬────────────┘
        │
        │ 1:N
        ▼
┌────────────────────┐
│      datasets      │
├────────────────────┤
│ PK id              │
│ dataset_name       │
│ original_filename  │
│ file_path          │
│ total_rows         │
│ total_columns      │
│ missing_values     │
│ duplicate_rows     │
│ status             │
│ FK uploaded_by     │
└────────┬───────────┘
         │
         │ 1:N
         ▼
┌────────────────────────┐
│ dataset_cleaning_logs  │
├────────────────────────┤
│ PK id                  │
│ FK dataset_id          │
│ missing_values_found   │
│ duplicates_found       │
│ invalid_gpa            │
│ invalid_attendance     │
│ invalid_scores         │
│ outliers_found         │
│ total_records_cleaned  │
│ FK applied_by          │
└────────────────────────┘


┌────────────────────┐
│      students      │
├────────────────────┤
│ PK id              │
│ student_id UNIQUE  │
│ name               │
│ major              │
│ current_semester   │
└──────┬─────────────┘
       │
       ├──────────────────────┐
       │                      │
       │ 1:N                  │ 1:N
       ▼                      ▼
┌────────────────────┐  ┌────────────────────┐
│ academic_records   │  │ risk_assessments   │
├────────────────────┤  ├────────────────────┤
│ PK id              │  │ PK id              │
│ FK student_id      │  │ FK student_id      │
│ semester           │  │ semester           │
│ gpa                │  │ risk_level         │
│ attendance         │  │ risk_score         │
│ assignment_score   │  │ main_factors       │
│ midterm_score      │  └────────────────────┘
│ final_score        │
│ study_hours        │
│ academic_status    │
└────────────────────┘


       students
           │
           │ 1:N
           ▼
┌────────────────────────┐
│   prediction_results   │
├────────────────────────┤
│ PK id                  │
│ FK student_id          │
│ semester               │
│ attendance             │
│ assignment_score       │
│ midterm_score          │
│ final_score            │
│ study_hours            │
│ predicted_gpa          │
│ performance_category   │
│ model_name             │
│ mae                    │
│ rmse                   │
│ r2                     │
└────────────────────────┘
16. Relationship Summary
Parent	Child	Relationship
users	datasets	1:N
users	dataset_cleaning_logs	1:N
datasets	dataset_cleaning_logs	1:N
students	academic_records	1:N
students	risk_assessments	1:N
students	prediction_results	1:N
17. Query untuk Dashboard

Dengan schema ini Dashboard dapat mengambil data aktual.

Total Students
SELECT COUNT(*) AS total_students
FROM students;
Average GPA
SELECT AVG(gpa) AS average_gpa
FROM academic_records;
Average Attendance
SELECT AVG(attendance) AS average_attendance
FROM academic_records;
At-Risk Students
SELECT COUNT(DISTINCT student_id) AS at_risk
FROM risk_assessments
WHERE risk_level IN ('medium', 'high');
GPA by Major
SELECT
    s.major,
    AVG(a.gpa) AS average_gpa
FROM students s
JOIN academic_records a
    ON s.id = a.student_id
GROUP BY s.major
ORDER BY average_gpa DESC;
GPA Trend
SELECT
    semester,
    AVG(gpa) AS average_gpa
FROM academic_records
GROUP BY semester
ORDER BY semester;

Query-query tersebut nantinya menjadi sumber data untuk KPI dan chart Dashboard yang memang ditentukan dalam Dashboard.md.

18. SQL Schema Lengkap

Untuk implementasi nanti kita dapat membuat:

database/
└── schema.sql

dengan isi:

CREATE DATABASE IF NOT EXISTS student_performance_analytics;

USE student_performance_analytics;

-- USERS
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'analyst') NOT NULL DEFAULT 'analyst',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- STUDENTS
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(100) NOT NULL,
    current_semester INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_student_name (name),
    INDEX idx_student_major (major),
    INDEX idx_student_semester (current_semester)
);

-- ACADEMIC RECORDS
CREATE TABLE academic_records (
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_academic_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_student_semester
        UNIQUE (student_id, semester)
);

-- RISK ASSESSMENTS
CREATE TABLE risk_assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    semester INT NOT NULL,
    risk_level ENUM('low', 'medium', 'high') NOT NULL,
    risk_score DECIMAL(5,2),
    main_factors TEXT,
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_risk_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);

-- PREDICTION RESULTS
CREATE TABLE prediction_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NULL,
    semester INT NOT NULL,
    attendance DECIMAL(5,2) NOT NULL,
    assignment_score DECIMAL(5,2) NOT NULL,
    midterm_score DECIMAL(5,2) NOT NULL,
    final_score DECIMAL(5,2) NOT NULL,
    study_hours DECIMAL(5,2) NOT NULL,
    predicted_gpa DECIMAL(3,2) NOT NULL,
    performance_category VARCHAR(30),
    model_name VARCHAR(100) NOT NULL,
    mae DECIMAL(10,4),
    rmse DECIMAL(10,4),
    r2 DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prediction_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE SET NULL
);

-- DATASETS
CREATE TABLE datasets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dataset_name VARCHAR(150) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    total_rows INT DEFAULT 0,
    total_columns INT DEFAULT 0,
    missing_values INT DEFAULT 0,
    duplicate_rows INT DEFAULT 0,

    status ENUM(
        'uploaded',
        'validated',
        'cleaned',
        'processed',
        'failed'
    ) DEFAULT 'uploaded',

    uploaded_by INT,

    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dataset_user
        FOREIGN KEY (uploaded_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);

-- DATASET CLEANING LOGS
CREATE TABLE dataset_cleaning_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dataset_id INT NOT NULL,
    missing_values_found INT DEFAULT 0,
    duplicates_found INT DEFAULT 0,
    invalid_gpa INT DEFAULT 0,
    invalid_attendance INT DEFAULT 0,
    invalid_scores INT DEFAULT 0,
    incorrect_data_types INT DEFAULT 0,
    outliers_found INT DEFAULT 0,
    total_records_cleaned INT DEFAULT 0,
    cleaning_method TEXT,
    applied_by INT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cleaning_dataset
        FOREIGN KEY (dataset_id)
        REFERENCES datasets(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_cleaning_user
        FOREIGN KEY (applied_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);
19. Status Database

Dengan ini:

Bagian	Status
Student table	Selesai
Academic records	Selesai
Risk table	Selesai
Prediction table	Selesai
User/auth table	Selesai
Dataset table	Selesai
Cleaning log	Selesai
Relationship	Selesai
Dashboard query foundation	Selesai
Risk threshold	Belum ditentukan
Academic category threshold	Belum ditentukan
