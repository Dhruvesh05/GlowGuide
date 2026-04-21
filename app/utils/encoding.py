"""
BLOCK 3: ENCODING
================
Converts categorical features to numerical using LabelEncoder.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Tuple, Dict
from sklearn.preprocessing import LabelEncoder
from app.utils.preprocessing import clean_dataset
from app.utils.data_loader import load_celestia_dataset


# Set up paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Create models directory if it doesn't exist
MODELS_DIR.mkdir(exist_ok=True)


class EncodingManager:
    """Manages label encoding for all categorical features."""
    
    def __init__(self):
        """Initialize all label encoders."""
        self.le_skin = LabelEncoder()        # For Skin_Type
        self.le_sens = LabelEncoder()        # For Sensitivity
        self.le_concern = LabelEncoder()     # For Concern
        self.le_target = LabelEncoder()      # For clean_Ingredients (target)
        
        self.df_encoded = None
        self.df_original = None
    
    def encode_dataset(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Encode all categorical columns in the dataset.
        
        Args:
            df: Cleaned DataFrame from Block 2
        
        Returns:
            Encoded DataFrame or None if encoding fails
        """
        try:
            if df is None or df.empty:
                print("❌ Error: Input DataFrame is None or empty")
                return None
            
            # Store original for reference
            self.df_original = df.copy()
            
            # Create a copy for encoding
            df_encoded = df.copy()
            
            # Encode Skin_Type column
            print("\n🔹 Encoding Skin_Type...")
            df_encoded['Skin_Type'] = self.le_skin.fit_transform(df['Skin_Type'])
            print(f"   ✅ Fitted on {len(self.le_skin.classes_)} unique values")
            
            # Encode Sensitivity column
            print("\n🔹 Encoding Sensitivity...")
            df_encoded['Sensitivity'] = self.le_sens.fit_transform(df['Sensitivity'])
            print(f"   ✅ Fitted on {len(self.le_sens.classes_)} unique values")
            
            # Encode Concern column
            print("\n🔹 Encoding Concern...")
            df_encoded['Concern'] = self.le_concern.fit_transform(df['Concern'])
            print(f"   ✅ Fitted on {len(self.le_concern.classes_)} unique values")
            
            # Encode clean_Ingredients column (TARGET)
            print("\n🔹 Encoding clean_Ingredients (TARGET)...")
            df_encoded['clean_Ingredients'] = self.le_target.fit_transform(df['clean_Ingredients'])
            print(f"   ✅ Fitted on {len(self.le_target.classes_)} unique values")
            
            self.df_encoded = df_encoded
            return df_encoded
        
        except Exception as e:
            print(f"❌ Error during encoding: {str(e)}")
            return None
    
    def print_mappings(self) -> None:
        """Print all encoder class mappings."""
        if self.df_original is None or self.df_encoded is None:
            print("❌ Error: Encoding not performed yet")
            return
        
        print("\n" + "="*70)
        print("🗂️  ENCODING MAPPINGS")
        print("="*70)
        
        # Skin_Type mappings
        print("\n🔹 Skin_Type Encoder (le_skin):")
        print(f"   Classes: {list(self.le_skin.classes_)}")
        print(f"   Mapping:")
        for i, label in enumerate(self.le_skin.classes_):
            count = (self.df_original['Skin_Type'] == label).sum()
            print(f"      {i} ← {label} ({count} records)")
        
        # Sensitivity mappings
        print("\n🔹 Sensitivity Encoder (le_sens):")
        print(f"   Classes: {list(self.le_sens.classes_)}")
        print(f"   Mapping:")
        for i, label in enumerate(self.le_sens.classes_):
            count = (self.df_original['Sensitivity'] == label).sum()
            print(f"      {i} ← {label} ({count} records)")
        
        # Concern mappings
        print("\n🔹 Concern Encoder (le_concern):")
        print(f"   Classes: {list(self.le_concern.classes_)}")
        print(f"   Mapping:")
        for i, label in enumerate(self.le_concern.classes_):
            count = (self.df_original['Concern'] == label).sum()
            print(f"      {i} ← {label} ({count} records)")
        
        # clean_Ingredients mappings (TARGET)
        print("\n🔹 clean_Ingredients Encoder (le_target) - TARGET:")
        print(f"   Classes: {len(self.le_target.classes_)} unique ingredients")
        print(f"   First 20 mappings:")
        for i, label in enumerate(self.le_target.classes_[:20]):
            count = (self.df_original['clean_Ingredients'] == label).sum()
            print(f"      {i} ← {label} ({count} records)")
        
        if len(self.le_target.classes_) > 20:
            print(f"   ... and {len(self.le_target.classes_) - 20} more")
        
        print("="*70)
    
    def get_encoded_dataset(self) -> Optional[pd.DataFrame]:
        """Return the encoded dataset."""
        return self.df_encoded
    
    def get_encoders_dict(self) -> Dict:
        """Return all encoders as dictionary."""
        return {
            'le_skin': self.le_skin,
            'le_sens': self.le_sens,
            'le_concern': self.le_concern,
            'le_target': self.le_target
        }
    
    def get_encoder_info(self) -> Dict:
        """Return information about all encoders."""
        return {
            'le_skin': {
                'name': 'Skin_Type',
                'classes': list(self.le_skin.classes_),
                'n_classes': len(self.le_skin.classes_)
            },
            'le_sens': {
                'name': 'Sensitivity',
                'classes': list(self.le_sens.classes_),
                'n_classes': len(self.le_sens.classes_)
            },
            'le_concern': {
                'name': 'Concern',
                'classes': list(self.le_concern.classes_),
                'n_classes': len(self.le_concern.classes_)
            },
            'le_target': {
                'name': 'clean_Ingredients',
                'classes': list(self.le_target.classes_),
                'n_classes': len(self.le_target.classes_)
            }
        }


