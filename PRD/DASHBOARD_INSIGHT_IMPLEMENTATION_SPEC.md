# DASHBOARD_INSIGHT_IMPLEMENTATION_SPEC.md

## 1. Tujuan

Tahap ini mengimplementasikan **Dashboard** sebagai pusat informasi utama aplikasi dan menghubungkan seluruh engine yang sudah dibuat:

```text
Students
Academic Records
Dataset
     │
     ▼
Analytics ───────┐
                 │
Risk Engine ─────┤
                 │
ML Prediction ───┤
                 ▼
             Dashboard
                 │
                 ▼
              Insights
```

Dashboard harus menjawab tiga pertanyaan utama:

1. **Bagaimana performa akademik saat ini?**
2. **Apa yang sedang berubah?**
3. **Mahasiswa mana yang membutuhkan perhatian?**

Dashboard bukan sekadar kumpulan chart, tetapi menjadi **data-first overview** dari seluruh sistem.

---

# 2. Scope

Tahap ini mencakup:

### Dashboard

* Page Header
* KPI Cards
* GPA Trend
* Performance Distribution
* Attendance vs GPA
* GPA by Major
* Academic Insights
* Students Requiring Attention
* filters bila diperlukan
* loading state
* empty state
* error state
* responsive
* dark mode

### Insight Engine

* GPA Trend Insight
* Performance Distribution Insight
* Attendance Insight
* Score Performance Insight
* Study Hours Insight
* Correlation Insight
* Risk Insight
* Students Requiring Attention

---

# 3. Struktur File

Tambahkan:

```text
services/
├── dashboard_service.py
├── insight_service.py
└── ...

routes/
├── dashboard.py
└── ...

templates/
└── dashboard/
    └── index.html

static/
├── css/
│   └── pages/
│       └── dashboard.css
│
└── js/
    └── pages/
        └── dashboard.js
```

---

# 4. Dashboard Architecture

```text
Dashboard Route
       ↓
Dashboard Service
       │
       ├── Student Data
       ├── Academic Data
       ├── Analytics
       ├── Risk
       └── Insights
       ↓
Dashboard API
       ↓
Frontend
       ↓
KPI + Charts + Insights + Attention
```

Dashboard Service tidak menghitung ulang business logic yang sudah dimiliki service lain.

Contoh:

```text
Risk data
   ↓
Risk Service
   ↓
Dashboard Service
```

bukan:

```text
Dashboard Service
   ↓
menghitung ulang Risk Score
```

---

# 5. Dashboard Page Structure

Sesuai struktur Dashboard:

```text
Dashboard
│
├── Page Header
│
├── KPI
│   ├── Total Students
│   ├── Average GPA
│   ├── Average Attendance
│   └── At Risk
│
├── Main Analytics
│   ├── GPA Trend
│   └── Performance Distribution
│
├── Secondary Analytics
│   ├── Attendance vs GPA
│   └── GPA by Major
│
├── Academic Insights
│
└── Students Requiring Attention
```

---

# 6. Dashboard Header

Header:

```text
Dashboard

Overview of your academic data
```

Tambahkan:

```text
Last updated
```

Contoh:

```text
Last updated
7 October 2026, 13:20
```

Tanggal harus dihasilkan secara dinamis.

---

# 7. Last Updated

Sumber:

```text
latest relevant data update
```

Jangan menggunakan tanggal hardcoded.

Jika tidak tersedia:

```text
Last updated — 
```

atau:

```text
Last updated information unavailable
```

---

# 8. KPI Cards

Empat KPI utama:

```text
Total Students
Average GPA
Average Attendance
At Risk
```

Layout desktop:

```text
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ Students   │ │ Avg GPA    │ │ Attendance │ │ At Risk    │
│ 1,250      │ │ 3.42       │ │ 89.4%      │ │ 47         │
└────────────┘ └────────────┘ └────────────┘ └────────────┘
```

---

# 9. KPI — Total Students

Query:

