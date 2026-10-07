# `API_SPECIFICATION.md`

Dokumen ini menjadi jembatan antara **System Architecture** dan tahap coding. Semua endpoint mengikuti modul yang sudah ditentukan sebelumnya dan tidak menambahkan fitur bisnis baru di luar scope.

---

# 1. Tujuan API

API digunakan untuk menghubungkan:

```text
Frontend
   ↓
Flask Routes / API
   ↓
Services
   ↓
Database / ML
```

API bertanggung jawab untuk:

* mengambil data,
* menerima input,
* melakukan validasi,
* menjalankan service,
* mengembalikan hasil,
* menangani error.

Business logic tetap berada di `services/`.

---

# 2. API Convention

Base URL:

```text
/api
```

Format response:

```json
{
  "success": true,
  "data": {}
}
```

Untuk error:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

JSON digunakan untuk endpoint yang dikonsumsi JavaScript.

---

# 3. Authentication API

## Login

```http
POST /login
```

Request:

```json
{
  "username": "admin",
  "password": "password"
}
```

Success:

```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid username or password."
  }
}
```

Pesan login gagal dibuat generik agar tidak membocorkan apakah username atau password yang salah.

---

# 4. Logout

```http
POST /logout
```

Response:

```json
{
  "success": true,
  "message": "Logout successful."
}
```

Session harus dihapus setelah logout.

---

# 5. Current User

```http
GET /api/auth/me
```

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

Password tidak pernah dikirim melalui response.

---

# 6. Dashboard API

Dashboard membutuhkan beberapa data sekaligus.

Endpoint utama:

```http
GET /api/dashboard
```

Response konseptual:

```json
{
  "success": true,
  "data": {
    "kpi": {
      "total_students": 120,
      "average_gpa": 3.24,
      "average_attendance": 87.5,
      "at_risk_students": 18
    },
    "gpa_trend": [],
    "performance_distribution": [],
    "attendance_vs_gpa": [],
    "gpa_by_major": [],
    "insights": [],
    "students_requiring_attention": []
  }
}
```

Dashboard tidak menghitung sendiri data tersebut.

Data berasal dari:

```text
Analytics Service
Risk Service
Insight Service
```

---

# 7. Student API

## Get Students

```http
GET /api/students
```

Query:

```text
?page=1
&limit=10
&search=Muhammad
&major=Informatika
&semester=4
&risk=high
```

Contoh:

```http
GET /api/students?page=1&limit=10&search=Muhammad
```

Response:

```json
{
  "success": true,
  "data": {
    "students": [],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 120,
      "total_pages": 12
    }
  }
}
```

---

# 8. Student Detail

```http
GET /api/students/<student_id>
```

Response:

```json
{
  "success": true,
  "data": {
    "student": {
      "student_id": "20240001",
      "name": "Student Name",
      "major": "Informatics",
      "current_semester": 4
    },
    "current_performance": {},
    "academic_history": [],
    "risk": {},
    "early_warnings": []
  }
}
```

---

# 9. Create Student

**Admin only**

```http
POST /api/students
```

Request:

```json
{
  "student_id": "20240001",
  "name": "Student Name",
  "major": "Informatics",
  "current_semester": 1
}
```

Response:

```json
{
  "success": true,
  "message": "Student created successfully.",
  "data": {
    "id": 1
  }
}
```

---

# 10. Update Student

**Admin only**

```http
PUT /api/students/<student_id>
```

Request:

```json
{
  "name": "Updated Name",
  "major": "Informatics",
  "current_semester": 2
}
```

---

# 11. Delete Student

**Admin only**

```http
DELETE /api/students/<student_id>
```

Response:

```json
{
  "success": true,
  "message": "Student deleted successfully."
}
```

Frontend harus meminta confirmation sebelum melakukan operasi ini.

---

# 12. Academic Record API

Karena academic record merupakan bagian penting dari analytics, prediction, dan risk analysis:

## Get Academic History

```http
GET /api/students/<student_id>/academic-records
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "semester": 1,
      "gpa": 3.12,
      "attendance": 85,
      "assignment_score": 80,
      "midterm_score": 78,
      "final_score": 82,
      "study_hours": 5
    }
  ]
}
```

---

## Create Academic Record

**Admin only**

```http
POST /api/students/<student_id>/academic-records
```

Request:

```json
{
  "semester": 2,
  "gpa": 3.25,
  "attendance": 88,
  "assignment_score": 82,
  "midterm_score": 80,
  "final_score": 85,
  "study_hours": 6
}
```

Setelah data akademik berubah, sistem dapat memperbarui:

```text
Analytics
Risk Assessment
Dashboard
Insights
```

---

# 13. Analytics API

Analytics merupakan salah satu bagian utama sistem.

## GPA Distribution

```http
GET /api/analytics/gpa-distribution
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "category": "Excellent",
      "count": 25
    },
    {
      "category": "Good",
      "count": 50
    },
    {
      "category": "Average",
      "count": 35
    },
    {
      "category": "Poor",
      "count": 10
    }
  ]
}
```

Kategori dan hasil harus berasal dari data aktual.

---

# 14. GPA by Semester

```http
GET /api/analytics/gpa-semester
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "semester": 1,
      "average_gpa": 3.12
    },
    {
      "semester": 2,
      "average_gpa": 3.21
    }
  ]
}
```

---

# 15. GPA by Major

```http
GET /api/analytics/gpa-major
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "major": "Informatics",
      "average_gpa": 3.31
    },
    {
      "major": "Information Systems",
      "average_gpa": 3.18
    }
  ]
}
```

---

# 16. GPA Trend

```http
GET /api/analytics/gpa-trend
```

Karena GPA trend pada dasarnya merupakan perkembangan GPA antarsemester, response dapat menggunakan struktur semester + GPA.

```json
{
  "success": true,
  "data": [
    {
      "semester": 1,
      "average_gpa": 3.10
    },
    {
      "semester": 2,
      "average_gpa": 3.20
    },
    {
      "semester": 3,
      "average_gpa": 3.28
    }
  ]
}
```

---

# 17. Attendance vs GPA

```http
GET /api/analytics/attendance-gpa
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "student_id": "20240001",
      "name": "Student Name",
      "attendance": 92,
      "gpa": 3.60
    }
  ]
}
```

Digunakan untuk scatter plot.

---

# 18. Study Hours vs GPA

```http
GET /api/analytics/study-hours-gpa
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "student_id": "20240001",
      "study_hours": 6,
      "gpa": 3.42
    }
  ]
}
```

Hasil chart tidak boleh ditafsirkan sebagai hubungan sebab-akibat.

---

# 19. Score vs GPA

Endpoint:

```text
GET /api/analytics/assignment-gpa
GET /api/analytics/midterm-gpa
GET /api/analytics/final-gpa
```

Contoh:

```json
{
  "success": true,
  "data": [
    {
      "student_id": "20240001",
      "score": 85,
      "gpa": 3.45
    }
  ]
}
```

---

# 20. Correlation API

```http
GET /api/analytics/correlation
```

Response:

```json
{
  "success": true,
  "data": {
    "gpa": {
      "gpa": 1.0,
      "attendance": 0.62,
      "assignment_score": 0.58,
      "midterm_score": 0.71,
      "final_score": 0.76,
      "study_hours": 0.31
    }
  }
}
```

Nilai correlation harus dihitung dari dataset aktual.

---

# 21. Analytics Filters

Endpoint analytics dapat menerima filter:

```text
?major=Informatics
&semester=4
&min_gpa=2.5
&max_gpa=4
&min_attendance=75
&risk=high
```

Contoh:

```http
GET /api/analytics/gpa-major?semester=4&major=Informatics
```

Filter diterapkan sebelum analytics dihitung.

---

# 22. Insights API

```http
GET /api/insights
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "type": "gpa_trend",
      "priority": "medium",
      "title": "GPA Trend",
      "message": "Average GPA increased compared with the previous semester.",
      "value": 3.25,
      "change": 0.15
    }
  ]
}
```

Insight harus berasal dari:

```text
Analytics
+
Risk
+
Academic Data
```

---

# 23. Risk API

## Risk Overview

```http
GET /api/risk
```

Response:

```json
{
  "success": true,
  "data": {
    "low": 80,
    "medium": 25,
    "high": 15,
    "total": 120
  }
}
```

---

# 24. Student Risk

```http
GET /api/students/<student_id>/risk
```

Response:

```json
{
  "success": true,
  "data": {
    "risk_level": "high",
    "risk_score": 72.5,
    "factors": [
      "GPA decreased",
      "Attendance decreased",
      "Assessment performance decreased"
    ],
    "early_warnings": [
      "Significant GPA decline"
    ]
  }
}
```

