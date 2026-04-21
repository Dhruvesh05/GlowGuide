"""
🔷 BLOCK 6: SAVE MODELS - Model Persistence using Pickle

Purpose: Save trained models and encoders to disk for reuse in future blocks
         Enables loading pre-trained models without retraining

Models to save:
  - knn_model.pkl (Block 4 trained KNeighborsClassifier)
  - kmeans_model.pkl (Block 5 trained KMeans)
  - le_skin.pkl (Block 3 LabelEncoder for Skin_Type)
  - le_sens.pkl (Block 3 LabelEncoder for Sensitivity)
  - le_concern.pkl (Block 3 LabelEncoder for Concern)
  - le_target.pkl (Block 3 LabelEncoder for clean_Ingredients)

Save Location: data/ folder (persistent storage)

Data Flow:
  Block 3 (Encoders) + Block 4 (KNN) + Block 5 (KMeans) → Block 6 (Save)

Block 6 ONLY handles saving - no training, no loading yet.
"""

from typing import Optional, Dict, Any, Tuple
import pickle
import os
from pathlib import Path

# Import from previous blocks
from app.utils.data_loader import load_celestia_dataset
from app.utils.preprocessing import clean_dataset
from app.utils.encoding import EncodingManager
from app.utils.training import ModelTrainer
from app.utils.clustering import ClusteringManager


class ModelPersistence:
    """
    Manages saving and loading of trained models and encoders.
    
    Attributes:
        data_dir (Path): Directory to save/load models
        models (dict): Dictionary of model objects
        encoders (dict): Dictionary of encoder objects
        save_status (dict): Status of each saved file
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize ModelPersistence.
        
        Args:
            data_dir (str): Directory to save models. Default: data/ folder
        """
        if data_dir is None:
            # Use data/ folder in project root
            base_dir = Path(__file__).parent.parent.parent
            data_dir = base_dir / "data"
        else:
            data_dir = Path(data_dir)
        
        self.data_dir = data_dir
        self.models = {}
        self.encoders = {}
        self.save_status = {}
    
    def add_model(self, name: str, model: Any) -> None:
        """
        Add a model to be saved.
        
        Args:
            name (str): Model name (will be saved as name.pkl)
            model: Model object to save
        """
        self.models[name] = model
    
    def add_encoder(self, name: str, encoder: Any) -> None:
        """
        Add an encoder to be saved.
        
        Args:
            name (str): Encoder name (will be saved as name.pkl)
            encoder: Encoder object to save
        """
        self.encoders[name] = encoder
    
    def save_models(self) -> bool:
        """
        Save all registered models to disk using pickle.
        
        Returns:
            bool: True if all saves successful, False otherwise
        """
        try:
            # Create data directory if it doesn't exist
            self.data_dir.mkdir(parents=True, exist_ok=True)
            print(f"\n💾 Saving models to: {self.data_dir}")
            
            # Save all models
            for model_name, model_obj in self.models.items():
                file_path = self.data_dir / f"{model_name}.pkl"
                
                try:
                    with open(file_path, 'wb') as f:
                        pickle.dump(model_obj, f)
                    
                    self.save_status[model_name] = {
                        'status': 'saved',
                        'path': str(file_path),
                        'size': os.path.getsize(file_path)
                    }
                    
                    print(f"   ✅ {model_name}.pkl saved ({os.path.getsize(file_path)} bytes)")
                
                except Exception as e:
                    self.save_status[model_name] = {
                        'status': 'failed',
                        'error': str(e)
                    }
                    print(f"   ❌ {model_name}.pkl failed: {e}")
                    return False
            
            # Save all encoders
            for encoder_name, encoder_obj in self.encoders.items():
                file_path = self.data_dir / f"{encoder_name}.pkl"
                
                try:
                    with open(file_path, 'wb') as f:
                        pickle.dump(encoder_obj, f)
                    
                    self.save_status[encoder_name] = {
                        'status': 'saved',
                        'path': str(file_path),
                        'size': os.path.getsize(file_path)
                    }
                    
                    print(f"   ✅ {encoder_name}.pkl saved ({os.path.getsize(file_path)} bytes)")
                
                except Exception as e:
                    self.save_status[encoder_name] = {
                        'status': 'failed',
                        'error': str(e)
                    }
                    print(f"   ❌ {encoder_name}.pkl failed: {e}")
                    return False
            
            return True
        
        except Exception as e:
            print(f"❌ Error saving models: {e}")
            return False
    
    def load_models(self, model_names: list) -> Dict[str, Any]:
        """
        Load saved models from disk.
        
        Args:
            model_names (list): List of model names to load
            
        Returns:
            dict: {model_name: model_object} or empty dict if failed
        """
        loaded = {}
        
        for model_name in model_names:
            file_path = self.data_dir / f"{model_name}.pkl"
            
            if not file_path.exists():
                print(f"❌ {model_name}.pkl not found at {file_path}")
                return {}
            
            try:
                with open(file_path, 'rb') as f:
                    model_obj = pickle.load(f)
                loaded[model_name] = model_obj
                print(f"✅ {model_name}.pkl loaded")
            
            except Exception as e:
                print(f"❌ Error loading {model_name}.pkl: {e}")
                return {}
        
        return loaded
    
    def get_save_status(self) -> Dict[str, Any]:
        """
        Get status of all saved files.
        
        Returns:
            dict: Status information for each file
        """
        return self.save_status
    
    def print_save_summary(self) -> None:
        """
        Print detailed save summary.
        """
        print("\n📊 SAVE SUMMARY")
        print("━" * 60)
        
        print("\n📁 Save Location:")
        print(f"   {self.data_dir}")
        
        print("\n💾 Models Saved:")
        model_count = 0
        total_size = 0
        for model_name, status in self.save_status.items():
            if status['status'] == 'saved':
                size = status['size']
                total_size += size
                print(f"   ✅ {model_name}.pkl ({size} bytes)")
                model_count += 1
            else:
                print(f"   ❌ {model_name}.pkl (Failed: {status.get('error', 'Unknown')})")
        
        print(f"\n📈 Statistics:")
        print(f"   Files saved: {model_count}")
        print(f"   Total size: {total_size} bytes ({total_size / 1024:.2f} KB)")
        
        print("\n✨ All models persisted successfully!")
        print("━" * 60)


