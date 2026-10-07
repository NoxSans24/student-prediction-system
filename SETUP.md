# 🚀 QUICK START GUIDE - Student Performance Analytics

## ⚡ 5 Minutes Setup

### Step 1: Activate Virtual Environment
```bash
cd "C:\Project Mandiri\prediksi mahasiswa"
.venv\Scripts\activate
```

### Step 2: Ensure MySQL is Running
- Start MySQL Server (or XAMPP/Laragon)
- Verify: MySQL should be accessible on localhost:3306

### Step 3: Initialize Database
```bash
python database/schema.py
```

**Expected Output:**
```
[OK] Database 'student_performance_analytics' initialized successfully
```

### Step 4: Seed Sample Data
```bash
python database/seeder.py
```

**Expected Output:**
```
==================================================
✓ Created user: admin (admin123)
✓ Created user: analyst (analyst123)
✓ Seeded 150 students
✓ Seeded ... academic records
==================================================
```

### Step 5: Train ML Models
```bash
python ml/train.py
```

**Expected Output:**
```
==================================================
Starting ML training pipeline...
==================================================
Linear Regression - MAE: X.XXXX, RMSE: X.XXXX, R²: X.XXXX
Random Forest - MAE: X.XXXX, RMSE: X.XXXX, R²: X.XXXX
Gradient Boosting - MAE: X.XXXX, RMSE: X.XXXX, R²: X.XXXX
Best model: GradientBoosting with R²: X.XXXX
==================================================
```

### Step 6: Run Application
```bash
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
```

### Step 7: Open Browser
Navigate to: **http://127.0.0.1:5000**

---

## 🔐 Login Credentials

### Admin Account
```
Username: admin
Password: admin123
```
✅ Full access to all features including student management and model training

### Analyst Account
```
Username: analyst
Password: analyst123
```
✅ View-only access to analytics and predictions

---

## 📊 What You Can Do

### As Admin
- ✅ Manage students (add, edit, delete)
- ✅ View analytics & predictions
- ✅ Monitor risk assessments
- ✅ Train ML models
- ✅ Generate reports

### As Analyst
- ✅ View dashboard
- ✅ View analytics
- ✅ Make predictions
- ✅ View risk assessments
- ✅ (Cannot modify data)

---

## 🎯 Key Features to Test

### 1. Dashboard
- **URL**: http://127.0.0.1:5000/dashboard
- View KPI cards, charts, insights
- See top 5 at-risk students

### 2. Student Management
- **URL**: http://127.0.0.1:5000/students
- List 150 sample students
- Search, filter, pagination
- Add/edit/delete (admin only)

### 3. Analytics
- **URL**: http://127.0.0.1:5000/analytics
- GPA statistics and trends
- Correlation analysis
- Scatter plots

### 4. Risk Assessment
- **URL**: http://127.0.0.1:5000/risk
- Students grouped by risk level
- Risk factor breakdown
- Visual indicators

### 5. GPA Prediction
- **URL**: http://127.0.0.1:5000/prediction
- Input academic data
- Get GPA prediction
- View model metrics

---

## 🗂️ Project Structure Summary

```
database/
├── connection.py       → MySQL connection manager
├── schema.py          → Database schema & initialization
└── seeder.py          → Seed 150 students + academic data

services/
├── auth_service.py    → Authentication & user management
├── student_service.py → Student CRUD operations
├── analytics_service.py → Analytics & statistics
├── risk_service.py    → Risk assessment engine
└── prediction_service.py → GPA prediction

ml/
├── train.py           → Train Linear Regression, Random Forest, Gradient Boosting
├── predict.py         → Prediction engine using trained model
└── models/            → Stored trained models (auto-generated)

templates/
├── base.html          → Layout template
├── auth/              → Login & register pages
├── dashboard/         → Dashboard with charts
├── students/          → Student management
├── analytics/         → Analytics dashboard
├── risk/              → Risk assessment page
└── prediction/        → Prediction simulator

static/
├── css/               → Styling (DM Sans, dark/light mode)
├── js/                → JavaScript (Chart.js integration)
└── icons/             → SVG icons
```

---

## 🔧 Configuration

### Edit `.env` for Custom Settings

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=student_performance_analytics

