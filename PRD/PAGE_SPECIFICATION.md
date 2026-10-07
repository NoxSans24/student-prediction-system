# `PAGE_SPECIFICATION.md`

Dokumen ini menerjemahkan **PRD + Dashboard UX + API Specification + Frontend Design System** menjadi spesifikasi setiap halaman. Fokusnya adalah: **apa yang tampil, data dari mana, action apa yang tersedia, dan bagaimana halaman berperilaku pada kondisi berbeda.**

---

# 1. Struktur Halaman

Aplikasi memiliki halaman:

```text
Authentication
└── Login

Overview
├── Dashboard
├── Students
└── Analytics

Intelligence
├── Prediction
└── Risk Analysis

Data
├── Dataset
└── Reports

Settings
└── Settings
```

---

# 2. Global Page Structure

Semua halaman setelah login menggunakan:

```text
┌─────────────────────────────────────────────┐
│ Sidebar │ Topbar                            │
│         ├───────────────────────────────────┤
│         │ Page Header                       │
│         │                                   │
│         │ Main Content                      │
│         │                                   │
│         │                                   │
└─────────┴───────────────────────────────────┘
```

`base.html` menjadi parent template.

---

# 3. Login Page

## Tujuan

Mengautentikasi user sebelum mengakses sistem.

## Layout

```text
┌──────────────────────────────────────────────┐
│                                              │
│             Student Performance              │
│                  Analytics                   │
│                                              │
│          ┌──────────────────────┐            │
│          │ Username / Email     │            │
│          │                      │            │
│          │ Password             │            │
│          │                      │            │
│          │ [      Login      ]  │            │
│          └──────────────────────┘            │
│                                              │
└──────────────────────────────────────────────┘
```

## Components

* Logo/brand
* Username/email input
* Password input
* Login button
* Error message

## States

### Default

Form kosong.

### Loading

```text
Logging in...
```

Button disabled sementara request berjalan.

### Error

```text
Invalid username or password.
```

### Success

Redirect:

```text
/dashboard
```

---

# 4. Dashboard

Dashboard adalah **halaman utama aplikasi**.

Tujuan utamanya:

> Menjawab bagaimana performa akademik sekarang, apa yang berubah, dan siapa yang membutuhkan perhatian.

---

## Header

```text
Dashboard

Overview of your academic data

Last updated: ...
```

---

## KPI

```text
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ Students   │ │ Avg GPA    │ │ Attendance │ │ At Risk    │
│            │ │            │ │            │ │            │
│ 120        │ │ 3.24       │ │ 87.5%      │ │ 18         │
│ +8         │ │ +0.15      │ │ +2.1%      │ │ 15%        │
└────────────┘ └────────────┘ └────────────┘ └────────────┘
```

Data:

```text
GET /api/dashboard
```

---

# 5. Dashboard — Main Analytics

## GPA Trend

Menampilkan:

```text
Average GPA across semesters
```

Chart:

```text
Line Chart
```

Hover:

```text
Semester 3
Average GPA: 3.28
```

---

## Performance Distribution

Chart:

```text
Donut / simple distribution chart
```

Kategori:

```text
Excellent
Good
Average
Poor
```

Nilai harus dihitung dari dataset aktual.

---

# 6. Dashboard — Secondary Analytics

## Attendance vs GPA

Scatter plot.

Data:

```text
Student
Attendance
GPA
```

Hover:

```text
Student Name
Attendance: 88%
GPA: 3.42
```

---

## GPA by Major

Horizontal bar chart.

Contoh:

```text
Informatics          ███████████ 3.42
Information Systems  ██████████  3.28
...
```

---

# 7. Dashboard — Academic Insights

Bagian:

```text
Academic Insights
```

Berisi insight yang dihasilkan secara dinamis.

Contoh struktur:

```text
GPA Trend
Average GPA increased compared with the previous semester.

Attendance
Average attendance remains stable.

Risk
15% of students currently require attention.
```

Tidak boleh menggunakan kalimat yang tidak didukung data.

---

# 8. Dashboard — Students Requiring Attention

Table:

```text
Student
Major
GPA
Attendance
Change
Risk
```

Contoh:

```text
Muhammad    Informatics    2.41    68%    -0.42    HIGH
Andi        Informatics    2.72    74%    -0.21    MEDIUM
```

Data berasal dari Risk Engine.

Button:

```text
View All
```

mengarahkan ke Risk Analysis atau Students sesuai implementasi final.

---

# 9. Dashboard States

### Loading

KPI skeleton + chart skeleton.

### Empty

```text
No academic data available.

Add or upload academic data to start analyzing performance.
```

### Error

```text
Unable to load dashboard data.

[ Retry ]
```

---

# 10. Students Page

