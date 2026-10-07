1. Tujuan

Data Cleaning bertujuan memastikan dataset yang digunakan Student Performance Analytics:

memiliki struktur kolom yang benar,
memiliki tipe data yang sesuai,
tidak memiliki data duplikat yang tidak diperlukan,
tidak memiliki nilai di luar range,
dapat diproses oleh Pandas dan Scikit-learn,
siap digunakan untuk Analytics, Dashboard, Risk Analysis, dan Machine Learning.

Pipeline:

Raw Dataset
    ↓
Column Validation
    ↓
Data Type Validation
    ↓
Missing Value Detection
    ↓
Duplicate Detection
    ↓
Range Validation
    ↓
Outlier Detection
    ↓
Cleaning Preview
    ↓
Apply Cleaning
    ↓
Processed Dataset

PRD memang menempatkan validation dan cleaning sebagai bagian penting dari Dataset Management sebelum data digunakan untuk analisis dan ML.

2. Input Dataset

Format utama:

CSV

Minimal kolom:

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

Contoh:

student_id,name,major,semester,gpa,attendance,assignment_score,midterm_score,final_score,study_hours
STD001,Muhammad Ihsan,Informatics,4,3.72,94,88,86,91,18
STD002,Andi Pratama,Information System,3,2.81,76,74,71,78,10
STD003,Budi Santoso,Informatics,5,2.21,68,61,64,59,6
3. Column Validation

Ketika CSV di-upload, sistem harus memeriksa apakah seluruh kolom wajib tersedia.

Required Columns
REQUIRED_COLUMNS = [
    "student_id",
    "name",
    "major",
    "semester",
    "gpa",
    "attendance",
    "assignment_score",
    "midterm_score",
    "final_score",
    "study_hours"
]

Jika kolom lengkap:

Validation: PASSED

Jika misalnya:

study_hours

tidak ditemukan:

Validation: FAILED

Missing required column:
study_hours

Dataset tidak boleh langsung diproses ke tahap berikutnya.

4. Extra Columns

Dataset boleh memiliki kolom tambahan.

Contoh:

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
email
phone

Kolom tambahan tidak langsung dianggap error.

Sistem harus menampilkan:

Required Columns: 10
Additional Columns: 2

Kemudian user dapat menentukan apakah kolom tambahan digunakan atau diabaikan.

5. Data Type Validation

Sistem memeriksa tipe setiap kolom.

Column	Expected Type
student_id	String
name	String
major	String
semester	Integer
gpa	Float
attendance	Float
assignment_score	Float
midterm_score	Float
final_score	Float
study_hours	Float

Contoh masalah:

gpa
"three point five"

harus ditandai:

Invalid Data Type
6. Automatic Type Conversion

Untuk nilai yang masih dapat dikonversi dengan aman, sistem boleh melakukan conversion.

Contoh:

"3.72"

menjadi:

3.72

atau:

"94"

menjadi:

94.0

Namun data seperti:

"abc"

tidak boleh dipaksakan menjadi angka.

Status:

Invalid
7. Missing Values

Kolom yang diperiksa:

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

Contoh:

STD001 | Muhammad | Informatics | 4 | NULL | 90 | 80 | 85 | 87 | 15

Sistem harus mendeteksi:

Missing GPA: 1

Dataset Management pada PRD memang membutuhkan informasi missing values.

8. Missing Value Policy

Tidak semua missing value boleh diperlakukan sama.

Student ID
Missing → Invalid record

Karena student ID diperlukan untuk identifikasi.

Name
Missing → Invalid record
Major
Missing → Invalid record
GPA
Missing → Mark for cleaning
Attendance
Missing → Mark for cleaning
Academic Scores
Missing → Mark for cleaning
Study Hours
Missing → Mark for cleaning

Catatan penting: PRD tidak menentukan metode imputasi tertentu. Jadi kita tidak akan otomatis menetapkan mean/median/forward-fill sebagai aturan final.

Metode cleaning akan dibuat configurable.

9. Duplicate Detection

Sistem harus mendeteksi duplicate record.

Contoh:

STD001 | Muhammad | Informatics | 4 | 3.72 | ...
STD001 | Muhammad | Informatics | 4 | 3.72 | ...

akan dianggap duplicate.

Dashboard Dataset harus menampilkan:

Duplicate Rows
2

atau jumlah baris duplicate sesuai hasil preprocessing.

10. Student ID Duplicate

Selain duplicate seluruh baris, sistem juga harus memeriksa duplicate berdasarkan:

student_id + semester

Contoh:

STD001 | Semester 4
STD001 | Semester 4

