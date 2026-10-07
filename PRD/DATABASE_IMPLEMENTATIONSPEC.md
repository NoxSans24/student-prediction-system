# DATABASE_IMPLEMENTATION_SPEC.md

## 1. Tujuan

Tahap ini mengimplementasikan database layer untuk **Student Performance Analytics** berdasarkan `DATABASE_SCHEMA.md`.

Fokus tahap ini:

* koneksi MySQL
* query database
* transaction
* CRUD dasar
* relationship
* seed data
* error handling
* database testing

Pada tahap ini kita **belum mengimplementasikan seluruh business logic** Analytics, Risk, ML, dan Reports.

---

# 2. Arsitektur Database Layer

Struktur:

```text
Route
  ↓
Service
  ↓
Database Layer
  ↓
MySQL
```

Contoh:

```text
Student Route
     ↓
Student Service
     ↓
Student Repository / Query
     ↓
MySQL
```

Tujuannya agar SQL tidak tersebar di berbagai route.

---

# 3. Struktur Folder

Setelah tahap ini:

```text
database/
├── __init__.py
├── connection.py
├── schema.sql
├── seed.sql
└── queries/
    ├── __init__.py
    ├── user_queries.py
    ├── student_queries.py
    ├── academic_queries.py
    ├── risk_queries.py
    ├── prediction_queries.py
    └── dataset_queries.py
```

Jika implementasi menggunakan repository pattern, dapat menggunakan:

```text
database/
└── repositories/
    ├── user_repository.py
    ├── student_repository.py
    ├── academic_repository.py
    ├── risk_repository.py
    ├── prediction_repository.py
    └── dataset_repository.py
```

Untuk project ini, repository layer direkomendasikan agar query tetap terorganisir.

---

# 4. Connection Management

`database/connection.py` bertanggung jawab untuk:

```text
Create connection
Get connection
Close connection
Handle connection error
```

Konfigurasi diambil dari:

```text
.env
```

Contoh konfigurasi:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

Tidak boleh ada credential hardcoded.

---

# 5. Connection Lifecycle

Setiap operasi database mengikuti:

```text
Request
 ↓
Get Connection
 ↓
Create Cursor
 ↓
Execute Query
 ↓
Commit / Rollback
 ↓
Close Cursor
 ↓
Close Connection
```

Untuk query SELECT:

```text
Execute
 ↓
Fetch
 ↓
Close
```

Untuk INSERT/UPDATE/DELETE:

```text
Execute
 ↓
Commit
```

Jika gagal:

```text
Execute
 ↓
Exception
 ↓
Rollback
 ↓
Raise handled error
```

---

# 6. Parameterized Query

Semua query yang menerima input user wajib menggunakan parameterized query.

Jangan:

```python
query = f"""
SELECT * FROM students
WHERE name = '{name}'
"""
```

Gunakan parameter:

```python
query = """
SELECT *
FROM students
WHERE name = %s
"""

cursor.execute(query, (name,))
```

Tujuannya mencegah SQL injection.

---

# 7. Transaction

Operasi yang mengubah database harus menggunakan transaction.

Contoh:

```text
Create Student
      ↓
Insert Student
      ↓
Insert Academic Record
      ↓
Commit
```

Jika academic record gagal:

```text
Insert Student
      ↓
Insert Academic Record
      ↓
ERROR
      ↓
ROLLBACK
```

Dengan demikian database tidak berada dalam kondisi setengah tersimpan.

---

# 8. Database Tables

Database final terdiri dari:

```text
users
students
academic_records
risk_assessments
prediction_results
datasets
dataset_cleaning_logs
```

---

# 9. Users Table

Digunakan untuk authentication.

Field utama:

```text
id
username
email
password_hash
role
created_at
updated_at
```

Role:

```text
admin
analyst
```

Constraint:

```text
username UNIQUE
email UNIQUE
```

Password tidak pernah disimpan sebagai plaintext.

---

# 10. Students Table

Menyimpan informasi utama mahasiswa.

Field:

```text
id
student_id
name
major
current_semester
created_at
updated_at
```

`student_id` harus unik.

Contoh:

```text
student_id = 20240001
```

---