## Tujuan

Mengelola dan melihat seluruh mahasiswa.

Header:

```text
Students

Manage student academic profiles

[ + Add Student ]
```

---

## Search

```text
[ Search students... ]
```

Mencari berdasarkan:

```text
Student ID
Name
Major
```

---

## Filters

```text
[ Major ]
[ Semester ]
[ GPA ]
[ Risk ]
```

---

# 11. Students Table

```text
┌─────────────────────────────────────────────────────┐
│ Student │ Major │ Semester │ GPA │ Risk │ Actions │
├─────────────────────────────────────────────────────┤
│ ...                                                   │
└─────────────────────────────────────────────────────┘
```

Action:

```text
View
Edit
Delete
```

`Edit` dan `Delete` hanya Admin.

---

# 12. Add Student

Route:

```text
/students/create
```

Form:

```text
Student ID
Name
Major
Current Semester
```

Button:

```text
[ Cancel ] [ Create Student ]
```

Validation:

```text
Student ID required
Name required
Major required
Semester valid
```

---

# 13. Edit Student

Route:

```text
/students/<id>/edit
```

Form menggunakan data existing.

```text
Student ID
Name
Major
Current Semester
```

Student ID sebaiknya tidak diubah jika digunakan sebagai identifier unik.

---

# 14. Delete Student

Sebelum delete:

```text
Delete Student?

This action will also remove related academic records.

[ Cancel ] [ Delete ]
```

Karena database menggunakan:

```text
ON DELETE CASCADE
```

penghapusan student berdampak pada academic records dan data terkait yang menggunakan cascade tersebut.

---

# 15. Student Detail

Route:

```text
/students/<id>
```

Header:

```text
Muhammad Ihsan Hanafi

20240001 · Informatics · Semester 4
```

---

## Current Performance

```text
┌────────────┐ ┌────────────┐ ┌────────────┐
│ GPA        │ │ Attendance │ │ Risk       │
│ 3.42       │ │ 89%        │ │ LOW        │
└────────────┘ └────────────┘ └────────────┘
```

---

# 16. Student GPA History

Line chart:

```text
GPA
│
│       ●
│   ●       ●
│ ●
└────────────────
  S1 S2 S3 S4
```

Menunjukkan perkembangan GPA mahasiswa dari semester ke semester.

---

# 17. Student Performance Factors

Tampilkan:

```text
Attendance
Assignment
Midterm
Final
Study Hours
```

Bisa menggunakan card kecil atau bar/list.

Tujuan:

> Memberikan konteks terhadap performa mahasiswa.

Jangan menyatakan faktor tersebut sebagai penyebab GPA tanpa analisis kausal.

---

# 18. Student Risk Assessment

Tampilkan:

```text
Risk Level
Risk Score
Main Factors
Early Warnings
```

Contoh:

```text
HIGH

Risk score: 72

Main factors:
• GPA decreased
• Attendance decreased
• Score trend decreased

Early warning:
Significant GPA decline
```

---

# 19. Analytics Page

Header:

```text
Analytics

Explore academic performance patterns
```

---

## Filter

```text
Major
Semester
GPA
Attendance
Risk
```

Semua chart harus berubah mengikuti filter.

---

# 20. Analytics Chart Order

Urutan:

```text
1. GPA Distribution
2. GPA by Semester
3. GPA by Major
4. GPA Trend
5. Attendance vs GPA
6. Study Hours vs GPA
7. Assignment vs GPA
8. Midterm vs GPA
9. Final vs GPA
10. Correlation Heatmap
```

---

# 21. Analytics Interpretation

Setiap chart dapat memiliki deskripsi singkat.

Contoh:

```text
GPA Trend

Average GPA across semesters.
```

Untuk correlation:

```text
Correlation

Shows relationships between selected academic variables.
```

Tidak menggunakan bahasa:

```text
Attendance causes higher GPA.
```

karena correlation tidak membuktikan causation.

---

# 22. Prediction Page

Header:

```text
GPA Prediction

Estimate GPA based on academic performance factors.
```

---

## Prediction Form

Input:

```text
Semester
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours
```

Layout desktop:

```text
┌───────────────────────────┐
│ Semester                 │
│ Attendance               │
│ Assignment Score         │
│ Midterm Score             │
│ Final Score               │
│ Study Hours               │
│                           │
│ [ Predict GPA ]           │
└───────────────────────────┘
```

---

# 23. Prediction Result

Setelah berhasil:

```text
Prediction Result

3.41

Good

Model
Random Forest Regressor

MAE       0.18
RMSE      0.24
R²        0.82
```

Jangan menampilkan:

```text
Confidence: 95%
```

kecuali model benar-benar menyediakan confidence interval/probabilistic estimate yang valid.

