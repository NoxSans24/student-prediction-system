Siap. Kita rancang **PRD (Product Requirements Document)** untuk **Student Performance Analytics** terlebih dahulu sebelum masuk ke UI dan coding.

Saya akan buat PRD-nya dengan pendekatan yang cukup serius untuk proyek portofolio Data Science, tetapi tetap realistis untuk dikerjakan sebagai mahasiswa.

# Product Requirements Document

## Student Performance Analytics

**Version:** 1.0
**Product Type:** Web-based Data Science & Machine Learning Platform
**Target User:** Mahasiswa, dosen, akademik, atau analis
**Primary Focus:** Student Performance Analysis & Prediction

---

# 1. Product Overview

**Student Performance Analytics** adalah aplikasi berbasis web yang digunakan untuk mengelola, menganalisis, memvisualisasikan, dan memprediksi performa akademik mahasiswa berdasarkan data akademik dan faktor pendukungnya.

Aplikasi tidak hanya menampilkan data mahasiswa, tetapi juga menggunakan **Data Science dan Machine Learning** untuk menemukan pola performa, mendeteksi mahasiswa yang berisiko mengalami penurunan akademik, serta memberikan prediksi GPA.

### Core Concept

```text
Student Data
     ↓
Data Cleaning
     ↓
Data Analysis
     ↓
Visualization
     ↓
Machine Learning
     ↓
Prediction
     ↓
Risk Detection
     ↓
Actionable Insights
```

---

# 2. Problem Statement

Data akademik mahasiswa biasanya hanya digunakan untuk melihat nilai akhir atau IPK.

Masalahnya, pendekatan tersebut belum menjawab:

* Mengapa performa mahasiswa menurun?
* Apakah kehadiran berpengaruh terhadap GPA?
* Apakah waktu belajar berhubungan dengan performa?
* Mahasiswa mana yang berpotensi mengalami penurunan?
* Bagaimana performa mahasiswa berdasarkan semester?
* Faktor apa yang paling berpengaruh terhadap GPA?
* Berapa perkiraan GPA mahasiswa berdasarkan kondisi akademiknya?

**Student Performance Analytics** dibuat untuk menjawab pertanyaan tersebut berdasarkan data.

---

# 3. Product Goals

### Primary Goals

1. Menampilkan kondisi akademik mahasiswa secara jelas.
2. Membantu pengguna memahami pola performa akademik.
3. Menemukan faktor yang berkaitan dengan GPA.
4. Memprediksi GPA menggunakan Machine Learning.
5. Mendeteksi mahasiswa yang berpotensi mengalami masalah akademik.
6. Menghasilkan insight otomatis berdasarkan data aktual.
7. Menyediakan laporan yang dapat digunakan untuk evaluasi.

### Secondary Goals

* Menyediakan dataset management.
* Mempermudah proses data cleaning.
* Menyediakan visualisasi interaktif.
* Membandingkan beberapa model Machine Learning.
* Menyediakan export laporan.

---

# 4. Target Users

## 4.1 Admin

Admin memiliki akses penuh terhadap sistem.

**Permissions:**

* Mengelola dataset
* Menambahkan/mengubah/menghapus data mahasiswa
* Melakukan data cleaning
* Melatih model ML
* Melihat analytics
* Melakukan prediction
* Melihat risk analysis
* Membuat laporan

---

## 4.2 Analyst / User

User memiliki akses untuk melakukan analisis tanpa mengubah data utama.

**Permissions:**

* Dashboard
* Student analytics
* Student profile
* Prediction
* Risk analysis
* Dataset overview
* Reports

---

# 5. Core Features

Aplikasi akan memiliki **8 modul utama**.

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

---

# 6. Dashboard

Dashboard menjadi halaman pertama setelah login.

### KPI

Dashboard menampilkan:

* Total Students
* Average GPA
* Highest GPA
* Lowest GPA
* Average Attendance
* At-Risk Students

Contoh:

```text
Total Students       1,248
Average GPA           3.42
Average Attendance    87.4%
At Risk               86
```

### Charts

Dashboard memiliki:

**GPA Trend**

```text
Semester 1 → 3.21
Semester 2 → 3.30
Semester 3 → 3.42
Semester 4 → 3.51
```

**Performance Distribution**

```text
Excellent
Good
Average
Poor
```

**GPA by Major**

Membandingkan rata-rata GPA antar jurusan.

**Attendance vs GPA**

Scatter plot untuk melihat hubungan kehadiran dengan GPA.

