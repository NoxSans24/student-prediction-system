# DATASET_CLEANING_IMPLEMENTATION_SPEC.md

## 1. Tujuan

Tahap ini mengimplementasikan **Dataset Management dan Data Cleaning Pipeline** sebagai fondasi sebelum data digunakan untuk Analytics, Risk Analysis, dan Machine Learning.

Tujuan utamanya:

* upload dataset CSV
* membaca dataset
* memeriksa struktur data
* validasi kolom
* validasi tipe data
* mendeteksi missing values
* mendeteksi duplicate
* mendeteksi nilai tidak valid
* mendeteksi outlier
* membuat cleaning preview
* menerapkan cleaning
* menyimpan dataset processed
* mencatat hasil cleaning

Pipeline:

```text
CSV
 ↓
Upload
 ↓
Validation
 ↓
Inspection
 ↓
Cleaning Preview
 ↓
User Confirmation
 ↓
Apply Cleaning
 ↓
Processed Dataset
 ↓
Analytics / Risk / ML
```

---

# 2. Scope

Modul ini mencakup:

### Dataset Management

* upload CSV
* dataset list
* dataset metadata
* dataset status
* dataset preview
* dataset validation

### Data Cleaning

* missing values
* duplicate rows
* duplicate student + semester
* incorrect data types
* invalid values
* range validation
* outlier detection
* cleaning preview
* apply cleaning
* cleaning report

---

# 3. Prinsip Utama

Ada satu aturan penting:

> **Raw dataset tidak boleh dimodifikasi.**

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

Dengan demikian:

```text
Raw Dataset
    │
    ├── tetap utuh
    │
    ▼
Cleaning Process
    │
    ▼
Processed Dataset
```

Jika proses cleaning gagal, dataset original tetap tersedia.

---

# 4. Struktur File

Tambahkan:

```text
routes/
├── dataset.py
└── ...

services/
├── data_cleaning_service.py
└── ...

database/
└── repositories/
    ├── dataset_repository.py
    └── dataset_cleaning_repository.py

templates/
└── dataset/
    ├── index.html
    ├── detail.html
    ├── preview.html
    └── cleaning.html

static/
├── css/
│   └── pages/
│       └── dataset.css
│
└── js/
    └── pages/
        └── dataset.js

data/
├── raw/
├── processed/
└── reports/
```

---

# 5. Dataset Schema

Dataset utama menggunakan kolom:

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

Contoh:

| student_id | name | major              | semester |  gpa | attendance | assignment_score | midterm_score | final_score | study_hours |
| ---------- | ---- | ------------------ | -------: | ---: | ---------: | ---------------: | ------------: | ----------: | ----------: |
| 20240001   | Andi | Informatics        |        1 | 3.20 |         90 |               85 |            80 |          88 |          12 |
| 20240002   | Budi | Information System |        1 | 3.40 |         95 |               90 |            87 |          91 |          15 |

---

# 6. Required Columns

Kolom wajib:

```python
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
```

Jika salah satu kolom wajib tidak tersedia:

```text
INVALID_DATASET
```

Dataset tidak boleh masuk ke tahap processing.

---

# 7. Extra Columns

Dataset boleh mempunyai kolom tambahan.

Contoh:

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
email
class
```

Kolom tambahan tidak langsung dihapus.

UI harus menunjukkan:

```text
Required Columns
10

Additional Columns
2
```

User dapat mengetahui adanya kolom tambahan sebelum cleaning.

---

# 8. Dataset Upload

Endpoint:

```text
POST /api/datasets/upload
```

Permission:

```text
Admin only
```

Flow:

```text
Select CSV
     ↓
Frontend validation
     ↓
Upload
     ↓
Backend validation
     ↓
Save raw dataset
     ↓
Create datasets record
     ↓
