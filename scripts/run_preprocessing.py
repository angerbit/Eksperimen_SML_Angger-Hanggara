#!/usr/bin/env python
"""
Local Data Preprocessing Script
Mirrors the GitHub Actions preprocessing workflow
"""

import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

def run_command(cmd, description):
    """Execute a command and report results"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed with code {result.returncode}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    """Main preprocessing pipeline"""
    
    print("\n" + "="*60)
    print("📊 LOCAL DATA PREPROCESSING PIPELINE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from sklearn.preprocessing import StandardScaler
        print("✓ All dependencies available")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nInstalling dependencies...")
        run_command("pip install -r requirements.txt", "Dependency installation")
    
    # Check data file
    csv_path = Path("Membangun_model/Churn_preprocessing/Churn_Modelling.csv")
    if not csv_path.exists():
        print(f"✗ Data file not found: {csv_path}")
        sys.exit(1)
    
    print(f"✓ Data file found: {csv_path}")
    
    # Run data quality checks
    success = run_command(
        "python scripts/data_quality_check.py",
        "Data quality checks"
    )
    
    if not success:
        print("\n⚠ Data quality checks failed, but continuing...")
    
    # Execute the preprocessing notebook
    success = run_command(
        "jupyter nbconvert --to notebook --execute "
        "Membangun_model/data_preparation.ipynb "
        "--output Membangun_model/data_preparation_executed.ipynb",
        "Notebook execution"
    )
    
    if not success:
        print("\n✗ Notebook execution failed!")
        sys.exit(1)
    
    # Generate HTML report
    success = run_command(
        "jupyter nbconvert --to html "
        "Membangun_model/data_preparation_executed.ipynb "
        "--output Membangun_model/data_preparation_report.html",
        "HTML report generation"
    )
    
    # Summary
    print("\n" + "="*60)
    print("📋 PREPROCESSING PIPELINE SUMMARY")
    print("="*60)
    
    output_files = [
        "Membangun_model/data_preparation_executed.ipynb",
        "Membangun_model/data_preparation_report.html"
    ]
    
    for file in output_files:
        path = Path(file)
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"✓ {file} ({size_mb:.2f} MB)")
        else:
            print(f"✗ {file} (not found)")
    
    print("\n" + "="*60)
    print(f"✅ Preprocessing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("\n📍 Next steps:")
    print("1. Review generated report: Membangun_model/data_preparation_report.html")
    print("2. Commit executed notebook to repository")
    print("3. Continue with model training pipeline")
    print("="*60)

if __name__ == "__main__":
    main()