### Automated Insights

Sistem menghasilkan insight berdasarkan data.

Contoh:

> Average GPA increased by 4.8% compared with the previous semester.

atau:

> Students with attendance below 75% have a significantly lower average GPA.

Insight **tidak boleh hardcoded**.

Semua insight harus berasal dari hasil analisis dataset.

---

# 7. Student Management

Halaman untuk melihat seluruh mahasiswa.

### Features

* Search
* Filter
* Sorting
* Pagination
* Student detail
* GPA status
* Risk status

Contoh tabel:

| Student        | Major              | Semester |  GPA | Attendance | Risk   |
| -------------- | ------------------ | -------: | ---: | ---------: | ------ |
| Muhammad Ihsan | Informatics        |        4 | 3.72 |        94% | Low    |
| Andi           | Information System |        3 | 2.81 |        76% | Medium |
| Budi           | Informatics        |        5 | 2.21 |        68% | High   |

### Filters

* Major
* Semester
* GPA
* Risk Level
* Attendance

---

# 8. Student Profile

Setiap mahasiswa memiliki halaman detail.

### Profile Information

```text
Name
Student ID
Major
Semester
```

### Academic Overview

```text
Current GPA
Average Attendance
Study Hours
Academic Status
Risk Level
```

### Academic History

Grafik GPA per semester.

```text
Semester 1   3.20
Semester 2   3.31
Semester 3   3.45
Semester 4   3.52
```

### Performance Factors

Menampilkan:

* Attendance
* Assignment Score
* Midterm Score
* Final Score
* Study Hours

### Risk Assessment

Contoh:

```text
Risk Level
LOW

Main Factors
✓ High attendance
✓ Stable GPA
✓ Consistent scores
```

---

# 9. Analytics

Ini menjadi salah satu bagian utama dari sisi **Data Science**.

## 9.1 GPA Analysis

Visualisasi:

* GPA distribution
* GPA by semester
* GPA by major
* GPA trend

---

## 9.2 Attendance Analysis

Analisis hubungan:

```text
Attendance ↔ GPA
```

Menggunakan scatter plot.

---

## 9.3 Study Hours Analysis

```text
Study Hours ↔ GPA
```

Tujuannya melihat apakah waktu belajar memiliki hubungan dengan performa akademik.

---

## 9.4 Score Analysis

Analisis:

* Assignment
* Midterm
* Final Exam

Terhadap GPA.

---

## 9.5 Correlation Analysis

Heatmap:

```text
                 GPA Attendance Study
GPA               1      0.62    0.48
Attendance       0.62     1      0.31
Study Hours      0.48    0.31     1
```

Nilai sebenarnya tentu dihitung dari dataset.

---

# 10. Machine Learning

Modul Machine Learning digunakan untuk memprediksi GPA.

### Candidate Models

Minimal tiga model:

1. Linear Regression
2. Random Forest Regressor
3. Gradient Boosting Regressor

Model dibandingkan berdasarkan:

* MAE
* RMSE
* R²

Contoh hasil:

| Model             |  MAE | RMSE |   R² |
| ----------------- | ---: | ---: | ---: |
| Linear Regression | 0.21 | 0.29 | 0.72 |
| Random Forest     | 0.15 | 0.21 | 0.84 |
| Gradient Boosting | 0.14 | 0.20 | 0.86 |

Kemudian sistem memilih model terbaik berdasarkan metrik evaluasi.

---

# 11. GPA Prediction

User dapat memasukkan kondisi akademik mahasiswa.

### Input

```text
Semester
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours
```

Kemudian sistem melakukan:

```text
Input
 ↓
Preprocessing
 ↓
Best ML Model
 ↓
Predicted GPA
```

Contoh output:

```text
Predicted GPA

3.48

Performance
Good

Prediction Confidence
Based on model evaluation
```

> Catatan penting: jangan menampilkan "confidence" jika model yang digunakan tidak benar-benar menghasilkan probabilitas/interval yang valid. Untuk model regresi biasa, lebih aman menampilkan **model + MAE/R²** atau rentang prediksi jika memang diimplementasikan.

---

# 12. Risk Analysis

Sistem mengidentifikasi mahasiswa yang membutuhkan perhatian.

### Risk Level

**LOW**

Mahasiswa memiliki performa stabil.

**MEDIUM**

Terdapat beberapa indikator penurunan.

**HIGH**

Terdapat indikator kuat bahwa mahasiswa membutuhkan perhatian.

