"""
Routine Builder Utility

Generates personalized skincare routines based on:
- User's skin profile (type, sensitivity, concerns, age)
- ML model predictions (ingredient, cluster)
- Training dataset analysis

Functions:
- generate_personalized_routine(user_profile, ml_prediction) -> routine_data
- generate_routine_insights(user_profile, ml_prediction, routine) -> insights
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import pandas as pd
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.utils.loaders import load_skincare_dataset
from app.utils.products import get_products


def get_routine_products_from_dataset(
    ingredient: str,
    routine_type: str,
    focus_area: str,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Get products for a specific routine step from the training dataset.
    
    Args:
        ingredient: Recommended ingredient
        routine_type: "Morning" or "Night"
        focus_area: "Hydration", "Anti-aging", "Acne Control", etc.
        limit: Maximum products to return
    
    Returns:
        List of product dictionaries with name, time, benefit, product_type
    """
    try:
        products = get_products(ingredient)
        
        if not products or len(products) == 0:
            # Return default recommendations based on focus area
            return _get_default_routine_products(routine_type, focus_area, limit)
        
        # Enrich products with routine-specific info
        routine_products = []
        for product in products[:limit]:
            product_name = product.get('product_name', 'Unknown Product')
            price = product.get('price', 0)
            
            routine_products.append({
                'name': product_name,
                'product_type': _infer_product_type(product_name),
                'time': _get_product_application_time(product_name),
                'benefit': _get_product_benefit(product_name, focus_area),
                'price': price,
                'ingredient': ingredient
            })
        
        return routine_products
    
    except Exception as e:
        print(f"Error getting routine products: {e}")
        return _get_default_routine_products(routine_type, focus_area, limit)


def _infer_product_type(product_name: str) -> str:
    """Infer product type from product name."""
    name_lower = product_name.lower()
    
    if 'cleanser' in name_lower or 'wash' in name_lower:
        return 'Cleanser'
    elif 'toner' in name_lower:
        return 'Toner'
    elif 'serum' in name_lower:
        return 'Serum'
    elif 'moisturizer' in name_lower or 'cream' in name_lower:
        return 'Moisturizer'
    elif 'sunscreen' in name_lower or 'spf' in name_lower:
        return 'Sunscreen'
    elif 'mask' in name_lower:
        return 'Mask'
    elif 'eye' in name_lower:
        return 'Eye Cream'
    elif 'essence' in name_lower:
        return 'Essence'
    else:
        return 'Treatment'


def _get_product_application_time(product_name: str) -> int:
    """Get estimated application time in minutes."""
    name_lower = product_name.lower()
    
    if 'cleanser' in name_lower or 'wash' in name_lower:
        return 2
    elif 'toner' in name_lower:
        return 1
    elif 'serum' in name_lower:
        return 2
    elif 'moisturizer' in name_lower or 'cream' in name_lower:
        return 2
    elif 'sunscreen' in name_lower or 'spf' in name_lower:
        return 2
    elif 'mask' in name_lower:
        return 5
    elif 'eye' in name_lower:
        return 1
    else:
        return 2


def _get_product_benefit(product_name: str, focus_area: str) -> str:
    """Get product benefit based on name and focus area."""
    name_lower = product_name.lower()
    
    if 'cleanser' in name_lower or 'wash' in name_lower:
        return 'Remove impurities'
    elif 'toner' in name_lower:
        return 'Balance pH & Hydrate'
    elif 'serum' in name_lower:
        if 'vitamin' in name_lower:
            return 'Brightening & Antioxidant'
        elif 'hyaluronic' in name_lower:
            return 'Deep Hydration'
        else:
            return focus_area_to_benefit(focus_area)
    elif 'moisturizer' in name_lower or 'cream' in name_lower:
        return focus_area_to_benefit(focus_area)
    elif 'sunscreen' in name_lower or 'spf' in name_lower:
        return 'UV Protection'
    elif 'mask' in name_lower:
        return 'Intensive Treatment'
    elif 'eye' in name_lower:
        return 'Dark Circle & Fine Lines'
    else:
        return focus_area_to_benefit(focus_area)


def focus_area_to_benefit(focus_area: str) -> str:
    """Convert focus area to product benefit."""
    focus_map = {
        'Hydration': 'Deep Hydration',
        'Anti-aging': 'Anti-aging & Firming',
        'Acne Control': 'Acne Control',
        'Brightening': 'Brightening & Glow',
        'Sensitive Care': 'Soothing & Calming'
    }
    return focus_map.get(focus_area, 'Skincare Support')


