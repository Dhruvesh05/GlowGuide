"""Model and data loading with Streamlit caching."""

import joblib
import streamlit as st
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent.parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"


@st.cache_resource
def load_classifier():
    """Load Random Forest classifier from models/classifier_rf.pkl."""
    try:
        path = MODELS_DIR / "classifier_rf.pkl"
        if not path.exists():
            st.error(f"Classifier not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading classifier: {str(e)}")
        return None


@st.cache_resource
def load_vectorizer():
    """Load TF-IDF vectorizer from models/tfidf_vectorizer.pkl."""
    try:
        path = MODELS_DIR / "tfidf_vectorizer.pkl"
        if not path.exists():
            st.error(f"TF-IDF vectorizer not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading vectorizer: {str(e)}")
        return None


@st.cache_resource
def load_regressor():
    """Load price regressor from models/regressor.pkl."""
    try:
        path = MODELS_DIR / "regressor.pkl"
        if not path.exists():
            st.error(f"Regressor not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading regressor: {str(e)}")
        return None


@st.cache_resource
def load_kmeans():
    """Load K-Means model from models/kmeans_model.pkl."""
    try:
        path = MODELS_DIR / "kmeans_model.pkl"
        if not path.exists():
            st.error(f"K-Means model not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading K-Means model: {str(e)}")
        return None


@st.cache_data
def load_dataframe():
    """Load and validate cleaned.csv from data/cleaned.csv."""
    try:
        path = DATA_DIR / "product.csv"
        if not path.exists():
            st.error(f"Data file not found at {path}")
            return None
        df = pd.read_csv(path)
        
        required_cols = ["product_name", "price", "clean_ingredients"]
        assert all(col in df.columns for col in required_cols), \
            f"Missing columns: {[c for c in required_cols if c not in df.columns]}"
        
        return df
    except AssertionError as e:
        st.error(f"Invalid data schema: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None


def validate_all_assets() -> bool:
    """Return True only if all models and dataframe loaded successfully."""
    clf = load_classifier()
    vec = load_vectorizer()
    reg = load_regressor()
    km = load_kmeans()
    df = load_dataframe()
    return all(x is not None for x in [clf, vec, reg, km, df])


# ============================================================================
# BLOCK 3: SKINCARE DATASET LOADING FUNCTIONS
# ============================================================================

import numpy as np
from typing import Tuple, Dict, List


@st.cache_data
def load_skincare_dataset(filepath: str = None) -> pd.DataFrame:
    """
    Load the skincare dataset from CSV file.
    
    Args:
        filepath: Path to CSV file. If None, uses default data/skincare_dataset.csv
    
    Returns:
        Pandas DataFrame with columns: 
        SkinType, Acne, Dryness, Sensitivity, Aging, RecommendedIngredient
    
    Raises:
        FileNotFoundError: If dataset file not found
        ValueError: If required columns missing
    """
    
    if filepath is None:
        filepath = DATA_DIR / "skincare_dataset.csv"
    
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    
    # Load CSV
    df = pd.read_csv(filepath)
    
    # Validate required columns
    required_cols = ['SkinType', 'Acne', 'Dryness', 'Sensitivity', 'Aging', 'RecommendedIngredient']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    return df


def validate_skincare_dataset(df: pd.DataFrame) -> Dict:
    """
    Validate dataset integrity and return statistics.
    
    Args:
        df: Skincare dataset DataFrame
    
    Returns:
        Dictionary containing validation results and statistics
    """
    
    validation = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'skin_types': sorted(df['SkinType'].unique().tolist()),
        'ingredients': sorted(df['RecommendedIngredient'].unique().tolist()),
        'binary_columns_valid': True,
        'warnings': []
    }
    
    # Check binary columns (Acne, Dryness, Sensitivity, Aging)
    binary_cols = ['Acne', 'Dryness', 'Sensitivity', 'Aging']
    for col in binary_cols:
        unique_vals = df[col].unique()
        if not all(val in [0, 1] for val in unique_vals):
            validation['binary_columns_valid'] = False
            validation['warnings'].append(f"{col} contains non-binary values: {unique_vals}")
    
    # Check for class imbalance
    ingredient_counts = df['RecommendedIngredient'].value_counts()
    if ingredient_counts.max() > ingredient_counts.min() * 3:
        validation['warnings'].append(
            f"Class imbalance detected: {ingredient_counts.to_dict()}"
        )
    
    # Distribution by skin type
    validation['skin_type_distribution'] = df['SkinType'].value_counts().to_dict()
    
    # Distribution by ingredient
    validation['ingredient_distribution'] = df['RecommendedIngredient'].value_counts().to_dict()
    
    return validation