def print_encoded_data_info(df_encoded: pd.DataFrame, df_original: pd.DataFrame) -> None:
    """Print information about the encoded dataset."""
    if df_encoded is None or df_original is None:
        print("❌ Error: DataFrames are None")
        return
    
    print("\n" + "="*70)
    print("📊 ENCODED DATASET INFO")
    print("="*70)
    
    print(f"\nShape: {df_encoded.shape[0]} rows × {df_encoded.shape[1]} columns")
    print(f"Columns: {list(df_encoded.columns)}")
    
    print(f"\nData Types:")
    for col in df_encoded.columns:
        print(f"  • {col}: {df_encoded[col].dtype}")
    
    print(f"\nValue Ranges:")
    for col in df_encoded.columns:
        min_val = df_encoded[col].min()
        max_val = df_encoded[col].max()
        print(f"  • {col}: [{min_val}, {max_val}]")
    
    print(f"\nMissing Values: {df_encoded.isnull().sum().sum()}")
    print(f"Memory Usage: {df_encoded.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    print("\n" + "="*70)


def main():
    """Execute Block 3: Encoding."""
    
    print("\n" + "="*70)
    print("🔷 BLOCK 3: ENCODING")
    print("="*70)
    
    # Step 1: Load cleaned data from Block 2
    print("\n📥 Loading cleaned data from Block 2...")
    df_main = load_celestia_dataset()
    
    if df_main is None:
        print("❌ Failed to load data from Block 1")
        return None, None
    
    df_cleaned = clean_dataset(df_main)
    
    if df_cleaned is None:
        print("❌ Failed to clean dataset from Block 2")
        return None, None
    
    print(f"✅ Loaded cleaned data: {df_cleaned.shape[0]} rows × {df_cleaned.shape[1]} columns")
    
    # Step 2: Create encoding manager and encode
    print("\n🔐 Creating label encoders and encoding data...")
    manager = EncodingManager()
    df_encoded = manager.encode_dataset(df_cleaned)
    
    if df_encoded is None:
        print("❌ Failed to encode dataset")
        return None, None
    
    print(f"✅ Encoding complete: {df_encoded.shape[0]} rows × {df_encoded.shape[1]} columns")
    
    # Step 3: Print mappings
    manager.print_mappings()
    
    # Step 4: Print encoded data info
    print_encoded_data_info(df_encoded, df_cleaned)
    
    print("\n✨ Block 3 Encoding Complete!")
    print("   Ready for Block 4 (Feature Engineering)")
    print("="*70 + "\n")
    
    return df_encoded, manager


if __name__ == "__main__":
    df_encoded, manager = main()
