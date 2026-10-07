📖 PANDUAN LENGKAP PENGGUNAAN APLIKASI
Saya akan menjelaskan cara menggunakan aplikasi Student Performance Analytics secara detail, dari login hingga menggunakan semua fitur.
🔐 STEP 1: LOGIN KE APLIKASI
Akses Website
1. Buka browser (Chrome, Edge, Firefox)
2. Ketik URL: http://127.0.0.1:5000
3. Akan masuk ke halaman Login
Login Credentials
Ada 2 akun yang tersedia:
👨‍💼 Akun Admin (Full Access)
Username: admin
Password: admin123
- Akses ke semua fitur
- Bisa tambah/edit/hapus mahasiswa
- Bisa train ML models
- Lihat semua data
📊 Akun Analyst (View-Only)
Username: analyst
Password: analyst123
- Hanya bisa lihat data
- Tidak bisa modify/delete
- Bisa buat predictions
- Bisa lihat analytics
Cara Login
1. Masukkan username di field "Username"
2. Masukkan password di field "Password"
3. Klik tombol "Sign In"
4. ✅ Login berhasil → masuk ke Dashboard
📊 STEP 2: DASHBOARD (HOME PAGE)
Setelah login, Anda akan melihat Dashboard Utama.
Apa yang Ditampilkan di Dashboard?
1. KPI Cards (Kartu Statistik)
┌─────────────────────────────────────────┐
│ Total Students: 150                     │
│ At Risk: 18                             │
│ Average GPA: 3.12                       │
│ Average Attendance: 83.5%               │
└─────────────────────────────────────────┘
Keterangan:
- Total Students: Jumlah total mahasiswa di sistem
- At Risk: Mahasiswa dengan risk level HIGH
- Average GPA: Rata-rata GPA semua mahasiswa
- Average Attendance: Rata-rata kehadiran
2. Grafik & Chart
┌─────────────────────────────────────────┐
│ GPA Trend Chart                         │
│ (Menunjukkan trend GPA per semester)    │
│                                         │
│     ↗️ Naik dari S1 ke S4              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ GPA Distribution Chart                  │
│ Excellent: 20%  □                       │
│ Good:      45%  ████                    │
│ Average:   30%  ██                      │
│ Poor:      5%   ░                       │
└─────────────────────────────────────────┘
3. Top 5 At-Risk Students
Tabel dengan kolom:
- Student ID
- Name
- Major
- Risk Level (HIGH/MEDIUM/LOW)
- Actions (View details)
4. Insights (Rekomendasi)
Contoh:
✓ 50 mahasiswa memiliki GPA stabil
✓ 18 mahasiswa memerlukan intervensi
✓ Rata-rata jam belajar: 8.2 jam/minggu
👥 STEP 3: STUDENT MANAGEMENT
Akses Student List
Klik menu "Students" di sidebar atau navigasi
Halaman Students - Apa yang Bisa Dilakukan?
A. LIHAT DAFTAR MAHASISWA
┌────────────────────────────────────────────┐
│ Student List                               │
├────────────────────────────────────────────┤
│ ID          │ Name           │ Major │ S   │
├────────────────────────────────────────────┤
│ 202400001   │ Mahasiswa_1    │ Info  │ 4   │
│ 202400002   │ Mahasiswa_2    │ SI    │ 3   │
│ 202400003   │ Mahasiswa_3    │ Info  │ 5   │
│ ...         │ ...            │ ...   │ ... │
└────────────────────────────────────────────┘
Informasi setiap baris:
- ID: Nomor induk mahasiswa
- Name: Nama lengkap
- Major: Jurusan (Informatics, Information Systems, dll)
- S (Semester): Semester saat ini
B. SEARCH MAHASISWA
1. Cari di search box: "202400001" atau "Mahasiswa_1"
2. Tekan Enter atau klik Search
3. List otomatis filter ke hasil pencarian
C. FILTER MAHASISWA
1. Filter by Major: Pilih jurusan di dropdown
2. Filter by Semester: Pilih semester
3. Kombinasikan kedua filter untuk hasil lebih spesifik
D. PAGINATION (Navigasi Halaman)
Jika ada 150 mahasiswa, tampil 20 per halaman:
[First] [← Previous] Page 1 [Next →] [Last]
- Klik nomor halaman untuk navigate
- Setiap halaman menampilkan 20 mahasiswa
E. ACTION BUTTONS
Untuk setiap mahasiswa ada 3 tombol:
🔍 VIEW Button
- Klik untuk lihat detail mahasiswa
- Tampil: ID, Nama, Jurusan, Semester
✏️ EDIT Button (Admin Only)
- Klik untuk edit data
- Modal akan muncul dengan form
- Bisa ubah: Name, Major, Semester
- Klik "Save" untuk simpan
- Form akan close dan list refresh
🗑️ DELETE Button (Admin Only)
- Klik untuk hapus mahasiswa
- Akan muncul konfirmasi: "Are you sure?"
- Klik OK untuk confirm delete
- Mahasiswa dihapus dari sistem
F. TAMBAH MAHASISWA BARU (Admin Only)
1. Klik tombol "+ Add Student" di atas tabel
2. Modal form akan terbuka dengan field:
   ├── Student ID: 202400XXX (required, unique)
   ├── Full Name: [nama lengkap]
   ├── Major: [jurusan]
   └── Current Semester: [1-8]