def get_feature_matrix_and_labels(
    df: pd.DataFrame,
    encode_skin_type: bool = True
) -> Tuple[np.ndarray, np.ndarray, Dict]:
    """
    Convert DataFrame to feature matrix and labels for ML model.
    
    Args:
        df: Skincare dataset DataFrame
        encode_skin_type: If True, one-hot encode SkinType; if False, leave as strings
    
    Returns:
        Tuple of (X, y, metadata)
        - X: Feature matrix (numpy array)
        - y: Labels (numpy array)
        - metadata: Dict with feature names and label mappings
    """
    
    df_copy = df.copy()
    
    # Create ingredient label mapping
    unique_ingredients = sorted(df_copy['RecommendedIngredient'].unique())
    ingredient_to_label = {ing: idx for idx, ing in enumerate(unique_ingredients)}
    label_to_ingredient = {idx: ing for ing, idx in ingredient_to_label.items()}
    
    # Convert labels
    y = df_copy['RecommendedIngredient'].map(ingredient_to_label).values
    
    # Prepare features
    if encode_skin_type:
        # One-hot encode SkinType
        skin_type_dummies = pd.get_dummies(df_copy['SkinType'], prefix='SkinType')
        X = pd.concat([
            skin_type_dummies,
            df_copy[['Acne', 'Dryness', 'Sensitivity', 'Aging']]
        ], axis=1)
        feature_names = X.columns.tolist()
    else:
        # Keep SkinType as categorical (string)
        X = df_copy[['SkinType', 'Acne', 'Dryness', 'Sensitivity', 'Aging']].copy()
        feature_names = X.columns.tolist()
    
    # Convert to numpy array
    X_array = X.values if encode_skin_type else X.values
    
    metadata = {
        'feature_names': feature_names,
        'n_features': len(feature_names),
        'ingredient_to_label': ingredient_to_label,
        'label_to_ingredient': label_to_ingredient,
        'unique_ingredients': unique_ingredients,
        'n_classes': len(unique_ingredients),
        'n_samples': len(X_array),
        'skin_types': sorted(df['SkinType'].unique().tolist())
    }
    
    return X_array, y, metadata


def get_dataset_summary(df: pd.DataFrame) -> str:
    """
    Generate a human-readable summary of the dataset.
    
    Args:
        df: Skincare dataset DataFrame
    
    Returns:
        String containing dataset summary
    """
    
    summary = []
    summary.append("\n" + "="*80)
    summary.append("📊 SKINCARE DATASET SUMMARY")
    summary.append("="*80)
    
    summary.append(f"\nTotal Samples: {len(df)}")
    summary.append(f"Total Features: {len(df.columns) - 1}")  # Excluding label
    
    summary.append("\n🔷 SKIN TYPES:")
    for skin_type, count in df['SkinType'].value_counts().items():
        percentage = (count / len(df)) * 100
        summary.append(f"  • {skin_type}: {count} samples ({percentage:.1f}%)")
    
    summary.append("\n🧴 RECOMMENDED INGREDIENTS:")
    for ingredient, count in df['RecommendedIngredient'].value_counts().items():
        percentage = (count / len(df)) * 100
        summary.append(f"  • {ingredient}: {count} samples ({percentage:.1f}%)")
    
    summary.append("\n🎯 CONCERNS DISTRIBUTION:")
    for concern in ['Acne', 'Dryness', 'Sensitivity', 'Aging']:
        count = (df[concern] == 1).sum()
        percentage = (count / len(df)) * 100
        summary.append(f"  • {concern}: {count} samples ({percentage:.1f}%)")
    
    summary.append("\n" + "="*80 + "\n")
    
    return "\n".join(summary)


def get_dataset_statistics(df: pd.DataFrame) -> Dict:
    """
    Compute detailed statistics for the dataset.
    
    Args:
        df: Skincare dataset DataFrame
    
    Returns:
        Dictionary containing detailed statistics
    """
    
    stats = {
        'shape': df.shape,
        'missing_values': df.isnull().sum().to_dict(),
        'skin_type_counts': df['SkinType'].value_counts().to_dict(),
        'ingredient_counts': df['RecommendedIngredient'].value_counts().to_dict(),
        'concern_counts': {
            concern: int((df[concern] == 1).sum())
            for concern in ['Acne', 'Dryness', 'Sensitivity', 'Aging']
        },
    }
    
    return stats
