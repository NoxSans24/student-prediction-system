# INSIGHT_SPECIFICATION.md

Bagian ini mendefinisikan **Automated Academic Insights**. Tujuannya adalah mengubah hasil Analytics menjadi informasi yang mudah dipahami oleh Admin/Analyst.

Prinsip utamanya:

> **Insight harus selalu berasal dari data aktual dan tidak boleh menggunakan klaim yang di-hardcode.**

---

# 1. Tujuan Insight Engine

Insight Engine berada setelah Analytics:

```text id="q1m7xa"
Database
   ↓
Analytics Service
   ↓
Statistical Results
   ↓
Insight Engine
   ↓
Academic Insights
   ↓
Dashboard / Analytics
```

Contoh:

```text id="h9wq2p"
Average GPA
Semester 3 = 3.12
Semester 4 = 3.28
        ↓
Difference = +0.16
        ↓
Insight:
"Average GPA increased compared with
the previous semester."
```

---

# 2. Prinsip Insight

Insight harus:

* berdasarkan data aktual
* dinamis
* dapat berubah ketika dataset berubah
* mudah dipahami
* singkat
* relevan terhadap kondisi akademik
* tidak memberikan kesimpulan sebab-akibat tanpa bukti

Insight tidak boleh seperti:

```python
return "Students are performing better."
```

tanpa melakukan analisis terhadap data.

---

# 3. Jenis Insight

Insight Engine memiliki beberapa kategori:

```text id="7d5f2x"
Academic Performance
        │
        ├── GPA Trend
        ├── Performance Distribution
        ├── Attendance
        ├── Score Performance
        ├── Study Hours
        ├── Risk
        └── Correlation
```

---

# 4. GPA Trend Insight

Insight pertama berasal dari perubahan GPA.

Data yang diperlukan:

```text id="qzq6f1"
Current Average GPA
Previous Average GPA
Difference
Percentage Change
```

Contoh:

```text id="r9t4xp"
Previous GPA = 3.10
Current GPA  = 3.25
Difference   = +0.15
```

Insight:

> Average GPA increased compared with the previous semester.

Jika turun:

> Average GPA decreased compared with the previous semester.

Jika hampir tidak berubah:

> Average GPA remained relatively stable compared with the previous semester.

Threshold "relatively stable" harus menjadi konfigurasi aplikasi, bukan angka tersebar di berbagai file.

---

# 5. GPA Distribution Insight

Insight dapat dibuat berdasarkan distribusi kategori performa.

Contoh:

```text id="a1r2k8"
Excellent → 25%
Good      → 45%
Average   → 25%
Poor       → 5%
```

Sistem dapat menentukan kategori yang paling dominan:

```text id="3lq9af"
Dominant Category = Good
```

Insight:

> Most students are currently in the Good performance category.

Namun jika distribusi berubah:

> Most students are currently in the Average performance category.

Jadi kalimat mengikuti hasil aktual.

---

# 6. Attendance Insight

Data:

```text id="k8r4tz"
Average Attendance
Previous Attendance
Attendance Change
```

Contoh:

```text id="q5a0xm"
Previous = 82%
Current  = 87%
```

Insight:

> Average attendance increased compared with the previous semester.

Jika menurun:

> Average attendance decreased compared with the previous semester.

---

# 7. Low Attendance Insight

Sistem dapat menghitung jumlah mahasiswa dengan attendance rendah.

Contoh:

```text id="0g3jbs"
Total Students       = 100
Low Attendance       = 12
Percentage           = 12%
```

Insight:

> 12% of students have relatively low attendance.

Batas "low attendance" harus berasal dari konfigurasi Risk/Analytics, bukan hardcoded di fungsi insight.

---

# 8. Score Performance Insight

Insight dapat melihat:

```text id="f4v8xq"
Assignment Score
Midterm Score
Final Score
```

Tujuannya menemukan komponen dengan rata-rata terendah/tertinggi.

Contoh:

```text id="6s0lwv"
Assignment = 82
Midterm    = 76
Final      = 85
```

Maka:

> Midterm scores have the lowest average among the main academic assessments.

Jika hasil dataset berbeda, insight juga berubah.

---

# 9. Study Hours Insight

Data:

```text id="k2b8pz"
Average Study Hours
```

Insight sederhana:

> Average study time is X hours per week.

Namun insight tidak boleh mengatakan:

> More study hours cause higher GPA.

Karena Analytics hanya menunjukkan hubungan/pola, bukan causal relationship.

---

# 10. Correlation Insight

Correlation berasal dari:

```text id="8r7k1p"
Correlation Matrix
```

Contoh:

```text
Final Score ↔ GPA = 0.76
Midterm      ↔ GPA = 0.70
Attendance   ↔ GPA = 0.42
```

Insight:

> Final score shows the strongest positive correlation with GPA among the analyzed academic factors.

Angka correlation harus dihitung dari data aktual.

