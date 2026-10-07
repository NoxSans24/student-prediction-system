

## 1. Tujuan

Tahap ini membuat fondasi Flask sebelum fitur bisnis mulai dibuat.

Target akhirnya:

```text
Browser
   ↓
Flask Application
   ↓
Blueprint
   ↓
Route
   ↓
Response
```

Pada tahap ini **belum membuat fitur Student, Analytics, ML, Risk, dan Dataset secara lengkap**.

Fokusnya adalah memastikan aplikasi Flask dapat berjalan dengan struktur yang benar.

---

# 2. Struktur Foundation

Struktur minimum:

```text
student-performance-analytics/
│
├── app.py
├── config.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   └── dashboard.py
│
├── services/
│   └── __init__.py
│
├── database/
│   ├── __init__.py
│   └── connection.py
│
├── templates/
│   ├── base.html
│   └── errors/
│       ├── 403.html
│       ├── 404.html
│       └── 500.html
│
└── static/
    ├── css/
    └── js/
```

Folder fitur lainnya tetap dibuat sesuai struktur final, tetapi belum harus memiliki logic lengkap.

---

# 3. Application Factory

Flask menggunakan pola **Application Factory**.

Konsep:

```text
create_app()
     │
     ├── Load config
     ├── Initialize extensions
     ├── Register blueprints
     ├── Register error handlers
     └── Return app
```

Tujuannya agar aplikasi tidak bergantung pada satu konfigurasi global.

Struktur:

```python
def create_app():
    app = Flask(__name__)

    # configuration

    # extensions

    # blueprints

    # error handlers

    return app
```

Kemudian `app.py` menjadi entry point.

---

# 4. Flask Configuration

Configuration harus mengambil nilai sensitif dari `.env`.

Contoh:

```text
SECRET_KEY
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

Jangan:

```python
SECRET_KEY = "abc123"
```

untuk production.

---

# 5. Environment

Environment dibagi menjadi:

```text
Development
Testing
Production
```

Untuk tahap awal:

```text
FLASK_ENV=development
```

Development memungkinkan debugging selama proses pembuatan aplikasi.

Namun error detail tidak boleh diberikan kepada user pada production.

---

# 6. Database Connection Foundation

File:

```text
database/connection.py
```

Tanggung jawab:

```text
Configuration
     ↓
MySQL Connector
     ↓
Database Connection
```

Connection harus:

* menggunakan environment variable
* memiliki error handling
* dapat digunakan service
* tidak menyimpan credential langsung di source code

---

# 7. Database Health Check

Aplikasi harus dapat mengecek koneksi MySQL.

Contoh:

```text
GET /health
```

Response ketika semuanya normal:

```json
{
    "success": true,
    "data": {
        "status": "ok",
        "database": "connected"
    }
}
```

Jika database bermasalah:

```json
{
    "success": false,
    "error": {
        "code": "DATABASE_ERROR",
        "message": "Database connection failed"
    }
}
```

Jangan menampilkan informasi internal seperti:

```text
password
host credential
SQL traceback
database driver traceback
```

---

# 8. Blueprint Architecture

Blueprint yang akan digunakan:

```text
routes/
├── auth.py
├── dashboard.py
├── students.py
├── analytics.py
├── prediction.py
├── risk.py
├── dataset.py
└── reports.py
```

Setiap blueprint bertanggung jawab pada domain masing-masing.

Contoh:

```text
dashboard.py
     ↓
Dashboard routes

students.py
     ↓
Student routes

analytics.py
     ↓
Analytics routes
```

---

# 9. Route Responsibility

Route harus tipis.

Route bertugas:

```text
Request
 ↓
Authentication
 ↓
Validation
 ↓
Service
 ↓
Response
```

Route **tidak** seharusnya berisi business logic panjang.

Contoh yang dihindari:

```text
Route
 ├── SQL
 ├── Pandas
 ├── Risk calculation
 ├── ML calculation
 ├── Formatting
 └── Response
```

Sebaliknya:

```text
Route
 ↓
Service
 ↓
Database / ML / Data Processing
```

---

# 10. Initial Routes

Pada foundation, minimal tersedia:

```text
GET /
GET /health
GET /login
```

Jika authentication belum selesai, `/login` hanya menjadi halaman dasar.

Endpoint API nantinya mengikuti `API_SPECIFICATION.md`.

---

# 11. Root Route

Root:

```text
/
```

Untuk tahap awal dapat diarahkan ke:

```text
/login
```

atau Dashboard jika user sudah authenticated.

Flow final:

```text
/
 ↓
Authenticated?
 ├── Yes → Dashboard
 └── No  → Login
