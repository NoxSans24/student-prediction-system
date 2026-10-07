# ANALYTICS_RISK_IMPLEMENTATION_SPEC.md

## 1. Tujuan

Tahap ini mengimplementasikan dua engine inti:

1. **Analytics Engine**
2. **Risk Engine**

Keduanya menggunakan data akademik yang sudah tersedia dan telah melalui proses validasi/cleaning.

```text
Processed Data
      ↓
 ┌────┴─────┐
 ▼          ▼
Analytics   Risk Engine
 │          │
 ▼          ▼
Charts     Risk Level
 │          │
 └────┬─────┘
      ▼
   Insights
      ↓
   Dashboard
```

---

# 2. Scope

### Analytics

* GPA Distribution
* GPA by Semester
* GPA by Major
* GPA Trend
* Attendance vs GPA
* Study Hours vs GPA
* Assignment Score vs GPA
* Midterm Score vs GPA
* Final Score vs GPA
* Correlation Heatmap
* Filtering
* API analytics

### Risk

* Current GPA
* Previous GPA
* GPA change
* Attendance
* Attendance change
* Score trend
* Study hours
* Risk score
* Risk level
* Risk factors
* Early warnings
* Risk recalculation

---

# 3. Struktur File

```text
services/
├── analytics_service.py
├── risk_service.py
└── ...

routes/
├── analytics.py
├── risk.py
└── ...

database/
└── repositories/
    ├── analytics_repository.py
    └── risk_repository.py

templates/
├── analytics/
│   └── index.html
│
└── risk/
    └── index.html

static/
├── css/
│   └── pages/
│       ├── analytics.css
│       └── risk.css
│
└── js/
    └── pages/
        ├── analytics.js
        └── risk.js
```

---

# 4. Architecture

```text
Frontend
   ↓
Analytics / Risk Routes
   ↓
Services
   ↓
Repository
   ↓
MySQL / Processed Dataset
```

Route tidak melakukan kalkulasi analytics secara langsung.

Contoh:

```text
Route
 ↓
analytics_service.get_gpa_trend()
 ↓
Repository
 ↓
Database
 ↓
JSON
 ↓
Frontend Chart
```

---

# 5. Analytics Data Source

Analytics menggunakan:

```text
academic_records
```

dan relationship:

```text
students
    │
    └── academic_records
```

Untuk beberapa analytics, informasi `major` membutuhkan JOIN.

Contoh:

```sql
SELECT
    s.major,
    AVG(a.gpa) AS average_gpa
FROM students s
JOIN academic_records a
    ON s.id = a.student_id
GROUP BY s.major;
```

---

# 6. Analytics Service

File:

```text
services/analytics_service.py
```

Fungsi:

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

---

# 7. Analytics Filter

Filter global:

```text
Major
Semester
GPA
Risk
Attendance
```

Contoh:

```text
Major = Informatics
Semester = 4
```

Maka seluruh chart yang relevan harus menggunakan subset data tersebut.

---

# 8. Filter Flow

```text
User Changes Filter
        ↓
Frontend
        ↓
API Request
        ↓
Analytics Service
        ↓
Database Query
        ↓
Filtered Data
        ↓
Chart Update
```

Jangan hanya memfilter tampilan chart tanpa memperbarui data.

---

# 9. GPA Distribution

Tujuan:

Mengetahui distribusi kategori performa akademik.

Kategori:

```text
Excellent
Good
Average
Poor
```

Threshold kategori **belum ditentukan dalam PRD**, sehingga threshold final harus ditetapkan sebagai configuration sebelum implementasi final.

Jangan hardcode threshold tanpa keputusan desain.

---

# 10. GPA Distribution Response

Contoh struktur:

```json
{
    "excellent": 20,
    "good": 35,
    "average": 30,
    "poor": 15
}
```

Angka hanya contoh struktur.

Data sebenarnya harus dihitung dari database.

---

# 11. GPA by Semester

Menampilkan:

```text
Semester 1 → Average GPA
Semester 2 → Average GPA
Semester 3 → Average GPA
...
```

Query:

```sql
SELECT
    semester,
    AVG(gpa) AS average_gpa
FROM academic_records
GROUP BY semester
ORDER BY semester;
```

Visualisasi:

```text
Line Chart
```

---

# 12. GPA by Major

Menampilkan rata-rata GPA berdasarkan jurusan.

