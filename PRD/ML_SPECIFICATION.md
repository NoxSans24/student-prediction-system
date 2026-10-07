1. Tujuan

Machine Learning digunakan untuk memprediksi GPA mahasiswa berdasarkan faktor akademik yang tersedia.

Alur utama:

Academic Dataset
      ↓
Data Validation
      ↓
Data Preprocessing
      ↓
Feature Selection
      ↓
Train / Test Split
      ↓
Train Multiple Models
      ↓
Model Evaluation
      ↓
Compare Models
      ↓
Select Best Model
      ↓
Save Model
      ↓
GPA Prediction

ML tidak digunakan untuk menentukan risk_level.

Pembagian tanggung jawab:

Sistem	Fungsi
Machine Learning	Prediksi GPA
Risk Engine	Menentukan Low / Medium / High Risk
Analytics	Menganalisis kondisi data
Dashboard	Menampilkan hasil
2. Target Machine Learning

Target yang ingin diprediksi:

gpa

Contoh:

Input:
- Semester = 4
- Attendance = 85
- Assignment = 82
- Midterm = 78
- Final = 84
- Study Hours = 15

Output:
Predicted GPA = 3.21

Nilai GPA merupakan nilai numerik sehingga masalah ini termasuk:

Regression

Bukan classification.

3. Features

Feature yang digunakan:

Feature	Tipe	Keterangan
semester	Integer	Semester mahasiswa
attendance	Float	Persentase kehadiran
assignment_score	Float	Nilai tugas
midterm_score	Float	Nilai UTS
final_score	Float	Nilai UAS
study_hours	Float	Jam belajar

Target:

gpa

Sehingga dataset ML secara konsep:

X =
[
    semester,
    attendance,
    assignment_score,
    midterm_score,
    final_score,
    study_hours
]

y =
[
    gpa
]
4. Data yang Tidak Digunakan Sebagai Feature

Beberapa kolom tidak digunakan secara langsung untuk prediksi:

student_id
name
major

Alasannya:

student_id hanya identifier.
name merupakan identitas mahasiswa.
major belum ditetapkan dalam PRD sebagai feature ML.

Jadi untuk MVP:

ML Features
├── semester
├── attendance
├── assignment_score
├── midterm_score
├── final_score
└── study_hours

Target
└── gpa

Catatan: Jika nantinya major ingin digunakan sebagai feature, perlu dibuat preprocessing kategorikal terlebih dahulu. Itu dapat menjadi pengembangan lanjutan.

5. Data Preprocessing

Sebelum training, data harus melewati preprocessing.

5.1 Validasi

Pastikan:

semester >= 1
0 <= attendance <= 100
0 <= assignment_score <= 100
0 <= midterm_score <= 100
0 <= final_score <= 100
study_hours >= 0
0 <= gpa <= 4

Data yang tidak valid tidak boleh langsung digunakan untuk training.

6. Missing Values

Missing values harus diperiksa sebelum training.

Contoh:

attendance = NULL
midterm_score = NULL

Dataset tidak langsung digunakan.

Pipeline:

Dataset
   ↓
Check Missing Values
   ↓
Missing?
 ┌───────┐
 │       │
YES     NO
 │       │
Cleaning │
 │       │
 └───┬───┘
     ↓
Preprocessing

Strategi imputation perlu ditentukan berdasarkan hasil eksplorasi dataset.

Jangan menetapkan satu metode secara permanen sebelum melihat karakteristik dataset.

7. Duplicate Data

Duplicate harus diperiksa sebelum training.

Terutama kombinasi:

student_id + semester

Karena pada database terdapat constraint:

UNIQUE(student_id, semester)

Data duplikat harus ditangani pada proses cleaning terlebih dahulu.

8. Train-Test Split

Dataset dibagi menjadi:

Training Data
Testing Data

Tujuannya agar model dapat dievaluasi menggunakan data yang tidak digunakan ketika training.

Contoh desain awal:

80% → Training
20% → Testing

Random state harus dibuat konsisten agar hasil eksperimen dapat direproduksi.

Contoh:

train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

80/20 dan random_state=42 merupakan keputusan implementasi awal, bukan ketentuan eksplisit dari PRD.

9. Model yang Digunakan

Platform membandingkan tiga model regression.

9.1 Linear Regression
from sklearn.linear_model import LinearRegression

Model digunakan sebagai baseline.

Kelebihan:

sederhana
cepat
mudah dijelaskan
cocok sebagai pembanding awal
9.2 Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor

Digunakan untuk menangkap hubungan yang lebih kompleks antara feature dan GPA.

Kelebihan:

dapat menangani hubungan non-linear
relatif robust
dapat memberikan feature importance
9.3 Gradient Boosting Regressor
from sklearn.ensemble import GradientBoostingRegressor

Digunakan sebagai model pembanding dengan pendekatan boosting.

Kelebihan:

mampu menangkap hubungan non-linear
dapat menghasilkan performa yang baik pada data tabular
cocok untuk eksperimen dataset akademik
10. Model Comparison

Ketiga model akan dilatih menggunakan dataset yang sama.

                    Dataset
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
   Linear Regression Random Forest Gradient Boosting
          │            │            │
          ↓            ↓            ↓
       Evaluate      Evaluate     Evaluate
          │            │            │
          └────────────┼────────────┘
                       ↓
                Compare Metrics
                       ↓
                  Best Model
11. Evaluation Metrics

Model dievaluasi menggunakan tiga metric:

MAE

Mean Absolute Error

Mengukur rata-rata selisih absolut antara nilai aktual dan prediksi.

Semakin kecil:

MAE ↓

semakin baik.

RMSE

Root Mean Squared Error

Memberikan penalti lebih besar terhadap error yang besar.

Semakin kecil:

RMSE ↓

semakin baik.

R²

R-squared

Mengukur seberapa baik model menjelaskan variasi target.

Semakin tinggi:

R² ↑

semakin baik.

12. Model Evaluation Table

Halaman ML nantinya dapat menampilkan hasil seperti:

Model	MAE	RMSE	R²
Linear Regression	0.21	0.29	0.82
Random Forest	0.16	0.23	0.89
Gradient Boosting	0.14	0.20	0.92

Angka di atas hanya contoh UI, bukan hasil dataset sebenarnya.

13. Best Model Selection

Model terbaik dipilih berdasarkan hasil evaluasi.

Secara umum:

MAE  → semakin kecil semakin baik
RMSE → semakin kecil semakin baik
R²   → semakin besar semakin baik

Tidak boleh menentukan model terbaik hanya berdasarkan satu metric secara sembarangan.

Untuk implementasi MVP, aturan pemilihan dapat ditetapkan setelah dataset aktual dianalisis.

Contoh:

Best Model:
Gradient Boosting Regressor

MAE  : ...
RMSE : ...
R²   : ...

Nama model terbaik harus berasal dari hasil training aktual.

Tidak boleh hardcode Random Forest atau Gradient Boosting sebagai model terbaik.

14. Model Storage

Setelah model terbaik ditemukan, model disimpan sehingga tidak perlu training ulang setiap kali user melakukan prediction.

Contoh struktur:

ml/
├── models/
│   ├── best_model.pkl
│   └── model_metadata.json
│
├── preprocessing.py
├── train.py
├── evaluate.py
└── predict.py

Model dapat disimpan menggunakan mekanisme serialisasi yang sesuai, misalnya joblib.

Metadata dapat berisi:

{
    "model_name": "Gradient Boosting Regressor",
    "features": [
        "semester",
        "attendance",
        "assignment_score",
        "midterm_score",
        "final_score",
        "study_hours"
    ],
    "target": "gpa",
    "mae": 0.14,
    "rmse": 0.20,
    "r2": 0.92
}

Nilai tersebut harus berasal dari hasil training aktual.

15. Training Flow

Training dilakukan melalui halaman Prediction / ML atau bagian training yang tersedia untuk Admin.

Flow:

Admin
 ↓
Load Processed Dataset
 ↓
Validate Dataset
 ↓
Select Features
 ↓
Split Dataset
 ↓
Train Linear Regression
 ↓
Train Random Forest
 ↓
Train Gradient Boosting
 ↓
Evaluate All Models
 ↓
Compare Metrics
 ↓
Select Best Model
 ↓
Save Model
 ↓
Save Metadata
16. Prediction Flow

Ketika user ingin melakukan prediksi:

User
 ↓
Prediction Form
 ↓
Input Academic Data
 ↓
Validate Input
 ↓
Load Best Model
 ↓
Preprocess Input
 ↓
Model Prediction
 ↓
Predicted GPA
 ↓
Performance Category
 ↓
Display Result

Contoh:

