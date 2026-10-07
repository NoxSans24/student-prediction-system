# REPORT_SPECIFICATION.md

Kita lanjut ke **Report & Export Specification**. Bagian ini menentukan bagaimana seluruh hasil analisis platform dikemas menjadi laporan yang bisa dibaca, diunduh, dan digunakan kembali.

Prinsipnya:

> **Report adalah output dari data dan engine yang sudah ada, bukan tempat membuat perhitungan baru.**

---

# 1. Tujuan Reports

Reports menggabungkan hasil dari:

```text
Data
 ↓
Analytics
 ↓
Machine Learning
 ↓
Risk Analysis
 ↓
Insights
 ↓
Reports
```

Report digunakan untuk memberikan dokumentasi yang lebih lengkap dibanding Dashboard.

---

# 2. Jenis Report

Berdasarkan scope project, terdapat 4 jenis report utama:

```text
Reports
├── Overall Performance Report
├── Student Report
├── Risk Report
└── ML Report
```

Masing-masing mempunyai tujuan berbeda.

---

# 3. Overall Performance Report

Tujuan:

> Memberikan gambaran keseluruhan performa akademik mahasiswa.

Isi utama:

```text
Overall Performance Report
│
├── Report Information
├── Summary
├── GPA Statistics
├── Attendance Statistics
├── Performance Distribution
├── GPA Trend
├── GPA by Major
├── Academic Insights
└── Risk Summary
```

---

# 4. Report Information

Bagian awal laporan:

```text
Student Performance Analytics
Overall Performance Report

Generated At:
07 October 2026

Dataset:
Academic Dataset

Period:
Semester 1 - Semester 4
```

Informasi harus berasal dari data aktual.

---

# 5. Overall Summary

Contoh:

```text
Total Students        250
Average GPA           3.24
Average Attendance    86.7%
At Risk               32
```

Angka harus diambil dari database/analytics service.

Tidak boleh disimpan sebagai nilai statis di template.

---

# 6. GPA Statistics

Report dapat menampilkan:

```text
Average GPA
Highest GPA
Lowest GPA
Median GPA
```

Contoh:

```text
GPA Statistics

Average       3.24
Highest       4.00
Lowest        1.82
Median        3.31
```

Jika statistik tertentu belum tersedia dari engine, report service harus menghitungnya dari data sumber yang valid.

---

# 7. Performance Distribution

Menampilkan distribusi kategori:

```text
Excellent
Good
Average
Poor
```

Contoh:

```text
Excellent    18%
Good         47%
Average      29%
Poor          6%
```

Visualisasi dapat berupa:

* table
* chart
* percentage summary

---

# 8. GPA Trend

Report menampilkan GPA berdasarkan semester.

```text
Semester    Average GPA
1              3.12
2              3.18
3              3.26
4              3.31
```

Visualisasi:

> Line chart

Untuk PDF, chart dapat dirender menjadi image menggunakan Matplotlib.

---

# 9. GPA by Major

Menampilkan:

```text
Major
Average GPA
Student Count
```

Contoh:

| Major                | Students | Average GPA |
| -------------------- | -------: | ----------: |
| Informatics          |      120 |        3.31 |
| Information Systems  |       80 |        3.24 |
| Computer Engineering |       50 |        3.18 |

Data harus berasal dari Analytics Service.

---

# 10. Academic Insights

Report dapat memasukkan hasil dari:

```text
Insight Service
```

Contoh:

> Average GPA increased compared with the previous semester.

> Final score shows the strongest positive correlation with GPA among the analyzed factors.

Insight harus sama-sama berasal dari data aktual seperti Dashboard.

---

# 11. Risk Summary

Overall Report juga dapat menyertakan:

```text
Low Risk       180
Medium Risk     48
High Risk      22
```

Kemudian:

> 22 students are currently classified as high risk.

Risk level berasal dari **Risk Engine**, bukan dihitung ulang oleh Report Service.

---

# 12. Student Report

Student Report berfokus pada satu mahasiswa.

Flow:

