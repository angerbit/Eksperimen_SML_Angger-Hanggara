"""
Automated Data Preprocessing Pipeline
For Churn Modelling Dataset

Author: Angger Hanggara
Purpose: Automate the preprocessing data
Output: Training-ready features (X) and target (y)
"""

import pandas as pd
import numpy as np
import logging
import io
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Automated data preprocessing for Churn Modelling dataset.
    
    This class encapsulates all preprocessing steps from the Jupyter notebook
    into reusable functions with consistent structure.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialize preprocessor with data path.
        
        Args:
            csv_path (str): Path to the CSV file
        """
        self.csv_path = csv_path
        self.df = None
        self.X = None
        self.y = None
        self.scaler = StandardScaler()
        self.numerical_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'EstimatedSalary']
        self.categorical_features = ['Geography', 'Gender']
        
        logger.info("DataPreprocessor initialized")
    
    def load_data(self) -> pd.DataFrame:
        """
        Load dataset from CSV file.
        
        Returns:
            pd.DataFrame: Loaded dataset
            
        Raises:
            FileNotFoundError: If CSV file not found
            pd.errors.ParserError: If CSV file cannot be parsed
        """
        try:
            if not Path(self.csv_path).exists():
                raise FileNotFoundError(f"CSV file not found at {self.csv_path}")
            
            self.df = pd.read_csv(self.csv_path, encoding='latin-1')
            logger.info(f"✓ Dataset loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            return self.df
            
        except Exception as e:
            logger.error(f"✗ Error loading data: {str(e)}")
            raise
    
    def data_wrangling(self) -> dict:
        """
        Perform data wrangling - check for issues in the dataset.
        
        Returns:
            dict: Dictionary containing data quality metrics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        logger.info("\n" + "="*60)
        logger.info("DATA WRANGLING")
        logger.info("="*60)
        
        # Check dataset info
        logger.info(f"\nDataset Info:")
        logger.info(f"  Shape: {self.df.shape}")
        logger.info(f"  Data types:\n{self.df.dtypes}")
        
        # Check missing values
        missing_count = self.df.isna().sum().sum()
        if missing_count == 0:
            logger.info(f"\n✓ No missing values detected")
        else:
            logger.warning(f"\n⚠ Warning: {missing_count} missing values found")
            logger.warning(self.df.isna().sum())
        
        # Check duplicates
        duplicates = self.df.duplicated().sum()
        if duplicates == 0:
            logger.info(f"✓ No duplicate rows detected")
        else:
            logger.warning(f"⚠ Warning: {duplicates} duplicate rows found")
        
        # Identify numeric columns for outlier analysis
        numeric_columns = self.df.select_dtypes(include=['int64', 'float64']).columns
        logger.info(f"\n✓ Numeric columns identified: {list(numeric_columns)}")
        logger.info(f"  (Outliers analysis can be performed if needed)")
        
        wrangling_report = {
            'missing_values': missing_count,
            'duplicates': duplicates,
            'numeric_columns': numeric_columns
        }
        
        logger.info("✓ Data wrangling completed\n")
        return wrangling_report

    def data_quality_checks(self, show_plots: bool = False, save_plots: bool = False, output_dir: Optional[str] = None) -> dict:
        """
        Run data quality checks: info, missing values, duplicates, and boxplots for numeric columns.

        Args:
            show_plots (bool): Whether to call plt.show() for interactive viewing.
            save_plots (bool): Whether to save generated plots to disk.
            output_dir (Optional[str]): Directory to save plots when `save_plots` is True.

        Returns:
            dict: Summary of quality metrics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        logger.info("Running data quality checks...")

        # Capture df.info()
        buf = io.StringIO()
        self.df.info(buf=buf)
        info_str = buf.getvalue()
        logger.info(f"\nDataFrame info:\n{info_str}")

        # Missing values
        missing = self.df.isna().sum()
        total_missing = int(missing.sum())
        logger.info(f"Missing values (per column):\n{missing}")
        logger.info(f"Total missing values: {total_missing}")

        # Duplicates
        duplicates = int(self.df.duplicated().sum())
        logger.info(f"Duplicate rows: {duplicates}")

        # Boxplots for numeric columns
        numeric_columns = list(self.df.select_dtypes(include=['int64', 'float64']).columns)
        logger.info(f"Numeric columns for boxplot: {numeric_columns}")

        if numeric_columns:
            fig, axes = plt.subplots(nrows=(len(numeric_columns) + 3) // 4, ncols=4, figsize=(15, 10))
            axes = axes.flatten()
            for i, col in enumerate(numeric_columns):
                sns.boxplot(x=self.df[col], ax=axes[i])
                axes[i].set_title(f'Boxplot of {col}')
            # hide unused axes
            for j in range(i + 1, len(axes)):
                axes[j].axis('off')
            plt.tight_layout()
            if save_plots:
                out_dir = Path(output_dir) if output_dir else Path.cwd() / 'preprocessing' / 'eda_plots'
                out_dir.mkdir(parents=True, exist_ok=True)
                plot_path = out_dir / 'boxplots_numeric.png'
                fig.savefig(plot_path)
                logger.info(f"Saved boxplots to {plot_path}")
            if show_plots:
                plt.show()
            plt.close(fig)

        quality_report = {
            'info': info_str,
            'missing_per_column': missing.to_dict(),
            'total_missing': total_missing,
            'duplicates': duplicates,
            'numeric_columns': numeric_columns,
        }

        logger.info("Data quality checks completed")
        return quality_report

    def exploratory_data_analysis(self, show_plots: bool = False, save_plots: bool = False, output_dir: Optional[str] = None) -> None:
        """
        Run exploratory data analysis (univariate, bivariate, correlation heatmap).

        Args:
            show_plots (bool): Whether to call plt.show() for interactive viewing.
            save_plots (bool): Whether to save generated plots to disk.
            output_dir (Optional[str]): Directory to save plots when `save_plots` is True.
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        logger.info("Starting exploratory data analysis (EDA)...")

        out_dir = Path(output_dir) if output_dir else Path.cwd() / 'preprocessing' / 'eda_plots'
        if save_plots:
            out_dir.mkdir(parents=True, exist_ok=True)

        # --- Univariate analysis for categorical variables ---
        plt.figure(figsize=(12, 15))
        cats = ['Geography', 'Gender', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'Exited']
        for i, col in enumerate(cats):
            ax = plt.subplot(3, 2, i + 1)
            sns.countplot(x=self.df[col], ax=ax)
            for container in ax.containers:
                ax.bar_label(container)
            plt.title(f'Countplot of {col}')
        plt.tight_layout()
        if save_plots:
            p = out_dir / 'univariate_categorical.png'
            plt.savefig(p)
            logger.info(f"Saved univariate categorical plots to {p}")
        if show_plots:
            plt.show()
        plt.close()

        # --- Numeric distributions ---
        numeric_single = ['CreditScore', 'Age']
        for col in numeric_single:
            plt.figure()
            sns.histplot(self.df[col], kde=True)
            plt.title(f'Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            if save_plots:
                p = out_dir / f'dist_{col}.png'
                plt.savefig(p)
                logger.info(f"Saved distribution plot {p}")
            if show_plots:
                plt.show()
            plt.close()

        # Tenure count
        plt.figure()
        ax = sns.countplot(x=self.df['Tenure'])
        ax.bar_label(ax.containers[0])
        plt.title('Distribution of Tenure')
        if save_plots:
            p = out_dir / 'dist_tenure.png'
            plt.savefig(p)
            logger.info(f"Saved tenure distribution to {p}")
        if show_plots:
            plt.show()
        plt.close()

        # Balance distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['Balance'], kde=True)
        plt.title('Distribution of Balance')
        if save_plots:
            p = out_dir / 'dist_balance.png'
            plt.savefig(p)
            logger.info(f"Saved balance distribution to {p}")
        if show_plots:
            plt.show()
        plt.close()

        # --- Bivariate analysis ---
        numerical_features = ['CreditScore', 'Age', 'Balance', 'EstimatedSalary']
        plt.figure(figsize=(20, 15))
        for i, column in enumerate(numerical_features):
            plt.subplot(2, 2, i + 1)
            sns.boxplot(x=self.df['Exited'], y=self.df[column], hue=self.df['Exited'])
            plt.title(f'{column} vs Exited')
        plt.tight_layout()
        if save_plots:
            p = out_dir / 'bivariate_numeric_vs_exited.png'
            plt.savefig(p)
            logger.info(f"Saved bivariate numeric plots to {p}")
        if show_plots:
            plt.show()
        plt.close()

        # Categorical vs target
        categorical_features = ['Geography', 'Gender', 'NumOfProducts', 'Tenure', 'HasCrCard', 'IsActiveMember']
        plt.figure(figsize=(20, 15))
        for i, column in enumerate(categorical_features):
            plt.subplot(3, 2, i + 1)
            sns.countplot(x=self.df[column], hue=self.df['Exited'])
            plt.title(f'{column} vs Exited')
        plt.tight_layout()
        if save_plots:
            p = out_dir / 'bivariate_categorical_vs_exited.png'
            plt.savefig(p)
            logger.info(f"Saved bivariate categorical plots to {p}")
        if show_plots:
            plt.show()
        plt.close()

        # Correlation matrix
        plt.figure(figsize=(12, 10))
        corr_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary', 'Exited']
        correlation_matrix = self.df[corr_features].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title('Correlation Matrix')
        if save_plots:
            p = out_dir / 'correlation_matrix.png'
            plt.savefig(p)
            logger.info(f"Saved correlation matrix to {p}")
        if show_plots:
            plt.show()
        plt.close()

        logger.info("EDA completed")
    
    def drop_unnecessary_columns(self) -> None:
        """
        Drop columns that are not needed for modeling.
        
        Drops: RowNumber, CustomerId, Surname
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        logger.info("Dropping unnecessary columns...")
        columns_to_drop = ['RowNumber', 'CustomerId', 'Surname']
        
        # Only drop columns that exist
        existing_columns = [col for col in columns_to_drop if col in self.df.columns]
        
        if existing_columns:
            self.df.drop(columns=existing_columns, inplace=True)
            logger.info(f"✓ Dropped columns: {existing_columns}")
        else:
            logger.warning("⚠ No unnecessary columns found to drop")
        
        logger.info(f"  New shape: {self.df.shape}\n")
    
    def define_features_and_target(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separate features (X) and target (y) from dataset.
        
        Target variable: 'Exited' (last column)
        Features: All other columns
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]: Features and target
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        logger.info("Defining features and target...")
        
        self.X = self.df.iloc[:, :-1]
        self.y = self.df.iloc[:, -1]
        
        logger.info(f"✓ Features shape: {self.X.shape}")
        logger.info(f"✓ Target shape: {self.y.shape}")
        logger.info(f"  Target variable: 'Exited'")
        logger.info(f"  Target distribution:\n{self.y.value_counts()}\n")
        
        return self.X, self.y
    
    def encode_categorical_features(self) -> pd.DataFrame:
        """
        Encode categorical variables using one-hot encoding.
        
        Categorical features: Geography, Gender
        
        Returns:
            pd.DataFrame: Features with encoded categorical variables
        """
        if self.X is None:
            raise ValueError("Features not defined. Call define_features_and_target() first.")
        
        logger.info("Encoding categorical variables...")
        logger.info(f"  Categorical columns: {self.categorical_features}")
        
        # Get dummies for categorical features, drop first to avoid multicollinearity
        self.X = pd.get_dummies(
            self.X,
            columns=self.categorical_features,
            drop_first=True
        )
        
        logger.info(f"✓ Categorical encoding completed")
        logger.info(f"  New features shape: {self.X.shape}")
        logger.info(f"  New columns: {list(self.X.columns)}\n")
        
        return self.X
    
    def scale_numerical_features(self) -> pd.DataFrame:
        """
        Scale numerical features using StandardScaler.
        
        Numerical features: CreditScore, Age, Tenure, Balance, EstimatedSalary
        
        Returns:
            pd.DataFrame: Features with scaled numerical variables
        """
        if self.X is None:
            raise ValueError("Features not defined. Call define_features_and_target() first.")
        
        logger.info("Scaling numerical features...")
        logger.info(f"  Numerical columns: {self.numerical_features}")
        
        # Only scale columns that exist in X
        existing_numerical = [col for col in self.numerical_features if col in self.X.columns]
        
        if existing_numerical:
            self.X[existing_numerical] = self.scaler.fit_transform(self.X[existing_numerical])
            logger.info(f"✓ Scaling completed for {len(existing_numerical)} numerical features")
            logger.info(f"  Scaler: StandardScaler()")
            logger.info(f"  Scaled columns: {existing_numerical}\n")
        else:
            logger.warning("⚠ No numerical features found to scale")
        
        return self.X
    
    def save_preprocessed_data(self, output_dir: str = None) -> Tuple[str, str]:
        """
        Save preprocessed features and target to CSV files.
        
        Args:
            output_dir (str): Output directory path. If None, uses preprocessing folder
            
        Returns:
            Tuple[str, str]: Paths to saved X and y files
        """
        if self.X is None or self.y is None:
            raise ValueError("Features not preprocessed yet.")
        
        if output_dir is None:
            # Use current directory's parent (project root) / preprocessing as default
            output_dir = Path.cwd() / "preprocessing"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save preprocessed data
        X_path = output_dir / "X_preprocessed.csv"
        y_path = output_dir / "y_preprocessed.csv"
        
        self.X.to_csv(X_path, index=False)
        self.y.to_csv(y_path, index=False, header=['Exited'])
        
        logger.info("Saving preprocessed data...")
        logger.info(f"✓ Features saved to: {X_path}")
        logger.info(f"✓ Target saved to: {y_path}\n")
        
        return str(X_path), str(y_path)
    
    def get_processed_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Get the preprocessed features and target.
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]: Processed features and target
        """
        if self.X is None or self.y is None:
            raise ValueError("Data not preprocessed yet.")
        
        return self.X, self.y
    
    def preprocess(self, save_output: bool = True, output_dir: str = None, run_checks: bool = False, show_plots: bool = False, save_plots: bool = True) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Execute complete preprocessing pipeline.
        
        Steps:
        1. Load data
        2. Data wrangling
        3. (Optional) Data quality checks + EDA
        4. Drop unnecessary columns
        5. Define features and target
        6. Encode categorical features
        7. Scale numerical features
        8. (Optional) Save preprocessed data
        
        Args:
            save_output (bool): Whether to save preprocessed data to CSV
            output_dir (str): Output directory for saving. If None, uses default
            run_checks (bool): Whether to run data quality checks and EDA
            show_plots (bool): Whether to display plots (may be ignored in headless CI)
            save_plots (bool): Whether to save EDA plots to disk
            
        Returns:
            Tuple[pd.DataFrame, pd.Series]: Preprocessed features and target ready for training
        """
        logger.info("\n" + "="*60)
        logger.info("STARTING AUTOMATED PREPROCESSING PIPELINE")
        logger.info("="*60 + "\n")
        
        try:
            # Step 1: Load data
            self.load_data()
            
            # Step 2: Data wrangling
            self.data_wrangling()

            # Optional: data quality checks and EDA
            if run_checks:
                logger.info("\nRunning data quality checks and EDA as requested...\n")
                self.data_quality_checks(show_plots=show_plots, save_plots=save_plots, output_dir=output_dir)
                self.exploratory_data_analysis(show_plots=show_plots, save_plots=save_plots, output_dir=output_dir)
            
            # Step 3: Drop unnecessary columns
            self.drop_unnecessary_columns()
            
            # Step 4: Define features and target
            self.define_features_and_target()
            
            # Step 5: Encode categorical features
            self.encode_categorical_features()
            
            # Step 6: Scale numerical features
            self.scale_numerical_features()
            
            # Step 7: Save output
            if save_output:
                self.save_preprocessed_data(output_dir)
            
            logger.info("="*60)
            logger.info("✅ PREPROCESSING COMPLETED SUCCESSFULLY")
            logger.info("="*60)
            logger.info(f"\nFinal Data Shape:")
            logger.info(f"  Features (X): {self.X.shape}")
            logger.info(f"  Target (y): {self.y.shape}")
            logger.info(f"  Ready for model training!\n")
            
            return self.X, self.y
            
        except Exception as e:
            logger.error(f"\n❌ PREPROCESSING FAILED: {str(e)}")
            raise


def main():
    """
    Main function to run the preprocessing pipeline.
    """
    # Define CSV path
    csv_path = r'Churn_Modelling.csv'
    
    try:
        # Initialize preprocessor
        preprocessor = DataPreprocessor(csv_path)
        
        # Run complete preprocessing pipeline (also run quality checks and EDA)
        X, y = preprocessor.preprocess(save_output=True, run_checks=True, show_plots=False, save_plots=True)
        
        # Display final results
        logger.info("="*60)
        logger.info("PREPROCESSING OUTPUT SUMMARY")
        logger.info("="*60)
        logger.info(f"\nFeatures (X) - First 5 rows:")
        logger.info(f"{X.head()}")
        logger.info(f"\nTarget (y) - First 5 values:")
        logger.info(f"{y.head()}")
        
        return X, y
        
    except Exception as e:
        logger.error(f"Failed to preprocess data: {str(e)}")
        raise


if __name__ == "__main__":
    X, y = main()