Return dataset ID
```

---

# 9. File Validation

Backend harus memeriksa:

### Extension

Hanya:

```text
.csv
```

### File availability

File harus benar-benar dikirim.

### Filename

Nama file tidak boleh digunakan langsung sebagai path filesystem tanpa sanitization.

Gunakan mekanisme secure filename atau generated filename.

---

# 10. Dataset Size

Ukuran maksimum file sebaiknya dikonfigurasi melalui Flask configuration.

Contoh:

```python
MAX_CONTENT_LENGTH
```

Jangan hardcode batas file di banyak tempat.

Jika terlalu besar:

```text
DATASET_TOO_LARGE
```

---

# 11. Dataset Metadata

Tabel `datasets` menyimpan:

```text
dataset_name
original_filename
file_path
total_rows
total_columns
missing_values
duplicate_rows
status
uploaded_by
uploaded_at
```

Status:

```text
uploaded
validated
cleaned
processed
failed
```

---

# 12. Dataset List

URL:

```text
/dataset
```

Tampilan:

```text
Dataset
├── Upload Dataset
├── Dataset Summary
└── Dataset List
```

Kolom:

```text
Dataset
Rows
Columns
Missing
Duplicates
Status
Uploaded
Actions
```

---

# 13. Dataset Summary

Dataset detail menampilkan:

```text
Total Rows
Total Columns
Missing Values
Duplicate Rows
Status
```

Contoh:

```text
Rows              1,250
Columns           10
Missing Values    14
Duplicates        5
Status            Validated
```

Nilai harus berasal dari dataset aktual.

---

# 14. Dataset Preview

Endpoint:

```text
GET /api/datasets/<dataset_id>/preview
```

Preview hanya menampilkan sebagian data.

Contoh:

```text
First 20 rows
```

Tujuannya agar dataset besar tidak seluruhnya dikirim ke browser.

---

# 15. Validation Pipeline

Setelah upload:

```text
Dataset
 ↓
Column Validation
 ↓
Type Validation
 ↓
Missing Validation
 ↓
Duplicate Validation
 ↓
Range Validation
 ↓
Outlier Detection
```

Hasilnya disimpan dalam object validation.

---

# 16. Column Validation

Service:

```python
validate_columns(df)
```

Output:

```json
{
    "required_columns": [],
    "missing_columns": [],
    "extra_columns": [],
    "valid": true
}
```

Jika:

```text
missing_columns != []
```

dataset invalid.

---

# 17. Type Validation

Expected type:

| Column           | Expected |
| ---------------- | -------- |
| student_id       | string   |
| name             | string   |
| major            | string   |
| semester         | integer  |
| gpa              | numeric  |
| attendance       | numeric  |
| assignment_score | numeric  |
| midterm_score    | numeric  |
| final_score      | numeric  |
| study_hours      | numeric  |

---

# 18. Safe Numeric Conversion

Untuk kolom numeric:

```python
pd.to_numeric(
    df[column],
    errors="coerce"
)
```

Nilai yang gagal dikonversi menjadi:

```text
NaN
```

Kemudian masuk ke missing/invalid validation.

Contoh:

```text
gpa = "abc"
```

menjadi:

```text
NaN
```

dan harus ditangani sebelum dataset digunakan.

---

# 19. Missing Values

Deteksi:

```python
df.isnull().sum()
```

Sistem harus mengetahui:

```text
Total Missing Values
Missing per Column
```

Contoh:

```text
gpa                 2
attendance          3
study_hours         5
```

---

# 20. Missing Identity Fields

Missing pada:

```text
student_id
name
major
```

harus dianggap sebagai masalah data penting.

Contoh:

```text
student_id = NULL
```

Tidak boleh langsung dimasukkan ke database mahasiswa.

---

# 21. Missing Numeric Values

Missing:

```text
gpa
attendance
assignment_score
midterm_score
final_score
study_hours
```

harus ditampilkan pada cleaning preview.

Sistem tidak boleh otomatis memilih metode imputation tanpa kebijakan yang ditentukan.

Pilihan action:

```text
Remove
Impute
Ignore
```

Metode imputation perlu dikonfigurasi/ditentukan sebelum Apply Cleaning.

---

# 22. Duplicate Rows

Deteksi:

```python
df.duplicated()
```

Output:

```text
Duplicate Rows
```

Contoh:

```text
Total rows = 1000
Duplicate rows = 12
```

---

# 23. Duplicate Student + Semester

Selain duplicate row penuh, perlu memeriksa:

```text
student_id + semester
```

Contoh:

```text
20240001 + Semester 3
20240001 + Semester 3
```

Ini dianggap conflict meskipun kolom lainnya berbeda.

Alasannya database memiliki:

```sql
UNIQUE(student_id, semester)
```

---

# 24. Range Validation

Aturan:

### GPA

```text
0 <= GPA <= 4
```

### Attendance

```text
0 <= attendance <= 100
```

### Assignment

```text
0 <= assignment_score <= 100
```

### Midterm

```text
0 <= midterm_score <= 100
```

### Final

```text
0 <= final_score <= 100
```

### Semester

```text
semester >= 1
```

### Study Hours

```text
study_hours >= 0
```

---

# 25. Invalid Values

Contoh:

```text
GPA = 5.7
Attendance = 120
Final Score = -10
Semester = 0
Study Hours = -4
```

Semua harus ditandai sebagai invalid.

Jangan langsung menghapus tanpa user confirmation.

---

# 26. Outlier Detection

Outlier menggunakan pendekatan IQR.

Formula:

```text
IQR = Q3 - Q1
```

Lower bound:

```text
Q1 - 1.5 × IQR
```

Upper bound:

```text
Q3 + 1.5 × IQR
```

Outlier hanya:

> **Flagged, bukan otomatis dihapus.**

Ini penting karena outlier akademik belum tentu merupakan data yang salah.

---

# 27. Cleaning Preview

Sebelum Apply Cleaning:

```text
Cleaning Preview
```

harus menunjukkan:

```text
Missing Values
Duplicates
Invalid GPA
Invalid Attendance
Invalid Scores
Incorrect Types
Outliers
Records Affected
```

Contoh:

```text
Missing Values              14
Duplicate Rows               5
Invalid GPA                  2
Invalid Attendance           1
Invalid Scores               3
Incorrect Data Types         4
Potential Outliers           8
```

---

# 28. Cleaning Actions

Action yang tersedia:

```text
Remove
Convert
Impute
Ignore
Flag
```

Namun setiap action harus sesuai jenis masalah.

Contoh:

```text
Invalid GPA
→ Remove / Fix manually
```

```text
Incorrect numeric type
→ Convert
```

```text
Outlier
→ Flag / Ignore
```

Tidak semua masalah boleh diperlakukan sama.

---

# 29. Cleaning Configuration

Gunakan konfigurasi terpusat.

Contoh:

```python
CLEANING_CONFIG = {
    "duplicate_action": "remove",
    "invalid_range_action": "flag",
    "outlier_action": "flag"
}
```

Nilai di atas adalah contoh implementasi, bukan aturan final produk.

Tujuannya agar policy cleaning tidak tersebar di banyak file.

---

# 30. Apply Cleaning

Endpoint:

```text
POST /api/datasets/<dataset_id>/clean/apply
```

Permission:

```text
Admin only
```

Flow:

```text
Cleaning Preview
       ↓
