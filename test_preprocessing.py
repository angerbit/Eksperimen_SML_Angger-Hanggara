"""
Test and Validation Script for Automated Preprocessing
Verifies that the preprocessing pipeline works correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import with proper module name handling
import importlib.util
spec = importlib.util.spec_from_file_location("automate", "automate_Angger-Hanggara.py")
automate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(automate_module)
DataPreprocessor = automate_module.DataPreprocessor

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_preprocessing_output(X, y):
    """
    Validate preprocessed data meets expected criteria.
    
    Args:
        X (pd.DataFrame): Features
        y (pd.Series): Target
        
    Returns:
        bool: True if validation passes
    """
    logger.info("\n" + "="*60)
    logger.info("VALIDATING PREPROCESSING OUTPUT")
    logger.info("="*60)
    
    checks_passed = 0
    checks_total = 0
    
    # Check 1: X and y have same number of rows
    checks_total += 1
    if X.shape[0] == y.shape[0]:
        logger.info(f"✓ Check 1: X and y have matching rows ({X.shape[0]})")
        checks_passed += 1
    else:
        logger.error(f"✗ Check 1: X ({X.shape[0]}) and y ({y.shape[0]}) row mismatch")
    
    # Check 2: X has no NaN values
    checks_total += 1
    nan_count = X.isna().sum().sum()
    if nan_count == 0:
        logger.info(f"✓ Check 2: X has no NaN values")
        checks_passed += 1
    else:
        logger.error(f"✗ Check 2: X has {nan_count} NaN values")
    
    # Check 3: y has no NaN values
    checks_total += 1
    if y.isna().sum() == 0:
        logger.info(f"✓ Check 3: y has no NaN values")
        checks_passed += 1
    else:
        logger.error(f"✗ Check 3: y has {y.isna().sum()} NaN values")
    
    # Check 4: Categorical columns are encoded
    checks_total += 1
    if 'Geography' not in X.columns and 'Gender' not in X.columns:
        logger.info(f"✓ Check 4: Categorical columns are encoded (not raw)")
        checks_passed += 1
    else:
        logger.error(f"✗ Check 4: Found raw categorical columns")
    
    # Check 5: Numerical features are scaled (should have values close to 0 mean)
    checks_total += 1
    numerical_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'EstimatedSalary']
    existing_cols = [col for col in numerical_cols if col in X.columns]
    
    if existing_cols:
        mean_vals = X[existing_cols].mean()
        if (abs(mean_vals) < 1).all():  # After scaling, mean should be close to 0
            logger.info(f"✓ Check 5: Numerical features appear to be scaled")
            checks_passed += 1
        else:
            logger.warning(f"⚠ Check 5: Numerical features might not be properly scaled")
            logger.info(f"  Mean values (should be ~0): {mean_vals.to_dict()}")
    else:
        logger.info(f"✓ Check 5: No numerical features to verify")
        checks_passed += 1
    
    # Check 6: Target variable is binary (for binary classification)
    checks_total += 1
    unique_targets = y.unique()
    if len(unique_targets) == 2:
        logger.info(f"✓ Check 6: Target is binary classification (2 classes)")
        checks_passed += 1
    else:
        logger.warning(f"⚠ Check 6: Target has {len(unique_targets)} unique values")
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info(f"VALIDATION SUMMARY: {checks_passed}/{checks_total} checks passed")
    logger.info("="*60 + "\n")
    
    return checks_passed == checks_total


def test_preprocessing():
    """Run complete preprocessing test."""
    
    csv_path = 'Membangun_model/Churn_preprocessing/Churn_Modelling.csv'
    
    logger.info("\n" + "="*60)
    logger.info("TESTING AUTOMATED PREPROCESSING PIPELINE")
    logger.info("="*60)
    
    try:
        # Initialize and run preprocessor
        preprocessor = DataPreprocessor(csv_path)
        X, y = preprocessor.preprocess(save_output=True)
        
        # Validate output
        is_valid = validate_preprocessing_output(X, y)
        
        if is_valid:
            logger.info("✅ ALL TESTS PASSED!")
            return True
        else:
            logger.warning("⚠ Some tests failed - review output above")
            return False
            
    except Exception as e:
        logger.error(f"❌ TEST FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_preprocessing()
    sys.exit(0 if success else 1)
