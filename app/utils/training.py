"""
BLOCK 4: MODEL TRAINING (CLASSIFICATION)
========================================
Trains a KNeighborsClassifier on the encoded dataset.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
from sklearn.neighbors import KNeighborsClassifier
from app.utils.encoding import EncodingManager
from app.utils.preprocessing import clean_dataset
from app.utils.data_loader import load_celestia_dataset


# Set up paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Create models directory if it doesn't exist
MODELS_DIR.mkdir(exist_ok=True)


class ModelTrainer:
    """Manages KNN model training."""
    
    def __init__(self, n_neighbors: int = 3):
        """
        Initialize the model trainer.
        
        Args:
            n_neighbors: Number of neighbors for KNN (default: 3)
        """
        self.n_neighbors = n_neighbors
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.X = None
        self.y = None
        self.feature_columns = ['Skin_Type', 'Sensitivity', 'Concern']
        self.target_column = 'clean_Ingredients'
        self.is_trained = False
    
    def prepare_data(self, df_encoded: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features (X) and target (y) from encoded dataset.
        
        Args:
            df_encoded: Encoded DataFrame from Block 3
        
        Returns:
            Tuple of (X, y)
        """
        try:
            if df_encoded is None or df_encoded.empty:
                print("❌ Error: Encoded DataFrame is None or empty")
                return None, None
            
            # Check if required columns exist
            missing_cols = [col for col in self.feature_columns if col not in df_encoded.columns]
            if missing_cols:
                print(f"❌ Error: Missing feature columns: {missing_cols}")
                return None, None
            
            if self.target_column not in df_encoded.columns:
                print(f"❌ Error: Target column '{self.target_column}' not found")
                return None, None
            
            # Extract features (X)
            X = df_encoded[self.feature_columns].copy()
            print(f"✅ Features (X) prepared: {X.shape}")
            print(f"   Columns: {list(X.columns)}")
            
            # Extract target (y)
            y = df_encoded[self.target_column].copy()
            print(f"✅ Target (y) prepared: {len(y)} samples")
            print(f"   Unique classes: {y.nunique()}")
            
            self.X = X
            self.y = y
            
            return X, y
        
        except Exception as e:
            print(f"❌ Error preparing data: {str(e)}")
            return None, None
    
    def train(self) -> bool:
        """
        Train the KNN model.
        
        Returns:
            True if training successful, False otherwise
        """
        try:
            if self.X is None or self.y is None:
                print("❌ Error: Data not prepared. Call prepare_data() first.")
                return False
            
            print(f"\n🤖 Training KNN model (n_neighbors={self.n_neighbors})...")
            
            # Fit the model
            self.model.fit(self.X, self.y)
            
            self.is_trained = True
            print(f"✅ Model trained successfully!")
            print(f"   Training samples: {len(self.X)}")
            print(f"   Features: {len(self.X.columns)}")
            print(f"   Classes: {len(self.model.classes_)}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error training model: {str(e)}")
            return False
    
    def get_model_info(self) -> dict:
        """Get information about the trained model."""
        if not self.is_trained:
            return {"status": "Model not trained yet"}
        
        return {
            "status": "Model trained",
            "algorithm": "KNeighborsClassifier",
            "n_neighbors": self.n_neighbors,
            "n_training_samples": len(self.X),
            "n_features": len(self.X.columns),
            "feature_names": list(self.X.columns),
            "n_classes": len(self.model.classes_),
            "classes": list(self.model.classes_),
            "is_trained": self.is_trained
        }
    
    def print_model_summary(self) -> None:
        """Print a summary of the trained model."""
        if not self.is_trained:
            print("❌ Model not trained yet")
            return
        
        print("\n" + "="*70)
        print("🤖 MODEL SUMMARY")
        print("="*70)
        
        info = self.get_model_info()
        
        print(f"\n📊 Model Details:")
        print(f"   Algorithm: {info['algorithm']}")
        print(f"   n_neighbors: {info['n_neighbors']}")
        print(f"   Training samples: {info['n_training_samples']}")
        print(f"   Feature count: {info['n_features']}")
        print(f"   Feature names: {info['feature_names']}")
        print(f"   Classes: {info['n_classes']}")
        print(f"   Status: {info['status']}")
        
        print(f"\n🎯 Target Classes ({info['n_classes']} total):")
        for i, cls in enumerate(self.model.classes_[:10]):
            count = (self.y == cls).sum()
            print(f"   {i}: {cls} ({count} samples)")
        
        if len(self.model.classes_) > 10:
            print(f"   ... and {len(self.model.classes_) - 10} more classes")
        
        print("="*70)
    
    def get_model(self):
        """Return the trained model."""
        return self.model if self.is_trained else None


def main():
    """Execute Block 4: Model Training."""
    
    print("\n" + "="*70)
    print("🔷 BLOCK 4: MODEL TRAINING (CLASSIFICATION)")
    print("="*70)
    
    # Step 1: Load data from Block 1
    print("\n📥 Loading data from Block 1...")
    df_main = load_celestia_dataset()
    
    if df_main is None:
        print("❌ Failed to load data from Block 1")
        return None, None
    
    # Step 2: Clean data from Block 2
    print("\n🧹 Cleaning data from Block 2...")
    df_cleaned = clean_dataset(df_main)
    
    if df_cleaned is None:
        print("❌ Failed to clean dataset from Block 2")
        return None, None
    
    # Step 3: Encode data from Block 3
    print("\n🔐 Encoding data from Block 3...")
    manager = EncodingManager()
    df_encoded = manager.encode_dataset(df_cleaned)
    
    if df_encoded is None:
        print("❌ Failed to encode dataset from Block 3")
        return None, None
    
    print(f"✅ Encoded dataset ready: {df_encoded.shape[0]} rows × {df_encoded.shape[1]} columns")
    
    # Step 4: Create and train model
    print("\n🎯 Creating and training KNN model...")
    trainer = ModelTrainer(n_neighbors=3)
    
    # Prepare features and target
    print("\n📊 Preparing features and target...")
    X, y = trainer.prepare_data(df_encoded)
    
    if X is None or y is None:
        print("❌ Failed to prepare data")
        return None, None
    
    # Train the model
    print()
    success = trainer.train()
    
    if not success:
        print("❌ Failed to train model")
        return None, None
    
    # Print model summary
    trainer.print_model_summary()
    
    print("\n✨ Block 4 Model Training Complete!")
    print("   Ready for Block 5 (Model Evaluation & Predictions)")
    print("="*70 + "\n")
    
    return trainer.get_model(), trainer


if __name__ == "__main__":
    model, trainer = main()
