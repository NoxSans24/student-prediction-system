# AUTHENTICATION_SPECIFICATION.md

Kita lanjut ke **Authentication & Authorization Specification**. Bagian ini menentukan bagaimana user masuk ke sistem, bagaimana role bekerja, dan module mana yang boleh diakses oleh **Admin** dan **Analyst**.

Prinsip utama:

> **Authentication menentukan siapa user-nya, sedangkan Authorization menentukan apa yang boleh dilakukan user tersebut.**

---

# 1. Tujuan Authentication

Authentication digunakan untuk:

* Login user
* Mengidentifikasi user
* Menyimpan session
* Menentukan role
* Melindungi halaman internal
* Membatasi akses berdasarkan permission
* Logout secara aman

Flow:

```text
Login
  ↓
Validate Credentials
  ↓
User Found?
  ↓
Verify Password
  ↓
Create Session
  ↓
Check Role
  ↓
Dashboard
```

---

# 2. User Roles

Sistem memiliki dua role:

```text
Admin
Analyst
```

Sesuai PRD:

### Admin

Memiliki akses penuh terhadap platform.

Dapat:

* Dashboard
* Students
* Analytics
* Prediction
* Risk Analysis
* Dataset Management
* Reports
* Settings
* Dataset upload
* Data cleaning
* Student CRUD
* Train ML

### Analyst

Memiliki akses analisis.

Dapat:

* Dashboard
* Students
* Analytics
* Prediction
* Risk Analysis
* Dataset overview
* Reports

Tidak memiliki akses penuh terhadap administrative dataset management atau training model jika fitur tersebut membutuhkan hak Admin.

---

# 3. Permission Matrix

| Module           | Admin |      Analyst      |
| ---------------- | :---: | :---------------: |
| Dashboard        |   ✓   |         ✓         |
| Students         |   ✓   |         ✓         |
| Student CRUD     |   ✓   |         —         |
| Analytics        |   ✓   |         ✓         |
| Prediction       |   ✓   |         ✓         |
| Risk Analysis    |   ✓   |         ✓         |
| Dataset Overview |   ✓   |         ✓         |
| Dataset Upload   |   ✓   |         —         |
| Data Cleaning    |   ✓   |         —         |
| ML Training      |   ✓   |         —         |
| Reports          |   ✓   |         ✓         |
| Settings         |   ✓   | sesuai permission |

Tanda `—` berarti tidak tersedia untuk role tersebut.

---

# 4. User Database

Authentication menggunakan tabel:

```text
users
```

Struktur:

```text
users
├── id
├── username
├── email
├── password_hash
├── role
├── created_at
└── updated_at
```

Password **tidak boleh disimpan sebagai plaintext**.

---

# 5. Password Security

Password harus disimpan dalam bentuk hash.

Flow:

```text
User Password
      ↓
Password Hashing
      ↓
Database
```

Saat login:

```text
Input Password
      ↓
Verify Against Hash
      ↓
Valid?
```

Jangan melakukan:

```python
if password == database_password:
```

Password database harus berupa hash.

---

# 6. Login

Halaman login minimal memiliki:

```text
Login

Username / Email
[________________]

Password
[________________]

[ Login ]
```

Optional:

```text
Remember me
```

tetapi fitur ini tidak wajib untuk MVP.

---

# 7. Login Validation

Validasi:

```text
Username/email tidak kosong
Password tidak kosong
```

Jika kosong:

> Please enter your username and password.

Jika credentials salah:

> Invalid username or password.

Jangan memberitahu apakah username atau password yang salah secara spesifik karena dapat memberikan informasi tambahan kepada attacker.

---

# 8. Login Flow

```text
User
 ↓
Login Page
 ↓
POST /login
 ↓
Find User
 ↓
Verify Password
 ↓
Valid?
 ├── NO → Error
 │
 └── YES
       ↓
    Create Session
       ↓
    Store User ID
       ↓
    Store Role
       ↓
    Dashboard
```

