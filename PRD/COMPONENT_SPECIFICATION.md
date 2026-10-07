# `COMPONENT_SPECIFICATION.md`

Dokumen ini mendefinisikan **komponen UI reusable** untuk Student Performance Analytics. Tujuannya agar kita tidak membuat elemen yang sama berulang-ulang di setiap halaman.

Prinsipnya:

```text
Page
 ↓
Section
 ↓
Reusable Component
 ↓
Data
```

---

# 1. Component Architecture

Komponen utama:

```text
Global
├── App Shell
├── Sidebar
├── Topbar
├── Page Header
└── Theme Toggle

Data Display
├── KPI Card
├── Chart Card
├── Data Table
├── Status Badge
├── Metric
└── Insight Card

Form
├── Input
├── Select
├── Search Input
├── Filter Bar
└── Form Group

Feedback
├── Toast
├── Modal
├── Loading State
├── Empty State
└── Error State

Specialized
├── Student Card
├── Risk Card
├── Prediction Result
├── Dataset Summary
└── Report Card
```

---

# 2. App Shell

## Purpose

Menjadi wrapper utama seluruh halaman setelah login.

Struktur:

```html
<div class="app-shell">

    <aside class="sidebar">
        ...
    </aside>

    <div class="app-main">

        <header class="topbar">
            ...
        </header>

        <main class="page-content">
            ...
        </main>

    </div>

</div>
```

---

# 3. Sidebar

## Struktur

```text
Sidebar
├── Brand
├── Navigation
│   ├── Overview
│   ├── Intelligence
│   └── Data
└── Settings
```

## Data

Contoh struktur JavaScript:

```javascript
const navigation = [
    {
        group: "Overview",
        items: [
            {
                label: "Dashboard",
                href: "/dashboard",
                icon: "dashboard"
            },
            {
                label: "Students",
                href: "/students",
                icon: "students"
            },
            {
                label: "Analytics",
                href: "/analytics",
                icon: "analytics"
            }
        ]
    }
];
```

---

# 4. Sidebar Behavior

Desktop:

```text
Expanded
240px
```

Tablet:

```text
Collapsed
```

Mobile:

```text
Off-canvas
```

Active menu ditentukan berdasarkan current route.

---

# 5. Sidebar Role Behavior

Navigation dapat disesuaikan dengan role.

Namun:

> Menyembunyikan tombol atau menu bukan pengganti authorization backend.

Contoh:

```text
Admin
→ Dataset Upload terlihat

Analyst
→ Dataset Upload tidak tersedia
```

Tetapi endpoint tetap harus dilindungi backend.

---

# 6. Topbar

Struktur:

```text
Topbar
├── Sidebar Toggle
├── Global Search
└── Actions
    ├── Theme Toggle
    ├── Notification
    └── Profile
```

Desktop:

```text
[ Menu ] [ Search........................ ]

                              [Theme] [Bell] [Profile]
```

Mobile:

```text
[Menu]                     [Theme] [Profile]
```

Search dapat disembunyikan atau diperkecil pada mobile.

---

# 7. Page Header

Props/data:

```text
title
subtitle
metadata
actions
```

Contoh:

```html
<header class="page-header">

    <div>
        <h1>Dashboard</h1>
        <p>Overview of your academic data</p>
    </div>

    <div class="page-header__meta">
        Last updated: ...
    </div>

</header>
```

Untuk Students:

```text
Students
Manage student academic profiles

                         [ + Add Student ]
```

---

# 8. Button Component

Variants:

```text
primary
secondary
danger
ghost
icon
```

Contoh:

```html
<button class="btn btn-primary">
    Add Student
</button>
```

Icon button:

```html
<button
    class="btn-icon"
    aria-label="Toggle theme">
    ...
</button>
```

---

# 9. Button States

Setiap button harus mendukung:

```text
Default
Hover
Focus
Active
Disabled
Loading
```

Loading:

```text
[ Saving... ]
```

Button tidak boleh dapat ditekan berkali-kali ketika request sedang diproses.

---

# 10. KPI Card

## Data

```javascript
{
    label: "Average GPA",
    value: "3.24",
    change: "+0.15",
    changeLabel: "from previous semester",
    trend: "positive"
}
```

Struktur:

```text
┌────────────────────────────┐
│ Average GPA                │
│                            │
│ 3.24                       │
│ +0.15 from previous        │
└────────────────────────────┘
```

---

# 11. KPI Card Variants

KPI:

```text
Total Students
Average GPA
Average Attendance
At Risk Students
```

Tidak perlu membuat variant berdasarkan warna.