```text
Select Student
      ↓
Student Profile
      ↓
Academic Records
      ↓
Analytics
      ↓
Risk Assessment
      ↓
Generate Student Report
```

---

# 13. Student Report Content

Struktur:

```text
Student Report
│
├── Student Information
├── Current Academic Performance
├── GPA History
├── Attendance History
├── Score Performance
├── Study Hours
├── Risk Assessment
├── Early Warnings
└── Academic Summary
```

---

# 14. Student Information

Contoh:

```text
Student ID    : 20240001
Name          : Muhammad
Major         : Informatics
Semester      : 4
```

Data berasal dari tabel:

```text
students
```

---

# 15. Current Academic Performance

Menampilkan:

```text
Current GPA
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours
Academic Status
Risk Level
```

Contoh:

```text
Current GPA        3.42
Attendance         91%
Assignment         86
Midterm            82
Final              88
Study Hours        16
Risk Level         Low
```

---

# 16. GPA History

Menampilkan histori GPA:

```text
Semester    GPA
1           3.10
2           3.25
3           3.31
4           3.42
```

Visualisasi:

> Line chart

---

# 17. Score Performance

Menampilkan:

```text
Assignment
Midterm
Final
```

Contoh table:

| Semester | Assignment | Midterm | Final |
| -------- | ---------: | ------: | ----: |
| 1        |         78 |      75 |    81 |
| 2        |         82 |      79 |    84 |
| 3        |         85 |      81 |    86 |
| 4        |         86 |      82 |    88 |

---

# 18. Risk Assessment

Student Report mengambil hasil:

```text
Risk Engine
```

Contoh:

```text
Risk Level
LOW

Risk Score
18

Main Factors
- Stable GPA
- Good attendance
- Positive GPA trend
```

Jika risk assessment tidak tersedia:

```text
Risk assessment is not available.
```

Jangan membuat risk level baru hanya untuk report.

---

# 19. Early Warning

Jika tersedia:

```text
Early Warnings
```

Contoh:

> Attendance decreased significantly compared with the previous semester.

atau:

> GPA declined compared with the previous semester.

Jika tidak ada warning:

> No significant early warning detected.

---

# 20. Risk Report

Risk Report berfokus pada mahasiswa yang membutuhkan perhatian.

Struktur:

```text
Risk Report
│
├── Risk Summary
├── Risk Distribution
├── High Risk Students
├── Medium Risk Students
├── Main Risk Factors
└── Early Warnings
```

---

# 21. Risk Distribution

Contoh:

| Risk Level | Students | Percentage |
| ---------- | -------: | ---------: |
| Low        |      180 |        72% |
| Medium     |       48 |      19.2% |
| High       |       22 |       8.8% |

Angka dihitung dari Risk Engine.

---

# 22. High Risk Students

Tabel:

| Student   | Major               |  GPA | Attendance | Change | Risk |
| --------- | ------------------- | ---: | ---------: | -----: | ---- |
| Student A | Informatics         | 2.31 |        68% |  -0.42 | High |
| Student B | Information Systems | 2.45 |        71% |  -0.31 | High |

Fields mengikuti kebutuhan Dashboard:

```text
Student
Major
GPA
Attendance
Change
Risk
```

---

# 23. Main Risk Factors

Report dapat mengelompokkan faktor risiko:

```text
Risk Factors

Low GPA                  18 students
Low Attendance           14 students
GPA Decline              12 students
Score Decline             9 students
Low Study Hours           7 students
```

Data harus berasal dari risk assessment.

---

# 24. ML Report

ML Report berfokus pada performa model Machine Learning.

Struktur:

```text
ML Report
│
├── Dataset Information
├── Features
├── Target
├── Train/Test Information
├── Model Comparison
├── Best Model
└── Evaluation Metrics
```

---

# 25. Dataset Information

Contoh:

```text
Dataset:
Academic Dataset

Total Records:
1,250

Features:
6

Target:
GPA
```

---

# 26. ML Features

Report menampilkan:

```text
Features

- Semester
- Attendance
- Assignment Score
- Midterm Score
- Final Score
- Study Hours

Target

- GPA
```

---

# 27. Model Comparison

Contoh:

| Model             |  MAE | RMSE |   R² |
| ----------------- | ---: | ---: | ---: |
| Linear Regression | 0.21 | 0.29 | 0.82 |
| Random Forest     | 0.16 | 0.23 | 0.89 |
| Gradient Boosting | 0.14 | 0.20 | 0.92 |

Sekali lagi, angka tersebut hanya contoh.

Report harus mengambil hasil training aktual.

---

# 28. Best Model

Contoh:

```text
Best Model

Gradient Boosting Regressor

MAE      0.14
RMSE     0.20
R²       0.92
```

Best model berasal dari hasil `ML Specification`.

Report tidak menentukan model terbaik sendiri.

---

# 29. Export Formats

Reports mendukung:

```text
PDF
Excel
CSV
```

Pembagian:

| Format | Kegunaan                  |
| ------ | ------------------------- |
| PDF    | Laporan siap dibaca/cetak |
| Excel  | Analisis lanjutan         |
| CSV    | Data mentah/tabular       |

---

# 30. PDF Export

PDF digunakan untuk report yang bersifat presentable.

Contoh:

```text
┌──────────────────────────────────────┐
│ Student Performance Analytics        │
│ Overall Performance Report           │
├──────────────────────────────────────┤
│ Summary                              │
│                                      │
│ Total Students     250               │
│ Average GPA        3.24              │
│ Attendance         86.7%             │
│ At Risk            32                │
│                                      │
│ GPA Trend                           │
│ [Chart]                              │
│                                      │
│ Academic Insights                    │
│ ...                                  │
└──────────────────────────────────────┘
```

PDF menggunakan **ReportLab** sesuai technology stack project.

---

# 31. Excel Export

Excel digunakan ketika user ingin melakukan analisis lebih lanjut.

Contoh workbook:

```text
Overall Performance.xlsx

├── Summary
├── Students
├── Academic Records
├── Risk Analysis
└── Analytics
```

Excel dibuat menggunakan:

```text
Pandas
+
openpyxl
```

---

# 32. CSV Export

CSV cocok untuk data tabular.

Contoh:

```text
student_id,name,major,semester,gpa,attendance
20240001,Muhammad,Informatics,4,3.42,91
```

CSV tidak perlu memasukkan layout visual seperti PDF.

---

# 33. Report Service

Buat:

```text
services/
└── report_service.py
```

Fungsi:

```python
generate_overall_report()
generate_student_report()
generate_risk_report()
generate_ml_report()

export_pdf()
export_excel()
export_csv()
```

---

# 34. Report Data Flow

```text
                    ┌─────────────┐
                    │   Database  │
                    └──────┬──────┘
                           ↓
                ┌────────────────────┐
                │ Existing Services  │
                ├────────────────────┤
                │ Analytics          │
                │ Risk               │
                │ ML                 │
                │ Insights           │
                └─────────┬──────────┘
                          ↓
                  Report Service
                          ↓
             ┌────────────┼────────────┐
             ↓            ↓            ↓
            PDF         Excel         CSV
```

Dengan demikian Report Service tidak menduplikasi business logic.

---

# 35. Report Filters

Report harus mendukung filter yang relevan.

### Overall Report

```text
Major
Semester
Date / Period
```

### Student Report

```text
Student
Semester / Period
```

### Risk Report

```text
Risk Level
Major
Semester
```

### ML Report

```text
Dataset
Training Run
Model
```

Filter harus memengaruhi data report yang dihasilkan.

---

# 36. Report Naming

Nama file harus konsisten.

Contoh:

```text
overall-performance-report-2026-10-07.pdf

student-report-20240001-2026-10-07.pdf

risk-report-2026-10-07.xlsx

ml-report-2026-10-07.pdf
```

Tanggal dapat dibuat otomatis ketika report dibuat.

---

# 37. Report Metadata

