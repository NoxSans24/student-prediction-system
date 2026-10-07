Student Performance Analytics — Data Specification
1. Tujuan

Dokumen ini mendefinisikan struktur data yang digunakan oleh Student Performance Analytics.

Data menjadi fondasi untuk:

CSV / Database
      ↓
Data Validation
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Prediction
      ↓
Risk Analysis
      ↓
Dashboard / Report

Alur tersebut sesuai dengan data flow pada PRD.

2. Sumber Data

Aplikasi akan mendukung dua sumber utama:

CSV

Digunakan untuk:

upload dataset
import data
data cleaning
preprocessing
analisis awal
MySQL

Digunakan sebagai database utama aplikasi untuk:

data mahasiswa
data akademik
riwayat GPA
hasil risk analysis
data yang telah dibersihkan
3. Struktur Dataset Utama

Dataset mahasiswa menggunakan struktur berikut:

Column	Type	Required	Keterangan
student_id	VARCHAR(30)	Yes	ID unik mahasiswa
name	VARCHAR(100)	Yes	Nama mahasiswa
major	VARCHAR(100)	Yes	Jurusan
semester	INT	Yes	Semester aktif
gpa	DECIMAL(3,2)	Yes	GPA mahasiswa
attendance	DECIMAL(5,2)	Yes	Persentase kehadiran
assignment_score	DECIMAL(5,2)	Yes	Nilai tugas
midterm_score	DECIMAL(5,2)	Yes	Nilai UTS
final_score	DECIMAL(5,2)	Yes	Nilai UAS
study_hours	DECIMAL(5,2)	Yes	Jam belajar
academic_status	VARCHAR(30)	No	Status akademik
risk_level	VARCHAR(20)	No	Level risiko
Contoh CSV
student_id,name,major,semester,gpa,attendance,assignment_score,midterm_score,final_score,study_hours
STD001,Muhammad Ihsan H.,Informatics,4,3.72,94,88,86,91,18
STD002,Andi Pratama,Information System,3,2.81,76,74,71,78,10
STD003,Budi Santoso,Informatics,5,2.21,68,61,64,59,6
STD004,Siti Rahma,Computer Science,4,3.45,89,84,82,87,15

Nama student_id, gpa, attendance, study_hours, dan score fields adalah implementasi teknis dari kebutuhan PRD yang secara eksplisit meminta Student ID, GPA, attendance, study hours, assignment, midterm, dan final score.

4. Data Validation

Sebelum data masuk ke database, sistem harus melakukan validasi.

4.1 Student ID

Aturan:

Tidak boleh kosong
Harus unik
Tidak boleh duplicate

Contoh valid:

STD001
STD002
STD003

Contoh invalid:

STD001
STD001
4.2 Name
Required
String
Tidak boleh kosong
4.3 Major
Required
String
Tidak boleh kosong

Contoh:

Informatics
Information System
Computer Science
Management
5. Semester

Tipe:

INT

Validasi:

semester >= 1

Untuk dataset normal:

1 - 14

Jika ditemukan:

semester = 0
semester = -1
semester = "empat"

maka data dianggap invalid.

6. GPA

GPA menggunakan skala:

0.00 - 4.00

Contoh valid:

2.21
3.42
3.72
4.00

Contoh invalid:

-1.20
4.50
5.00

Database:

DECIMAL(3,2)
7. Attendance

Attendance menggunakan persentase:

0 - 100

Contoh:

94
87.4
76
68

Invalid:

-10
105
150

Database:

DECIMAL(5,2)
8. Academic Scores

Tiga nilai utama:

assignment_score
midterm_score
final_score

Range:

0 - 100

Contoh:

Assignment = 88
Midterm    = 86
Final      = 91

Data:

Assignment = 120
Midterm    = -20

dianggap invalid.

PRD memang meminta ketiga faktor tersebut ditampilkan dalam Performance Factors dan dianalisis terhadap GPA.

9. Study Hours

Field:

study_hours

Tipe:

DECIMAL(5,2)

Contoh:

6
10
15
18.5

Nilai negatif tidak diperbolehkan.

Data ini digunakan untuk:

Study Hours ↔ GPA

sebagaimana kebutuhan Analytics pada PRD.

10. Academic Status

Field ini bersifat turunan.

Contoh kategori:

Excellent
Good
Average
Poor

Kategori tersebut juga digunakan untuk Performance Distribution pada Dashboard.

Namun, batas kategori belum ditentukan secara eksplisit dalam PRD/Dashboard.

Karena itu, jangan hardcode batasnya sebelum kita menetapkan aturan klasifikasi secara resmi.

