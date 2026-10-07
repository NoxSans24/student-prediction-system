# `BACKEND_IMPLEMENTATION_SPEC.md`

Dokumen ini menerjemahkan `SYSTEM_ARCHITECTURE.md`, `API_SPECIFICATION.md`, `DATABASE_IMPLEMENTATION_SPEC.md`, dan spesifikasi fitur sebelumnya menjadi struktur backend Flask yang konkret.

Prinsip utama:

```text
Frontend
   ↓
Routes / API
   ↓
Services
   ↓
Database / ML / Data Processing
```

Route **tidak** menjadi tempat business logic utama.

---

# 1. Backend Stack

Backend:

```text
Python
Flask
MySQL
Pandas
NumPy
Scikit-learn
ReportLab
openpyxl
```

Struktur:

```text
student-performance-analytics/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── config/
│   └── settings.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── students.py
│   ├── analytics.py
│   ├── prediction.py
│   ├── risk.py
│   ├── dataset.py
│   └── reports.py
│
├── services/
│   ├── auth_service.py
│   ├── analytics_service.py
│   ├── insight_service.py
│   ├── risk_service.py
│   ├── prediction_service.py
│   ├── data_cleaning_service.py
│   └── report_service.py
│
├── database/
│   ├── connection.py
│   └── schema.sql
│
└── ml/
    ├── preprocessing.py
    ├── train.py
    ├── evaluate.py
    ├── predict.py
    └── models/
```

---

# 2. `app.py`

`app.py` menjadi application entry point.

Tanggung jawab:

```text
Create Flask app
        ↓
Load configuration
        ↓
Register blueprints
        ↓
Register error handlers
        ↓
Start application
```

Tidak menaruh:

```text
SQL query
ML training
Risk calculation
Data cleaning
```

di `app.py`.

---

# 3. Application Factory

Struktur yang direkomendasikan:

```python
def create_app():
    app = Flask(__name__)

    # configuration
    # extensions
    # blueprints
    # error handlers

    return app
```

Kemudian:

```python
app = create_app()
```

Keuntungannya adalah struktur aplikasi lebih mudah dikembangkan dan dites.

---

# 4. `config.py`

Berisi konfigurasi environment.

Contoh:

```text
SECRET_KEY
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
UPLOAD_FOLDER
MAX_CONTENT_LENGTH
```

Nilai sensitif berasal dari `.env`.

---

# 5. Environment Configuration

Contoh:

```env
SECRET_KEY=your-secret-key

DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_performance_analytics
DB_USER=root
DB_PASSWORD=

UPLOAD_FOLDER=data/raw
```

`.env`:

```gitignore
.env
```

---

# 6. `requirements.txt`

Dependensi utama:

```text
Flask
python-dotenv
mysql-connector-python
pandas
numpy
scikit-learn
matplotlib
seaborn
reportlab
openpyxl
joblib
```

Versi dependency dapat dikunci ketika implementasi final dilakukan.

---

# 7. Blueprint Architecture

Setiap domain mempunyai blueprint sendiri:

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

Contoh:

```text
/auth
/dashboard
/students
/analytics
/prediction
/risk
/dataset
/reports
```

---

# 8. Route Responsibility

Route hanya menangani:

```text
Request
↓
Authentication
↓
Validation dasar
↓
Service call
↓
Response
```

Contoh:

```python
@students_bp.get("/")
@login_required
def get_students():
    result = student_service.get_students(...)
    return jsonify(result)
```

Bukan:

```python
@students_bp.get("/")
def get_students():
    # 100 lines SQL
    # filtering
    # calculations
    # risk calculation
```

---

# 9. Service Responsibility

Service menjadi pusat business logic.

Contoh:

```text
students.py
     ↓
student_service
     ↓
database
```

Untuk project ini service yang sudah ditentukan:

```text
auth_service.py
analytics_service.py
insight_service.py
risk_service.py
prediction_service.py
data_cleaning_service.py
report_service.py
```

Jika student CRUD semakin kompleks, `student_service.py` dapat ditambahkan.

---

# 10. Database Layer

File:

```text
database/connection.py
```