---

# 9. Session

Setelah login berhasil, Flask session digunakan untuk mempertahankan authentication state.

Contoh informasi:

```text
session
├── user_id
├── username
└── role
```

Jangan menyimpan password di session.

---

# 10. Protected Routes

Halaman internal harus membutuhkan login.

Contoh:

```text
/dashboard
/students
/analytics
/prediction
/risk
/dataset
/reports
/settings
```

Jika user belum login:

```text
Protected Route
      ↓
Authenticated?
   ┌──┴──┐
  NO    YES
   ↓      ↓
Login   Continue
```

User diarahkan ke:

```text
/login
```

---

# 11. Role-Based Access Control

Setelah authentication, sistem memeriksa role.

Contoh:

```text
Admin
 ↓
Dataset Management
 ↓
Allowed
```

Sedangkan:

```text
Analyst
 ↓
Dataset Management
 ↓
Forbidden
```

User tidak boleh mendapatkan akses hanya dengan mengetik URL secara manual.

Contoh:

```text
/dataset/upload
```

Tetap harus dicek di backend.

---

# 12. Backend Authorization

Authorization **tidak boleh hanya dilakukan di frontend**.

Tidak cukup hanya menyembunyikan tombol:

```html
<button>Upload Dataset</button>
```

Karena user masih dapat memanggil endpoint secara langsung.

Backend harus memeriksa:

```text
Request
 ↓
Authenticated?
 ↓
Correct Role?
 ↓
Execute Action
```

---

# 13. Flask Decorator

Untuk mempermudah authorization, dapat dibuat decorator.

Contoh konsep:

```python
@login_required
def dashboard():
    ...
```

Untuk Admin:

```python
@role_required("admin")
def upload_dataset():
    ...
```

Untuk beberapa role:

```python
@roles_required("admin", "analyst")
def analytics():
    ...
```

Ini merupakan desain implementasi, bukan requirement langsung dari PRD.

---

# 14. Unauthorized Response

Jika user tidak memiliki permission:

```text
403 Forbidden
```

Namun UI sebaiknya memberikan halaman yang mudah dipahami:

> You don't have permission to access this page.

Tersedia tombol:

```text
[ Back to Dashboard ]
```

---

# 15. Login Redirect

Setelah login:

### Admin

```text
/login
  ↓
/dashboard
```

### Analyst

```text
/login
  ↓
/dashboard
```

Dashboard menjadi landing page untuk kedua role.

---

# 16. Logout

Flow:

```text
User
 ↓
Logout
 ↓
Clear Session
 ↓
/login
```

Endpoint:

```text
/logout
```

Setelah logout, halaman protected tidak boleh dapat diakses menggunakan session lama.

---

# 17. Navigation Based on Role

Sidebar dapat menyesuaikan role.

### Admin

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

### Analyst

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
```

Perbedaan utama dapat terlihat pada action yang tersedia di masing-masing halaman.

Contoh Dataset:

Admin:

```text
[ Upload Dataset ]
[ Clean Dataset ]
[ Process Dataset ]
```

Analyst:

```text
Dataset Overview
```

Tetapi backend tetap melakukan authorization.

---

# 18. Student CRUD Authorization

Admin memiliki akses:

```text
Create
Read
Update
Delete
```

Analyst:

```text
Read
```

Contoh:

```text
Admin
Student List
 ↓
[Add Student]
[Edit]
[Delete]
```

Analyst:

```text
Student List
 ↓
[View]
```

---

# 19. Dataset Authorization

Admin:

```text
Upload
Validate
Clean
Process
View
```

Analyst:

```text
View
```

Ini sesuai pembagian tanggung jawab dalam PRD.

---

# 20. ML Training Authorization

Training model merupakan operasi yang dapat memengaruhi model aktif.

Karena itu:

```text
Admin → Train Model
Analyst → View ML Results / Prediction
```

Flow:

```text
Admin
 ↓
ML Training
 ↓