---

# 24. Prediction History

Di bawah form/result:

```text
Prediction History
```

Table:

```text
Date
Student
Semester
Predicted GPA
Model
```

Jika prediction tidak dikaitkan dengan student:

```text
Student: General Prediction
```

atau nilai kosong sesuai desain database.

---

# 25. Prediction Error States

Jika model belum tersedia:

```text
Prediction model is not available.

An administrator needs to train a model first.
```

Jika data tidak cukup:

```text
There is not enough valid data to make a prediction.
```

Jika input tidak valid:

```text
Please check the highlighted fields.
```

---

# 26. Risk Analysis Page

Header:

```text
Risk Analysis

Identify students who may require academic attention.
```

---

## Risk Summary

```text
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Low        │ │ Medium     │ │ High       │
│ 80         │ │ 25         │ │ 15         │
└────────────┘ └────────────┘ └────────────┘
```

---

# 27. Risk Distribution

Chart:

```text
Low
Medium
High
```

Tujuannya memberikan gambaran distribusi risiko.

---

# 28. Risk Table

```text
Student
Major
GPA
Attendance
GPA Change
Risk
```

Filter:

```text
Risk
Major
Semester
```

Sorting:

```text
Risk severity
GPA
Attendance
GPA change
```

---

# 29. Early Warnings

Section:

```text
Early Warnings
```

Contoh:

```text
GPA decline
Attendance decline
Score decline
```

Warning harus dihasilkan berdasarkan threshold yang configurable.

---

# 30. Dataset Page

Header:

```text
Dataset

Manage and validate academic datasets

[ Upload Dataset ]
```

---

## Dataset Overview

```text
Rows
Columns
Missing Values
Duplicates
Status
```

---

# 31. Dataset List

Table:

```text
Dataset
Original Filename
Rows
Columns
Status
Uploaded At
Actions
```

Status:

```text
Uploaded
Validated
Cleaned
Processed
Failed
```

---

# 32. Dataset Upload

Upload area:

```text
┌─────────────────────────────────────┐
│                                     │
│       Upload academic CSV           │
│                                     │
│       [ Choose File ]               │
│                                     │
└─────────────────────────────────────┘
```

Validasi:

```text
File type
Required columns
Data structure
```

---

# 33. Dataset Preview

Setelah upload:

```text
Dataset Preview

Rows: 1000
Columns: 10

[ Data Table ]
```

Kemudian:

```text
Validation Results
```

---

# 34. Dataset Validation

Tampilkan:

```text
Missing Values
Duplicates
Invalid GPA
Invalid Attendance
Invalid Scores
Incorrect Data Types
Potential Outliers
```

Contoh:

```text
Missing values             12
Duplicate rows              4
Invalid GPA                 2
Invalid attendance          1
Invalid scores              3
Outliers                     8
```

---

# 35. Cleaning Preview

Sebelum data diubah:

```text
Cleaning Preview
```

Tampilkan:

```text
Original rows
Rows affected
Missing values
Duplicates
Invalid values
Outliers
```

Action:

```text
[ Cancel ] [ Apply Cleaning ]
```

Admin harus melakukan confirmation.

---

# 36. Cleaning Result

Setelah cleaning:

```text
Dataset cleaned successfully.

Original rows: 1000
Final rows: 992
Rows removed: 8
Missing values handled: 12
```

Cleaning log disimpan ke:

```text
dataset_cleaning_logs
```

---

# 37. Reports Page

Header:

```text
Reports

Generate and export academic analysis reports.
```

---

## Report Cards

```text
Overall Performance
Academic performance overview

[ Generate ]
```

```text
Student Report
Detailed student performance

[ Generate ]
```

```text
Risk Report
Students requiring attention

[ Generate ]
```

```text
ML Report
Model training and evaluation

[ Generate ]
```

---

# 38. Report Filters

### Overall

```text
Major
Semester
Period
```

### Student

```text
Student
Semester / Period
```

### Risk

```text
Risk Level
Major
Semester
```

### ML

```text
Dataset
Training Run
Model
```

---

# 39. Report Preview

Sebelum export:

```text
Report Preview

Summary
Statistics
Charts
Insights
```

Action:

```text
[ PDF ]
[ Excel ]
[ CSV ]
```

---

# 40. Settings Page

Struktur:

```text
Settings

Appearance
Account
Security
```

---

## Appearance

```text
Theme

○ Light
○ Dark
```

Theme toggle juga tersedia di topbar.

---

# 41. Account

```text
Username
Email
Role
```

Informasi role bersifat read-only.

Contoh:

```text
Role
Administrator
```

---

# 42. Security

```text
Change Password
```

Input:

```text
Current Password
New Password
Confirm Password
```