```sql
SELECT COUNT(*) AS total_students
FROM students;
```

Output:

```json
{
    "value": 1250
}
```

Angka harus berasal dari database.

---

# 10. KPI — Average GPA

Average GPA berasal dari academic records.

```sql
SELECT AVG(gpa)
FROM academic_records;
```

Format:

```text
3.42
```

Tampilkan dengan precision yang konsisten, misalnya:

```text
2 decimal places
```

---

# 11. KPI — Average Attendance

Query:

```sql
SELECT AVG(attendance)
FROM academic_records;
```

Format:

```text
89.4%
```

Jangan menampilkan:

```text
89.423847293%
```

---

# 12. KPI — At Risk

At Risk menggunakan Risk Engine.

Kategori:

```text
medium
high
```

Query konsep:

```sql
SELECT COUNT(DISTINCT student_id)
FROM risk_assessments
WHERE risk_level IN ('medium', 'high');
```

Gunakan assessment yang relevan/current sesuai implementasi Risk Engine.

---

# 13. KPI Change

Dashboard specification menyebut perubahan dibandingkan periode sebelumnya.

Contoh:

```text
Total Students
1,250
+8.2% from previous semester
```

Untuk GPA:

```text
Average GPA
3.42
+0.12 from previous semester
```

Perubahan harus dihitung dari data aktual.

---

# 14. Change Calculation

Contoh GPA:

```text
Current Average GPA
        -
Previous Average GPA
```

Misalnya:

```text
Current = 3.42
Previous = 3.30

Change = +0.12
```

Jangan menggunakan angka perubahan hardcoded.

---

# 15. Change Percentage

Untuk metric yang sesuai:

```text
percentage_change =
(current - previous) / previous × 100
```

Namun untuk GPA, display perubahan absolut dapat lebih mudah dipahami:

```text
+0.12 GPA
```

Daripada:

```text
+3.63%
```

Format final harus konsisten dengan konteks metric.

---

# 16. GPA Trend

Chart:

```text
Line Chart
```

Data:

```text
Semester
Average GPA
```

Contoh:

```text
S1 → 3.10
S2 → 3.24
S3 → 3.31
S4 → 3.42
```

Tooltip:

```text
Semester 4
Average GPA: 3.42
```

---

# 17. GPA Trend Source

Dashboard tidak membuat query trend sendiri jika Analytics Service sudah menyediakan fungsi:

```python
get_gpa_trend()
```

Gunakan:

```text
Dashboard
 ↓
Analytics Service
 ↓
GPA Trend
```

Hal ini menghindari duplicate business logic.

---

# 18. Performance Distribution

Chart:

```text
Donut Chart
```

Kategori:

```text
Excellent
Good
Average
Poor
```

Data harus dihitung dari academic data aktual.

Threshold kategori harus mengambil configuration yang sama dengan Analytics/Insight.

---

# 19. Consistency Rule

Jangan sampai:

```text
Dashboard:
Excellent = GPA >= 3.5
```

sementara:

```text
Analytics:
Excellent = GPA >= 3.6
```

Gunakan satu konfigurasi kategori.

Contoh:

```python
PERFORMANCE_CATEGORIES
```

sebagai single source of truth.

---

# 20. Attendance vs GPA

Chart:

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

Tooltip:

```text
Student
Attendance
GPA
```

Tujuan:

memberikan gambaran hubungan antara attendance dan GPA.

Tidak boleh menyatakan causal relationship.

---

# 21. GPA by Major

Chart:

```text
Horizontal Bar Chart
```

Contoh:

```text
Informatics          ███████████ 3.42
Information System   ██████████  3.35
Management           █████████   3.21
```

Sorting:

```text
Highest GPA
↓
Lowest GPA
```

---

# 22. Academic Insights

Insight Engine mengubah hasil analytics menjadi informasi yang mudah dipahami.

Contoh:

```text
GPA Trend

Average GPA increased compared with
the previous semester.
```

Pesan harus dihasilkan dari data aktual.