def main() -> Tuple[bool, Optional[ModelPersistence]]:
    """
    Execute complete Block 6 model persistence pipeline.
    
    Pipeline:
        Block 1-5 (Train) → Block 6 (Save)
    
    Returns:
        Tuple[bool, ModelPersistence]: (success, persistence_manager)
    """
    print("\n🔷 BLOCK 6: SAVE MODELS (MODEL PERSISTENCE)")
    print("=" * 60)
    
    # Step 1: Load data and train models from previous blocks
    print("\n📥 Loading and training models from previous blocks...")
    
    # Load and clean data
    df_main = load_celestia_dataset()
    if df_main is None:
        print("❌ Failed to load data")
        return False, None
    
    df_cleaned = clean_dataset(df_main)
    if df_cleaned is None:
        print("❌ Failed to clean data")
        return False, None
    
    # Encode data (Block 3)
    print("\n🔐 Creating encoders from Block 3...")
    encoding_manager = EncodingManager()
    df_encoded = encoding_manager.encode_dataset(df_cleaned)
    if df_encoded is None:
        print("❌ Failed to encode data")
        return False, None
    
    print("✅ Encoders ready")
    
    # Train KNN model (Block 4)
    print("\n🤖 Training KNN model from Block 4...")
    trainer = ModelTrainer(n_neighbors=3)
    X, y = trainer.prepare_data(df_encoded)
    trainer.train()
    
    if not trainer.is_trained:
        print("❌ Failed to train KNN model")
        return False, None
    
    print("✅ KNN model trained")
    
    # Train KMeans model (Block 5)
    print("\n🔷 Training KMeans model from Block 5...")
    clustering = ClusteringManager(n_clusters=3)
    clustering.extract_features(df_encoded)
    clustering.fit_kmeans()
    
    if not clustering.is_fitted:
        print("❌ Failed to fit KMeans model")
        return False, None
    
    print("✅ KMeans model trained")
    
    # Step 2: Create persistence manager
    print("\n💾 Creating model persistence manager...")
    persistence = ModelPersistence()
    
    # Step 3: Register models for saving
    print("\n📝 Registering models for saving...")
    
    # Add KNN model
    persistence.add_model('knn_model', trainer.get_model())
    print("   ✅ Registered: knn_model")
    
    # Add KMeans model
    persistence.add_model('kmeans_model', clustering.get_model())
    print("   ✅ Registered: kmeans_model")
    
    # Add encoders
    encoders_dict = encoding_manager.get_encoders_dict()
    persistence.add_encoder('le_skin', encoders_dict['le_skin'])
    persistence.add_encoder('le_sens', encoders_dict['le_sens'])
    persistence.add_encoder('le_concern', encoders_dict['le_concern'])
    persistence.add_encoder('le_target', encoders_dict['le_target'])
    print("   ✅ Registered: le_skin, le_sens, le_concern, le_target")
    
    # Step 4: Save all models and encoders
    print("\n💾 Saving models and encoders to disk...")
    if not persistence.save_models():
        print("❌ Failed to save models")
        return False, None
    
    # Step 5: Print summary
    persistence.print_save_summary()
    
    return True, persistence


if __name__ == '__main__':
    success, persistence = main()
    
    if success and persistence is not None:
        print("\n✅ Block 6 Model Persistence Complete!")
        print("   Status: All models saved successfully")
        print("   Ready for: Block 7 (Load and use models)")
    else:
        print("\n❌ Block 6 Model Persistence Failed")