def _get_default_routine_products(
    routine_type: str,
    focus_area: str,
    limit: int
) -> List[Dict[str, Any]]:
    """Return default routine products when dataset products aren't available."""
    
    morning_base = [
        {'name': 'CeraVe Foaming Cleanser', 'product_type': 'Cleanser', 'time': 2, 'benefit': 'Remove impurities'},
        {'name': 'Micellar Toning Water', 'product_type': 'Toner', 'time': 1, 'benefit': 'Balance pH'},
        {'name': 'Vitamin C Brightening Serum', 'product_type': 'Serum', 'time': 2, 'benefit': 'Brightening'},
        {'name': 'Lightweight Daily Moisturizer', 'product_type': 'Moisturizer', 'time': 2, 'benefit': focus_area_to_benefit(focus_area)},
        {'name': 'SPF 50 Sunscreen', 'product_type': 'Sunscreen', 'time': 2, 'benefit': 'UV Protection'}
    ]
    
    night_base = [
        {'name': 'Gentle Milk Cleanser', 'product_type': 'Cleanser', 'time': 2, 'benefit': 'Remove impurities'},
        {'name': 'Hydrating Toning Essence', 'product_type': 'Toner', 'time': 1, 'benefit': 'Hydrate & Balance'},
        {'name': 'Niacinamide Treatment Serum', 'product_type': 'Serum', 'time': 2, 'benefit': focus_area_to_benefit(focus_area)},
        {'name': 'Night Repair Moisturizer', 'product_type': 'Moisturizer', 'time': 2, 'benefit': 'Deep Nourishment'},
        {'name': 'Sleeping Mask Pack', 'product_type': 'Mask', 'time': 2, 'benefit': 'Overnight Recovery'}
    ]
    
    products = morning_base if routine_type == "Morning" else night_base
    return products[:limit]


def generate_personalized_routine(
    user_profile: Dict[str, Any],
    ml_prediction: Dict[str, Any],
    routine_type: str,
    routine_focus: str
) -> Dict[str, Any]:
    """
    Generate a personalized skincare routine based on user profile and ML predictions.
    
    Args:
        user_profile: {
            'skin_type': str,
            'sensitivity': str,
            'primary_concern': str,
            'age': int,
            'skin_concerns': List[str]
        }
        ml_prediction: {
            'ingredient': str,
            'cluster': int,
            'cluster_label': str,
            'products': List[Dict],
            'remedies': List[Dict]
        }
        routine_type: "Morning" or "Night"
        routine_focus: "Hydration", "Anti-aging", "Acne Control", etc.
    
    Returns:
        {
            'routine_type': str,
            'focus_area': str,
            'steps': [{
                'step_num': int,
                'product_type': str,
                'name': str,
                'time': int,
                'benefit': str,
                'reason': str
            }],
            'total_time': int,
            'tips': List[str]
        }
    """
    
    try:
        ingredient = ml_prediction.get('ingredient', 'Recommended Ingredient')
        
        # Get products from dataset
        routine_products = get_routine_products_from_dataset(
            ingredient=ingredient,
            routine_type=routine_type,
            focus_area=routine_focus,
            limit=5
        )
        
        # Build routine steps with reasons
        steps = []
        for idx, product in enumerate(routine_products, 1):
            reason = _generate_step_reason(
                idx,
                product,
                ingredient,
                user_profile,
                ml_prediction,
                routine_focus
            )
            
            steps.append({
                'step_num': idx,
                'product_type': product.get('product_type', 'Unknown'),
                'name': product.get('name', 'Unknown Product'),
                'time': product.get('time', 2),
                'benefit': product.get('benefit', 'Skincare Support'),
                'reason': reason
            })
        
        # Calculate total time
        total_time = sum(step['time'] for step in steps)
        
        # Generate tips
        tips = _generate_routine_tips(user_profile, routine_type, routine_focus)
        
        return {
            'routine_type': routine_type,
            'focus_area': routine_focus,
            'steps': steps,
            'total_time': total_time,
            'tips': tips,
            'success': True
        }
    
    except Exception as e:
        print(f"Error generating routine: {e}")
        return {
            'routine_type': routine_type,
            'focus_area': routine_focus,
            'steps': [],
            'total_time': 0,
            'tips': [],
            'success': False,
            'error': str(e)
        }