---

# 23. Insight Categories

Insight Engine memiliki:

```text
GPA Trend
Performance Distribution
Attendance
Score Performance
Study Hours
Correlation
Risk
```

---

# 24. Insight Object

Format:

```json
{
    "type": "gpa_trend",
    "priority": "medium",
    "title": "GPA Trend",
    "message": "...",
    "value": 3.42,
    "change": 0.12
}
```

---

# 25. GPA Trend Insight

Input:

```text
Current average GPA
Previous average GPA
```

Logic:

```text
Current > Previous
    ↓
Improvement

Current < Previous
    ↓
Decline

Difference within configured threshold
    ↓
Stable
```

Threshold harus configurable.

---

# 26. Distribution Insight

Sistem mencari kategori dengan jumlah terbesar.

Contoh:

```text
Good = 540
Average = 430
Excellent = 200
Poor = 80
```

Insight:

```text
Good performance is the dominant
academic category.
```

Angka harus berasal dari data aktual.

---

# 27. Attendance Insight

Bandingkan attendance:

```text
Current
vs
Previous
```

Contoh:

```text
Average attendance decreased
from 91% to 87%.
```

Jika tidak ada previous period:

```text
Average attendance is 87%.
```

Jangan membuat klaim perubahan jika data pembanding tidak tersedia.

---

# 28. Score Performance Insight

Bandingkan:

```text
Assignment
Midterm
Final
```

Contoh:

```text
Final scores have the highest
average among the three assessments.
```

Tujuannya menunjukkan area performa yang relatif kuat/lemah.

---

# 29. Study Hours Insight

Dapat menampilkan:

```text
Average study hours
```

Contoh:

```text
Students study an average of
12.4 hours per period.
```

Jangan mengatakan:

```text
Studying 12.4 hours causes
higher GPA.
```

---

# 30. Correlation Insight

Gunakan correlation matrix.

Contoh:

```text
Final Score has the strongest
positive correlation with GPA.
```

Gunakan kata:

```text
correlation
relationship
association
```

Hindari:

```text
causes
guarantees
results in
```

---

# 31. Risk Insight

Menggunakan Risk Engine.

Contoh:

```text
47 students currently require
academic attention based on medium
or high risk assessments.
```

Jumlah harus berasal dari:

```text
Risk Service
```

bukan dihitung ulang oleh Insight Service.

---

# 32. Insight Priority

Priority:

```text
high
medium
low
```

Contoh:

```text
High Risk
↓
high priority
```

GPA stable:

```text
low priority
```

Priority rules harus configurable jika diperlukan.

---

# 33. Insight Service

File:

```text
services/insight_service.py
```

Fungsi:

```python
generate_gpa_insight()
generate_distribution_insight()
generate_attendance_insight()
generate_score_insight()
generate_study_hours_insight()
generate_correlation_insight()
generate_risk_insight()
generate_all_insights()
```

---

# 34. Insight Configuration

Gunakan:

```python
INSIGHT_CONFIG = {
    "gpa_stable_threshold": ...,
    "attendance_change_threshold": ...,
    "score_change_threshold": ...
}
```

Nilai final harus ditentukan berdasarkan dataset/testing.

Jangan menyebarkan angka threshold di berbagai function.

---

# 35. Dashboard Insight Selection

Dashboard tidak perlu menampilkan semua insight.

Gunakan:

```text
generate_all_insights()
        ↓
Priority Sorting
        ↓
Top 4
        ↓
Dashboard
```

Contoh:

```text
1. GPA Trend
2. Risk
3. Attendance
4. Distribution
```

---

# 36. Students Requiring Attention

Sumber:

```text
Risk Engine
```

bukan Insight Engine.

Insight hanya menjelaskan kondisi.

Risk Engine menentukan siapa yang membutuhkan perhatian.

---

# 37. Attention Table