# 11. Academic Records

Menyimpan performa mahasiswa berdasarkan semester.

Field:

```text
id
student_id
semester
gpa
attendance
assignment_score
midterm_score
final_score
study_hours
academic_status
created_at
updated_at
```

Relationship:

```text
students
   │
   └── academic_records
```

Satu mahasiswa dapat mempunyai banyak academic record.

---

# 12. Student-Semester Constraint

Tidak boleh terdapat dua record untuk mahasiswa yang sama pada semester yang sama.

Constraint:

```sql
UNIQUE (student_id, semester)
```

Contoh valid:

```text
20240001 → Semester 1
20240001 → Semester 2
20240001 → Semester 3
```

Tidak valid:

```text
20240001 → Semester 2
20240001 → Semester 2
```

---

# 13. Risk Assessments

Menyimpan hasil Risk Engine.

Field:

```text
id
student_id
semester
risk_level
risk_score
main_factors
assessed_at
```

Risk:

```text
low
medium
high
```

`risk_score` digunakan sebagai nilai internal risk engine sesuai implementasi yang telah dirancang.

---

# 14. Prediction Results

Menyimpan hasil prediksi GPA.

Field:

```text
id
student_id
semester
attendance
assignment_score
midterm_score
final_score
study_hours
predicted_gpa
performance_category
model_name
mae
rmse
r2
created_at
```

Tujuannya agar prediction history dapat ditampilkan.

---

# 15. Dataset Table

Menyimpan metadata dataset.

Field:

```text
id
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

Database menyimpan metadata, bukan isi seluruh CSV.

---

# 16. Dataset Cleaning Logs

Mencatat hasil proses cleaning.

Field:

```text
id
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

Relationship:

```text
datasets
    │
    └── dataset_cleaning_logs
```

---

# 17. Foreign Key Rules

Relationship:

```text
users
 └── datasets
 └── dataset_cleaning_logs

students
 ├── academic_records
 ├── risk_assessments
 └── prediction_results

datasets
 └── dataset_cleaning_logs
```

Behavior:

### Student deleted

Academic records:

```text
ON DELETE CASCADE
```

Risk assessments:

```text
ON DELETE CASCADE
```

Prediction:

```text
ON DELETE SET NULL
```

Artinya prediction history tetap ada meskipun student dihapus, tetapi `student_id` menjadi `NULL`.

---

# 18. Student Query Layer

Query yang diperlukan:

```text
get_all_students()
get_student_by_id()
get_student_by_student_id()
search_students()
filter_students()
create_student()
update_student()
delete_student()
```

Search dapat menggunakan:

```text
student_id
name
major
```

---

# 19. Student Filtering

Filter yang dibutuhkan:

```text
major
semester
GPA
risk
```

Namun filter risk tidak selalu berasal langsung dari `students`.

Risk perlu menggunakan relationship:

```text
students
 ↓
academic_records
 ↓
risk_assessments
```

Query harus disusun agar tidak menghasilkan duplicate student akibat JOIN.

---

# 20. Pagination

Student list harus mendukung:

```text
page
limit
```

Contoh:

```text
page = 1
limit = 10
```

Database query menggunakan:

```text
LIMIT
OFFSET
```

Offset:

```text
(page - 1) * limit
```

Response nantinya memiliki:

```json
{
    "items": [],
    "pagination": {
        "page": 1,
        "limit": 10,
        "total": 100,
        "pages": 10
    }
}
```

---

# 21. Academic Query Layer

Query:

```text
get_student_academic_records()
get_academic_record()
create_academic_record()
update_academic_record()
delete_academic_record()
get_latest_record()
get_previous_record()
```

Query `get_latest_record()` penting untuk:

* Dashboard
* Risk
* Student Profile
* Prediction

---

# 22. Current Academic Record

Current performance ditentukan berdasarkan semester terbaru.

Contoh:

```text
Semester 1 → GPA 3.10
Semester 2 → GPA 3.25
Semester 3 → GPA 3.40
```

Current:

```text
Semester 3
GPA 3.40
```

Previous:

```text
Semester 2
GPA 3.25
```

Database layer hanya mengambil data.

Penentuan risk tetap dilakukan oleh:

```text
Risk Service
```

---

# 23. Academic History

Student detail membutuhkan history:

```text
Semester
GPA
Attendance
Assignment
Midterm
Final
Study Hours
```

Query:

```sql
SELECT
    semester,
    gpa,
    attendance,
    assignment_score,
    midterm_score,
    final_score,
    study_hours
FROM academic_records
WHERE student_id = %s
ORDER BY semester ASC;
```

Data ini nantinya digunakan oleh:

* Student Profile
* Analytics
* Risk
* Insights

---

# 24. User Query Layer

Query:

```text
get_user_by_id()
get_user_by_username()
get_user_by_email()
create_user()
update_user()
```

Authentication service akan menggunakan query ini.

Password hashing dilakukan di:

```text
services/auth_service.py
```

bukan di database layer.

---

# 25. Risk Query Layer

Query:

```text
get_latest_risk()
get_student_risk_history()
get_students_by_risk()
save_risk_assessment()
```

Contoh:

```text
Risk Engine
     ↓
Risk Result
     ↓
Risk Repository
     ↓
risk_assessments
```

---

# 26. Prediction Query Layer

Query:

```text
save_prediction()
get_prediction_history()
get_student_predictions()
get_latest_prediction()
```

Prediction history tidak menggantikan academic record.

Keduanya memiliki tujuan berbeda:

```text
academic_records
→ performa aktual

prediction_results
→ hasil prediksi model
```

---

# 27. Dataset Query Layer

Query:

```text
create_dataset()
get_dataset()
get_all_datasets()
update_dataset_status()
update_dataset_statistics()
```

Contoh lifecycle:

```text
uploaded
    ↓
validated
    ↓
cleaned
    ↓
processed
```

---

# 28. Cleaning Log Query

Query:

```text
create_cleaning_log()
get_cleaning_logs()
get_latest_cleaning_log()
```

Cleaning log harus immutable secara konsep.

Artinya hasil historis cleaning tidak boleh sembarangan diubah hanya karena dataset diproses lagi.

---

# 29. Dashboard Database Queries

Database layer harus menyediakan data dasar untuk Dashboard.

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

### GPA Trend

```sql
SELECT
    semester,
    AVG(gpa) AS average_gpa
FROM academic_records
GROUP BY semester
ORDER BY semester;
```

Database layer hanya mengambil data.

Interpretasi tetap berada di service.

---

# 30. At-Risk Query

At-risk student dihitung berdasarkan hasil Risk Engine.

Contoh:

```sql
SELECT COUNT(DISTINCT student_id)
FROM risk_assessments
WHERE risk_level IN ('medium', 'high');
```

Jangan membuat query berdasarkan asumsi:

```text
GPA < 2.5 = automatically high risk
```

karena aturan tersebut belum ditetapkan sebagai threshold final.

Risk classification tetap menjadi tanggung jawab:

```text
Risk Service
```

---

# 31. Data Validation

Database tetap harus memiliki validation dasar.

Contoh:

```text
student_id → required + unique
name → required
major → required
semester → >= 1
GPA → 0–4
attendance → 0–100
scores → 0–100
study_hours → >= 0
```

Namun validasi dataset yang kompleks tetap dilakukan oleh:

```text
Data Cleaning Service
```

---

# 32. Transaction Boundary

Transaction ditentukan berdasarkan satu operasi bisnis.

Contoh:

### Create Student

```text
BEGIN
 ↓
Insert student
 ↓
COMMIT
```

### Update Student + Academic Record

Jika memang merupakan satu operasi:

```text
BEGIN
 ↓
Update student
 ↓
Update academic record
 ↓
COMMIT
```

Jika salah:

```text
ROLLBACK
```

Jangan membuat transaction terlalu besar sehingga menahan database lock terlalu lama.

---

# 33. Database Error Handling

Contoh error:

```text
Duplicate student_id
```

harus diterjemahkan menjadi:

```text
DUPLICATE_STUDENT
```

Bukan mengirim pesan MySQL mentah ke frontend.

Contoh:

```json
{
    "success": false,
    "error": {
        "code": "DUPLICATE_STUDENT",
        "message": "Student ID already exists"
    }
}
```