# Session (30 minutes)
PERMANENT_SESSION_LIFETIME=1800
```

### Risk Thresholds in `config.py`
```python
RISK_GPA_LOW_THRESHOLD = 3.0          # GPA below = medium risk
RISK_GPA_MEDIUM_THRESHOLD = 2.5       # GPA below = high risk
RISK_ATTENDANCE_THRESHOLD = 75.0      # Attendance below = risk
RISK_SCORE_THRESHOLD = 60.0           # Average score below = risk
```

---

## 🐛 Troubleshooting

### Q: "Connection refused" error
**A**: MySQL is not running
```bash
# Start MySQL
# Windows: Start MySQL service or XAMPP
# Verify on localhost:3306
```

### Q: "ModuleNotFoundError"
**A**: Dependencies not installed
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Q: "Model not available"
**A**: ML models not trained
```bash
# Train models first
python ml/train.py
```

### Q: Port 5000 already in use
**A**: Change port in app.py
```python
# Line at bottom: app.run(debug=True, port=5001)
```

### Q: Login fails with correct credentials
**A**: Check database seeder ran successfully
```bash
# Re-seed database
python database/seeder.py
```

---

## 📈 Database Statistics

After seeding, your database will contain:

| Table | Count |
|-------|-------|
| users | 2 (admin, analyst) |
| students | 150 |
| academic_records | ~600+ (4-8 semesters per student) |
| risk_assessments | 150 (1 per student) |
| prediction_results | ~100 sample predictions |

---

## 🤖 Machine Learning Models

### Trained Models

Three models are trained on academic data:

1. **Linear Regression**
   - Simple baseline model
   - Fast prediction
   - Less accurate than ensemble

2. **Random Forest** (100 estimators)
   - Ensemble method
   - Good generalization
   - Moderate prediction time

3. **Gradient Boosting** (100 estimators)
   - Boosting ensemble
   - Usually best accuracy
   - Slightly slower

### Best Model Selection

The model with highest **R² score** is automatically selected and saved:
- Saved location: `ml/models/`
- Files: `{model_name}_model.joblib`, `scaler.joblib`, `model_metadata.json`

### Prediction Features

Input parameters for GPA prediction:
```json
{
  "attendance": 85.5,           // 0-100%
  "assignment_score": 78,        // 0-100
  "midterm_score": 82,           // 0-100
  "final_score": 80,             // 0-100
  "study_hours": 10              // per week
}
```

---

## 📝 Common Tasks

### Add New Student
1. Login as admin
2. Go to /students
3. Click "+ Add Student"
4. Fill form and submit
5. Student appears in list

### Predict GPA for Student
1. Go to /prediction
2. Select student from dropdown
3. Input academic scores
4. Click "Generate Prediction"
5. View predicted GPA + metrics

### Monitor At-Risk Students
1. Go to /risk
2. Filter by risk level (High, Medium, Low)
3. View risk factors breakdown
4. Export or take action

### View Analytics
1. Go to /analytics
2. Scroll through charts
3. Analyze trends and correlations
4. Export data if needed

---

## 🔒 Security Notes

### Already Implemented
- ✅ Password hashing (PBKDF2:SHA256)
- ✅ SQL injection protection (parameterized queries)
- ✅ Session-based authentication
- ✅ Environment variables for secrets
- ✅ CSRF protection (Flask default)

### For Production
- ⚠️ Change SECRET_KEY
- ⚠️ Enable HTTPS/SSL
- ⚠️ Setup proper logging
- ⚠️ Database backups
- ⚠️ Rate limiting
- ⚠️ Input validation

---

## 📊 Dashboard Overview

### Key Performance Indicators
- **Total Students**: 150
- **Average GPA**: 3.0-3.5
- **At Risk**: ~15-20 students
- **Avg Attendance**: 80-85%

### Charts Available
- GPA Trend (by semester)
- GPA Distribution (Excellent/Good/Average/Poor)
- GPA by Major
- Attendance vs GPA (scatter)
- Study Hours vs GPA (scatter)
- Score Analysis (radar)
- Correlation Matrix

---

## 🎓 Learning Resources

### Understanding Risk Assessment

Risk is calculated using multiple factors:

```
Risk Score = Average of:
  - GPA Risk (0-3 scale)
  - Attendance Risk (0-3 scale)
  - Score Trend Risk (0-3 scale)
  - Study Hours Risk (0-2 scale)

Classification:
  >= 2.0 → HIGH (red)
  1.0-2.0 → MEDIUM (orange)
  < 1.0 → LOW (green)
```

### Understanding GPA Prediction

Model predicts next semester GPA based on:
- Current attendance rate
- Assignment, midterm, final scores
- Study hours per week

Accuracy depends on:
- Historical data quality
- Model selection (Linear/RF/GB)
- Feature importance

---

## 📞 Support & Next Steps

### Next Development Tasks

- [ ] Add export to Excel/PDF
- [ ] Email notifications for at-risk students
- [ ] Advanced filtering options
- [ ] Student profile page
- [ ] Academic trend analysis
- [ ] Batch student import
- [ ] API documentation (Swagger)
- [ ] Unit & integration tests
- [ ] Performance optimization
- [ ] Mobile app integration

### Questions?

Check README.md for detailed documentation or review PRD/ folder for specifications.

---

## ✅ Verification Checklist

- [ ] Virtual environment activated
- [ ] MySQL running and accessible
- [ ] Database initialized (schema.py ran)
- [ ] Sample data seeded (seeder.py ran)
- [ ] ML models trained (train.py ran)
- [ ] Flask application running (app.py)
- [ ] Browser accessible at http://127.0.0.1:5000
- [ ] Can login with admin/admin123
- [ ] Dashboard shows data and charts
- [ ] Can make predictions

---

**🎉 You're all set! Happy analyzing!**

For detailed information, see README.md