Kolom:

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
Andi Pratama
Informatics
2.81
76%
-0.35
High
```

---

# 38. Attention Priority

Urutan:

```text
High Risk
↓
Medium Risk
↓
Significant Warning
```

Jika beberapa student memiliki risk sama, dapat diurutkan berdasarkan:

```text
Risk Score DESC
```

---

# 39. View All

Di bawah table:

```text
View all students
```

Action:

```text
/students?risk=high
```

atau route/filter equivalent.

Jangan membuat halaman attention terpisah jika Student page sudah dapat menangani filter risk.

---

# 40. Dashboard API

Endpoint:

```text
GET /api/dashboard
```

API menggabungkan data:

```text
KPI
GPA Trend
Distribution
Attendance vs GPA
GPA by Major
Insights
Students Requiring Attention
```

---

# 41. Dashboard Response

Struktur:

```json
{
    "success": true,
    "data": {
        "summary": {
            "total_students": 1250,
            "average_gpa": 3.42,
            "average_attendance": 89.4,
            "at_risk": 47
        },
        "gpa_trend": [],
        "performance_distribution": {},
        "attendance_vs_gpa": [],
        "gpa_by_major": [],
        "insights": [],
        "students_attention": []
    }
}
```

Angka hanya contoh struktur.

---

# 42. Dashboard Service

File:

```text
services/dashboard_service.py
```

Fungsi:

```python
get_dashboard_summary()
get_dashboard_analytics()
get_dashboard_insights()
get_students_requiring_attention()
get_dashboard_data()
```

`get_dashboard_data()` menjadi orchestrator.

---

# 43. Dashboard Service Flow

```text
get_dashboard_data()
        │
        ├── get_dashboard_summary()
        │
        ├── analytics_service
        │
        ├── risk_service
        │
        └── insight_service
```

Tidak melakukan duplicate calculation.

---

# 44. Dashboard Loading

Saat halaman dibuka:

```text
Dashboard
    ↓
Skeleton
    ↓
API request
    ↓
Data loaded
    ↓
Render
```

KPI skeleton:

```text
┌──────────────┐
│ ▬▬▬▬▬        │
│ ▬▬▬▬▬▬▬      │
└──────────────┘
```

---

# 45. Dashboard Empty State

Jika belum ada academic data:

```text
No academic data available.

Add academic records or upload a dataset
to start analyzing student performance.
```

Chart tidak menampilkan data dummy.

---

# 46. Dashboard Partial Empty State

Jika satu chart tidak memiliki data:

```text
Not enough data for this analysis.
```

Chart lain tetap boleh ditampilkan.

Jangan membuat seluruh dashboard gagal hanya karena satu analytics kosong.

---

# 47. Dashboard Error Handling

Jika API dashboard gagal total:

```text
Unable to load dashboard data.

Please try again.
```

Button:

```text
Retry
```

Jika hanya salah satu section gagal, section tersebut menampilkan error state tanpa merusak seluruh halaman.

---

# 48. Responsive Layout

Desktop:

```text
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ KPI         │ KPI         │ KPI         │ KPI         │
└─────────────┴─────────────┴─────────────┴─────────────┘

┌──────────────────────────┬───────────────────────────┐
│ GPA Trend                │ Performance Distribution  │
└──────────────────────────┴───────────────────────────┘

┌──────────────────────────┬───────────────────────────┐
│ Attendance vs GPA        │ GPA by Major              │
└──────────────────────────┴───────────────────────────┘
```

Mobile:

```text
KPI
KPI

KPI
KPI

GPA Trend

Distribution

Attendance vs GPA

GPA by Major

Insights

