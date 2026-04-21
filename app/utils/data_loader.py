"""
BLOCK 1: DATA LOADING MODULE
============================
Handles loading and verification of core datasets for GlowGuide AI backend.
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, Optional

# Set up paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"


def load_celestia_dataset() -> Optional[pd.DataFrame]:
    """
    Load celestia_clean.csv (main dataset).
    
    Returns:
        pd.DataFrame or None if loading fails
    """
    try:
        file_path = DATA_DIR / "celestia_clean.csv"
        
        if not file_path.exists():
            print(f"❌ Error: File not found at {file_path}")
            return None
        
        df = pd.read_csv(file_path)
        print(f"✅ Celestia dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"   Columns: {list(df.columns)}")
        
        return df
    
    except Exception as e:
        print(f"❌ Error loading celestia_clean.csv: {str(e)}")
        return None


def load_products_dataset() -> Optional[pd.DataFrame]:
    """
    Load product.csv (product dataset).
    
    Returns:
        pd.DataFrame or None if loading fails
    """
    try:
        file_path = DATA_DIR / "product.csv"
        
        if not file_path.exists():
            print(f"❌ Error: File not found at {file_path}")
            return None
        
        df = pd.read_csv(file_path)
        print(f"✅ Products dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"   Columns: {list(df.columns)}")
        
        return df
    
    except Exception as e:
        print(f"❌ Error loading product.csv: {str(e)}")
        return None


def load_remedies_dataset() -> Optional[pd.DataFrame]:
    """
    Load remedies.csv (remedy dataset).
    
    Returns:
        pd.DataFrame or None if loading fails
    """
    try:
        file_path = DATA_DIR / "remedies.csv"
        
        if not file_path.exists():
            print(f"❌ Error: File not found at {file_path}")
            return None
        
        df = pd.read_csv(file_path)
        print(f"✅ Remedies dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"   Columns: {list(df.columns)}")
        
        return df
    
    except Exception as e:
        print(f"❌ Error loading remedies.csv: {str(e)}")
        return None


def load_all_datasets() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Load all three datasets at once.
    
    Returns:
        Tuple of (df_main, products_df, remedies_df)
        Returns None for any dataset that fails to load
    """
    print("\n" + "="*70)
    print("🔷 BLOCK 1: DATA LOADING")
    print("="*70)
    
    df_main = load_celestia_dataset()
    products_df = load_products_dataset()
    remedies_df = load_remedies_dataset()
    
    print("="*70 + "\n")
    
    return df_main, products_df, remedies_df


def verify_datasets(df_main: pd.DataFrame, products_df: pd.DataFrame, remedies_df: pd.DataFrame) -> bool:
    """
    Verify that all datasets loaded successfully with non-zero rows.
    
    Returns:
        True if all datasets are valid, False otherwise
    """
    if df_main is None:
        print("❌ Celestia dataset failed to load")
        return False
    
    if products_df is None:
        print("❌ Products dataset failed to load")
        return False
    
    if remedies_df is None:
        print("❌ Remedies dataset failed to load")
        return False
    
    if df_main.empty:
        print("❌ Celestia dataset is empty")
        return False
    
    if products_df.empty:
        print("❌ Products dataset is empty")
        return False
    
    if remedies_df.empty:
        print("❌ Remedies dataset is empty")
        return False
    
    print("✅ All datasets verified successfully!")
    return True


if __name__ == "__main__":
    # Load all datasets
    df_main, products_df, remedies_df = load_all_datasets()
    
    # Verify they loaded correctly
    if verify_datasets(df_main, products_df, remedies_df):
        print("\n✨ Data loading complete! All datasets ready for preprocessing.")
        print("\nVariables available:")
        print("  • df_main: Main celestia dataset")
        print("  • products_df: Product dataset")
        print("  • remedies_df: Remedy dataset")