---

# 34. Service dan Database Separation

Contoh flow Create Student:

```text
POST /api/students
        ↓
Student Route
        ↓
Validation
        ↓
Student Service
        ↓
Student Repository
        ↓
MySQL
```

Bukan:

```text
POST /api/students
        ↓
SQL langsung di Route
```

---

# 35. Query Result Mapping

Database result sebaiknya dikonversi menjadi struktur Python yang konsisten.

Contoh:

```python
{
    "id": 1,
    "student_id": "20240001",
    "name": "Andi Pratama",
    "major": "Informatics",
    "current_semester": 4
}
```

Service kemudian dapat memproses struktur tersebut tanpa bergantung pada cursor MySQL.

---

# 36. Database Index

Index yang sudah direncanakan:

```text
students.student_id
students.name
students.major
students.current_semester
```

Selain itu:

```text
academic_records.student_id
academic_records.semester
risk_assessments.student_id
risk_assessments.risk_level
prediction_results.student_id
datasets.status
```

Index digunakan secara terukur.

Jangan membuat index pada semua kolom karena dapat memperbesar storage dan memperlambat operasi write.

---

# 37. Seed Data Development

Seed data harus cukup untuk menguji:

```text
Student Search
Pagination
Major Filter
Semester Filter
GPA
Risk
Charts
Trend
```

Disarankan dataset development memiliki:

```text
≥ 20 students
```

dan beberapa semester per student.

Angka ini merupakan rekomendasi untuk testing, bukan requirement PRD.

---

# 38. Data Distribution

Seed data sebaiknya tidak semuanya memiliki nilai sama.

Contohnya harus terdapat variasi:

```text
GPA
Attendance
Assignment
Midterm
Final
Study Hours
Major
Semester
```

Sehingga chart seperti:

```text
GPA Distribution
GPA Trend
Attendance vs GPA
GPA by Major
```

benar-benar dapat diuji.

---

# 39. Database Testing

Minimal test:

### Connection

```text
[ ] MySQL connection berhasil
[ ] Invalid credential menghasilkan error
```

### Student

```text
[ ] Create
[ ] Read
[ ] Update
[ ] Delete
[ ] Duplicate ID ditolak
```

### Academic

```text
[ ] Create record
[ ] Read history
[ ] Duplicate semester ditolak
[ ] Delete mengikuti student
```

### Risk

```text
[ ] Save assessment
[ ] Read assessment
```

### Prediction

```text
[ ] Save prediction
[ ] Read prediction history
```

---

# 40. Referential Integrity Testing

Test:

### Delete student

Pastikan:

```text
students → deleted
academic_records → deleted
risk_assessments → deleted
prediction_results → student_id NULL
```

Ini harus mengikuti foreign key yang telah ditetapkan.

---

# 41. Database Performance

Untuk query student list:

```text
Search
Filter
Pagination
```

harus menggunakan query database secara langsung.

Jangan:

```text
SELECT semua data
↓
Python filter semua data
↓
Python pagination
```

untuk dataset besar.

Gunakan:

```text
MySQL
↓
WHERE
↓
ORDER BY
↓
LIMIT
↓
OFFSET
```

sehingga database mengembalikan data yang diperlukan saja.

---

# 42. Definition of Done

Database Implementation selesai apabila:

* [ ] MySQL connection berjalan.
* [ ] Semua tabel tersedia.
* [ ] Foreign key bekerja.
* [ ] Query layer tersedia.
* [ ] Repository layer tersedia jika digunakan.
* [ ] User query tersedia.
* [ ] Student CRUD tersedia.
* [ ] Academic record query tersedia.
* [ ] Risk query tersedia.
* [ ] Prediction query tersedia.
* [ ] Dataset query tersedia.
* [ ] Cleaning log query tersedia.
* [ ] Parameterized query digunakan.
* [ ] Transaction digunakan pada write operation.
* [ ] Rollback tersedia.
* [ ] Database error ditangani.
* [ ] Pagination database tersedia.
* [ ] Index utama tersedia.
* [ ] Seed data tersedia.
* [ ] Referential integrity diuji.
* [ ] Tidak ada credential hardcoded.