---

# 11. Risk Insight

Insight juga dapat mengambil hasil dari Risk Engine.

Contoh:

```text id="x5u7cf"
Low Risk     = 70
Medium Risk  = 20
High Risk    = 10
```

Insight:

> 10% of students are currently classified as high risk.

Atau:

> 30 students require academic attention based on the current risk assessment.

Jumlah harus berasal dari Risk Engine.

---

# 12. Students Requiring Attention

Dashboard memiliki bagian:

```text id="q6s2xz"
Students Requiring Attention
```

Insight Engine dapat menentukan jumlah mahasiswa yang perlu diperhatikan berdasarkan hasil Risk Engine.

Contoh:

```text id="3h6v5s"
High Risk
+
Significant GPA Decline
+
Attendance Decline
```

Kemudian Dashboard menampilkan mahasiswa terkait.

Tetapi **Insight Engine tidak menggantikan Risk Engine**.

Pembagian:

```text id="j4r8ny"
Risk Engine
     ↓
Risk Level + Risk Factors
     ↓
Insight Engine
     ↓
Human-readable Insight
```

---

# 13. Insight Priority

Tidak semua insight harus ditampilkan sekaligus.

Insight dapat memiliki priority:

```text id="9m4xqf"
high
medium
low
```

Contoh:

### High

```text
High-risk students increased significantly.
```

### Medium

```text
Average GPA decreased compared with the previous semester.
```

### Low

```text
Average study hours remained relatively stable.
```

Priority digunakan agar Dashboard tidak terlalu penuh.

---

# 14. Insight Object

Insight sebaiknya memiliki struktur data yang konsisten.

Contoh:

```json id="6j9x4m"
{
    "type": "gpa_trend",
    "priority": "medium",
    "title": "GPA Trend",
    "message": "Average GPA increased compared with the previous semester.",
    "value": 3.25,
    "change": 0.15
}
```

Struktur ini memudahkan frontend menampilkan insight.

---

# 15. Insight Service

Buat service:

```text id="j4m8tw"
services/
└── insight_service.py
```

Fungsi yang disarankan:

```python id="b7r2sp"
generate_gpa_insight()
generate_distribution_insight()
generate_attendance_insight()
generate_score_insight()
generate_study_hours_insight()
generate_correlation_insight()
generate_risk_insight()
generate_all_insights()
```

Fungsi utama:

```python id="n8v5kq"
generate_all_insights()
```

menggabungkan seluruh insight yang tersedia.

---

# 16. Insight Generation Flow

```text id="z5p3hy"
Analytics Service
       ↓
Calculate Metrics
       ↓
Insight Service
       ↓
Apply Insight Rules
       ↓
Generate Messages
       ↓
Assign Priority
       ↓
Sort Insights
       ↓
Dashboard
```

---

# 17. Insight Rules

Rule sebaiknya dipisahkan dari UI.

Contoh:

```python id="8z0f4a"
if current_gpa > previous_gpa:
    ...
elif current_gpa < previous_gpa:
    ...
else:
    ...
```

Jangan membuat rule di HTML atau JavaScript.

Arsitektur:

```text id="4p8zqv"
Database
   ↓
Analytics
   ↓
Insight Service
   ↓
Flask Route
   ↓
Template / JSON
```

---

# 18. Configurable Threshold

Threshold harus dapat dikonfigurasi.

Contoh:

```python id="r2n7xm"
INSIGHT_CONFIG = {
    "stable_gpa_change": 0.05,
    "significant_change": 0.20
}
```

Nilai di atas hanya contoh desain.

Nilai final harus ditentukan setelah melihat dataset aktual dan pengujian.

Tujuannya supaya tidak ada angka seperti:

```python
if change > 0.17:
```

tersebar di banyak file tanpa penjelasan.

---

# 19. Multiple Insights

Satu Dashboard dapat menghasilkan beberapa insight.

Contoh:

```text id="e4w7vn"
Academic Insights

1. Average GPA increased compared with the previous semester.

2. Final score has the strongest positive correlation
   with GPA among the analyzed factors.

3. 12% of students are currently classified as high risk.

4. Attendance increased compared with the previous semester.
```

Jumlah insight yang ditampilkan dapat dibatasi agar Dashboard tetap bersih.

---

# 20. Insight Ranking

Jika terdapat banyak insight:

```text id="4v8p3a"
Generate
   ↓
Filter Valid Insights
   ↓
Priority
   ↓
Severity
   ↓
Limit Results
```

Contoh:

```python id="x2f9mw"
MAX_DASHBOARD_INSIGHTS = 4
```

Dashboard hanya menampilkan insight paling relevan.

Halaman Analytics dapat menampilkan insight lebih lengkap.

---

# 21. Invalid Insight Prevention

Insight harus dicegah jika data tidak mencukupi.

Contoh:

```text id="q3n6ys"
Previous semester unavailable
```

Jangan menghasilkan:

