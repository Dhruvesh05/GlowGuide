"""
Scoring-based Recommendation Engine for GlowGuide.

This module implements a weighted scoring system to recommend skincare ingredients
based on user profile (skin type, concerns, age, preferences).

Components:
    - ingredient_score_mapping(): Build dynamic score mappings
    - get_recommendations(): Main recommendation function
    - explain_recommendation(): Provide explainability
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class RecommendationResult:
    """Data class to hold recommendation results with explainability."""
    ingredient: str
    score: float
    reasoning: List[str]  # List of reasons for the score


def get_ingredient_score_mapping() -> Dict[str, Dict[str, float]]:
    """
    Define ingredient scoring rules based on skin types and concerns.
    
    Returns:
        Dict mapping skin_type/concern → ingredient → score_adjustment
        
    Example:
        {
            'Oily': {'Salicylic Acid': 3.5, 'Niacinamide': 2.0, ...},
            'Acne': {'Salicylic Acid': 3.0, 'Zinc': 2.5, ...},
            ...
        }
    """
    
    # Base ingredient scores by skin type
    skin_type_scores = {
        'Oily': {
            'Salicylic Acid': 3.5,
            'Niacinamide': 2.5,
            'Clay': 3.0,
            'Zinc': 2.0,
            'Charcoal': 2.5,
            'Glycolic Acid': 2.0,
            'Witch Hazel': 2.0,
        },
        'Dry': {
            'Hyaluronic Acid': 4.0,
            'Ceramide': 4.0,
            'Glycerin': 3.5,
            'Panthenol': 3.0,
            'Squalane': 3.5,
            'Lanolin': 2.5,
            'Shea Butter': 3.0,
            'Peptide': 2.5,
        },
        'Combination': {
            'Niacinamide': 3.5,
            'Hyaluronic Acid': 3.0,
            'Glycerin': 3.0,
            'Salicylic Acid': 2.0,
            'Ceramide': 2.5,
            'Peptide': 2.5,
            'Ferulic Acid': 2.0,
        },
        'Sensitive': {
            'Panthenol': 4.0,
            'Ceramide': 4.0,
            'Allantoin': 3.5,
            'Aloe Vera': 3.5,
            'Glycerin': 3.0,
            'Centella Asiatica': 3.5,
            'Oat Extract': 3.0,
            'Chamomile': 2.5,
        },
        'Normal': {
            'Hyaluronic Acid': 3.0,
            'Niacinamide': 3.0,
            'Vitamin C': 2.5,
            'Retinol': 2.5,
            'Glycerin': 2.5,
            'Peptide': 2.0,
            'Green Tea': 2.0,
        },
    }
    
    # Ingredient scores by concern
    concern_scores = {
        'Acne': {
            'Salicylic Acid': 4.0,
            'Zinc': 3.5,
            'Azelaic Acid': 3.5,
            'Tea Tree Oil': 3.0,
            'Niacinamide': 3.0,
            'Clay': 2.5,
            'Witch Hazel': 2.0,
        },
        'Dryness': {
            'Hyaluronic Acid': 4.0,
            'Ceramide': 4.0,
            'Glycerin': 3.5,
            'Squalane': 3.5,
            'Panthenol': 3.5,
            'Lanolin': 3.0,
            'Shea Butter': 3.0,
        },
        'Oiliness': {
            'Salicylic Acid': 3.5,
            'Niacinamide': 3.0,
            'Clay': 3.5,
            'Zinc': 2.5,
            'Mattifying Agent': 2.5,
            'Witch Hazel': 2.0,
        },
        'Sensitivity': {
            'Ceramide': 4.0,
            'Panthenol': 4.0,
            'Allantoin': 3.5,
            'Centella Asiatica': 3.5,
            'Aloe Vera': 3.5,
            'Chamomile': 3.0,
            'Oat Extract': 3.0,
        },
        'Aging': {
            'Retinol': 4.0,
            'Vitamin C': 3.5,
            'Peptide': 3.5,
            'Ferulic Acid': 3.0,
            'Hyaluronic Acid': 3.0,
            'Bakuchiol': 3.0,
            'Niacinamide': 2.5,
            'Resveratrol': 2.5,
        },
        'Hyperpigmentation': {
            'Vitamin C': 4.0,
            'Kojic Acid': 3.5,
            'Azelaic Acid': 3.5,
            'Tranexamic Acid': 3.5,
            'Niacinamide': 2.5,
            'Licorice Extract': 3.0,
            'Glycolic Acid': 2.5,
        },
        'Redness': {
            'Centella Asiatica': 4.0,
            'Niacinamide': 3.5,
            'Ceramide': 3.5,
            'Chamomile': 3.0,
            'Allantoin': 3.0,
            'Panthenol': 3.0,
            'Green Tea': 2.5,
        },
    }
    
    # Age-specific ingredient boosts
    age_scores = {
        '13-18': {
            'Salicylic Acid': 1.5,
            'Tea Tree Oil': 1.0,
            'Clay': 1.5,
            'Zinc': 1.0,
        },
        '19-25': {
            'Niacinamide': 1.5,
            'Hyaluronic Acid': 1.0,
            'Vitamin C': 1.0,
        },
        '26-35': {
            'Retinol': 2.0,
            'Peptide': 1.5,
            'Vitamin C': 1.5,
            'Ferulic Acid': 1.0,
        },
        '36-50': {
            'Retinol': 2.5,
            'Peptide': 2.0,
            'Hyaluronic Acid': 1.5,
            'Bakuchiol': 1.5,
        },
        '50+': {
            'Retinol': 3.0,
            'Peptide': 2.5,
            'Hyaluronic Acid': 2.0,
            'Ceramide': 2.0,
            'Niacinamide': 1.5,
        },
    }
    
    return {
        'skin_type': skin_type_scores,
        'concern': concern_scores,
        'age': age_scores,
    }


def _get_age_group(age: int) -> str:
    """Classify age into groups for scoring."""
    if age < 19:
        return '13-18'
    elif age < 26:
        return '19-25'
    elif age < 36:
        return '26-35'
    elif age < 51:
        return '36-50'
    else:
        return '50+'


def _calculate_ingredient_score(
    ingredient: str,
    skin_type: str,
    concerns: List[str],
    age: int,
    mappings: Dict,
) -> Tuple[float, List[str]]:
    """
    Calculate score for a single ingredient based on user profile.
    
    Args:
        ingredient: Name of ingredient to score
        skin_type: User's skin type
        concerns: List of skin concerns
        age: User's age
        mappings: Score mapping dictionary from get_ingredient_score_mapping()
    
    Returns:
        Tuple of (total_score, list_of_reasons)
    """
    score = 50.0  # Base score
    reasons = []
    
    # 1. Skin type score
    skin_scores = mappings['skin_type'].get(skin_type, {})
    if ingredient in skin_scores:
        skin_boost = skin_scores[ingredient]
        score += skin_boost * 1.5  # Weight skin type more heavily
        reasons.append(f"+{skin_boost*1.5:.1f} for {skin_type} skin type")
    
    # 2. Concern scores
    concern_scores = mappings['concern']
    for concern in concerns:
        if concern in concern_scores:
            if ingredient in concern_scores[concern]:
                concern_boost = concern_scores[concern][ingredient]
                score += concern_boost
                reasons.append(f"+{concern_boost:.1f} for {concern} concern")
    
    # 3. Age-specific boosts
    age_group = _get_age_group(age)
    age_scores = mappings['age'].get(age_group, {})
    if ingredient in age_scores:
        age_boost = age_scores[ingredient]
        score += age_boost
        reasons.append(f"+{age_boost:.1f} recommended for age {age_group}")
    
    # 4. Bonus for multi-concern match
    matching_concerns = sum(
        1 for concern in concerns
        if concern in concern_scores and ingredient in concern_scores[concern]
    )
    if matching_concerns >= 2:
        multi_concern_bonus = 2.0
        score += multi_concern_bonus
        reasons.append(f"+{multi_concern_bonus:.1f} bonus for matching {matching_concerns} concerns")
    
    return score, reasons


def get_recommendations(
    user_input: Dict,
    top_n: int = 5,
    include_all_ingredients: bool = False,
) -> List[RecommendationResult]:
    """
    Generate skincare ingredient recommendations based on user profile.
    
    Args:
        user_input: Dictionary containing:
            {
                'skin_type': str (e.g., 'Oily', 'Dry', 'Combination', 'Sensitive', 'Normal'),
                'concerns': List[str] (e.g., ['Acne', 'Aging']),
                'age': int (13-80),
                'preferences': Optional[Dict] (e.g., {'alcohol_free': True, 'vegan': True}),
            }
        top_n: Number of recommendations to return (default 5, max 5)
        include_all_ingredients: If True, return all ingredients; if False, return top_n
    
    Returns:
        List of RecommendationResult objects sorted by score (descending)
    
    Raises:
        ValueError: If user_input is missing required fields
    
    Example:
        >>> user_input = {
        ...     'skin_type': 'Oily',
        ...     'concerns': ['Acne', 'Oiliness'],
        ...     'age': 22,
        ... }
        >>> results = get_recommendations(user_input, top_n=5)
        >>> for rec in results:
        ...     print(f"{rec.ingredient}: {rec.score:.1f}")
    """
    
    # Validate input
    required_keys = {'skin_type', 'concerns', 'age'}
    if not all(key in user_input for key in required_keys):
        missing = required_keys - set(user_input.keys())
        raise ValueError(f"Missing required keys: {missing}")
    
    skin_type = user_input['skin_type']
    concerns = user_input['concerns'] if isinstance(user_input['concerns'], list) else [user_input['concerns']]
    age = user_input['age']
    preferences = user_input.get('preferences', {})
    
    # Validate inputs
    valid_skin_types = {'Oily', 'Dry', 'Combination', 'Sensitive', 'Normal'}
    if skin_type not in valid_skin_types:
        raise ValueError(f"Invalid skin_type '{skin_type}'. Must be one of {valid_skin_types}")
    
    if not isinstance(age, int) or not (13 <= age <= 80):
        raise ValueError(f"Age must be integer between 13-80, got {age}")
    
    # Get all ingredients from mappings
    mappings = get_ingredient_score_mapping()
    all_ingredients = set()
    
    # Collect all unique ingredients
    for ingredient_dict in mappings['skin_type'].values():
        all_ingredients.update(ingredient_dict.keys())
    for ingredient_dict in mappings['concern'].values():
        all_ingredients.update(ingredient_dict.keys())
    for ingredient_dict in mappings['age'].values():
        all_ingredients.update(ingredient_dict.keys())
    
    # Score each ingredient
    recommendations = []
    for ingredient in all_ingredients:
        score, reasons = _calculate_ingredient_score(
            ingredient, skin_type, concerns, age, mappings
        )
        
        # Apply preference filters (penalty-based approach)
        if preferences.get('alcohol_free') and 'alcohol' in ingredient.lower():
            score -= 10
            reasons.append(f"-10 for containing alcohol (preference)")
        
        if preferences.get('fragrance_free') and 'fragrance' in ingredient.lower():
            score -= 10
            reasons.append(f"-10 for containing fragrance (preference)")
        
        if preferences.get('vegan') and ingredient in {
            'Lanolin', 'Beeswax', 'Carmine', 'Keratin', 'Collagen'
        }:
            score -= 10
            reasons.append(f"-10 for non-vegan ingredient (preference)")
        
        recommendations.append(
            RecommendationResult(
                ingredient=ingredient,
                score=max(0, score),  # Clamp to non-negative
                reasoning=reasons,
            )
        )
    
    # Sort by score descending
    recommendations.sort(key=lambda x: x.score, reverse=True)
    
    # Return top N or all
    if include_all_ingredients:
        return recommendations
    else:
        return recommendations[:min(top_n, len(recommendations))]


def explain_recommendation(
    user_input: Dict,
    ingredient: str,
) -> Optional[Dict]:
    """
    Provide detailed explanation for why a specific ingredient was recommended.
    
    Args:
        user_input: User profile dictionary (same as get_recommendations)
        ingredient: Ingredient to explain
    
    Returns:
        Dict with keys:
            - 'ingredient': str
            - 'score': float
            - 'reasoning': List[str]
            - 'matches': Dict with breakdown by category
        or None if ingredient not found
    
    Example:
        >>> explanation = explain_recommendation(user_input, 'Salicylic Acid')
        >>> print(explanation['reasoning'])
    """
    
    results = get_recommendations(user_input, top_n=1000, include_all_ingredients=True)
    
    for result in results:
        if result.ingredient.lower() == ingredient.lower():
            mappings = get_ingredient_score_mapping()
            skin_type = user_input['skin_type']
            concerns = user_input['concerns']
            age = user_input['age']
            age_group = _get_age_group(age)
            
            # Build detailed breakdown
            matches = {
                'skin_type': skin_type if ingredient in mappings['skin_type'].get(skin_type, {}) else None,
                'concerns': [
                    c for c in concerns
                    if c in mappings['concern'] and ingredient in mappings['concern'][c]
                ],
                'age_group': age_group if ingredient in mappings['age'].get(age_group, {}) else None,
            }
            
            return {
                'ingredient': result.ingredient,
                'score': result.score,
                'reasoning': result.reasoning,
                'matches': matches,
            }
    
    return None


# ============= EXAMPLE USAGE =============
if __name__ == '__main__':
    # Example user profile
    example_user = {
        'skin_type': 'Oily',
        'concerns': ['Acne', 'Oiliness'],
        'age': 22,
        'preferences': {
            'alcohol_free': False,
            'fragrance_free': False,
            'vegan': False,
        }
    }
    
    print("=" * 70)
    print("🎯 SKINCARE INGREDIENT RECOMMENDATIONS FOR USER")
    print("=" * 70)
    print(f"Profile: {example_user['skin_type']} skin, {example_user['concerns']}, Age {example_user['age']}")
    print()
    
    # Get recommendations
    recommendations = get_recommendations(example_user, top_n=5)
    
    print(f"{'Rank':<6} {'Ingredient':<25} {'Score':<10} {'Reasoning':<30}")
    print("-" * 70)
    
    for i, rec in enumerate(recommendations, 1):
        reasoning_short = rec.reasoning[0][:25] if rec.reasoning else "No reason"
        print(f"{i:<6} {rec.ingredient:<25} {rec.score:<10.1f} {reasoning_short:<30}")
    
    print("\n" + "=" * 70)
    print("📋 DETAILED EXPLANATION FOR TOP RECOMMENDATION")
    print("=" * 70)
    
    top_ingredient = recommendations[0].ingredient
    explanation = explain_recommendation(example_user, top_ingredient)
    
    print(f"Ingredient: {explanation['ingredient']}")
    print(f"Score: {explanation['score']:.1f}/100")
    print(f"\nWhy is it recommended:")
    for reason in explanation['reasoning']:
        print(f"  • {reason}")
    print(f"\nMatches:")
    print(f"  • Skin type match: {explanation['matches']['skin_type']}")
    print(f"  • Concern matches: {explanation['matches']['concerns']}")
    print(f"  • Age group: {explanation['matches']['age_group']}")
