import pandas as pd
import numpy as np

def load_data():
    """Load the credit card dataset"""
    print("Loading credit card dataset...")
    df = pd.read_csv('data/creditcard.csv')
    print(f"Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
    return df

def check_data_quality(df):
    """Check the quality of our data"""
    print("\n===== DATA QUALITY CHECK =====")
    
    # Total records
    total_records = len(df)
    print(f"Total Records: {total_records:,}")
    
    # Missing values
    missing_values = df.isnull().sum().sum()
    missing_percent = (missing_values / (total_records * df.shape[1])) * 100
    print(f"Missing Values: {missing_values} ({missing_percent:.2f}%)")
    
    # Duplicate records
    duplicates = df.duplicated().sum()
    print(f"Duplicates: {duplicates}")
    
    # Invalid transaction amounts (negative or zero)
    invalid_amounts = (df['Amount'] <= 0).sum()
    print(f"Invalid Amounts (≤0): {invalid_amounts}")
    
    # Check for extreme outliers in Amount
    amount_q99 = df['Amount'].quantile(0.99)
    extreme_outliers = (df['Amount'] > amount_q99).sum()
    print(f"Extreme Outliers (>99th percentile): {extreme_outliers}")
    
    # Class distribution
    fraud_count = df['Class'].sum()
    normal_count = total_records - fraud_count
    fraud_rate = (fraud_count / total_records) * 100
    print(f"Fraud Transactions: {fraud_count} ({fraud_rate:.3f}%)")
    print(f"Normal Transactions: {normal_count} ({100-fraud_rate:.3f}%)")
    
    # Calculate data quality score
    quality_score = 100 - (missing_percent + (duplicates/total_records)*100 + (invalid_amounts/total_records)*100)
    print(f"\nOverall Data Quality Score: {quality_score:.2f}%")
    
    return {
        'total_records': total_records,
        'missing_values': missing_values,
        'missing_percent': missing_percent,
        'duplicates': duplicates,
        'invalid_amounts': invalid_amounts,
        'extreme_outliers': extreme_outliers,
        'fraud_count': fraud_count,
        'normal_count': normal_count,
        'fraud_rate': fraud_rate,
        'quality_score': quality_score
    }

def get_data_summary(df):
    """Get basic summary statistics"""
    print("\n=== DATA SUMMARY ===")
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nBasic statistics for Amount:")
    print(df['Amount'].describe())
    print(f"\nBasic statistics for Time:")
    print(df['Time'].describe())

if __name__ == "__main__":
    # Load the data
    df = load_data()
    
    # Check data quality
    quality_results = check_data_quality(df)
    
    # Get data summary
    get_data_summary(df)
    
    