> GPA increased compared with previous semester.

Sebaliknya:

> GPA trend is currently unavailable because previous semester data is missing.

---

# 22. Empty Dataset

Jika belum ada data:

```text id="f7k2xw"
No insights available yet.

Add or upload academic data to generate insights.
```

Tidak boleh membuat insight palsu.

---

# 23. Insufficient Data

Misalnya hanya terdapat satu record semester.

Maka:

```text id="7z9mqp"
Current GPA = 3.21
Previous GPA = unavailable
```

Sistem tetap dapat membuat:

> Current average GPA is 3.21.

Tetapi tidak boleh membuat:

> GPA increased compared with the previous semester.

---

# 24. Insight API

Jika frontend membutuhkan data dinamis:

```text id="t5x8vn"
/api/insights
```

Response:

```json id="g2w7cz"
{
    "insights": [
        {
            "type": "gpa_trend",
            "priority": "medium",
            "title": "GPA Trend",
            "message": "Average GPA increased compared with the previous semester."
        },
        {
            "type": "risk",
            "priority": "high",
            "title": "Students at Risk",
            "message": "10% of students are currently classified as high risk."
        }
    ]
}
```

---

# 25. Dashboard Presentation

Bagian Dashboard:

```text id="z4q8tw"
Academic Insights
─────────────────────────────────────

↑ GPA Trend
Average GPA increased compared with
the previous semester.

! Students at Risk
10% of students are currently classified
as high risk.

• Performance
Most students are currently in the
Good performance category.
```

Icon menggunakan **SVG**, mengikuti aturan UI project.

Tidak menggunakan Unicode emoji.

---

# 26. Light / Dark Mode

Insight component harus mengikuti design system.

Light:

```text id="y8p2fk"
Background: #FFFFFF
Border: #E5E5E3
Text: #171717
Secondary: #737373
```

Dark:

```text id="3v6rpa"
Background: #181818
Border: #2A2A2A
Text: #F5F5F5
Secondary: #A3A3A3
```

Status color hanya digunakan jika memang memiliki makna:

```text id="s2k6cx"
Low     → muted green
Medium  → muted amber
High    → muted red
```

Tidak menggunakan neon atau gradient berlebihan.

---

# 27. Insight dan Machine Learning

Insight tidak boleh mengambil hasil ML secara sembarangan.

Contoh yang valid:

> “The selected model achieved an R² of 0.91 on the test dataset.”

Tetapi insight ML sebaiknya berada di **ML Report / Prediction page**, bukan menjadi insight utama Dashboard kecuali memang relevan.

Dashboard lebih berfokus pada:

```text id="7m2z4c"
Current Performance
Trend
Risk
Attention
```

---

# 28. Insight dan Risk Engine

Pembagian final:

```text id="r3q8wp"
                    Academic Data
                         │
             ┌───────────┴───────────┐
             ↓                       ↓
        Analytics               Risk Engine
             │                       │
             ↓                       ↓
      Statistical Data         Risk Assessment
             │                       │
             └───────────┬───────────┘
                         ↓
                   Insight Engine
                         │
                         ↓
                 Academic Insights
```

Dengan demikian:

* Analytics menghitung data.
* Risk Engine menghitung risiko.
* Insight Engine menjelaskan hasilnya.

---

# 29. Definition of Done

Insight Engine dianggap selesai jika:

* [ ] GPA trend insight tersedia
* [ ] GPA distribution insight tersedia
* [ ] Attendance insight tersedia
* [ ] Score performance insight tersedia
* [ ] Study hours insight tersedia
* [ ] Correlation insight tersedia
* [ ] Risk insight tersedia
* [ ] Insight berasal dari data aktual
* [ ] Tidak ada klaim hardcoded
* [ ] Tidak ada causal claim tanpa bukti
* [ ] Insight memiliki kategori
* [ ] Insight memiliki priority
* [ ] Insight dapat diurutkan
* [ ] Threshold dapat dikonfigurasi
* [ ] Missing data ditangani
* [ ] Empty state tersedia
* [ ] API insight tersedia jika diperlukan
* [ ] Dashboard dapat menampilkan insight
* [ ] Light mode tersedia
* [ ] Dark mode tersedia
* [ ] SVG icons digunakan
* [ ] Tidak ada Unicode emoji
* [ ] Responsive
* [ ] Tidak mengganggu fokus data-first Dashboard

---

## Arsitektur yang sudah terbentuk

Sekarang alurnya semakin lengkap:

```text
                    ┌──────────────┐
                    │    DATA      │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  VALIDATION  │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ DATA CLEANING│
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   ANALYTICS  │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
        Dashboard       Insights       ML
             │             │             │
             │             │             ↓
             │             │       GPA Prediction
             │             │
             └──────┬──────┘
                    ↓
              Risk Analysis
                    │
                    ↓
             Early Warning
                    │
                    ↓
                 Reports
```
