# 📤 PANDUAN UPLOAD KE GITHUB

## STEP 1: Setup Repository di GitHub

### 1.1 Buat Repository Baru di GitHub.com

**A. Login ke GitHub**
- Buka https://github.com
- Login dengan akun Anda
- Jika belum punya akun, buat yang baru (https://github.com/signup)

**B. Create New Repository**
- Klik **+ icon** di top-right → "New repository"
- Atau langsung ke: https://github.com/new

**C. Fill Repository Details**
```
Repository name: prediksi-mahasiswa
(atau nama yang Anda inginkan)

Description: 
Student Performance Analytics - Web-based platform for analyzing, 
predicting, and detecting academic performance risks using ML

Visibility: Public (agar orang bisa lihat)

Initialize with:
☐ Add a README file (jangan check - kita punya README.md)
☐ Add .gitignore (jangan check - kita punya .gitignore)
☐ Choose a license (optional)
```

**D. Create Repository**
- Klik tombol **"Create repository"**
- GitHub akan membuat repo kosong

**E. Copy Repository URL**
Setelah dibuat, Anda akan melihat:
```
Quick setup — if you've done this kind of thing before
Set up in Desktop   HTTPS   SSH

https://github.com/USERNAME/prediksi-mahasiswa.git
(copy URL ini)
```

---

## STEP 2: Add Remote Origin ke Local Git

Jalankan command di terminal (dari folder project):

```bash
cd "C:\Project Mandiri\prediksi mahasiswa"

# Replace USERNAME dan REPO_NAME sesuai GitHub Anda
git remote add origin https://github.com/USERNAME/prediksi-mahasiswa.git

# Verify remote ditambahkan
git remote -v
```

**Expected Output:**
```
origin  https://github.com/USERNAME/prediksi-mahasiswa.git (fetch)
origin  https://github.com/USERNAME/prediksi-mahasiswa.git (push)
```

---

## STEP 3: Rename Branch (Jika Diperlukan)

**Cek current branch:**
```bash
git branch -a
```

**Jika current branch bukan "main" atau "master", rename:**
```bash
# Jika current branch adalah "master"
git branch -M main
```

---

## STEP 4: Push Code ke GitHub

```bash
# Push semua commits ke GitHub
git push -u origin main
# atau jika branch Anda "master":
git push -u origin master
```

**Akan muncul prompt untuk login:**
```
Username for 'https://github.com': YOUR_USERNAME
Password for 'https://YOUR_USERNAME@github.com': YOUR_PASSWORD
```

**Atau jika pake Personal Access Token (PAT):**
```
Username: USERNAME
Password: (paste your PAT token)
```

---

## STEP 5: Verify Push Success

Setelah push selesai, Anda akan lihat:
```
Enumerating objects: 68, done.
Counting objects: 100% (68/68), done.
Delta compression using up to 8 threads
Compressing objects: 100% (45/45), done.
Writing objects: 100% (68/68), 42.96 KiB | 5.37 MiB/s, done.
Total 68 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/USERNAME/prediksi-mahasiswa.git
 * [new branch]      main -> main
Branch 'main' set to track remote branch 'main' from 'origin'.
```

**Check di GitHub:**
1. Refresh halaman repository GitHub
2. Anda akan lihat semua files sudah ter-upload
3. Commits history akan terlihat

---

## 🔐 AUTHENTICATION OPTIONS

### Option A: HTTPS dengan Password (Sederhana)

**Pro:**
- Mudah setup
- Tidak perlu install SSH tools

**Con:**
- GitHub deprecated password authentication
- Harus pakai Personal Access Token

**Setup:**
1. Buat Personal Access Token di GitHub:
   - Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Klik "Generate new token (classic)"
   - Select scopes: `repo` (full control of private repositories)
   - Generate dan copy token
2. Saat prompt password, paste token

### Option B: SSH (Recommended)

**Pro:**
- Lebih secure
- Tidak perlu input password setiap kali
- Industry standard

**Con:**
- Perlu generate SSH key terlebih dahulu

**Setup SSH:**

```bash
# 1. Generate SSH key (jika belum punya)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Or jika ed25519 tidak support:
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 2. Tekan Enter untuk default location
# Akan tanya passphrase - bisa skip (tekan Enter)

# 3. Output akan ke:
# ~/.ssh/id_ed25519 (private key - jangan dibagikan!)
# ~/.ssh/id_ed25519.pub (public key - untuk GitHub)

# 4. Copy public key
cat ~/.ssh/id_ed25519.pub

# 5. Di GitHub:
# - Settings → SSH and GPG keys
# - New SSH key
# - Paste public key
# - Save

# 6. Test connection
ssh -T git@github.com
# Expected: Hi username! You've successfully authenticated...
```

**Push dengan SSH:**
```bash
git remote set-url origin git@github.com:USERNAME/prediksi-mahasiswa.git
git push -u origin main
```

---

## TROUBLESHOOTING

### Error: "fatal: remote origin already exists"
```bash
# Hapus remote yang ada
git remote remove origin

# Tambah yang baru
git remote add origin https://github.com/USERNAME/prediksi-mahasiswa.git
```

### Error: "authentication failed"
**Solusi:**
1. Cek credential manager di Windows:
   - Control Panel → Credential Manager → Windows Credentials
   - Hapus GitHub entry yang lama
   - Push lagi, akan prompt login baru

2. Atau update credential:
```bash
git config --global user.email "your@email.com"
git config --global user.name "Your Name"
```

### Error: "branch 'main' set up to track remote"
**Solusi:**
```bash
# Cek branch name
git branch -a

# Jika branch adalah 'master', rename:
git branch -M main

# Push lagi
git push -u origin main
```

### Error: ".gitignore tidak ter-push"
```bash
# .gitignore tidak ter-track
git rm --cached .gitignore
git add .gitignore
git commit -m "fix: properly add gitignore"
git push
```

### Mau override remote (HATI-HATI!)
```bash
# Jika GitHub punya commit yang berbeda
git push -u origin main --force

# INGAT: ini akan overwrite remote branch!
# Gunakan hanya jika Anda yakin
```

---

## ✅ VERIFICATION CHECKLIST

Setelah push berhasil:

- [ ] Refresh GitHub page, files sudah muncul
- [ ] README.md terlihat di halaman utama
- [ ] Commit history terlihat (3 commits)
- [ ] Branch adalah "main" atau "master"
- [ ] Code badge/status tersedia (optional)

---

## 📊 GITHUB PAGE STRUCTURE

Setelah push, GitHub akan menampilkan:

```
prediksi-mahasiswa
├── 📄 README.md (tampil di preview)
├── 📁 database/
├── 📁 ml/
├── 📁 services/
├── 📁 templates/
├── 📁 static/
├── 📁 PRD/
├── 📄 app.py
├── 📄 config.py
├── 📄 requirements.txt
└── ... (semua files)

Commits: 3
  - ed9eb36 docs: add project initialization summary...
  - 6b8bdc3 docs: add comprehensive quick start guide...
  - 30f0e5e chore: initialize project structure...
```

---

## 🔄 FUTURE UPDATES

Setelah project di GitHub, untuk update:

```bash
# Edit file di local
# Contoh: tambah fitur baru

# Commit changes
git add .
git commit -m "feat: add new feature description"

# Push ke GitHub
git push origin main
```

---

## 🎯 NEXT STEPS SETELAH UPLOAD

### 1. Add README Badge (Optional)
Di README.md, tambahkan:
```markdown
[![GitHub license](https://img.shields.io/github/license/USERNAME/prediksi-mahasiswa)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/USERNAME/prediksi-mahasiswa)](https://github.com/USERNAME/prediksi-mahasiswa/stargazers)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
```

### 2. Add Topics (Di GitHub repo settings)
```
Topics: machine-learning, flask, analytics, gpa-prediction, student-performance
```

### 3. Add Collaborators (Optional)
Jika ada tim:
- Settings → Collaborators → Add people

### 4. Setup GitHub Pages (Optional)
Untuk dokumentasi web:
- Settings → Pages → Source: main/docs

### 5. Enable Issues & Discussions
- Untuk bugs tracking
- Feature requests
- Q&A

---

## 📞 COMMAND REFERENCE

```bash
# Check git config
git config --list
git config --global user.name
git config --global user.email

# Check remote
git remote -v
git remote show origin

# Check status
git status
git log --oneline

# Push changes
git push origin main
git push origin main --force (use with caution!)

# Pull changes
git pull origin main

# Create new branch
git branch feature/new-feature
git checkout feature/new-feature
git push -u origin feature/new-feature

# Merge branch
git checkout main
git merge feature/new-feature
git push origin main
```

---

## 🚀 SELESAI!

Project Anda sudah ter-upload ke GitHub!

**Bagikan repository URL Anda:**
```
https://github.com/USERNAME/prediksi-mahasiswa
```

**Orang bisa:**
- Clone project: `git clone https://github.com/USERNAME/prediksi-mahasiswa.git`
- Fork project
- Star project
- Buat issues
- Contribute via pull requests

---

**Happy coding! 🎉**
