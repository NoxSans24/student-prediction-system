# ML_PREDICTION_IMPLEMENTATION_SPEC.md

## 1. Tujuan

Tahap ini mengimplementasikan **Machine Learning Engine** dan fitur **GPA Prediction**.

Tujuan utamanya:

* preprocessing data
* training model
* membandingkan beberapa model regresi
* evaluasi model
* memilih model terbaik berdasarkan hasil aktual
* menyimpan model
* melakukan prediksi GPA
* menyimpan prediction history
* menyediakan halaman Prediction
* menyediakan API prediction
* menangani kondisi ketika model belum tersedia atau dataset belum siap

Pipeline:

```text
Processed Dataset
       ↓
Preprocessing
       ↓
Feature Selection
       ↓
Train / Test Split
       ↓
┌─────────────────────────────┐
│ Linear Regression           │
│ Random Forest Regressor     │
│ Gradient Boosting Regressor │
└──────────────┬──────────────┘
               ↓
          Evaluation
               ↓
        MAE / RMSE / R²
               ↓
          Best Model
               ↓
       Model Persistence
               ↓
          Prediction
               ↓
     Prediction History
```

---

# 2. Scope

Tahap ini mencakup:

### Machine Learning

* dataset preparation
* feature selection
* preprocessing
* train/test split
* Linear Regression
* Random Forest Regressor
* Gradient Boosting Regressor
* MAE
* RMSE
* R²
* model comparison
* best model selection
* model persistence
* training metadata

### GPA Prediction

* prediction form
* input validation
* model loading
* GPA prediction
* performance category
* model information
* model metrics
* prediction history

---

# 3. Struktur File

Tambahkan:

```text
ml/
├── __init__.py
├── preprocessing.py
├── train.py
├── evaluate.py
├── predict.py
└── models/
    ├── best_model.joblib
    └── metadata.json

services/
├── prediction_service.py
└── ...

routes/
├── prediction.py
└── ...

templates/
└── prediction/
    └── index.html

static/
├── css/
│   └── pages/
│       └── prediction.css
│
└── js/
    └── pages/
        └── prediction.js
```

---

# 4. ML Target

Target:

```text id="8gq6d1"
gpa
```

Model harus memprediksi:

```text
Predicted GPA
```

Problem type:

```text
Regression
```

Karena GPA merupakan nilai numerik kontinu.

---

# 5. ML Features

Features MVP:

```text id="f0h3g5"
semester
attendance
assignment_score
midterm_score
final_score
study_hours
```

Model tidak menggunakan:

```text id="u4a8p6"
student_id
name
major
```

sebagai feature ML MVP.

Alasannya:

* student ID merupakan identifier
* name merupakan identifier
* major belum ditetapkan sebagai feature dalam ML MVP

---

# 6. Dataset ML

Dataset training harus berasal dari data yang sudah diproses.

```text id="0m2f8y"
Raw Dataset
    ↓
Validation
    ↓
Cleaning
    ↓
Processed Dataset
    ↓
ML Training
```

Dataset yang belum melalui pipeline cleaning tidak boleh langsung digunakan untuk training.

---

# 7. Feature Matrix

`X`:

```text id="8zj5u4"
semester
attendance
assignment_score
midterm_score
final_score
study_hours
```

Target `y`:

```text id="m6z4h7"
gpa
```

Secara konsep:

```python id="y4km0m"
X = df[
    [
        "semester",
        "attendance",
        "assignment_score",
        "midterm_score",
        "final_score",
        "study_hours"
    ]
]

y = df["gpa"]
```

---

# 8. Preprocessing

File:

```text id="v2g8c3"
ml/preprocessing.py
```

Tanggung jawab:

* memilih feature
* memilih target
* validasi data
* menangani missing values
* memastikan numeric type
* menyiapkan pipeline

Fungsi yang disarankan:

```python id="p7w4t1"
load_processed_dataset()
validate_ml_dataset()
prepare_features()
prepare_target()
build_preprocessor()
```

---

# 9. Data Validation Sebelum Training

Sebelum training, sistem harus memastikan:

* feature tersedia
* target tersedia
* data tidak kosong
* numeric data valid
* missing value sudah ditangani
* dataset cukup untuk training

Jika tidak:

```text id="4zj7k2"
INSUFFICIENT_DATA
```

---

# 10. Train/Test Split

Initial configuration:

```text id="i5x0w8"
Training = 80%
Testing = 20%
```

Gunakan:

```python id="3y6n4a"
train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
```

`random_state=42` merupakan keputusan implementasi agar hasil split dapat direproduksi.

---

# 11. Model 1 — Linear Regression

Model baseline:

```python id="e5j2n9"
LinearRegression()
```

Tujuannya:

* baseline model
* sederhana
* mudah dibandingkan
* memberikan titik referensi awal

---

# 12. Model 2 — Random Forest

Model:

```python id="9k5wq1"
RandomForestRegressor()
```

Random Forest dapat menangkap hubungan non-linear yang lebih kompleks dibandingkan Linear Regression.

Parameter final sebaiknya ditentukan melalui pengujian dataset, bukan diasumsikan dari awal.

---

# 13. Model 3 — Gradient Boosting

Model:

```python id="7s4qv0"
GradientBoostingRegressor()
```

Model digunakan sebagai kandidat ketiga untuk dibandingkan dengan:

```text
Linear Regression
Random Forest
Gradient Boosting
```

---

# 14. Model Comparison

Semua model harus dilatih menggunakan split yang sama.

```text id="z2p6w8"
Dataset
   ↓
Same Train/Test Split
   ├── Linear Regression
   ├── Random Forest
   └── Gradient Boosting
```

Tujuannya membuat perbandingan lebih konsisten.

---

# 15. Evaluation Metrics

Gunakan:

### MAE

```text id="z2y7h4"
Mean Absolute Error
```

Semakin rendah semakin baik.

---

### RMSE

```text id="q4v5w7"
Root Mean Squared Error
```

Semakin rendah semakin baik.

---

### R²

```text id="j1r6v9"
R² Score
```

Semakin tinggi semakin baik.

---

# 16. Evaluation Service

File:

```text id="t6k8z0"
ml/evaluate.py
```

Fungsi:

```python id="3r2n8v"
calculate_mae()
calculate_rmse()
calculate_r2()
evaluate_model()
compare_models()
```

Contoh struktur hasil:

```json id="j8x4d2"
{
    "model": "Random Forest",
    "mae": 0.18,
    "rmse": 0.24,
    "r2": 0.82
}
```

Angka tersebut hanya contoh struktur.

---

# 17. Best Model Selection

Model terbaik **tidak boleh ditentukan secara hardcoded**.

Hasil aktual digunakan:

```text id="4v8k2q"
MAE  ↓
RMSE ↓
R²   ↑
```

Pemilihan model harus menggunakan aturan evaluasi yang konsisten.

Untuk MVP, primary selection metric dapat ditetapkan sebagai:

```text
RMSE
```

dengan nilai lebih rendah lebih baik.

MAE dan R² tetap ditampilkan untuk konteks evaluasi.

Jika keputusan metric utama ingin diubah, letakkan di configuration.

---

# 18. Training Result

Training menghasilkan:

```text id="m7c4x2"
Model
MAE
RMSE
R²
Training Rows
Testing Rows
Features
Target
Trained At
```

Contoh:

```text
Linear Regression
MAE   0.21
RMSE  0.28
R²    0.76
```

Semua angka berasal dari hasil training aktual.

---

# 19. Model Metadata

Simpan metadata bersama model.

Contoh:

```json id="h8p3w5"
{
    "model_name": "Random Forest Regressor",
    "target": "gpa",
    "features": [
        "semester",
        "attendance",
        "assignment_score",
        "midterm_score",
        "final_score",
        "study_hours"
    ],
    "mae": 0.18,
    "rmse": 0.24,
    "r2": 0.82,
    "train_size": 1000,
    "test_size": 250,
    "trained_at": "2026-10-07T12:00:00"
}
```

Tanggal di atas hanya contoh.

---

# 20. Model Persistence

Gunakan:

```text id="3u5q9r"
joblib
```

Contoh file:

```text id="y7c4x1"
ml/models/best_model.joblib
```

Metadata:

```text id="s5k8m2"
ml/models/metadata.json
```

Model harus dapat dimuat kembali tanpa melakukan training ulang setiap prediction.

---

# 21. Model Versioning

Untuk MVP:

```text id="h7f2s5"
best_model.joblib
metadata.json
```

sudah cukup.

Namun metadata sebaiknya memiliki:

```text
trained_at
model_name
features
metrics
dataset information
```

sehingga model yang digunakan dapat diketahui.

Versioning model yang lebih kompleks dapat ditambahkan kemudian.

---

# 22. Training Script

File:

```text id="p4m7x9"
ml/train.py
```

Flow:

```text id="g3c8w1"
Load Dataset
     ↓
Validate
     ↓
Prepare X / y
     ↓
Split
     ↓
Train 3 Models
     ↓
Evaluate
     ↓
Compare
     ↓
Select Best
     ↓
Save Model
     ↓
Save Metadata
```

---

# 23. ML Training Permission

Training model hanya boleh dilakukan:

```text id="4u8m2a"
Admin
```

Analyst:

```text
Tidak dapat training
```

Backend harus melakukan authorization.

---

# 24. ML Training API

Endpoint:

```text id="m8j5x2"
POST /api/ml/train
```

Permission:

```text
Admin only
```

Response:

```json id="r5x8c1"
{
    "success": true,
    "data": {
        "best_model": "Random Forest Regressor",
        "metrics": {
            "mae": 0.18,
            "rmse": 0.24,
            "r2": 0.82
        }
    }
}
```

---

# 25. Training Confirmation

Training merupakan proses yang dapat memakan waktu.

Sebelum training:

```text id="q1m7z8"
Train Machine Learning Model?

The current model will be replaced
if a new model is successfully trained.
```

Button:

```text
Cancel
Train Model
```

---

# 26. Training State

Frontend harus memiliki:

```text id="f4x7q1"
Idle
↓
Training
↓
Success / Error
```

Saat training:

```text
Training model...
```

Button training harus disabled untuk mencegah request ganda.

---

# 27. Training Failure

Jika training gagal:

```text id="5k7q3m"
MODEL_TRAINING_ERROR
```

Pesan user:

```text
Unable to train the model.
Please check the dataset and try again.
```

Jangan menampilkan stack trace kepada user.

---

# 28. Prediction Service

File:

```text id="v9k3w6"
services/prediction_service.py
```

Fungsi:

```python id="6q4m8r"
load_best_model()
get_model_metadata()
validate_prediction_input()
predict_gpa()
categorize_performance()
save_prediction()
get_prediction_history()
```

---

# 29. Prediction Input

Form:

```text id="x8q2n7"
Semester
Attendance
Assignment Score
Midterm Score
Final Score
Study Hours
```

Input harus sama dengan feature training.

```text
Training Features
        =
Prediction Features
```

Jangan sampai training menggunakan 6 feature tetapi prediction hanya mengirim 5.

---

# 30. Prediction Validation

### Semester

```text id="5f8k2w"
>= 1
```

### Attendance

```text id="2m7q4p"
0–100
```

### Assignment

```text
3v7h1q
0–100
```

### Midterm

```text
0–100
```

### Final

```text
0–100
```

### Study Hours

```text
>= 0
```

---

# 31. Prediction Flow

