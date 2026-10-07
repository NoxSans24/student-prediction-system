# STUDENT_ACADEMIC_IMPLEMENTATION_SPEC.md

## 1. Tujuan

Tahap ini mulai mengimplementasikan fitur utama **Student Performance Analytics**, yaitu:

* Student Management
* Student CRUD
* Academic Records
* Student Profile
* GPA History
* Performance Factors

Data yang dihasilkan pada tahap ini akan menjadi sumber untuk:

```text id="s7j9qf"
Student Data
      ↓
Academic Records
      ↓
Analytics
      ↓
Risk Analysis
      ↓
Machine Learning
      ↓
Dashboard
      ↓
Reports
```

---

# 2. Scope

Tahap ini mencakup:

### Student Management

* daftar mahasiswa
* search
* filter
* sorting
* pagination
* detail mahasiswa
* tambah mahasiswa
* edit mahasiswa
* hapus mahasiswa

### Academic Records

* tambah record semester
* lihat record
* edit record
* hapus record
* GPA history
* performance factors

### Student Profile

* identitas
* current GPA
* attendance
* academic status
* academic history
* performance factors
* placeholder risk information

Risk calculation lengkap **belum dilakukan pada tahap ini** karena menjadi tanggung jawab `Risk Engine`.

---

# 3. Struktur File

Tambahkan:

```text id="1lq4i8"
routes/
├── students.py
└── ...

services/
├── student_service.py
├── academic_service.py
└── ...

database/
└── repositories/
    ├── student_repository.py
    └── academic_repository.py

templates/
└── students/
    ├── index.html
    ├── detail.html
    ├── create.html
    └── edit.html

static/
├── css/
│   └── pages/
│       └── students.css
│
└── js/
    └── pages/
        └── students.js
```

---

# 4. Student Data Model

Entity utama:

```text id="6h9s7h"
Student
│
├── id
├── student_id
├── name
├── major
├── current_semester
├── created_at
└── updated_at
```

`id` adalah primary key internal database.

`student_id` adalah identitas mahasiswa yang ditampilkan kepada user.

---

# 5. Student ID

`student_id` harus:

* wajib
* unik
* tidak boleh kosong
* tidak boleh duplicate

Contoh:

```text id="1u5g2b"
20240001
20240002
20240003
```

Jika duplicate:

```text id="5h8r1e"
DUPLICATE_STUDENT
```

---

# 6. Student Create Flow

```text id="7bq5tm"
Add Student
     ↓
Form
     ↓
Validation
     ↓
Student Service
     ↓
Student Repository
     ↓
MySQL
     ↓
Success
```

Field:

```text id="t7rc8b"
Student ID
Name
Major
Current Semester
```

---

# 7. Student Validation

Validasi:

### Student ID

```text id="g5jv5p"
Required
Unique
```

### Name

```text id="9r6x2k"
Required
```

### Major

```text id="b4kq2y"
Required
```

### Current Semester

```text id="j5g1hz"
Integer
>= 1
```

Jika invalid:

```json id="4d8z2h"
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid student data"
    }
}
```

---

# 8. Student List

Halaman:

```text id="v1pr3m"
/students
```

Struktur:

```text id="b6nq8r"
Students
├── Page Header
├── Search
├── Filters
├── Student Table
└── Pagination
```

Header:

```text
Students

Manage student academic information
```

Admin:

```text
+ Add Student
```

Analyst:

```text
Tidak menampilkan Add Student
```

---

# 9. Student Table

Kolom:

```text id="c1nq5v"
Student
Major
Semester
GPA
Risk
Actions
```

Student:

```text id="u8m3q2"
Name
Student ID
```

Contoh:

```text
Muhammad Ihsan Hanafi
20240001
```

---

# 10. Current GPA

GPA pada Student List berasal dari:

```text id="w2v6z8"
Academic Record semester terbaru
```

Contoh:

```text id="2m2k8w"
Semester 1 → 3.10
Semester 2 → 3.25
Semester 3 → 3.42
```

Maka:

```text
Current GPA = 3.42
```

Jangan mengambil:

```text id="m1h6b7"
AVG seluruh semester
```

untuk field current GPA.

---

# 11. Risk Status

Risk pada Student List nantinya berasal dari:

```text id="j5q7cz"
Risk Engine
```

Tahap ini hanya menyiapkan struktur UI.

Contoh:

```text
Low
Medium
High
```

Jika Risk Engine belum dijalankan:

```text
—
```

atau:

```text
Not assessed
```

Jangan membuat risk berdasarkan hardcoded GPA threshold pada tahap ini.

---

# 12. Search

Search mendukung:

```text id="w6n3q9"
Student ID
Name
Major
```

Contoh:

```text
/search?q=andi
```

Database query menggunakan:

```sql
LIKE
```

atau mekanisme search yang sesuai.

Search harus dilakukan di database, bukan mengambil semua mahasiswa lalu memfilter seluruh data di browser.

---

# 13. Search Debounce

Frontend search dapat menggunakan debounce.

Flow:

```text id="j7v2k0"
User typing
   ↓
Wait ~300ms
   ↓
API request
```

Tujuannya mengurangi request berulang ketika user sedang mengetik.

---

# 14. Filter

Filter utama:

```text id="q9x4z1"
Major
Semester
GPA
Risk
```

Contoh:

```text
Major = Informatics
Semester = 4
```

Query harus menghasilkan mahasiswa yang memenuhi filter tersebut.

---

# 15. Pagination

Default:

```text id="k7f3x0"
10 students/page
```

User dapat berpindah:

```text
Previous
1
2
3
Next
```

Pagination dilakukan oleh backend/database.

---

# 16. Sorting

Student list dapat mendukung sorting:

```text id="3m5r9x"
Name
Student ID
Major
Semester
GPA
```

Contoh:

```text
GPA ↓
```

berarti GPA tertinggi berada di atas.

Sorting column harus menggunakan whitelist kolom yang diperbolehkan.

Jangan langsung memasukkan parameter sorting user ke SQL tanpa validasi.

---

# 17. Student Detail

URL:

```text id="e8b4c2"
/students/<student_id>
```

Halaman:

```text id="r2q8z9"
Student Detail
│
├── Student Information
├── Current Performance
├── GPA History
├── Performance Factors
└── Risk Assessment
```

---

# 18. Student Information

Menampilkan:

```text id="x4k7w2"
Student ID
Name
Major
Current Semester
```

Contoh:

```text
Student ID
20240001

Name
Andi Pratama

Major
Informatics

Current Semester
4
```

---

# 19. Current Performance

KPI:

```text id="y6q2k3"
Current GPA
Attendance
Semester
Academic Status
```

Contoh:

```text
GPA
3.42

Attendance
91%

Semester
4
```

Data berasal dari academic record terbaru.

---

# 20. Academic Status

Field:

```text id="7f2z5m"
academic_status
```

Status dapat berupa:

```text
Active
```

atau status lain jika nanti didefinisikan.

Namun jangan membuat banyak kategori status yang belum ditentukan requirement.

---

# 21. Academic Records

Halaman detail menampilkan history:

| Semester |  GPA | Attendance | Assignment | Midterm | Final | Study Hours |
| -------- | ---: | ---------: | ---------: | ------: | ----: | ----------: |
| 1        | 3.10 |         85 |         78 |      80 |    82 |          10 |
| 2        | 3.25 |         88 |         82 |      84 |    85 |          12 |
| 3        | 3.42 |         91 |         87 |      88 |    90 |          14 |

Nilai di atas hanya contoh.

---

# 22. Academic Record Create

Admin dapat menambahkan record semester.

Form:

```text id="w4y7q2"
Semester
GPA
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours
Academic Status
```

Analyst:

```text
Read only
```

---

# 23. Academic Validation

### Semester

```text
Integer
>= 1
```

### GPA

```text
0 <= GPA <= 4
```

### Attendance

```text
0 <= Attendance <= 100
```

### Assignment

```text
0 <= Assignment <= 100
```

### Midterm

```text
0 <= Midterm <= 100
```

### Final

```text
0 <= Final <= 100
```

### Study Hours

```text
>= 0
```

---

# 24. Duplicate Semester

Seorang mahasiswa tidak boleh memiliki dua record pada semester yang sama.

Contoh invalid:

```text
20240001
Semester 3
```

sudah ada.

Kemudian:

```text
20240001
Semester 3
```

ditambahkan lagi.

Database akan menolak melalui:

```text
UNIQUE(student_id, semester)
```

Service menerjemahkan error menjadi:

```text
ACADEMIC_RECORD_EXISTS
```

---

# 25. Academic Record Update

Admin dapat mengubah:

```text
GPA
Attendance
Assignment
Midterm
Final
Study Hours
Academic Status
```

Semester juga dapat diedit jika diperlukan, tetapi harus kembali melewati validasi duplicate constraint.

Setelah academic record berubah:

```text id="4v9w3j"
Academic Record Updated
        ↓
Risk harus direcalculate
        ↓
Analytics menggunakan data terbaru
        ↓
Dashboard menggunakan data terbaru
```

Risk recalculation akan diimplementasikan pada tahap Risk Engine.

---

