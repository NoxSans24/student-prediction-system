# Student Performance Analytics (SPA)

Platform berbasis web untuk menganalisis, memprediksi, dan mendeteksi risiko performa akademik mahasiswa menggunakan Data Science dan Machine Learning.

## 🎯 Fitur Utama

- **Dashboard Analytics** - Monitoring KPI dan performa akademik real-time
- **Student Management** - CRUD mahasiswa dengan pagination dan filtering
- **Advanced Analytics** - Statistik, trend, dan correlation analysis
- **GPA Prediction** - Prediksi GPA menggunakan ML models (Linear Regression, Random Forest, Gradient Boosting)
- **Risk Assessment** - Deteksi dini mahasiswa berisiko berdasarkan multiple factors
- **Role-Based Access** - Admin dan Analyst roles dengan permission berbeda
- **Responsive Design** - Optimized untuk desktop dan mobile

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: MySQL
- **Session**: Flask-Session (filesystem)
- **Security**: Werkzeug (password hashing)

### Data Science & ML
- **Processing**: Pandas, NumPy
- **ML Models**: Scikit-learn (Linear Regression, Random Forest, Gradient Boosting)
- **Model Storage**: joblib
- **Metrics**: MAE, RMSE, R²

### Frontend
- **Templating**: Jinja2
- **Styling**: Vanilla CSS (DM Sans, dark/light mode support)
- **Charts**: Chart.js
- **JavaScript**: Vanilla (no framework)
- **Icons**: SVG

## 📋 Prerequisites

- Python 3.11+
- MySQL Server
- Git
- Modern browser (Chrome, Edge, Firefox)

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
cd "C:\Project Mandiri\prediksi mahasiswa"
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database

Edit `.env` file (default values sudah tersedia):
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=student_performance_analytics
```

Initialize database schema:
```bash
python database/schema.py
```

### 5. Seed Database with Initial Data

Buat admin user dan dummy data untuk testing:
```bash
python database/seeder.py
```

Output:
```
==================================================
Starting database seeding...
==================================================
✓ Created user: admin (admin)
✓ Created user: analyst (analyst)
✓ Seeded 150 students
✓ Seeded ... academic records
✓ Seeded ... risk assessments
✓ Seeded ... prediction results

==================================================
✓ Database seeding completed successfully!
==================================================

Default credentials:
  Admin:    admin / admin123
  Analyst:  analyst / analyst123
==================================================
```

### 6. Train ML Models

```bash
python ml/train.py
```

Models dilatih: Linear Regression, Random Forest, Gradient Boosting
Model terbaik (berdasarkan R²) disimpan ke `ml/models/`

### 7. Run Application

```bash
python app.py
```

Aplikasi dapat diakses di: `http://127.0.0.1:5000`

## 🔐 Login

### Admin Account
- **Username**: admin
- **Password**: admin123
- **Akses**: Full access ke semua fitur

### Analyst Account
- **Username**: analyst
- **Password**: analyst123
- **Akses**: View-only untuk analytics dan predictions

## 📊 Menggunakan Aplikasi

### Dashboard
- Lihat KPI: Total students, at-risk count, GPA statistics
- Monitor chart: GPA trend, distribution, by major
- View top 5 at-risk students
- Generate insights otomatis

### Student Management
- List semua mahasiswa dengan pagination (20 per page)
- Search berdasarkan nama atau nomor induk
- Filter berdasarkan jurusan dan semester
- **Admin**: Tambah, edit, hapus mahasiswa

### Analytics
- GPA statistics: mean, median, std dev, min, max
- GPA distribution: Excellent, Good, Average, Poor
- GPA by major comparison
- GPA trend over semesters
- Scatter plot: Attendance vs GPA
- Scatter plot: Study hours vs GPA
- Score analysis: Assignment, midterm, final vs GPA
- Correlation matrix

### Risk Assessment
- Filter by risk level: High, Medium, Low
- View risk breakdown untuk setiap student
- Risk factors: GPA risk, Attendance risk, Score trend risk, Study hours risk
- Visual indicators dengan color coding

### GPA Prediction
- Input student dan academic data
- Generate prediction untuk GPA next semester
- View model confidence (R²), MAE, RMSE
- Historical predictions table

## 🗂️ Struktur Project

