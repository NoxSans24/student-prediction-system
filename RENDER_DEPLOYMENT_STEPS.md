# 🚀 RENDER DEPLOYMENT GUIDE - STEP BY STEP

## ✅ SELESAI: Persiapan Lokal

Files yang sudah disiapkan:
- ✅ `requirements.txt` - Updated dengan gunicorn & pymysql
- ✅ `Procfile` - Web service configuration
- ✅ `.env.production` - Template environment variables
- ✅ `app.py` - Updated untuk production (environment variables)
- ✅ Semua files di-push ke GitHub

---

## 🌐 STEP 2: SETUP DI RENDER.COM

### 2.1 Sign Up / Login ke Render

1. Buka https://render.com
2. Klik **"Get Started"** atau **"Sign Up"**
3. Pilih **"Sign up with GitHub"**
4. Authorize Render untuk akses GitHub
5. Klik **"Authorize render-oss"**

### 2.2 Connect Repository

Setelah login:

1. Klik **"New +"** (tombol biru di atas)
2. Pilih **"Web Service"**
3. Di halaman "Select Repository":
   - Cari: `student-prediction-system`
   - Klik repository yang muncul
   - Klik **"Connect"**

### 2.3 Configure Web Service

Isi form dengan:

```
Name: student-prediction-system
(atau: prediksi-mahasiswa)

Environment: Python 3

Region: Singapore (atau terdekat)

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app

Plan: Free
```

### 2.4 Add Environment Variables

**Scroll ke bawah, klik "Advanced"**

Tambahkan setiap variable:

```
FLASK_ENV
production

FLASK_DEBUG
False

SECRET_KEY
(Generate random: lihat di bawah)

MYSQL_HOST
(Dari PlanetScale: lihat di bawah)

MYSQL_USER
(Dari PlanetScale)

MYSQL_PASSWORD
(Dari PlanetScale)

MYSQL_DATABASE
student_performance_analytics

SESSION_TYPE
filesystem

PERMANENT_SESSION_LIFETIME
1800
```

**Cara generate SECRET_KEY:**

Di local Python shell:
```python
python
>>> import secrets
>>> secrets.token_hex(32)
'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6...'
```

Copy hasil tersebut sebagai SECRET_KEY

### 2.5 Deploy Web Service

1. Scroll ke bawah
2. Klik **"Create Web Service"**
3. Render akan:
   - Pull code dari GitHub
   - Install dependencies
   - Build application
   - Start server

**Wait 2-3 minutes untuk deployment selesai**

---

## 🗄️ STEP 3: SETUP DATABASE (PLANETSCALE)

### 3.1 Create PlanetScale Account

1. Buka https://planetscale.com
2. Klik **"Sign Up"**
3. Pilih **"Sign up with GitHub"** (opsional)
4. Verify email

### 3.2 Create Database

1. Di dashboard PlanetScale, klik **"Create a new database"**
2. Isi:
   ```
   Database name: student_performance_analytics
   Plan: Free (Hobby)
   Region: Singapore (atau terdekat)
   ```
3. Klik **"Create database"**

### 3.3 Get Connection String

1. Database sudah dibuat
2. Klik tab **"Connections"**
3. Di "Select a language", pilih: **"MySQL"**
4. Copy connection string

Format:
```
mysql+pymysql://USER:PASSWORD@HOST/DATABASE?charset=utf8mb4
```

Contoh:
```
mysql+pymysql://xxxxxxxx:pscale_pw_xxxxxxxx@aws.connect.psdb.cloud/student_performance_analytics?charset=utf8mb4
```

### 3.4 Dari Connection String, Extract:

```
MYSQL_HOST: aws.connect.psdb.cloud
MYSQL_USER: xxxxxxxx
MYSQL_PASSWORD: pscale_pw_xxxxxxxx
MYSQL_DATABASE: student_performance_analytics
```

### 3.5 Update di Render Dashboard

