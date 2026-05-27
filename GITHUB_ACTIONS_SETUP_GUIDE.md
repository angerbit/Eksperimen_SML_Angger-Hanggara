# 📊 Panduan GitHub Actions untuk Data Preprocessing

## 🎯 Tujuan

Workflow GitHub Actions mengotomatisasi proses preprocessing data dengan:
- ✅ Automated notebook execution
- ✅ Data quality validation
- ✅ Report generation
- ✅ Artifact storage
- ✅ Multi-environment testing

---

## 📦 File yang Dibuat

### 1. **GitHub Actions Workflows**

#### `.github/workflows/data-preprocessing.yml`
- Menjalankan notebook preprocessing
- Trigger: push, schedule, atau manual
- Output: executed notebook + HTML report
- Test: Python 3.9 dan 3.10

#### `.github/workflows/data-quality.yml`
- Validasi kualitas data
- Trigger: push dan pull request
- Checks: missing values, duplicates, statistics

### 2. **Configuration Files**

#### `requirements.txt`
Daftar semua dependencies Python yang diperlukan

#### `.gitignore`
Mengecualikan file yang tidak perlu di-commit

### 3. **Helper Scripts**

#### `scripts/data_quality_check.py`
Script untuk validasi kualitas data dengan output yang detail

#### `scripts/run_preprocessing.py`
Script untuk menjalankan preprocessing secara lokal

### 4. **Documentation**

#### `GITHUB_ACTIONS_README.md` & `GITHUB_ACTIONS_GUIDE.md`
Dokumentasi lengkap setup dan usage

---

## 🚀 Quick Start

### Step 1: Initialize Git Repository

```powershell
cd "SMSML_Angger-Hanggara"
git init
git add .
git commit -m "Add GitHub Actions workflows for data preprocessing"
```

### Step 2: Push ke GitHub

```powershell
# Setup remote
git remote add origin https://github.com/username/repo.git
git branch -M main
git push -u origin main
```

### Step 3: Enable Actions

Buka repository di GitHub → Actions tab → Enable workflows

### Step 4: Run Workflow

Pilih workflow di Actions tab → Click "Run workflow"

---

## 📊 Workflow Triggers

### Data Preprocessing Workflow

**Automatically triggered by:**
- Push ke `main` atau `develop` branch
- Perubahan file preprocessing
- Setiap minggu (Minggu 2 AM UTC)

**Manual trigger:**
1. GitHub → Actions tab
2. Pilih "Data Preprocessing Pipeline"
3. Click "Run workflow"

---

## 🔍 Monitoring & Outputs

### View Workflow Run

1. GitHub → Actions tab
2. Klik workflow run
3. Lihat logs per step

### Download Artifacts

1. Workflow run details
2. Scroll ke bagian "Artifacts"
3. Download hasil preprocessing

### Artifact Types

| Artifact | Deskripsi |
|----------|-----------|
| `preprocessed-notebook-py3.9` | Notebook executed dengan Python 3.9 |
| `preprocessed-notebook-py3.10` | Notebook executed dengan Python 3.10 |
| `preprocessing-report-py3.9` | HTML report dari Python 3.9 run |
| `preprocessing-report-py3.10` | HTML report dari Python 3.10 run |

---

## 💻 Local Testing

Jalankan preprocessing secara lokal sebelum push:

```powershell
# Option 1: Gunakan provided script
python scripts/run_preprocessing.py

# Option 2: Manual steps
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute Membangun_model/data_preparation.ipynb --output Membangun_model/data_preparation_executed.ipynb
jupyter nbconvert --to html Membangun_model/data_preparation_executed.ipynb --output Membangun_model/data_preparation_report.html
```

---

## 🔧 Konfigurasi & Customization

### Mengubah Schedule

Edit `.github/workflows/data-preprocessing.yml`:

```yaml
schedule:
  - cron: '0 2 * * 0'  # Minggu pukul 2 AM UTC
```

Cron format: `minute hour day month day_of_week`

Contoh:
- `'0 0 * * 0'` - Setiap minggu pukul midnight
- `'0 */6 * * *'` - Setiap 6 jam
- `'30 2 * * 1'` - Senin pukul 2:30 AM