Perbedaan utama berasal dari:

```text
Data
Label
Trend
```

---

# 12. Metric Component

Metric adalah versi kecil dari KPI.

Contoh Student Detail:

```text
GPA
3.42
```

atau:

```text
Attendance
89%
```

Struktur:

```html
<div class="metric">
    <span class="metric__label">GPA</span>
    <strong class="metric__value">3.42</strong>
</div>
```

---

# 13. Chart Card

Reusable untuk seluruh chart.

Props:

```text
title
description
chart
actions
loading
empty
error
```

Struktur:

```text
┌──────────────────────────────────────┐
│ GPA Trend                     [ ... ]│
│ Average GPA across semesters         │
│                                      │
│             CHART                    │
│                                      │
└──────────────────────────────────────┘
```

---

# 14. Chart Card States

### Loading

Chart skeleton.

### Empty

```text
No data available for this chart.
```

### Error

```text
Unable to load chart data.

[ Retry ]
```

### Success

Chart normal.

---

# 15. Chart Types

Komponen chart harus mendukung:

```text
Line
Bar
Horizontal Bar
Donut
Scatter
Heatmap
```

Mapping:

| Chart              | Component      |
| ------------------ | -------------- |
| GPA Trend          | Line           |
| GPA Distribution   | Donut          |
| GPA by Major       | Horizontal Bar |
| Attendance vs GPA  | Scatter        |
| Study Hours vs GPA | Scatter        |
| Assignment vs GPA  | Scatter        |
| Midterm vs GPA     | Scatter        |
| Final vs GPA       | Scatter        |
| Correlation        | Heatmap        |

---

# 16. Data Table

Reusable untuk:

```text
Students
Risk
Prediction History
Dataset
Reports
Attention List
```

Props:

```text
columns
rows
pagination
sorting
actions
loading
empty
```

---

# 17. Table Column Definition

Contoh:

```javascript
const columns = [
    {
        key: "name",
        label: "Student"
    },
    {
        key: "major",
        label: "Major"
    },
    {
        key: "gpa",
        label: "GPA"
    },
    {
        key: "attendance",
        label: "Attendance"
    },
    {
        key: "risk",
        label: "Risk"
    }
];
```

Dengan pendekatan ini table tidak perlu dibuat ulang untuk setiap halaman.

---

# 18. Table Actions

Action dapat berupa:

```text
View
Edit
Delete
More
```

Permission menentukan apakah action ditampilkan.

Contoh:

```text
Admin:
View | Edit | Delete

Analyst:
View
```

---

# 19. Pagination

Pagination:

```text
Previous
1
2
3
...
Next
```

Informasi:

```text
Showing 1–10 of 120 students
```

API:

```text
?page=1&limit=10
```

Pagination harus berasal dari backend, bukan mengambil seluruh data kemudian memotongnya di browser.

---

# 20. Status Badge

Component:

```html
<span class="status-badge status-high">
    HIGH
</span>
```

Variants:

```text
low
medium
high
success
warning
error
neutral
```

Namun semantic colors digunakan secukupnya.

---

# 21. Risk Badge

Khusus risk:

```text
LOW
MEDIUM
HIGH
```

Risk badge tidak boleh menjadi satu-satunya informasi risk.

Pada halaman detail, tetap tampilkan:

```text
Risk Level
Risk Score
Main Factors
Early Warnings
```

---

# 22. Search Input

Reusable untuk:

```text
Students
Dataset
Reports
Prediction History
```

Struktur:

```text
┌────────────────────────────────────┐
│ [search] Search students...        │
└────────────────────────────────────┘
```

Props:

```text
placeholder
value
onInput
onSubmit
```

---

# 23. Filter Bar

Struktur:

```text
Filter Bar
├── Major
├── Semester
├── GPA
├── Attendance
├── Risk
└── Apply / Reset
```

Tidak semua halaman harus menampilkan seluruh filter.

---

# 24. Filter State

Filter dapat disimpan sebagai query parameter:

```text
/analytics?major=Informatics&semester=4
```

Keuntungannya:

* URL dapat dibagikan.
* Refresh tidak menghilangkan filter.
* Browser back/forward lebih konsisten.

---

# 25. Input Component

Variants:

```text
text
number
password
date
file
```

Struktur:

```html
<div class="form-group">

    <label for="student-name">
        Student Name
    </label>

    <input
        id="student-name"
        type="text"
        name="name">

    <span class="form-error">
        ...
    </span>

</div>
```

---

# 26. Input States

```text
Default
Focus
Filled
Disabled
Error
Success
```

