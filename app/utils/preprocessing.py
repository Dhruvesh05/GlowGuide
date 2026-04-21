"""
BLOCK 2: DATA CLEANING & PREPROCESSING
======================================
Prepares the main dataset for ML by cleaning and selecting relevant columns.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
from app.utils.data_loader import load_celestia_dataset


# Set up paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"


def clean_dataset(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Clean and preprocess the main dataset.
    
    Steps:
    1. Remove rows with missing/null values (dropna)
    2. Select relevant columns: Skin_Type, Sensitivity, Concern, clean_Ingredients
    3. Ensure all values are strings and consistent
    
    Args:
        df: Raw DataFrame from load_celestia_dataset()
    
    Returns:
        Cleaned DataFrame or None if cleaning fails
    """
    try:
        if df is None or df.empty:
            print("❌ Error: Input DataFrame is None or empty")
            return None
        
        # Step 1: Remove missing/null values
        initial_rows = len(df)
        df_cleaned = df.dropna()
        rows_removed = initial_rows - len(df_cleaned)
        
        if rows_removed > 0:
            print(f"🧹 Removed {rows_removed} rows with missing values")
        else:
            print(f"✅ No missing values found - all {initial_rows} rows retained")
        
        # Step 2: Select relevant columns
        required_columns = ['Skin_Type', 'Sensitivity', 'Concern', 'clean_Ingredients']
        
        # Check if all required columns exist
        missing_cols = [col for col in required_columns if col not in df_cleaned.columns]
        if missing_cols:
            print(f"❌ Error: Missing columns: {missing_cols}")
            print(f"   Available columns: {list(df_cleaned.columns)}")
            return None
        
        df_cleaned = df_cleaned[required_columns].copy()
        print(f"✅ Selected columns: {required_columns}")
        print(f"   Shape after column selection: {df_cleaned.shape}")
        
        # Step 3: Ensure all values are strings and consistent
        for col in df_cleaned.columns:
            # Convert to string
            df_cleaned[col] = df_cleaned[col].astype(str)
            
            # Strip whitespace
            if df_cleaned[col].dtype == 'object':
                df_cleaned[col] = df_cleaned[col].str.strip()
        
        print(f"✅ Converted all values to strings and stripped whitespace")
        
        return df_cleaned
    
    except Exception as e:
        print(f"❌ Error during cleaning: {str(e)}")
        return None


def print_unique_values(df: pd.DataFrame) -> None:
    """
    Print unique values for key columns: Skin_Type, Sensitivity, Concern.
    
    Args:
        df: Cleaned DataFrame
    """
    if df is None or df.empty:
        print("❌ Error: Cannot print unique values - DataFrame is None or empty")
        return
    
    print("\n" + "="*70)
    print("📊 UNIQUE VALUES")
    print("="*70)
    
    # Skin_Type unique values
    print("\n🔹 Skin_Type:")
    skin_types = df['Skin_Type'].unique()
    print(f"   Count: {len(skin_types)}")
    for skin_type in sorted(skin_types):
        count = (df['Skin_Type'] == skin_type).sum()
        print(f"      • {skin_type} ({count} records)")
    
    # Sensitivity unique values
    print("\n🔹 Sensitivity:")
    sensitivities = df['Sensitivity'].unique()
    print(f"   Count: {len(sensitivities)}")
    for sensitivity in sorted(sensitivities):
        count = (df['Sensitivity'] == sensitivity).sum()
        print(f"      • {sensitivity} ({count} records)")
    
    # Concern unique values
    print("\n🔹 Concern:")
    concerns = df['Concern'].unique()
    print(f"   Count: {len(concerns)}")
    for concern in sorted(concerns):
        count = (df['Concern'] == concern).sum()
        print(f"      • {concern} ({count} records)")
    
    print("="*70)


def get_dataset_info(df: pd.DataFrame) -> None:
    """
    Print detailed information about the cleaned dataset.
    
    Args:
        df: Cleaned DataFrame
    """
    if df is None or df.empty:
        print("❌ Error: Cannot print info - DataFrame is None or empty")
        return
    
    print("\n" + "="*70)
    print("📋 CLEANED DATASET INFO")
    print("="*70)
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nData Types:")
    for col in df.columns:
        print(f"  • {col}: {df[col].dtype}")
    
    print(f"\nMissing Values:")
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()
    if total_nulls == 0:
        print(f"  ✅ No missing values")
    else:
        for col, count in null_counts.items():
            if count > 0:
                print(f"  ❌ {col}: {count} missing values")
    
    print(f"\nMemory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print("="*70)


def main():
    """Execute Block 2: Data Cleaning."""
    
    print("\n" + "="*70)
    print("🔷 BLOCK 2: DATA CLEANING & PREPROCESSING")
    print("="*70)
    
    # Load data from Block 1
    print("\n📥 Loading data from Block 1...")
    df_main = load_celestia_dataset()
    
    if df_main is None:
        print("❌ Failed to load data from Block 1")
        return None
    
    print(f"✅ Loaded: {df_main.shape[0]} rows × {df_main.shape[1]} columns")
    
    # Clean the dataset
    print("\n🧹 Cleaning dataset...")
    df_cleaned = clean_dataset(df_main)
    
    if df_cleaned is None:
        print("❌ Failed to clean dataset")
        return None
    
    # Print unique values
    print_unique_values(df_cleaned)
    
    # Print dataset info
    get_dataset_info(df_cleaned)
    
    print("\n✨ Block 2 Data Cleaning Complete!")
    print("   Ready for Block 3 (Dataset Creation)")
    print("="*70 + "\n")
    
    return df_cleaned


if __name__ == "__main__":
    df_cleaned = main()
