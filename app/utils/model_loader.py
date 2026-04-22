"""
🔷 BLOCK 7: LOAD MODELS - Load Pre-trained Models from Disk

Purpose: Load trained models and encoders from pickle files to avoid retraining
         Enables fast inference without rebuilding the pipeline

Models to load:
  - knn_model.pkl (Block 4 trained KNeighborsClassifier)
  - kmeans_model.pkl (Block 5 trained KMeans)
  - le_skin.pkl (Block 3 LabelEncoder for Skin_Type)
  - le_sens.pkl (Block 3 LabelEncoder for Sensitivity)
  - le_concern.pkl (Block 3 LabelEncoder for Concern)
  - le_target.pkl (Block 3 LabelEncoder for clean_Ingredients)

Load Location: data/ folder

Data Flow:
  Block 6 (Save) → Block 7 (Load)

Block 7 ONLY handles loading - no training, no saving.
"""

from typing import Optional, Dict, Any, Tuple
import pickle
from pathlib import Path


class ModelLoader:
    """
    Manages loading of pre-trained models and encoders from disk.
    
    Attributes:
        data_dir (Path): Directory to load models from
        models (dict): Loaded model objects
        encoders (dict): Loaded encoder objects
        load_status (dict): Status of each loaded file
        all_loaded (bool): Whether all required files loaded successfully
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize ModelLoader.
        
        Args:
            data_dir (str): Directory to load models from. Default: models/ folder
        """
        if data_dir is None:
            # Use models/ folder in project root
            base_dir = Path(__file__).parent.parent.parent
            data_dir = base_dir / "models"
        else:
            data_dir = Path(data_dir)
        
        self.data_dir = data_dir
        self.models = {}
        self.encoders = {}
        self.load_status = {}
        self.all_loaded = False
    
    def load_model(self, model_name: str) -> bool:
        """
        Load a single model from disk.
        
        Args:
            model_name (str): Model name (will be loaded from name.pkl)
            
        Returns:
            bool: True if load successful, False otherwise
        """
        file_path = self.data_dir / f"{model_name}.pkl"
        
        if not file_path.exists():
            self.load_status[model_name] = {
                'status': 'failed',
                'error': f'File not found: {file_path}'
            }
            print(f"   ❌ {model_name}.pkl not found at {file_path}")
            return False
        
        try:
            with open(file_path, 'rb') as f:
                model_obj = pickle.load(f)
            
            self.models[model_name] = model_obj
            
            self.load_status[model_name] = {
                'status': 'loaded',
                'path': str(file_path),
                'size': file_path.stat().st_size
            }
            
            print(f"   ✅ {model_name}.pkl loaded ({file_path.stat().st_size} bytes)")
            return True
        
        except Exception as e:
            self.load_status[model_name] = {
                'status': 'failed',
                'error': str(e)
            }
            print(f"   ❌ {model_name}.pkl failed to load: {e}")
            return False
    
    def load_encoder(self, encoder_name: str) -> bool:
        """
        Load a single encoder from disk.
        
        Args:
            encoder_name (str): Encoder name (will be loaded from name.pkl)
            
        Returns:
            bool: True if load successful, False otherwise
        """
        file_path = self.data_dir / f"{encoder_name}.pkl"
        
        if not file_path.exists():
            self.load_status[encoder_name] = {
                'status': 'failed',
                'error': f'File not found: {file_path}'
            }
            print(f"   ❌ {encoder_name}.pkl not found at {file_path}")
            return False
        
        try:
            with open(file_path, 'rb') as f:
                encoder_obj = pickle.load(f)
            
            self.encoders[encoder_name] = encoder_obj
            
            self.load_status[encoder_name] = {
                'status': 'loaded',
                'path': str(file_path),
                'size': file_path.stat().st_size
            }
            
            print(f"   ✅ {encoder_name}.pkl loaded ({file_path.stat().st_size} bytes)")
            return True
        
        except Exception as e:
            self.load_status[encoder_name] = {
                'status': 'failed',
                'error': str(e)
            }
            print(f"   ❌ {encoder_name}.pkl failed to load: {e}")
            return False
    
    def load_all_models(self) -> bool:
        """
        Load all required models from disk.
        
        Loads: knn_model.pkl, kmeans_model.pkl
        
        Returns:
            bool: True if all loads successful, False otherwise
        """
        print("\n🤖 Loading ML Models...")
        
        model_names = ['knn_model', 'kmeans_model']
        all_success = True
        
        for model_name in model_names:
            if not self.load_model(model_name):
                all_success = False
        
        return all_success
    
    def load_all_encoders(self) -> bool:
        """
        Load all required encoders from disk.
        
        Loads: le_skin.pkl, le_sens.pkl, le_concern.pkl, le_target.pkl
        
        Returns:
            bool: True if all loads successful, False otherwise
        """
        print("\n🔐 Loading Encoders...")
        
        encoder_names = ['le_skin', 'le_sens', 'le_concern', 'le_target']
        all_success = True
        
        for encoder_name in encoder_names:
            if not self.load_encoder(encoder_name):
                all_success = False
        
        return all_success
    
    def load_all(self) -> bool:
        """
        Load all models and encoders from disk.
        
        Returns:
            bool: True if all loads successful, False otherwise
        """
        print(f"\n📁 Loading from: {self.data_dir}")
        
        # Load all models
        models_success = self.load_all_models()
        
        # Load all encoders
        encoders_success = self.load_all_encoders()
        
        # Set flag
        self.all_loaded = models_success and encoders_success
        
        return self.all_loaded
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """
        Get a loaded model by name.
        
        Args:
            model_name (str): Model name
            
        Returns:
            Model object or None if not loaded
        """
        if model_name not in self.models:
            print(f"❌ Model '{model_name}' not loaded")
            return None
        
        return self.models[model_name]
    
    def get_encoder(self, encoder_name: str) -> Optional[Any]:
        """
        Get a loaded encoder by name.
        
        Args:
            encoder_name (str): Encoder name
            
        Returns:
            Encoder object or None if not loaded
        """
        if encoder_name not in self.encoders:
            print(f"❌ Encoder '{encoder_name}' not loaded")
            return None
        
        return self.encoders[encoder_name]
    
    def get_all_models(self) -> Dict[str, Any]:
        """
        Get all loaded models.
        
        Returns:
            dict: {model_name: model_object}
        """
        return self.models.copy()
    
    def get_all_encoders(self) -> Dict[str, Any]:
        """
        Get all loaded encoders.
        
        Returns:
            dict: {encoder_name: encoder_object}
        """
        return self.encoders.copy()
    
    def get_load_status(self) -> Dict[str, Any]:
        """
        Get status of all loaded files.
        
        Returns:
            dict: Status information for each file
        """
        return self.load_status.copy()
    
    def is_ready(self) -> bool:
        """
        Check if all required models/encoders are loaded.
        
        Returns:
            bool: True if all loaded successfully
        """
        return self.all_loaded
    
    def print_load_summary(self) -> None:
        """
        Print detailed load summary.
        """
        print("\n📊 LOAD SUMMARY")
        print("━" * 60)
        
        print("\n📁 Load Location:")
        print(f"   {self.data_dir}")
        
        print("\n✅ Models Loaded:")
        model_count = 0
        total_size = 0
        for model_name, status in self.load_status.items():
            if 'model' in model_name or 'kmeans' in model_name:
                if status['status'] == 'loaded':
                    size = status['size']
                    total_size += size
                    print(f"   ✅ {model_name}.pkl ({size} bytes)")
                    model_count += 1
                else:
                    print(f"   ❌ {model_name}.pkl (Failed: {status.get('error', 'Unknown')})")
        
        print("\n🔐 Encoders Loaded:")
        encoder_count = 0
        for encoder_name, status in self.load_status.items():
            if encoder_name.startswith('le_'):
                if status['status'] == 'loaded':
                    size = status['size']
                    total_size += size
                    print(f"   ✅ {encoder_name}.pkl ({size} bytes)")
                    encoder_count += 1
                else:
                    print(f"   ❌ {encoder_name}.pkl (Failed: {status.get('error', 'Unknown')})")
        
        print(f"\n📈 Statistics:")
        print(f"   Models loaded: {model_count}")
        print(f"   Encoders loaded: {encoder_count}")
        print(f"   Total size: {total_size} bytes ({total_size / 1024:.2f} KB)")
        print(f"   Status: {'✅ Ready' if self.all_loaded else '❌ Incomplete'}")
        
        print("\n✨ All models loaded successfully!")
        print("━" * 60)
    
    # ========== PROPERTY ACCESSORS ==========
    @property
    def knn_model(self):
        """Get KNN model."""
        return self.get_model('knn_model')
    
    @property
    def kmeans_model(self):
        """Get KMeans model."""
        return self.get_model('kmeans_model')
    
    @property
    def le_skin(self):
        """Get skin type encoder."""
        return self.get_encoder('le_skin')
    
    @property
    def le_sens(self):
        """Get sensitivity encoder."""
        return self.get_encoder('le_sens')
    
    @property
    def le_concern(self):
        """Get concern encoder."""
        return self.get_encoder('le_concern')
    
    @property
    def le_target(self):
        """Get target ingredient encoder."""
        return self.get_encoder('le_target')