```text id="y3f7k1"
User Input
    ↓
Frontend Validation
    ↓
POST /api/prediction
    ↓
Backend Validation
    ↓
Load Model
    ↓
Prepare Features
    ↓
Predict
    ↓
Clamp / Validate Output
    ↓
Performance Category
    ↓
Save History
    ↓
Return Result
```

---

# 32. Model Availability

Jika model belum pernah dilatih:

```text id="6w4k8m"
MODEL_NOT_FOUND
```

UI:

```text
Prediction model is not available yet.

An administrator needs to train a model first.
```

Admin dapat diarahkan ke training action.

---

# 33. Predicted GPA

Output:

```text id="t9k5v2"
Predicted GPA
```

Contoh:

```text
3.47
```

Model output harus dibatasi secara aman ke domain GPA:

```text
0 ≤ predicted_gpa ≤ 4
```

Jika model menghasilkan nilai di luar domain karena model regression, hasil prediction perlu divalidasi sebelum ditampilkan/disimpan.

---

# 34. Performance Category

Output:

```text id="p2n8m4"
Excellent
Good
Average
Poor
```

Threshold kategori belum ditentukan oleh PRD.

Karena itu gunakan configuration:

```python id="e3c6q9"
PERFORMANCE_CATEGORIES = {
    # thresholds to be determined
}
```

Jangan mengarang threshold final tanpa keputusan produk.

---

# 35. Prediction Result

UI menampilkan:

```text id="x6v3n1"
Predicted GPA
Performance Category
Model Used
MAE
RMSE
R²
```

Contoh:

```text
Predicted GPA
3.47

Performance
Good

Model
Random Forest Regressor

MAE
0.18

RMSE
0.24

R²
0.82
```

---

# 36. Confidence

Jangan menampilkan:

```text id="5a9q2x"
Confidence: 92%
```

kecuali model dan metode memang menyediakan confidence/probability/interval yang valid.

Regression biasa tidak otomatis memiliki confidence percentage yang dapat ditampilkan sebagai angka sederhana.

Sebagai gantinya:

```text
Model Metrics
```

sudah cukup untuk MVP.

---

# 37. Prediction History

Setiap prediction dapat disimpan ke:

```text id="s1j7q3"
prediction_results
```

Data:

```text
student_id
semester
attendance
assignment_score
midterm_score
final_score
study_hours
predicted_gpa
performance_category
model_name
mae
rmse
r2
created_at
```

---

# 38. Prediction Without Student

`student_id` boleh `NULL`.

Hal ini memungkinkan user melakukan prediction secara manual.

Contoh:

```text id="m6y8p2"
Input hypothetical data
        ↓
Prediction
        ↓
student_id = NULL
```

Jika prediction berasal dari student tertentu:

```text
student_id = student.id
```

---

# 39. Prediction History API

```text id="5n9q7k"
GET /api/predictions
```

Dapat memiliki filter:

```text id="4k7x2m"
student_id
date
model
```

---

# 40. Prediction API

Endpoint:

```text id="r8m2w5"
POST /api/prediction
```

Request:

```json id="1d8w6v"
{
    "student_id": 1,
    "semester": 4,
    "attendance": 91,
    "assignment_score": 87,
    "midterm_score": 88,
    "final_score": 90,
    "study_hours": 14
}
```

---

# 41. Prediction Response

```json id="q4v8m1"
{
    "success": true,
    "data": {
        "predicted_gpa": 3.47,
        "performance_category": "Good",
        "model_name": "Random Forest Regressor",
        "metrics": {
            "mae": 0.18,
            "rmse": 0.24,
            "r2": 0.82
        }
    }
}
```

---

# 42. Prediction Page

Struktur:

```text id="9c4x7m"
Prediction
│
├── Page Header
│
├── Prediction Form
│
├── Prediction Result
│
├── Model Information
│
└── Prediction History
```

---

# 43. Prediction Form