Semester          4
Attendance        88%
Assignment        85
Midterm           80
Final             87
Study Hours       16
                     ↓
             ML Prediction
                     ↓
             Predicted GPA
                  3.35
17. Performance Category

Hasil GPA dapat diterjemahkan menjadi kategori performa.

Contoh:

Predicted GPA
     ↓
Performance Category

Kategori yang digunakan harus mengikuti aturan yang ditetapkan aplikasi.

Contoh desain:

Excellent
Good
Average
Poor

Catatan: PRD menyebut kategori performa untuk output prediction, tetapi tidak menetapkan batas angka masing-masing kategori. Jadi threshold final harus ditentukan sebagai aturan aplikasi, bukan dianggap berasal dari PRD.

18. Prediction Result

Halaman Prediction menampilkan:

Predicted GPA
Performance Category
Model Used
Model Metrics

Contoh:

Predicted GPA

3.35

Good Performance

Model
Gradient Boosting Regressor

MAE
0.14

RMSE
0.20

R²
0.92

Sesuai PRD, jangan menampilkan "confidence" kecuali implementasi model memang menyediakan confidence/probability/interval yang valid.

19. Prediction History

Setiap prediksi yang dilakukan dapat disimpan ke:

prediction_results

Data yang disimpan:

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

Dengan begitu sistem dapat menyimpan histori prediksi.

20. Retraining

Model tidak perlu melakukan training setiap kali user melakukan prediction.

Konsep:

TRAINING
    ↓
Best Model
    ↓
Save Model
    ↓
────────────────
    ↓
PREDICTION
    ↓
Load Saved Model

Training ulang dilakukan ketika dataset akademik berubah secara signifikan atau Admin menjalankan proses training kembali.

21. Error Handling

ML module harus menangani kondisi seperti:

Dataset terlalu sedikit
Insufficient training data
Feature tidak lengkap
Required feature missing
Dataset belum dibersihkan
Dataset must be cleaned before training
Model belum tersedia
No trained model available
Input prediction tidak valid
Please enter valid academic values

Jangan biarkan error Python mentah muncul ke user.

22. Struktur Service

Implementasi dapat dipisahkan menjadi:

ml/
├── preprocessing.py
├── train.py
├── evaluate.py
├── predict.py
└── models/

Dan service Flask:

services/
└── prediction_service.py
preprocessing.py

Bertanggung jawab terhadap:

prepare_features()
validate_ml_data()
prepare_training_data()
prepare_prediction_input()
train.py

Bertanggung jawab terhadap:

load_dataset()
split_dataset()
train_linear_regression()
train_random_forest()
train_gradient_boosting()
evaluate.py

Bertanggung jawab terhadap:

calculate_mae()
calculate_rmse()
calculate_r2()
compare_models()
select_best_model()
predict.py

Bertanggung jawab terhadap:

load_best_model()
prepare_input()
predict_gpa()
23. Hubungan ML dengan Sistem

ML tidak berdiri sendiri.

                Dataset
                   │
                   ↓
            Data Cleaning
                   │
                   ↓
           Processed Dataset
             ┌─────┴─────┐
             ↓           ↓
        Analytics       ML
             │           │
             ↓           ↓
        Dashboard    GPA Prediction
                         │
                         ↓
                  Prediction Result

Risk Engine tetap terpisah:

Academic Records
       │
       ├──────────────→ ML
       │                  ↓
       │             Predicted GPA
       │
       └──────────────→ Risk Engine
                          ↓
                    Risk Level

Ini penting supaya prediksi GPA tidak disamakan dengan deteksi risiko.

24. Definition of Done — Machine Learning

ML dianggap selesai jika:

 Dataset tervalidasi
 Missing values ditangani
 Duplicate ditangani
 Feature berhasil dipersiapkan
 Target gpa berhasil dipisahkan
 Train/test split berjalan
 Linear Regression berhasil dilatih
 Random Forest Regressor berhasil dilatih
 Gradient Boosting Regressor berhasil dilatih
 MAE berhasil dihitung
 RMSE berhasil dihitung
 R² berhasil dihitung
 Model berhasil dibandingkan
 Best model dipilih berdasarkan hasil aktual
 Best model disimpan
 Metadata model disimpan
 Prediction menggunakan model yang tersimpan
 Predicted GPA ditampilkan
 Performance category ditampilkan
 Model dan metric ditampilkan
 Prediction history disimpan
 Error handling tersedia
 Tidak ada hasil ML yang di-hardcode