Error:

```text
Attendance must be between 0 and 100.
```

Validasi harus dilakukan frontend **dan backend**.

---

# 27. Select Component

Contoh:

```text
Major

[ Informatics              ▼ ]
```

Digunakan untuk:

```text
Major
Semester
Risk
Report Type
```

---

# 28. File Upload Component

Digunakan Dataset.

Struktur:

```text
┌───────────────────────────────────┐
│                                   │
│     Upload academic dataset       │
│                                   │
│     CSV files only                │
│                                   │
│     [ Choose File ]               │
│                                   │
└───────────────────────────────────┘
```

Setelah file dipilih:

```text
students.csv
1.2 MB

[ Remove ] [ Upload ]
```

---

# 29. Modal Component

Props:

```text
title
description
content
confirmLabel
cancelLabel
variant
```

Contoh:

```text
Delete Student?

This action cannot be undone.

[ Cancel ] [ Delete ]
```

Variants:

```text
default
danger
```

---

# 30. Modal Accessibility

Ketika modal dibuka:

```text
Focus → modal
```

Ketika ditutup:

```text
Focus → element sebelumnya
```

Keyboard:

```text
Escape → close
Tab → stay inside modal
```

---

# 31. Toast Component

Variants:

```text
success
error
warning
info
```

Contoh:

```text
┌─────────────────────────────────┐
│ ✓ Student created successfully. │
└─────────────────────────────────┘
```

Icon tetap SVG.

---

# 32. Empty State

Props:

```text
title
description
action
```

Contoh Students:

```text
No students found.

Try changing your filters or add a new student.

[ Add Student ]
```

Dataset:

```text
No datasets available.

Upload a dataset to begin.

[ Upload Dataset ]
```

---

# 33. Loading State

Reusable skeleton:

```text
Skeleton Text
Skeleton Card
Skeleton Table
Skeleton Chart
```

Contoh KPI:

```text
┌──────────────────┐
│ █████████        │
│ █████            │
│ ████████         │
└──────────────────┘
```

---

# 34. Error State

Props:

```text
title
description
retry
```

Contoh:

```text
Unable to load student data.

Please try again.

[ Retry ]
```

Tidak menampilkan:

```text
SQL syntax error...
Traceback...
```

kepada user.

Detail teknis tetap masuk server logs.

---

# 35. Insight Card

Digunakan Dashboard.

Data:

```javascript
{
    type: "gpa_trend",
    priority: "medium",
    title: "GPA Trend",
    message: "Average GPA increased compared with the previous semester.",
    value: 3.25,
    change: 0.15
}
```

UI:

```text
┌─────────────────────────────────┐
│ GPA Trend                       │
│                                 │
│ Average GPA increased compared  │
│ with the previous semester.     │
│                                 │
│ 3.25       +0.15                │
└─────────────────────────────────┘
```

---

# 36. Insight Priority

```text
high
medium
low
```

Priority tidak harus berarti warna mencolok.

Prioritas dapat ditunjukkan dengan:

```text
position
icon
small semantic indicator
```

---

# 37. Student Card

Digunakan terutama pada mobile.

```text
┌─────────────────────────────────┐
│ Muhammad Ihsan Hanafi           │
│ 20240001 · Informatics          │
│                                 │
│ GPA       Attendance      Risk  │
│ 3.42      89%             LOW   │
│                                 │
│ [ View Details ]                │
└─────────────────────────────────┘
```

---

# 38. Risk Summary Card

Digunakan pada Risk Analysis.

```text
┌────────────────────┐
│ High Risk          │
│                    │
│ 15 students        │
│ 12.5% of students  │
└────────────────────┘
```

Tidak menggunakan background merah penuh.

---

# 39. Prediction Result Component

Props:

```text
predictedGPA
performanceCategory
modelName
metrics
```

Struktur:

```text
Prediction Result

3.41
Good

Model
RandomForestRegressor

MAE
0.18

RMSE
0.24

R²
0.82
```

---

# 40. Dataset Summary Component

```text
┌────────────┐ ┌────────────┐
│ Rows       │ │ Columns    │
│ 1,000      │ │ 10         │
└────────────┘ └────────────┘

┌────────────┐ ┌────────────┐
│ Missing    │ │ Duplicate  │
│ 12         │ │ 4          │
└────────────┘ └────────────┘
```

Reusable pada:

* Dataset detail
* ML Report
* Dataset validation

---

# 41. Cleaning Summary Component

Menampilkan:

```text
Original Rows
Rows Removed
Missing Values Handled
Invalid Values
Outliers Flagged
Final Rows
```

