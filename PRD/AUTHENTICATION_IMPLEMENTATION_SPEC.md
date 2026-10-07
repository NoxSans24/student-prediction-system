# AUTHENTICATION_IMPLEMENTATION_SPEC.md

## 1. Tujuan

Tahap ini mengimplementasikan sistem **Authentication & Authorization** untuk Student Performance Analytics.

Authentication bertugas menjawab:

> “Siapa user yang sedang menggunakan aplikasi?”

Authorization menjawab:

> “Apa yang boleh dilakukan user tersebut?”

Flow:

```text
User
 ↓
Login
 ↓
Credential Verification
 ↓
Password Hash Verification
 ↓
Create Session
 ↓
Role Detection
 ↓
Access Protected Page/API
```

Role yang digunakan:

```text
Admin
Analyst
```

---

# 2. Scope

Tahap ini mencakup:

* Login
* Logout
* Password hashing
* Session
* Role
* Route protection
* API protection
* Permission checking
* 401/403 handling
* User profile dasar
* Change password
* CSRF untuk form sensitif
* Security configuration

Belum mencakup:

* Student CRUD
* Dataset upload
* ML training
* Risk Engine
* Reports

Fitur tersebut akan menggunakan authentication yang dibuat pada tahap ini.

---

# 3. Struktur File

Setelah tahap ini:

```text
routes/
├── __init__.py
├── auth.py
└── dashboard.py

services/
├── __init__.py
└── auth_service.py

utils/
├── __init__.py
├── decorators.py
└── security.py

templates/
├── base.html
├── auth/
│   └── login.html
├── settings/
│   └── profile.html
└── errors/
    ├── 401.html
    ├── 403.html
    └── 404.html
```

Jika CSRF membutuhkan module tersendiri, dapat ditambahkan:

```text
utils/csrf.py
```

---

# 4. Authentication Flow

Flow login:

```text
Login Form
    ↓
POST /login
    ↓
Validate Input
    ↓
Find User
    ↓
Verify Password Hash
    ↓
Valid?
 ┌──┴──┐
No    Yes
 ↓      ↓
Error  Create Session
          ↓
       Dashboard
```

Password tidak pernah dibandingkan sebagai plaintext.

---

# 5. Login Form

Halaman:

```text
/login
```

Input:

```text
Username / Email
Password
```

Button:

```text
Sign In
```

State:

```text
Initial
Loading
Error
Success
```

Error login harus menggunakan pesan umum seperti:

```text
Invalid username/email or password.
```

Jangan memberi tahu:

```text
Username benar, password salah.
```

atau:

```text
User tidak ditemukan.
```

Karena dapat membantu user enumeration.

---

# 6. Password Hashing

Password disimpan sebagai:

```text
password_hash
```

Bukan:

```text
password
```

Hashing dilakukan menggunakan mekanisme password hashing yang aman dari library Python/Flask yang sesuai.

Flow:

```text
Register/Create User
        ↓
Plain Password
        ↓
Password Hash
        ↓
Database
```

Login:

```text
Password Input
      ↓
Verify Against Hash
      ↓
Valid / Invalid
```

Password asli tidak disimpan kembali.

---

# 7. User Creation

Untuk development awal, user dapat dibuat melalui seed process.

Contoh:

```text
admin
analyst
```

Password seed hanya digunakan untuk development dan harus sudah melalui hashing sebelum masuk database.

Jangan memasukkan plaintext password ke `users.password_hash`.

---

# 8. Session

Setelah login berhasil, session hanya menyimpan informasi minimum:

```text
user_id
username
role
```

Contoh konsep:

```python
session["user_id"] = user["id"]
session["username"] = user["username"]
session["role"] = user["role"]
```

Tidak boleh:

```python
session["password"] = ...
```

atau:

```python
session["password_hash"] = ...
```

---

# 9. Session Lifecycle

```text
Login
 ↓
Session Created
 ↓
User navigates application
 ↓
Session Checked
 ↓
Logout
 ↓
Session Cleared
```