3. Isi semua field
4. Klik "Save" button
5. ✅ Student baru ditambahkan ke list
📈 STEP 4: ANALYTICS PAGE
Akses Analytics
Klik menu "Analytics" di sidebar
Halaman Analytics - Menampilkan Analisis Mendalam
A. STATISTIK CARDS
┌─────────────┬─────────────┬─────────────┬──────────┐
│ Total Stud. │ Avg GPA     │ At Risk     │ Avg Att. │
│ 150         │ 3.12        │ 18          │ 83.5%    │
└─────────────┴─────────────┴─────────────┴──────────┘
B. 8 INTERACTIVE CHARTS
Chart 1: GPA Trend
Line chart menunjukkan:
- X-axis: Semester (S1, S2, S3, S4...)
- Y-axis: Average GPA (0-4.0)
- Melihat trend naik/turun GPA per semester
Chart 2: GPA Distribution
Pie/Doughnut chart:
- Excellent (GPA ≥ 3.5): 20%
- Good (3.0-3.5): 45%
- Average (2.5-3.0): 30%
- Poor (< 2.5): 5%
Chart 3: GPA by Major
Bar chart:
- X-axis: Jurusan (Informatics, SI, dll)
- Y-axis: Average GPA
- Bandingkan performa antar jurusan
Chart 4: GPA by Semester
Line chart:
- Trend GPA per semester
- Melihat progression mahasiswa
Chart 5: Attendance vs GPA
Scatter plot (titik-titik):
- X-axis: Attendance (%)
- Y-axis: GPA
- Melihat korelasi kehadiran dengan GPA
Chart 6: Study Hours vs GPA
Scatter plot:
- X-axis: Study Hours per week
- Y-axis: GPA
- Melihat hubungan jam belajar dengan GPA
Chart 7: Score Analysis
Radar chart (bintang):
- Assignment score
- Midterm score
- Final score
- GPA
- Membandingkan level kesulitan
Chart 8: Correlation Matrix
Tabel warna:
         GPA  Att  Assign  Midterm  Final  Study
GPA      1.0  0.72  0.65    0.73   0.68   0.45
Att      0.72 1.0  0.58    0.62   0.60   0.38
...

