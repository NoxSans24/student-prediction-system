# ANALYTICS_SPECIFICATION.md

Bagian ini menentukan bagaimana **Analytics** mengolah data akademik menjadi informasi yang bisa digunakan Dashboard, Insight, dan Risk Analysis.

Analytics bukan sekadar kumpulan chart. Fokusnya adalah menjawab:

> **Bagaimana performa akademik mahasiswa, faktor apa yang berkaitan dengan performa tersebut, dan bagaimana perubahannya dari waktu ke waktu?**

---

# 1. Tujuan Analytics

Analytics bertugas menyediakan analisis:

```text
Academic Data
     ↓
Aggregation
     ↓
Statistical Analysis
     ↓
Visualization
     ↓
Academic Insight
```

Analytics digunakan oleh:

* Dashboard
* Analytics Page
* Automated Insights
* Student Profile
* Risk Analysis

---

# 2. Analisis yang Wajib Tersedia

Berdasarkan scope project, Analytics mencakup:

1. GPA Distribution
2. GPA by Semester
3. GPA by Major
4. GPA Trend
5. Attendance vs GPA
6. Study Hours vs GPA
7. Assignment Score vs GPA
8. Midterm Score vs GPA
9. Final Score vs GPA
10. Correlation Heatmap

---

# 3. GPA Distribution

Tujuan:

> Melihat bagaimana GPA mahasiswa tersebar.

Contoh kategori:

```text
Excellent
Good
Average
Poor
```

Hasil analisis dapat ditampilkan dalam:

* Donut chart
* Bar chart

Contoh struktur data:

```text
Category      Students
----------------------
Excellent        25
Good             42
Average          28
Poor              5
```

Nilai tersebut harus dihitung dari database/dataset aktual.

Tidak boleh menggunakan angka hardcoded.

---

# 4. GPA by Semester

Menampilkan rata-rata GPA untuk setiap semester.

Contoh:

```text
Semester     Average GPA
------------------------
1               3.12
2               3.18
3               3.24
4               3.31
```

Query konsep:

```sql
SELECT
    semester,
    AVG(gpa) AS average_gpa
FROM academic_records
GROUP BY semester
ORDER BY semester;
```

Visualisasi yang sesuai:

> Line chart

---

# 5. GPA by Major

Menampilkan rata-rata GPA berdasarkan jurusan.

Contoh:

```text
Major                  Average GPA
-----------------------------------
Informatics                3.31
Information Systems        3.24
Computer Engineering       3.18
```

Visualisasi:

> Horizontal bar chart

Query konsep:

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

---

# 6. GPA Trend

GPA Trend digunakan untuk melihat perubahan performa akademik dari semester ke semester.

Contoh:

```text
Semester
1 ─── 3.10
2 ─── 3.18
3 ─── 3.24
4 ─── 3.31
```

Visualisasi:

> Line chart

Data harus berasal dari:

```text
academic_records
```

Bukan dari hasil prediksi ML.

---

# 7. Attendance vs GPA

Analisis ini digunakan untuk melihat hubungan antara kehadiran dan GPA.

Data:

```text
attendance
gpa
student
```

Visualisasi:

> Scatter plot

Setiap titik mewakili mahasiswa/record akademik.

Contoh informasi ketika hover:

```text
Student: Muhammad
Attendance: 91%
GPA: 3.54
```

---

# 8. Study Hours vs GPA

Digunakan untuk melihat hubungan antara jam belajar dan GPA.

Input:

```text
study_hours
gpa
```

Visualisasi:

> Scatter plot

Tujuannya bukan menyatakan bahwa study hours **menyebabkan** GPA meningkat.

Sistem hanya menunjukkan pola atau hubungan yang terlihat pada dataset.

---

# 9. Assignment Score vs GPA

Analisis:

```text
assignment_score
        ↓
       GPA
```

Visualisasi:

> Scatter plot

Digunakan untuk melihat pola hubungan antara nilai tugas dan GPA.

---

# 10. Midterm Score vs GPA

Analisis:

```text
midterm_score
      ↓
     GPA
```

Visualisasi:

> Scatter plot

Data diambil dari `academic_records`.

---

# 11. Final Score vs GPA

Analisis:

```text
final_score
     ↓
    GPA
```

Visualisasi:

> Scatter plot

Digunakan untuk melihat hubungan nilai final dengan GPA.

---

# 12. Correlation Heatmap