11. Risk Level

Risk level:

LOW
MEDIUM
HIGH

Risk ditentukan berdasarkan beberapa faktor:

GPA
Attendance
Score Trend
Study Hours
Previous GPA
Assignment Score
Midterm Score
Final Score

Ini mengikuti kebutuhan Risk Analysis pada PRD.

Penting: threshold LOW/MEDIUM/HIGH belum diberikan secara eksplisit dalam file sumber, sehingga jangan menganggap angka tertentu sebagai aturan final. Threshold akan kita definisikan pada spesifikasi Risk Engine berikutnya.

12. Database Schema

Untuk tahap awal, database dapat menggunakan beberapa tabel.

students
    │
    ├──────── academic_records
    │
    ├──────── risk_assessments
    │
    └──────── prediction_results
12.1 Table students
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(100) NOT NULL,
    current_semester INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
13. Table academic_records

Tabel ini menyimpan performa akademik mahasiswa per semester.

CREATE TABLE academic_records (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id VARCHAR(30) NOT NULL,

    semester INT NOT NULL,

    gpa DECIMAL(3,2) NOT NULL,

    attendance DECIMAL(5,2) NOT NULL,

    assignment_score DECIMAL(5,2) NOT NULL,

    midterm_score DECIMAL(5,2) NOT NULL,

    final_score DECIMAL(5,2) NOT NULL,

    study_hours DECIMAL(5,2) NOT NULL,

    academic_status VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
);

Dengan struktur ini kita bisa menghasilkan:

Semester 1 → GPA
Semester 2 → GPA
Semester 3 → GPA
Semester 4 → GPA

yang diperlukan untuk GPA Trend dan student academic history.

14. Table risk_assessments
CREATE TABLE risk_assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id VARCHAR(30) NOT NULL,

    semester INT NOT NULL,

    risk_level VARCHAR(20) NOT NULL,

    risk_score DECIMAL(5,2),

    main_factors TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
);

Contoh:

Student:
STD003

Risk Level:
HIGH

Risk Score:
82.50

Main Factors:
Low attendance
Low GPA
Declining score trend
Low study hours
15. Table prediction_results

Untuk menyimpan hasil prediksi GPA.