Warna:
🟢 Hijau (0.6-1.0) = Korelasi kuat positif
🟡 Kuning (0.3-0.6) = Korelasi sedang
🔴 Merah (0-0.3) = Korelasi lemah
⚠️ STEP 5: RISK ANALYSIS PAGE
Akses Risk Analysis
Klik menu "Risk Analysis" di sidebar
Halaman Risk Analysis - Identifikasi Mahasiswa Berisiko
A. RISK LEVEL FILTER
Tombol Filter:
[ All ] [ High Risk ] [ Medium Risk ] [ Low Risk ]
- Default: Semua siswa ditampilkan
- Klik untuk filter berdasarkan risk level
B. RISK STATISTICS CARDS
┌───────────────┬──────────────┬──────────┐
│ 🔴 HIGH RISK  │ 🟠 MED RISK  │ 🟢 LOW   │
│ 18 students   │ 35 students  │ 97 stud. │
│ Intervention  │ Monitor      │ Stable   │
│ Required      │ Closely      │ Perf.    │
└───────────────┴──────────────┴──────────┘
C. RISK ASSESSMENT TABLE
┌────────────┬──────────┬──────────┬────────┬────────┬────────┬────────┐
│ Student ID │ Name     │ Risk Lvl │ GPA R  │ Att R  │ Trend R│ Study R│
├────────────┼──────────┼──────────┼────────┼────────┼────────┼────────┤
│ 202400001  │ Student1 │ 🔴 HIGH  │ [====] │ [=   ] │ [===  ]│ [==   ]│
│ 202400002  │ Student2 │ 🟠 MEDIUM│ [==  ] │ [==  ] │ [=    ]│ [=    ]│
│ 202400003  │ Student3 │ 🟢 LOW   │ [=    ]│ [=    ]│ [=    ]│ [=    ]│
└────────────┴──────────┴──────────┴────────┴────────┴────────┴────────┘

Kolom:
- GPA Risk: Risk dari nilai GPA rendah
- Att Risk: Risk dari kehadiran rendah
- Trend Risk: Risk dari penurunan GPA
- Study Risk: Risk dari jam belajar kurang
D. RISK FACTOR CHARTS
Empat chart menunjukkan breakdown:
1. GPA Risk - Bar chart
2. Attendance Risk - Doughnut chart
3. Score Trend Risk - Polar area chart
4. Study Hours Risk - Line chart
E. RISK INTERPRETATION
🔴 HIGH RISK (Risk Score ≥ 2.0)
   → Butuh intervensi segera
   → Hubungi untuk academic counseling
   → Bisa di-referral ke remedial

🟠 MEDIUM RISK (1.0 - 2.0)
   → Monitor progress semester depan
   → Berikan motivasi
   → Lihat trend perbaikan

🟢 LOW RISK (< 1.0)
   → Performa stabil
   → Pertahankan konsistensi
   → Bisa jadi tutor peer
🔮 STEP 6: PREDICTION PAGE
Akses Prediction
Klik menu "Prediction" di sidebar
Halaman Prediction - Prediksi GPA Semester Depan
A. PREDICTION FORM
Left Panel: Input Form
┌─────────────────────────────────────────┐
│ PREDICTION SIMULATOR                    │
├─────────────────────────────────────────┤
│                                         │
│ Select Student: [Dropdown ▼]           │
│   202400001 - Mahasiswa_1               │
│   202400002 - Mahasiswa_2               │
│   202400003 - Mahasiswa_3               │
│   ...                                   │
│                                         │
│ ACADEMIC SCORES:                        │
│ ├─ Assignment Score: [75    ]           │
│ ├─ Midterm Score:    [80    ]           │
│ ├─ Final Score:      [82    ]           │
│ └─ Attendance Rate:  [85.5  ] %         │
│                                         │
│ LEARNING HABITS:                        │
│ └─ Study Hours/Week: [10    ]           │
│                                         │
│ [ Generate Prediction ] [ Clear Form ]  │
│                                         │
└─────────────────────────────────────────┘
B. CARA INPUT DATA
Langkah 1: Pilih Student
1. Klik dropdown "Select Student"
2. Pilih mahasiswa dari list
3. Contoh: "202400001 - Mahasiswa_1"
Langkah 2: Input Academic Scores
Assignment Score: Masukkan nilai tugas (0-100)
  Contoh: 75 (atau 78.5 jika ada decimal)