```
prediksi mahasiswa/
├── app.py                          # Flask entry point
├── config.py                       # Configuration
├── requirements.txt                # Dependencies
├── .env                           # Environment variables
├── .gitignore                     # Git ignore
│
├── database/
│   ├── connection.py              # MySQL connection
│   ├── schema.py                  # Database schema
│   └── seeder.py                  # Initial data seeder
│
├── services/
│   ├── auth_service.py            # Authentication
│   ├── student_service.py         # Student CRUD
│   ├── analytics_service.py       # Analytics & statistics
│   ├── risk_service.py            # Risk assessment
│   ├── prediction_service.py      # Predictions
│   └── (other services)
│
├── ml/
│   ├── train.py                   # Model training pipeline
│   ├── predict.py                 # Prediction engine
│   ├── __init__.py
│   └── models/                    # Trained models storage
│
├── templates/
│   ├── base.html                  # Base template
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   ├── students/
│   ├── analytics/
│   ├── prediction/
│   ├── risk/
│   └── errors/
│
├── static/
│   ├── css/                       # Stylesheets
│   ├── js/                        # JavaScript
│   └── icons/                     # SVG icons
│
└── data/
    ├── raw/                       # Raw datasets
    ├── processed/                 # Cleaned datasets
    └── reports/                   # Generated reports
```

## 🔄 Database Schema

### Main Tables
- **users** - User accounts (admin, analyst)
- **students** - Student records
- **academic_records** - GPA, attendance, scores per semester
- **risk_assessments** - Risk level classification
- **prediction_results** - ML prediction results

### Risk Thresholds (Configurable in config.py)
- GPA Low Threshold: 3.0
- GPA Medium Threshold: 2.5
- Attendance Threshold: 75%
- Score Threshold: 60

## 🤖 Machine Learning Pipeline

### Training Process
1. Load academic records dari database
2. Prepare features: attendance, assignment, midterm, final, study hours
3. Split data: 80% train, 20% test
4. Scale features using StandardScaler
5. Train 3 models:
   - Linear Regression
   - Random Forest (100 estimators)
   - Gradient Boosting (100 estimators)
6. Evaluate: MAE, RMSE, R²
7. Save best model (highest R²) ke `ml/models/`

### Prediction Features
```json
{
  "attendance": 85.5,
  "assignment_score": 78,
  "midterm_score": 82,
  "final_score": 80,
  "study_hours": 10
}
```

## 🧪 Development Commands

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run Flask development server
python app.py

# Initialize database
python database/schema.py

# Seed database with test data
python database/seeder.py

# Train ML models
python ml/train.py

# View logs
tail -f *.log
```

## 🔍 API Endpoints

### Authentication
```
POST   /login              - Login user
POST   /register           - Register new user
GET    /logout             - Logout
```

### Dashboard & Analytics
```
GET    /                   - Dashboard
GET    /analytics          - Analytics page
GET    /api/analytics/summary  - Analytics data
```

### Students
```
GET    /students           - List students
POST   /api/students       - Create (Admin)
PUT    /api/students/<id>  - Update (Admin)
DELETE /api/students/<id>  - Delete (Admin)
```

### Risk & Prediction
```
GET    /risk               - Risk analysis page
GET    /api/risk/assessment - Risk data
GET    /prediction         - Prediction page
POST   /api/predict        - Generate prediction
```

## 🚨 Troubleshooting

### "Database connection failed"
```bash
# Check MySQL is running
# Verify credentials in .env
python database/schema.py
```

### "Module not found"
```bash
# Activate virtual environment
.venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

### "Model not available"
```bash
# Train models first
python ml/train.py
```

### Port already in use
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

## 📝 Notes

- Default theme: Light mode (toggle di topbar)
- Session timeout: 30 minutes
- Pagination: 20 items per page
- Dark mode preference disimpan di localStorage
- Model training requires minimal 10 records

## 🔒 Security Notes

- Password hashing: PBKDF2:SHA256
- SQL injection protection: Parameterized queries
- Session-based authentication
- CSRF protection (Flask default)
- Environment variables untuk sensitive data

### Production Checklist
- [ ] Change SECRET_KEY
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS/SSL
- [ ] Setup proper logging
- [ ] Database backups
- [ ] Monitor performance
- [ ] Rate limiting
- [ ] Input validation

## 📄 License

Project ini dibuat untuk keperluan akademik.

## 👤 Author

Created for Student Performance Analytics project

## 📞 Support

Untuk bantuan atau pertanyaan, silakan buat issue di repository ini.

---

**Happy analyzing! 📊**
