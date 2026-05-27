# GitHub Actions Cheat Sheet - Data Preprocessing

## ⚡ Quick Commands

### Git Setup
```powershell
git init
git add .
git commit -m "message"
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

### Local Testing
```powershell
# Install dependencies
pip install -r requirements.txt

# Run data quality checks
python scripts/data_quality_check.py

# Run full preprocessing pipeline
python scripts/run_preprocessing.py

# Manual notebook execution
jupyter nbconvert --to notebook --execute Membangun_model/data_preparation.ipynb --output data_preparation_executed.ipynb

# Generate HTML report
jupyter nbconvert --to html data_preparation_executed.ipynb --output report.html
```

---

## 🔄 Workflow Triggers

| Trigger | Config | Manual |
|---------|--------|--------|
| On Push | `on: push` | ❌ |
| On Schedule | `on: schedule` | ❌ |
| On PR | `on: pull_request` | ❌ |
| Manual | `on: workflow_dispatch` | ✅ GitHub UI |

---

## 📊 Common Cron Schedules

```yaml
# Setiap hari pukul 2 AM
'0 2 * * *'

# Setiap Minggu Minggu 2 AM
'0 2 * * 0'

# Setiap jam
'0 * * * *'

# Setiap 6 jam
'0 */6 * * *'

# Setiap hari kerja pukul 9 AM
'0 9 * * 1-5'
```

---

## 🔍 Workflow Structure

```yaml
name: Workflow Name                    # Display name
on: [push, pull_request]              # Triggers
jobs:
  job-name:
    runs-on: ubuntu-latest             # Runner OS
    steps:
      - uses: actions/checkout@v3      # Action
      - name: Step description         # Step name
        run: command                   # Shell command
```

---

## 🎯 Key Actions Used

```yaml
# Checkout code
- uses: actions/checkout@v3

# Setup Python
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'

# Cache dependencies
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip

# Upload artifacts
- uses: actions/upload-artifact@v3
  with:
    name: artifact-name
    path: path/to/file

# Download artifacts
- uses: actions/download-artifact@v3
  with:
    name: artifact-name
```

---

## 📂 Project Structure Required

```
repository/
├── .github/workflows/
│   ├── data-preprocessing.yml      ✅ Created
│   └── data-quality.yml            ✅ Created
├── Membangun_model/
│   ├── data_preparation.ipynb      ✅ Existing
│   └── Churn_preprocessing/
│       └── Churn_Modelling.csv     ✅ Existing
├── scripts/
│   ├── data_quality_check.py       ✅ Created
│   └── run_preprocessing.py        ✅ Created
├── requirements.txt                ✅ Created
├── .gitignore                      ✅ Created
└── README files                    ✅ Created
```

---

## 🚀 Step-by-Step Setup

```
1. Git init & commit
   git init && git add . && git commit -m "Initial commit"

2. Add GitHub remote
   git remote add origin https://github.com/user/repo.git

3. Push to GitHub
   git push -u origin main

4. Enable Actions
   Go to GitHub → Settings → Actions → Allow local and third party

5. Run first workflow
   GitHub → Actions → Select workflow → Run workflow

6. Monitor execution
   Click workflow run → View logs
```

---

## 📝 Environment Variables

```yaml
env:
  # Global
  PYTHON_VERSION: '3.10'
  DATA_PATH: 'Membangun_model/Churn_preprocessing/Churn_Modelling.csv'

jobs:
  job-name:
    env:
      # Job level
      JOB_VAR: 'value'
    steps:
      - name: Use env
        env:
          # Step level
          STEP_VAR: 'value'
        run: echo $STEP_VAR
```

---

## 🔐 Secrets Management

```yaml
# Add secrets in GitHub Settings → Secrets and variables

# Use in workflow
- name: Use secret
  run: |
    echo "Database: ${{ secrets.DB_HOST }}"
    echo "Token: ${{ secrets.API_TOKEN }}"
```

---

## ⚠️ Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `No such file` | Wrong path | Check `pwd` and file location |
| `Command not found` | Not installed | Add to `requirements.txt` |
| `Permission denied` | Access issue | Check file permissions |
| `Artifact not found` | Not uploaded | Check upload step |
| `Timeout` | Long execution | Increase timeout or optimize code |

---

## 📊 Status Badges

```markdown
# Add to README.md
![Data Preprocessing](https://github.com/user/repo/actions/workflows/data-preprocessing.yml/badge.svg)
![Data Quality](https://github.com/user/repo/actions/workflows/data-quality.yml/badge.svg)
```

---

## 🔗 Useful Links

- [GitHub Actions](https://github.com/features/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Action Marketplace](https://github.com/marketplace?type=actions)
- [Cron Guru](https://crontab.guru/) - Cron schedule helper

---

## 💡 Best Practices

✅ DO:
- Keep workflows simple
- Use descriptive names
- Cache dependencies
- Test locally first
- Document changes

❌ DON'T:
- Commit secrets
- Use large files
- Ignore errors
- Skip testing
- Hardcode paths

---

## 🔄 Workflow Life Cycle

```
Code Push
    ↓
Trigger Workflow
    ↓
Checkout Code
    ↓
Setup Environment
    ↓
Run Jobs
    ↓
Generate Artifacts
    ↓
Complete (Success/Failure)
    ↓
Notification
```

---

**Quick Reference untuk GitHub Actions Data Preprocessing**  
Untuk info lengkap, lihat `GITHUB_ACTIONS_SETUP_GUIDE.md`
