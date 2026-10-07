1. Tujuan

Risk Engine bertugas mengidentifikasi mahasiswa yang berpotensi mengalami masalah akademik berdasarkan data performa.

Output utama:

LOW
MEDIUM
HIGH

Risk Analysis dalam PRD mempertimbangkan:

GPA
Attendance
Score Trend
Study Hours
Previous GPA
Assignment Score
Midterm Score
Final Score

2. Konsep Risk Engine

Alur:

Academic Records
       ↓
Feature Extraction
       ↓
Risk Factor Analysis
       ↓
Risk Score
       ↓
Risk Level
       ↓
Early Warning
       ↓
Student Attention List

Risk Engine tidak hanya melihat GPA saat ini.

Contohnya:

Mahasiswa A
GPA        = 3.20
Attendance = 92%
Trend      = meningkat

bisa memiliki risiko lebih rendah dibanding:

Mahasiswa B
GPA        = 3.30
Attendance = 68%
Trend      = menurun

Karena sistem juga mempertimbangkan perubahan performa.

3. Risk Factors
Faktor	Sumber
Current GPA	academic_records.gpa
Attendance	academic_records.attendance
Previous GPA	academic_records.gpa semester sebelumnya
GPA Trend	Academic history
Study Hours	academic_records.study_hours
Assignment	assignment_score
Midterm	midterm_score
Final	final_score
4. Current GPA

Current GPA merupakan GPA pada semester terbaru mahasiswa.

Query konsep:

SELECT *
FROM academic_records
WHERE student_id = ?
ORDER BY semester DESC
LIMIT 1;

Contoh:

Semester 4
GPA = 2.45

Risk Engine menggunakan nilai tersebut sebagai salah satu faktor.

5. Previous GPA

Previous GPA adalah GPA semester sebelum semester aktif.

Contoh:

Semester 3 → 3.20
Semester 4 → 2.60

Maka:

Previous GPA = 3.20
Current GPA  = 2.60
6. GPA Change

Formula:

GPA Change = Current GPA - Previous GPA

Contoh:

Current  = 2.60
Previous = 3.20

Change = -0.60

Artinya terjadi penurunan.

Sebaliknya:

Current  = 3.50
Previous = 3.20

Change = +0.30

berarti performa meningkat.

7. Score Trend

Score trend digunakan untuk melihat perubahan nilai akademik.

Contoh:

Assignment
Semester 3 = 82
Semester 4 = 70

Midterm
Semester 3 = 80
Semester 4 = 68

Final
Semester 3 = 84
Semester 4 = 65

Sistem dapat mengidentifikasi:

Score Trend = Declining
8. Attendance

Attendance menjadi salah satu indikator risiko.

Data:

attendance

berupa persentase:

0 - 100

Contoh:

95% → kondisi attendance relatif baik
70% → perlu perhatian

Namun angka threshold resmi belum ditetapkan dalam PRD.

Jadi nilai seperti 70% di atas hanya contoh interpretasi, bukan aturan final.

9. Study Hours

Study hours digunakan sebagai faktor tambahan.

Contoh:

study_hours = 5

dibandingkan dengan:

study_hours = 18

Tetapi kita tidak akan mengatakan:

"5 jam pasti berisiko."

Karena study hours harus dianalisis bersama faktor lain.

10. Academic Score Factors

Tiga nilai:

Assignment
Midterm
Final

dapat digunakan untuk melihat kondisi akademik mahasiswa.

Contoh:

Assignment = 60
Midterm    = 65
Final      = 58

Jika nilai tersebut juga menurun dibandingkan periode sebelumnya, risk engine dapat memberikan faktor:

Declining Academic Scores
11. Risk Score

Kita membutuhkan satu nilai numerik internal:

risk_score

Range yang disarankan untuk desain awal:

0 - 100

Interpretasi:

0   → risiko sangat rendah
100 → risiko sangat tinggi

Ini adalah keputusan desain, bukan threshold yang berasal dari PRD.

12. Risk Score Architecture

Daripada langsung membuat satu formula besar, gunakan beberapa komponen:

                    ┌───────────────┐
                    │ Current GPA   │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │ Attendance    │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │ GPA Trend     │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │ Score Trend   │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │ Study Hours   │
                    └───────┬───────┘
                            │
                            ▼
                     Risk Calculation
                            │
                            ▼
                       Risk Score
                            │
                            ▼
                       Risk Level