Attention
```

---

# 49. KPI Mobile

KPI:

```text
2 columns
```

Contoh:

```text
┌────────────┐ ┌────────────┐
│ Students   │ │ GPA        │
└────────────┘ └────────────┘
┌────────────┐ ┌────────────┐
│ Attendance │ │ At Risk    │
└────────────┘ └────────────┘
```

---

# 50. Sidebar Integration

Dashboard berada pada:

```text
Overview
├── Dashboard
├── Students
└── Analytics
```

Active state:

```text
Dashboard
```

menggunakan style active yang sudah didefinisikan dalam design system.

---

# 51. Topbar Integration

Topbar:

```text
Sidebar Toggle
Global Search
Theme Toggle
Notification
Profile
```

Global search placeholder:

```text
Search students, major, reports...
```

---

# 52. Notification

Notification dapat digunakan untuk:

* important risk alerts
* dataset processing
* model training

Namun jangan membuat notifikasi dummy.

Jika belum ada notification engine:

```text
Notification icon
```

dapat tetap menjadi UI placeholder tanpa menghasilkan data palsu.

---

# 53. Global Search

Search dashboard dapat mengarah ke:

```text
Students
Reports
```

Contoh:

```text
Search "Andi"
      ↓
Student result
```

Global search bukan bagian utama dashboard analytics.

---

# 54. Theme

Dashboard mengikuti:

```text
data-theme="light"
```

atau:

```text
data-theme="dark"
```

Jangan membuat CSS dashboard sendiri yang bertentangan dengan `base.css`.

---

# 55. Chart Theme

Chart.js harus membaca theme aktif.

Light:

```text
Text
Border
Grid
Tooltip
```

Dark:

```text
Text
Border
Grid
Tooltip
```

Chart tidak boleh tetap memiliki label gelap yang sulit dibaca ketika dark mode aktif.

---

# 56. SVG Icons

Semua icon:

```text
SVG
```

Contoh penggunaan:

```text
KPI
Trend
Risk
Students
Insights
```

Tidak menggunakan Unicode emoji.

---

# 57. Animation

Dashboard menggunakan animasi ringan:

### Page

```text
opacity
translateY
```

### KPI

```text
count-up
```

### Charts

```text
fade-in
```

### Table

```text
subtle appearance
```

Durasi sekitar:

```text
150ms
200ms
300ms
```

Tidak menggunakan:

```text
bounce
glow
particle
excessive scale
```

---

# 58. KPI Count-Up

Jika:

```text
Total Students = 1250
```

angka dapat dianimasikan:

```text
0
↓
250
↓
600
↓
900
↓
1250
```

Animasi harus tetap sederhana.

Untuk reduced-motion user, animasi harus dapat dikurangi/dimatikan.

---

# 59. Accessibility

Dashboard wajib:

* semantic headings
* accessible labels
* keyboard navigation
* visible focus
* chart descriptions jika diperlukan
* sufficient contrast
* button labels
* tidak bergantung pada warna saja untuk status risk

Contoh:

```text
High
```

tidak hanya dibedakan dengan warna merah.

---

# 60. Dashboard Performance

Dashboard API sebaiknya mengambil data dalam satu request:

```text
GET /api/dashboard
```

daripada frontend melakukan:

```text
GET /api/summary
GET /api/trend
GET /api/distribution
GET /api/risk
GET /api/insights
...
```

secara terpisah pada initial load.

Tujuannya mengurangi request awal.

---

# 61. Service Reuse

Dashboard menggunakan service yang sudah tersedia:

```text
Analytics Service
Risk Service
Insight Service
Student Service
Academic Service
```

Tidak membuat versi kedua dari:

```text
calculate_risk_score()
```

atau:

```text
get_gpa_trend()
```

di `dashboard_service.py`.

---

# 62. Data Consistency

Semua bagian dashboard harus berasal dari dataset/data period yang konsisten.

Contoh jangan sampai:

```text
Average GPA
→ Semester 4

GPA Trend
→ Semua semester

At Risk
→ Semester 3
```

tanpa konteks.

Dashboard harus menjelaskan scope data jika ada perbedaan periode.

---

# 63. Current Period

Dashboard dapat menggunakan academic records terbaru yang tersedia.

Untuk trend:

```text
Semua semester
```

Untuk current KPI:

```text
Current/latest relevant period
```

Implementasi harus konsisten dengan definisi metric.

---

# 64. Dashboard Insights Rule

Insight hanya boleh muncul jika datanya mendukung.

Contoh:

Tidak ada previous semester:

```text
Jangan:
"GPA increased by 0.12"
```

Gunakan:

```text
"Current average GPA is 3.42."
```

---

# 65. No Hardcoded Insights

Tidak boleh:

```python
message = "GPA meningkat tahun ini."
```

secara statis.

Harus:

```text
Actual Data
 ↓