Contoh:

```text
Original rows       1,000
Rows removed            8
Missing handled        12
Outliers flagged        8
Final rows             992
```

---

# 42. Report Card

Props:

```text
title
description
availableFormats
action
```

Contoh:

```text
Overall Performance

Academic performance overview.

[ PDF ] [ Excel ] [ CSV ]
```

---

# 43. Navigation Component

Link harus memiliki:

```text
SVG Icon
Label
Active State
Hover State
Focus State
```

Contoh:

```text
[SVG] Dashboard
[SVG] Students
[SVG] Analytics
```

Tidak:

```text
📊 Dashboard
👨‍🎓 Students
```

---

# 44. SVG Icon Rules

Semua icon:

```text
SVG
Consistent stroke
Consistent viewBox
Accessible
```

Direkomendasikan menggunakan satu icon library yang konsisten daripada mencampur banyak gaya.

Contoh struktur:

```text
static/icons/
├── dashboard.svg
├── students.svg
├── analytics.svg
├── prediction.svg
├── risk.svg
├── dataset.svg
├── reports.svg
└── settings.svg
```

---

# 45. Icon Sizing

Standard:

```text
16px
18px
20px
24px
```

Navigation:

```text
18–20px
```

Button:

```text
16–18px
```

Decorative icon:

```text
20–24px
```

Tidak menggunakan icon sangat besar hanya untuk memenuhi ruang kosong.

---

# 46. Card Component Rules

Card digunakan ketika:

> Sekelompok informasi memang perlu dikelompokkan.

Gunakan card untuk:

```text
KPI
Chart
Insight
Report
Prediction Result
Risk Summary
```

Jangan membuat:

```text
Card di dalam card di dalam card
```

secara berlebihan.

---

# 47. Section Component

Section reusable:

```html
<section class="section">

    <div class="section-header">
        <h2>Academic Insights</h2>
    </div>

    <div class="section-content">
        ...
    </div>

</section>
```

Tujuan utamanya menjaga spacing antar bagian.

---

# 48. Divider

Gunakan border tipis ketika perlu memisahkan informasi.

```css
border-top: 1px solid var(--border);
```

Jangan menggunakan divider pada setiap elemen.

---

# 49. Dropdown / Menu

Digunakan untuk:

```text
Table actions
Profile menu
Chart actions
```

Contoh:

```text
[ ... ]

View
Edit
Delete
```

Dropdown harus:

* memiliki focus state,
* dapat ditutup dengan Escape,
* tidak keluar viewport.

---

# 50. Tooltip

Digunakan hanya untuk informasi tambahan.

Contoh:

```text
[ icon ]
   ↓
"Export report"
```

Jangan menggunakan tooltip untuk informasi penting yang wajib diketahui user.

---

# 51. Component State Convention

Setiap component data-driven menggunakan pola:

```text
idle
loading
success
empty
error
```

Contoh:

```javascript
switch (state) {
    case "loading":
        renderSkeleton();
        break;

    case "empty":
        renderEmpty();
        break;

    case "error":
        renderError();
        break;

    default:
        renderData();
}
```

---

# 52. Component Data Principle

Component UI tidak boleh mengambil data database secara langsung.

Buruk:

```text
KPI Card
 ↓
MySQL
```

Benar:

```text
MySQL
 ↓
Service
 ↓
API
 ↓
Page JS
 ↓
KPI Card
```

---

# 53. Component Communication

Pola:

```text
API
 ↓
Page Controller
 ↓
Component
```

Contoh Dashboard:

```text
/api/dashboard
       ↓
dashboard.js
       ↓
├── renderKPI()
├── renderGPAChart()
├── renderDistribution()
├── renderInsights()
└── renderAttentionTable()
```

---

# 54. Reusability Rule

Jika sebuah UI muncul **minimal dua kali** dan struktur/behavior-nya sama, pertimbangkan menjadikannya component.

Contoh:

```text
KPI Card
Chart Card
Button
Table
Modal
Badge
```

Tetapi jangan membuat component untuk setiap `<div>` kecil.

---

# 55. Component File Strategy

Untuk Flask + HTML/CSS/JS, struktur dapat menggunakan:

```text
templates/
└── components/
    ├── sidebar.html
    ├── topbar.html
    ├── page_header.html
    ├── kpi_card.html
    ├── chart_card.html
    ├── status_badge.html
    ├── empty_state.html
    └── modal.html
```

Kemudian digunakan dengan Jinja:

```html
{% include "components/kpi_card.html" %}
```

---

# 56. CSS Component Strategy

