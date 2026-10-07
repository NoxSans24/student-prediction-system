# `DATABASE_IMPLEMENTATION_SPEC.md`

Dokumen ini menerjemahkan **Database Schema** yang sudah disepakati menjadi aturan implementasi yang siap digunakan ketika project Flask mulai dibuat.

Tujuannya bukan mengubah desain database, tetapi membuat implementasinya lebih konsisten dan aman.

---

# 1. Database Overview

Nama database:

```sql
student_performance_analytics
```

Database terdiri dari 7 tabel utama:

```text
users
students
academic_records
risk_assessments
prediction_results
datasets
dataset_cleaning_logs
```

Relasi utamanya:

```text
users
 ├──< datasets
 └──< dataset_cleaning_logs

students
 ├──< academic_records
 ├──< risk_assessments
 └──< prediction_results

datasets
 └──< dataset_cleaning_logs
```

---

# 2. Database Responsibility

Database tidak bertugas melakukan business logic.

Pembagian tanggung jawab:

```text
Flask Routes
     ↓
Services
     ↓
Database
```

Database bertanggung jawab terhadap:

* menyimpan data
* menjaga integritas data
* menjaga relationship
* unique constraint
* foreign key
* indexing
* persistence

Sedangkan:

* Risk calculation → `risk_service.py`
* Analytics → `analytics_service.py`
* ML → `ml/`
* Data cleaning → `data_cleaning_service.py`
* Insights → `insight_service.py`

---

# 3. Table: `users`

Digunakan untuk authentication dan authorization.

```sql
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
```

## Fields

| Field         | Type         | Rule             |
| ------------- | ------------ | ---------------- |
| id            | INT          | Primary Key      |
| username      | VARCHAR(50)  | Required, Unique |
| email         | VARCHAR(100) | Unique           |
| password_hash | VARCHAR(255) | Required         |
| role          | ENUM         | admin / analyst  |
| created_at    | TIMESTAMP    | Automatic        |
| updated_at    | TIMESTAMP    | Automatic        |

Password **tidak boleh disimpan dalam plaintext**.

---

# 4. User Roles

## Admin

Memiliki akses:

```text
Dashboard
Students CRUD
Analytics
Prediction
Risk
Dataset
Upload Dataset
Cleaning
ML Training
Reports
Settings
```

## Analyst

Memiliki akses:

```text
Dashboard
Students View
Analytics
Prediction
Risk
Dataset Overview
Reports
Settings
```

Authorization tetap dilakukan di backend.

---

# 5. Table: `students`

Menyimpan identitas utama mahasiswa.

```sql
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
```

## Important

`student_id` adalah ID mahasiswa yang digunakan aplikasi.

Contoh:

```text
20240001
20240002
20240003
```

Bukan primary key database.

Primary key tetap:

```text
id
```

---

# 6. Student Identity Rule

`student_id` harus unique.

Contoh yang tidak diperbolehkan:

```text
20240001
20240001
```

Database akan menolak duplicate tersebut.

---

# 7. Table: `academic_records`

Menyimpan performa akademik mahasiswa berdasarkan semester.

```sql
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
```

---

# 8. Academic Record Rule

Satu mahasiswa hanya memiliki satu academic record untuk satu semester.

Valid:

```text
Student A
Semester 1
Semester 2
Semester 3
```

Tidak valid:

```text
Student A
Semester 2
Semester 2
```

Constraint:

```sql
UNIQUE (student_id, semester)
```

menjaga aturan tersebut.

---

# 9. Academic Data Types

| Data        | Type         |
| ----------- | ------------ |
| GPA         | DECIMAL(3,2) |
| Attendance  | DECIMAL(5,2) |
| Assignment  | DECIMAL(5,2) |
| Midterm     | DECIMAL(5,2) |
| Final       | DECIMAL(5,2) |
| Study Hours | DECIMAL(5,2) |

Validasi range tetap dilakukan oleh application/service layer.

Contoh:

```text
GPA       → 0–4
Attendance → 0–100
Scores     → 0–100
Semester   → >= 1
Study hour → >= 0
```

---

# 10. Table: `risk_assessments`

Menyimpan hasil Risk Engine.

```sql
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
```

---

# 11. Risk Assessment Rule

Risk assessment berbeda dengan academic record.

```text
Academic Record
→ data akademik

Risk Assessment
→ interpretasi risiko berdasarkan data
```

