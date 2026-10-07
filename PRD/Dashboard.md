1. Struktur Dashboard

Layout utama:

┌──────────────────────────────────────────────────────────────┐
│ Sidebar │ Topbar                                             │
│         ├─────────────────────────────────────────────────────┤
│         │                                                     │
│         │  Dashboard                                          │
│         │  Overview of your academic data                    │
│         │                                                     │
│         │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│         │  │Students │ │ Avg GPA │ │Attend.  │ │At Risk  │ │
│         │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│         │                                                     │
│         │  ┌──────────────────────────┐ ┌──────────────────┐ │
│         │  │                          │ │                  │ │
│         │  │       GPA Trend          │ │ Performance      │ │
│         │  │                          │ │ Distribution     │ │
│         │  │                          │ │                  │ │
│         │  └──────────────────────────┘ └──────────────────┘ │
│         │                                                     │
│         │  ┌──────────────────────────┐ ┌──────────────────┐ │
│         │  │                          │ │                  │ │
│         │  │ Attendance vs GPA        │ │ GPA by Major     │ │
│         │  │                          │ │                  │ │
│         │  └──────────────────────────┘ └──────────────────┘ │
│         │                                                     │
│         │  ┌────────────────────────────────────────────────┐ │
│         │  │ Academic Insights                              │ │
│         │  │                                                 │ │
│         │  └────────────────────────────────────────────────┘ │
│         │                                                     │
│         │  ┌────────────────────────────────────────────────┐ │
│         │  │ Students Requiring Attention                   │ │
│         │  └────────────────────────────────────────────────┘ │
└─────────┴─────────────────────────────────────────────────────┘
2. Topbar

Topbar dibuat tipis dan tidak mengambil terlalu banyak ruang.

Kiri

Pada desktop:

☰

Tetapi icon-nya SVG, bukan emoji.

Fungsinya:

Collapse sidebar
Expand sidebar
Tengah

Search global:

Search students, major, reports...

Search tidak perlu terlalu besar.

Kanan
Theme Toggle
Notification
Profile

Contoh:

                         ◐    ◇    Muhammad Ihsan

Semua menggunakan SVG.

3. Page Header

Bagian paling atas content:

Dashboard

Overview of your academic data

Di kanan:

Last updated
07 October 2026

Tidak perlu membuat header terlalu besar.

Typography
Dashboard
28px / 700 / DM Sans

Overview of your academic data
14px / 400 / DM Sans
4. KPI Section

Kita gunakan 4 KPI utama.

Card 1 — Total Students
Total Students

1,248

+6.2%
from previous semester

Icon SVG kecil di kiri/atas.

Card 2 — Average GPA
Average GPA

3.42

+0.18
from previous semester

Angka GPA menjadi fokus utama.

Card 3 — Attendance
Average Attendance

87.4%

+2.1%
from previous semester
Card 4 — At Risk
At Risk Students

86

6.9% of students

Untuk card ini baru kita gunakan warna status muted red.

Jangan membuat KPI terlalu dekoratif

Tidak perlu:

Gradient besar
Icon raksasa
Animasi berlebihan
Banyak warna
Progress bar di setiap card

Tujuannya adalah data first.

5. GPA Trend

Ini menjadi chart paling penting di Dashboard.

Ukuran:

~65% width

Judul:

GPA Trend

Subtitle:

Average GPA across semesters

Visual:

Line Chart

3.6 ┤                         ●
3.5 ┤                    ●────
3.4 ┤               ●────
3.3 ┤          ●────
3.2 ┤     ●────
    └──────────────────────────
      S1    S2    S3    S4    S5
Interaction

Hover pada titik:

Semester 4

Average GPA
3.51
6. Performance Distribution

Di sebelah GPA Trend.

Judul:

Performance Distribution

Gunakan Donut Chart atau horizontal bar.

Saya lebih menyarankan Donut Chart yang sederhana.

Kategori:

Excellent
Good
Average
Poor

Contoh:

          ╭──────╮
       ╭──│  42% │──╮
      │   ╰──────╯   │
      │    Good      │
       ╰─────────────╯

Di bawahnya:

Excellent     18%
Good          42%
Average       31%
Poor           9%

Warna tetap muted.

7. Attendance vs GPA