```

---

# 12. Error Handling

Aplikasi harus memiliki handler:

```text
400
401
403
404
422
500
```

Contoh:

```text
404
Page Not Found
```

bukan traceback Flask.

---

# 13. Error Page

Struktur:

```text
templates/errors/
├── 403.html
├── 404.html
└── 500.html
```

Desain mengikuti design system:

* DM Sans
* light/dark theme
* neutral
* minimal
* SVG icon
* responsive

Tidak menggunakan halaman error default Flask yang masih terlihat seperti halaman development.

---

# 14. API Error Format

Semua API menggunakan format:

```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable message"
    }
}
```

Contoh:

```json
{
    "success": false,
    "error": {
        "code": "NOT_FOUND",
        "message": "Student not found"
    }
}
```

---

# 15. API Success Format

Format standar:

```json
{
    "success": true,
    "data": {}
}
```

Untuk collection:

```json
{
    "success": true,
    "data": {
        "items": [],
        "pagination": {}
    }
}
```

---

# 16. Logging

Foundation harus memiliki logging dasar.

Minimal mencatat:

```text
INFO
WARNING
ERROR
```

Contoh:

```text
INFO  Application started
INFO  Database connected
WARNING Invalid request
ERROR Database connection failed
```

Jangan mencatat password.

---

# 17. Security Foundation

Minimal:

```text
SECRET_KEY
Session configuration
Environment variables
Error handling
Input validation
Password protection
```

Untuk authentication nanti ditambahkan:

```text
CSRF
HTTPOnly
SameSite
Role authorization
```

---

# 18. Session Configuration

Session final menggunakan:

```text
HTTPOnly
SameSite
Secure
```

Namun `Secure` perlu disesuaikan ketika development masih menggunakan:

```text
http://localhost
```

karena HTTPS belum tersedia.

---

# 19. Template Foundation

`base.html` menjadi template utama.

Struktur konseptual:

```text
base.html
│
├── <head>
│   ├── DM Sans
│   ├── CSS
│   └── metadata
│
├── Sidebar
│
├── Topbar
│
├── Main Content
│
└── JavaScript
```

Halaman lain menggunakan:

```jinja2
{% extends "base.html" %}
```

Dengan:

```text
content
scripts
styles
```

sebagai block.

---

# 20. Static Asset

CSS:

```text
static/css/
├── base.css
├── layout.css
├── components.css
└── utilities.css
```

JavaScript:

```text
static/js/
├── app.js
├── theme.js
└── sidebar.js
```

Foundation tidak perlu langsung membuat seluruh CSS halaman.

---

# 21. Theme Foundation

Theme menggunakan:

```text
data-theme
```

Contoh:

```html
<html data-theme="light">
```

JavaScript:

```text
Theme toggle
 ↓
Change data-theme
 ↓
Save preference
 ↓
Reload
 ↓
Restore preference
```

---

# 22. Sidebar Foundation

Sidebar harus sudah mendukung:

### Desktop

```text
240px
```

### Tablet

```text
Collapsed
```

### Mobile

```text
Off-canvas
```

Navigation final:

```text
Overview
├── Dashboard
├── Students
└── Analytics

Intelligence
├── Prediction
└── Risk Analysis

Data
├── Dataset
└── Reports

Settings
```

Pada tahap foundation, menu boleh masih berupa placeholder.

---

# 23. Global JavaScript

`static/js/app.js` bertanggung jawab untuk fungsi global.

Contoh:

```text
API helper
Global initialization
Toast
Loading state
Common utilities
```

Sedangkan:

```text
theme.js
```

khusus theme.

Dan:

```text
sidebar.js
```

khusus sidebar.

---

# 24. API Fetch Helper

Frontend nantinya tidak melakukan:

```javascript
fetch(...)
```

secara berulang dengan konfigurasi berbeda.

Gunakan helper:

```text
apiFetch()
```

yang menangani:

```text
Request
 ↓
Response
 ↓
JSON
 ↓
HTTP error
 ↓
Application error
```

Dengan begitu semua halaman menggunakan pola API yang konsisten.

---

# 25. CORS

Karena frontend menggunakan Flask + Jinja2 pada aplikasi yang sama, **CORS tidak perlu menjadi dependency utama untuk MVP**.

Arsitektur:

```text
Browser
   ↓
Flask
 ┌─┴─────────────┐
 │               │
HTML/Jinja      API
```

Bukan:

```text
Frontend Server
       ↓
Different Backend Server
```

CORS baru diperlukan jika arsitektur berubah menjadi frontend dan backend terpisah.

---

# 26. Initial Testing

Setelah foundation selesai:

### Test 1

```text
python app.py
```

Expected:

```text
Flask starts successfully
```

### Test 2

```text
GET /
```

Expected:

```text
Redirect/Login page
```

### Test 3

```text
GET /health
```

Expected:

```text
success = true
database = connected
```

### Test 4

Akses URL yang tidak ada:

```text
/test-random
```

Expected:

```text
404 page
```

---

# 27. Definition of Done

Flask Foundation selesai jika:

* [ ] Application Factory berjalan.
* [ ] Configuration berhasil dimuat.
* [ ] `.env` terbaca.
* [ ] Flask dapat berjalan.
* [ ] Blueprint berhasil diregistrasikan.
* [ ] Database connection berhasil.
* [ ] `/health` tersedia.
* [ ] Database health check tersedia.
* [ ] Error handler tersedia.
* [ ] 404 page tersedia.
* [ ] 403 page tersedia.
* [ ] 500 page tersedia.
* [ ] Base template tersedia.
* [ ] DM Sans terpasang.
* [ ] Theme foundation tersedia.
* [ ] Sidebar foundation tersedia.
* [ ] Global JavaScript tersedia.
* [ ] API response format konsisten.
* [ ] Logging dasar tersedia.
* [ ] Tidak ada credential hardcoded.