Tanggung jawab:

```text
Create connection
Execute query
Return result
Commit
Rollback
Close connection
```

Service tidak perlu mengetahui detail konfigurasi database.

---

# 11. Request Flow

Contoh:

```text
GET /api/students
        ↓
routes/students.py
        ↓
authentication
        ↓
student service
        ↓
database connection
        ↓
MySQL
        ↓
service
        ↓
JSON response
```

---

# 12. Authentication Flow

Login:

```text
POST /login
       ↓
auth.py
       ↓
auth_service.py
       ↓
users table
       ↓
verify password hash
       ↓
create session
       ↓
Dashboard
```

---

# 13. Session Data

Session hanya menyimpan informasi minimum:

```python
session["user_id"]
session["username"]
session["role"]
```

Tidak boleh:

```python
session["password"]
session["password_hash"]
```

---

# 14. Authentication Decorator

Minimal terdapat:

```text
@login_required
@role_required("admin")
@roles_required("admin", "analyst")
```

Contoh:

```python
@students_bp.post("/")
@login_required
@role_required("admin")
def create_student():
    ...
```

---

# 15. Authorization

Frontend boleh menyembunyikan tombol:

```text
[ Delete ]
```

untuk Analyst.

Tetapi backend tetap wajib melakukan:

```text
Analyst
 ↓
POST /api/students
 ↓
403 Forbidden
```

Jadi security tidak bergantung pada frontend.

---

# 16. HTTP Status Rules

| Status | Penggunaan               |
| ------ | ------------------------ |
| 200    | Success                  |
| 201    | Created                  |
| 400    | Bad request              |
| 401    | Not authenticated        |
| 403    | Not authorized           |
| 404    | Resource tidak ditemukan |
| 409    | Conflict                 |
| 422    | Validation error         |
| 500    | Server error             |

---

# 17. API Response Format

Success:

```json
{
  "success": true,
  "data": {}
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid GPA value."
  }
}
```

Frontend tidak perlu menebak struktur response.

---

# 18. Global Error Handling

Backend menyediakan handler untuk:

```text
400
401
403
404
422
500
```

Contoh error 404:

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Student not found."
  }
}
```

Error internal tidak membocorkan traceback ke user.

---

# 19. Authentication API

### Login

```http
POST /login
```

Input:

```json
{
  "username": "admin",
  "password": "..."
}
```

Success:

```json
{
  "success": true,
  "data": {
    "user": {
      "username": "admin",
      "role": "admin"
    }
  }
}
```

---

# 20. Logout

```http
POST /logout
```

Action:

```text
Clear session
↓
Return success
```

---

# 21. Current User

```http
GET /api/auth/me
```

Response:

```json
{
  "success": true,
  "data": {
    "username": "admin",
    "role": "admin"
  }
}
```

Password tidak pernah dikirim.

---

# 22. Dashboard API

```http
GET /api/dashboard
```

Data minimal:

```text
total_students
average_gpa
average_attendance
at_risk
gpa_trend
performance_distribution
attendance_vs_gpa
gpa_by_major
insights
students_requiring_attention
```

Dashboard API menjadi aggregation layer.

---

# 23. Dashboard Service Flow

```text
/dashboard
      ↓
dashboard route
      ↓
dashboard service / aggregation
      ↓
analytics_service
risk_service
insight_service
      ↓