### Potential Factors

Risk analysis dapat mempertimbangkan:

* GPA
* Attendance
* Score trend
* Study hours
* Previous semester GPA
* Assignment performance
* Midterm performance
* Final performance

---

# 13. Early Warning System

Sistem mendeteksi perubahan performa.

Contoh:

```text
Previous GPA
3.45

Current GPA
2.91

Change
-0.54
```

Sistem menghasilkan:

> Significant academic performance decline detected.

Early warning juga dapat muncul ketika:

```text
Attendance < threshold
GPA decreases significantly
Score trend decreases
```

Threshold sebaiknya dapat dikonfigurasi, bukan semuanya hardcoded.

---

# 14. Dataset Management

Admin dapat mengelola dataset.

### Upload

Format:

```text
CSV
```

### Dataset Preview

Menampilkan:

* Rows
* Columns
* Missing values
* Duplicate rows
* Data types

Contoh:

```text
Rows             1,248
Columns             12
Missing Values      24
Duplicates           7
```

---

# 15. Data Cleaning

Sistem membantu membersihkan dataset.

### Detection

* Missing values
* Duplicate data
* Invalid GPA
* Invalid attendance
* Invalid score
* Incorrect data types
* Outliers

### Cleaning Report

Contoh:

```text
Missing values        24
Duplicates             7
Invalid GPA            3
Invalid attendance     5

Total records cleaned: 39
```

User sebaiknya dapat melihat perubahan sebelum menerapkan cleaning.

---

# 16. Automated Data Insights

Sistem menghasilkan kesimpulan dari data.

Contoh:

> Attendance shows a moderate positive relationship with GPA.

> Informatics students have the highest average GPA among available majors.

> 8.4% of students are currently classified as high risk.

> Average GPA increased from semester 3 to semester 4.

Semua insight dihitung secara dinamis dari dataset.

---

# 17. Reports

Sistem menyediakan beberapa jenis laporan.

### Reports

**Overall Performance Report**

Berisi:

* Total students
* Average GPA
* GPA distribution
* Attendance statistics
* Major comparison

**Student Report**

Berisi profil dan riwayat akademik mahasiswa.

**Risk Report**

Berisi:

* Low risk
* Medium risk
* High risk
* Risk factors

**Machine Learning Report**

Berisi:

* Dataset
* Features
* Models
* MAE
* RMSE
* R²
* Best model

### Export

Target:

* PDF
* Excel
* CSV

---

# 18. Search & Filtering

Global search dapat mencari:

```text
Student name
Student ID
Major
```

Filter tersedia berdasarkan:

```text
Major
Semester
GPA
Risk
Attendance
```

---

# 19. Authentication

Jika authentication digunakan:

### Login

```text
Email / Username
Password
```

### Roles

```text
Admin
Analyst
```

Admin memiliki akses penuh.

Analyst memiliki akses analisis tetapi tidak dapat mengubah dataset utama.

---

# 20. UI / UX Requirements

Design menggunakan:

### Font

**DM Sans**

Karena kita sudah sepakati font ini sebagai font utama.

### Style

```text
Modern
Clean
Neutral
Minimal
Data-focused
Friendly
```

### Light Mode

```text
Background    #F7F7F5
Surface       #FFFFFF
Border        #E5E5E3
Primary Text  #171717
Secondary     #737373
Muted         #A3A3A3
Accent        #262626
```

### Dark Mode

```text
Background    #111111
Surface       #181818
Border        #2A2A2A
Primary Text  #F5F5F5
Secondary     #A3A3A3
Muted         #737373
Accent        #E5E5E5
```

Status menggunakan warna secara terbatas:

```text
Low       → muted green
Medium    → muted amber
High      → muted red
```

Tidak menggunakan neon.

---

# 21. Icon System

**SVG icons only.**

Tidak menggunakan:

```text
Unicode emoji
Emoji icons
Random icon styles
```

Icon harus memiliki satu visual language yang konsisten.

Untuk project ini kita bisa menggunakan **Lucide SVG** atau custom SVG.

---

# 22. Main Layout

Struktur:

```text
┌──────────────────────────────────────────────┐
│ Sidebar │ Topbar                             │
│         ├────────────────────────────────────┤
│         │                                    │
│         │ Main Content                       │
│         │                                    │
│         │                                    │
│         │                                    │
│         └────────────────────────────────────┘
└──────────────────────────────────────────────┘
```

### Sidebar