Train Models
 ↓
Evaluate
 ↓
Select Best Model
 ↓
Save Model
```

Analyst menggunakan model yang sudah tersedia.

---

# 21. Prediction Authorization

Prediction tersedia untuk:

```text
Admin
Analyst
```

Flow:

```text
Prediction Form
 ↓
Validate Input
 ↓
Load Best Model
 ↓
Predict GPA
 ↓
Save Result
 ↓
Display Result
```

---

# 22. Risk Analysis Authorization

Risk Analysis tersedia untuk:

```text
Admin
Analyst
```

Karena keduanya membutuhkan informasi mahasiswa yang memerlukan perhatian.

---

# 23. Reports Authorization

Kedua role dapat menghasilkan report sesuai scope.

```text
Admin
  ↓
Reports

Analyst
  ↓
Reports
```

Tetapi report harus tetap mengikuti data access policy role.

---

# 24. Settings

Settings dapat dibagi berdasarkan jenis pengaturan.

Contoh:

```text
Settings
├── Profile
├── Appearance
└── System Settings
```

Admin dapat memiliki akses ke pengaturan sistem.

Analyst dapat mengakses pengaturan personal seperti:

```text
Profile
Appearance
```

Jika diperlukan.

---

# 25. Profile

User dapat melihat informasi:

```text
Username
Email
Role
```

Contoh:

```text
Profile

Username
noxsans

Email
admin@example.com

Role
Admin
```

Password tidak pernah ditampilkan.

---

# 26. Change Password

Jika fitur tersedia:

```text
Current Password
New Password
Confirm New Password
```

Validasi:

```text
Current password valid
New password tidak kosong
Confirmation sama
```

Setelah berhasil:

> Password changed successfully.

---

# 27. Password Requirements

Minimal aplikasi dapat memiliki aturan:

```text
Password tidak kosong
Password confirmation harus sama
```

Aturan kompleks seperti panjang minimum, karakter khusus, dan sebagainya dapat ditetapkan sebagai security policy implementasi.

Jika diterapkan, aturan harus konsisten antara frontend dan backend.

---

# 28. Account Status

Untuk MVP, user cukup memiliki:

```text
active
```

atau status dapat ditambahkan jika memang dibutuhkan.

Jika sistem nantinya mendukung:

```text
active
inactive
```

maka login user inactive harus ditolak.

Namun ini bukan requirement utama dari PRD, sehingga dapat menjadi pengembangan lanjutan.

---

# 29. Security Configuration

Konfigurasi sensitif tidak boleh ditulis langsung di source code.

Contoh:

```text
.env
```

Berisi:

```text
SECRET_KEY=...
DB_HOST=...
DB_USER=...
DB_PASSWORD=...
DB_NAME=student_performance_analytics
```

File `.env` tidak boleh masuk Git repository.

---

# 30. Database Credentials

Jangan:

```python
DB_PASSWORD = "123456"
```

di dalam source code production.

Gunakan environment variable.

Flow:

```text
.env
 ↓
Configuration
 ↓
Flask
 ↓
Database Connection
```

---

# 31. Session Security

Session configuration harus memperhatikan:

```text
SECRET_KEY
SESSION_COOKIE_HTTPONLY
SESSION_COOKIE_SECURE
SESSION_COOKIE_SAMESITE
```

Nilai konfigurasi final mengikuti environment deployment.

Untuk development lokal, HTTPS mungkin belum tersedia sehingga `Secure` perlu disesuaikan.

---

# 32. CSRF Protection

Form yang melakukan operasi penting sebaiknya memiliki perlindungan CSRF.

Terutama:

```text
Login
Upload Dataset
Create Student
Edit Student
Delete Student
Change Password
Train Model
```

Untuk Flask, implementasi dapat menggunakan mekanisme CSRF protection seperti Flask-WTF atau solusi yang sesuai.

---

# 33. Dangerous Actions

Operasi berikut memerlukan perhatian khusus:

```text
Delete Student
Delete Dataset
Apply Cleaning
Train Model
```

UI harus memberikan confirmation untuk operasi destruktif atau berdampak besar.

Contoh:

```text
Delete Student?