Risk Engine menghasilkan:

```text
risk_score
risk_level
main_factors
```

Contoh:

```text
Risk Level: HIGH
Risk Score: 72.50

Main Factors:
- GPA decreased
- Attendance decreased
- Final score decreased
```

---

# 12. Risk History

Tabel risk assessment dirancang untuk memungkinkan histori assessment.

Contoh:

```text
Student A
├── Semester 1 → LOW
├── Semester 2 → MEDIUM
└── Semester 3 → HIGH
```

Karena itu assessment tidak harus menimpa record lama.

---

# 13. Table: `prediction_results`

Menyimpan histori prediksi GPA.

```sql
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
```

---

# 14. Prediction Rule

Prediction tidak harus selalu terkait dengan mahasiswa.

Karena:

```sql
student_id INT NULL
```

maka sistem dapat melakukan:

```text
Prediction untuk mahasiswa
```

atau:

```text
Prediction menggunakan input manual
```

Jika mahasiswa dihapus:

```text
student
    ↓
prediction
```

prediction tetap tersimpan, tetapi:

```text
student_id = NULL
```

karena:

```sql
ON DELETE SET NULL
```

---

# 15. ML Metrics

Prediction menyimpan:

```text
MAE
RMSE
R²
```

Tujuannya agar hasil prediction dapat menunjukkan model yang digunakan dan performanya.

Contoh:

```text
Model
RandomForestRegressor

MAE
0.18

RMSE
0.24

R²
0.82
```

Nilai tersebut harus berasal dari hasil training sebenarnya.

Tidak boleh hardcoded.

---

# 16. Table: `datasets`

Menyimpan metadata dataset yang di-upload.

```sql
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
```

---

# 17. Dataset Status Flow

Status dataset mengikuti lifecycle:

```text
uploaded
    ↓
validated
    ↓
cleaned
    ↓
processed
```

Jika terjadi kegagalan:

```text
failed
```

Visualisasi:

```text
Upload
  ↓
Validation
  ↓
Cleaning
  ↓
Processing
  ↓
Analytics / ML
```

---

# 18. Dataset Rule

File asli tidak boleh dimodifikasi.

Struktur:

```text
data/
├── raw/
│   └── original_dataset.csv
│
├── processed/
│   └── cleaned_dataset.csv
│
└── reports/
```

Prinsip:

```text
RAW ≠ PROCESSED
```

---

# 19. Table: `dataset_cleaning_logs`

Menyimpan hasil proses cleaning.

```sql
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
```

---

# 20. Cleaning Log Rule

Satu dataset dapat mempunyai beberapa cleaning log.

Contoh:

```text
Dataset A
├── Cleaning #1
├── Cleaning #2
└── Cleaning #3
```

Ini memungkinkan histori proses cleaning tetap tersedia.

---

# 21. Foreign Key Map

```text
users.id
 │
 ├───────────────< datasets.uploaded_by
 │
 └───────────────< dataset_cleaning_logs.applied_by


students.id
 │
 ├───────────────< academic_records.student_id
 │
 ├───────────────< risk_assessments.student_id
 │
 └───────────────< prediction_results.student_id


datasets.id
 │
 └───────────────< dataset_cleaning_logs.dataset_id
```

---

# 22. Delete Behavior

## Delete Student

```text
students
   │
   ├── academic_records
   └── risk_assessments
```

Menggunakan:

```sql
ON DELETE CASCADE
```

Artinya record yang bergantung pada student ikut dihapus.

Prediction berbeda:

```text
prediction_results
```

menggunakan:

```sql
ON DELETE SET NULL
```

sehingga histori prediction tetap ada.

---

# 23. Delete Dataset

Jika dataset dihapus:

```text
datasets
   ↓
dataset_cleaning_logs
```

Cleaning logs ikut dihapus karena:

```sql
ON DELETE CASCADE
```

---

# 24. Index Strategy

Index yang sudah ditentukan:

### Students

```sql
INDEX idx_student_name (name)
INDEX idx_student_major (major)
INDEX idx_student_semester (current_semester)
```

Tujuannya mempercepat pencarian/filter mahasiswa.

---

# 25. Unique Constraints

Constraint penting:

```text
users.username
users.email
students.student_id
students(student_id, semester)
```

Tujuannya mencegah duplicate data penting.

---

# 26. Database Validation vs Application Validation