Setiap report sebaiknya memiliki:

```text
Report Type
Generated At
Generated By
Dataset / Period
```

Contoh:

```text
Report Type: Risk Report
Generated By: admin
Generated At: 07 October 2026
Period: Semester 1–4
```

---

# 38. Error Handling

Jika export gagal:

```text
Unable to generate report.
Please try again.
```

Jangan menampilkan traceback Python kepada user.

Jika dataset kosong:

```text
No data available for this report.
```

Jika student tidak ditemukan:

```text
Student report cannot be generated because
the selected student was not found.
```

---

# 39. Security

Report harus mengikuti permission user.

### Admin

Dapat:

```text
Generate
View
Export
```

semua report.

### Analyst

Dapat:

```text
View
Generate
Export
```

sesuai scope yang ditentukan PRD.

Report tidak boleh memberikan akses ke data yang tidak boleh dilihat oleh role tersebut.

---

# 40. Report UI

Halaman Reports:

```text
Reports

Generate reports from your academic data.

┌─────────────────────────────────────────────┐
│ Overall Performance                         │
│ Complete academic performance overview      │
│                                             │
│ [Generate PDF] [Excel] [CSV]               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Student Report                              │
│ Detailed report for a selected student     │
│                                             │
│ [Select Student] [Generate]                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Risk Report                                 │
│ Students requiring academic attention       │
│                                             │
│ [Generate PDF] [Excel] [CSV]               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ML Report                                   │
│ Machine learning model evaluation           │
│                                             │
│ [Generate PDF] [Excel]                     │
└─────────────────────────────────────────────┘
```

Tetap mengikuti prinsip UI:

* DM Sans
* neutral
* clean
* minimal
* data-first
* SVG icons
* light/dark mode
* responsive

---

# 41. Definition of Done

Reports dianggap selesai jika:

* [ ] Overall Performance Report tersedia
* [ ] Student Report tersedia
* [ ] Risk Report tersedia
* [ ] ML Report tersedia
* [ ] PDF export tersedia
* [ ] Excel export tersedia
* [ ] CSV export tersedia
* [ ] Report menggunakan data aktual
* [ ] Report tidak membuat business logic baru
* [ ] Analytics Service digunakan
* [ ] Risk Engine digunakan
* [ ] ML result digunakan
* [ ] Insight Service digunakan
* [ ] Filter report tersedia
* [ ] Report metadata tersedia
* [ ] Naming file konsisten
* [ ] Empty state tersedia
* [ ] Error handling tersedia
* [ ] Permission berdasarkan role
* [ ] Responsive Reports UI
* [ ] Light/dark mode
* [ ] SVG icons
* [ ] Tidak ada hardcoded hasil analisis

---

# Posisi desain sekarang

Kita sudah sampai:

```text
01  PRD
02  Dashboard Specification
03  Data Specification
04  Database Schema
05  Data Cleaning Specification
06  Risk Engine Specification
07  ML Specification
08  Analytics Specification
09  Insight Specification
10  Report Specification ← SELESAI
```

Dan keseluruhan pipeline sekarang:

```text
                         ┌─────────────┐
                         │    DATA     │
                         └──────┬──────┘
                                ↓
                         ┌─────────────┐
                         │ VALIDATION  │
                         └──────┬──────┘
                                ↓
                         ┌─────────────┐
                         │   CLEANING  │
                         └──────┬──────┘
                                ↓
                    ┌───────────┴───────────┐
                    ↓                       ↓
               ANALYTICS                   ML
                    │                       │
             ┌──────┴──────┐                ↓
             ↓             ↓          GPA Prediction
        Dashboard       Insights            │
             │             │                │
             └──────┬──────┘                │
                    ↓                       │
               RISK ENGINE                  │
                    │                       │
                    ↓                       │
              Risk Analysis                 │
                    │                       │
                    └───────────┬───────────┘
                                ↓
                           REPORTS
                        ┌───────┼───────┐
                        ↓       ↓       ↓
                       PDF    Excel    CSV
```