CREATE TABLE prediction_results (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id VARCHAR(30),

    semester INT NOT NULL,

    attendance DECIMAL(5,2) NOT NULL,

    assignment_score DECIMAL(5,2) NOT NULL,

    midterm_score DECIMAL(5,2) NOT NULL,

    final_score DECIMAL(5,2) NOT NULL,

    study_hours DECIMAL(5,2) NOT NULL,

    predicted_gpa DECIMAL(3,2) NOT NULL,

    performance_category VARCHAR(30),

    model_name VARCHAR(100),

    mae DECIMAL(10,4),

    rmse DECIMAL(10,4),

    r2 DECIMAL(10,4),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

PRD menetapkan minimal tiga model:

Linear Regression
Random Forest Regressor
Gradient Boosting Regressor

dan evaluasi menggunakan:

MAE
RMSE
R²

16. Machine Learning Dataset
Target

Target utama:

GPA
Features

Untuk prediksi GPA:

semester
attendance
assignment_score
midterm_score
final_score
study_hours

Sehingga konsepnya:

                ┌──────────────┐
                │ Attendance   │
                └──────┬───────┘
                       │
┌──────────────┐       │
│ Assignment   │───────┤
└──────────────┘       │
                       ▼
┌──────────────┐   ┌────────────┐
│ Midterm      │──▶│ ML Model   │
└──────────────┘   └─────┬──────┘
                         │
┌──────────────┐         │
│ Final        │─────────┤
└──────────────┘         │
                         ▼
┌──────────────┐     Predicted
│ Study Hours  │       GPA
└──────────────┘
17. Model Comparison

Training pipeline:

Dataset
   ↓
Validation
   ↓
Cleaning
   ↓
Feature Selection
   ↓
Train/Test Split
   ↓
Linear Regression
   ↓
Random Forest
   ↓
Gradient Boosting
   ↓
Evaluation
   ↓
Best Model

Evaluation:

Model	MAE	RMSE	R²
Linear Regression	calculated	calculated	calculated
Random Forest	calculated	calculated	calculated
Gradient Boosting	calculated	calculated	calculated

Tidak boleh menggunakan angka contoh sebagai hasil final.

Nilai harus dihitung dari dataset aktual.

18. Data Cleaning

Dataset yang di-upload harus diperiksa terhadap:

Missing Values

Contoh:

student_id   = STD001
gpa          = NULL
attendance   = 90

Sistem harus mendeteksi:

Missing GPA
Duplicate

Contoh:

STD001
STD001

Sistem mendeteksi duplicate record.

Invalid GPA
GPA = 4.80

Invalid karena:

GPA > 4.00
Invalid Attendance
attendance = 120

Invalid karena:

attendance > 100
Invalid Score
final_score = 150

Invalid karena:

score > 100
Invalid Data Type

Contoh:

gpa = "three point five"

harus masuk ke validation error.

19. Cleaning Pipeline
Raw Dataset
     ↓
Check Columns
     ↓
Check Data Types
     ↓
Check Missing Values
     ↓
Check Duplicates
     ↓
Check Invalid Values
     ↓
Check Outliers
     ↓
Cleaning Preview
     ↓
Apply Cleaning
     ↓
Processed Dataset

PRD memang menetapkan dataset management dengan preview, row/column count, missing values, duplicates, data types, invalid values, outliers, cleaning preview, apply cleaning, dan cleaning report.

20. Analytics Data

Dari struktur data di atas, sistem dapat menghasilkan:

GPA Analysis
GPA Distribution
GPA by Semester
GPA by Major
GPA Trend
Attendance Analysis
Attendance ↔ GPA
Study Analysis
Study Hours ↔ GPA
Score Analysis
Assignment ↔ GPA
Midterm ↔ GPA
Final ↔ GPA
Correlation
GPA
Attendance
Study Hours
Assignment
Midterm
Final

PRD secara eksplisit menetapkan analisis-analisis tersebut.

21. Dashboard Data Mapping

Struktur data harus mampu menyediakan semua data yang diperlukan Dashboard.

Dashboard	Sumber
Total Students	students
Average GPA	academic_records
Average Attendance	academic_records
At Risk	risk_assessments
GPA Trend	academic_records
Performance Distribution	academic_records.academic_status
Attendance vs GPA	academic_records
GPA by Major	students + academic_records
Academic Insights	analytics engine
Students Requiring Attention	risk engine

Dashboard memang dirancang untuk menjawab tiga pertanyaan utama: kondisi performa sekarang, perubahan performa, dan mahasiswa yang membutuhkan perhatian.

22. Contoh Relasi Data

Misalnya:

students

STD001
Muhammad Ihsan H.
Informatics
Semester 4

Memiliki:

academic_records

STD001 | S1 | 3.20
STD001 | S2 | 3.31
STD001 | S3 | 3.45
STD001 | S4 | 3.72

Kemudian:

risk_assessments

STD001 | S4 | LOW

Maka Dashboard dapat membuat:

GPA Trend

S1  3.20
S2  3.31
S3  3.45
S4  3.72

dan Student Profile dapat menampilkan academic history yang sama.

23. Prinsip Penting

Ada beberapa aturan yang harus kita pegang selama development.

1. Jangan hardcode hasil analytics

Salah:

const averageGPA = 3.42;

Benar:

MySQL
 ↓
Python / Pandas
 ↓
Calculate Average GPA
 ↓
Flask
 ↓
Dashboard
2. Jangan hardcode insight

Salah:

"GPA is increasing."

Benar:

Dataset
 ↓
Calculate current GPA
 ↓
Compare previous GPA
 ↓
Determine percentage change
 ↓
Generate insight

Dashboard.md juga secara eksplisit menyatakan insight harus berasal dari data aktual, bukan hardcoded.

3. Jangan menggunakan hasil contoh sebagai data nyata

Angka seperti:

1,248 students
3.42 GPA
87.4% attendance
86 at risk

yang ada di PRD/Dashboard hanyalah contoh UI, bukan data final.

4. ML harus menggunakan data aktual

Jangan:

predicted_gpa = 3.5

Tetapi:

Dataset
→ preprocessing
→ training
→ evaluation
→ best model
→ prediction
24. MVP Dataset

Untuk MVP, minimal kita membutuhkan:

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

Dengan 10 kolom ini kita sudah dapat membangun fondasi:

Students
   ↓
Analytics
   ↓
Dashboard
   ↓
ML Prediction
   ↓
Risk Analysis
   ↓
Insights
25. Data Specification Status
Komponen	Status
Student structure	Defined
Academic structure	Defined
GPA	Defined
Attendance	Defined
Assignment	Defined
Midterm	Defined
Final	Defined
Study Hours	Defined
ML Target	Defined
ML Features	Defined
Database structure	Defined
Validation	Defined
Cleaning pipeline	Defined
Risk fields	Defined
Risk thresholds	Belum ditentukan
Academic category thresholds	Belum ditentukan