```text
Informatics          3.42
Information System   3.35
Management           3.21
```

Visualisasi:

```text
Horizontal Bar Chart
```

Sorting:

```text
Highest → Lowest
```

---

# 13. GPA Trend

GPA Trend merupakan average GPA berdasarkan semester.

```text
Semester
   ↓
Average GPA
```

Contoh:

```text
S1 → 3.10
S2 → 3.24
S3 → 3.31
S4 → 3.42
```

Chart:

```text
Line Chart
```

---

# 14. GPA Trend vs GPA by Semester

Keduanya memiliki data yang mirip, tetapi konsepnya berbeda:

### GPA by Semester

Menampilkan agregasi GPA per semester.

### GPA Trend

Menekankan perubahan/pergerakan GPA dari waktu ke waktu.

Service dapat menggunakan query yang sama apabila hasilnya memang identik, tetapi presentation layer dapat memberikan konteks berbeda.

Jangan membuat kalkulasi berbeda hanya demi memisahkan nama fitur.

---

# 15. Attendance vs GPA

Visualisasi:

```text
Scatter Plot
```

X:

```text
Attendance
```

Y:

```text
GPA
```

Setiap titik dapat mewakili satu academic record/student-semester.

Tooltip:

```text
Student
Attendance
GPA
Semester
```

---

# 16. Study Hours vs GPA

X:

```text
Study Hours
```

Y:

```text
GPA
```

Visualisasi:

```text
Scatter Plot
```

Penting:

Jangan menghasilkan statement:

> “Study hours menyebabkan GPA meningkat.”

Yang diperbolehkan:

> “Study hours memiliki hubungan/korelasi dengan GPA.”

Hubungan statistik tidak otomatis berarti causation.

---

# 17. Assignment Score vs GPA

Scatter:

```text
X = Assignment Score
Y = GPA
```

Tooltip:

```text
Student
Assignment Score
GPA
Semester
```

---

# 18. Midterm Score vs GPA

Scatter:

```text
X = Midterm Score
Y = GPA
```

Data aktual berasal dari:

```text
midterm_score
gpa
```

---

# 19. Final Score vs GPA

Scatter:

```text
X = Final Score
Y = GPA
```

Data:

```text
final_score
gpa
```

---

# 20. Correlation Heatmap

Variabel:

```text
GPA
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours
```

Correlation matrix:

```text
            GPA Attendance Assignment ...
GPA
Attendance
Assignment
Midterm
Final
Study Hours
```

Perhitungan dapat menggunakan:

```python
df.corr(numeric_only=True)
```

---

# 21. Correlation Interpretation

Sistem boleh mencari korelasi terkuat.

Contoh:

```text
Final Score memiliki korelasi positif
terkuat dengan GPA.
```

Tetapi tidak boleh menyimpulkan:

```text
Final Score menyebabkan GPA meningkat.
```

---

# 22. Empty Analytics

Jika tidak ada data:

```text
No academic data available.

Upload or add academic records to see analytics.
```

Chart tidak boleh menampilkan data palsu.

---

# 23. Insufficient Data

Beberapa analisis membutuhkan data yang cukup.

Jika data tidak mencukupi:

```text
Not enough data to generate this analysis.
```

Jangan memaksakan insight.

---

# 24. Analytics API

Endpoint:

```text
GET /api/analytics/gpa-distribution
GET /api/analytics/gpa-semester
GET /api/analytics/gpa-major
GET /api/analytics/gpa-trend

GET /api/analytics/attendance-gpa
GET /api/analytics/study-hours-gpa
GET /api/analytics/assignment-gpa
GET /api/analytics/midterm-gpa
GET /api/analytics/final-gpa

GET /api/analytics/correlation
```

---

# 25. Query Parameters

Contoh:

```text
/api/analytics/gpa-trend?major=Informatics&semester=4
```

Filter dapat diterapkan secara dinamis.

---

# 26. Analytics Response

Format standar:

```json
{
    "success": true,
    "data": {
        "labels": [],
        "values": []
    }
}
```

Scatter dapat menggunakan:

```json
{
    "success": true,
    "data": {
        "points": []
    }
}
```

---

# 27. Chart Library

Frontend menggunakan Chart.js.

Chart yang dibutuhkan:

```text
Line
Bar
Doughnut
Scatter
Heatmap
```