1. Kembali ke Render dashboard
2. Select service: `student-prediction-system`
3. Klik **"Environment"**
4. Update environment variables dengan data dari PlanetScale:
   ```
   MYSQL_HOST = aws.connect.psdb.cloud
   MYSQL_USER = xxxxxxxx
   MYSQL_PASSWORD = pscale_pw_xxxxxxxx
   ```
5. Klik **"Save"**

Render akan **auto-redeploy** dengan config baru

---

## 📊 STEP 4: INITIALIZE DATABASE

### 4.1 Create Tables

**Local setup:**

```bash
# Pastikan connected ke PlanetScale
python database/schema.py

# Akan create semua tables di PlanetScale
```

### 4.2 Seed Data

```bash
python database/seeder.py

# Akan insert:
# - 2 users (admin, analyst)
# - 150 students
# - 600+ academic records
# - Risk assessments
# - Prediction samples
```

Output:
```
==================================================
✓ Created user: admin (admin123)
✓ Created user: analyst (analyst123)
✓ Seeded 150 students
...
==================================================
```

### 4.3 Verify Data di PlanetScale

1. PlanetScale dashboard
2. Tab **"Browser"**
3. Select database
4. Check tables created
5. Check data inserted

---

## ✅ STEP 5: VERIFY DEPLOYMENT

### 5.1 Check Render Logs

1. Render dashboard
2. Select service
3. Scroll ke **"Logs"**
4. Should see:
   ```
   Building...
   Installing dependencies...
   Build succeeded!
   Listening on 0.0.0.0:10000
   ```

### 5.2 Get Live URL

Di Render service page, lihat:
```
URL: https://student-prediction-system.onrender.com
(atau nama yang Anda pilih)
```

### 5.3 Test Application

1. Buka URL: https://student-prediction-system.onrender.com
2. Should see login page
3. Login dengan:
   ```
   Username: admin
   Password: admin123
   ```
4. Should see dashboard
5. Check data loaded correctly

### 5.4 Test Features

- [ ] Dashboard loads
- [ ] KPI cards show data
- [ ] Charts render
- [ ] Students list works
- [ ] Search/filter works
- [ ] Analytics page works
- [ ] Prediction form works
- [ ] Risk analysis works

---

## 🎉 DEPLOYMENT COMPLETE!

**Your app is now LIVE at:**
```
https://student-prediction-system.onrender.com
```

**Share dengan:**
- Team members
- Stakeholders
- Portfolio
- GitHub README

---

## 🔗 USEFUL LINKS

- **Render Dashboard**: https://dashboard.render.com
- **PlanetScale Dashboard**: https://app.planetscale.com
- **GitHub Repository**: https://github.com/NoxSans24/student-prediction-system
- **Live App**: https://student-prediction-system.onrender.com

---

## 🐛 TROUBLESHOOTING

### Error: "Build failed"
- Check Render logs
- Verify requirements.txt
- Check Procfile format

### Error: "Cannot connect to database"
- Verify MYSQL_HOST, USER, PASSWORD
- Check PlanetScale connection string
- Update Render environment variables
- Click "Manual Deploy" button

### Error: "Application crashed"
- Check Render logs for error message
- Fix locally
- Git push
- Render auto-redeploy

### App shows "Service Unavailable"
- Wait 2-3 minutes (might be sleeping on free tier)
- Click service to wake it up
- Or upgrade to paid plan

---

## 💡 NEXT STEPS

1. **Monitor app** - Check logs regularly
2. **Backup database** - PlanetScale auto-backups
3. **Custom domain** - Add custom domain ($3/month)
4. **SSL certificate** - Auto-renew (included)
5. **Performance optimization** - Monitor & optimize

---

## 📋 CHECKLIST

- [ ] Web Service created di Render
- [ ] Environment variables set
- [ ] PlanetScale database created
- [ ] Connection string configured
- [ ] Tables created (schema.py)
- [ ] Data seeded (seeder.py)
- [ ] App accessible at HTTPS URL
- [ ] Login works
- [ ] Dashboard loads
- [ ] Features tested

**ALL DONE! ✅ Application is LIVE! 🚀**