Tidak semua validation diletakkan di database.

### Database

Menjaga:

```text
Primary Key
Foreign Key
Unique
Required fields
Relationship
```

### Application

Menjaga:

```text
GPA range
Attendance range
Score range
Semester validation
Study hours
CSV validation
Data type conversion
Outlier detection
Cleaning rules
```

Pembagian ini membuat sistem lebih fleksibel.

---

# 27. Dataset-to-Database Mapping

Dataset utama:

```text
student_id
name
major
semester
gpa
attendance
assignment_score
midterm_score
final_score
study_hours
```

Ketika dataset diproses:

```text
student_id
name
major
        ↓
students

semester
gpa
attendance
assignment_score
midterm_score
final_score
study_hours
        ↓
academic_records
```

---

# 28. Important Mapping Rule

`student_id` dari CSV bukan langsung menjadi:

```text
academic_records.student_id
```

Karena:

```text
CSV student_id
```

adalah identifier mahasiswa, sedangkan:

```text
academic_records.student_id
```

adalah foreign key ke:

```text
students.id
```

Alurnya:

```text
CSV student_id
      ↓
Cari students.student_id
      ↓
Ambil students.id
      ↓
Simpan ke academic_records.student_id
```

Ini penting agar relationship database tetap benar.

---

# 29. Database Setup Order

Database dibuat dengan urutan:

```text
1. Create database
        ↓
2. users
        ↓
3. students
        ↓
4. academic_records
        ↓
5. risk_assessments
        ↓
6. prediction_results
        ↓
7. datasets
        ↓
8. dataset_cleaning_logs
```

Alasan:

Foreign key membutuhkan tabel parent sudah tersedia.

---

# 30. Seed Data

Untuk development, database membutuhkan minimal:

```text
1 Admin
1 Analyst
```

Contoh konsep:

```text
Admin
username: admin

Analyst
username: analyst
```

Password tetap harus dibuat menggunakan password hashing dari application layer.

Jangan menyimpan password plaintext di `schema.sql`.

---

# 31. Development Seed

Seed juga dapat digunakan untuk:

```text
Students
Academic Records
Risk Assessments
Prediction History
```

Namun data tersebut hanya digunakan untuk development/testing.

Production tidak boleh bergantung pada dummy data.

---

# 32. Initial Database Flow

Saat aplikasi pertama kali dijalankan:

```text
Flask
 ↓
Read .env
 ↓
Connect MySQL
 ↓
Check database
 ↓
Check required tables
 ↓
Application ready
```

Credential database berasal dari environment variable.

Contoh:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_performance_analytics
DB_USER=root
DB_PASSWORD=
```

---

# 33. `.env` Security

`.env` wajib masuk:

```gitignore
.env
```

Jangan commit:

```text
DB_PASSWORD
SECRET_KEY
```

ke GitHub.

---

# 34. Database Connection Layer

File:

```text
database/connection.py
```

Tanggung jawab:

```text
Create connection
Create cursor
Close connection
Handle database connection errors
```

Service tidak boleh membuat koneksi database dengan cara berbeda-beda.

---

# 35. Recommended Connection Flow

```text
Route
 ↓
Service
 ↓
Connection
 ↓
Query
 ↓
Result
 ↓
Service
 ↓
Route/API
```

Contoh:

```text
/api/students
      ↓
students.py
      ↓
student service
      ↓
connection.py
      ↓
MySQL
```

---

# 36. Transaction Rule

Operasi yang terdiri dari beberapa perubahan database harus menggunakan transaction.

Contoh import dataset:

```text
Begin
 ↓
Insert students
 ↓
Insert academic records
 ↓
Commit
```

Jika terjadi error:

```text
Rollback
```

Sehingga tidak terjadi kondisi:

```text
50 students berhasil
20 academic records gagal
```

tanpa kontrol.

---

# 37. Transaction Candidates

Transaction diperlukan terutama untuk:

```text
Dataset import
Dataset cleaning apply
Student + academic record creation
Bulk academic record update
Risk recalculation
```

---

# 38. Query Rule

Hindari:

```python
query = f"SELECT * FROM students WHERE name = '{name}'"
```

Gunakan parameterized query.

Contoh:

```python
query = """
    SELECT *
    FROM students
    WHERE name LIKE %s
"""