Heatmap dapat menggunakan pendekatan/library yang sesuai dengan frontend architecture.

---

# 28. Analytics Page

Struktur:

```text
Analytics
│
├── Page Header
├── Filters
│
├── GPA Distribution
├── GPA by Semester
├── GPA by Major
├── GPA Trend
│
├── Attendance vs GPA
├── Study Hours vs GPA
│
├── Assignment vs GPA
├── Midterm vs GPA
├── Final vs GPA
│
└── Correlation Heatmap
```

---

# 29. Risk Engine

Risk Engine berbeda dari Machine Learning.

### Risk Engine

```text
Rule-based
```

Tujuan:

```text
Academic Data
     ↓
Risk Score
     ↓
Low / Medium / High
```

### ML

```text
Machine Learning
```

Tujuan:

```text
Academic Features
     ↓
Predicted GPA
```

Keduanya tidak boleh digabung menjadi satu engine.

---

# 30. Risk Factors

Risk Engine menggunakan:

```text
Current GPA
Previous GPA
GPA Trend
Attendance
Attendance Trend
Score Trend
Study Hours
Assignment Score
Midterm Score
Final Score
```

---

# 31. Current GPA

Current GPA:

```text
Academic record dengan semester terbaru
```

Contoh:

```text
S1 3.10
S2 3.20
S3 3.05
```

Current:

```text
3.05
```

---

# 32. Previous GPA

Previous:

```text
Semester sebelum current semester
```

Contoh:

```text
Current = S3
Previous = S2
```

Jika hanya ada satu semester:

```text
Previous = None
```

---

# 33. GPA Change

Formula:

```text
GPA Change = Current GPA - Previous GPA
```

Contoh:

```text
Current = 3.10
Previous = 3.40

Change = -0.30
```

Display:

```text
-0.30
```

---

# 34. Attendance Change

Formula:

```text
Current Attendance - Previous Attendance
```

Contoh:

```text
Current = 80
Previous = 90

Change = -10%
```

---

# 35. Score Trend

Bandingkan:

```text
Current scores
vs
Previous scores
```

Komponen:

```text
Assignment
Midterm
Final
```

Sistem dapat menghitung perubahan masing-masing.

---

# 36. Risk Score

Risk Engine menggunakan internal score:

```text
0–100
```

Ini adalah desain implementasi, bukan angka yang ditetapkan PRD.

Semakin tinggi:

```text
Risk semakin tinggi
```

---

# 37. Risk Components

Risk score dapat terdiri dari:

```text
GPA Risk
Attendance Risk
GPA Trend Risk
Score Trend Risk
Study Hours Risk
```

Contoh struktur internal:

```python
risk_components = {
    "gpa": 0,
    "attendance": 0,
    "gpa_trend": 0,
    "score_trend": 0,
    "study_hours": 0
}
```

---

# 38. Risk Weight

**Jangan menentukan bobot final secara hardcoded sekarang.**

PRD belum menentukan bobot.

Tahapan yang benar:

```text
Dataset Exploration
        ↓
Test Risk Logic
        ↓
Evaluate Results
        ↓
Determine Weight
        ↓
Configuration
```

---

# 39. Risk Threshold

Gunakan configuration:

```python
RISK_THRESHOLDS = {
    "low_max": 30,
    "medium_max": 60
}
```

Contoh tersebut adalah desain awal.

Maka:

```text
0–30   → Low
31–60  → Medium
61–100 → High
```

Namun threshold final harus divalidasi menggunakan dataset nyata.

---

# 40. Risk Level

Output:

```text
LOW
MEDIUM
HIGH
```

Database:

```sql
ENUM('low', 'medium', 'high')
```

---

# 41. Risk Factors Explanation

Selain risk level, sistem harus menjelaskan faktor utama.

Contoh:

```text
High Risk

Main factors:
- GPA decreased from previous semester.
- Attendance decreased significantly.
- Final score decreased.
```

Kalimat harus dihasilkan berdasarkan data aktual.

---

# 42. Risk Assessment Object

Struktur:

```json
{
    "student_id": 1,
    "semester": 4,
    "risk_level": "medium",
    "risk_score": 52,
    "main_factors": [
        "GPA decreased from previous semester",
        "Attendance is relatively low"
    ]
}
```

---

# 43. Risk Service

File:

```text
services/risk_service.py
```

Fungsi:

