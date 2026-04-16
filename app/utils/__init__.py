"""
GlowGuide Utils Package

Exposes utility modules for the skincare recommendation system.
"""

from app.utils.recommendations import (
    get_recommendations,
    explain_recommendation,
    get_ingredient_score_mapping,
    RecommendationResult,
)

from app.utils.loaders import (
    load_skincare_dataset,
    validate_skincare_dataset,
    get_feature_matrix_and_labels,
    get_dataset_summary,
    get_dataset_statistics,
)

from app.utils.ml_model import (
    predict_ingredient,
    initialize_model,
    get_model_info,
    compare_with_block1,
    get_model_performance_report,
)

from app.utils.coordinator import (
    UserProfile,
    MLUserProfile,
    RecommendationResults,
    build_user_profile,
    convert_to_ml_profile,
    get_combined_recommendations,
    validate_sidebar_inputs,
    get_dataset_info,
    get_model_status,
)

__all__ = [
    # Recommendations (Block 1)
    'get_recommendations',
    'explain_recommendation',
    'get_ingredient_score_mapping',
    'RecommendationResult',
    
    # Dataset Loading (Block 3)
    'load_skincare_dataset',
    'validate_skincare_dataset',
    'get_feature_matrix_and_labels',
    'get_dataset_summary',
    'get_dataset_statistics',
    
    # ML Model (Block 4)
    'predict_ingredient',
    'initialize_model',
    'get_model_info',
    'compare_with_block1',
    'get_model_performance_report',
    
    # Coordinator (Block 8)
    'UserProfile',
    'MLUserProfile',
    'RecommendationResults',
    'build_user_profile',
    'convert_to_ml_profile',
    'get_combined_recommendations',
    'validate_sidebar_inputs',
    'get_dataset_info',
    'get_model_status',
]