```text id="5p7m2k"
Semester
[ 4 ]

Attendance
[ 91 ]

Assignment Score
[ 87 ]

Midterm Score
[ 88 ]

Final Score
[ 90 ]

Study Hours
[ 14 ]

[ Predict GPA ]
```

---

# 44. Student Selection

Prediction dapat menyediakan:

```text id="m4n8q2"
Student
[ Select Student ]
```

Jika student dipilih:

```text id="z7k1v4"
Student data
     ↓
Prefill prediction input
```

Namun user tetap harus dapat mengubah input jika fitur tersebut memang dibutuhkan untuk hypothetical prediction.

---

# 45. Prediction Result Card

Hasil utama harus menjadi fokus.

```text id="6v2p8m"
┌──────────────────────────────────┐
│ Predicted GPA                    │
│                                  │
│             3.47                 │
│                                  │
│ Good                             │
└──────────────────────────────────┘
```

Informasi model berada di bawahnya.

---

# 46. Model Information

```text id="r7x3k5"
Model Used
Random Forest Regressor

MAE
0.18

RMSE
0.24

R²
0.82
```

Tujuannya membuat hasil prediction transparan.

---

# 47. Prediction History Table

Kolom:

```text id="f8m3q6"
Date
Student
Semester
Predicted GPA
Category
Model
```

Jika student NULL:

```text
Manual Prediction
```

---

# 48. Empty State

Jika belum ada history:

```text id="1k9v5z"
No predictions yet.

Create a prediction to see the history.
```

---

# 49. Prediction Error States

### Model belum tersedia

```text id="x5q8m2"
Prediction model is not available.
```

### Dataset tidak cukup

```text id="n4r7k1"
There is not enough data to train a model.
```

### Input invalid

```text id="j8m2q5"
Please check the prediction inputs.
```

### Prediction failure

```text id="v6k3p9"
Unable to generate prediction.
```

---

# 50. ML Service Separation

Jangan membuat:

```text id="w4h7s1"
prediction.py
```

melakukan semua hal.

Pisahkan:

```text
ml/
├── preprocessing.py
├── train.py
├── evaluate.py
└── predict.py
```

dengan:

```text
services/
└── prediction_service.py
```

### ML layer

Menangani:

* model
* preprocessing
* training
* evaluation
* prediction

### Service layer

Menangani:

* business logic
* database
* validation
* history
* model metadata

---

# 51. Database Integration

Prediction result:

```text id="8j5m2w"
Prediction Service
       ↓
Prediction Repository
       ↓
prediction_results
```

Training metadata dapat tetap berada pada filesystem/model metadata untuk MVP.

Jika nanti dibutuhkan training history lengkap, dapat dibuat tabel `model_training_runs`.

Itu belum wajib untuk MVP.

---

# 52. Retraining

Model tidak boleh dilatih ulang setiap kali user melakukan prediction.

Flow yang benar:

```text id="v7m3q8"
Dataset Changes
       ↓
Admin decides to retrain
       ↓
Train Models
       ↓
Evaluate
       ↓
Replace Best Model
```

Prediction:

```text id="u5n8k2"
Load Existing Model
       ↓
Predict
```

---

# 53. Retraining Trigger

MVP:

```text id="q2x7m4"
Manual Admin Trigger
```

Future:

```text
Automatic retraining based on
dataset changes
```

Automatic retraining belum diperlukan untuk MVP.

---

# 54. Model Security

File model harus:

* berada di folder server
* tidak dapat diakses langsung dari public static directory
* hanya digunakan backend
* tidak menerima model file dari user sebagai model terpercaya

User hanya mengupload dataset.

---

# 55. Performance

Training merupakan proses yang lebih berat dibanding prediction.

Untuk MVP:

```text id="5y8k2m"
Admin Request
    ↓
Train
    ↓
Response
```

Jika dataset menjadi besar, training dapat dipindahkan ke background job.

Belum diperlukan pada tahap awal.