```python
get_current_record()
get_previous_record()

calculate_gpa_change()
calculate_score_trend()
calculate_attendance_change()

calculate_gpa_risk()
calculate_attendance_risk()
calculate_trend_risk()
calculate_study_hours_risk()

calculate_risk_score()
determine_risk_level()
generate_risk_factors()
generate_early_warnings()
```

---

# 44. Risk Calculation Flow

```text
Student
   ↓
Current Record
   ↓
Previous Record
   ↓
Calculate Changes
   ↓
Calculate Risk Components
   ↓
Calculate Risk Score
   ↓
Determine Risk Level
   ↓
Generate Explanation
   ↓
Save Assessment
```

---

# 45. Risk Assessment Storage

Table:

```text
risk_assessments
```

Data:

```text
student_id
semester
risk_level
risk_score
main_factors
assessed_at
```

---

# 46. Risk Recalculation

Risk harus dihitung ulang ketika academic record berubah.

```text
Academic Record Updated
        ↓
Risk Recalculation
        ↓
New Assessment
```

Admin/internal endpoint:

```text
POST /api/risk/recalculate
```

---

# 47. Risk History

Risk assessment sebaiknya disimpan berdasarkan semester.

Contoh:

```text
Semester 1 → Low
Semester 2 → Low
Semester 3 → Medium
Semester 4 → High
```

Hal ini memungkinkan sistem melihat perubahan risiko.

---

# 48. Risk API

```text
GET /api/risk
GET /api/students/<student_id>/risk
POST /api/risk/recalculate
```

---

# 49. Risk Filters

Risk page:

```text
Risk Level
Major
Semester
```

Tambahan:

```text
GPA
Attendance
```

dapat mengikuti filter yang tersedia pada analytics/student data.

---

# 50. Risk Dashboard

Summary:

```text
Low Risk
Medium Risk
High Risk
```

Contoh struktur:

```text
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Low        │ │ Medium     │ │ High       │
│ 120        │ │ 35         │ │ 12         │
└────────────┘ └────────────┘ └────────────┘
```

Angka berasal dari `risk_assessments`.

---

# 51. Risk Table

Kolom:

```text
Student
Major
GPA
Attendance
GPA Change
Risk
```

Contoh:

```text
Andi
Informatics
2.81
76%
-0.35
High
```

---

# 52. Early Warning

Early Warning bukan hanya risk level.

Sistem mencari perubahan signifikan:

```text
GPA decline
Attendance decline
Score decline
```

---

# 53. Early Warning Threshold

Threshold harus configurable.

Contoh struktur:

```python
EARLY_WARNING_CONFIG = {
    "gpa_decline": 0.20,
    "attendance_decline": 10,
    "score_decline": 10
}
```

Nilai tersebut merupakan contoh implementasi dan harus diuji dengan dataset nyata.

---

# 54. Early Warning Output

Contoh:

```json
{
    "type": "gpa_decline",
    "severity": "high",
    "message": "GPA decreased significantly from the previous semester.",
    "change": -0.35
}
```

---

# 55. Risk vs Early Warning

Perbedaannya:

### Risk

Menjawab:

> Seberapa besar risiko akademik mahasiswa saat ini?

### Early Warning

Menjawab:

> Apakah ada perubahan yang perlu diperhatikan?

Contoh:

```text
Risk = Medium

Early Warning:
GPA decreased significantly.
Attendance decreased.
```

Keduanya dapat muncul bersamaan.

---

# 56. Students Requiring Attention

Dashboard mengambil data dari Risk Engine.

Prioritas:

```text
High Risk
↓
Medium Risk
↓
Significant Early Warning
```

Data:

```text
Student
Major
GPA
Attendance
Change
Risk
```

---

# 57. Analytics dan Risk Integration

```text
                 Academic Records
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   Analytics Service           Risk Service
          │                         │
          ▼                         ▼
       Charts                 Risk Assessment
          │                         │
          └────────────┬────────────┘
                       ▼
                    Insights
```

Analytics tidak menentukan risk.

Risk Engine tidak membuat chart analytics.

---

# 58. API Error Handling

Jika data tidak cukup:

```json
{
    "success": false,
    "error": {
        "code": "INSUFFICIENT_DATA",
        "message": "Not enough academic data."
    }
}
```

Jika database error:

```json
{
    "success": false,
    "error": {
        "code": "DATABASE_ERROR",
        "message": "Unable to retrieve academic data."
    }
}
```