### Mengubah Python Version

Edit `.github/workflows/data-preprocessing.yml`:

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
```

### Menambah Dependencies

1. Edit `requirements.txt`
2. Tambah package dan version
3. Commit dan push
4. Workflow akan otomatis install

---

## ⚠️ Troubleshooting

### Workflow tidak triggered

**Kemungkinan penyebab:**
- Branch tidak ada di workflow trigger
- File path tidak match
- Actions belum di-enable

**Solusi:**
```yaml
# Check trigger configuration
on:
  push:
    branches: [ main, develop ]
    paths:
      - 'Membangun_model/**'
      - 'requirements.txt'
```

### Notebook execution error

**Kemungkinan penyebab:**
- Missing library
- Wrong file path
- Encoding issue

**Debugging:**
```powershell
# Test locally dulu
python -c "import pandas; print(pandas.__version__)"
jupyter nbconvert --debug --to notebook --execute notebook.ipynb
```

### Artifact tidak tersimpan

**Kemungkinan penyebab:**
- Notebook tidak execute successfully
- Permission issue
- Storage limit tercapai

**Solusi:**
- Check workflow logs untuk error
- Verify file paths correct
- Check artifact retention settings

---

## 📈 Performance Tips

1. **Cache Dependencies**
   - Workflow sudah include caching
   - Faster subsequent runs

2. **Optimize Notebook**
   - Reduce data size untuk testing
   - Use sampling untuk large datasets
   - Split preprocessing ke multiple notebooks

3. **Parallel Testing**
   - Matrix strategy test multiple Python versions
   - Faster overall validation

---

## 🔐 Security Considerations

1. **Sensitive Data**
   - Jangan commit API keys atau passwords
   - Gunakan GitHub Secrets untuk credentials

   Contoh:
   ```yaml
   - name: Use secret
     run: echo ${{ secrets.API_KEY }}
   ```

2. **Data Privacy**
   - Artifact retention 30 hari
   - Data otomatis dihapus setelah itu

3. **Access Control**
   - Restrict branch push permissions
   - Require reviews sebelum merge

---

## 🔗 Integrasi dengan Tools Lain

### Slack Notifications

Add di workflow:
```yaml
- name: Send Slack notification
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

### Email Notifications

GitHub bawaan untuk workflow failures

### Code Coverage

Integrate dengan coverage tools seperti CodeCov

---

## 📚 Referensi & Resources

| Resource | Link |
|----------|------|
| GitHub Actions Docs | https://docs.github.com/actions |
| Jupyter nbconvert | https://nbconvert.readthedocs.io/ |
| Pandas Documentation | https://pandas.pydata.org/docs/ |
| Scikit-learn | https://scikit-learn.org/stable/ |

---

## 📝 Checklist Setup

- [ ] Initialize git repository
- [ ] Push ke GitHub
- [ ] Enable GitHub Actions
- [ ] Run first workflow manually
- [ ] Verify artifacts generated
- [ ] Download dan review reports
- [ ] Setup branch protection rules
- [ ] Configure notifications (optional)

---

## 🎓 Contoh Use Cases

### 1. **Automated Data Validation**
Setiap kali data file updated, workflow otomatis check kualitas

### 2. **Scheduled Preprocessing**
Setiap minggu data di-preprocess otomatis dengan latest code

### 3. **Multi-version Testing**
Ensure compatibility dengan Python 3.9 dan 3.10

### 4. **Report Generation**
Auto-generate HTML reports untuk stakeholder review

### 5. **CI/CD Pipeline**
Integrate dengan model training untuk full MLOps pipeline

---

## 🤝 Contributing

Untuk modifikasi workflows:

1. Create feature branch
2. Test changes locally
3. Create pull request
4. Review dan merge

---

## 📞 Support & Questions

Jika ada pertanyaan:
1. Check GitHub Actions documentation
2. Review workflow logs untuk error details
3. Test secara lokal sebelum push

---

**Dibuat untuk**: SMSML Project - Churn Modelling Preprocessing  
**Version**: 1.0  
**Last Updated**: 2024
