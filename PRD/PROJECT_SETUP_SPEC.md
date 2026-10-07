# PROJECT_SETUP_SPEC.md

## 1. Tujuan

Dokumen ini menjadi panduan setup awal project **Student Performance Analytics** sebelum masuk ke tahap implementasi fitur.

Setup harus menghasilkan environment yang siap untuk:

* Flask
* MySQL
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* ReportLab
* Excel export
* Frontend HTML/CSS/JavaScript
* Authentication
* Machine Learning
* Dataset processing

Prinsip utama:

> **Environment → Database → Struktur Project → Configuration → Seed Data → Run → Git**

---

# 2. Prerequisite

Pastikan perangkat sudah memiliki:

| Software | Keterangan              |
| -------- | ----------------------- |
| Python   | Disarankan Python 3.11+ |
| MySQL    | Database utama          |
| VS Code  | Editor                  |
| Git      | Version control         |
| Browser  | Chrome/Edge/Firefox     |

Opsional:

| Software        | Fungsi           |
| --------------- | ---------------- |
| MySQL Workbench | GUI MySQL        |
| XAMPP           | Alternatif MySQL |
| Laragon         | Alternatif MySQL |
| Postman         | Testing API      |

Project tidak membutuhkan Node.js untuk MVP karena frontend menggunakan:

* HTML
* CSS
* Vanilla JavaScript
* Jinja2
* Chart.js

---

# 3. Struktur Project Final

Buat struktur awal:

```text
student-performance-analytics/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
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
│   ├── schema.sql
│   └── seed.sql
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
│   ├── components/
│   ├── auth/
│   ├── dashboard/
│   ├── students/
│   ├── analytics/
│   ├── prediction/
│   ├── risk/
│   ├── dataset/
│   ├── reports/
│   ├── settings/
│   └── errors/
│
├── static/
│   ├── css/
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   ├── utilities.css
│   │   └── pages/
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── theme.js
│   │   ├── sidebar.js
│   │   ├── charts.js
│   │   └── pages/
│   │
│   └── icons/
│
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_students.py
    ├── test_analytics.py
    ├── test_risk.py
    ├── test_prediction.py
    └── test_dataset.py
```

---

# 4. Virtual Environment

Project harus menggunakan virtual environment agar dependency tidak bercampur dengan Python global.

Windows:

```bash
python -m venv .venv
```

Aktifkan:

```bash
.venv\Scripts\activate
```

Jika berhasil, terminal biasanya menampilkan:

```text
(.venv)
```

Untuk keluar:

```bash
deactivate
```

---

# 5. requirements.txt

Dependency utama:

```txt
Flask
python-dotenv
mysql-connector-python
pandas
numpy
scikit-learn
matplotlib
seaborn
reportlab
openpyxl
joblib
```

Testing:

```txt
pytest
```

Development server dan dependency tambahan tidak perlu ditambahkan jika belum digunakan.

Install:

```bash
pip install -r requirements.txt
```

Verifikasi:

```bash
pip list
```

---

# 6. Environment Configuration

Gunakan `.env` untuk informasi sensitif.

Contoh:

```env
SECRET_KEY=change-this-secret-key

DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_performance_analytics
DB_USER=root
DB_PASSWORD=

FLASK_ENV=development
```

Jika MySQL memiliki password:

```env
DB_PASSWORD=your_mysql_password
```

Jangan menaruh:

```python
DB_PASSWORD = "password123"
```

langsung di source code.

---

# 7. `.gitignore`

File `.gitignore` harus dibuat sejak awal.

Contoh:

```gitignore
# Python
__pycache__/
*.py[cod]

# Virtual environment
.venv/
venv/
env/

# Environment
.env

# Flask
instance/

# Database/local files
*.db

# Machine Learning
*.pkl
*.joblib

# Generated data
data/raw/*
data/processed/*
data/reports/*

# Keep folder structure
!data/raw/.gitkeep
!data/processed/.gitkeep
!data/reports/.gitkeep

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Test/cache
.pytest_cache/
.coverage
htmlcov/
```

Tujuannya agar credential, environment, model lokal, dataset, dan file hasil generate tidak ikut masuk repository secara tidak sengaja.

---

# 8. Database Setup

Nama database:

```text
student_performance_analytics
```

Buat database:

```sql
CREATE DATABASE IF NOT EXISTS student_performance_analytics;
```