cursor.execute(query, (f"%{name}%",))
```

Ini membantu mencegah SQL injection.

---

# 39. Query Responsibility

Route tidak menulis SQL kompleks.

Buruk:

```text
routes/students.py
    ↓
20 SQL queries
```

Lebih baik:

```text
routes/students.py
        ↓
service
        ↓
database layer
```

Dengan demikian route tetap tipis.

---

# 40. Dashboard Data Queries

Database menyediakan data dasar seperti:

### Total Students

```sql
SELECT COUNT(*) AS total_students
FROM students;
```

### Average GPA

```sql
SELECT AVG(gpa) AS average_gpa
FROM academic_records;
```

### Average Attendance

```sql
SELECT AVG(attendance) AS average_attendance
FROM academic_records;
```

### GPA by Major

```sql
SELECT
    s.major,
    AVG(a.gpa) AS average_gpa
FROM students s
JOIN academic_records a
    ON s.id = a.student_id
GROUP BY s.major
ORDER BY average_gpa DESC;
```

---

# 41. GPA Trend Query

```sql
SELECT
    semester,
    AVG(gpa) AS average_gpa
FROM academic_records
GROUP BY semester
ORDER BY semester;
```

Output kemudian digunakan oleh:

```text
Analytics Service
        ↓
Dashboard
        ↓
GPA Trend Chart
```

---

# 42. Risk Query

```sql
SELECT
    risk_level,
    COUNT(*) AS total
FROM risk_assessments
GROUP BY risk_level;
```

Risk calculation tetap dilakukan oleh Risk Engine.

Database hanya menyimpan hasilnya.

---

# 43. Database Does Not Decide Risk

Jangan memasukkan business logic seperti:

```sql
CASE
    WHEN gpa < 2.0 THEN 'high'
    ...
END
```

ke query utama.

Risk rule berada di:

```text
services/risk_service.py
```

Dengan begitu threshold dapat dikonfigurasi.

---

# 44. Database Does Not Train ML

Database hanya menyediakan dataset.

Flow:

```text
MySQL
 ↓
Data Retrieval
 ↓
Pandas
 ↓
Preprocessing
 ↓
Train Model
 ↓
Evaluate
 ↓
Save Model
```

Training tidak dilakukan menggunakan SQL.

---

# 45. Database and Analytics

Analytics menggunakan data database melalui service.

```text
academic_records
        ↓
analytics_service.py
        ↓
aggregate / transform
        ↓
JSON
        ↓
Chart
```

---

# 46. Database and Reports

Report juga tidak langsung membaca database dari route.

```text
Database
 ↓
Services
 ↓
Report Service
 ↓
PDF / Excel / CSV
```

---

# 47. Database Integrity Rules

Sistem harus menjaga:

```text
□ Student ID unique
□ Username unique
□ Email unique
□ One academic record per student/semester
□ Foreign keys valid
□ Required fields tidak NULL
□ Student deletion mengikuti cascade policy
□ Prediction history mengikuti SET NULL
□ Dataset cleaning log memiliki dataset valid
```

---

# 48. Final SQL Setup File

File:

```text
database/schema.sql
```

akan menjadi sumber utama struktur database.

Strukturnya:

```text
CREATE DATABASE
        ↓
USE DATABASE
        ↓
CREATE users
        ↓
CREATE students
        ↓
CREATE academic_records
        ↓
CREATE risk_assessments
        ↓
CREATE prediction_results
        ↓
CREATE datasets
        ↓
CREATE dataset_cleaning_logs
```

---

# 49. Final Database Architecture

```text
                    MySQL
                      │
       ┌──────────────┼──────────────┐
       │              │              │
     Users         Students       Datasets
       │              │              │
       │       ┌──────┼──────┐       │
       │       │      │      │       │
       │   Academic  Risk  Prediction│
       │   Records   Assessments      │
       │                             │
       └──────────────┬──────────────┘
                      │
              Cleaning Logs
```

---

# 50. Database Implementation Checklist

Sebelum masuk coding backend:

```text
□ Database name finalized
□ 7 tables finalized
□ Primary keys finalized
□ Foreign keys finalized
□ Cascade rules finalized
□ Unique constraints finalized
□ Indexes finalized
□ Dataset mapping finalized
□ Role structure finalized
□ Seed strategy finalized
□ .env strategy finalized
□ Transaction rules finalized
□ Parameterized query required
□ Raw dataset remains untouched
```