Validasi:

```text
Current password correct
New password valid
Passwords match
```

---

# 43. Role-Based UI

### Admin

Sidebar:

```text
Dashboard
Students
Analytics
Prediction
Risk Analysis
Dataset
Reports
Settings
```

Admin memiliki action:

```text
Add Student
Edit
Delete
Upload Dataset
Clean Dataset
Train Model
```

---

### Analyst

Sidebar tetap dapat menampilkan:

```text
Dashboard
Students
Analytics
Prediction
Risk Analysis
Dataset
Reports
Settings
```

Namun action administratif tidak tersedia.

Contoh:

```text
Dataset
→ View only
```

dan:

```text
Students
→ View only
```

Backend tetap memvalidasi permission.

---

# 44. Responsive Page Behavior

## Desktop

```text
Sidebar
+
Full content
+
2-column analytics
```

## Tablet

```text
Collapsed sidebar
+
2-column jika ruang cukup
```

## Mobile

```text
Topbar
Off-canvas sidebar
Single-column content
```

---

# 45. Mobile Dashboard

Urutan:

```text
Dashboard

KPI
[ 1 ][ 2 ]
[ 3 ][ 4 ]

GPA Trend

Performance Distribution

Attendance vs GPA

GPA by Major

Insights

Students Requiring Attention
```

Informasi paling penting tetap berada di atas.

---

# 46. Mobile Student Detail

Urutan:

```text
Student Header

GPA
Attendance
Risk

GPA History

Performance Factors

Risk Assessment

Academic Records
```

Tidak memaksakan layout desktop.

---

# 47. Mobile Prediction

Form menjadi single column:

```text
Semester

Attendance

Assignment

Midterm

Final

Study Hours

[ Predict GPA ]
```

Result muncul langsung di bawah form.

---

# 48. Mobile Tables

Jika tabel terlalu lebar:

```text
overflow-x: auto;
```

Tidak mengecilkan font sampai sulit dibaca.

---

# 49. Global State Pattern

Setiap halaman harus memiliki minimal:

```text
Initial
Loading
Success
Empty
Error
```

Contoh:

```text
Initial
  ↓
Loading
  ↓
Success
```

atau:

```text
Loading
  ↓
Empty
```

atau:

```text
Loading
  ↓
Error
```

---

# 50. Page-to-API Mapping

| Page               | API                                         |
| ------------------ | ------------------------------------------- |
| Login              | `/login`                                    |
| Dashboard          | `/api/dashboard`                            |
| Students           | `/api/students`                             |
| Student Detail     | `/api/students/<id>`                        |
| Academic History   | `/api/students/<id>/academic-records`       |
| Analytics          | `/api/analytics/*`                          |
| Insights           | `/api/insights`                             |
| Prediction         | `/api/prediction`                           |
| Prediction History | `/api/predictions`                          |
| Risk               | `/api/risk`                                 |
| Student Risk       | `/api/students/<id>/risk`                   |
| Dataset            | `/api/datasets`                             |
| Dataset Preview    | `/api/datasets/<id>/preview`                |
| Cleaning           | `/api/datasets/<id>/clean/*`                |
| Reports            | `/api/reports/*`                            |
| Settings           | `/api/auth/me` + account/security endpoints |

---

# 51. Page-to-Service Mapping

```text
Dashboard
 ├── Analytics Service
 ├── Risk Service
 └── Insight Service

Students
 └── Student / Database Layer

Analytics
 └── Analytics Service

Prediction
 └── Prediction Service
       └── ML Pipeline

Risk
 └── Risk Service

Dataset
 └── Data Cleaning Service

Reports
 └── Report Service

Login
 └── Auth Service
```

---

# 52. Final User Journey

Alur penggunaan utama:

```text
Login
  ↓
Dashboard
  ↓
┌─────────────────────────────────┐
│                                 │
├→ Students → Student Detail      │
│                                 │
├→ Analytics → Academic Patterns  │
│                                 │
├→ Prediction → GPA Prediction    │
│                                 │
├→ Risk → Student Attention       │
│                                 │
├→ Dataset → Upload/Clean         │
│                                 │
└→ Reports → Export               │
```

---

# 53. Core Product Journey

Yang paling penting adalah alur data:

```text
Dataset
   ↓
Validation
   ↓
Cleaning
   ↓
Processed Data
   ↓
┌───────────────┬──────────────┬───────────────┐
↓               ↓              ↓
Analytics       Risk           ML
↓               ↓              ↓
Insights        Warning        Prediction
└───────────────┴──────────────┴───────────────┘
                    ↓
                Dashboard
                    ↓
                 Reports
```

Ini menjadi **alur utama produk**, bukan sekadar perpindahan antarhalaman.


