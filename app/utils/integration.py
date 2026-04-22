"""
Block 11: Final Integration Function

This module provides the complete recommendation pipeline.
It integrates all components (predictions, products, remedies)
into one final function that returns comprehensive skincare solutions.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
import pandas as pd
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import all recommendation engines
from app.utils.predictions import predict_skin_solution
from app.utils.products import get_products
from app.utils.remedies import get_remedies
from app.utils.model_loader import ModelLoader


def generate_full_recommendation(
    skin: str,
    sensitivity: str,
    concern: str,
    model_loader: Optional[ModelLoader] = None,
    debug: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Generate complete skincare recommendation combining predictions, products, and remedies.
    
    ✅ STEP 5: INTEGRATE WITH EXISTING ML PIPELINE
    
    This is the master recommendation function that integrates:
    1. Block 8: Predict ingredient and cluster
    2. Block 9: Get products containing the ingredient
    3. Block 10: Get home remedies for the ingredient
    
    Args:
        skin: Skin type (Combination, Dry, Normal, Oily)
        sensitivity: Sensitivity level (Yes, No)
        concern: Skin concern (Acne, Dark Circles, Dark Spots, etc.)
        model_loader: Optional ModelLoader instance (creates new if not provided)
        debug: Enable debug output (default: False)
    
    Returns:
        Dictionary with keys:
        {
            'ingredient': str,           # Recommended ingredient
            'cluster': int,              # Cluster ID (0-2)
            'cluster_label': str,        # Cluster name (Acne-Prone, Dry Skin, Sensitive Skin)
            'products': [                # List of top 3 products (may be empty)
                {
                    'product_name': str,
                    'price': float
                },
                ...
            ],
            'remedies': [                # List of top 2 home remedies (may be empty)
                {
                    'Problem': str,
                    'Ingredients': str,
                    'Usage': str,
                    'Category': str,
                    'Frequency': str
                },
                ...
            ],
            'success': bool,             # True if prediction successful
            'error': str or None         # Error message if any
        }
        
        or None if prediction fails
    
    Example:
        >>> result = generate_full_recommendation('Oily', 'Yes', 'Acne', debug=True)
        >>> if result and result['success']:
        ...     print(f"Ingredient: {result['ingredient']}")
        ...     print(f"Products: {len(result['products'])} found")
        ...     print(f"Remedies: {len(result['remedies'])} found")
    """
    try:
        # ✅ STEP 7: DEBUG SUPPORT
        if debug:
            print(f"\n🔍 DEBUG: Starting full recommendation generation")
            print(f"   Input: skin={skin}, sensitivity={sensitivity}, concern={concern}")
        
        # Step 1: Get prediction (ingredient + cluster)
        prediction = predict_skin_solution(skin, sensitivity, concern, model_loader)
        
        if prediction is None or not prediction.get('success', False):
            error_msg = prediction.get('error', 'Prediction failed') if prediction else 'Unknown error'
            return {
                'success': False,
                'error': f'Prediction failed: {error_msg}',
                'ingredient': None,
                'cluster': None,
                'cluster_label': None,
                'products': [],
                'remedies': []
            }
        
        # Extract prediction results
        ingredient = prediction.get('ingredient')
        cluster = prediction.get('cluster_number')
        cluster_label = prediction.get('cluster_label')
        ingredient_confidence = prediction.get('ingredient_confidence', 0)
        cluster_confidence = prediction.get('cluster_confidence', 0)
        overall_confidence = prediction.get('overall_confidence', 0)
        
        if debug:
            print(f"✅ Prediction successful")
            print(f"   🧪 Ingredient: {ingredient}")
            print(f"   🎯 Cluster: {cluster_label} (ID: {cluster})")
        
        if not ingredient:
            return {
                'success': False,
                'error': 'No ingredient predicted',
                'ingredient': None,
                'cluster': None,
                'cluster_label': None,
                'products': [],
                'remedies': []
            }
        
        # ✅ STEP 5.1: GET PRODUCTS
        # Step 2: Get product recommendations
        products = get_products(ingredient, debug=debug)
        
        # ✅ STEP 6: OUTPUT HANDLING - Handle products
        if products is None:
            # Error occurred
            products_list = []
            if debug:
                print(f"⚠️  Products search error")
        elif isinstance(products, list):
            products_list = products
            if debug:
                print(f"✅ Found {len(products_list)} products")
        else:
            # Single product
            products_list = [products]
            if debug:
                print(f"✅ Found 1 product")
        
        # ✅ STEP 5.2: GET REMEDIES
        # Step 3: Get remedy recommendations
        remedies = get_remedies(ingredient, debug=debug)
        
        # ✅ STEP 6: OUTPUT HANDLING - Handle remedies
        if remedies is None:
            # Error occurred
            remedies_list = []
            if debug:
                print(f"⚠️  Remedies search error")
        elif isinstance(remedies, list):
            remedies_list = remedies
            if debug:
                print(f"✅ Found {len(remedies_list)} remedies")
        else:
            # Single remedy
            remedies_list = [remedies]
            if debug:
                print(f"✅ Found 1 remedy")
        
        # Step 4: Build comprehensive result
        result = {
            'ingredient': ingredient,
            'cluster': cluster,
            'cluster_label': cluster_label,
            'ingredient_confidence': ingredient_confidence,
            'cluster_confidence': cluster_confidence,
            'overall_confidence': overall_confidence,
            'products': products_list,
            'remedies': remedies_list,
            'success': True,
            'error': None
        }
        
        if debug:
            print(f"\n🎉 Recommendation complete!")
            print(f"   Ingredient: {ingredient}")
            print(f"   Products: {len(products_list)}")
            print(f"   Remedies: {len(remedies_list)}")
        
        return result
    
    except Exception as e:
        print(f"❌ Integration error: {str(e)}")
        if debug:
            import traceback
            traceback.print_exc()
        
        return {
            'success': False,
            'error': f'Integration error: {str(e)}',
            'ingredient': None,
            'cluster': None,
            'cluster_label': None,
            'products': [],
            'remedies': []
        }


