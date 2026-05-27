# GitHub Actions Workflow untuk Data Preprocessing

Dokumentasi lengkap untuk GitHub Actions workflow yang mengotomatisasi data preprocessing pipeline.

## 📋 Overview

Workflow GitHub Actions ini mengotomatisasi proses preprocessing data Churn Modelling dengan fitur-fitur berikut:

- **Automated Execution**: Menjalankan notebook preprocessing secara otomatis
- **Quality Checks**: Validasi kualitas data sebelum dan sesudah preprocessing
- **Report Generation**: Menghasilkan laporan HTML dari hasil preprocessing
- **Multi-version Testing**: Test dengan Python 3.9 dan 3.10
- **Artifact Management**: Menyimpan hasil preprocessing sebagai artifacts

## 🚀 Workflow yang Tersedia

### 1. **Data Preprocessing Pipeline** (`data-preprocessing.yml`)

Workflow utama yang menjalankan notebook preprocessing.

**Trigger:**
- Push ke branch `main` atau `develop`
- Perubahan pada file-file terkait preprocessing
- Penjadwalan otomatis (Minggu pukul 2 AM UTC)
- Manual trigger via GitHub UI

**Steps:**
1. Checkout kode repository
2. Setup Python environment
3. Cache pip dependencies
4. Install requirements
5. Jalankan notebook preprocessing
6. Upload hasil notebook yang sudah dieksekusi
7. Generate laporan HTML
8. Validasi hasil preprocessing

**Outputs:**
- `data_preparation_executed.ipynb` - Notebook yang sudah dijalankan
- `data_preparation_report.html` - Laporan HTML hasil preprocessing

---

### 2. **Data Quality Checks** (`data-quality.yml`)

Workflow untuk validasi kualitas data.

**Trigger:**
- Push ke branch `main` atau `develop`
- Pull request ke branch `main`
- Perubahan pada data files

**Checks:**
- Validasi file data tersedia
- Pengecekan missing values
- Pengecekan duplicate rows
- Validasi data types
- Summary statistics

---

## 📦 Dependencies

Semua dependencies tercantum dalam `requirements.txt`:

```
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=1.0.0
jupyter>=1.0.0
nbconvert>=6.0.0
ipynb>=0.5.1
```

## 📁 Struktur Project

```
SMSML_Angger-Hanggara/
├── .github/
│   └── workflows/
│       ├── data-preprocessing.yml
│       └── data-quality.yml
├── Membangun_model/
│   ├── data_preparation.ipynb
│   └── Churn_preprocessing/
│       └── Churn_Modelling.csv
├── Monitoring dan Logging/
├── scripts/
│   └── data_quality_check.py
├── requirements.txt
└── .gitignore
```

## 🔧 Setup Instructions

### Step 1: Initialize Git Repository

```bash
cd "SMSML_Angger-Hanggara"
git init
git add .
git commit -m "Initial commit with GitHub Actions workflows"
```

### Step 2: Push ke GitHub

```bash
git remote add origin https://github.com/username/repository.git
git branch -M main
git push -u origin main
```

### Step 3: Enable Actions

1. Buka repository di GitHub
2. Klik tab **Actions**
3. Confirm untuk enable GitHub Actions

### Step 4: Configure Branch Protection (Optional)

1. Buka **Settings** > **Branches**
2. Add rule untuk branch `main`
3. Require workflows sebelum merge

## 📊 Memantau Workflow

### Via GitHub UI:

1. Buka repository
2. Klik tab **Actions**
3. Lihat workflow runs dan status

### Manual Trigger:

1. Klik **Actions** tab
2. Pilih workflow yang diinginkan
3. Klik **Run workflow** button

## 📈 Output & Artifacts

Setiap workflow run menghasilkan artifacts yang dapat didownload:

- **preprocessed-notebook**: Notebook yang sudah diexecute dengan output
- **preprocessing-report**: Laporan HTML visual dari hasil preprocessing

Artifacts tersimpan selama 30 hari dan dapat diakses dari workflow run details.

## ✅ Best Practices

1. **Regular Execution**: Workflow berjalan secara otomatis sesuai schedule
2. **Data Validation**: Selalu validate data sebelum digunakan
3. **Version Control**: Gunakan branch untuk development, merge ke main setelah testing
4. **Monitor Logs**: Check workflow logs untuk troubleshooting
5. **Update Dependencies**: Secara berkala update `requirements.txt`

## 🐛 Troubleshooting

### Workflow tidak trigger:

- Cek apakah branch ada di `on` clause
- Verify file paths dalam workflow
- Check branch protection rules

### Notebook execution error:

- Cek `requirements.txt` lengkap
- Verify path ke CSV file correct
- Check encoding (latin-1 untuk Churn_Modelling.csv)

### Memory/Timeout issues:

- Reduce notebook complexity
- Optimize data operations
- Increase workflow timeout jika perlu

## 📝 Environment Variables

Untuk menambah environment variables, edit workflow file:

```yaml
env:
  DATA_PATH: "Membangun_model/Churn_preprocessing/Churn_Modelling.csv"
  OUTPUT_PATH: "Membangun_model/"
```

## 🔐 Security

- Tidak commit sensitive data (API keys, passwords)
- Gunakan GitHub Secrets untuk credentials
- Regular update dependencies untuk security patches
- Review workflow logs untuk issues

## 📚 Referensi

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jupyter nbconvert](https://nbconvert.readthedocs.io/)
- [GitHub Actions Artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)

## 🎯 Next Steps

1. Push repository ke GitHub
2. Verify workflows run successfully
3. Monitor hasil preprocessing
4. Integrate dengan model training pipeline
5. Setup notifications untuk workflow failures

---

**Dibuat untuk**: SMSML Project - Churn Modelling  
**Last Updated**: 2024