# 26. Academic Record Delete

Admin dapat menghapus record.

Harus ada confirmation:

```text
Delete this academic record?
```

Action:

```text
Cancel
Delete
```

Tidak boleh langsung menghapus hanya karena user menekan tombol sekali.

---

# 27. Student Delete

Admin dapat menghapus student.

Karena relationship:

```text
students
 ├── academic_records
 └── risk_assessments
```

delete student dapat menghapus data terkait melalui:

```text
ON DELETE CASCADE
```

Prediction:

```text
ON DELETE SET NULL
```

Karena itu harus ada confirmation yang jelas.

Contoh:

```text
Delete this student?

This will also remove the student's academic
records and risk assessments.
```

---

# 28. Student Service

File:

```text id="uh4k8m"
services/student_service.py
```

Fungsi:

```text id="q8v4s1"
get_students()
get_student()
create_student()
update_student()
delete_student()
search_students()
filter_students()
```

Service bertanggung jawab:

* validation
* business rules
* repository calls
* error translation

---

# 29. Academic Service

File:

```text id="2y8w7q"
services/academic_service.py
```

Fungsi:

```text id="s9g2m4"
get_records()
get_record()
create_record()
update_record()
delete_record()
get_current_record()
get_previous_record()
get_gpa_history()
```

---

# 30. Current Record Service

Service:

```text id="4n7p2k"
get_current_record(student_id)
```

Logic:

```text
Academic Records
      ↓
ORDER BY semester DESC
      ↓
First record
```

Contoh:

```text
Semester 4 → Current
Semester 3
Semester 2
Semester 1
```

---

# 31. Previous Record Service

Logic:

```text id="k3x7q1"
Current = latest
Previous = second latest
```

Jika hanya ada satu semester:

```text
Previous = None
```

Service tidak boleh membuat data palsu.

---

# 32. GPA History

GPA history:

```text id="s7m2p9"
Semester 1 → 3.10
Semester 2 → 3.25
Semester 3 → 3.42
Semester 4 → 3.35
```

Data ini akan digunakan oleh:

* Student Profile
* GPA Trend
* Risk Engine
* Analytics

---

# 33. Performance Factors

Student Profile menampilkan:

```text id="f6q8w2"
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours
```

Tujuannya memberikan konteks terhadap GPA.

Contoh:

```text
Attendance       91%
Assignment       87
Midterm          88
Final            90
Study Hours      14
```

Tidak boleh mengatakan:

> “Study hours menyebabkan GPA meningkat”

karena analytics specification secara eksplisit membedakan **correlation** dan **causation**.

---

# 34. Student API

Endpoint:

```text id="2h7x4m"
GET    /api/students
GET    /api/students/<student_id>
POST   /api/students
PUT    /api/students/<student_id>
DELETE /api/students/<student_id>
```

Permission:

```text
GET
Admin + Analyst

POST
Admin

PUT
Admin

DELETE
Admin
```

---

# 35. Academic API

Endpoint:

```text id="6k9q2w"
GET  /api/students/<student_id>/academic-records
POST /api/students/<student_id>/academic-records
```

Jika edit/delete academic record diperlukan:

```text
PUT
DELETE
```

dapat menggunakan endpoint:

```text
/api/students/<student_id>/academic-records/<record_id>
```

Permission:

```text
GET
Admin + Analyst

POST/PUT/DELETE
Admin
```

---

# 36. Student API Response

Contoh:

```json id="l7d5q3"
{
    "success": true,
    "data": {
        "id": 1,
        "student_id": "20240001",
        "name": "Andi Pratama",
        "major": "Informatics",
        "current_semester": 4,
        "current_gpa": 3.42,
        "attendance": 91
    }
}
```

`current_gpa` dan `attendance` dapat berasal dari current academic record.

---

# 37. Student List Response

```json id="v2s7m4"
{
    "success": true,
    "data": {
        "items": [],
        "pagination": {
            "page": 1,
            "limit": 10,
            "total": 20,
            "pages": 2
        }
    }
}
```

---

# 38. Frontend Student Flow

```text id="m8x2q7"
Students
   ↓
Load API
   ↓
Loading State
   ↓
Render Table
```

Jika tidak ada data:

```text id="2q8w5p"
Empty State
```

Jika error:

```text id="j6v9r1"
Error State
```

---

# 39. Empty State

Jika belum ada mahasiswa:

```text
No students found

Add your first student to start managing
academic performance data.
```

Admin:

```text
+ Add Student
```

Analyst:

Tidak perlu menampilkan action create.

---

# 40. Loading State

Saat data sedang diambil:

```text id="4v7m1s"
Table Skeleton
```