Midterm Score: Masukkan nilai UTS (0-100)
  Contoh: 80

Final Score: Masukkan nilai UAS (0-100)
  Contoh: 82

Attendance Rate: Masukkan persentase kehadiran (0-100%)
  Contoh: 85.5
Langkah 3: Input Learning Habits
Study Hours/Week: Jam belajar per minggu (0-168)
  Contoh: 10 (berarti 10 jam/minggu)
Langkah 4: Generate Prediction
1. Klik tombol "Generate Prediction"
2. Sistem akan:
   ✓ Validate input
   ✓ Scale features
   ✓ Load trained model
   ✓ Calculate prediction
3. Hasil muncul di right panel
C. PREDICTION RESULT (Right Panel)
┌─────────────────────────────────────────┐
│ PREDICTION RESULT                       │
├─────────────────────────────────────────┤
│                                         │
│ Predicted GPA                           │
│           3.42                          │
│                                         │
│ ┌────────────────────────────┐          │
│ │ Model: GradientBoosting    │          │
│ │ Confidence: 92.3%          │          │
│ │ MAE: 0.1852                │          │
│ │ RMSE: 0.2425               │          │
│ └────────────────────────────┘          │
│                                         │
│ Catatan:                                │
│ Prediksi berdasarkan performa saat ini. │
│ Hasil aktual bisa berbeda dengan       │
│ effort dan faktor eksternal.           │
│                                         │
└─────────────────────────────────────────┘
Penjelasan Hasil:
Predicted GPA: 3.42
  → Prediksi GPA semester depan

Model Used: GradientBoosting
  → Model ML yang digunakan untuk prediksi

Confidence (R²): 92.3%
  → Tingkat akurasi model (semakin tinggi semakin baik)

MAE: 0.1852
  → Mean Absolute Error (rata-rata penyimpangan absolut)
  → Contoh: prediksi bisa meleset ±0.185

RMSE: 0.2425
  → Root Mean Squared Error
  → Ukuran error yang lebih sensitif ke outlier
D. HISTORICAL PREDICTIONS TABLE
Tabel yang menampilkan prediksi sebelumnya:

Student │ Semester │ Predicted │ Actual │ Model  │ MAE    │ RMSE
--------|----------|-----------|--------|--------|--------|--------
Stud.1  │ S2       │ 3.40      │ 3.38   │ GB     │ 0.1850 │ 0.2400
Stud.2  │ S3       │ 3.15      │ 3.18   │ RF     │ 0.1920 │ 0.2510
Stud.3  │ S2       │ 2.85      │ 2.87   │ LR     │ 0.2100 │ 0.2800
...
📱 STEP 7: NAVIGATION & SIDEBAR
Struktur Menu
┌─────────────────────────────┐
│ SPA                         │
│ Student Performance         │
├─────────────────────────────┤
│ OVERVIEW                    │
│ ├─ 📊 Dashboard            │
│ ├─ 👥 Students             │
│ └─ 📈 Analytics            │
│                             │
│ INTELLIGENCE                │
│ ├─ 🔮 Prediction           │
│ └─ ⚠️  Risk Analysis        │
│                             │
│ [Admin Only]                │
│ ├─ 📁 Dataset              │
│ └─ 🤖 Training             │
├─────────────────────────────┤
│ [Admin]                     │
│ Logout                      │
└─────────────────────────────┘
Keterangan Menu
Menu	Akses
Dashboard	Semua
Students	Semua
Analytics	Semua
Prediction	Semua
Risk Analysis	Semua
Dataset	Admin
Training	Admin
🌓 STEP 8: THEME & SETTINGS
Dark/Light Mode
Tombol di top-right navbar (◐ icon)
Klik untuk toggle antara:
- 🌞 Light Mode (default)
- 🌙 Dark Mode

Preference disimpan di browser localStorage
User Info
Di bottom sidebar:
- Username yang login
- Role (ADMIN / ANALYST)