```text
Overview
 ├─ Dashboard
 ├─ Students
 └─ Analytics

Intelligence
 ├─ Prediction
 └─ Risk Analysis

Data
 ├─ Dataset
 └─ Reports

Settings
```

Sidebar desktop sekitar **240px**.

Mobile menggunakan off-canvas navigation.

---

# 23. Responsive Requirements

### Desktop

Dashboard:

```text
2-column charts
Full student table
Sidebar visible
```

### Tablet

```text
Reduced sidebar
2-column where possible
```

### Mobile

```text
Sidebar → Off canvas
Charts → 1 column
Table → Student cards / horizontal scrolling
KPI → 2 columns
```

---

# 24. Non-Functional Requirements

### Performance

* Dashboard harus cepat ditampilkan.
* Chart tidak boleh menyebabkan UI terasa berat.
* Dataset besar harus diproses secara efisien.

### Usability

User dapat memahami dashboard tanpa membaca dokumentasi panjang.

### Responsiveness

Target:

```text
Desktop
Tablet
Mobile
```

### Maintainability

Struktur project harus modular.

---

# 25. Suggested Technology Stack

Untuk proyek ini saya menyarankan:

### Frontend

```text
HTML
CSS
JavaScript
```

atau jika ingin lebih advanced:

```text
React
```

Namun untuk project mahasiswa dan portfolio, kita bisa tetap menggunakan frontend sederhana jika backend sudah kuat.

### Backend

**Python + Flask**

Karena cocok dengan Data Science dan Machine Learning.

### Data Science

```text
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
```

### Database

Untuk awal:

```text
MySQL
```

atau SQLite untuk prototype.

### ML

```text
Scikit-learn
```

### Export

```text
Pandas → Excel/CSV
ReportLab → PDF
```

---

# 26. High-Level Architecture

```text
                 ┌──────────────────┐
                 │      User        │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Web Interface  │
                 │ HTML/CSS/JS      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Flask Backend  │
                 └────────┬─────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
     ┌─────────┐    ┌────────────┐   ┌──────────┐
     │ MySQL   │    │ Data       │   │ ML Model │
     │ Database│    │ Processing │   │          │
     └─────────┘    └────────────┘   └──────────┘
                          │                │
                          └───────┬────────┘
                                  ▼
                         ┌────────────────┐
                         │ Analytics      │
                         │ & Prediction   │
                         └────────────────┘
```

---

# 27. Data Flow

```text
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
Train/Test Split
      ↓
Model Training
      ↓
Model Evaluation
      ↓
Best Model
      ↓
Prediction
      ↓
Dashboard / Report
```

---

# 28. MVP

Agar project tidak terlalu besar sejak awal, **MVP** kita adalah:

### Phase 1 — Data

* Dataset
* Data cleaning
* Database
* Student management

### Phase 2 — Analytics

* Dashboard
* GPA analysis
* Attendance analysis
* Study hours analysis
* Correlation analysis

### Phase 3 — Machine Learning

* Model training
* Model comparison
* GPA prediction

### Phase 4 — Intelligence

* Risk detection
* Early warning
* Automated insights

### Phase 5 — Reporting

* PDF
* Excel
* CSV

### Phase 6 — Polish

* Authentication
* Light/dark mode
* Responsive design
* UI animations
* Optimization

---

# 29. Success Metrics

Project dianggap berhasil jika:

* Dataset dapat di-upload dan divalidasi.
* Data dapat dibersihkan.
* Dashboard menampilkan statistik aktual.
* User dapat mencari dan memfilter mahasiswa.
* Analytics menghasilkan visualisasi berdasarkan dataset.
* Minimal 3 model ML dapat dibandingkan.
* Model terbaik dapat digunakan untuk prediksi.
* Sistem dapat mengidentifikasi risiko mahasiswa.
* Insight dibuat berdasarkan data aktual.
* Report dapat diekspor.
* UI responsive dan nyaman digunakan.

---

# 30. Positioning Project

Yang paling penting, project ini jangan terlihat seperti:

> **"Website CRUD mahasiswa yang ditambahkan grafik."**

Kita ingin positioning-nya menjadi:

> **"Data Science platform untuk memahami, memprediksi, dan mendeteksi risiko performa akademik mahasiswa."**

Jadi **CRUD hanya menjadi pendukung**, sedangkan inti project adalah:

```text
DATA
 ↓
ANALYSIS
 ↓
INSIGHT
 ↓
MACHINE LEARNING
 ↓
PREDICTION
 ↓
EARLY WARNING
```