database
```

Jika implementasi membutuhkan `dashboard_service.py`, file tersebut dapat ditambahkan untuk menghindari route terlalu kompleks.

---

# 24. Student API

List:

```http
GET /api/students
```

Query:

```text
?page=1
&limit=10
&search=
&major=
&semester=
&risk=
```

---

# 25. Student Detail API

```http
GET /api/students/<student_id>
```

Mengembalikan:

```text
student information
current performance
academic records
risk
```

---

# 26. Student CRUD

Create:

```http
POST /api/students
```

Admin only.

Update:

```http
PUT /api/students/<student_id>
```

Admin only.

Delete:

```http
DELETE /api/students/<student_id>
```

Admin only.

---

# 27. Academic Records API

Get:

```http
GET /api/students/<student_id>/academic-records
```

Create:

```http
POST /api/students/<student_id>/academic-records
```

Create academic record hanya Admin.

Data:

```json
{
  "semester": 4,
  "gpa": 3.42,
  "attendance": 89,
  "assignment_score": 86,
  "midterm_score": 82,
  "final_score": 88,
  "study_hours": 12
}
```

---

# 28. Analytics API

Endpoint:

```text
GET /api/analytics/gpa-distribution
GET /api/analytics/gpa-semester
GET /api/analytics/gpa-major
GET /api/analytics/gpa-trend
GET /api/analytics/attendance-gpa
GET /api/analytics/study-hours-gpa
GET /api/analytics/assignment-gpa
GET /api/analytics/midterm-gpa
GET /api/analytics/final-gpa
GET /api/analytics/correlation
```

---

# 29. Analytics Filter

Endpoint dapat menerima:

```text
major
semester
gpa
attendance
risk
```

Contoh:

```http
GET /api/analytics/gpa-major?major=Informatics&semester=4
```

Analytics service mengolah filter sebelum melakukan aggregation.

---

# 30. Analytics Rule

Analytics hanya menggunakan data aktual.

Tidak boleh:

```python
return {
    "average_gpa": 3.42
}
```

secara hardcoded.

Harus:

```text
Database
 ↓
Query
 ↓
Pandas/aggregation jika diperlukan
 ↓
JSON
```

---

# 31. Insights API

```http
GET /api/insights
```

Flow:

```text
Analytics
   ↓
Insight Service
   ↓
Actual data
   ↓
Insight objects
```

Contoh:

```json
{
  "type": "gpa_trend",
  "priority": "medium",
  "title": "GPA Trend",
  "message": "...",
  "value": 3.25,
  "change": 0.15
}
```

---

# 32. Risk API

List risk:

```http
GET /api/risk
```

Student risk:

```http
GET /api/students/<student_id>/risk
```

Recalculate:

```http
POST /api/risk/recalculate
```

Recalculate merupakan operasi administratif/internal dan tidak boleh tersedia bebas untuk user biasa.

---

# 33. Risk Service Flow

```text
Student
 ↓
Get latest record
 ↓
Get previous record
 ↓
Calculate GPA change
 ↓
Calculate attendance change
 ↓
Calculate score trend
 ↓
Evaluate risk factors
 ↓
Calculate risk score
 ↓
Determine risk level
 ↓
Generate explanation
 ↓
Save assessment
```

---

# 34. Prediction API

```http
POST /api/prediction
```

Input:

```json
{
  "semester": 4,
  "attendance": 89,
  "assignment_score": 86,
  "midterm_score": 82,
  "final_score": 88,
  "study_hours": 12
}
```

---

# 35. Prediction Flow

```text
Request
 ↓
Validate input
 ↓
Check trained model
 ↓
Load model
 ↓
Preprocess input
 ↓
Predict GPA
 ↓
Determine performance category
 ↓
Get model metadata
 ↓
Save prediction history
 ↓
Return result
```

---

# 36. Prediction Error Cases

Backend harus menangani:

```text
MODEL_NOT_FOUND
INSUFFICIENT_DATA
VALIDATION_ERROR
PREDICTION_ERROR
```

Contoh:

```json
{
  "success": false,
  "error": {
    "code": "MODEL_NOT_FOUND",
    "message": "No trained model is available."
  }
}
```

---

# 37. ML Training API

```http
POST /api/ml/train
```

Admin only.

Flow:

```text
Request
 ↓
Authorization
 ↓
Load processed dataset
 ↓
Validate data
 ↓
Preprocess
 ↓
Train models
 ↓
Evaluate
 ↓
Compare
 ↓
Select best model
 ↓
Save model
 ↓