User Confirmation
       ↓
Apply Cleaning
       ↓
Validate Again
       ↓
Save Processed Dataset
       ↓
Create Cleaning Log
       ↓
Update Dataset Status
```

---

# 31. Confirmation

Sebelum apply:

```text
Apply Cleaning?

This action will create a processed dataset
based on the selected cleaning rules.
```

Button:

```text
Cancel
Apply Cleaning
```

Raw dataset tetap tidak berubah.

---

# 32. Processed Dataset

Output:

```text
data/processed/
```

Contoh:

```text
dataset_1_cleaned.csv
```

Dataset processed harus berasal dari raw dataset.

---

# 33. Cleaning Log

Setiap proses cleaning dicatat di:

```text
dataset_cleaning_logs
```

Informasi:

```text
dataset_id
missing_values_found
duplicates_found
invalid_gpa
invalid_attendance
invalid_scores
incorrect_data_types
outliers_found
total_records_cleaned
cleaning_method
applied_by
applied_at
```

---

# 34. Cleaning Report

Setelah cleaning, tampilkan:

```text
Original Rows
Rows Removed
Missing Values Handled
Invalid GPA
Invalid Attendance
Invalid Scores
Potential Outliers
Final Rows
```

Contoh:

```text
Original Rows       1,250
Rows Removed           7
Missing Handled       14
Invalid GPA             2
Invalid Attendance      1
Outliers Flagged        8
Final Rows          1,243
```

Angka harus berasal dari proses aktual.

---

# 35. Dataset Status

Lifecycle:

```text
uploaded
   ↓
validated
   ↓
cleaned
   ↓
processed
```

Jika error:

```text
failed
```

Contoh:

```text
Upload
→ uploaded

Validation berhasil
→ validated

Cleaning berhasil
→ cleaned

Dataset siap digunakan
→ processed
```

---

# 36. Dataset Repository

File:

```text
database/repositories/dataset_repository.py
```

Fungsi:

```text
create_dataset()
get_datasets()
get_dataset()
update_dataset_status()
update_dataset_statistics()
```

---

# 37. Cleaning Repository

File:

```text
database/repositories/dataset_cleaning_repository.py
```

Fungsi:

```text
create_cleaning_log()
get_cleaning_logs()
get_latest_cleaning_log()
```

---

# 38. Data Cleaning Service

File:

```text
services/data_cleaning_service.py
```

Fungsi utama:

```text
validate_columns()
validate_types()
detect_missing_values()
detect_duplicates()
detect_duplicate_student_semester()
validate_ranges()
detect_outliers()
generate_cleaning_preview()
apply_cleaning()
generate_cleaning_report()
```

---

# 39. Dataset Route

File:

```text
routes/dataset.py
```

Route harus tetap tipis.

Contoh flow:

```text
Route
 ↓