Klik Logout untuk keluar
💡 CONTOH USE CASE LENGKAP
Skenario: Admin Ingin Monitor Mahasiswa Berisiko
Step 1: Login
Username: admin
Password: admin123
→ Masuk ke Dashboard
Step 2: Lihat Statistics
Dashboard menampilkan:
- Total: 150 mahasiswa
- At Risk: 18 mahasiswa
Step 3: Cek Risk Analysis
1. Klik "Risk Analysis" menu
2. Filter "High Risk"
3. Lihat 18 mahasiswa dengan HIGH risk
Step 4: Analisis Penyebab
1. Klik "Analytics"
2. Lihat chart:
   - GPA trend menurun
   - Attendance rendah
   - Study hours kurang
Step 5: Prediksi GPA Semester Depan
1. Klik "Prediction"
2. Pilih mahasiswa berisiko
3. Input data akademik saat ini
4. Lihat prediksi GPA semester depan
5. Tentukan aksi (intervention, tutoring, dll)
Step 6: Manage Mahasiswa
1. Klik "Students"
2. Search mahasiswa tertentu
3. Edit data jika perlu
4. Add mahasiswa baru
🎯 TIPS PENGGUNAAN
✅ Best Practices
1. PASTIKAN DATA ACCURATE
   - GPA valid: 0.0 - 4.0
   - Attendance: 0 - 100%
   - Scores: 0 - 100

2. UPDATE REGULAR
   - Input data setiap semester
   - Keep tracking progress
   - Monitor trends

3. USE PREDICTIONS WISELY
   - Predictions ≠ certainties
   - Use sebagai guidance, bukan keputusan final
   - Kombinasikan dengan penilaian human

4. MONITOR AT-RISK STUDENTS
   - Follow up dengan counseling
   - Provide academic support
   - Check progress regularly

5. LEVERAGE ANALYTICS
   - Identify patterns & trends
   - Find correlation factors
   - Make data-driven decisions
❌ Common Mistakes
❌ Input data yang tidak valid
   ✅ Pastikan range sesuai

❌ Forget to save changes
   ✅ Klik Save button setelah edit

❌ Percaya 100% pada predictions
   ✅ Gunakan sebagai insight tambahan

❌ Ignore low-risk students
   ✅ Monitor semua, tidak hanya at-risk

❌ Jarang update data
   ✅ Update regularly untuk akurasi
📊 DATA INPUT REFERENCE
Inputan yang Diperlukan untuk Prediction
┌────────────────────────────────────────┐
│ FIELD                  │ RANGE │ NOTES  │
├────────────────────────┼───────┼────────┤
│ Assignment Score       │ 0-100 │ Nilai  │
│ Midterm Score          │ 0-100 │ Nilai  │
│ Final Score            │ 0-100 │ Nilai  │
│ Attendance Rate        │ 0-100 │ % keha │
│ Study Hours/Week       │ 0-168 │ jam/mg │
└────────────────────────┴───────┴────────┘

Format inputan:
- Decimal OK: 75.5, 85.25
- Whole number: 75, 80
- Hindari: tanda khusus, huruf
Risk Level Interpretation
GPA < 2.5          → HIGH GPA Risk
Attendance < 75%   → HIGH Attendance Risk
Score Avg < 60     → HIGH Score Risk
Study Hours < 5    → MEDIUM Study Risk

Overall Risk Score Calculation:
Average dari semua risk factors
≥ 2.0 → HIGH RISK
1.0-2.0 → MEDIUM RISK
< 1.0 → LOW RISK
✨ KESIMPULAN
Aplikasi Student Performance Analytics memudahkan Anda untuk:
1. 📊 Monitor performa akademik mahasiswa secara real-time
2. 🔍 Analyze trends dan patterns dari data
3. ⚠️ Identify mahasiswa berisiko lebih awal
4. 🔮 Predict GPA semester depan berdasarkan data
5. 🎯 Make keputusan berbasis data untuk academic intervention
Siap untuk mulai menggunakan aplikasi? 🚀
Buka browser dan akses: http://127.0.0.1:5000