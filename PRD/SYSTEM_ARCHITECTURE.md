## `SYSTEM_ARCHITECTURE.md`

Dokumen ini menyatukan seluruh spesifikasi sebelumnya menjadi arsitektur teknis final untuk **Student Performance Analytics**. Fokusnya adalah memastikan setiap fitur punya tempat yang jelas dan tidak terjadi logika yang berantakan ketika mulai coding.

---

# SYSTEM ARCHITECTURE

## 1. Tujuan Arsitektur

Student Performance Analytics menggunakan arsitektur modular berbasis **Flask** dengan pemisahan antara:

```text
Frontend
    ↓
Routes / API
    ↓
Services
    ↓
Data Processing / ML
    ↓
Database
```

Arsitektur harus mendukung:

* Dashboard
* Student Management
* Analytics
* Prediction
* Risk Analysis
* Dataset Management
* Reports
* Authentication
* Machine Learning
* Data Cleaning
* Automated Insights

Prinsip utama:

> **Routes menangani request, Services menangani business logic, ML menangani machine learning, Database menangani persistence, dan Frontend menangani presentation.**

---

# 2. Arsitektur Keseluruhan

```text
┌───────────────────────────────────────────────┐
│                   USER                        │
│        Admin / Analyst                        │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│                 FRONTEND                      │
│                                               │
│ HTML + CSS + JavaScript                       │
│ DM Sans + SVG Icons                           │
│ Charts + Forms + Tables                       │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│              FLASK ROUTES                     │
│                                               │
│ Auth │ Dashboard │ Students │ Analytics       │
│ Prediction │ Risk │ Dataset │ Reports         │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│                 SERVICES                      │
│                                               │
│ Analytics Service                             │
│ Insight Service                               │
│ Risk Service                                  │
│ Prediction Service                            │
│ Data Cleaning Service                         │
│ Report Service                                │
│ Auth Service                                  │
└───────────────┬─────────────────┬─────────────┘
                │                 │
                ▼                 ▼
┌────────────────────────┐ ┌─────────────────────┐
│   DATA PROCESSING      │ │    ML PIPELINE      │
│                        │ │                     │
│ Pandas                 │ │ Preprocessing       │
│ NumPy                  │ │ Training            │
│ Validation             │ │ Evaluation          │
│ Cleaning               │ │ Prediction          │
└────────────┬───────────┘ └──────────┬──────────┘
             │                        │
             └────────────┬───────────┘
                          ▼
              ┌────────────────────────┐
              │        MySQL           │
              │                        │
              │ users                  │
              │ students               │
              │ academic_records       │
              │ risk_assessments       │
              │ prediction_results     │
              │ datasets               │
              │ dataset_cleaning_logs  │
              └────────────────────────┘
```

---

# 3. Technology Layer

## Presentation Layer

```text
HTML
CSS
JavaScript
DM Sans
SVG Icons
Chart Library
```

Tanggung jawab:

* Menampilkan data.
* Menampilkan chart.
* Form input.
* Filter.
* Search.
* Table.
* Modal.
* Dark/light mode.
* Responsive layout.
* Loading/error/empty state.

Frontend **tidak boleh menjadi tempat utama business logic**.

Contoh:

```text
Jangan:
JavaScript menentukan apakah mahasiswa HIGH RISK.

Gunakan:
Backend → Risk Service → hasil HIGH RISK
Frontend → hanya menampilkan hasil.
```

---

# 4. Routing Layer

Folder:

```text
routes/
├── auth.py
├── dashboard.py
├── students.py
├── analytics.py
├── prediction.py
├── risk.py
├── dataset.py
└── reports.py
```

Setiap file bertanggung jawab terhadap domain tertentu.

---

## `auth.py`

Menangani:

```text
/login
/logout
/profile
/change-password
```

Tanggung jawab:

* Login.
* Logout.
* Session.
* Authentication.
* Authorization.

---

## `dashboard.py`

Menangani:

```text
/dashboard
```

Dashboard mengambil data dari beberapa service:

```text
Analytics Service
       ↓
Risk Service
       ↓
Insight Service
       ↓
Dashboard
```

Dashboard tidak menghitung seluruh statistik sendiri.

---

## `students.py`

Menangani:

```text
/students
/students/<id>
/students/create
/students/<id>/edit
/students/<id>/delete
```

Admin dapat melakukan CRUD.

Analyst dapat melihat data sesuai permission.

---

## `analytics.py`

Menangani:

```text
/analytics
/api/analytics/gpa-distribution
/api/analytics/gpa-semester
/api/analytics/gpa-major
/api/analytics/gpa-trend
/api/analytics/attendance-gpa
/api/analytics/study-hours-gpa
/api/analytics/correlation
```

Analytics menggunakan data aktual dari database.

---

# 5. Prediction Route

File:

```text
routes/prediction.py
```

Endpoint utama:

```text
/prediction
/api/prediction
```

Flow:

```text
User Input
    ↓
Validation
    ↓
Prediction Service
    ↓
ML Model
    ↓
Predicted GPA
    ↓
Performance Category
    ↓
Save History
    ↓
Response
```

Contoh:

```text
Attendance       85
Assignment       80
Midterm          78
Final            82
Study Hours       5
Semester          4
```

↓

```text
Prediction Service
```

↓

```text
ML Model
```

↓

```text
Predicted GPA: 3.xx
```

---

# 6. Risk Route

File:

```text
routes/risk.py
```

Flow:

```text
Academic Records
       ↓
Risk Service
       ↓
Risk Calculation
       ↓
Risk Level
       ↓
Risk Factors
       ↓
Early Warning
       ↓
Database
```

Contoh:

```text
GPA turun
Attendance turun
Score turun
Study hours rendah
        ↓
Risk Engine
        ↓
HIGH
```

Risk Engine **bukan machine learning**.

```text
Risk Analysis
= Rule-based

GPA Prediction
= Machine Learning
```

Keduanya harus tetap terpisah.

---

# 7. Dataset Architecture

File:

```text
routes/dataset.py
services/data_cleaning_service.py
```

Flow:

```text
CSV Upload
    ↓
Dataset Validation
    ↓
Dataset Preview
    ↓
Detect Problems
    ↓
Cleaning Preview
    ↓
Admin Confirmation
    ↓
Apply Cleaning
    ↓
Processed Dataset
    ↓
Database / ML Pipeline
```

Contoh masalah:

```text
Missing Value
Duplicate
Invalid GPA
Invalid Attendance
Invalid Score
Wrong Data Type
Outlier
```

---

# 8. Data Processing Layer

Folder:

```text
data/
├── raw/
├── processed/
└── reports/
```

Prinsip penting:

```text
RAW
 ↓
VALIDATE
 ↓
CLEAN
 ↓
PROCESSED
```

Dataset asli tidak langsung dimodifikasi.

Contoh:

```text
data/raw/students.csv

        ↓

data/processed/students_cleaned.csv
```

Dengan begitu dataset asli tetap dapat digunakan untuk audit atau proses ulang.

---

# 9. Analytics Service

File:

```text
services/analytics_service.py
```

Service menyediakan:

```python
get_gpa_distribution()
get_gpa_by_semester()
get_gpa_by_major()
get_gpa_trend()
get_attendance_vs_gpa()
get_study_hours_vs_gpa()
get_assignment_vs_gpa()
get_midterm_vs_gpa()
get_final_vs_gpa()
get_correlation_matrix()
```

Flow:

```text
Database
    ↓
Analytics Service
    ↓
Aggregated Data
    ↓
API
    ↓
JavaScript
    ↓
Chart
```

Dengan demikian chart tidak perlu mengetahui struktur database.

---

# 10. Insight Architecture

File:

```text
services/insight_service.py
```

Flow:

```text
Analytics
    +
Risk Analysis
    +
Academic Data
        ↓
Insight Service
        ↓
Dynamic Insights
        ↓
Dashboard
```

Contoh output:

```json
{
    "type": "gpa_trend",
    "priority": "medium",
    "title": "GPA Trend",
    "message": "Average GPA increased compared with the previous semester.",
    "value": 3.25,
    "change": 0.15
}
```

Pesan harus berasal dari data aktual.

Tidak boleh:

```text
"90% mahasiswa mengalami peningkatan"
```

jika angka tersebut tidak benar-benar dihitung dari dataset.

---

# 11. Machine Learning Architecture

Folder:

```text
ml/
├── preprocessing.py
├── train.py
├── evaluate.py
├── predict.py
└── models/
```

Flow:

```text
Processed Dataset
       ↓
Preprocessing
       ↓
Train/Test Split
       ↓
┌──────────────────────┐
│ Linear Regression    │
│ Random Forest        │
│ Gradient Boosting    │
└──────────┬───────────┘
           ↓
       Evaluation
           ↓
 MAE / RMSE / R²
           ↓
    Best Model
           ↓
      Save Model
```

Model tidak boleh langsung digunakan sebelum proses training dan evaluation.

---

# 12. ML Training Flow

```text
Admin
  ↓
Train Model
  ↓
Load Processed Dataset
  ↓
Validate Dataset
  ↓
Prepare Features
  ↓
Split Dataset
  ↓
Train 3 Models
  ↓
Evaluate
  ↓
Compare Metrics
  ↓
Select Best Model
  ↓
Save Model
  ↓
Save Metadata
```

Model yang menang ditentukan berdasarkan hasil evaluasi aktual.

Bukan:

```text
Random Forest selalu terbaik.
```

---

# 13. Prediction Flow

Setelah model tersedia:

```text
User
 ↓
Prediction Form
 ↓
Input Validation
 ↓
Load Best Model
 ↓
Preprocess Input
 ↓
Predict GPA
 ↓
Performance Category
 ↓
Save Prediction
 ↓
Display Result
```

Output:

```text
Predicted GPA
Performance Category
Model Used
MAE
RMSE
R²
```

---

# 14. Database Layer

File:

```text
database/
├── connection.py
└── schema.sql
```

Database:

```text
student_performance_analytics
```

Relasi utama:

```text
users
  │
  ├──── datasets
  │
  └──── dataset_cleaning_logs


students
  │
  ├──── academic_records
  ├──── risk_assessments
  └──── prediction_results
```

---

# 15. Student Data Flow

Ketika mahasiswa dibuat:

```text
Admin
 ↓
Student Form
 ↓
students.py
 ↓
Student Service / Database
 ↓
students table
```

Ketika nilai akademik ditambahkan:

```text
Academic Record
 ↓
academic_records
 ↓
Analytics
 ↓
Risk Engine
 ↓
Dashboard
```

Jadi perubahan data akademik dapat memengaruhi:

```text
Analytics
Risk
Insights
Dashboard
```

---

# 16. Report Architecture

File:

```text
services/report_service.py
```

Report tidak membuat business logic baru.

Flow:

```text
Existing Data
     ↓
Analytics
     ↓
Risk
     ↓
Insights
     ↓
Report Service
     ↓
PDF / Excel / CSV
```

Contoh:

```text
Dashboard
Analytics
Risk Analysis
ML Results
     ↓
Report Service
     ↓
Overall Report
```

---

# 17. Report Export

### PDF

```text
ReportLab
```

### Excel

```text
Pandas
openpyxl
```

### CSV

```text
Pandas
```

Report harus menggunakan data aktual.

---

# 18. Authentication Architecture

Flow:

```text
Login
 ↓
Validate Credentials
 ↓
Check Password Hash
 ↓
Create Session
 ↓
Dashboard
```

Session hanya menyimpan informasi yang diperlukan:

```text
user_id
username
role
```

Tidak menyimpan:

```text
password
password_hash
```

---

# 19. Authorization

Setiap request sensitif harus diperiksa backend.

Contoh:

```python
@admin_required
def upload_dataset():
    ...
```

Bukan hanya:

```text
Hide Upload button
```

karena user tetap bisa mencoba mengakses endpoint secara langsung.

---

# 20. Permission Flow

```text
                    ┌── Admin
User ── Login ──────┤
                    └── Analyst
                         │
                         ▼
                    Permission
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          Allowed                 Denied
              │                     │
              ▼                     ▼
          Execute                  403
```

---

# 21. Final Folder Structure

Struktur final yang direkomendasikan:

```text
student-performance-analytics/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
├── config/
│   └── settings.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── students.py
│   ├── analytics.py
│   ├── prediction.py
│   ├── risk.py
│   ├── dataset.py
│   └── reports.py
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── analytics_service.py
│   ├── insight_service.py
│   ├── risk_service.py
│   ├── prediction_service.py
│   ├── data_cleaning_service.py
│   └── report_service.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── schema.sql
│
├── ml/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── models/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── reports/
│
├── templates/
│   ├── base.html
│   │
│   ├── auth/
│   │   ├── login.html
│   │   └── profile.html
│   │
│   ├── dashboard/
│   │   └── index.html
│   │
│   ├── students/
│   │   ├── index.html
│   │   ├── detail.html
│   │   ├── create.html
│   │   └── edit.html
│   │
│   ├── analytics/
│   │   └── index.html
│   │
│   ├── prediction/
│   │   └── index.html
│   │
│   ├── risk/
│   │   └── index.html
│   │
│   ├── dataset/
│   │   ├── index.html
│   │   ├── upload.html
│   │   └── cleaning.html
│   │
│   ├── reports/
│   │   └── index.html
│   │
│   ├── settings/
│   │   └── index.html
│   │
│   └── errors/
│       ├── 403.html
│       ├── 404.html
│       └── 500.html
│
├── static/
│   ├── css/
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   ├── utilities.css
│   │   └── pages/
│   │       ├── dashboard.css
│   │       ├── students.css
│   │       ├── analytics.css
│   │       ├── prediction.css
│   │       ├── risk.css
│   │       ├── dataset.css
│   │       └── reports.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── theme.js
│   │   ├── sidebar.js
│   │   ├── charts.js
│   │   └── pages/
│   │       ├── dashboard.js
│   │       ├── students.js
│   │       ├── analytics.js
│   │       ├── prediction.js
│   │       ├── risk.js
│   │       ├── dataset.js
│   │       └── reports.js
│   │
│   └── icons/
│
└── tests/
    ├── test_auth.py
    ├── test_students.py
    ├── test_analytics.py
    ├── test_prediction.py
    ├── test_risk.py
    └── test_dataset.py
```

---

# 22. Dependency Flow

Bagian ini penting agar tidak terjadi circular dependency.

```text
routes
  ↓
services
  ↓
database / ml / data processing
```

Bukan:

```text
database → routes
```

atau:

```text
services → templates
```

Service tidak boleh bergantung langsung pada HTML.

---

# 23. Contoh Request Flow Dashboard

Ketika user membuka:

```text
/dashboard
```

alur:

```text
Browser
   ↓
dashboard.py
   ↓
┌──────────────────────────────┐
│ Analytics Service            │
│ Risk Service                 │
│ Insight Service              │
└──────────────┬───────────────┘
               ↓
            MySQL
               ↓
        Processed Results
               ↓
          dashboard.py
               ↓
        dashboard/index.html
               ↓
         JavaScript
               ↓
             Charts
```

---

# 24. Contoh Request Flow Dataset

```text
Admin
 ↓
Upload CSV
 ↓
dataset.py
 ↓
data_cleaning_service.py
 ↓
Validate
 ↓
Detect:
 ├─ Missing
 ├─ Duplicate
 ├─ Invalid
 ├─ Type Error
 └─ Outlier
 ↓
Cleaning Preview
 ↓
Admin Confirm
 ↓
Apply Cleaning
 ↓
Processed Dataset
 ↓
Database
```

---

# 25. Contoh Request Flow Risiko

```text
Academic Records
       ↓
Risk Service
       ↓
Current GPA
       ↓
Previous GPA
       ↓
GPA Change
       ↓
Attendance
       ↓
Score Trend
       ↓
Study Hours
       ↓
Risk Score
       ↓
Risk Level
       ↓
Risk Factors
       ↓
Early Warning
       ↓
risk_assessments
```

Kemudian:

```text
risk_assessments
       ↓
Dashboard
       ↓
Students Requiring Attention
```

---

# 26. Contoh Request Flow Analytics

```text
MySQL
 ↓
academic_records
 ↓
Analytics Service
 ↓
Pandas / NumPy
 ↓
Calculated Dataset
 ↓
JSON API
 ↓
JavaScript
 ↓
Chart
```

---

# 27. Contoh Request Flow Machine Learning

```text
CSV / Database
      ↓
Processed Dataset
      ↓
ML Preprocessing
      ↓
Feature Selection
      ↓
Train/Test Split
      ↓
┌───────────────┐
│ Linear        │
│ Random Forest │
│ Gradient Boost│
└───────┬───────┘
        ↓
Evaluation
        ↓
MAE / RMSE / R²
        ↓
Best Model
        ↓
models/
        ↓
Prediction Service
```