Save metadata
```

---

# 38. ML Models

Backend harus mencoba:

```text
LinearRegression
RandomForestRegressor
GradientBoostingRegressor
```

Metrik:

```text
MAE
RMSE
R²
```

Model terbaik ditentukan berdasarkan hasil aktual.

Tidak boleh menentukan:

```text
Random Forest selalu terbaik
```

sebelum training.

---

# 39. Dataset API

List:

```http
GET /api/datasets
```

Upload:

```http
POST /api/datasets/upload
```

Admin only.

Preview:

```http
GET /api/datasets/<dataset_id>/preview
```

Validation:

```http
GET /api/datasets/<dataset_id>/validation
```

---

# 40. Dataset Cleaning API

Preview:

```http
POST /api/datasets/<dataset_id>/clean/preview
```

Apply:

```http
POST /api/datasets/<dataset_id>/clean/apply
```

Keduanya untuk Admin.

Flow:

```text
Upload
 ↓
Validation
 ↓
Cleaning Preview
 ↓
User Confirmation
 ↓
Apply Cleaning
 ↓
Processed Dataset
```

---

# 41. Cleaning Preview

Preview harus memberi tahu user:

```text
Missing values
Duplicates
Invalid GPA
Invalid attendance
Invalid scores
Incorrect types
Potential outliers
```

Sebelum perubahan permanen diterapkan.

---

# 42. Cleaning Safety

Tidak boleh:

```text
Upload
 ↓
Automatic destructive cleaning
```

Lebih aman:

```text
Upload
 ↓
Analyze
 ↓
Preview
 ↓
Confirm
 ↓
Apply
```

Raw file tetap dipertahankan.

---

# 43. Report API

Overall:

```http
GET /api/reports/overall
```

Student:

```http
GET /api/reports/student/<student_id>
```

Risk:

```http
GET /api/reports/risk
```

ML:

```http
GET /api/reports/ml
```

---

# 44. Report Export

Format:

```text
PDF
Excel
CSV
```

Endpoint:

```text
GET /api/reports/<report_type>/export/pdf
GET /api/reports/<report_type>/export/excel
GET /api/reports/<report_type>/export/csv
```

Report service yang menangani pembuatan file.

---

# 45. Service Dependency

```text
auth_service
      ↓
users / session


analytics_service
      ↓
academic_records
students


risk_service
      ↓
students
academic_records
risk_assessments


prediction_service
      ↓
ML model
prediction_results


data_cleaning_service
      ↓
Pandas
CSV
datasets
dataset_cleaning_logs


report_service
      ↓
analytics
risk
ML
database
```

---

# 46. ML Layer

Struktur:

```text
ml/
├── preprocessing.py
├── train.py
├── evaluate.py
├── predict.py
└── models/
```

### `preprocessing.py`

Menangani:

```text
Feature preparation
Data cleaning prerequisites
Train/test preparation
```

### `train.py`

Menangani:

```text
Model training
```

### `evaluate.py`

Menangani:

```text
MAE
RMSE
R²
```

### `predict.py`

Menangani:

```text
Load model
Predict
```

---

# 47. Service vs ML Boundary

`prediction_service.py`:

```text
Application/business flow
```

`ml/predict.py`:

```text
Machine learning operation
```

Jadi:

```text
Prediction Route
      ↓
Prediction Service
      ↓
ML Predict
      ↓
Model
```

---

# 48. File Storage

Model:

```text
ml/models/
```

Dataset:

```text
data/raw/
data/processed/
```

Report:

```text
data/reports/
```

Jangan mencampur ketiganya.

---

# 49. File Naming

Model:

```text
best_model.joblib
model_metadata.json
```

Dataset:

```text
original_dataset.csv
cleaned_dataset.csv
```

Report:

```text
overall-performance-report-YYYY-MM-DD.pdf
student-report-STUDENTID-YYYY-MM-DD.pdf
risk-report-YYYY-MM-DD.xlsx
ml-report-YYYY-MM-DD.pdf
```

---

# 50. Validation Layers

Input harus melewati beberapa lapisan:

```text
Frontend Validation
        ↓
API Validation
        ↓
Service Validation
        ↓
Database Constraint
```

Frontend validation meningkatkan UX.

Backend validation tetap menjadi sumber kebenaran.

---

# 51. Example Student Creation Flow

```text
Admin
 ↓
POST /api/students
 ↓
Authentication
 ↓
Authorization
 ↓
Validate payload
 ↓
Check duplicate student_id
 ↓
