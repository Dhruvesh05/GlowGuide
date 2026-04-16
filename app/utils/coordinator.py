"""
Block 8: Coordinator Module (Clean Code Structure)

This module serves as the orchestrator/coordinator layer that handles:
- User profile building and validation
- Format conversions between different blocks
- Orchestrating calls to Block 1 (rule-based) and Block 4 (ML)
- Data transformation logic
- Business logic operations

The Coordinator ensures that:
- All business logic is separated from UI (app.py)
- Each block has a single, clear interface
- Format conversions happen in one place (DRY principle)
- No duplicated logic across components

Architecture:
    app.py (UI only)
         ↓
    coordinator.py (orchestrator/business logic)
         ↓
    block 1, block 3, block 4 (individual logic modules)
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

import streamlit as st

# Import blocks with caching
from app.utils.recommendations import get_recommendations, RecommendationResult
from app.utils.ml_model import predict_ingredient, get_model_info, initialize_model
from app.utils.loaders import (
    load_skincare_dataset,
    get_dataset_summary,
    get_dataset_statistics,
)


@dataclass
class UserProfile:
    """Standardized user profile for Block 1 (rule-based recommendations)."""
    skin_type: str
    concerns: List[str]
    age: int
    preferences: Dict[str, bool]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'skin_type': self.skin_type,
            'concerns': self.concerns,
            'age': self.age,
            'preferences': self.preferences,
        }


@dataclass
class MLUserProfile:
    """Standardized user profile for Block 4 (ML model)."""
    skin_type: str
    acne: int  # Binary (0 or 1)
    dryness: int
    sensitivity: int
    aging: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'skin_type': self.skin_type,
            'acne': self.acne,
            'dryness': self.dryness,
            'sensitivity': self.sensitivity,
            'aging': self.aging,
        }


@dataclass
class RecommendationResults:
    """Container for results from both Block 1 and Block 4."""
    user_profile: UserProfile
    ml_user_profile: MLUserProfile
    block1_results: List[RecommendationResult]
    block4_result: Dict[str, Any]
    
    def to_display_dict(self) -> Dict[str, Any]:
        """Convert to display-friendly dictionary."""
        return {
            'user_profile': self.user_profile.to_dict(),
            'ml_user_profile': self.ml_user_profile.to_dict(),
            'block1_results': [
                {
                    'ingredient': r.ingredient,
                    'score': r.score,
                    'reasoning': r.reasoning,
                }
                for r in self.block1_results
            ],
            'block4_result': self.block4_result,
        }


# ========== BUILD PROFILES ==========

def build_user_profile(
    skin_type: str,
    concerns: List[str],
    age: int,
    alcohol_free: bool = False,
    fragrance_free: bool = False,
    vegan: bool = False,
    cruelty_free: bool = False,
) -> UserProfile:
    """
    Build a standardized user profile for Block 1 (rule-based recommendations).
    
    This function centralizes the logic for constructing user profiles, ensuring
    consistency across the application and making it easy to modify profile logic
    in one place.
    
    Args:
        skin_type: Type of skin (Oily, Dry, Combination, Sensitive, Normal)
        concerns: List of skin concerns (Acne, Dryness, Sensitivity, Aging, etc.)
        age: User age (13-80)
        alcohol_free: Whether to prefer alcohol-free products
        fragrance_free: Whether to prefer fragrance-free products
        vegan: Whether to prefer vegan products
        cruelty_free: Whether to prefer cruelty-free products
        
    Returns:
        UserProfile: Standardized profile for Block 1
        
    Raises:
        ValueError: If skin_type is invalid or concerns list is empty
    """
    # Validate skin type
    valid_skin_types = ['Oily', 'Dry', 'Combination', 'Sensitive', 'Normal']
    if skin_type not in valid_skin_types:
        raise ValueError(f"Invalid skin type: {skin_type}. Must be one of {valid_skin_types}")
    
    # Handle empty concerns (use sensible default)
    if not concerns or not any(concerns):
        concerns = ['No concerns']
    
    # Build preferences dict
    preferences = {
        'alcohol_free': alcohol_free,
        'fragrance_free': fragrance_free,
        'vegan': vegan,
        'cruelty_free': cruelty_free,
    }
    
    return UserProfile(
        skin_type=skin_type,
        concerns=concerns,
        age=age,
        preferences=preferences,
    )


def convert_to_ml_profile(user_profile: UserProfile) -> MLUserProfile:
    """
    Convert Block 1 user profile format to Block 4 (ML) format.
    
    This function implements the format conversion logic, ensuring that the same
    conversion rules are applied consistently across the application.
    
    Conversion Rules:
    - Concerns list → binary features (1 if present, 0 if absent)
    - Supported concerns: Acne, Dryness, Sensitivity, Aging
    - Other concerns are ignored (not used by ML model)
    
    Args:
        user_profile: Block 1 format user profile
        
    Returns:
        MLUserProfile: Block 4 (ML) format user profile
        
    Example:
        >>> block1_profile = UserProfile(
        ...     skin_type='Oily',
        ...     concerns=['Acne', 'Sensitivity'],
        ...     age=25,
        ...     preferences={}
        ... )
        >>> ml_profile = convert_to_ml_profile(block1_profile)
        >>> ml_profile.acne
        1
        >>> ml_profile.sensitivity
        1
        >>> ml_profile.dryness
        0
    """
    return MLUserProfile(
        skin_type=user_profile.skin_type,
        acne=1 if 'Acne' in user_profile.concerns else 0,
        dryness=1 if 'Dryness' in user_profile.concerns else 0,
        sensitivity=1 if 'Sensitivity' in user_profile.concerns else 0,
        aging=1 if 'Aging' in user_profile.concerns else 0,
    )


# ========== ORCHESTRATION FUNCTIONS ==========

def get_combined_recommendations(
    skin_type: str,
    concerns: List[str],
    age: int,
    alcohol_free: bool = False,
    fragrance_free: bool = False,
    vegan: bool = False,
    cruelty_free: bool = False,
    top_n: int = 5,
) -> RecommendationResults:
    """
    Orchestrate getting recommendations from both Block 1 (rule-based) and Block 4 (ML).
    
    This is the main coordinator function that:
    1. Builds user profiles in both formats
    2. Calls Block 1 for rule-based recommendations
    3. Calls Block 4 for ML predictions
    4. Returns combined results in a single container
    
    This function encapsulates the complete recommendation workflow, making it
    easy for app.py to get recommendations without understanding the internal
    orchestration logic.
    
    Args:
        skin_type: User's skin type
        concerns: User's skin concerns
        age: User's age
        alcohol_free: Preference filter
        fragrance_free: Preference filter
        vegan: Preference filter
        cruelty_free: Preference filter
        top_n: Number of top recommendations to return from Block 1
        
    Returns:
        RecommendationResults: Combined results from Block 1 and Block 4
        
    Raises:
        ValueError: If profile building fails (invalid input)
        RuntimeError: If recommendation engines fail
        
    Example:
        >>> results = get_combined_recommendations(
        ...     skin_type='Oily',
        ...     concerns=['Acne'],
        ...     age=25
        ... )
        >>> print(f"Top recommendation: {results.block1_results[0].ingredient}")
        >>> print(f"ML prediction: {results.block4_result['ingredient']}")
    """
    # Step 1: Build user profile for Block 1
    user_profile = build_user_profile(
        skin_type=skin_type,
        concerns=concerns,
        age=age,
        alcohol_free=alcohol_free,
        fragrance_free=fragrance_free,
        vegan=vegan,
        cruelty_free=cruelty_free,
    )
    
    # Step 2: Convert to ML profile format
    ml_user_profile = convert_to_ml_profile(user_profile)
    
    # Step 3: Get Block 1 (rule-based) recommendations
    block1_results = get_recommendations(user_profile.to_dict(), top_n=top_n)
    
    # Step 4: Get Block 4 (ML) prediction
    block4_result = predict_ingredient(ml_user_profile.to_dict())
    
    # Step 5: Return combined results
    return RecommendationResults(
        user_profile=user_profile,
        ml_user_profile=ml_user_profile,
        block1_results=block1_results,
        block4_result=block4_result,
    )


# ========== UTILITY FUNCTIONS ==========

def validate_sidebar_inputs(
    skin_type: str,
    concerns: List[str],
    age: int,
) -> Tuple[bool, str]:
    """
    Validate sidebar inputs before processing.
    
    Ensures that user inputs are valid before passing them to recommendation engines.
    
    Args:
        skin_type: User's selected skin type
        concerns: User's selected concerns
        age: User's selected age
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
            - is_valid: True if all inputs are valid
            - error_message: Empty string if valid, error description if invalid
            
    Example:
        >>> is_valid, msg = validate_sidebar_inputs('Oily', ['Acne'], 25)
        >>> if is_valid:
        ...     print("Inputs are valid")
        ... else:
        ...     print(f"Error: {msg}")
    """
    # Validate skin type
    valid_skin_types = ['Oily', 'Dry', 'Combination', 'Sensitive', 'Normal']
    if skin_type not in valid_skin_types:
        return False, f"Invalid skin type: {skin_type}"
    
    # Validate concerns (can be empty, but if provided should be strings)
    if concerns and not all(isinstance(c, str) for c in concerns):
        return False, "All concerns must be strings"
    
    # Validate age
    if not isinstance(age, int) or age < 13 or age > 80:
        return False, "Age must be between 13 and 80"
    
    return True, ""


def get_dataset_info() -> Dict[str, Any]:
    """
    Get dataset information and statistics.
    
    Retrieves comprehensive dataset information including:
    - Basic stats (sample count, feature count, etc.)
    - Detailed statistics (distributions, correlations, etc.)
    - Data quality metrics
    
    Returns:
        Dict with keys:
            - summary: Basic dataset summary
            - statistics: Detailed statistics
            - quality: Data quality metrics
            
    Example:
        >>> info = get_dataset_info()
        >>> print(f"Samples: {info['summary']['samples']}")
        >>> print(f"Quality: {info['quality']['missing_values']}%")
    """
    try:
        dataset = load_skincare_dataset()
        summary = get_dataset_summary(dataset)
        statistics = get_dataset_statistics(dataset)
        
        return {
            'summary': summary,
            'statistics': statistics,
            'quality': {
                'missing_values': 0,  # We know dataset has no missing values
                'data_completeness': 100,
            },
        }
    except Exception as e:
        return {
            'error': str(e),
            'summary': None,
            'statistics': None,
            'quality': None,
        }


def get_model_status() -> Dict[str, Any]:
    """
    Get ML model initialization status and performance metrics.
    
    Returns current model status, whether it's initialized, and performance metrics.
    
    Returns:
        Dict with keys:
            - initialized: Whether model is initialized
            - info: Model information (if initialized)
            - accuracy: Model accuracy metrics
            - status: Human-readable status message
            
    Example:
        >>> status = get_model_status()
        >>> print(f"Model status: {status['status']}")
        >>> print(f"Accuracy: {status['accuracy']['train']:.1%}")
    """
    try:
        # Initialize model (cached after first call)
        info = initialize_model()
        
        return {
            'initialized': True,
            'info': info,
            'accuracy': {
                'train': info.get('train_accuracy', 0.725),
                'test': info.get('test_accuracy', 0.5),
            },
            'status': info.get('status', 'Ready'),
        }
    except Exception as e:
        return {
            'initialized': False,
            'info': None,
            'accuracy': None,
            'status': f'Error: {str(e)}',
        }


# ========== SUMMARY ==========

"""
Block 8 Coordinator Module Summary:

This module provides a clean, orchestrator layer between the UI (app.py) and
the business logic blocks (Block 1, Block 3, Block 4).

Key Functions:
- build_user_profile(): Create Block 1 format profiles
- convert_to_ml_profile(): Convert between Block 1 and Block 4 formats
- get_combined_recommendations(): Orchestrate both recommendation engines

Benefits:
✓ All business logic isolated from UI
✓ Format conversions in one place (DRY principle)
✓ Easy to test and maintain
✓ Clear interfaces between layers
✓ Changes to business logic don't affect UI

Usage in app.py:
    from app.utils.coordinator import get_combined_recommendations
    
    results = get_combined_recommendations(
        skin_type=skin_type,
        concerns=concerns,
        age=age
    )
    
    # No need to handle profiles, formats, or block calls
    # Just display the results!
"""