Correlation heatmap digunakan untuk melihat hubungan antar variabel numerik.

Variabel:

```text
GPA
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours
```

Contoh struktur:

```text
                GPA Attendance Assignment Midterm Final Study
GPA             1.0    0.42      0.61      0.70   0.76  0.31
Attendance      0.42   1.0       0.28      0.32   0.35  0.18
Assignment      0.61   0.28      1.0       0.55   0.58  0.22
Midterm         0.70   0.32      0.55      1.0    0.72  0.25
Final           0.76   0.35      0.58      0.72   1.0   0.27
Study Hours     0.31   0.18      0.22      0.25   0.27  1.0
```

Angka di atas hanya contoh.

Correlation harus dihitung dari dataset aktual.

---

# 13. Correlation Interpretation

Analytics boleh memberikan interpretasi seperti:

> “Final score memiliki hubungan positif dengan GPA pada dataset.”

Namun sistem **tidak boleh langsung menyatakan hubungan sebab-akibat**.

Contoh yang harus dihindari:

> “Nilai final menyebabkan GPA meningkat.”

Lebih tepat:

> “Terdapat korelasi positif antara final score dan GPA.”

---

# 14. Filters

Analytics harus mendukung filtering berdasarkan:

```text
Major
Semester
GPA
Risk Level
Attendance
```

Contoh:

```text
Major:
[All]

Semester:
[All]

GPA:
[All]

Risk:
[All]
```

Ketika filter berubah:

```text
Filter
  ↓
Query / Dataset
  ↓
Recalculate
  ↓
Update Charts
  ↓
Update Insights
```

Chart tidak boleh tetap menampilkan data sebelum filter.

---

# 15. Analytics Service

Disarankan membuat:

```text
services/
└── analytics_service.py
```

Fungsi yang dapat disediakan:

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

Filter dapat diberikan sebagai parameter.

Contoh konsep:

```python
get_gpa_by_major(
    major=None,
    semester=None
)
```

---

# 16. Data Aggregation

Analytics membutuhkan dua jenis data.

### Aggregate Data

Digunakan untuk:

* GPA trend
* GPA by major
* GPA distribution

Contoh:

```text
semester → average GPA
major → average GPA
category → student count
```

### Record-Level Data

Digunakan untuk:

* Scatter plot
* Correlation
* Student-level analysis

Contoh:

```text
student_id
attendance
gpa
study_hours
assignment_score
midterm_score
final_score
```

---

# 17. Analytics API

Jika frontend menggunakan JavaScript, backend dapat menyediakan endpoint JSON.

Contoh:

```text
/api/analytics/gpa-distribution
/api/analytics/gpa-semester
/api/analytics/gpa-major
/api/analytics/gpa-trend
/api/analytics/attendance-gpa
/api/analytics/study-hours-gpa
/api/analytics/correlation
```

Response contoh:

```json
{
    "data": [
        {
            "semester": 1,
            "average_gpa": 3.12
        },
        {
            "semester": 2,
            "average_gpa": 3.18
        }
    ]
}
```

Frontend kemudian menggunakan data tersebut untuk membuat chart.

---

# 18. Chart Rendering

Frontend menggunakan JavaScript untuk merender visualisasi.

Arsitektur:

```text
Flask
  ↓
Analytics Service
  ↓
JSON
  ↓
JavaScript
  ↓
Chart
```

Dengan pendekatan ini, HTML tidak perlu berisi data analytics secara hardcoded.

---

# 19. Empty State

Jika belum ada data:

```text
No academic data available
```

Contoh:

```text
┌────────────────────────────────────┐
│ GPA Trend                          │
│                                    │
│       No data available            │
│                                    │
│ Upload or add academic data first. │
└────────────────────────────────────┘
```

Jangan menampilkan chart kosong tanpa penjelasan.

---

# 20. Error State

Jika analytics gagal dimuat:

```text
Unable to load analytics
Please try again.
```

User tidak boleh melihat error Python/SQL mentah.

---

# 21. Loading State

Saat data sedang diproses:

```text
Loading analytics...
```

Untuk chart dapat digunakan skeleton sederhana.

Animasi tetap minimal dan tidak menggunakan efek berlebihan.

---

# 22. Automated Insights

Analytics menjadi sumber data untuk:

```text
Insight Service
```

Contoh:

```text
Analytics
    ↓
Statistical Results
    ↓
Insight Engine
    ↓
Human-readable Insight
```