Chart berikutnya digunakan untuk menunjukkan hubungan antara dua variabel.

Judul

Attendance vs GPA

Subtitle
Relationship between attendance and academic performance

Gunakan:

Scatter Plot

GPA
4.0 |                 •
3.5 |          •  •  •   •
3.0 |      • •  •
2.5 |   • •
2.0 | •
    └──────────────────────
       60  70  80  90 100
             Attendance

Hover:

Student
Muhammad Ihsan

Attendance
94%

GPA
3.72

Ini jauh lebih berguna daripada sekadar menampilkan angka attendance.

8. GPA by Major

Sebelah kanan:

GPA by Major

Gunakan Horizontal Bar Chart.

Informatics          ███████████  3.51

Information System   ██████████   3.42

Computer Science     █████████     3.38

Management            ████████     3.21

Kenapa horizontal?

Karena nama jurusan bisa panjang.

9. Academic Insights

Ini salah satu bagian yang membuat aplikasi terasa seperti Data Science platform, bukan dashboard CRUD.

Judul:

Academic Insights

Subtitle:

Key patterns identified from the current dataset

Contoh:

┌─────────────────────────────────────────────────────────────┐
│ Attendance has a moderate positive relationship with GPA.   │
│                                                             │
│ Students with attendance above 85% have an average GPA of   │
│ 3.51, compared with 2.94 for students below 75%.            │
└─────────────────────────────────────────────────────────────┘

Insight kedua:

GPA has increased by 4.8% compared with the previous semester.

Insight ketiga:

86 students are currently classified as high or medium risk.
Penting

Insight harus dihasilkan dari data.

Bukan:

const insight = "GPA is increasing";

Tetapi sistem melakukan perhitungan kemudian menghasilkan insight berdasarkan hasil tersebut.

10. Students Requiring Attention

Bagian terakhir Dashboard.

Judul:

Students Requiring Attention

Di kanan:

View all →

Tabel sederhana:

Student	Major	GPA	Attendance	Change	Risk
Student A	Informatics	2.41	69%	-0.52	High
Student B	Informatics	2.74	73%	-0.31	High
Student C	SI	2.92	78%	-0.24	Medium
Student D	Informatics	3.01	81%	-0.18	Medium
Risk

Gunakan badge kecil:

HIGH
MEDIUM

Bukan card besar berwarna.

11. Mobile Dashboard

Di mobile layout berubah menjadi:

Dashboard

Overview...


┌──────────────┐ ┌──────────────┐
│ Total        │ │ Average GPA  │
│ 1,248        │ │ 3.42         │
└──────────────┘ └──────────────┘

┌──────────────┐ ┌──────────────┐
│ Attendance   │ │ At Risk      │
│ 87.4%        │ │ 86           │
└──────────────┘ └──────────────┘


┌──────────────────────────────┐
│ GPA Trend                    │
│                              │
│          Chart               │
│                              │
└──────────────────────────────┘


┌──────────────────────────────┐
│ Performance Distribution     │
│                              │
└──────────────────────────────┘


┌──────────────────────────────┐
│ Attendance vs GPA            │
│                              │
└──────────────────────────────┘

Semua chart menjadi 1 column.

12. Dark Mode

Dark mode tidak sekadar membalik warna.

Light
Page
#F7F7F5

Card
#FFFFFF

Border
#E5E5E3

Text
#171717
Dark
Page
#111111

Card
#181818

Border
#2A2A2A

Text
#F5F5F5

Chart juga mengikuti theme.

13. Animation

Karena project ingin modern, kita boleh menggunakan animation, tetapi subtle.

Contoh:

Page load

Content:

opacity: 0 → 1
transform: translateY(6px) → 0
KPI

Angka dapat menggunakan count-up animation:

0 → 1,248
Chart

Chart muncul dengan animasi ringan.

Hover

Card:

translateY(-1px)

Tidak perlu:

bouncing
glowing
particle
gradient animation
excessive motion
14. Dashboard Final Hierarchy

Urutannya menjadi:

Dashboard
│
├── Page Header
│
├── KPI
│   ├── Total Students
│   ├── Average GPA
│   ├── Attendance
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

Menurut saya ini sudah cukup kuat tanpa membuat dashboard terasa penuh atau berantakan.