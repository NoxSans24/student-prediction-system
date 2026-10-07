# `FRONTEND_DESIGN_SYSTEM.md`

Dokumen ini menjadi acuan visual dan interaksi untuk seluruh **Student Performance Analytics**. Design system mengikuti arah yang sudah ditetapkan: **neutral, modern, clean, data-focused, friendly**, menggunakan **DM Sans**, SVG icons, serta light/dark mode.

---

# 1. Design Direction

### Karakter visual

```text
Modern
Clean
Neutral
Minimal
Data-focused
Friendly
Professional but not formal
```

Yang **dihindari**:

```text
Neon
Excessive gradient
Glassmorphism berlebihan
Glow
Particle animation
Terlalu banyak warna
Card berlebihan
Shadow berat
UI yang terlalu formal
```

Tujuan utamanya:

> Data menjadi fokus utama, bukan dekorasi interface.

---

# 2. Typography

Font utama:

```text
DM Sans
```

Fallback:

```css
font-family:
    "DM Sans",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
```

## Type Scale

| Element       |    Size | Weight |
| ------------- | ------: | -----: |
| Page Title    |    28px |    600 |
| Section Title |    20px |    600 |
| Card Title    |    16px |    600 |
| Body          |    14px |    400 |
| Secondary     |    13px |    400 |
| Caption       |    12px |    400 |
| KPI Value     | 28–32px |    600 |
| Button        |    14px |    500 |
| Table         |    14px |    400 |

---

# 3. Typography Rules

Jangan menggunakan terlalu banyak ukuran font.

Contoh:

```text
Dashboard
Overview of your academic data

Average GPA
3.24

+0.15 from previous semester
```

Hierarki harus terlihat dari:

```text
Size
Weight
Color
Spacing
```

bukan dari penggunaan berbagai macam font.

---

# 4. Color System

## Light Theme

```css
--bg: #F7F7F5;
--surface: #FFFFFF;
--surface-secondary: #FAFAF9;

--border: #E5E5E3;

--text-primary: #171717;
--text-secondary: #737373;
--text-muted: #A3A3A3;

--accent: #262626;
--accent-hover: #404040;
```

---

## Dark Theme

```css
--bg: #111111;
--surface: #181818;
--surface-secondary: #1E1E1E;

--border: #2A2A2A;

--text-primary: #F5F5F5;
--text-secondary: #A3A3A3;
--text-muted: #737373;

--accent: #E5E5E5;
--accent-hover: #FFFFFF;
```

Dark mode bukan sekadar:

```css
filter: invert();
```

Melainkan menggunakan palette khusus.

---

# 5. Semantic Colors

Warna hanya digunakan ketika memiliki makna.

### Low Risk

```text
Muted Green
```

### Medium Risk

```text
Muted Amber
```

### High Risk

```text
Muted Red
```

Contoh:

```text
LOW
MEDIUM
HIGH
```

Tidak menggunakan warna status pada seluruh card.

---

# 6. Spacing System

Gunakan kelipatan:

```text
4px
8px
12px
16px
24px
32px
48px
```

Contoh:

```text
Page padding       32px
Section gap        24px
Card padding       20–24px
Element gap        12–16px
Icon-text gap      8px
```

Tujuannya agar layout terasa konsisten.

---

# 7. Border Radius

Gunakan radius moderat.

```text
Small       6px
Medium      8px
Large       12px
```

Contoh:

```css
--radius-sm: 6px;
--radius-md: 8px;
--radius-lg: 12px;
```

Hindari semua elemen menjadi bentuk pill.

---

# 8. Shadow

Shadow digunakan sangat sedikit.

Default:

```css
box-shadow: none;
```

Jika diperlukan:

```text
Subtle shadow
```

terutama untuk:

* dropdown,
* modal,
* floating element.

Card utama cukup menggunakan:

```text
background
+
border
```

---

# 9. Application Layout

Struktur utama:

```text
┌─────────────────────────────────────────────┐
│ Sidebar │ Topbar                            │
│         ├───────────────────────────────────┤
│         │                                   │
│         │ Main Content                      │
│         │                                   │
│         │                                   │
│         │                                   │
└─────────┴───────────────────────────────────┘
```

---

# 10. Sidebar

Desktop:

```text
Width: 240px
```