atau loading indicator yang sederhana.

Jangan menggunakan animasi berlebihan.

---

# 41. Error State

Jika API gagal:

```text
Unable to load students.

Please try again.
```

Button:

```text
Retry
```

Tidak menampilkan error database mentah.

---

# 42. Student Form UI

Form menggunakan:

```text
Label
Input
Helper Text
Validation
Error Message
```

Contoh:

```text
Student ID
[ 20240001 ]

Name
[ Andi Pratama ]

Major
[ Informatics ]

Current Semester
[ 4 ]
```

---

# 43. Form Validation

Frontend melakukan validasi untuk UX.

Backend tetap melakukan validasi untuk security.

```text
Frontend Validation
        ↓
Backend Validation
        ↓
Database Constraint
```

Tiga layer ini saling melengkapi.

---

# 44. Student Detail Layout

Desktop:

```text
┌───────────────────────────────────────────────┐
│ Student Header                                │
├──────────────────────┬────────────────────────┤
│ Student Information  │ Current Performance    │
├──────────────────────┴────────────────────────┤
│ GPA History                                   │
├───────────────────────────────────────────────┤
│ Performance Factors                           │
├───────────────────────────────────────────────┤
│ Risk Assessment                               │
└───────────────────────────────────────────────┘
```

Mobile:

```text
Student Header
      ↓
Information
      ↓
Performance
      ↓
GPA History
      ↓
Factors
      ↓
Risk
```

---

# 45. Student Detail Chart

GPA history dapat divisualisasikan sebagai line chart.

X:

```text
Semester
```

Y:

```text
GPA
```

Contoh:

```text
3.5 ┤           ●
3.4 ┤        ●
3.3 ┤
3.2 ┤     ●
3.1 ┤  ●
    └──────────────
      S1 S2 S3 S4
```

Chart menggunakan Chart.js.

---

# 46. Responsive Table

Pada mobile, student table tidak boleh merusak layout.

Pilihan:

```text
Horizontal Scroll
```

atau:

```text
Mobile Student Card
```

Untuk MVP, horizontal scroll dapat digunakan agar struktur data tetap konsisten.

---

# 47. Security

Student API wajib menggunakan:

```text
@login_required
```

Mutation:

```text
POST
PUT
DELETE
```

wajib:

```text
@role_required("admin")
```

Analyst tidak boleh memanipulasi data hanya dengan memanggil endpoint secara manual.

---

# 48. Data Flow

Setelah tahap ini:

```text
                 MySQL
                   │
                   ▼
            Student Repository
                   │
                   ▼
             Student Service
                   │
             ┌─────┴─────┐
             ▼           ▼
         Student       Academic
          Route         Service
             │           │
             └─────┬─────┘
                   ▼
                Frontend
```

---

# 49. Integration dengan Modul Berikutnya

Student + Academic Records menjadi input:

### Analytics

```text
academic_records
       ↓
Analytics Service
```

### Risk

```text
academic_records
       ↓
Risk Engine
```

### Machine Learning

```text
academic_records
       ↓
Training Dataset
```

### Dashboard

```text
students
+
academic_records
+
risk_assessments
       ↓
Dashboard
```

---

# 50. Definition of Done

Tahap Student & Academic selesai apabila:

* [ ] Student list tersedia.
* [ ] Student search tersedia.
* [ ] Student filtering tersedia.
* [ ] Student sorting tersedia.
* [ ] Pagination tersedia.
* [ ] Student detail tersedia.
* [ ] Admin dapat create student.
* [ ] Admin dapat update student.
* [ ] Admin dapat delete student.
* [ ] Analyst hanya dapat membaca data.
* [ ] Academic record dapat ditampilkan.
* [ ] Admin dapat menambah academic record.
* [ ] Admin dapat mengubah academic record.
* [ ] Admin dapat menghapus academic record.
* [ ] Duplicate student ID ditolak.
* [ ] Duplicate student-semester ditolak.
* [ ] GPA tervalidasi 0–4.
* [ ] Attendance tervalidasi 0–100.
* [ ] Score tervalidasi 0–100.
* [ ] Study hours tervalidasi >= 0.
* [ ] Current GPA berasal dari semester terbaru.
* [ ] Previous record dapat diambil.
* [ ] GPA history tersedia.
* [ ] Performance factors tersedia.
* [ ] Delete confirmation tersedia.
* [ ] Loading state tersedia.
* [ ] Empty state tersedia.
* [ ] Error state tersedia.
* [ ] Responsive.
* [ ] Dark mode.
* [ ] SVG icons.
* [ ] Tidak ada hardcoded student result.

---