```text
static/css/components.css
```

Berisi:

```text
.btn
.card
.kpi-card
.chart-card
.table
.status-badge
.input
.select
.modal
.toast
.empty-state
.loading-state
```

CSS halaman hanya mengatur layout khusus halaman.

---

# 57. JavaScript Component Strategy

Tidak semua component membutuhkan JavaScript.

### CSS/HTML only

```text
Button
Card
Badge
Input
Page Header
```

### JavaScript

```text
Sidebar
Theme Toggle
Modal
Toast
Table Pagination
Charts
Filter
File Upload
```

Ini menjaga aplikasi tetap sederhana.

---

# 58. Component Dependency

```text
App Shell
├── Sidebar
├── Topbar
└── Page

Page
├── Page Header
├── Section
└── Components

Data Components
├── KPI
├── Chart
├── Table
├── Badge
└── Insight
```

Tidak boleh terjadi dependency yang saling berputar.

---

# 59. Final Component Tree — Dashboard

```text
Dashboard
│
├── Page Header
│
├── KPI Grid
│   ├── KPI Card
│   ├── KPI Card
│   ├── KPI Card
│   └── KPI Card
│
├── Main Analytics
│   ├── Chart Card
│   │   └── GPA Trend
│   │
│   └── Chart Card
│       └── Performance Distribution
│
├── Secondary Analytics
│   ├── Chart Card
│   │   └── Attendance vs GPA
│   │
│   └── Chart Card
│       └── GPA by Major
│
├── Academic Insights
│   └── Insight Card
│
└── Students Requiring Attention
    └── Data Table
```

---

# 60. Final Component Tree — Student Detail

```text
Student Detail
│
├── Page Header
│
├── Student Information
│
├── Performance Metrics
│   ├── Metric
│   ├── Metric
│   └── Risk Badge
│
├── GPA History
│   └── Chart Card
│
├── Performance Factors
│   └── Metric / Data List
│
└── Risk Assessment
    ├── Risk Summary
    ├── Risk Factors
    └── Early Warnings
```

---

# 61. Final Component Tree — Prediction

```text
Prediction
│
├── Page Header
│
├── Prediction Form
│   ├── Input
│   ├── Input
│   ├── Input
│   ├── Input
│   ├── Input
│   └── Button
│
├── Prediction Result
│   ├── Predicted GPA
│   ├── Performance Badge
│   └── Model Metrics
│
└── Prediction History
    └── Data Table
```

---

# 62. Final Component Tree — Dataset

```text
Dataset
│
├── Page Header
│
├── Dataset Summary
│
├── Upload Component
│
├── Dataset Preview
│   └── Data Table
│
├── Validation Results
│
└── Cleaning Preview
    ├── Cleaning Summary
    └── Confirmation Modal
```

---

# 63. Final Component Tree — Risk

```text
Risk Analysis
│
├── Page Header
│
├── Risk Summary
│   ├── Low
│   ├── Medium
│   └── High
│
├── Risk Distribution
│   └── Chart Card
│
├── Filters
│
├── Students Requiring Attention
│   └── Data Table
│
└── Early Warnings
```

---

# 64. Component Design Principle

Seluruh UI harus mengikuti prinsip:

```text
Consistent
Reusable
Predictable
Accessible
Responsive
Data-first
```

Bukan:

```text
Every page has a different style.
```

---

# 65. Final Visual Hierarchy

Prioritas visual:

```text
1. Primary information
2. Current state
3. Change / trend
4. Supporting information
5. Actions
6. Metadata
```

Contoh KPI:

```text
3.24       ← Primary
+0.15      ← Change
Average GPA ← Label
```

---

# 66. Final Component Checklist

Sebelum sebuah component dianggap selesai:

```text
□ Light mode
□ Dark mode
□ Responsive
□ Hover state
□ Focus state
□ Disabled state jika relevan
□ Loading state jika data-driven
□ Empty state jika data-driven
□ Error state jika data-driven
□ SVG icon
□ Accessible label
□ Tidak menggunakan hardcoded business data
```

---

# 67. Component Architecture Final

```text
                    APPLICATION
                         │
                ┌────────┴────────┐
                │                 │
             Layout            Pages
                │                 │
       ┌────────┼───────┐         │
       │        │       │         │
    Sidebar   Topbar   Main        │
                                  │
                         ┌────────┴────────┐
                         │                 │
                    Components         Data
                         │                 │
              ┌──────────┼──────────┐      │
              │          │          │      │
            Cards      Tables     Forms    API
              │          │          │      │
              └──────────┴──────────┴──────┘
```

---