Struktur:

```text
┌────────────────────┐
│ Nox / SPA          │
│                    │
│ Overview           │
│   Dashboard        │
│   Students         │
│   Analytics        │
│                    │
│ Intelligence       │
│   Prediction       │
│   Risk Analysis    │
│                    │
│ Data               │
│   Dataset          │
│   Reports          │
│                    │
│ Settings           │
└────────────────────┘
```

---

# 11. Sidebar Active State

Active navigation tidak menggunakan gradient atau glow.

Gunakan:

```text
background
+
text contrast
+
subtle indicator
```

Contoh konsep:

```text
Dashboard
████████████
```

dengan indicator kecil di sisi kiri.

---

# 12. Sidebar Icon

Semua icon menggunakan **SVG**.

Tidak menggunakan:

```text
Unicode emoji
```

Contoh kategori:

```text
Dashboard      → grid/dashboard SVG
Students       → users SVG
Analytics      → chart SVG
Prediction     → trend/chart SVG
Risk           → warning/status SVG
Dataset        → database/file SVG
Reports        → document SVG
Settings       → settings SVG
```

Icon harus memiliki visual language yang konsisten.

---

# 13. Topbar

Topbar:

```text
┌───────────────────────────────────────────────┐
│ [☰] Search...               Theme Bell Profile│
└───────────────────────────────────────────────┘
```

Semua icon tetap SVG.

Komponen:

```text
Sidebar Toggle
Global Search
Theme Toggle
Notification
Profile
```

---

# 14. Global Search

Placeholder:

```text
Search students, major, reports...
```

Input tidak terlalu tinggi.

```text
Height: 40px
```

Visual:

```text
[ Search icon ] Search students, major, reports...
```

Search dapat berkembang menjadi global search, tetapi MVP tidak perlu membuat pencarian kompleks jika belum diperlukan.

---

# 15. Page Header

Contoh:

```text
Dashboard

Overview of your academic data

Last updated 7 Oct 2026
```

Struktur:

```text
Page title
Subtitle
Metadata / action
```

Untuk halaman yang membutuhkan action:

```text
Students                         [ Add Student ]
```

---

# 16. Button System

## Primary

Digunakan untuk action utama.

```text
+ Add Student
Upload Dataset
Generate Report
Predict GPA
```

Style:

```text
Dark neutral
```

Light:

```text
#262626
```

Dark:

```text
#E5E5E5
```

---

## Secondary

Untuk action pendukung:

```text
Export
Filter
Cancel
View Details
```

Gunakan:

```text
Surface
+
Border
```

---

## Danger

Untuk destructive action:

```text
Delete
Remove
```

Gunakan muted red secara terbatas.

---

# 17. Button Rules

Button tidak boleh:

```text
terlalu besar
terlalu bulat
menggunakan gradient
menggunakan glow
```

Default:

```text
Height: 40px
Padding: 12px 16px
Radius: 8px
```

---

# 18. Icon Button

Untuk action kecil:

```text
[ SVG ]
```

Contoh:

```text
Edit
Delete
More
Refresh
Download
```

Harus memiliki tooltip atau accessible label.

---

# 19. KPI Card

Dashboard menggunakan empat KPI utama:

```text
Total Students
Average GPA
Average Attendance
At Risk Students
```

Struktur:

```text
┌──────────────────────────────┐
│ Total Students               │
│                              │
│ 120                          │
│ +8 from previous semester    │
└──────────────────────────────┘
```

KPI card tidak perlu icon besar atau dekorasi berlebihan.

---

# 20. KPI Card Hierarchy

```text
Label
   ↓
Value
   ↓
Change
```

Contoh:

```text
Average GPA

3.24

+0.15 from previous semester
```

Value menjadi elemen paling menonjol.

---

# 21. Chart Container

Chart menggunakan container sederhana:

```text
┌───────────────────────────────────────┐
│ GPA Trend                             │
│ Average GPA across semesters          │
│                                       │
│           chart                       │
│                                       │
└───────────────────────────────────────┘
```

Header:

```text
Title
Description / filter
Optional action
```

Chart tidak diberi dekorasi tambahan.

---

# 22. Chart Style

Chart harus:

```text
Clean
Readable
Low visual noise
Responsive
```

Hindari:

```text
3D chart
Excessive grid
Neon colors
Heavy gradients
Decorative chart backgrounds
```

---

# 23. Dashboard Grid

Desktop:

```text
KPI

[ KPI ][ KPI ][ KPI ][ KPI ]

Main Analytics

[ GPA Trend              ][ Performance Distribution ]

Secondary Analytics

[ Attendance vs GPA      ][ GPA by Major ]

Insights

[ Academic Insights ]

Attention

[ Students Requiring Attention ]
```

---

# 24. Analytics Page

Struktur:

```text
Analytics
Academic performance analysis

[ Filters ]

[ GPA Distribution       ]
[ GPA Trend              ]

[ GPA by Major           ]
[ Attendance vs GPA      ]

[ Study Hours vs GPA     ]
[ Assignment vs GPA      ]

[ Midterm vs GPA         ]
[ Final vs GPA           ]

[ Correlation Heatmap    ]
```

Pada desktop menggunakan dua kolom jika ruang memungkinkan.

---

# 25. Filter Bar

Filter:

```text
Major
Semester
GPA
Attendance
Risk
```

Visual:

```text
[ Major ▼ ]
[ Semester ▼ ]
[ GPA      ]
[ Risk ▼  ]
[ Apply ]
```

Jangan membuat filter terlihat seperti dashboard card.

---

# 26. Table System

Table digunakan untuk:

* Students
* Students Requiring Attention
* Risk Analysis
* Prediction History
* Dataset
* Reports

Contoh:

```text
┌──────────────────────────────────────────────┐
│ Student     Major      GPA    Attend.  Risk │
├──────────────────────────────────────────────┤
│ Muhammad    Informatics 3.4    89%     Low  │
│ Andi        Informatics 2.7    71%     Med  │
└──────────────────────────────────────────────┘
```

---

# 27. Table Rules

Header:

```text
12–13px
medium
secondary text
```

Body:

```text
14px
```

Gunakan border horizontal ringan.

Hindari:

```text
border setiap cell
warna berbeda setiap row
gradient row
```

---

# 28. Table Mobile

Pada layar kecil jangan memaksa seluruh kolom masuk.

Pilihan:

```text
Horizontal scroll
```

atau:

```text
Student Card
```

Untuk data yang banyak, horizontal scroll lebih cocok karena mempertahankan informasi tabel.

---

# 29. Status Badge

Contoh:

```text
LOW
MEDIUM
HIGH
```

Badge:

```text
font-size: 12px
padding: 4px 8px
border-radius: 6px
```

Gunakan semantic color secara halus.

---

# 30. Input

Default:

```text
Height: 40px
Border: 1px solid
Radius: 8px
Padding: 0 12px
```

Focus:

```text
border
+
subtle focus ring
```

Tidak menggunakan glow.

---

# 31. Select

Select harus konsisten dengan input.

```text
[ Informatics                ▼ ]
```

Digunakan pada:

* major
* semester
* risk
* report type
* model selection jika diperlukan.

---

# 32. Modal

Modal digunakan untuk:

```text
Delete confirmation
Cleaning confirmation
Training confirmation
Important action
```

Contoh:

```text
┌───────────────────────────────────┐
│ Delete Student                    │
│                                   │
│ Are you sure you want to delete   │
│ this student?                     │
│                                   │
│ [ Cancel ]        [ Delete ]      │
└───────────────────────────────────┘
```

Tidak menggunakan modal untuk informasi sederhana yang bisa ditampilkan inline.

---

# 33. Toast

Toast digunakan untuk feedback singkat.

Contoh:

```text
Student created successfully.
```

atau:

```text
Dataset cleaning applied successfully.
```

Posisi:

```text
Top-right
```

Toast tidak boleh menutupi konten penting.

---

# 34. Empty State

Jika belum ada data:

```text
No academic data available.

Upload or add data to start analyzing performance.
```

Tetap sederhana.

Jangan membuat empty state terlalu ilustratif.

---

# 35. Loading State

Gunakan:

```text
Skeleton
```

atau loading indicator sederhana.

Contoh:

```text
┌──────────────────────┐
│ █████████            │
│ █████████████        │
│ ██████               │
└──────────────────────┘
```

Hindari spinner besar di tengah halaman untuk setiap request kecil.

---

# 36. Error State

Contoh:

```text
Unable to load analytics.

Please try again.
```

Button:

```text
[ Retry ]
```

Error harus menjelaskan kondisi tanpa membocorkan detail teknis internal.

---

# 37. Student Profile Layout

```text
Student Profile

┌─────────────────────────────────────────┐
│ Student Information                     │
│ Name / ID / Major / Semester            │
└─────────────────────────────────────────┘

┌─────────────┐ ┌─────────────┐
│ GPA         │ │ Attendance  │
│ 3.42        │ │ 89%         │
└─────────────┘ └─────────────┘

┌─────────────────────────────────────────┐
│ GPA History                             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Performance Factors                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Risk Assessment                         │
└─────────────────────────────────────────┘
```

---

# 38. Prediction Page

Layout:

```text
Prediction

Predict student GPA based on academic factors.

┌──────────────────────┐
│ Prediction Form      │
│                      │
│ Semester             │
│ Attendance           │
│ Assignment           │
│ Midterm              │
│ Final                │
│ Study Hours          │
│                      │
│ [ Predict GPA ]      │
└──────────────────────┘
```

Setelah berhasil:

```text
┌─────────────────────────────┐
│ Predicted GPA               │
│                             │
│ 3.41                        │
│ Good                        │
│                             │
│ Random Forest               │
│ MAE / RMSE / R²             │
└─────────────────────────────┘
```

---

# 39. Risk Page

Struktur:

```text
Risk Analysis

[ Low ] [ Medium ] [ High ]

Risk Distribution

[ Chart ]

Students Requiring Attention

[ Table ]

Early Warnings

[ List ]
```

High risk harus mudah ditemukan tetapi tidak memenuhi seluruh interface dengan warna merah.

---

# 40. Dataset Page

Struktur:

```text
Dataset

[ Upload Dataset ]

Dataset Overview

Rows
Columns
Missing Values
Duplicates

Dataset Table

Cleaning Status

Cleaning Preview
```

Flow UI:

```text
Upload
 ↓
Preview
 ↓
Validation
 ↓
Cleaning Preview
 ↓
Confirm
 ↓
Processed
```

---

# 41. Reports Page

```text
Reports

┌───────────────────────────┐
│ Overall Performance       │
│ Academic overview         │
│                           │
│ [ PDF ] [ Excel ] [ CSV ] │
└───────────────────────────┘

┌───────────────────────────┐
│ Student Report            │
│                           │
│ [ Generate ]              │
└───────────────────────────┘
```

Report type:

```text
Overall Performance
Student Report
Risk Report
ML Report
```

---

# 42. Settings Page

Settings dibuat sederhana.

```text
Settings

Appearance
├── Theme
└── Interface preferences

Account
├── Username
├── Email
└── Role

Security
└── Change Password
```

System settings hanya tersedia untuk Admin jika memang diperlukan.

---

# 43. Light / Dark Mode

Theme toggle berada di topbar.

Konsep:

```text
Light
☼
```

dan

```text
Dark
☾
```

Namun icon tetap **SVG**, bukan Unicode.

Theme disimpan pada browser sehingga preference tetap ada ketika user kembali membuka aplikasi.

---

# 44. Animation System

Animation harus subtle.

### Page Load

```text
opacity: 0 → 1
transform: translateY(4px) → 0
```

### KPI

Count-up sederhana.

### Chart

Fade/scale ringan ketika pertama kali muncul.

### Hover

```text
translateY(-1px)
```

Tidak menggunakan:

```text
bounce
glow
particle
large scale
```

---

# 45. Motion Duration

```css
--duration-fast: 150ms;
--duration-normal: 200ms;
--duration-slow: 300ms;
```

Gunakan easing sederhana.

Animasi tidak boleh mengganggu penggunaan dashboard.

---

# 46. Accessibility

Minimal:

```text
Semantic HTML
Keyboard navigation
Visible focus
Accessible labels
Button labels
Sufficient contrast
```

Icon-only button harus mempunyai:

```html
aria-label="Toggle theme"
```

bukan hanya SVG tanpa informasi.

---

# 47. Responsive Breakpoints

Design awal:

```text
Desktop:
≥ 1200px

Tablet:
768px – 1199px

Mobile:
< 768px
```

Layout harus mengikuti ruang yang tersedia, bukan bergantung pada device tertentu.