def main() -> Tuple[bool, Optional[ModelLoader]]:
    """
    Execute complete Block 7 model loading pipeline.
    
    Pipeline:
        Block 6 (Save) → Block 7 (Load)
    
    Returns:
        Tuple[bool, ModelLoader]: (success, loader)
    """
    print("\n🔷 BLOCK 7: LOAD MODELS (AVOID RETRAINING)")
    print("=" * 60)
    
    # Step 1: Create loader
    print("\n📦 Creating model loader...")
    loader = ModelLoader()
    
    # Step 2: Load all models and encoders
    print("\n⏳ Loading all models and encoders from disk...")
    if not loader.load_all():
        print("\n❌ Failed to load some files")
        loader.print_load_summary()
        return False, loader
    
    # Step 3: Print summary
    loader.print_load_summary()
    
    return True, loader


if __name__ == '__main__':
    success, loader = main()
    
    if success and loader is not None:
        print("\n✅ Block 7 Model Loading Complete!")
        print("   Status: All models and encoders loaded successfully")
        print("   Ready for: Block 8+ (Use loaded models in application)")
        
        # Show loaded models
        print("\n📋 Loaded Models and Encoders:")
        print(f"   - KNN Model: {loader.get_model('knn_model') is not None}")
        print(f"   - KMeans Model: {loader.get_model('kmeans_model') is not None}")
        print(f"   - Skin Encoder: {loader.get_encoder('le_skin') is not None}")
        print(f"   - Sensitivity Encoder: {loader.get_encoder('le_sens') is not None}")
        print(f"   - Concern Encoder: {loader.get_encoder('le_concern') is not None}")
        print(f"   - Target Encoder: {loader.get_encoder('le_target') is not None}")
    else:
        print("\n❌ Block 7 Model Loading Failed")