---

# 56. Responsive Design

Desktop:

```text id="3w8k1p"
┌─────────────────────┬──────────────────────┐
│ Prediction Form     │ Result                │
└─────────────────────┴──────────────────────┘
```

Mobile:

```text id="f6m2q9"
Prediction Form
       ↓
Result
       ↓
Model Information
       ↓
History
```

---

# 57. Dark Mode

Mengikuti design system:

```text id="6m9q3x"
Light
#F7F7F5
#FFFFFF
#E5E5E3
#171717

Dark
#111111
#181818
#2A2A2A
#F5F5F5
```

Status prediction menggunakan semantic colors secara terbatas.

Tidak menggunakan neon/glow.

---

# 58. Testing Preprocessing

* [ ] required feature tersedia
* [ ] target tersedia
* [ ] numeric conversion bekerja
* [ ] missing values ditolak/ditangani sesuai policy
* [ ] dataset kosong ditolak
* [ ] feature order konsisten

---

# 59. Testing Training

* [ ] dataset valid
* [ ] train/test split bekerja
* [ ] Linear Regression berhasil
* [ ] Random Forest berhasil
* [ ] Gradient Boosting berhasil
* [ ] MAE dihitung
* [ ] RMSE dihitung
* [ ] R² dihitung
* [ ] model dibandingkan
* [ ] best model dipilih berdasarkan hasil
* [ ] model disimpan
* [ ] metadata disimpan

---

# 60. Testing Prediction

* [ ] model tersedia
* [ ] model tidak tersedia
* [ ] input valid
* [ ] input invalid
* [ ] GPA prediction berada pada domain valid
* [ ] category dihasilkan
* [ ] model metrics ditampilkan
* [ ] prediction history tersimpan
* [ ] student_id NULL didukung
* [ ] student prediction didukung

---

# 61. Definition of Done

Tahap ML & Prediction selesai apabila:

* [ ] Processed dataset dapat digunakan untuk training.
* [ ] Feature selection tersedia.
* [ ] Target GPA tersedia.
* [ ] Train/test split tersedia.
* [ ] Linear Regression tersedia.
* [ ] Random Forest tersedia.
* [ ] Gradient Boosting tersedia.
* [ ] MAE tersedia.
* [ ] RMSE tersedia.
* [ ] R² tersedia.
* [ ] Model comparison tersedia.
* [ ] Best model dipilih dari hasil aktual.
* [ ] Model disimpan.
* [ ] Metadata model disimpan.
* [ ] Admin dapat melakukan training.
* [ ] Analyst tidak dapat melakukan training.
* [ ] Prediction API tersedia.
* [ ] Prediction form tersedia.
* [ ] Input validation tersedia.
* [ ] Predicted GPA tersedia.
* [ ] Performance category tersedia.
* [ ] Model metrics tersedia.
* [ ] Prediction history tersedia.
* [ ] Model-not-found state tersedia.
* [ ] Insufficient-data state tersedia.
* [ ] Error state tersedia.
* [ ] Responsive.
* [ ] Dark mode.
* [ ] SVG icons.
* [ ] Tidak ada prediction yang di-hardcode.
* [ ] Tidak ada fake confidence score.

---

# 62. Posisi Project Sekarang

Setelah tahap ML selesai, arsitektur intelligence sudah menjadi:

```text
                    DATASET
                       │
                       ▼
                 VALIDATION
                       │
                       ▼
                  CLEANING
                       │
                       ▼
               PROCESSED DATA
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      ANALYTICS       RISK          ML
          │          ENGINE          │
          │            │             │
          ▼            ▼             ▼
       Charts      Risk Level    Best Model
          │        Early Warn        │
          │            │             ▼
          │            │          Prediction
          └────────────┼────────────┘
                       ▼
                   INSIGHTS
                       │
                       ▼
                   DASHBOARD
                       │
                       ▼
                    REPORTS
```

---

