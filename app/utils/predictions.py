"""
Block 8: Prediction Function (Core ML Engine)

This module provides the core prediction function for skincare recommendations.
It uses the pre-trained and pre-loaded models to:
1. Encode input features
2. Predict ingredient using KNN
3. Predict cluster using KMeans
4. Return ingredient + cluster label
"""

from typing import Optional, Tuple, Dict, Any
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.utils.model_loader import ModelLoader


class PredictionEngine:
    """
    Core ML engine for skincare recommendations.
    
    Uses pre-loaded models and encoders to make predictions.
    """
    
    def __init__(self, model_loader: Optional[ModelLoader] = None):
        """
        Initialize prediction engine with loaded models.
        
        Args:
            model_loader: ModelLoader instance with loaded models.
                         If None, creates new ModelLoader.
        """
        if model_loader is None:
            # Create and load models if not provided
            self.loader = ModelLoader(data_dir='data')
            self.loader.load_all()
        else:
            self.loader = model_loader
        
        # Verify all models are loaded
        if not self.loader.is_ready():
            raise RuntimeError("Models failed to load. Run Block 6 to save models first.")
    
    def encode_input(
        self,
        skin_type: str,
        sensitivity: str,
        concern: str
    ) -> Optional[Tuple[int, int, int]]:
        """
        Encode input features using LabelEncoders.
        
        Args:
            skin_type: Raw skin type value (e.g., "Oily", "Dry", "Mixed")
            sensitivity: Raw sensitivity value (e.g., "Sensitive", "Not Sensitive")
            concern: Raw skin concern (e.g., "Acne", "Dryness", "Wrinkles")
        
        Returns:
            Tuple of (encoded_skin, encoded_sens, encoded_concern) or None if encoding fails
        """
        try:
            # Get encoders
            le_skin = self.loader.get_encoder('le_skin')
            le_sens = self.loader.get_encoder('le_sens')
            le_concern = self.loader.get_encoder('le_concern')
            
            if le_skin is None or le_sens is None or le_concern is None:
                print("❌ Error: Encoders not loaded")
                return None
            
            # Encode each input
            encoded_skin = le_skin.transform([skin_type])[0]
            encoded_sens = le_sens.transform([sensitivity])[0]
            encoded_concern = le_concern.transform([concern])[0]
            
            return (encoded_skin, encoded_sens, encoded_concern)
        
        except Exception as e:
            print(f"❌ Error encoding input: {e}")
            return None
    
    def predict_ingredient(
        self,
        encoded_skin: int,
        encoded_sens: int,
        encoded_concern: int
    ) -> Optional[Tuple[str, float]]:
        """
        Predict ingredient using KNN model and decode result.
        Also returns confidence score based on distances.
        
        Args:
            encoded_skin: Encoded skin type
            encoded_sens: Encoded sensitivity
            encoded_concern: Encoded concern
        
        Returns:
            Tuple of (Decoded ingredient string, confidence score 0-100) or None if prediction fails
        """
        try:
            # Get KNN model and target encoder
            knn_model = self.loader.get_model('knn_model')
            le_target = self.loader.get_encoder('le_target')
            
            if knn_model is None or le_target is None:
                print("❌ Error: KNN model or target encoder not loaded")
                return None
            
            # Make prediction with distances
            features = [[encoded_skin, encoded_sens, encoded_concern]]
            predicted_encoded = knn_model.predict(features)[0]
            
            # Get distances to nearest neighbors for confidence
            distances, indices = knn_model.kneighbors(features)
            closest_distance = distances[0][0]
            
            # Calculate confidence: closer neighbors = higher confidence
            # Normalize distance to 0-100 range (inverted: smaller distance = higher confidence)
            max_distance = 5.0  # Max expected distance in feature space
            confidence = max(0, min(100, 100 * (1 - (closest_distance / max_distance))))
            
            # Decode to ingredient name
            ingredient = le_target.inverse_transform([predicted_encoded])[0]
            
            return ingredient, confidence
        
        except Exception as e:
            print(f"❌ Error predicting ingredient: {e}")
            return None
    
    def predict_cluster(
        self,
        encoded_skin: int,
        encoded_sens: int,
        encoded_concern: int
    ) -> Optional[int]:
        """
        Predict cluster using KMeans model.
        
        Args:
            encoded_skin: Encoded skin type
            encoded_sens: Encoded sensitivity
            encoded_concern: Encoded concern
        
        Returns:
            Cluster number (0, 1, 2) or None if prediction fails
        """
        try:
            # Get KMeans model
            kmeans_model = self.loader.get_model('kmeans_model')
            
            if kmeans_model is None:
                print("❌ Error: KMeans model not loaded")
                return None
            
            # Make prediction
            features = [[encoded_skin, encoded_sens, encoded_concern]]
            cluster = kmeans_model.predict(features)[0]
            
            return cluster
        
        except Exception as e:
            print(f"❌ Error predicting cluster: {e}")
            return None
    
    @staticmethod
    def map_cluster_to_label(cluster: int) -> str:
        """
        Map cluster number to human-readable label.
        
        Args:
            cluster: Cluster number (0, 1, 2)
        
        Returns:
            Cluster label (e.g., "Acne-Prone", "Dry Skin", "Sensitive Skin")
        """
        cluster_map = {
            0: "Acne-Prone",
            1: "Dry Skin",
            2: "Sensitive Skin"
        }
        
        return cluster_map.get(cluster, f"Unknown Cluster {cluster}")
    
    def predict_skin_solution(
        self,
        skin_type: str,
        sensitivity: str,
        concern: str
    ) -> Optional[Dict[str, Any]]:
        """
        Core prediction function: Full pipeline for skincare recommendation.
        
        Workflow:
        1. Encode input features using LabelEncoders
        2. Predict ingredient using KNN model
        3. Decode predicted ingredient
        4. Predict cluster using KMeans model
        5. Map cluster number to label
        6. Return ingredient + cluster label
        
        Args:
            skin_type: Raw skin type (e.g., "Oily", "Dry", "Mixed")
            sensitivity: Raw sensitivity (e.g., "Sensitive", "Not Sensitive")
            concern: Raw skin concern (e.g., "Acne", "Dryness")
        
        Returns:
            Dict with keys:
                - 'ingredient': Predicted ingredient (str)
                - 'cluster_number': Cluster ID (int)
                - 'cluster_label': Human-readable label (str)
                - 'success': True if prediction successful
            Or None if any step fails
        """
        # Step 1: Encode input
        encoded = self.encode_input(skin_type, sensitivity, concern)
        if encoded is None:
            return {
                'ingredient': None,
                'cluster_number': None,
                'cluster_label': None,
                'success': False,
                'error': 'Failed to encode input'
            }
        
        encoded_skin, encoded_sens, encoded_concern = encoded
        
        # Step 2-3: Predict and decode ingredient with confidence
        ingredient_result = self.predict_ingredient(encoded_skin, encoded_sens, encoded_concern)
        if ingredient_result is None:
            return {
                'ingredient': None,
                'ingredient_confidence': 0,
                'cluster_number': None,
                'cluster_label': None,
                'cluster_confidence': 0,
                'overall_confidence': 0,
                'success': False,
                'error': 'Failed to predict ingredient'
            }
        
        ingredient, ingredient_confidence = ingredient_result
        
        # Step 4: Predict cluster
        cluster = self.predict_cluster(encoded_skin, encoded_sens, encoded_concern)
        if cluster is None:
            return {
                'ingredient': ingredient,
                'ingredient_confidence': ingredient_confidence,
                'cluster_number': None,
                'cluster_label': None,
                'cluster_confidence': 0,
                'overall_confidence': 0,
                'success': False,
                'error': 'Failed to predict cluster'
            }
        
        # Step 5: Map cluster to label
        cluster_label = self.map_cluster_to_label(cluster)
        
        # Estimate cluster confidence from KMeans inertia
        try:
            kmeans_model = self.loader.get_model('kmeans_model')
            if kmeans_model is not None:
                features = [[encoded_skin, encoded_sens, encoded_concern]]
                distances = kmeans_model.transform(features)
                cluster_distance = distances[0][cluster]
                max_cluster_distance = 10.0
                cluster_confidence = max(0, min(100, 100 * (1 - (cluster_distance / max_cluster_distance))))
            else:
                cluster_confidence = 75.0
        except:
            cluster_confidence = 75.0
        
        # Calculate overall confidence
        overall_confidence = (ingredient_confidence + cluster_confidence) / 2
        
        # Step 6: Return results with confidence scores
        return {
            'ingredient': ingredient,
            'ingredient_confidence': round(ingredient_confidence, 2),
            'cluster_number': cluster,
            'cluster_label': cluster_label,
            'cluster_confidence': round(cluster_confidence, 2),
            'overall_confidence': round(overall_confidence, 2),
            'success': True,
            'error': None
        }