Parse Request
 ↓
Permission
 ↓
Dataset Service
 ↓
Response
```

Jangan memasukkan seluruh Pandas processing ke route.

---

# 40. Dataset API

Endpoint:

```text
GET  /api/datasets
POST /api/datasets/upload

GET /api/datasets/<dataset_id>/preview
GET /api/datasets/<dataset_id>/validation

POST /api/datasets/<dataset_id>/clean/preview
POST /api/datasets/<dataset_id>/clean/apply
```

Permission:

| Endpoint         | Admin | Analyst |
| ---------------- | ----- | ------- |
| Dataset list     | Yes   | Yes     |
| Upload           | Yes   | No      |
| Preview          | Yes   | Yes     |
| Validation       | Yes   | Yes     |
| Cleaning preview | Yes   | No      |
| Apply cleaning   | Yes   | No      |

---

# 41. Validation Response

Contoh:

```json
{
    "success": true,
    "data": {
        "valid": false,
        "missing_columns": [],
        "extra_columns": ["email"],
        "missing_values": 14,
        "duplicate_rows": 5,
        "invalid_gpa": 2,
        "invalid_attendance": 1,
        "invalid_scores": 3,
        "outliers": 8
    }
}
```

---

# 42. Cleaning Preview Response

```json
{
    "success": true,
    "data": {
        "original_rows": 1250,
        "affected_rows": 21,
        "actions": [
            {
                "type": "duplicate",
                "count": 5,
                "action": "remove"
            },
            {
                "type": "outlier",
                "count": 8,
                "action": "flag"
            }
        ]
    }
}
```

---

# 43. Transaction

Proses database harus aman.

Contoh:

```text
Create Dataset
      ↓
Save metadata
      ↓
Process dataset
      ↓
Create cleaning log
      ↓
Commit
```

Jika terjadi error:

```text
Rollback
```

Raw file tidak boleh hilang.

---

# 44. File Handling

Gunakan struktur:

```text
data/
├── raw/
├── processed/
└── reports/
```

Jangan menyimpan:

```text
uploads/
```

secara sembarangan di root project tanpa aturan.

Path harus berasal dari konfigurasi aplikasi.

---

# 45. Dataset Security

Upload dataset harus:

* membatasi extension
* membatasi ukuran
* melakukan filename sanitization
* tidak mengeksekusi file
* tidak menerima file executable
* tidak mempercayai filename user
* membatasi akses berdasarkan role

Dataset upload:

```text
Admin only
```

---

# 46. Frontend Dataset Page

Struktur:

```text
Dataset
│
├── Header
│   ├── Title
│   └── Upload Dataset
│
├── Dataset Summary
│
├── Dataset List
│
└── Dataset Detail
```

---

# 47. Upload UI

Area:

```text
Upload Dataset
```

Contoh:

```text
┌───────────────────────────────────┐
│                                   │
│        Upload CSV Dataset         │
│                                   │
│       [ Choose CSV File ]         │
│                                   │
│       Maximum file size ...       │
│                                   │
└───────────────────────────────────┘
```

Gunakan SVG icon.

Tidak menggunakan Unicode emoji.

---

# 48. Validation Status UI

Status badge:

```text
Uploaded
Validated
Cleaned
Processed
Failed
```

Status menggunakan semantic colors yang sudah ditentukan design system.

Jangan menggunakan banyak warna dekoratif.

---

# 49. Cleaning Preview UI

Struktur:

```text
Cleaning Preview
│
├── Dataset Summary
│
├── Data Issues
│
├── Proposed Actions
│
├── Affected Records
│
└── Apply Cleaning
```

Tujuan utama:

> User memahami perubahan sebelum perubahan dilakukan.

---

# 50. Loading / Empty / Error

Dataset module wajib memiliki:

### Loading

```text
Loading dataset...
```

### Empty

```text
No datasets uploaded yet.
```

### Error

```text
Unable to load dataset.
Try again.
```

### Success

```text
Dataset processed successfully.
```

---

# 51. Responsive

Desktop:

```text
Dataset Summary
→ 4 columns
```

Mobile:

```text
Dataset Summary
→ 2 columns
```

Dataset table:

```text
Horizontal scroll
```

Cleaning preview dapat berubah menjadi stacked layout pada mobile.

---

# 52. Dark Mode

Mengikuti design system:

### Light

```text
Background #F7F7F5
Surface    #FFFFFF
Border     #E5E5E3
Text       #171717
```

### Dark

```text
Background #111111
Surface    #181818
Border     #2A2A2A
Text       #F5F5F5
```

Tidak menggunakan neon atau glow.

---

# 53. Integration dengan Analytics

Dataset processed menjadi salah satu sumber:

```text
Processed Dataset
       ↓
