# `FRONTEND_IMPLEMENTATION_SPEC.md`

Dokumen ini menerjemahkan **Frontend Design System**, **Page Specification**, **Component Specification**, dan **API Specification** menjadi struktur frontend konkret untuk Flask.

Targetnya:

```text id="5x1xqk"
Modern
Clean
Neutral
Data-focused
Friendly
Responsive
Light / Dark Mode
DM Sans
SVG Icons
Subtle Animation
```

Frontend tidak menjadi tempat business logic utama.

---

# 1. Frontend Architecture

Arsitektur:

```text id="6v3p1w"
Browser
   ↓
HTML / Jinja
   ↓
CSS
   ↓
JavaScript
   ↓
Flask API
   ↓
Services
```

Struktur:

```text id="j6v5f8"
templates/
├── base.html
├── components/
├── auth/
├── dashboard/
├── students/
├── analytics/
├── prediction/
├── risk/
├── dataset/
├── reports/
├── settings/
└── errors/

static/
├── css/
├── js/
└── icons/
```

---

# 2. Frontend Technology

Gunakan:

```text id="0dny0b"
HTML5
CSS3
Vanilla JavaScript
Jinja2
Chart.js
SVG
DM Sans
```

React tidak diperlukan untuk MVP.

Alasannya:

* project berbasis Flask,
* halaman tidak membutuhkan SPA penuh,
* lebih sederhana untuk mahasiswa,
* dependency lebih sedikit,
* struktur tetap mudah dipahami.

---

# 3. Template Architecture

`base.html` menjadi template utama.

```html id="l0v0bc"
<!DOCTYPE html>
<html>
<head>
    ...
</head>

<body>

    {% include "components/sidebar.html" %}

    <div class="app-main">

        {% include "components/topbar.html" %}

        <main class="page-content">
            {% block content %}
            {% endblock %}
        </main>

    </div>

    {% block scripts %}
    {% endblock %}

</body>
</html>
```

---

# 4. Template Components

Struktur:

```text id="p9l2oz"
templates/components/
├── sidebar.html
├── topbar.html
├── page_header.html
├── kpi_card.html
├── chart_card.html
├── status_badge.html
├── filter_bar.html
├── empty_state.html
├── error_state.html
├── loading_state.html
├── modal.html
├── toast.html
└── pagination.html
```

Komponen digunakan ulang di berbagai halaman.

---

# 5. Page Templates

```text id="jce0qi"
templates/
├── auth/
│   └── login.html
│
├── dashboard/
│   └── index.html
│
├── students/
│   ├── index.html
│   └── detail.html
│
├── analytics/
│   └── index.html
│
├── prediction/
│   └── index.html
│
├── risk/
│   └── index.html
│
├── dataset/
│   └── index.html
│
├── reports/
│   └── index.html
│
├── settings/
│   └── index.html
│
└── errors/
    ├── 403.html
    ├── 404.html
    └── 500.html
```

---

# 6. CSS Architecture

```text id="4ud1wm"
static/css/
├── base.css
├── layout.css
├── components.css
├── utilities.css
└── pages/
    ├── login.css
    ├── dashboard.css
    ├── students.css
    ├── analytics.css
    ├── prediction.css
    ├── risk.css
    ├── dataset.css
    ├── reports.css
    └── settings.css
```

---

# 7. `base.css`

Berisi:

```text id="x9b20h"
CSS reset
Typography
CSS variables
Theme variables
Body
Global elements
```

Contoh:

```css id="9sk2vl"
:root {
    --font-family: "DM Sans", sans-serif;

    --bg: #F7F7F5;
    --surface: #FFFFFF;
    --border: #E5E5E3;

    --text-primary: #171717;
    --text-secondary: #737373;
    --text-muted: #A3A3A3;

    --accent: #262626;
}
```

---

# 8. Dark Theme

Gunakan class:

```html id="e6n3cr"
<html data-theme="dark">
```

Variables:

```css id="r72gk5"
[data-theme="dark"] {
    --bg: #111111;
    --surface: #181818;
    --border: #2A2A2A;

    --text-primary: #F5F5F5;
    --text-secondary: #A3A3A3;
    --text-muted: #737373;

    --accent: #E5E5E5;
}
```

Jangan melakukan:

```css id="qu31wq"
filter: invert(...);
```

untuk membuat dark mode.

---

# 9. Theme Persistence

Theme disimpan di:

```text id="h9f4k8"
localStorage
```

Key:

```text id="oqif0j"
theme
```

Contoh:

```javascript id="5zq2jq"
localStorage.setItem("theme", "dark");
```

Ketika browser dibuka kembali, theme sebelumnya digunakan.

---

# 10. Theme Initialization

Theme harus diterapkan sedini mungkin untuk menghindari flash:

```text id="1e6grj"
Browser
 ↓
Read localStorage
 ↓
Set data-theme
 ↓
Render page
```

Bukan:

```text id="t1y0r6"
Render light
 ↓
JavaScript
 ↓
Switch dark
```

karena dapat menyebabkan flicker.

---

# 11. `layout.css`

Menangani:

```text id="8y9k4a"
App shell
Sidebar
Topbar
Main content
Grid
Responsive layout
```

Desktop:

```text id="lh4k8d"
┌─────────────┬──────────────────────────┐
│             │ Topbar                   │
│  Sidebar    ├──────────────────────────┤
│             │                          │
│             │ Main Content             │
│             │                          │
└─────────────┴──────────────────────────┘
```

---

# 12. Desktop Layout

Sidebar:

```text id="x6j3ef"
240px
```

Main:

```css id="wml8oj"
.app-main {
    margin-left: 240px;
}
```

Content memiliki max-width yang wajar agar dashboard tidak terlalu melebar.

---

# 13. Tablet Layout

Breakpoint:

```text id="t3jyl4"
768px – 1199px
```

Sidebar dapat menjadi collapsed.

Main content mengambil ruang lebih besar.

---

# 14. Mobile Layout

Breakpoint:

```text id="y3p5iz"
< 768px
```

Sidebar:

```text id="a4x9qn"
off-canvas
```

Main:

```text id="uwg56j"
margin-left: 0
```

Topbar tetap accessible.

---

# 15. Global Spacing

Gunakan:

```text id="z1d5ve"
4px
8px
12px
16px
24px
32px
48px
```

Contoh:

```css id="h0j7ef"
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 24px;
--space-6: 32px;
--space-7: 48px;
```

---

# 16. Typography

Font:

```text id="y1w1v6"
DM Sans
```

Hierarchy:

| Element       |    Size | Weight |
| ------------- | ------: | -----: |
| Page title    |    28px |    600 |
| Section title |    20px |    600 |
| Card title    |    16px |    600 |
| Body          |    14px |    400 |
| Secondary     |    13px |    400 |
| Caption       |    12px |    400 |
| KPI           | 28–32px |    600 |
| Button        |    14px |    500 |

Tidak menggunakan typography yang terlalu formal.

---

# 17. Component CSS

`components.css` berisi:

```text id="p9iykv"
.btn
.btn-primary
.btn-secondary
.btn-danger
.btn-ghost
.btn-icon

.card
.kpi-card
.chart-card

.input
.select
.filter-bar

.table
.status-badge

.modal
.toast

.empty-state
.error-state
.loading-state
```

---

# 18. Button Design

Primary:

```text id="v0e0yl"
Dark neutral
```

Secondary:

```text id="23v98s"
Border
```

Danger:

```text id="a4y0fj"
Muted red semantic
```

Tidak menggunakan:

```text id="uhf2t0"
Neon button
Gradient button
Glow
```

---

# 19. Global Icon System

Semua icon menggunakan SVG.

```text id="1pglp8"
static/icons/
├── dashboard.svg
├── students.svg
├── analytics.svg
├── prediction.svg
├── risk.svg
├── dataset.svg
├── reports.svg
├── settings.svg
├── search.svg
├── menu.svg
├── sun.svg
├── moon.svg
├── bell.svg
├── plus.svg
├── edit.svg
├── trash.svg
├── eye.svg
└── download.svg
```