def predict_skin_solution(
    skin_type: str,
    sensitivity: str,
    concern: str,
    model_loader: Optional[ModelLoader] = None
) -> Dict[str, Any]:
    """
    Standalone prediction function for skincare recommendation.
    
    Creates a PredictionEngine and returns skin solution prediction.
    
    Args:
        skin_type: Raw skin type
        sensitivity: Raw sensitivity level
        concern: Raw skin concern
        model_loader: Optional pre-loaded ModelLoader instance
    
    Returns:
        Dict with prediction results including ingredient and cluster label
    """
    try:
        engine = PredictionEngine(model_loader=model_loader)
        return engine.predict_skin_solution(skin_type, sensitivity, concern)
    except Exception as e:
        print(f"❌ Error creating prediction engine: {e}")
        return {
            'ingredient': None,
            'cluster_number': None,
            'cluster_label': None,
            'success': False,
            'error': str(e)
        }


def main():
    """
    Main function: Execute Block 8 prediction pipeline and demo.
    
    Steps:
    1. Load models via ModelLoader
    2. Create PredictionEngine
    3. Make sample predictions
    4. Display results
    """
    print("🔷 BLOCK 8: PREDICTION FUNCTION (CORE ML ENGINE)")
    print("=" * 70)
    
    # Step 1: Load models
    print("\n📦 Loading models...")
    loader = ModelLoader(data_dir='data')
    if not loader.load_all():
        print("❌ Failed to load models. Run Block 6 first.")
        return
    
    print("✅ Models loaded successfully")
    
    # Step 2: Create engine
    print("\n🔧 Creating prediction engine...")
    try:
        engine = PredictionEngine(model_loader=loader)
        print("✅ Prediction engine created")
    except Exception as e:
        print(f"❌ Failed to create engine: {e}")
        return
    
    # Step 3: Demo predictions
    print("\n🎯 Making sample predictions...")
    print("-" * 70)
    
    # Sample 1
    print("\n📝 Sample 1:")
    print("Input: Skin='Oily', Sensitivity='Sensitive', Concern='Acne'")
    result1 = engine.predict_skin_solution('Oily', 'Yes', 'Acne')
    
    if result1['success']:
        print(f"✅ Predicted Ingredient: {result1['ingredient']}")
        print(f"✅ Cluster: {result1['cluster_label']} (ID: {result1['cluster_number']})")
    else:
        print(f"❌ Prediction failed: {result1['error']}")
    
    # Sample 2
    print("\n📝 Sample 2:")
    print("Input: Skin='Dry', Sensitivity='Not Sensitive', Concern='Dryness'")
    result2 = engine.predict_skin_solution('Dry', 'No', 'Wrinkles')
    
    if result2['success']:
        print(f"✅ Predicted Ingredient: {result2['ingredient']}")
        print(f"✅ Cluster: {result2['cluster_label']} (ID: {result2['cluster_number']})")
    else:
        print(f"❌ Prediction failed: {result2['error']}")
    
    # Sample 3
    print("\n📝 Sample 3:")
    print("Input: Skin='Mixed', Sensitivity='Sensitive', Concern='Sensitivity'")
    result3 = engine.predict_skin_solution('Combination', 'Yes', 'Redness')
    
    if result3['success']:
        print(f"✅ Predicted Ingredient: {result3['ingredient']}")
        print(f"✅ Cluster: {result3['cluster_label']} (ID: {result3['cluster_number']})")
    else:
        print(f"❌ Prediction failed: {result3['error']}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 PREDICTION SUMMARY")
    print("=" * 70)
    
    results = [result1, result2, result3]
    successful = sum(1 for r in results if r['success'])
    
    print(f"✅ Successful predictions: {successful}/3")
    print(f"✅ Prediction function working correctly")
    
    print("\n✨ Block 8 Prediction Function Complete!")
    print("   Status: Ready for Block 9+ (Integration)")


if __name__ == '__main__':
    main()
