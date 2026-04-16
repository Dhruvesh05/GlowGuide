"""
🧠 BLOCK 4: ML MODEL - KNN INGREDIENT PREDICTION
================================================

Purpose: Train KNN classifier to predict skincare ingredients based on user profiles.

Key Components:
- KNN model with k=3 (3 nearest neighbors)
- Cached model to avoid retraining
- Prediction function with input validation
- Feature encoding for categorical data
- Model evaluation & performance metrics

Usage:
    from app.utils import predict_ingredient, get_model_info
    
    # Single prediction
    user_profile = {
        'skin_type': 'Oily',
        'acne': 1,
        'dryness': 0,
        'sensitivity': 0,
        'aging': 0
    }
    prediction = predict_ingredient(user_profile)
    # Returns: {'ingredient': 'Salicylic Acid', 'confidence': 0.95}
    
    # Model info
    info = get_model_info()
    # Returns: {'accuracy': 0.85, 'n_samples': 50, 'n_features': 8, ...}
"""

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from functools import lru_cache
import warnings

# Suppress convergence warnings
warnings.filterwarnings('ignore', category=UserWarning)

# ============================================================================
# GLOBAL STATE: Cached Model & Metadata
# ============================================================================

_trained_model = None
_model_metadata = None
_feature_encoder = None
_label_encoder = None
_feature_names = None


# ============================================================================
# STEP 1: DATA PREPARATION & MODEL TRAINING
# ============================================================================

@st.cache_data
def _load_and_prepare_data():
    """
    Load Block 3 dataset and prepare for ML training (CACHED).
    
    This function is cached with @st.cache_data because it's a pure function
    that doesn't have side effects and returns consistent data based on the
    input dataset.
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test, feature_names, label_mapping)
    """
    from app.utils import load_skincare_dataset, get_feature_matrix_and_labels
    
    # Load dataset from Block 3
    df = load_skincare_dataset()
    
    # Get ML-ready format
    X, y, metadata = get_feature_matrix_and_labels(df)
    
    # Split into train/test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Get feature names and label mapping
    feature_names = metadata['feature_names']
    # Convert label_to_ingredient to class_names format {0: 'ingredient', 1: 'ingredient', ...}
    label_mapping = metadata['label_to_ingredient']  # {0: 'Hyaluronic Acid', 1: 'Niacinamide', ...}
    
    return X_train, X_test, y_train, y_test, feature_names, label_mapping


def _train_knn_model(X_train, y_train, k=3):
    """
    Train KNN classifier on training data.
    
    Args:
        X_train: Training features (n_samples, n_features)
        y_train: Training labels (n_samples,)
        k: Number of neighbors (default: 3)
    
    Returns:
        KNeighborsClassifier: Trained model
    """
    model = KNeighborsClassifier(n_neighbors=k, metric='euclidean')
    model.fit(X_train, y_train)
    return model


@st.cache_resource
def _initialize_model_internal():
    """
    Internal function to train and initialize KNN model (CACHED WITH @st.cache_resource).
    
    This function is decorated with @st.cache_resource because it:
    1. Performs expensive computation (model training)
    2. Manages stateful resources (trained KNN classifier)
    3. Should only run once and be reused across Streamlit reruns
    
    Returns:
        tuple: (model, metadata) - Trained KNN model and its metadata
    """
    print("[*] Initializing KNN Model...")
    print("   Loading dataset...")
    
    # Load and prepare data (already cached via @st.cache_data)
    X_train, X_test, y_train, y_test, feature_names, label_mapping = _load_and_prepare_data()
    
    print(f"   Training data: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    print(f"   Test data: {X_test.shape[0]} samples")
    
    # Train KNN model
    print("   Training KNN model (k=3)...")
    model = _train_knn_model(X_train, y_train, k=3)
    
    # Evaluate
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"   [OK] Model trained!")
    print(f"   Train accuracy: {train_accuracy:.1%}")
    print(f"   Test accuracy: {test_accuracy:.1%}")
    
    # Convert label_mapping to class_names format {0: 'ingredient', 1: 'ingredient', ...}
    class_names = {int(k): v for k, v in label_mapping.items()}
    
    metadata = {
        'status': 'trained (CACHED)',
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'n_train_samples': X_train.shape[0],
        'n_test_samples': X_test.shape[0],
        'n_features': X_train.shape[1],
        'n_classes': len(class_names),
        'class_names': class_names,
        'feature_names': feature_names,
        'k_neighbors': 3,
        'metric': 'euclidean'
    }
    
    return model, metadata