Calculation
 ↓
Condition
 ↓
Generated Message
```

---

# 66. Insight Prioritization

Contoh:

```text
Risk High
GPA decline
Attendance decline
```

Maka insight risk dapat diprioritaskan lebih tinggi.

Tetapi aturan final harus konsisten dengan `INSIGHT_CONFIG`.

---

# 67. Dashboard Repository

Jika diperlukan:

```text
database/repositories/dashboard_repository.py
```

Namun dashboard sebaiknya menggunakan repository/service yang sudah ada jika query yang diperlukan sudah tersedia.

Jangan membuat repository duplicate tanpa kebutuhan.

---

# 68. Testing Dashboard

### KPI

* [ ] Total students benar.
* [ ] Average GPA benar.
* [ ] Average attendance benar.
* [ ] At-risk count benar.

### Analytics

* [ ] GPA trend benar.
* [ ] Distribution benar.
* [ ] Attendance vs GPA benar.
* [ ] GPA by major benar.

### Insights

* [ ] Insight berdasarkan data aktual.
* [ ] Tidak ada unsupported claims.
* [ ] Priority bekerja.
* [ ] Empty data ditangani.

### Attention

* [ ] High risk muncul.
* [ ] Medium risk muncul.
* [ ] Sorting benar.
* [ ] View all bekerja.

---

# 69. Integration Testing

Test full flow:

```text
Create Student
      ↓
Create Academic Record
      ↓
Risk Calculation
      ↓
Analytics Calculation
      ↓
Insight Generation
      ↓
Dashboard
```

Kemudian:

```text
Update Academic Record
      ↓
Recalculate Risk
      ↓
Refresh Dashboard
      ↓
New Result
```

---

# 70. Definition of Done

Tahap Dashboard & Insight selesai apabila:

* [ ] Dashboard page tersedia.
* [ ] Page header tersedia.
* [ ] Last updated dinamis.
* [ ] Total Students tersedia.
* [ ] Average GPA tersedia.
* [ ] Average Attendance tersedia.
* [ ] At Risk tersedia.
* [ ] KPI change tersedia jika data pembanding tersedia.
* [ ] GPA Trend tersedia.
* [ ] Performance Distribution tersedia.
* [ ] Attendance vs GPA tersedia.
* [ ] GPA by Major tersedia.
* [ ] Academic Insights tersedia.
* [ ] Students Requiring Attention tersedia.
* [ ] Semua data berasal dari service/database.
* [ ] Tidak ada data dummy/hardcoded.
* [ ] Analytics service digunakan kembali.
* [ ] Risk service digunakan kembali.
* [ ] Insight service digunakan kembali.
* [ ] Loading state tersedia.
* [ ] Empty state tersedia.
* [ ] Error state tersedia.
* [ ] Partial error ditangani.
* [ ] Responsive.
* [ ] Dark mode.
* [ ] SVG icons.
* [ ] Accessibility dasar tersedia.
* [ ] Animasi subtle.
* [ ] Tidak ada neon/glow/particle.

---

# 71. Posisi Project Sekarang

Setelah tahap ini, hampir seluruh **core intelligence** sudah terhubung:

```text
                         ┌──────────────┐
                         │   Students   │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │   Academic   │
                         │    Records   │
                         └──────┬───────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
            Analytics          Risk            ML
                 │              │              │
                 ▼              ▼              ▼
              Charts       Risk Level      Prediction
                 │              │              │
                 └──────────────┼──────────────┘
                                ▼
                           Insight Engine
                                │
                                ▼
                            Dashboard
```

---