Ini bermasalah karena satu mahasiswa seharusnya memiliki satu academic record untuk satu semester pada schema yang kita buat.

Database juga sudah memiliki constraint:

UNIQUE (student_id, semester)
11. Range Validation
GPA

Valid:

0.00 ≤ GPA ≤ 4.00

Invalid:

-1.00
4.50
5.00
Attendance

Valid:

0 ≤ attendance ≤ 100

Invalid:

-5
105
150
Assignment Score

Valid:

0 ≤ assignment_score ≤ 100
Midterm Score

Valid:

0 ≤ midterm_score ≤ 100
Final Score

Valid:

0 ≤ final_score ≤ 100
Semester

Untuk dataset akademik:

semester >= 1

PRD hanya membutuhkan semester sebagai input dan history. Karena tidak menetapkan batas maksimum semester, kita tidak akan mengunci batas atas tertentu pada cleaning rule.

Study Hours

Valid:

study_hours >= 0

Tidak boleh:

-5
-10
12. Invalid Value Report

Setelah validasi, sistem menghasilkan laporan seperti:

DATA VALIDATION REPORT

Total Rows       : 1000
Total Columns    : 10

Missing Values   : 12
Duplicate Rows   : 7

Invalid GPA      : 3
Invalid Attendance: 2
Invalid Scores   : 8
Invalid Types    : 4

Angka tersebut harus dihitung dari dataset aktual.

Tidak boleh hardcode.

13. Outlier Detection

PRD meminta sistem mendeteksi outliers pada Dataset Management.

Outlier detection dapat diterapkan pada data numerik seperti:

gpa
attendance
assignment_score
midterm_score
final_score
study_hours

Namun:

Outlier tidak otomatis berarti data salah.

Contoh:

study_hours = 35 jam

bisa saja merupakan data valid.

Karena itu hasilnya harus ditampilkan sebagai:

Potential Outlier

bukan langsung dihapus.

14. Outlier Strategy

Untuk tahap awal kita menggunakan IQR-based detection untuk analisis outlier.

Formula:

IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR

Jika:

value < Lower Bound

atau:

value > Upper Bound

maka ditandai sebagai potential outlier.

Contoh:

study_hours = 40

bisa muncul sebagai:

Potential Outlier

Tetapi tidak langsung dihapus.

15. Cleaning Preview

Sebelum perubahan diterapkan, sistem harus menampilkan preview.

Contoh:

┌───────────────────────────────────────────┐
│ Cleaning Preview                          │
├───────────────────────────────────────────┤
│ Missing Values        12                  │
│ Duplicate Rows         7                  │
│ Invalid GPA            3                  │
│ Invalid Attendance     2                  │
│ Invalid Scores         8                  │
│ Invalid Types          4                  │
│ Potential Outliers    15                  │
└───────────────────────────────────────────┘

Kemudian:

[Cancel]
[Apply Cleaning]

Ini sesuai dengan kebutuhan PRD yang meminta cleaning preview sebelum apply cleaning.

16. Cleaning Actions

Sistem cleaning harus memiliki beberapa tindakan:

Remove
Convert
Impute
Ignore
Flag

Contoh:

Invalid Data Type
"3.72"

→ Convert

Duplicate
duplicate row

→ Remove

Missing
GPA = NULL

→ Impute / Remove / Flag

Outlier
study_hours = 40

→ Flag

Bukan otomatis remove.

17. Jangan Mengubah Raw Dataset

Struktur file:

data/
│
├── raw/
│   └── original_dataset.csv
│
└── processed/
    └── cleaned_dataset.csv

Prinsip:

RAW
↓
tidak diubah
↓
PROCESSING
↓
PROCESSED

Ini penting agar kita masih mempunyai data original jika terjadi kesalahan cleaning.

18. Dataset Status

Dataset dapat memiliki status:

uploaded
validated
cleaned
processed
failed

Flow:

Upload
  ↓
uploaded
  ↓
Validation
  ↓
validated
  ↓
Cleaning
  ↓
cleaned
  ↓
Processing
  ↓
processed

Jika validation gagal:

uploaded
  ↓
failed
19. Cleaning Report

Setelah proses cleaning selesai:

CLEANING REPORT

Original Rows
1000

Rows Removed
7

Missing Values Handled
12

Invalid GPA
3

Invalid Attendance
2

Invalid Scores
8

Potential Outliers
15

Final Rows
993

Kemudian dataset dapat digunakan untuk:

Analytics
ML
Risk Analysis
Dashboard
20. Pandas Processing Concept

Implementasi nantinya kurang lebih:

import pandas as pd

df = pd.read_csv(file_path)