def initialize_model():
    """
    Initialize KNN model (public interface that uses cached internal function).
    
    This is a wrapper around _initialize_model_internal() that also updates
    global state for backwards compatibility.
    
    Returns:
        dict: Model metadata including accuracy and dimensions
    """
    global _trained_model, _model_metadata, _feature_names, _label_encoder
    
    # Call cached internal function
    model, metadata = _initialize_model_internal()
    
    # Update globals for backwards compatibility
    _trained_model = model
    _model_metadata = metadata
    
    # Extract feature names from the last training run
    X_train, X_test, y_train, y_test, feature_names, label_mapping = _load_and_prepare_data()
    _feature_names = feature_names
    _label_encoder = {v: int(k) for k, v in label_mapping.items()}  # ingredient -> class index
    
    return _model_metadata


# ============================================================================
# STEP 2: PREDICTION FUNCTION
# ============================================================================

def predict_ingredient(user_input):
    """
    Predict recommended ingredient for user profile using trained KNN model.
    
    This is the main prediction interface. It:
    1. Validates user input
    2. Encodes categorical features
    3. Makes prediction using KNN
    4. Calculates confidence (distance to nearest neighbors)
    5. Returns prediction with confidence score
    
    Args:
        user_input (dict): User profile with keys:
            - 'skin_type': str (Oily, Dry, Combination, Sensitive)
            - 'acne': int (0 or 1)
            - 'dryness': int (0 or 1)
            - 'sensitivity': int (0 or 1)
            - 'aging': int (0 or 1)
    
    Returns:
        dict: Prediction result
            {
                'ingredient': str,           # Predicted ingredient name
                'confidence': float,         # Confidence (0-1)
                'nearest_neighbors': list,   # Top 3 similar samples
                'distances': list,           # Distances to neighbors
                'reasoning': str             # Explanation
            }
    
    Example:
        >>> user = {'skin_type': 'Oily', 'acne': 1, 'dryness': 0, 
        ...         'sensitivity': 0, 'aging': 0}
        >>> result = predict_ingredient(user)
        >>> print(result['ingredient'])
        'Salicylic Acid'
    """
    global _trained_model, _model_metadata, _feature_names
    
    # Initialize model if not already done
    if _trained_model is None:
        initialize_model()
    
    # Validate input
    _validate_user_input(user_input)
    
    # Convert user input to feature vector
    feature_vector = _encode_user_input(user_input)
    
    # Make prediction
    prediction_class = _trained_model.predict([feature_vector])[0]
    
    # Get ingredient name
    class_names = _model_metadata['class_names']
    predicted_ingredient = class_names[prediction_class]
    
    # Calculate confidence using distances to neighbors
    distances, indices = _trained_model.kneighbors([feature_vector], n_neighbors=3)
    distances = distances[0]
    indices = indices[0]
    
    # Confidence: inverse of average distance (normalized to 0-1)
    # Closer neighbors = higher confidence
    max_distance = np.sqrt(_model_metadata['n_features'])  # Maximum possible distance
    confidence = 1.0 - (np.mean(distances) / max_distance)
    confidence = max(0.0, min(1.0, confidence))  # Clamp to [0, 1]
    
    # Create reasoning
    reasoning = _generate_reasoning(
        user_input, predicted_ingredient, confidence, distances, indices
    )
    
    return {
        'ingredient': predicted_ingredient,
        'confidence': round(confidence, 3),
        'distances': [round(d, 3) for d in distances],
        'neighbor_indices': list(indices),
        'reasoning': reasoning
    }


# ============================================================================
# STEP 3: INPUT VALIDATION & ENCODING
# ============================================================================

def _validate_user_input(user_input):
    """
    Validate user input format and values.
    
    Args:
        user_input (dict): User profile to validate
    
    Raises:
        ValueError: If input is invalid
    """
    # Required keys
    required_keys = {'skin_type', 'acne', 'dryness', 'sensitivity', 'aging'}
    if not all(key in user_input for key in required_keys):
        missing = required_keys - set(user_input.keys())
        raise ValueError(f"Missing required keys: {missing}")
    
    # Validate skin_type
    valid_skin_types = {'Oily', 'Dry', 'Combination', 'Sensitive'}
    skin_type = user_input['skin_type']
    if skin_type not in valid_skin_types:
        raise ValueError(
            f"Invalid skin_type '{skin_type}'. "
            f"Must be one of: {valid_skin_types}"
        )
    
    # Validate binary columns
    binary_keys = {'acne', 'dryness', 'sensitivity', 'aging'}
    for key in binary_keys:
        value = user_input[key]
        if value not in {0, 1}:
            raise ValueError(
                f"Invalid {key} value '{value}'. Must be 0 or 1."
            )