Insert database
 ↓
Return 201
```

Jika duplicate:

```text
409 DUPLICATE_STUDENT
```

---

# 52. Example Student Delete Flow

```text
Admin
 ↓
DELETE /api/students/20240001
 ↓
Authorization
 ↓
Find student
 ↓
Confirmation already handled by frontend
 ↓
Delete
 ↓
Database CASCADE
 ↓
Return success
```

Backend tidak boleh menganggap frontend confirmation sebagai security mechanism.

---

# 53. Logging

Backend perlu mencatat error penting:

```text
Database error
File processing error
ML training error
Prediction error
Report generation error
Authentication failure
```

Tetapi response kepada user tetap aman.

---

# 54. Security Rules

Backend wajib:

```text
□ Password hashing
□ Session authentication
□ Role authorization
□ CSRF protection untuk form/action yang relevan
□ Parameterized SQL
□ File type validation
□ File size validation
□ Secure environment variables
□ Tidak expose traceback
□ Tidak expose password
```

---

# 55. File Upload Security

Dataset upload harus memvalidasi:

```text
Extension
MIME/type jika memungkinkan
File size
CSV readability
Required columns
```

File yang tidak valid:

```text
INVALID_DATASET
```

---

# 56. Backend Error Codes

Kode utama:

```text
UNAUTHORIZED
FORBIDDEN
NOT_FOUND
VALIDATION_ERROR
INVALID_CREDENTIALS
DUPLICATE_STUDENT
INVALID_DATASET
UNCLEAN_DATASET
MODEL_NOT_FOUND
INSUFFICIENT_DATA
PREDICTION_ERROR
DATABASE_ERROR
REPORT_GENERATION_ERROR
```

Kode dibuat konsisten di seluruh endpoint.

---

# 57. Thin Route Principle

Contoh ideal:

```python
@prediction_bp.post("/")
@login_required
def predict():
    payload = request.get_json()

    result = prediction_service.predict(payload)

    return jsonify({
        "success": True,
        "data": result
    })
```

Route tidak menghitung GPA prediction sendiri.

---

# 58. Backend Architecture Final

```text
                         Flask App
                             │
                       ┌─────┴─────┐
                       │           │
                    Routes      Error Handler
                       │
             ┌─────────┼─────────┐
             │         │         │
          Auth      Services     API
                       │
       ┌───────────────┼────────────────┐
       │               │                │
   Analytics          Risk           Prediction
       │               │                │
       └───────────────┼────────────────┘
                       │
              ┌────────┴────────┐
              │                 │
          Database              ML
              │                 │
            MySQL          Scikit-learn
```

---

# 59. Backend Development Order

Jangan langsung membuat seluruh endpoint sekaligus.

Urutan implementasi:

```text
1. Flask Foundation
       ↓
2. Configuration
       ↓
3. Database Connection
       ↓
4. Authentication
       ↓
5. Student CRUD
       ↓
6. Academic Records
       ↓
7. Dataset Management
       ↓
8. Data Cleaning
       ↓
9. Analytics
       ↓
10. Risk Engine
       ↓
11. ML Training
       ↓
12. Prediction
       ↓
13. Insights
       ↓
14. Dashboard Aggregation
       ↓
15. Reports
       ↓
16. Testing
```

Urutan ini mengikuti dependency antar fitur, bukan urutan sidebar.

---

# 60. Backend Definition of Done

Backend dianggap siap memasuki tahap frontend integration ketika:

```text
□ Flask application berjalan
□ Environment configuration bekerja
□ MySQL connection bekerja
□ Schema berhasil dibuat
□ Login/logout bekerja
□ Session bekerja
□ Role authorization bekerja
□ Student CRUD bekerja
□ Academic records bekerja
□ Dataset upload bekerja
□ Dataset validation bekerja
□ Cleaning preview bekerja
□ Cleaning apply bekerja
□ Analytics API bekerja
□ Risk Engine bekerja
□ ML training bekerja
□ Prediction bekerja
□ Insights API bekerja
□ Dashboard API bekerja
□ Reports bekerja
□ Error response konsisten
□ Security dasar diterapkan
```

---