13. Risk Components

Untuk MVP, kita bisa membuat komponen:

gpa_risk
attendance_risk
gpa_trend_risk
score_trend_risk
study_hours_risk

Kemudian:

risk_score =
    gpa_risk
    + attendance_risk
    + gpa_trend_risk
    + score_trend_risk
    + study_hours_risk

Bobot belum boleh dianggap final.

14. Mengapa Tidak Langsung Menggunakan Bobot?

Karena PRD tidak menetapkan:

GPA = 40%
Attendance = 20%
Trend = 20%
Study Hours = 20%

Jadi jangan menulis angka tersebut seolah-olah berasal dari requirements.

Bobot sebaiknya ditentukan setelah:

dataset tersedia,
data dieksplorasi,
distribusi faktor diketahui,
rule diuji,
hasil dievaluasi.
15. Risk Level

Secara konsep:

LOW
MEDIUM
HIGH

PRD secara eksplisit menggunakan tiga kategori tersebut.

Untuk implementasi awal, kita bisa menggunakan konfigurasi:

RISK_THRESHOLDS = {
    "low_max": ...,
    "medium_max": ...
}

Jadi threshold tidak ditulis tersebar di banyak file.

16. Configurable Threshold

Contoh struktur:

RISK_THRESHOLDS = {
    "low_max": 30,
    "medium_max": 60
}

Maka:

0 - 30     → LOW
31 - 60    → MEDIUM
61 - 100   → HIGH

Angka tersebut hanya contoh konfigurasi awal dan belum menjadi keputusan final.

Nantinya threshold dapat diubah tanpa mengubah logic utama Risk Engine.

17. Risk Factor Explanation

Sistem tidak cukup menampilkan:

HIGH

Tetapi juga harus menjelaskan penyebabnya.

Contoh:

Risk Level: HIGH

Main Factors:
• GPA decreased significantly
• Attendance is low
• Final score decreased
• Study hours decreased

Field ini dapat disimpan pada:

risk_assessments.main_factors
18. Risk Assessment Example

Misalnya:

Student:
STD003

Current GPA:
2.21

Previous GPA:
2.80

Attendance:
68%

Study Hours:
6

Assignment:
61

Midterm:
64

Final:
59

Risk Engine menganalisis:

GPA
↓

Attendance
↓
GPA Trend
↓
Score Trend
↓
Study Hours
↓

Kemudian menghasilkan:

Risk Level:
HIGH

Main Factors:
- GPA decline
- Low attendance
- Low academic scores
- Low study hours

Nilai risk score aktual harus berasal dari formula yang telah ditentukan dan diuji.

19. Early Warning

Risk Analysis juga harus mendeteksi perubahan signifikan.

PRD menyebutkan:

significant GPA decline
significant attendance decline
significant score decline
configurable thresholds

20. GPA Early Warning

Contoh konsep:

Previous GPA
     ↓
Current GPA
     ↓
Calculate Change
     ↓
Compare Threshold
     ↓
Warning

Contoh:

Previous GPA = 3.50
Current GPA  = 2.90

Change = -0.60

Jika perubahan tersebut melewati threshold yang dikonfigurasi:

EARLY WARNING
21. Attendance Early Warning

Konsep:

Previous Attendance
        ↓
Current Attendance
        ↓
Calculate Difference
        ↓
Compare Threshold

Contoh:

Previous = 94%
Current  = 76%

Change = -18 percentage points

Jika melewati configured threshold:

Attendance Decline
22. Score Early Warning

Bisa diterapkan pada:

Assignment
Midterm
Final

Contoh:

Final Previous = 84
Final Current  = 65

Change = -19

Output:

Final Score Decline
23. Early Warning Object

Secara internal kita dapat menghasilkan struktur:

{
    "student_id": "STD003",
    "warnings": [
        {
            "type": "gpa_decline",
            "severity": "high"
        },
        {
            "type": "attendance_decline",
            "severity": "medium"
        },
        {
            "type": "score_decline",
            "severity": "high"
        }
    ]
}
24. Student Attention List

Output Risk Engine digunakan Dashboard untuk bagian:

Students Requiring Attention

Dashboard.md menentukan tabel:

Student
Major
GPA
Attendance
Change
Risk

Query konsep:

SELECT
    s.student_id,
    s.name,
    s.major,
    a.gpa,
    a.attendance,
    r.risk_level
FROM students s
JOIN academic_records a
    ON s.id = a.student_id
JOIN risk_assessments r
    ON s.id = r.student_id
WHERE r.risk_level IN ('medium', 'high');
25. Risk Engine Service

Struktur Python:

services/
└── risk_service.py

Fungsi:

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
26. Risk Engine Flow
Student ID
    ↓
Get Academic History
    ↓
Sort by Semester
    ↓
Get Current Record
    ↓
Get Previous Record
    ↓
Calculate:
    ├── GPA Change
    ├── Attendance Change
    ├── Score Change
    └── Study Hours
    ↓
Calculate Risk Components
    ↓
Calculate Risk Score
    ↓
Determine Risk Level
    ↓
Generate Main Factors
    ↓
Generate Early Warning
    ↓
Save Assessment
27. Important: Risk Engine vs Machine Learning

Risk Engine tidak sama dengan ML Prediction.

Risk Engine

Rule-based:

Current GPA
Attendance
Trend
Study Hours
Scores
        ↓
Risk Level
Machine Learning

Model-based:

Features
   ↓
Trained Model
   ↓
Predicted GPA

Jangan mencampurkan keduanya.

28. Risk Analysis vs Prediction

Contoh:

Prediction
──────────
Predicted GPA = 2.75

Sedangkan:

Risk Analysis
──────────────
Risk = HIGH

Factors:
GPA declining
Attendance declining
Final score declining

Keduanya dapat saling melengkapi tetapi mempunyai tujuan berbeda.

29. Dashboard Integration

Risk Engine menyediakan:

Total At Risk
        ↓
Risk Distribution
        ↓
Students Requiring Attention
        ↓
Academic Insights

Dashboard dapat menampilkan:

At Risk Students
─────────────────
HIGH     12
MEDIUM   27
LOW      209

Angka harus berasal dari database aktual.

30. Risk Engine Database Flow
academic_records
       │
       ▼
 risk_service.py
       │
       ▼
risk_assessments
       │
       ├── Dashboard
       ├── Risk Analysis
       ├── Student Profile
       └── Reports
31. Recalculation

Risk assessment harus dapat dihitung ulang ketika data akademik berubah.

Contoh:

Academic Data Updated
        ↓
Risk Assessment Invalidated
        ↓
Run Risk Engine
        ↓
New Risk Assessment

Jangan menganggap risk level lama selalu valid.

32. Risk Assessment Version

Untuk pengembangan lebih lanjut, sebaiknya hasil assessment menyimpan informasi:

assessment_date

dan nantinya dapat ditambahkan:

engine_version

Contoh:

Risk Engine v1
Risk Engine v2

Hal ini berguna jika formula risk berubah.

Untuk MVP, engine_version belum wajib.

33. Definition of Done

Risk Engine dianggap selesai jika:

 Bisa mengambil academic history
 Bisa menentukan current GPA
 Bisa menentukan previous GPA
 Bisa menghitung GPA change
 Bisa menghitung attendance change
 Bisa menganalisis score trend
 Bisa mempertimbangkan study hours
 Menghasilkan risk score
 Menghasilkan LOW/MEDIUM/HIGH
 Menghasilkan alasan risiko
 Menghasilkan early warning
 Menyimpan hasil ke database
 Dapat digunakan Dashboard
 Threshold dapat dikonfigurasi
 Tidak menggunakan hardcoded student results
34. Status Project Sekarang

Kita sudah memiliki:

PRD.MD
   ↓
Dashboard.md
   ↓
DATA_SPECIFICATION.md
   ↓
DATABASE_SCHEMA.md
   ↓
DATA_CLEANING_SPEC.md
   ↓
RISK_ENGINE_SPEC.md

Selanjutnya ada dua fondasi besar:

                PROJECT
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
  DATA PIPELINE              ML
        │                     │
        ▼                     ▼
  Analytics Engine      ML Specification
        │                     │
        └──────────┬──────────┘
                   ▼
              Application