def _encode_user_input(user_input):
    """
    Encode user input (categorical + binary) to feature vector.
    
    Converts user profile to the same format as training data:
    1. One-hot encode SkinType
    2. Keep binary columns as-is
    
    Args:
        user_input (dict): Raw user profile
    
    Returns:
        np.ndarray: Encoded feature vector (1, n_features)
    """
    global _feature_names
    
    # Extract values
    skin_type = user_input['skin_type']
    
    # Create feature vector matching training format
    # Training format: [SkinType_Combination, SkinType_Dry, SkinType_Oily, 
    #                   SkinType_Sensitive, Acne, Dryness, Sensitivity, Aging]
    
    feature_vector = []
    
    # One-hot encode skin type
    for st in ['Combination', 'Dry', 'Oily', 'Sensitive']:
        feature_vector.append(1 if skin_type == st else 0)
    
    # Add binary features in order: Acne, Dryness, Sensitivity, Aging
    feature_vector.append(user_input['acne'])
    feature_vector.append(user_input['dryness'])
    feature_vector.append(user_input['sensitivity'])
    feature_vector.append(user_input['aging'])
    
    return np.array(feature_vector)


# ============================================================================
# STEP 4: REASONING & EXPLANATION
# ============================================================================

def _generate_reasoning(user_input, predicted_ingredient, confidence, 
                       distances, neighbor_indices):
    """
    Generate human-readable explanation for prediction.
    
    Args:
        user_input (dict): User profile
        predicted_ingredient (str): Predicted ingredient
        confidence (float): Confidence score
        distances (list): Distances to neighbors
        neighbor_indices (list): Indices of neighbors
    
    Returns:
        str: Explanation text
    """
    # Skin type matching
    skin_type = user_input['skin_type']
    
    # Concern summary
    concerns = []
    if user_input['acne']: concerns.append("Acne")
    if user_input['dryness']: concerns.append("Dryness")
    if user_input['sensitivity']: concerns.append("Sensitivity")
    if user_input['aging']: concerns.append("Aging")
    
    concern_text = ", ".join(concerns) if concerns else "No specific concerns"
    
    # Build reasoning
    confidence_pct = int(confidence * 100)
    
    reasoning = (
        f"Based on {skin_type} skin type with {concern_text}. "
        f"The model found {confidence_pct}% confidence in recommending {predicted_ingredient}. "
        f"This prediction is supported by {len(neighbor_indices)} similar user profiles."
    )
    
    return reasoning


# ============================================================================
# STEP 5: MODEL INFO & EVALUATION
# ============================================================================

def get_model_info():
    """
    Get trained model information and performance metrics.
    
    Returns:
        dict: Model metadata
            {
                'status': str,              # 'trained' or 'not_initialized'
                'train_accuracy': float,    # Training accuracy (0-1)
                'test_accuracy': float,     # Test accuracy (0-1)
                'n_train_samples': int,     # Training samples
                'n_test_samples': int,      # Test samples
                'n_features': int,          # Number of features
                'n_classes': int,           # Number of ingredient classes
                'class_names': dict,        # {0: 'Hyaluronic Acid', ...}
                'feature_names': list,      # Feature names
                'k_neighbors': int,         # k value for KNN
                'metric': str               # Distance metric
            }
    """
    global _model_metadata
    
    if _model_metadata is None:
        return {'status': 'not_initialized'}
    
    return _model_metadata