Kemudian:

```sql
USE student_performance_analytics;
```

Setelah itu jalankan `database/schema.sql`.

Schema menggunakan 7 tabel utama:

```text
users
students
academic_records
risk_assessments
prediction_results
datasets
dataset_cleaning_logs
```

Relasi utama:

```text
users
 │
 ├── datasets
 │      │
 │      └── dataset_cleaning_logs
 │
students
 │
 ├── academic_records
 ├── risk_assessments
 └── prediction_results
```

---

# 9. Urutan Database Setup

Urutan yang harus digunakan:

```text
1. Create database
        ↓
2. Create users
        ↓
3. Create students
        ↓
4. Create academic_records
        ↓
5. Create risk_assessments
        ↓
6. Create prediction_results
        ↓
7. Create datasets
        ↓
8. Create dataset_cleaning_logs
        ↓
9. Insert seed data
```

Foreign key harus dibuat setelah tabel parent tersedia.

---

# 10. Seed Data

Project membutuhkan data awal untuk development.

Seed data minimal harus mencakup:

### Users

Minimal:

```text
Admin
Analyst
```

Contoh:

```text
username: admin
role: admin

username: analyst
role: analyst
```

Password harus disimpan dalam bentuk hash.

Jangan menggunakan:

```text
password = "admin123"
```

langsung di database.

---

# 11. Student Seed Data

Development membutuhkan beberapa mahasiswa agar Dashboard dan Analytics dapat diuji.

Contoh struktur:

```text
student_id
name
major
current_semester
```

Contoh data:

```text
20240001
Andi Pratama
Informatics
4

20240002
Budi Santoso
Information Systems
4

20240003
Citra Lestari
Informatics
3
```

Jumlah data development sebaiknya cukup untuk menguji:

* pagination
* search
* filtering
* chart
* risk
* analytics
* prediction

Untuk pengembangan awal, data sintetis dapat digunakan.

---

# 12. Academic Records

Setiap student harus dapat memiliki beberapa semester.

Contoh:

```text
Student
│
├── Semester 1
├── Semester 2
├── Semester 3
└── Semester 4
```

Contoh record:

```text
Semester: 1
GPA: 3.20
Attendance: 88
Assignment: 82
Midterm: 78
Final: 84
Study Hours: 12
```

Kemudian semester berikutnya memiliki data berbeda.

Ini penting karena beberapa fitur membutuhkan **trend**:

```text
GPA Trend
Attendance Change
Score Trend
Risk Analysis
Early Warning
```

---

# 13. Database Connection

File:

```text
database/connection.py
```

Tanggung jawab:

* membaca konfigurasi database
* membuat connection
* menyediakan database cursor
* menangani connection error

Route tidak boleh langsung mengatur detail koneksi MySQL.

Arsitektur:

```text
Route
 ↓
Service
 ↓
Database Connection
 ↓
MySQL
```

Bukan:

```text
Route
 ↓
SQL + Business Logic + MySQL
```

---

# 14. Flask Application

`app.py` menjadi entry point aplikasi.

Flow:

```text
app.py
 │
 ├── Load configuration
 │
 ├── Create Flask app
 │
 ├── Register Blueprints
 │
 ├── Configure error handlers
 │
 └── Run application
```

Blueprint:

```text
auth
dashboard
students
analytics
prediction
risk
dataset
reports
```

---

# 15. Configuration Layer

Gunakan:

```text
config.py
```

dan:

```text
config/settings.py
```

Konfigurasi minimal:

```text
SECRET_KEY
DATABASE
UPLOAD_FOLDER
MAX_CONTENT_LENGTH
SESSION SETTINGS
ML MODEL PATH
```

Contoh konfigurasi file upload:

```text
data/raw/
```

Maximum upload size harus dibatasi untuk mencegah upload file yang terlalu besar.

---

# 16. Folder Data

Struktur:

```text
data/
├── raw/
├── processed/
└── reports/
```

### `raw/`

Dataset asli.

```text
data/raw/students.csv
```

File di folder ini **tidak boleh dimodifikasi** oleh proses cleaning.

### `processed/`

Dataset setelah validasi/cleaning:

```text
data/processed/students_cleaned.csv
```

### `reports/`

File report hasil generate:

```text
data/reports/
```

---

# 17. Dataset Lifecycle