Tidak menggunakan Unicode emoji sebagai icon UI.

---

# 20. SVG Icon Usage

Gunakan:

```html id="d9y5wr"
<img
    src="{{ url_for('static', filename='icons/search.svg') }}"
    alt="">
```

atau inline SVG ketika membutuhkan manipulasi warna/state.

Icon dekoratif diberi:

```text id="9r2i1v"
aria-hidden="true"
```

Icon yang berfungsi sebagai tombol wajib mempunyai accessible label.

---

# 21. JavaScript Architecture

```text id="9by4cx"
static/js/
├── app.js
├── theme.js
├── sidebar.js
├── charts.js
└── pages/
    ├── dashboard.js
    ├── students.js
    ├── analytics.js
    ├── prediction.js
    ├── risk.js
    ├── dataset.js
    ├── reports.js
    └── settings.js
```

---

# 22. `app.js`

Global functionality:

```text id="j0ikc5"
API helper
Toast
Modal
Utility functions
Global event handling
```

Contoh API helper:

```javascript id="b6mtf3"
async function apiFetch(url, options = {}) {
    const response = await fetch(url, options);
    const result = await response.json();

    if (!response.ok || !result.success) {
        throw new Error(
            result.error?.message || "Something went wrong."
        );
    }

    return result.data;
}
```

---

# 23. `theme.js`

Tanggung jawab:

```text id="j4g7d8"
Read theme
Set theme
Toggle theme
Save theme
```

Flow:

```text id="c3c2hc"
Theme Button
 ↓
toggleTheme()
 ↓
data-theme
 ↓
localStorage
```

---

# 24. `sidebar.js`

Menangani:

```text id="bkgfvl"
Desktop collapse
Mobile open
Mobile close
Overlay
Escape
```

Mobile flow:

```text id="ljd7p1"
Menu button
 ↓
Sidebar open
 ↓
Overlay
```

Klik overlay:

```text id="29q66v"
Sidebar close
```

---

# 25. `charts.js`

Menjadi helper untuk Chart.js.

Contoh:

```javascript id="3n7psv"
function createLineChart(element, data, options = {}) {
    return new Chart(element, {
        type: "line",
        data,
        options
    });
}
```

Page-specific file menentukan data.

---

# 26. Dashboard JavaScript

`dashboard.js`:

```text id="e1a8b8"
loadDashboard()
    ↓
fetch /api/dashboard
    ↓
render KPI
    ↓
render charts
    ↓
render insights
    ↓
render attention table
```

---

# 27. Dashboard Loading

Saat API dipanggil:

```text id="4m6o91"
KPI → skeleton
Chart → skeleton
Insights → skeleton
Table → skeleton
```

Setelah berhasil:

```text id="p17zgj"
Skeleton
 ↓
Real content
```

---

# 28. Dashboard Empty State

Jika database belum mempunyai data:

```text id="vzzb3f"
No academic data available.

Upload or add student data to start analyzing performance.
```

Jangan menampilkan chart kosong yang membingungkan.

---

# 29. Dashboard Error State

Jika API gagal:

```text id="c8qg02"
Unable to load dashboard data.

[ Retry ]
```

Retry memanggil API kembali.

---

# 30. Students Frontend

Flow:

```text id="m0n3hi"
Page load
 ↓
Fetch students
 ↓
Render table
 ↓
Search / Filter
 ↓
Fetch filtered data
 ↓
Pagination
```

Query:

```text id="j9xj9f"
/api/students?page=1&limit=10&search=...
```

---

# 31. Student Search

Search tidak harus melakukan request pada setiap karakter.

Gunakan debounce.

Contoh konsep:

```text id="j7y8jr"
User typing
 ↓
Wait ~300ms
 ↓
API request
```

Ini mengurangi request yang tidak diperlukan.

---

# 32. Student Detail

Saat membuka:

```text id="i8q8p0"
/students/20240001
```

Frontend memanggil:

```text id="5t2y3x"
/api/students/20240001
```

Kemudian:

```text id="u6h4m7"
Student Info
Performance
GPA History
Factors
Risk
Early Warning
```

---

# 33. Analytics Frontend

Analytics menggunakan filter global halaman:

```text id="qjckf4"
Major
Semester
GPA
Attendance
Risk
```

Ketika filter berubah:

```text id="y1i1ot"
Filter
 ↓
API
 ↓
New data
 ↓
Charts update
```

Tidak reload seluruh halaman jika tidak diperlukan.

---

# 34. Analytics Charts

Urutan:

```text id="x1ng8v"
1. GPA Distribution
2. GPA by Semester
3. GPA by Major
4. GPA Trend
5. Attendance vs GPA
6. Study Hours vs GPA
7. Assignment vs GPA
8. Midterm vs GPA
9. Final vs GPA
10. Correlation Heatmap
```

---

# 35. Chart Responsive Rules

Desktop:

```text id="z2u0a4"
2 columns
```

Mobile:

```text id="n2z8q1"
1 column
```

Chart tidak boleh memiliki fixed width besar yang menyebabkan horizontal overflow.

---

# 36. Prediction Frontend

Form:

```text id="9pj5cm"
Semester
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours

[ Predict GPA ]
```

Submit:

```text id="2k4dko"
POST /api/prediction
```

---

# 37. Prediction Loading

Saat prediction berjalan:

```text id="ysn7iv"
[ Predicting... ]
```

Button disabled.

Setelah response:

```text id="5f7g4x"
Predicted GPA
Performance Category
Model
MAE
RMSE
R²
```

---

# 38. Prediction Error

Contoh:

```text id="s7q3k8"
No trained model is available.

An administrator needs to train a model first.
```

Ini lebih informatif daripada:

```text id="34i2i4"
500 Internal Server Error
```

---

# 39. Risk Frontend

Summary:

```text id="qcvd10"
Low
Medium
High
```

Kemudian:

```text id="a9x4b2"
Risk Distribution
```

dan:

```text id="5b5y4d"
Students Requiring Attention
```

---

# 40. Risk Table

Kolom:

```text id="b4x0bd"
Student
Major
GPA
Attendance
GPA Change
Risk
```

Klik student:

```text id="8j6v8n"
→ Student Detail
```

---

# 41. Dataset Frontend

Flow:

```text id="8a8rpp"
Dataset Page
 ↓
Upload
 ↓
Dataset Overview
 ↓
Preview
 ↓
Validation
 ↓
Cleaning Preview
 ↓
Confirm
 ↓
Apply Cleaning
```

---

# 42. Dataset Upload UX

File dipilih:

```text id="4i8phk"
students.csv
1.4 MB
```

Kemudian:

```text id="j9r9x4"
[ Upload Dataset ]
```

Saat upload:

```text id="l5a9qa"
Uploading...
```

Setelah selesai:

```text id="u5o8j4"
Upload successful.
```

---

# 43. Cleaning UX

Preview:

```text id="7o4p6d"
Cleaning Preview

Missing values       12
Duplicates             4
Invalid GPA            2
Invalid scores         3
Outliers               8

[ Cancel ] [ Apply Cleaning ]
```

Klik Apply:

```text id="5v0ux2"
Confirmation Modal
```

---

# 44. Reports Frontend

Report cards:

```text id="jv9gkm"
Overall Performance
Student Report
Risk Report
ML Report
```

Setiap report:

```text id="j0s9eu"
Preview
PDF
Excel
CSV
```

---

# 45. Report Export

Ketika user memilih PDF:

```text id="r5c5kc"
GET /api/reports/overall/export/pdf
```

Browser menerima file response.

Frontend tidak membuat PDF sendiri.

---

# 46. Settings Frontend

Sections:

```text id="f5f1he"
Appearance
Account
Security
```

Appearance:

```text id="0m1f5r"
Light
Dark
```

Account:

```text id="q2f8f9"
Username
Email
Role
```

Security:

```text id="72zq2a"
Change Password
```

---

# 47. Role-Based Rendering

Jinja dapat digunakan untuk mengatur tampilan:

```jinja2 id="g7z14v"
{% if session.role == "admin" %}
    ...
{% endif %}
```

Namun ini hanya untuk UX.

Backend tetap memvalidasi role.

---

# 48. Responsive Table

Desktop:

```text id="g1gd01"
Normal table
```

Mobile:

```text id="4glfbs"
Horizontal scroll
```

Jangan mengecilkan semua kolom sampai teks tidak terbaca.

Untuk beberapa bagian, table dapat berubah menjadi:

```text id="qf6eqp"
Student Card
```

terutama pada mobile.

---

# 49. Responsive KPI

Desktop:

```text id="j8y4n0"
4 columns
```

Mobile:

```text id="h8xv5w"
2 columns
```

Contoh:

```text id="l9i3xg"
┌──────────┐ ┌──────────┐
│ Students │ │ GPA      │
└──────────┘ └──────────┘

┌──────────┐ ┌──────────┐
│ Attend.  │ │ At Risk  │
└──────────┘ └──────────┘
```

---

# 50. Responsive Charts

Desktop:

```text id="qgy0i5"
┌────────────────┐ ┌────────────────┐
│ Chart          │ │ Chart          │
└────────────────┘ └────────────────┘
```

Mobile:

```text id="bq9hrv"
┌─────────────────────────┐
│ Chart                   │
└─────────────────────────┘

┌─────────────────────────┐
│ Chart                   │
└─────────────────────────┘
```

---

# 51. Animation Rules

Animasi hanya untuk membantu feedback.

Allowed:

```text id="5y0i2g"
Fade
Small translate
Count-up
Chart appearance
Hover transition
```

Durasi:

```text id="9oxpqu"
150ms
200ms
300ms
```

Tidak menggunakan:

```text id="6p4w4n"
Bounce
Particle
Glow
Excessive parallax
Continuous floating
```

---

# 52. Page Load Animation

Contoh:

```css id="iy3t3j"
.page-content {
    animation: page-enter 200ms ease-out;
}
```

Animasi ringan dan tidak mengganggu data.

---

# 53. Accessibility

Frontend wajib memperhatikan:

```text id="yq4c8s"
Semantic HTML
Keyboard navigation
Visible focus
Accessible labels
Button semantics
Form labels
Color contrast
```

Contoh:

```html id="0mt2w5"
<label for="attendance">
    Attendance
</label>

<input
    id="attendance"
    name="attendance"
    type="number">
```

Bukan input tanpa label.

---

# 54. Accessibility and Icons

Button:

```html id="v6jp47"
<button aria-label="Delete student">
    SVG
</button>
```

Bukan:

```html id="m0p7xu"
<button>
    SVG
</button>
```

tanpa informasi tambahan.

---

# 55. API Loading Strategy

Semua API request data-driven harus mempunyai:

```text id="k2oq7k"
Loading
Success
Empty
Error
```

Contoh:

```javascript id="g4k91s"
try {
    showLoading();

    const data = await apiFetch("/api/dashboard");

    renderDashboard(data);
} catch (error) {
    showError(error.message);
}
```

---

# 56. Frontend Data Rule

Jangan hardcode hasil analytics:

```javascript id="w6ut6f"
const averageGPA = 3.24;
```

Gunakan:

```javascript id="3i0q7y"
const data = await apiFetch("/api/dashboard");
```

Kemudian:

```javascript id="5eky8d"
renderKPI(data.average_gpa);
```

---

# 57. Frontend Business Logic Boundary

Frontend boleh melakukan:

```text id="g9m2ck"
Formatting
UI state
Chart configuration
Input validation untuk UX
Filtering presentation
```

Frontend tidak boleh menjadi sumber utama untuk:

```text id="w3v4a0"
Risk calculation
GPA prediction
Authorization
Database validation
ML training
```

---

# 58. Data Formatting

Frontend bertanggung jawab terhadap presentation.

Contoh:

Backend:

```text id="6l4g9k"
3.2456
```

Frontend:

```text id="2p8qg3"
3.25
```

Contoh:

```javascript id="o2f7y8"
function formatGPA(value) {
    return Number(value).toFixed(2);
}
```

---

# 59. Date Formatting

Database:

```text id="x5n7v0"
2026-10-07 13:20:45
```

UI:

```text id="4b1o0s"
7 October 2026
```

Format hanya presentation.

---

# 60. Frontend Folder Final

```text id="b2s6px"
static/
│
├── css/
│   ├── base.css
│   ├── layout.css
│   ├── components.css
│   ├── utilities.css
│   │
│   └── pages/
│       ├── login.css
│       ├── dashboard.css
│       ├── students.css
│       ├── analytics.css
│       ├── prediction.css
│       ├── risk.css
│       ├── dataset.css
│       ├── reports.css
│       └── settings.css
│
├── js/
│   ├── app.js
│   ├── theme.js
│   ├── sidebar.js
│   ├── charts.js
│   │
│   └── pages/
│       ├── dashboard.js
│       ├── students.js
│       ├── analytics.js
│       ├── prediction.js
│       ├── risk.js
│       ├── dataset.js
│       ├── reports.js
│       └── settings.js
│
└── icons/
    ├── dashboard.svg
    ├── students.svg
    ├── analytics.svg
    ├── prediction.svg
    ├── risk.svg
    ├── dataset.svg
    ├── reports.svg
    ├── settings.svg
    └── ...
```

---

# 61. Frontend Request Architecture

```text id="f6s8h3"
                    Browser
                       │
                       ▼
                  Flask Template
                       │
                       ▼
                  Page JavaScript
                       │
                       ▼
                   API Fetch
                       │
                       ▼
                 Flask Blueprint
                       │
                       ▼
                    Service
                       │
              ┌────────┴────────┐
              ▼                 ▼
           MySQL              ML/Data
              │                 │
              └────────┬────────┘
                       ▼
                     JSON
                       │
                       ▼
                  JavaScript
                       │
                       ▼
                    UI Update
```

---

# 62. Final Frontend Page Map

```text id="y1x4m5"
Login
 │
 └── Authentication

Dashboard
 ├── KPI
 ├── Analytics
 ├── Insights
 └── Attention

Students
 ├── Search
 ├── Filter
 ├── Table
 └── Student Detail

Analytics
 ├── Filters
 └── 10 Charts

Prediction
 ├── Form
 ├── Result
 └── History

Risk
 ├── Summary
 ├── Distribution
 ├── Table
 └── Early Warning

Dataset
 ├── Upload
 ├── Preview
 ├── Validation
 └── Cleaning

Reports
 ├── Overall
 ├── Student
 ├── Risk
 └── ML

Settings
 ├── Appearance
 ├── Account
 └── Security
```

---

# 63. Frontend Definition of Done

```text id="q8h9hz"
□ Base template selesai
□ Sidebar selesai
□ Topbar selesai
□ Theme system selesai
□ Light mode selesai
□ Dark mode selesai
□ Responsive layout selesai
□ Component CSS selesai
□ SVG icon system selesai
□ API helper selesai
□ Chart helper selesai
□ Dashboard JS selesai
□ Students JS selesai
□ Analytics JS selesai
□ Prediction JS selesai
□ Risk JS selesai
□ Dataset JS selesai
□ Reports JS selesai
□ Settings JS selesai
□ Loading state tersedia
□ Empty state tersedia
□ Error state tersedia
□ Accessibility dasar tersedia
□ Tidak ada hardcoded analytics result
```

---

# 64. Integrasi Backend + Frontend

Setelah backend dan frontend selesai, alur akhirnya:

```text id="e8h4uw"
                    USER
                      │
                      ▼
                 Flask Page
                      │
                      ▼
              HTML / Jinja
                      │
                      ▼
               JavaScript
                      │
                      ▼
                  REST API
                      │
                      ▼
                  Services
                /    |     \
               /     |      \
           MySQL    ML    Pandas
               \     |      /
                \    |     /
                 ─── Result
                      │
                      ▼
                 JSON Response
                      │
                      ▼
                UI Components
                      │
                      ▼
                 USER INSIGHT
```