This action cannot be undone.

[Cancel] [Delete]
```

---

# 34. Authentication Error Handling

System harus menangani:

### Invalid Login

```text
Invalid username or password.
```

### Session Expired

```text
Your session has expired.
Please log in again.
```

### Unauthorized

```text
You don't have permission to perform this action.
```

### Forbidden Page

```text
You don't have permission to access this page.
```

Tidak menampilkan stack trace.

---

# 35. Authentication Routes

Struktur route:

```text
routes/
└── auth.py
```

Endpoint yang disarankan:

```text
GET  /login
POST /login
POST /logout
GET  /profile
POST /profile/password
```

Route tambahan dapat dibuat sesuai kebutuhan implementasi.

---

# 36. Authentication Service

Jika logic mulai berkembang, buat:

```text
services/
└── auth_service.py
```

Fungsi:

```python
authenticate_user()
verify_password()
create_user()
change_password()
get_current_user()
```

Route hanya menangani request/response.

---

# 37. Architecture

Authentication:

```text
Browser
   ↓
Auth Route
   ↓
Auth Service
   ↓
Database
   ↓
User
   ↓
Session
```

Authorization:

```text
Request
   ↓
Authentication Check
   ↓
Role Check
   ↓
Permission Check
   ↓
Business Logic
```

---

# 38. Definition of Done

Authentication dianggap selesai jika:

* [ ] Login tersedia
* [ ] Logout tersedia
* [ ] Password disimpan dalam hash
* [ ] Session tersedia
* [ ] Protected routes tersedia
* [ ] Admin role tersedia
* [ ] Analyst role tersedia
* [ ] Role-based authorization tersedia
* [ ] Admin dapat mengakses fungsi administrative
* [ ] Analyst tidak dapat melakukan fungsi Admin
* [ ] Authorization dilakukan di backend
* [ ] Student CRUD dibatasi berdasarkan role
* [ ] Dataset management dibatasi berdasarkan role
* [ ] ML training dibatasi berdasarkan role
* [ ] Prediction tersedia sesuai scope
* [ ] Risk Analysis tersedia sesuai scope
* [ ] Reports tersedia sesuai scope
* [ ] Logout menghapus session
* [ ] Unauthorized response tersedia
* [ ] Error handling tersedia
* [ ] `.env` digunakan untuk secret/configuration
* [ ] `.env` masuk `.gitignore`
* [ ] CSRF protection untuk operasi sensitif
* [ ] Confirmation untuk operasi destruktif
* [ ] Tidak ada password plaintext
* [ ] Tidak ada credential hardcoded

---

# Arsitektur Project Setelah Authentication

Sekarang struktur sistem kita menjadi semakin jelas:

```text
                    ┌──────────────────┐
                    │   AUTHENTICATION │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ AUTHORIZATION    │
                    │ Admin / Analyst  │
                    └────────┬─────────┘
                             ↓
┌────────────────────────────────────────────────────┐
│                 APPLICATION                        │
│                                                    │
│ Dashboard                                          │
│ Students                                           │
│ Analytics                                          │
│ Prediction                                         │
│ Risk Analysis                                      │
│ Dataset                                            │
│ Reports                                            │
│ Settings                                           │
└────────────────────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
           Analytics         ML        Risk Engine
              ↓              ↓              ↓
          Insights      Prediction     Risk Level
              └──────────────┼──────────────┘
                             ↓
                           Reports
```

## Dokumen desain yang sudah selesai

```text
01. PRD
02. Dashboard Specification
03. Data Specification
04. Database Schema
05. Data Cleaning Specification
06. Risk Engine Specification
07. ML Specification
08. Analytics Specification
09. Insight Specification
10. Report Specification
11. Authentication Specification ← SELESAI
```