Contoh insight:

> “Average GPA increased compared with the previous semester.”

Atau:

> “Attendance and GPA show a positive correlation in the current dataset.”

Insight harus dibuat berdasarkan hasil aktual.

Tidak boleh:

```python
return "GPA mahasiswa meningkat."
```

tanpa melakukan pengecekan terhadap data.

---

# 23. Insight Rules

Insight dapat berasal dari:

### GPA

```text
current average GPA
previous average GPA
difference
```

### Attendance

```text
current average attendance
previous average attendance
difference
```

### Distribution

```text
percentage Excellent
percentage Good
percentage Average
percentage Poor
```

### Risk

```text
Low
Medium
High
```

### Correlation

```text
attendance ↔ GPA
study_hours ↔ GPA
assignment ↔ GPA
midterm ↔ GPA
final ↔ GPA
```

---

# 24. Analytics dan Dashboard

Dashboard tidak perlu membuat logic analytics sendiri.

Gunakan:

```text
Analytics Service
       ↓
Dashboard
```

Contoh:

```text
Dashboard
├── GPA Trend
├── Performance Distribution
├── Attendance vs GPA
└── GPA by Major
```

Semua data tersebut berasal dari Analytics Service.

Ini menghindari duplikasi logic.

---

# 25. Analytics dan Student Profile

Student Profile dapat menggunakan analytics untuk menampilkan:

```text
Student GPA History
Attendance History
Score History
Performance Trend
```

Contoh:

```text
Semester 1 → GPA 3.10
Semester 2 → GPA 3.25
Semester 3 → GPA 3.40
```

---

# 26. Analytics dan Risk Engine

Risk Engine dapat menggunakan hasil analytics tertentu sebagai pendukung.

Namun:

> **Risk Engine tetap memiliki logic sendiri.**

Jangan membuat:

```text
Correlation
    ↓
Risk Level
```

Correlation hanya informasi statistik.

Risk tetap dihitung berdasarkan faktor yang telah ditentukan dalam `RISK_ENGINE_SPECIFICATION.md`.

---

# 27. Performance Consideration

Analytics harus tetap efisien.

Untuk dataset kecil/menengah, query langsung ke MySQL dapat digunakan.

Untuk dataset besar, dapat dipertimbangkan:

```text
Database
   ↓
Aggregation
   ↓
Cache / Processed Data
   ↓
Visualization
```

Namun optimasi lanjutan dilakukan setelah kebutuhan dataset aktual diketahui.

---

# 28. Definition of Done

Analytics dianggap selesai apabila:

* [ ] GPA distribution tersedia
* [ ] GPA by semester tersedia
* [ ] GPA by major tersedia
* [ ] GPA trend tersedia
* [ ] Attendance vs GPA tersedia
* [ ] Study hours vs GPA tersedia
* [ ] Assignment vs GPA tersedia
* [ ] Midterm vs GPA tersedia
* [ ] Final vs GPA tersedia
* [ ] Correlation heatmap tersedia
* [ ] Filter analytics tersedia
* [ ] Data berasal dari database/dataset aktual
* [ ] Tidak ada hardcoded analytics
* [ ] Empty state tersedia
* [ ] Loading state tersedia
* [ ] Error state tersedia
* [ ] Analytics Service terpisah
* [ ] Dashboard menggunakan Analytics Service
* [ ] Insight menggunakan hasil analytics
* [ ] Interpretasi correlation tidak dianggap sebagai causal relationship
* [ ] Responsive
* [ ] Light/dark mode
* [ ] SVG icons
* [ ] Visual tetap mengikuti desain DM Sans dan UI neutral/minimal

---

## Posisi arsitektur sekarang

Kita sudah memiliki:

```text
                    STUDENT PERFORMANCE ANALYTICS
                               │
        ┌──────────────────────┼──────────────────────┐
        ↓                      ↓                      ↓
      DATA                  ANALYTICS                 ML
        │                      │                      │
        ↓                      ↓                      ↓
   Validation             Visualization          Prediction
        │                      │                      │
        ↓                      ↓                      ↓
   Data Cleaning          Insights              Predicted GPA
        │                                             │
        └──────────────────┐          ┌───────────────┘
                           ↓          ↓
                        RISK ENGINE
                           │
                           ↓
                       Risk Level
                           │
                           ↓
                       Dashboard
```