---

# 59. Frontend Animation

Analytics:

* chart fade-in
* filter transition
* skeleton loading
* subtle hover

Risk:

* badge transition
* table appearance
* summary count-up

Tidak menggunakan:

* particle
* glow
* bounce
* neon
* excessive gradient

---

# 60. Responsive Analytics

Desktop:

```text
2-column chart layout
```

Mobile:

```text
1-column chart layout
```

Contoh:

```text
Desktop

┌─────────────┬─────────────┐
│ GPA Trend   │ Distribution│
├─────────────┼─────────────┤
│ Attendance  │ GPA Major   │
└─────────────┴─────────────┘
```

Mobile:

```text
GPA Trend
Distribution
Attendance
GPA Major
```

---

# 61. Performance

Jangan mengambil seluruh database jika hanya membutuhkan agregasi.

Contoh:

```text
GPA by Major
```

lebih baik:

```sql
AVG(gpa)
GROUP BY major
```

daripada mengambil semua record lalu menghitung semuanya di browser.

---

# 62. Caching

Caching dapat dipertimbangkan untuk analytics yang mahal setelah sistem stabil.

Untuk MVP:

```text
Database
↓
Service
↓
API
```

sudah cukup.

Jangan menambahkan kompleksitas caching sebelum ada kebutuhan nyata.

---

# 63. Testing Analytics

Test:

* [ ] GPA distribution benar.
* [ ] GPA by semester benar.
* [ ] GPA by major benar.
* [ ] GPA trend benar.
* [ ] Attendance vs GPA benar.
* [ ] Study hours vs GPA benar.
* [ ] Assignment vs GPA benar.
* [ ] Midterm vs GPA benar.
* [ ] Final vs GPA benar.
* [ ] Correlation matrix benar.
* [ ] Filter bekerja.
* [ ] Empty dataset ditangani.
* [ ] Insufficient data ditangani.
* [ ] Tidak ada data hardcoded.

---

# 64. Testing Risk

Test:

* [ ] Current record benar.
* [ ] Previous record benar.
* [ ] GPA change benar.
* [ ] Attendance change benar.
* [ ] Score trend benar.
* [ ] Risk components benar.
* [ ] Risk score berada pada range yang ditentukan.
* [ ] Risk level sesuai threshold configuration.
* [ ] Risk factors sesuai data.
* [ ] Early warning sesuai threshold.
* [ ] Assessment tersimpan.
* [ ] Recalculation bekerja.
* [ ] Tidak ada hasil risk hardcoded.

---

# 65. Definition of Done

Tahap Analytics & Risk selesai apabila:

* [ ] Semua 10 analytics tersedia.
* [ ] Filter analytics tersedia.
* [ ] API analytics tersedia.
* [ ] Chart menggunakan data aktual.
* [ ] Correlation dihitung dari data aktual.
* [ ] Tidak ada klaim causation.
* [ ] Risk Engine tersedia.
* [ ] Current/previous GPA tersedia.
* [ ] GPA change tersedia.
* [ ] Attendance change tersedia.
* [ ] Score trend tersedia.
* [ ] Risk score tersedia.
* [ ] Risk level tersedia.
* [ ] Risk factors tersedia.
* [ ] Early warning tersedia.
* [ ] Risk assessment disimpan.
* [ ] Recalculation tersedia.
* [ ] Dashboard dapat menggunakan risk data.
* [ ] Empty/loading/error state tersedia.
* [ ] Responsive.
* [ ] Dark mode.
* [ ] SVG icons.
* [ ] Threshold configurable.
* [ ] Tidak ada student result yang di-hardcode.

---

# 66. Posisi Project Sekarang

Setelah tahap ini, core data intelligence sudah mulai terbentuk:

```text
                  DATA
                   │
                   ▼
             VALIDATION
                   │
                   ▼
              CLEANING
                   │
                   ▼
            PROCESSED DATA
                   │
          ┌────────┴────────┐
          ▼                 ▼
      ANALYTICS          RISK ENGINE
          │                 │
          │                 ├── Risk Score
          │                 ├── Risk Level
          │                 └── Early Warning
          │
          ├── GPA
          ├── Attendance
          ├── Scores
          ├── Study Hours
          └── Correlation
                   │
                   ▼
                INSIGHT
                   │
                   ▼
              DASHBOARD
```
