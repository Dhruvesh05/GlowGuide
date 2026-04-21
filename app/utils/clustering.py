"""
🔷 BLOCK 5: CLUSTERING - User Segmentation using KMeans

Purpose: Segment users into 3 clusters based on skin features
         (Skin_Type, Sensitivity, Concern)

This module implements KMeans clustering to group users into:
  - Cluster 0: Acne-Prone
  - Cluster 1: Dry Skin
  - Cluster 2: Sensitive Skin

Data Flow:
  Block 1 (Load) → Block 2 (Clean) → Block 3 (Encode) → Block 5 (Cluster)

Block 5 ONLY handles clustering - no evaluation, no predictions yet.
"""

from typing import Optional, Tuple, Dict, Any
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Import from previous blocks
from app.utils.data_loader import load_celestia_dataset
from app.utils.preprocessing import clean_dataset
from app.utils.encoding import EncodingManager


class ClusteringManager:
    """
    Manages KMeans clustering for user segmentation.
    
    Attributes:
        n_clusters (int): Number of clusters (3)
        feature_columns (list): Feature column names
        cluster_labels (dict): Mapping of cluster ID to label name
        model (KMeans): Fitted KMeans model
        clusters (np.array): Cluster assignments for each sample
        is_fitted (bool): Whether model is fitted
    """
    
    def __init__(self, n_clusters: int = 3):
        """
        Initialize ClusteringManager.
        
        Args:
            n_clusters (int): Number of clusters. Default: 3
        """
        self.n_clusters = n_clusters
        self.feature_columns = ['Skin_Type', 'Sensitivity', 'Concern']
        
        # Cluster labels mapping
        self.cluster_labels = {
            0: 'Acne-Prone',
            1: 'Dry Skin',
            2: 'Sensitive Skin'
        }
        
        # Model and data
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.X = None
        self.clusters = None
        self.is_fitted = False
    
    def extract_features(self, df_encoded: pd.DataFrame) -> bool:
        """
        Extract features from encoded dataset.
        
        Args:
            df_encoded (pd.DataFrame): Encoded dataset from Block 3
            
        Returns:
            bool: True if extraction successful, False otherwise
        """
        try:
            # Check if all required columns exist
            for col in self.feature_columns:
                if col not in df_encoded.columns:
                    print(f"❌ Column '{col}' not found in encoded data")
                    return False
            
            # Extract features
            self.X = df_encoded[self.feature_columns].values
            
            # Validate shape
            if self.X.shape[0] == 0:
                print("❌ No samples found")
                return False
            
            if self.X.shape[1] != len(self.feature_columns):
                print(f"❌ Expected {len(self.feature_columns)} features, got {self.X.shape[1]}")
                return False
            
            print(f"✅ Features extracted: {self.X.shape}")
            print(f"   Columns: {self.feature_columns}")
            print(f"   Data type: {self.X.dtype}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error extracting features: {e}")
            return False
    
    def fit_kmeans(self) -> bool:
        """
        Fit KMeans clustering model.
        
        Returns:
            bool: True if fitting successful, False otherwise
        """
        try:
            if self.X is None:
                print("❌ Features not extracted yet. Call extract_features() first.")
                return False
            
            print(f"\n🤖 Fitting KMeans clustering (n_clusters={self.n_clusters})...")
            
            # Fit the model
            self.model.fit(self.X)
            
            # Get cluster assignments
            self.clusters = self.model.labels_
            
            # Mark as fitted
            self.is_fitted = True
            
            print(f"✅ KMeans model fitted successfully!")
            print(f"   Samples used: {len(self.clusters)}")
            print(f"   Clusters: {self.n_clusters}")
            print(f"   Inertia: {self.model.inertia_:.2f}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error fitting KMeans: {e}")
            return False
    
    def get_cluster_assignments(self) -> Optional[np.ndarray]:
        """
        Get cluster assignments for all samples.
        
        Returns:
            np.ndarray: Array of cluster IDs (0-2) or None if not fitted
        """
        if not self.is_fitted or self.clusters is None:
            print("❌ Model not fitted yet. Call fit_kmeans() first.")
            return None
        
        return self.clusters
    
    def get_cluster_centers(self) -> Optional[np.ndarray]:
        """
        Get cluster centers in feature space.
        
        Returns:
            np.ndarray: Array of shape (n_clusters, n_features) or None if not fitted
        """
        if not self.is_fitted:
            print("❌ Model not fitted yet. Call fit_kmeans() first.")
            return None
        
        return self.model.cluster_centers_
    
    def get_cluster_distribution(self) -> Optional[Dict[str, int]]:
        """
        Get distribution of samples across clusters.
        
        Returns:
            dict: {cluster_label: count} or None if not fitted
        """
        if not self.is_fitted or self.clusters is None:
            print("❌ Model not fitted yet. Call fit_kmeans() first.")
            return None
        
        distribution = {}
        for cluster_id in range(self.n_clusters):
            label = self.cluster_labels[cluster_id]
            count = np.sum(self.clusters == cluster_id)
            distribution[label] = int(count)
        
        return distribution
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get comprehensive model information.
        
        Returns:
            dict: Model metadata
        """
        info = {
            'n_clusters': self.n_clusters,
            'n_features': len(self.feature_columns),
            'feature_names': self.feature_columns,
            'n_samples': len(self.clusters) if self.clusters is not None else 0,
            'cluster_labels': self.cluster_labels,
            'is_fitted': self.is_fitted,
            'inertia': self.model.inertia_ if self.is_fitted else None,
            'algorithm': 'KMeans',
            'random_state': 42,
            'n_init': 10
        }
        
        return info
    
    def get_model(self) -> Optional[KMeans]:
        """
        Get the fitted KMeans model.
        
        Returns:
            KMeans: Fitted model or None if not fitted
        """
        if not self.is_fitted:
            print("❌ Model not fitted yet. Call fit_kmeans() first.")
            return None
        
        return self.model
    
    def print_cluster_summary(self) -> None:
        """
        Print detailed cluster summary.
        """
        if not self.is_fitted:
            print("❌ Model not fitted yet. Call fit_kmeans() first.")
            return
        
        print("\n🎯 CLUSTER SUMMARY")
        print("━" * 60)
        
        # Model info
        print("\n📊 Model Details:")
        print(f"   Algorithm: KMeans")
        print(f"   n_clusters: {self.n_clusters}")
        print(f"   n_features: {len(self.feature_columns)}")
        print(f"   Features: {self.feature_columns}")
        print(f"   n_samples: {len(self.clusters)}")
        print(f"   Inertia: {self.model.inertia_:.2f}")
        
        # Cluster distribution
        distribution = self.get_cluster_distribution()
        print("\n🏷️  Cluster Distribution:")
        for cluster_id in range(self.n_clusters):
            label = self.cluster_labels[cluster_id]
            count = distribution[label]
            percentage = (count / len(self.clusters)) * 100
            print(f"   Cluster {cluster_id}: {label:20s} → {count:4d} samples ({percentage:5.1f}%)")
        
        # Cluster centers
        centers = self.get_cluster_centers()
        print("\n🎯 Cluster Centers (in feature space):")
        print(f"   {self.feature_columns[0]:15s} {self.feature_columns[1]:15s} {self.feature_columns[2]:15s}")
        for cluster_id in range(self.n_clusters):
            label = self.cluster_labels[cluster_id]
            center = centers[cluster_id]
            print(f"   Cluster {cluster_id} ({label:15s}): {center[0]:6.2f}     {center[1]:6.2f}     {center[2]:6.2f}")
        
        print("\n✨ Clustering Complete!")
        print("━" * 60)


def main() -> Tuple[Optional[KMeans], Optional[ClusteringManager]]:
    """
    Execute complete Block 5 clustering pipeline.
    
    Pipeline:
        Block 1 → Block 2 → Block 3 → Block 5
    
    Returns:
        Tuple[KMeans, ClusteringManager]: Fitted model and manager, or (None, None) on error
    """
    print("\n🔷 BLOCK 5: CLUSTERING (USER SEGMENTATION)")
    print("=" * 60)
    
    # Step 1: Load data (Block 1)
    print("\n📥 Loading data from Block 1...")
    df_main = load_celestia_dataset()
    if df_main is None:
        print("❌ Failed to load data")
        return None, None
    
    print(f"✅ Data loaded: {df_main.shape}")
    
    # Step 2: Clean data (Block 2)
    print("\n🧹 Cleaning data from Block 2...")
    df_cleaned = clean_dataset(df_main)
    if df_cleaned is None:
        print("❌ Failed to clean data")
        return None, None
    
    print(f"✅ Data cleaned: {df_cleaned.shape}")
    
    # Step 3: Encode data (Block 3)
    print("\n🔐 Encoding data from Block 3...")
    manager = EncodingManager()
    df_encoded = manager.encode_dataset(df_cleaned)
    if df_encoded is None:
        print("❌ Failed to encode data")
        return None, None
    
    print(f"✅ Data encoded: {df_encoded.shape}")
    
    # Step 4: Create clustering manager
    print("\n🎯 Creating clustering manager...")
    clustering_manager = ClusteringManager(n_clusters=3)
    
    # Step 5: Extract features
    print("\n📊 Extracting features from encoded data...")
    if not clustering_manager.extract_features(df_encoded):
        print("❌ Failed to extract features")
        return None, None
    
    # Step 6: Fit KMeans
    print("\n🤖 Fitting KMeans model...")
    if not clustering_manager.fit_kmeans():
        print("❌ Failed to fit KMeans")
        return None, None
    
    # Step 7: Print summary
    clustering_manager.print_cluster_summary()
    
    return clustering_manager.get_model(), clustering_manager


if __name__ == '__main__':
    model, manager = main()
    
    if model is not None and manager is not None:
        print("\n✅ Block 5 Clustering Complete!")
        print(f"   Model Status: Fitted")
        print(f"   Ready for: Block 6 (Integration with recommendations)")
    else:
        print("\n❌ Block 5 Clustering Failed")