required_columns = [
    "student_id",
    "name",
    "major",
    "semester",
    "gpa",
    "attendance",
    "assignment_score",
    "midterm_score",
    "final_score",
    "study_hours"
]

Kemudian:

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

Jika:

missing_columns

tidak kosong, dataset gagal validation.

21. Numeric Columns
numeric_columns = [
    "semester",
    "gpa",
    "attendance",
    "assignment_score",
    "midterm_score",
    "final_score",
    "study_hours"
]

Kemudian sistem melakukan conversion:

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

Nilai yang gagal dikonversi menjadi:

NaN

dan masuk ke missing/invalid data report.

22. Range Checking

Contoh:

invalid_gpa = df[
    (df["gpa"] < 0) |
    (df["gpa"] > 4)
]

Attendance:

invalid_attendance = df[
    (df["attendance"] < 0) |
    (df["attendance"] > 100)
]

Score:

score_columns = [
    "assignment_score",
    "midterm_score",
    "final_score"
]

for column in score_columns:
    invalid = df[
        (df[column] < 0) |
        (df[column] > 100)
    ]
23. Cleaning Pipeline Architecture

Implementasi Python nantinya sebaiknya dipisahkan:

services/
└── data_cleaning_service.py

Dengan konsep:

validate_columns()
validate_types()
detect_missing_values()
detect_duplicates()
validate_ranges()
detect_outliers()
generate_cleaning_preview()
apply_cleaning()
generate_cleaning_report()

Jangan memasukkan seluruh proses cleaning ke Flask route.

Contoh yang tidak disarankan:

@app.route("/dataset/upload")
def upload():
    # 300 baris cleaning code

Lebih baik:

Route
 ↓
Service
 ↓
Cleaning Engine
 ↓
Result
 ↓
Route
24. Cleaning Architecture
routes/dataset.py
        │
        ▼
services/data_cleaning_service.py
        │
        ├── validate_columns()
        ├── validate_types()
        ├── detect_missing()
        ├── detect_duplicates()
        ├── validate_ranges()
        ├── detect_outliers()
        ├── preview_cleaning()
        └── apply_cleaning()
                │
                ▼
             Pandas
                │
                ▼
       processed_dataset.csv
25. Data Quality Score

Untuk MVP, Data Quality Score tidak perlu dibuat dulu.

Alasannya:

PRD meminta informasi kualitas data seperti missing values, duplicates, invalid values, dan outliers, tetapi tidak menetapkan formula Data Quality Score.

Jadi kita tidak akan membuat formula sendiri sebelum dibutuhkan.

26. Cleaning Rules Summary
Data Issue	Detection	Default Action
Missing required column	Column check	Reject
Missing Student ID	Null check	Invalid
Missing Name	Null check	Invalid
Missing Major	Null check	Invalid
Missing GPA	Null check	Flag
Missing Attendance	Null check	Flag
Missing Score	Null check	Flag
Duplicate row	Duplicate detection	Remove candidate
Duplicate student + semester	Duplicate key	Remove/resolve candidate
GPA < 0	Range	Invalid
GPA > 4	Range	Invalid
Attendance < 0	Range	Invalid
Attendance > 100	Range	Invalid
Score < 0	Range	Invalid
Score > 100	Range	Invalid
Negative study hours	Range	Invalid
Potential outlier	IQR	Flag
27. Hal yang Sengaja Belum Ditentukan

Ada beberapa hal yang tidak boleh kita asal tentukan karena tidak didukung oleh PRD/Dashboard:

Missing Value Imputation

Belum ditentukan apakah menggunakan:

Mean
Median
Mode
Forward Fill
Backward Fill
Outlier Treatment

Belum ditentukan apakah outlier akan:

Removed
Capped
Transformed
Kept
Academic Category Threshold

Belum ditentukan angka untuk:

Excellent
Good
Average
Poor
Risk Threshold

Belum ditentukan angka untuk:

LOW
MEDIUM
HIGH

Jadi semuanya akan dibuat di spesifikasi berikutnya, bukan ditebak sekarang.

28. Status Project

Sekarang fondasi kita sudah:

PRD.MD
      ↓
Dashboard.md
      ↓
DATA_SPECIFICATION.md
      ↓
DATABASE_SCHEMA.md
      ↓
DATA_CLEANING_SPEC.md

Status:

Komponen	Status
Product requirements	Done
Dashboard specification	Done
Data specification	Done
Database schema	Done
Data validation	Done
Data cleaning	Done
Missing value strategy	Partial
Outlier strategy	Partial
Risk rules	Not started
ML specification	Not started
Backend implementation	Not started