Analytics Service
       ↓
Charts
```

Analytics hanya boleh menggunakan data yang sudah lolos validation/processing sesuai pipeline.

---

# 54. Integration dengan Machine Learning

ML training:

```text
Processed Dataset
       ↓
Preprocessing
       ↓
Train/Test Split
       ↓
Model Training
```

Dataset yang masih:

```text
uploaded
```

atau memiliki masalah validation tidak boleh langsung digunakan untuk training.

---

# 55. Integration dengan Student Database

Dataset CSV dan database mahasiswa harus dibedakan.

```text
CSV Dataset
    ↓
Data Processing
    ↓
Processed Dataset
```

sedangkan:

```text
Student Database
    ↓
Application Data
```

Import dataset ke database tidak otomatis dilakukan pada tahap ini kecuali workflow import memang ditambahkan kemudian.

---

# 56. Important Data Rule

Jangan menganggap:

```text
CSV = Database
```

CSV adalah sumber dataset/data processing.

MySQL adalah persistence layer aplikasi.

Keduanya dapat diintegrasikan, tetapi memiliki tanggung jawab berbeda.

---

# 57. Testing

Test minimal:

### Upload

* [ ] valid CSV
* [ ] non-CSV
* [ ] empty file
* [ ] oversized file

### Columns

* [ ] required columns lengkap
* [ ] missing column
* [ ] extra column

### Types

* [ ] valid numeric
* [ ] invalid numeric
* [ ] convertible numeric

### Missing

* [ ] no missing
* [ ] missing identity
* [ ] missing numeric

### Duplicate

* [ ] duplicate row
* [ ] duplicate student + semester

### Range

* [ ] valid GPA
* [ ] GPA > 4
* [ ] GPA < 0
* [ ] attendance > 100
* [ ] negative study hours

### Outlier

* [ ] detect IQR outlier
* [ ] verify outlier is only flagged

### Cleaning

* [ ] preview
* [ ] confirmation
* [ ] apply
* [ ] processed file
* [ ] cleaning log

---

# 58. Definition of Done

Tahap Dataset & Cleaning selesai apabila:

* [ ] CSV upload tersedia.
* [ ] Admin-only upload.
* [ ] File validation tersedia.
* [ ] Required columns tervalidasi.
* [ ] Extra columns terdeteksi.
* [ ] Data type validation tersedia.
* [ ] Missing values terdeteksi.
* [ ] Duplicate rows terdeteksi.
* [ ] Duplicate student + semester terdeteksi.
* [ ] GPA tervalidasi 0–4.
* [ ] Attendance tervalidasi 0–100.
* [ ] Assignment tervalidasi 0–100.
* [ ] Midterm tervalidasi 0–100.
* [ ] Final tervalidasi 0–100.
* [ ] Semester tervalidasi >= 1.
* [ ] Study hours tervalidasi >= 0.
* [ ] Outlier detection menggunakan IQR.
* [ ] Outlier hanya di-flag.
* [ ] Cleaning preview tersedia.
* [ ] Cleaning membutuhkan confirmation.
* [ ] Raw dataset tidak berubah.
* [ ] Processed dataset dibuat.
* [ ] Cleaning log tersimpan.
* [ ] Dataset status diperbarui.
* [ ] Loading state tersedia.
* [ ] Empty state tersedia.
* [ ] Error state tersedia.
* [ ] Responsive.
* [ ] Dark mode.
* [ ] SVG icons.
* [ ] Tidak ada hasil cleaning yang di-hardcode.

---

# 59. Posisi Project Setelah Tahap Ini

Pipeline project sekarang menjadi:

```text
┌─────────────────────┐
│ Student Management  │
│ Academic Records    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Dataset Upload      │
│ Validation          │
│ Cleaning            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Processed Data      │
└──────────┬──────────┘
           │
      ┌────┴────┐
      ▼         ▼
 Analytics    ML
      │         │
      ▼         ▼
   Insights  Prediction
      │
      ▼
    Risk
      │
      ▼
  Dashboard
      │
      ▼
   Reports
```