Saat logout:

```text
session.clear()
```

Setelah logout, halaman protected tidak boleh dapat diakses lagi.

---

# 10. Login Redirect

Jika login berhasil:

```text
/login
   ↓
Dashboard
```

Jika user mencoba membuka halaman protected sebelum login:

```text
/students
   ↓
Not authenticated
   ↓
/login
```

Setelah login, aplikasi dapat mengarahkan kembali ke halaman tujuan apabila mekanisme `next` diterapkan dengan aman.

Jangan menerima redirect URL secara bebas tanpa validasi karena dapat menyebabkan open redirect.

---

# 11. Authentication Decorator

Buat decorator:

```text
@login_required
```

Fungsinya:

```text
Request
 ↓
Session exists?
 ├── No → 401/Login
 └── Yes → Continue
```

Contoh:

```python
@login_required
def dashboard():
    ...
```

Semua halaman protected harus menggunakan decorator ini.

---

# 12. Role Decorator

Gunakan:

```text
@role_required("admin")
```

atau:

```text
@roles_required("admin", "analyst")
```

Contoh:

```python
@role_required("admin")
def upload_dataset():
    ...
```

Analyst yang mencoba mengaksesnya mendapatkan:

```text
403 Forbidden
```

---

# 13. Permission Matrix

| Feature           | Admin | Analyst |
| ----------------- | ----: | ------: |
| Dashboard         |   Yes |     Yes |
| Students View     |   Yes |     Yes |
| Student Create    |   Yes |      No |
| Student Edit      |   Yes |      No |
| Student Delete    |   Yes |      No |
| Analytics         |   Yes |     Yes |
| Prediction        |   Yes |     Yes |
| Risk Analysis     |   Yes |     Yes |
| Dataset View      |   Yes |     Yes |
| Dataset Upload    |   Yes |      No |
| Dataset Cleaning  |   Yes |      No |
| ML Training       |   Yes |      No |
| Reports           |   Yes |     Yes |
| Personal Settings |   Yes |     Yes |
| System Settings   |   Yes |      No |

---

# 14. Backend Authorization

Menyembunyikan tombol frontend **bukan security**.

Contoh:

```text
Analyst
 ↓
Frontend tidak menampilkan Delete
```

belum cukup.

Analyst masih dapat mencoba:

```http
DELETE /api/students/123
```

Backend harus memeriksa:

```text
Authenticated?
      ↓
Role?
      ↓
Admin?
```

Jika bukan:

```text
403 FORBIDDEN
```

---

# 15. API Authentication

API protected juga harus menggunakan authentication.

Contoh:

```text
GET /api/students
```

Tanpa session:

```json
{
    "success": false,
    "error": {
        "code": "UNAUTHORIZED",
        "message": "Authentication required"
    }
}
```

HTTP status:

```text
401
```

---

# 16. API Authorization

Contoh:

```text
POST /api/datasets/upload
```

Analyst:

```text
Authenticated
      ↓
Role = analyst
      ↓
Not authorized
      ↓
403
```

Response:

```json
{
    "success": false,
    "error": {
        "code": "FORBIDDEN",
        "message": "You do not have permission to perform this action"
    }
}
```

---

# 17. `/api/auth/me`

Endpoint:

```text
GET /api/auth/me
```

Digunakan frontend untuk mengetahui user yang sedang login.

Response:

```json
{
    "success": true,
    "data": {
        "id": 1,
        "username": "admin",
        "role": "admin"
    }
}
```

Jangan mengembalikan:

```text
password
password_hash
```

---

# 18. Logout

Endpoint:

```text
POST /logout
```

atau:

```text
POST /api/logout
```

Flow:

```text
Logout Request
 ↓
Clear Session
 ↓
Success
```

Response API:

```json
{
    "success": true,
    "data": {
        "message": "Logged out successfully"
    }
}
```

---

# 19. User Profile

Halaman:

```text
/settings/profile
```

Menampilkan:

```text
Username
Email
Role
```

Role ditampilkan sebagai informasi.

Contoh:

```text
Username
admin

Email
admin@example.com

Role
Administrator
```

Password tidak ditampilkan.

---

# 20. Change Password

Jika fitur change password digunakan:

```text
Current Password
New Password
Confirm New Password
```

Flow:

```text
Current Password
 ↓
Verify
 ↓
New Password Validation
 ↓
Hash New Password
 ↓
Update Database
 ↓
Success
```

Jika current password salah:

```text
Current password is incorrect.
```

Password baru tidak boleh disimpan plaintext.

---

# 21. Password Policy

Password policy minimal harus memastikan:

* tidak kosong
* panjang minimum
* confirmation sama

Project tidak perlu membuat aturan password yang terlalu kompleks jika belum dibutuhkan.

Tujuan utama adalah mencegah password kosong/lemah dan memastikan penyimpanan aman.

---

# 22. CSRF Protection

Form sensitif harus memiliki CSRF protection.

Terutama:

```text
Login
Logout
Change Password
Create Student
Update Student
Delete Student
Dataset Upload
Apply Cleaning
Train ML
```

Untuk request yang mengubah state:

```text
POST
PUT
PATCH
DELETE
```

harus ada perlindungan CSRF sesuai mekanisme Flask yang digunakan.

---

# 23. Session Security

Konfigurasi session harus mempertimbangkan:

```text
HTTPOnly
SameSite
Secure
```

Tujuan:

### HTTPOnly

Membantu mencegah JavaScript membaca cookie session secara langsung.

### SameSite

Membantu mengurangi risiko cross-site request.

### Secure

Cookie hanya dikirim melalui HTTPS ketika production sudah menggunakan HTTPS.

Untuk localhost development yang masih menggunakan HTTP, konfigurasi harus disesuaikan agar session tetap bekerja.

---

# 24. Session Expiration

Session sebaiknya tidak berlaku tanpa batas.

Konfigurasi dapat menggunakan:

```text
PERMANENT_SESSION_LIFETIME
```

Nilai final dapat ditentukan ketika deployment.

Untuk MVP development, session timeout dapat dibuat sederhana terlebih dahulu.

---

# 25. Brute Force Consideration

Authentication layer harus dirancang agar nantinya dapat mendukung:

```text
Login attempt tracking
Rate limiting
Account protection
```

Namun rate limiting bukan bagian wajib dari MVP awal jika belum menggunakan infrastructure khusus.

Minimal:

* jangan memberikan detail credential yang salah
* gunakan password hashing
* jangan expose user existence
* gunakan session security

---

# 26. Authentication Service

File:

```text
services/auth_service.py
```

Fungsi yang direkomendasikan:

```text
authenticate_user()
get_user_by_identity()
verify_password()
create_user()
update_password()
get_current_user()
logout_user()
```

Service bertanggung jawab atas business logic authentication.

---

# 27. Auth Route

File:

```text
routes/auth.py
```

Route:

```text
GET  /login
POST /login
POST /logout
GET  /api/auth/me
```

Route tidak melakukan hashing secara langsung.

Flow:

```text
Route
 ↓
Auth Service
 ↓
User Repository
 ↓
Database
```

---

# 28. Authentication State

Frontend membutuhkan tiga kondisi:

### Guest

```text
No session
```

Tampilan:

```text
Login
```

### Authenticated

```text
Session valid
```

Tampilan:

```text
Dashboard
Sidebar
Profile
```

### Forbidden

```text
Authenticated
but insufficient permission
```

Tampilan:

```text
403 Forbidden
```

---

# 29. Sidebar Role Awareness

Sidebar dapat menyesuaikan role.

Admin:

```text
Overview
Intelligence
Data
Settings
```

Analyst:

```text
Overview
Intelligence
Data
Settings
```

Tetapi action tertentu tidak ditampilkan.

Contoh Admin:

```text
+ Add Student
+ Upload Dataset
+ Train Model
```

Analyst:

```text
Tidak ada action admin
```

Sekali lagi, ini hanya UX.

Security tetap dilakukan backend.

---

# 30. Login UI

Login mengikuti design system yang sudah ditetapkan:

```text
DM Sans
Neutral
Modern
Clean
Minimal
Responsive
```

Tidak menggunakan:

* neon berlebihan
* gradient berlebihan
* glassmorphism berat
* animasi berlebihan
* Unicode emoji

Icon menggunakan SVG.

---

# 31. Login Loading State

Saat login:

```text
Normal
 ↓
Loading
 ↓
Success / Error
```

Button dapat berubah:

```text
Sign In
```

menjadi:

```text
Signing in...
```

Button harus disabled sementara request berlangsung untuk mencegah double submit.

---

# 32. Login Error State

Jika gagal:

```text
Invalid username/email or password.
```

UI tidak boleh menampilkan traceback.

Tidak:

```text
mysql.connector.errors...
```

Tidak:

```text
User ID 5 doesn't exist
```

---

# 33. Authorization Error Page

403 page:

```text
Access Restricted

You do not have permission to access this page.

[Back to Dashboard]
```

Tetap menggunakan:

* DM Sans
* SVG
* theme
* responsive layout

---

# 34. Authentication API Status Codes

| Kondisi             | HTTP |
| ------------------- | ---: |
| Login success       |  200 |
| Invalid credentials |  401 |
| Not authenticated   |  401 |
| Forbidden role      |  403 |
| User not found      |  404 |
| Validation error    |  422 |
| Database failure    |  500 |

---

# 35. Security Logging

Log yang boleh dicatat:

```text
Login success
Login failed
Logout
Unauthorized access
Forbidden access
Password change success/failure
```

Jangan log:

```text
Password
Password hash
Session secret
Database password
```

---

# 36. Authentication Testing

### Login

```text
[ ] Valid username + password
[ ] Valid email + password
[ ] Invalid password
[ ] Invalid username
[ ] Empty username
[ ] Empty password
```

### Session

```text
[ ] Session dibuat
[ ] Dashboard dapat diakses
[ ] Session tidak menyimpan password
[ ] Logout menghapus session
```

### Authorization

```text
[ ] Admin dapat melakukan admin action
[ ] Analyst tidak dapat melakukan admin action
[ ] Analyst mendapat 403
```

### API

```text
[ ] Protected API tanpa login → 401
[ ] Protected API dengan role salah → 403
[ ] Authenticated API → berhasil
```

---

# 37. Security Testing

Pastikan:

```text
[ ] Password tidak plaintext
[ ] Password hash tidak dikirim ke frontend
[ ] SQL menggunakan parameter
[ ] Session tidak menyimpan password
[ ] Credential tidak hardcoded
[ ] CSRF diterapkan pada state-changing request
[ ] Unauthorized request ditolak
[ ] Forbidden request ditolak
[ ] Error tidak membocorkan traceback
```

---

# 38. Authentication Definition of Done

Tahap Authentication selesai apabila:

* [ ] Login tersedia.
* [ ] Logout tersedia.
* [ ] Password hashing tersedia.
* [ ] Password verification tersedia.
* [ ] Session tersedia.
* [ ] Session hanya menyimpan data minimum.
* [ ] `login_required` tersedia.
* [ ] `role_required` tersedia.
* [ ] Admin role tersedia.
* [ ] Analyst role tersedia.
* [ ] `/api/auth/me` tersedia.
* [ ] Protected routes tersedia.
* [ ] Protected API tersedia.
* [ ] Backend authorization tersedia.
* [ ] 401 tersedia.
* [ ] 403 tersedia.
* [ ] CSRF protection tersedia.
* [ ] Session security dikonfigurasi.
* [ ] Profile tersedia.
* [ ] Change password tersedia jika diaktifkan.
* [ ] Authentication testing selesai.
* [ ] Tidak ada plaintext password.
* [ ] Tidak ada credential sensitif di frontend.

---