Risk score dan threshold tidak boleh dianggap sebagai nilai final sebelum konfigurasi/testing ditentukan.

---

# 25. Recalculate Risk

Endpoint internal/admin:

```http
POST /api/risk/recalculate
```

Tujuan:

```text
Academic Data
     ↓
Risk Engine
     ↓
Recalculate
```

Response:

```json
{
  "success": true,
  "message": "Risk assessment recalculated successfully."
}
```

---

# 26. Prediction API

## Predict GPA

```http
POST /api/prediction
```

Request:

```json
{
  "semester": 4,
  "attendance": 88,
  "assignment_score": 85,
  "midterm_score": 82,
  "final_score": 86,
  "study_hours": 6
}
```

Response:

```json
{
  "success": true,
  "data": {
    "predicted_gpa": 3.41,
    "performance_category": "Good",
    "model_name": "RandomForestRegressor",
    "metrics": {
      "mae": 0.18,
      "rmse": 0.24,
      "r2": 0.82
    }
  }
}
```

Angka di atas hanya contoh struktur response, **bukan hasil model sebenarnya**.

---

# 27. Prediction History

```http
GET /api/predictions
```

Query:

```text
?page=1
&limit=10
&student_id=20240001
```

Response:

```json
{
  "success": true,
  "data": {
    "predictions": [],
    "pagination": {}
  }
}
```

---

# 28. ML Training API

**Admin only**

```http
POST /api/ml/train
```

Flow:

```text
Request
 ↓
Check Admin
 ↓
Check Dataset
 ↓
Preprocessing
 ↓
Train Models
 ↓
Evaluate
 ↓
Select Best
 ↓
Save Model
```

Response konseptual:

```json
{
  "success": true,
  "data": {
    "best_model": "RandomForestRegressor",
    "models": [
      {
        "name": "LinearRegression",
        "mae": 0.21,
        "rmse": 0.29,
        "r2": 0.78
      }
    ]
  }
}
```

Hasil aktual akan bergantung pada dataset.

---

# 29. Dataset API

## Dataset List

```http
GET /api/datasets
```

Response:

```json
{
  "success": true,
  "data": []
}
```

---

# 30. Upload Dataset

**Admin only**

```http
POST /api/datasets/upload
```

Content type:

```text
multipart/form-data
```

Field:

```text
file
```

Flow:

```text
Upload
 ↓
File Validation
 ↓
Read CSV
 ↓
Validate Columns
 ↓
Analyze Dataset
 ↓
Save Metadata
```

---

# 31. Dataset Preview

```http
GET /api/datasets/<dataset_id>/preview
```

Response:

```json
{
  "success": true,
  "data": {
    "columns": [],
    "rows": [],
    "total_rows": 1000,
    "total_columns": 10
  }
}
```

---

# 32. Dataset Validation

```http
GET /api/datasets/<dataset_id>/validation
```

Response:

```json
{
  "success": true,
  "data": {
    "missing_values": 12,
    "duplicates": 4,
    "invalid_gpa": 2,
    "invalid_attendance": 1,
    "invalid_scores": 3,
    "incorrect_data_types": 0,
    "outliers": 8
  }
}
```

---

# 33. Cleaning Preview

**Admin only**

```http
POST /api/datasets/<dataset_id>/clean/preview
```

Request:

```json
{
  "missing_value_action": "impute",
  "duplicate_action": "remove",
  "invalid_value_action": "remove",
  "outlier_action": "flag"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "original_rows": 1000,
    "rows_to_remove": 8,
    "missing_values_handled": 12,
    "duplicates_removed": 4,
    "outliers_flagged": 8
  }
}
```

---

# 34. Apply Cleaning

**Admin only**

```http
POST /api/datasets/<dataset_id>/clean/apply
```

Frontend harus meminta confirmation sebelum menjalankan action ini.

Response:

```json
{
  "success": true,
  "message": "Dataset cleaning applied successfully."
}
```

Raw dataset tidak boleh ditimpa.

---

# 35. Reports API

## Overall Report

```http
GET /api/reports/overall
```

Filter:

```text
?major=Informatics
&semester=4
```

---

## Student Report

```http
GET /api/reports/student/<student_id>
```

---

## Risk Report

```http
GET /api/reports/risk
```