def compare_with_block1(user_input):
    """
    Compare Block 4 (ML) prediction with Block 1 (rule-based) recommendation.
    
    This enables validation by comparing two approaches:
    - Block 1: Rule-based scoring (deterministic)
    - Block 4: ML-based prediction (statistical learning)
    
    Args:
        user_input (dict): User profile with KNN format:
            {
                'skin_type': str,
                'acne': 0/1,
                'dryness': 0/1,
                'sensitivity': 0/1,
                'aging': 0/1
            }
    
    Returns:
        dict: Comparison result
            {
                'block1_ingredient': str,
                'block4_ingredient': str,
                'block4_confidence': float,
                'match': bool,
                'reasoning': str
            }
    """
    from app.utils import get_recommendations
    
    # Convert KNN format to Block 1 format
    # KNN input: binary concern flags
    # Block 1 input: list of concern names, skin type, age
    
    concerns = []
    if user_input.get('acne'): concerns.append('Acne')
    if user_input.get('dryness'): concerns.append('Dryness')
    if user_input.get('sensitivity'): concerns.append('Sensitivity')
    if user_input.get('aging'): concerns.append('Aging')
    
    # If no concerns, add a default one
    if not concerns:
        concerns = ['General Care']
    
    # Convert to Block 1 format
    block1_input = {
        'skin_type': user_input['skin_type'],
        'concerns': concerns,
        'age': 25  # Default age for Block 1 comparison
    }
    
    # Block 1: Rule-based approach
    try:
        block1_results = get_recommendations(block1_input)
        if block1_results:
            block1_ingredient = block1_results[0].ingredient
        else:
            block1_ingredient = "No recommendation"
    except Exception as e:
        # If Block 1 fails, just use "No recommendation"
        block1_ingredient = "No recommendation"
    
    # Block 4: ML-based approach
    try:
        block4_result = predict_ingredient(user_input)
        block4_ingredient = block4_result['ingredient']
        block4_confidence = block4_result['confidence']
    except Exception as e:
        # If Block 4 fails, return error
        raise
    
    # Compare
    match = block1_ingredient == block4_ingredient
    
    reasoning = (
        f"Block 1 (Rule-based): {block1_ingredient}\n"
        f"Block 4 (ML-based): {block4_ingredient} ({int(block4_confidence*100)}% confidence)\n"
        f"Match: {'✅ Yes' if match else '❌ No'}"
    )
    
    return {
        'block1_ingredient': block1_ingredient,
        'block4_ingredient': block4_ingredient,
        'block4_confidence': block4_confidence,
        'match': match,
        'reasoning': reasoning
    }


def get_model_performance_report():
    """
    Generate detailed model performance report.
    
    Returns:
        str: Formatted performance report
    """
    global _model_metadata
    
    if _model_metadata is None:
        return "Model not initialized. Call initialize_model() first."
    
    meta = _model_metadata
    
    report = f"""
╔════════════════════════════════════════════════════════════════════╗
║                    BLOCK 4: KNN MODEL PERFORMANCE                  ║
╚════════════════════════════════════════════════════════════════════╝

📊 DATASET INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Training Samples:          {meta['n_train_samples']}
Test Samples:              {meta['n_test_samples']}
Total Samples:             {meta['n_train_samples'] + meta['n_test_samples']}
Number of Features:        {meta['n_features']}
Number of Classes:         {meta['n_classes']}

🧠 MODEL CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Algorithm:                 KNN (k-Nearest Neighbors)
K Neighbors:               {meta['k_neighbors']}
Distance Metric:           {meta['metric']}

📈 PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Training Accuracy:         {meta['train_accuracy']:.1%}
Test Accuracy:             {meta['test_accuracy']:.1%}
Overfitting Risk:          {'Low' if abs(meta['train_accuracy'] - meta['test_accuracy']) < 0.15 else 'Moderate' if abs(meta['train_accuracy'] - meta['test_accuracy']) < 0.25 else 'High'}

📋 INGREDIENT CLASSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for class_idx, ingredient in meta['class_names'].items():
        report += f"  [{class_idx}] {ingredient}\n"
    
    report += f"""
🔧 FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{', '.join(meta['feature_names'])}

✅ STATUS: Model ready for predictions
"""
    
    return report


# ============================================================================
# INITIALIZATION & CACHING
# ============================================================================

@lru_cache(maxsize=None)
def _get_feature_encoding_info():
    """
    Cache feature encoding information.
    
    Returns:
        dict: Feature names and encoding details
    """
    global _feature_names
    
    if _feature_names is None:
        initialize_model()
    
    return {
        'feature_names': _feature_names,
        'n_features': len(_feature_names)
    }


# Auto-initialize model when module is imported
def _auto_initialize():
    """Initialize model on first import."""
    global _trained_model
    if _trained_model is None:
        try:
            initialize_model()
        except Exception as e:
            print(f"[!] Warning: Failed to auto-initialize model: {e}")
            print("   Model will be initialized on first prediction.")


# Initialize on module import
_auto_initialize()