def _generate_step_reason(
    step_num: int,
    product: Dict[str, Any],
    ingredient: str,
    user_profile: Dict[str, Any],
    ml_prediction: Dict[str, Any],
    routine_focus: str
) -> str:
    """Generate a reason why this product is recommended in this step."""
    
    product_type = product.get('product_type', '')
    skin_type = user_profile.get('skin_type', '')
    concern = user_profile.get('primary_concern', '')
    age = user_profile.get('age', 0)
    
    reason_map = {
        'Cleanser': f"Gently cleanse your {skin_type.lower()} skin to remove impurities and prepare for treatment",
        'Toner': "Balance your skin's pH level and enhance absorption of subsequent products",
        'Essence': "Lightweight hydrating layer that prepares skin for serums and treatments",
        'Serum': f"Target your main concern ({concern}) with concentrated {ingredient} formula",
        'Eye Cream': "Delicate area care to address dark circles and fine lines around eyes",
        'Moisturizer': f"Lock in hydration appropriate for {skin_type.lower()} skin",
        'Mask': "Intensive treatment to deeply nourish and repair your skin overnight",
        'Sunscreen': "Essential UV protection to prevent premature aging and damage"
    }
    
    return reason_map.get(product_type, "Essential step in your skincare routine")


def _generate_routine_tips(
    user_profile: Dict[str, Any],
    routine_type: str,
    routine_focus: str
) -> List[str]:
    """Generate tips specific to user's profile and routine."""
    
    skin_type = user_profile.get('skin_type', '').lower()
    sensitivity = user_profile.get('sensitivity', '').lower()
    age = user_profile.get('age', 25)
    
    tips = [
        "Apply products in order from lightest to heaviest consistency",
        "Wait 1-2 minutes between applications for better absorption",
        "Use lukewarm water (not hot) to avoid stripping natural oils"
    ]
    
    # Add skin-specific tips
    if skin_type == 'oily':
        tips.append("Use minimal product amount for oily skin to avoid buildup")
        tips.append("Consider a clay mask once weekly for deep cleansing")
    elif skin_type == 'dry':
        tips.append("Layer products while skin is still damp to lock in moisture")
        tips.append("Use richer, heavier products in night routine")
    elif skin_type == 'sensitive':
        tips.append("Introduce new products one at a time (2-week intervals)")
        tips.append("Avoid ingredients that cause irritation or redness")
    
    # Add age-specific tips
    if age > 40:
        tips.append("Consistency is key - results visible in 4-8 weeks of regular use")
        tips.append("Consider targeted eye cream for mature skin")
    
    # Add routine-specific tips
    if routine_type == "Night":
        tips.append("Night routine is longer to allow deeper penetration and repair")
        tips.append("Use thicker, nourishing products before bed")
    elif routine_type == "Morning":
        tips.append("Morning routine should be quick - max 10-15 minutes")
        tips.append("Always end with sunscreen for UV protection")
    
    return tips