---

# 48. Mobile Navigation

Desktop:

```text
Sidebar selalu terlihat
```

Mobile:

```text
Topbar
   ↓
Menu button
   ↓
Off-canvas sidebar
```

Sidebar ditutup setelah user memilih navigation.

---

# 49. Mobile KPI

Desktop:

```text
[ KPI ][ KPI ][ KPI ][ KPI ]
```

Mobile:

```text
[ KPI ][ KPI ]
[ KPI ][ KPI ]
```

---

# 50. Mobile Charts

Desktop:

```text
[ Chart ][ Chart ]
```

Mobile:

```text
[ Chart ]

[ Chart ]
```

Chart harus memiliki minimum height yang tetap nyaman dibaca.

---

# 51. Component Naming

Gunakan nama class yang jelas.

Contoh:

```text
.app-shell
.sidebar
.sidebar-nav
.topbar
.page-header
.kpi-grid
.kpi-card
.chart-card
.table-card
.status-badge
.filter-bar
.modal
.toast
.empty-state
.loading-state
```

Hindari nama seperti:

```text
.box1
.card2
.blue-container
```

---

# 52. CSS Architecture

```text
static/css/
│
├── base.css
├── layout.css
├── components.css
├── utilities.css
│
└── pages/
    ├── dashboard.css
    ├── students.css
    ├── analytics.css
    ├── prediction.css
    ├── risk.css
    ├── dataset.css
    └── reports.css
```

### `base.css`

Berisi:

```text
Reset
Variables
Typography
Theme
```

### `layout.css`

Berisi:

```text
Sidebar
Topbar
Main content
Grid
Responsive
```

### `components.css`

Berisi:

```text
Button
Card
Input
Table
Badge
Modal
Toast
```

### Page CSS

Berisi style khusus halaman.

---

# 53. JavaScript Architecture

```text
static/js/
│
├── app.js
├── theme.js
├── sidebar.js
├── charts.js
│
└── pages/
    ├── dashboard.js
    ├── students.js
    ├── analytics.js
    ├── prediction.js
    ├── risk.js
    ├── dataset.js
    └── reports.js
```

Prinsip:

```text
app.js
→ global functionality

theme.js
→ theme

sidebar.js
→ navigation

dashboard.js
→ dashboard-specific logic
```

---

# 54. Chart Data Flow Frontend

```text
dashboard.js
      ↓
fetch("/api/dashboard")
      ↓
JSON
      ↓
Validate response
      ↓
Render KPI
      ↓
Render Charts
      ↓
Render Insights
```

Frontend tidak melakukan query database.

---

# 55. Design Token Summary

```css id="c8b9wm"
:root {
    --bg: #F7F7F5;
    --surface: #FFFFFF;
    --surface-secondary: #FAFAF9;

    --border: #E5E5E3;

    --text-primary: #171717;
    --text-secondary: #737373;
    --text-muted: #A3A3A3;

    --accent: #262626;
    --accent-hover: #404040;

    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;

    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-5: 24px;
    --space-6: 32px;
    --space-7: 48px;

    --duration-fast: 150ms;
    --duration-normal: 200ms;
    --duration-slow: 300ms;
}
```

Dark theme mengganti token warna tanpa mengubah struktur component.

---

# 56. Visual Principle Utama

Setiap halaman harus menjawab:

> **Apa informasi paling penting yang perlu dilihat user sekarang?**

Contoh Dashboard:

```text
1. Kondisi performa
2. Perubahan performa
3. Mahasiswa yang perlu perhatian
```

Contoh Analytics:

```text
1. Pola
2. Distribusi
3. Relationship
```

Contoh Prediction:

```text
1. Input
2. Predicted GPA
3. Model information
```

Contoh Risk:

```text
1. Risk distribution
2. High-risk students
3. Risk factors
```

---

# 57. Final UI Philosophy

Student Performance Analytics **bukan** aplikasi yang dibuat untuk terlihat penuh fitur.

Prioritasnya:

```text
Data
 ↓
Clarity
 ↓
Insight
 ↓
Action
```

Bukan:

```text
Decoration
 ↓
Animation
 ↓
Color
 ↓
Data
```

Dengan demikian UI tetap terlihat modern tanpa menjadi ramai.