---

# 28. Frontend Architecture

Frontend menggunakan layout:

```text
┌─────────────────────────────────────────┐
│ Sidebar │ Topbar                         │
│         ├────────────────────────────────┤
│         │                                │
│         │ Main Content                   │
│         │                                │
│         │                                │
│         └────────────────────────────────┤
└─────────────────────────────────────────┘
```

`base.html` menjadi template utama.

Contoh:

```html
{% extends "base.html" %}
```

Kemudian setiap halaman hanya mengisi bagian content.

---

# 29. Design System

Semua halaman harus menggunakan sistem desain yang sama.

### Font

```text
DM Sans
```

### Light

```text
Background: #F7F7F5
Surface:    #FFFFFF
Border:     #E5E5E3
Text:       #171717
Secondary:  #737373
Muted:      #A3A3A3
Accent:     #262626
```

### Dark

```text
Background: #111111
Surface:    #181818
Border:     #2A2A2A
Text:       #F5F5F5
Secondary:  #A3A3A3
Muted:      #737373
Accent:     #E5E5E5
```

Status:

```text
LOW     → muted green
MEDIUM  → muted amber
HIGH    → muted red
```

Warna status hanya digunakan untuk informasi semantik.

---

# 30. Responsive Architecture

### Desktop

```text
Sidebar 240px
+
Main Content
```

### Tablet

```text
Collapsed Sidebar
+
Main Content
```

### Mobile

```text
Topbar
   ↓
Off-canvas Sidebar
   ↓
Single Column Content
```

Chart:

```text
Desktop → 2 columns
Mobile  → 1 column
```

KPI:

```text
Desktop → 4 columns
Mobile  → 2 columns
```

---

# 31. Error Handling

Sistem harus mempunyai kondisi:

```text
Loading
Empty
Error
Success
```

Contoh Analytics:

```text
Loading...
```

Jika tidak ada data:

```text
No academic data available.
```

Jika API gagal:

```text
Unable to load analytics data.
Try again.
```

Jangan menampilkan chart kosong seolah-olah data tersedia.

---

# 32. Security Architecture

Minimal:

```text
Password Hashing
Session Security
Role Authorization
CSRF Protection
Environment Variables
Input Validation
File Validation
```

`.env`:

```text
SECRET_KEY=
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
```

`.env` tidak boleh masuk Git.

`.gitignore` minimal:

```text
.env
__pycache__/
*.pyc
venv/
data/raw/*
data/processed/*
ml/models/*
```

Jika dataset/model memang ingin disimpan di repository, aturan `.gitignore` dapat disesuaikan.

---

# 33. Prinsip Penting Saat Implementasi

### Jangan membuat semua logic di `app.py`

Buruk:

```text
app.py
 ├── login
 ├── database
 ├── analytics
 ├── ML
 ├── risk
 ├── report
 └── dashboard
```

Gunakan:

```text
app.py
 ↓
Routes
 ↓
Services
 ↓
Database / ML
```

---

### Jangan membuat hasil palsu

Hindari:

```javascript
const averageGPA = 3.42;
```

Gunakan:

```text
Database
 ↓
Backend
 ↓
API
 ↓
Frontend
```

---

### Jangan hardcode hasil ML

Model terbaik harus berdasarkan:

```text
MAE
RMSE
R²
```

hasil training aktual.

---

### Jangan hardcode risk mahasiswa

Risk harus dihitung berdasarkan data aktual dan konfigurasi threshold.

---

# 34. Final System Flow

Pada akhirnya seluruh sistem akan membentuk pipeline:

```text
                    ┌──────────────┐
                    │     CSV      │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  Validation  │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Data Cleaning │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  Processed   │
                    │    Data      │
                    └──────┬───────┘
                           ↓
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
      Analytics         Risk Engine       ML
          ↓                ↓                ↓
      Charts          Risk Level       Prediction
          │                │                │
          └────────────────┼────────────────┘
                           ↓
                    ┌──────────────┐
                    │   Insights   │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  Dashboard   │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Reports    │
                    └──────────────┘
```