Filter:

```text
?risk=high
&major=Informatics
&semester=4
```

---

## ML Report

```http
GET /api/reports/ml
```

Berisi:

```text
Dataset
Features
Target
Train/Test
Model Comparison
Best Model
MAE
RMSE
R²
```

---

# 36. Report Export API

### PDF

```http
GET /api/reports/<report_type>/export/pdf
```

### Excel

```http
GET /api/reports/<report_type>/export/excel
```

### CSV

```http
GET /api/reports/<report_type>/export/csv
```

Contoh:

```http
GET /api/reports/risk/export/excel
```

---

# 37. HTTP Status Codes

Gunakan status code secara konsisten.

| Status | Penggunaan                |
| ------ | ------------------------- |
| `200`  | Request berhasil          |
| `201`  | Data berhasil dibuat      |
| `400`  | Input tidak valid         |
| `401`  | Belum login               |
| `403`  | Tidak memiliki permission |
| `404`  | Data tidak ditemukan      |
| `409`  | Conflict/duplicate        |
| `422`  | Validation error          |
| `500`  | Internal server error     |

---

# 38. Standard Error Codes

Beberapa error code yang digunakan:

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

---

# 39. API Permission Matrix

| Endpoint          | Admin | Analyst |
| ----------------- | :---: | :-----: |
| Dashboard         |   ✓   |    ✓    |
| View Students     |   ✓   |    ✓    |
| Create Student    |   ✓   |    —    |
| Update Student    |   ✓   |    —    |
| Delete Student    |   ✓   |    —    |
| Analytics         |   ✓   |    ✓    |
| Prediction        |   ✓   |    ✓    |
| Risk              |   ✓   |    ✓    |
| Dataset View      |   ✓   |    ✓    |
| Dataset Upload    |   ✓   |    —    |
| Dataset Cleaning  |   ✓   |    —    |
| ML Training       |   ✓   |    —    |
| Reports           |   ✓   |    ✓    |
| Personal Settings |   ✓   |    ✓    |
| System Settings   |   ✓   |    —    |

Backend harus menjadi sumber kebenaran permission.

---

# 40. API → Service Mapping

| API Module  | Service                    |
| ----------- | -------------------------- |
| Auth        | `auth_service.py`          |
| Dashboard   | Analytics + Risk + Insight |
| Students    | Student logic / database   |
| Analytics   | `analytics_service.py`     |
| Insights    | `insight_service.py`       |
| Risk        | `risk_service.py`          |
| Prediction  | `prediction_service.py`    |
| Dataset     | `data_cleaning_service.py` |
| Reports     | `report_service.py`        |
| ML Training | `ml/train.py`              |

---

# 41. API → Database Mapping

```text
users
 ↓
Authentication

students
 ↓
Student Management

academic_records
 ↓
Analytics
 ↓
Risk
 ↓
ML

risk_assessments
 ↓
Risk Dashboard

prediction_results
 ↓
Prediction History

datasets
 ↓
Dataset Management

dataset_cleaning_logs
 ↓
Cleaning History
```

---

# 42. Prinsip API

API harus mengikuti prinsip:

```text
Thin Routes
      ↓
Strong Services
      ↓
Clean Data Layer
```

Artinya route jangan berisi kode panjang seperti:

```python
@app.route(...)
def analytics():
    # 100 baris SQL
    # 50 baris pandas
    # 30 baris calculation
    # 20 baris formatting
```

Lebih baik:

```python
@app.route("/api/analytics/gpa-trend")
@login_required
def gpa_trend():
    data = analytics_service.get_gpa_trend()
    return jsonify({
        "success": True,
        "data": data
    })
```

Kemudian perhitungannya berada di:

```text
services/analytics_service.py
```

---

# 43. API Flow Final

```text
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │ HTTP
       ▼
┌──────────────┐
│ Flask Route  │
└──────┬───────┘
       │
       ├── Authentication
       │
       ├── Authorization
       │
       ├── Validation
       │
       ▼
┌──────────────┐
│   Service    │
└──────┬───────┘
       │
       ├─────────────┐
       ▼             ▼
┌────────────┐ ┌─────────────┐
│  Database  │ │ ML Pipeline │
└─────┬──────┘ └──────┬──────┘
      │               │
      └───────┬───────┘
              ▼
        Service Result
              ↓
        JSON Response
              ↓
           Browser
```