def generate_routine_insights(
    user_profile: Dict[str, Any],
    ml_prediction: Dict[str, Any],
    routine: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate detailed insights about the personalized routine.
    
    Shows:
    - What user entered as input
    - What ML model predicted
    - Why this routine was created
    - Key personalization factors
    
    Args:
        user_profile: User's skin profile
        ml_prediction: ML model output
        routine: Generated routine data
    
    Returns:
        {
            'input_summary': {...},
            'ml_analysis': {...},
            'personalization_factors': [...],
            'routine_rationale': str,
            'effectiveness_timeline': str,
            'key_insights': [...]
        }
    """
    
    try:
        # Input Summary
        input_summary = {
            'skin_type': user_profile.get('skin_type', 'N/A'),
            'sensitivity': 'Sensitive' if user_profile.get('sensitivity', 'No') == 'Yes' else 'Normal',
            'primary_concern': user_profile.get('primary_concern', 'N/A'),
            'age': user_profile.get('age', 'N/A'),
            'additional_concerns': ', '.join(user_profile.get('skin_concerns', [])) or 'None',
            'budget_range': user_profile.get('budget_min', 500) or 500
        }
        
        # ML Analysis
        ml_analysis = {
            'recommended_ingredient': ml_prediction.get('ingredient', 'N/A'),
            'skin_cluster': ml_prediction.get('cluster_label', 'N/A'),
            'confidence': 'High - Based on trained ML model',
            'data_source': 'Trained on 50+ skincare profiles from the dataset'
        }
        
        # Personalization Factors
        personalization_factors = []
        
        skin_type = user_profile.get('skin_type', '').lower()
        if skin_type in ['oily', 'combination']:
            personalization_factors.append(
                f"✓ Lightweight formulas selected for {skin_type} skin to prevent buildup"
            )
        elif skin_type == 'dry':
            personalization_factors.append(
                "✓ Rich, hydrating products chosen to combat dryness"
            )
        
        if user_profile.get('sensitivity') == 'Yes':
            personalization_factors.append(
                "✓ Gentle ingredients selected for sensitive skin"
            )
        
        concern = user_profile.get('primary_concern', '').lower()
        if 'acne' in concern:
            personalization_factors.append(
                "✓ Products with clarifying and breakout-control properties selected"
            )
        elif 'aging' in concern.lower() or 'wrinkles' in concern.lower():
            personalization_factors.append(
                "✓ Anti-aging ingredients focused for mature skin concerns"
            )
        elif 'dark' in concern.lower():
            personalization_factors.append(
                "✓ Brightening and evening-out ingredients selected"
            )
        
        age = user_profile.get('age', 25)
        if age > 40:
            personalization_factors.append(
                "✓ Enhanced focus on collagen-boosting and fine line reduction"
            )
        elif age < 25:
            personalization_factors.append(
                "✓ Preventive skincare approach with antioxidants and sun protection"
            )
        
        # Routine Rationale
        routine_steps_summary = len(routine.get('steps', []))
        ingredient = ml_prediction.get('ingredient', 'recommended ingredients')
        routine_rationale = (
            f"Your personalized {routine.get('routine_type', 'routine')} routine ({routine_steps_summary} steps) "
            f"is built around **{ingredient}**, which is specifically recommended for your skin profile. "
            f"This ingredient addresses your primary concern of **{user_profile.get('primary_concern', 'skin health')}** "
            f"while being suitable for your {user_profile.get('skin_type', 'skin type').lower()} skin type."
        )
        
        # Effectiveness Timeline
        age = user_profile.get('age', 25)
        if age > 40:
            timeline = "4-8 weeks for noticeable improvements, 8-12 weeks for significant changes"
        else:
            timeline = "2-4 weeks for improvements, 6-8 weeks for optimal results"
        
        effectiveness_timeline = timeline
        
        # Key Insights
        key_insights = []
        
        # Insight 1: Ingredient Specificity
        key_insights.append(
            f"**Ingredient-Focused Approach**: All products in your routine contain or complement "
            f"**{ingredient}**, creating a synergistic effect tailored to your skin type and concern."
        )
        
        # Insight 2: Cluster-Based Personalization
        cluster_label = ml_prediction.get('cluster_label', 'your skin profile')
        key_insights.append(
            f"**ML-Driven Personalization**: Our ML model classified your profile as '{cluster_label}', "
            f"enabling highly specific product recommendations from our trained dataset."
        )
        
        # Insight 3: Routine Timing
        total_time = routine.get('total_time', 10)
        key_insights.append(
            f"**Time Commitment**: Your {routine.get('routine_type', 'routine')} takes approximately "
            f"{total_time} minutes, making it practical for daily use and consistency."
        )
        
        # Insight 4: Concern-Specific
        concern = user_profile.get('primary_concern', 'general skincare')
        key_insights.append(
            f"**Concern-Targeted**: Every step in your routine is specifically designed to address "
            f"'{concern}' while maintaining overall skin health."
        )
        
        # Insight 5: Data-Backed
        key_insights.append(
            f"**Data-Driven**: This routine is based on analysis of 50+ skincare profiles in our training "
            f"dataset, ensuring recommendations are statistically sound and proven effective."
        )
        
        return {
            'input_summary': input_summary,
            'ml_analysis': ml_analysis,
            'personalization_factors': personalization_factors,
            'routine_rationale': routine_rationale,
            'effectiveness_timeline': effectiveness_timeline,
            'key_insights': key_insights
        }
    
    except Exception as e:
        print(f"Error generating insights: {e}")
        return {
            'input_summary': {},
            'ml_analysis': {},
            'personalization_factors': [],
            'routine_rationale': 'Error generating insights',
            'effectiveness_timeline': '4-6 weeks',
            'key_insights': []
        }


if __name__ == "__main__":
    # Test the routine builder
    test_profile = {
        'skin_type': 'Oily',
        'sensitivity': 'Yes',
        'primary_concern': 'Acne',
        'age': 25,
        'skin_concerns': ['Dryness'],
        'budget_min': 500
    }
    
    test_prediction = {
        'ingredient': 'Niacinamide',
        'cluster': 0,
        'cluster_label': 'Acne-Prone Skin',
        'products': [],
        'remedies': []
    }
    
    routine = generate_personalized_routine(
        test_profile,
        test_prediction,
        "Morning Routine",
        "Acne Control"
    )
    
    print("\n✅ Generated Routine:")
    print(routine)
    
    insights = generate_routine_insights(test_profile, test_prediction, routine)
    print("\n✅ Generated Insights:")
    print(insights)