Dataset mengikuti flow:

```text
Upload
 ↓
Validation
 ↓
Preview
 ↓
Cleaning Preview
 ↓
Apply Cleaning
 ↓
Processed Dataset
 ↓
Analytics / Risk / ML
```

Jangan langsung:

```text
Upload → Training
```

karena dataset harus melewati validasi dan cleaning terlebih dahulu.

---

# 18. Dataset Status

Status dataset:

```text
uploaded
validated
cleaned
processed
failed
```

Contoh:

```text
students.csv
      ↓
uploaded
      ↓
validated
      ↓
cleaned
      ↓
processed
```

Jika validasi gagal:

```text
uploaded
   ↓
failed
```

---

# 19. ML Model Storage

Model yang sudah dilatih disimpan menggunakan `joblib`.

Contoh:

```text
ml/models/
├── best_model.joblib
└── model_metadata.json
```

Metadata dapat menyimpan:

```json
{
    "model_name": "RandomForestRegressor",
    "mae": 0.18,
    "rmse": 0.24,
    "r2": 0.91
}
```

Nilai di atas hanya contoh format.

**Nilai sebenarnya harus berasal dari hasil training.**

---

# 20. Model Training Flow

Flow:

```text
Processed Dataset
        ↓
Preprocessing
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
Compare Metrics
        ↓
Best Model
        ↓
Save Model
```

Model tidak boleh dipilih berdasarkan asumsi.

Pemilihan berdasarkan:

* MAE
* RMSE
* R²

dari hasil aktual training.

---

# 21. Initial Application Flow

Saat project pertama kali dijalankan:

```text
Browser
   ↓
Flask
   ↓
Login
   ↓
Dashboard
   ↓
API
   ↓
Services
   ↓
MySQL
```

Jika belum login:

```text
Request
 ↓
Authentication Check
 ↓
Not authenticated
 ↓
Login
```

Jika sudah login:

```text
Request
 ↓
Authentication
 ↓
Authorization
 ↓
Service
 ↓
Response
```

---

# 22. Authentication Setup

Session hanya menyimpan informasi minimum:

```text
user_id
username
role
```

Jangan menyimpan:

```text
password
password_hash
```

di session.

Role:

```text
admin
analyst
```

---

# 23. Permission Test

Setelah authentication dibuat, lakukan pengujian:

### Admin

Harus bisa:

```text
Dashboard
Students
Add Student
Edit Student
Delete Student
Analytics
Prediction
Risk
Dataset
Upload Dataset
Cleaning
Train ML
Reports
Settings
```

### Analyst

Harus bisa:

```text
Dashboard
Students
Analytics
Prediction
Risk
Dataset Overview
Reports
Settings
```

Tetapi tidak boleh:

```text
Add Student
Delete Student
Upload Dataset
Apply Cleaning
Train ML
```

Backend tetap harus memblokir request meskipun tombol frontend disembunyikan.

---

# 24. Frontend Dependency

Frontend menggunakan:

```text
Jinja2
CSS
Vanilla JavaScript
Chart.js
SVG
DM Sans
```

Tidak diperlukan framework frontend untuk MVP.

Struktur:

```text
Browser
 │
 ├── HTML
 ├── CSS
 ├── JavaScript
 └── Chart.js
```

---

# 25. Icon System

Semua icon harus menggunakan SVG.

Tidak menggunakan:

```text
Unicode emoji
```

Contoh yang tidak digunakan:

```text
📊
👤
⚙️
🔔
```

Gunakan SVG untuk:

```text
Dashboard
Students
Analytics
Prediction
Risk
Dataset
Reports
Settings
Search
Notification
Theme
Menu
Edit
Delete
View
Download
Upload
```

Icon harus memiliki visual language yang konsisten.

---

# 26. Font Setup

Font utama:

```text
DM Sans
```

Hierarki:

```text
Page Title
28px / 600

Section Title
20px / 600

Card Title
16px / 600

Body
14px / 400

Secondary
13px / 400

Caption
12px / 400
```

Tujuannya tetap terasa modern dan tidak terlalu formal.

---

# 27. Theme Setup

Default theme dapat menggunakan:

```text
Light
```

dengan opsi:

```text
Dark
```

Gunakan:

```html
<html data-theme="light">
```

atau:

```html
<html data-theme="dark">
```

Theme preference disimpan di:

```text
localStorage
```

Contoh key:

```text
spa_theme
```

Nama key boleh disesuaikan saat implementasi.

---

# 28. Initial Light Theme

```text
Background    #F7F7F5
Surface       #FFFFFF
Border        #E5E5E3
Primary       #171717
Secondary     #737373
Muted         #A3A3A3
Accent        #262626
```

Status:

```text
Low       muted green
Medium    muted amber
High      muted red
```

Status color hanya digunakan ketika memang memiliki makna.

---

# 29. Initial Dark Theme

```text
Background    #111111
Surface       #181818
Border        #2A2A2A
Primary       #F5F5F5
Secondary     #A3A3A3
Muted         #737373
Accent        #E5E5E5
```

Dark mode bukan sekadar:

```css
filter: invert();
```

Tetapi menggunakan palette khusus.

---

# 30. Initial Layout

Desktop:

```text
┌──────────────────────────────────────────────┐
│ Sidebar │ Topbar                             │
│         ├────────────────────────────────────┤
│         │                                    │
│         │ Main Content                       │
│         │                                    │
│         │                                    │
│         │                                    │
└─────────┴────────────────────────────────────┘
```

Sidebar:

```text
240px
```

Main content menggunakan ruang yang tersedia.

---

# 31. Responsive Setup

Breakpoint:

```text
Desktop
>= 1200px

Tablet
768px - 1199px

Mobile
< 768px
```

Mobile:

```text
Sidebar
↓
Off-canvas
```

KPI:

```text
Desktop → 4 columns
Mobile  → 2 columns
```

Chart:

```text
Desktop → 2 columns
Mobile  → 1 column
```

---

# 32. Initial Flask Run

Setelah dependency dan database selesai:

```bash
python app.py
```

Aplikasi development biasanya tersedia melalui:

```text
http://127.0.0.1:5000
```

atau:

```text
http://localhost:5000
```

---

# 33. Initial Health Check

Sebelum membuat halaman Dashboard, aplikasi sebaiknya memiliki endpoint sederhana:

```text
GET /health
```

Response:

```json
{
    "success": true,
    "data": {
        "status": "ok"
    }
}
```

Tujuannya untuk memastikan Flask dapat berjalan.

---

# 34. Database Health Check

Selain Flask health check, lakukan pengecekan database.

Flow:

```text
GET /health
      ↓
Flask aktif
      ↓
Database connection
      ↓
MySQL aktif
```

Jika MySQL mati:

```text
Database connection failed
```

harus menghasilkan error yang jelas, bukan traceback mentah kepada user.

---

# 35. Development Workflow

Workflow standar:

```text
1. Activate .venv
        ↓
2. Start MySQL
        ↓
3. Check database
        ↓
4. Run Flask
        ↓
5. Open browser
        ↓
6. Develop feature
        ↓
7. Test
        ↓
8. Git commit
```

Setiap kali membuka project:

```bash
.venv\Scripts\activate
python app.py
```

---

# 36. Git Initialization

Jika project belum menggunakan Git:

```bash
git init
```

Kemudian:

```bash
git add .
```

Cek:

```bash
git status
```

Commit pertama:

```bash
git commit -m "chore: initialize project structure"
```

---

# 37. Repository Strategy

Repository hanya menyimpan:

```text
Source code
Schema
Configuration template
Documentation
Tests
```

Jangan menyimpan:

```text
.env
.venv/
password
database credential
raw private dataset
trained model besar
generated report
```

Jika membutuhkan contoh environment:

```text
.env.example
```

Contoh:

```env
SECRET_KEY=

DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_performance_analytics
DB_USER=root
DB_PASSWORD=
```

---

# 38. README.md

README minimal harus berisi:

```text
Student Performance Analytics
```

Kemudian:

### 1. Description

Menjelaskan platform:

> Web-based Data Science dan Machine Learning platform untuk memahami, memprediksi, dan mendeteksi risiko performa akademik mahasiswa.

### 2. Features

```text
Dashboard
Student Management
Analytics
GPA Prediction
Risk Analysis
Dataset Management
Reports
Authentication
```

### 3. Tech Stack

```text
Python
Flask
MySQL
Pandas
NumPy
Scikit-learn
Chart.js
HTML/CSS/JavaScript
```

### 4. Installation