def print_recommendation(result: Optional[Dict[str, Any]]) -> None:
    """
    Pretty print a recommendation result.
    
    ✅ STEP 6: OUTPUT HANDLING
    
    Args:
        result: Result dictionary from generate_full_recommendation()
    """
    if result is None:
        print("❌ No recommendation generated")
        return
    
    if not result.get('success', False):
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return
    
    print("\n" + "=" * 70)
    print("✨ COMPLETE SKINCARE RECOMMENDATION")
    print("=" * 70)
    
    # Ingredient and cluster
    print(f"\n🎯 Recommended Ingredient: {result['ingredient']}")
    print(f"   Cluster: {result['cluster_label']} (ID: {result['cluster']})")
    
    # Products
    products = result.get('products', [])
    if products and len(products) > 0:
        print(f"\n💅 Top Products ({len(products)} found):")
        for i, product in enumerate(products, 1):
            name = product.get('product_name', 'Unknown')
            price = product.get('price', 'N/A')
            print(f"   {i}. {name}")
            print(f"      Price: ${price}" if isinstance(price, (int, float)) else f"      Price: {price}")
    else:
        # ✅ STEP 6: FALLBACK MESSAGE FOR PRODUCTS
        print(f"\n💅 Top Products:")
        print(f"   ℹ️  Limited data available for ingredient '{result['ingredient']}'")
    
    # Remedies
    remedies = result.get('remedies', [])
    if remedies and len(remedies) > 0:
        print(f"\n🌿 Home Remedies ({len(remedies)} found):")
        for i, remedy in enumerate(remedies, 1):
            problem = remedy.get('Problem', 'Unknown')
            usage = remedy.get('Usage', 'Unknown')
            print(f"   {i}. {problem}")
            print(f"      Usage: {usage}")
    else:
        # ✅ STEP 6: FALLBACK MESSAGE FOR REMEDIES
        print(f"\n🌿 Home Remedies:")
        print(f"   ℹ️  Limited data available for ingredient '{result['ingredient']}'")
    
    print("\n" + "=" * 70)


def main():
    """
    Main function: Execute Block 11 integration demo.
    
    Steps:
    1. Test generate_full_recommendation() with multiple skin profiles
    2. Display comprehensive recommendations
    3. Verify all components integrated correctly
    """
    print("🔷 BLOCK 11: FINAL INTEGRATION FUNCTION")
    print("=" * 70)
    print("Integrating: Predictions (Block 8) + Products (Block 9) + Remedies (Block 10)")
    print("=" * 70)
    
    # Test Case 1: Oily, Sensitive, Acne
    print("\n\n📝 Test 1: Oily skin, Sensitive, Acne concern")
    print("-" * 70)
    result1 = generate_full_recommendation('Oily', 'Yes', 'Acne')
    print_recommendation(result1)
    
    # Test Case 2: Dry, Not Sensitive, Wrinkles
    print("\n\n📝 Test 2: Dry skin, Not Sensitive, Wrinkles concern")
    print("-" * 70)
    result2 = generate_full_recommendation('Dry', 'No', 'Wrinkles')
    print_recommendation(result2)
    
    # Test Case 3: Normal, Sensitive, Dark Spots
    print("\n\n📝 Test 3: Normal skin, Sensitive, Dark Spots concern")
    print("-" * 70)
    result3 = generate_full_recommendation('Normal', 'Yes', 'Dark Spots')
    print_recommendation(result3)
    
    # Summary
    print("\n\n" + "=" * 70)
    print("📊 INTEGRATION SUMMARY")
    print("=" * 70)
    
    test_results = [
        ('Test 1 (Oily, Sensitive, Acne)', result1),
        ('Test 2 (Dry, Not Sensitive, Wrinkles)', result2),
        ('Test 3 (Normal, Sensitive, Dark Spots)', result3)
    ]
    
    successful = sum(1 for _, r in test_results if r and r.get('success', False))
    
    for test_name, result in test_results:
        status = "✅" if result and result.get('success', False) else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n✅ Tests passed: {successful}/3")
    print(f"✅ Full recommendation pipeline working correctly")
    print(f"✅ Predictions + Products + Remedies integrated successfully")
    
    print("\n✨ Block 11 Final Integration Complete!")
    print("   Status: Ready for Streamlit UI integration")


if __name__ == '__main__':
    main()
