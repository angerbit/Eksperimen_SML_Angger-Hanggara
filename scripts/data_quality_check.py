"""
Data Quality Check Script
This script performs quality checks on the Churn Modelling dataset
"""

import pandas as pd
import sys
from pathlib import Path

def check_data_quality():
    """Perform comprehensive data quality checks"""
    
    csv_path = Path('Membangun_model/Churn_preprocessing/Churn_Modelling.csv')
    
    if not csv_path.exists():
        print(f"❌ Error: CSV file not found at {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path, encoding='latin-1')
        
        print("🔍 Data Quality Checks")
        print("=" * 60)
        
        # Check 1: Dataset shape
        print(f"\n✓ Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Check 2: Missing values
        missing_count = df.isna().sum().sum()
        if missing_count == 0:
            print("✓ No missing values detected")
        else:
            print(f"⚠ Warning: {missing_count} missing values found")
            print(df.isna().sum())
        
        # Check 3: Duplicates
        duplicates = df.duplicated().sum()
        if duplicates == 0:
            print("✓ No duplicate rows detected")
        else:
            print(f"⚠ Warning: {duplicates} duplicate rows found")
        
        # Check 4: Data types
        print("\n✓ Data types validation:")
        print(df.dtypes)
        
        # Check 5: Numeric columns statistics
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        print(f"\n✓ Numeric columns: {list(numeric_cols)}")
        
        # Check 6: Categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        print(f"✓ Categorical columns: {list(categorical_cols)}")
        
        # Check 7: Target variable distribution
        if 'Exited' in df.columns:
            print("\n✓ Target variable (Exited) distribution:")
            print(df['Exited'].value_counts())
        
        # Check 8: Summary statistics
        print("\n✓ Summary statistics:")
        print(df.describe())
        
        print("\n" + "=" * 60)
        print("✅ All data quality checks passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during data quality check: {str(e)}")
        return False

if __name__ == "__main__":
    success = check_data_quality()
    sys.exit(0 if success else 1)