```text
Clone
Create virtual environment
Install requirements
Configure .env
Setup database
Run Flask
```

### 5. Project Structure

Berikan struktur folder utama.

---

# 39. Development Environment Checklist

Sebelum masuk implementasi fitur, semua ini harus terpenuhi:

### Python

```text
[ ] Python terinstall
[ ] Virtual environment dibuat
[ ] Virtual environment aktif
[ ] requirements terinstall
```

### MySQL

```text
[ ] MySQL aktif
[ ] Database dibuat
[ ] schema.sql berhasil dijalankan
[ ] tabel berhasil dibuat
[ ] seed data berhasil dimasukkan
```

### Flask

```text
[ ] Flask dapat dijalankan
[ ] /health berhasil
[ ] database connection berhasil
```

### Environment

```text
[ ] .env dibuat
[ ] .env tidak masuk Git
[ ] .env.example tersedia
```

### Git

```text
[ ] git init
[ ] .gitignore
[ ] initial commit
```

### Frontend

```text
[ ] DM Sans
[ ] SVG icon system
[ ] Light theme
[ ] Dark theme
[ ] Responsive structure
```

---

# 40. Urutan Implementasi Setelah Setup

Setelah `PROJECT_SETUP_SPEC.md` selesai, implementasi tidak langsung dimulai dari Dashboard.

Urutan yang direkomendasikan:

```text
PROJECT SETUP
      ↓
FLASK FOUNDATION
      ↓
DATABASE CONNECTION
      ↓
AUTHENTICATION
      ↓
STUDENT CRUD
      ↓
ACADEMIC RECORDS
      ↓
DATASET MANAGEMENT
      ↓
DATA CLEANING
      ↓
ANALYTICS ENGINE
      ↓
RISK ENGINE
      ↓
ML TRAINING
      ↓
PREDICTION
      ↓
INSIGHT ENGINE
      ↓
DASHBOARD
      ↓
REPORTS
      ↓
RESPONSIVE + DARK MODE
      ↓
TESTING
      ↓
OPTIMIZATION
```

Ini mengikuti dependency antar fitur sehingga Dashboard tidak dibangun menggunakan data dummy yang nantinya harus dibongkar kembali.

---

# 41. Definition of Done — Project Setup

Setup dianggap selesai apabila:

* [ ] Project folder sudah sesuai struktur.
* [ ] `.venv` berhasil dibuat.
* [ ] Semua dependency berhasil di-install.
* [ ] `.env` berhasil dibuat.
* [ ] `.env` masuk `.gitignore`.
* [ ] `.env.example` tersedia.
* [ ] MySQL aktif.
* [ ] Database `student_performance_analytics` tersedia.
* [ ] Semua tabel berhasil dibuat.
* [ ] Foreign key berhasil.
* [ ] Seed user tersedia.
* [ ] Seed student tersedia.
* [ ] Seed academic records tersedia.
* [ ] Flask dapat dijalankan.
* [ ] `/health` bekerja.
* [ ] Flask dapat terhubung ke MySQL.
* [ ] Struktur frontend tersedia.
* [ ] Struktur ML tersedia.
* [ ] Folder dataset tersedia.
* [ ] Git sudah diinisialisasi.
* [ ] Initial commit berhasil.
* [ ] Tidak ada credential yang masuk repository.

---

# 42. Kondisi Akhir

Setelah tahap setup ini selesai, project harus berada pada kondisi:

```text
                STUDENT PERFORMANCE ANALYTICS
                           │
          ┌────────────────┴────────────────┐
          │                                 │
       FRONTEND                           BACKEND
          │                                 │
 HTML / CSS / JS                         Flask
 Jinja2                                  Routes
 Chart.js                                Services
 SVG                                     Database
          │                                 │
          └────────────────┬────────────────┘
                           │
                     DATA LAYER
                           │
                  ┌────────┴────────┐
                  │                 │
                MySQL          Dataset Files
                  │                 │
                  └────────┬────────┘
                           │
                      DATA SCIENCE
                           │
                 Pandas / NumPy
                           │
                      MACHINE
                      LEARNING
                           │
                    Scikit-learn
```

Dengan demikian, tahap berikutnya bukan lagi setup environment, melainkan **implementasi `FLASK_FOUNDATION_SPEC.md`**: application factory, configuration, database connection, blueprint dasar, error handler, health check, dan struktur awal API.
