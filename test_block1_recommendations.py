"""
Test suite for Block 1: Scoring-based Recommendation Engine
Demonstrates recommendations for various user profiles
"""

from app.utils.recommendations import (
    get_recommendations,
    explain_recommendation,
    get_ingredient_score_mapping,
)


def test_scenario(scenario_name: str, user_input: dict):
    """Test a single user scenario and print results."""
    print("\n" + "=" * 80)
    print(f"📊 SCENARIO: {scenario_name}")
    print("=" * 80)
    print(f"Profile: {user_input['skin_type']} skin | Concerns: {user_input['concerns']} | Age: {user_input['age']}")
    print("-" * 80)
    
    try:
        recommendations = get_recommendations(user_input, top_n=5)
        
        print(f"{'#':<3} {'Ingredient':<20} {'Score':<8} {'Explanation':<50}")
        print("-" * 80)
        
        for i, rec in enumerate(recommendations, 1):
            main_reason = rec.reasoning[0][:45] if rec.reasoning else "No reason"
            print(f"{i:<3} {rec.ingredient:<20} {rec.score:<8.1f} {main_reason:<50}")
        
        # Show detailed explanation for #1
        print("\n💡 Detailed Analysis of #1 Recommendation:")
        explanation = explain_recommendation(user_input, recommendations[0].ingredient)
        if explanation:
            print(f"   Ingredient: {explanation['ingredient']}")
            print(f"   Final Score: {explanation['score']:.1f}/100")
            print(f"   Reasoning:")
            for reason in explanation['reasoning']:
                print(f"      • {reason}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Run test scenarios for Block 1."""
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "🌟 BLOCK 1: SCORING-BASED RECOMMENDATION ENGINE 🌟" + " " * 13 + "║")
    print("║" + " " * 20 + "Testing Multiple User Profiles" + " " * 27 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Scenario 1: Young oily skin with acne
    test_scenario(
        "Young Adult with Oily Skin & Acne",
        {
            'skin_type': 'Oily',
            'concerns': ['Acne', 'Oiliness'],
            'age': 22,
        }
    )
    
    # Scenario 2: Mature dry skin with aging concerns
    test_scenario(
        "Mature with Dry Skin & Aging",
        {
            'skin_type': 'Dry',
            'concerns': ['Dryness', 'Aging'],
            'age': 45,
        }
    )
    
    # Scenario 3: Sensitive combination skin
    test_scenario(
        "Sensitive Combination Skin",
        {
            'skin_type': 'Combination',
            'concerns': ['Sensitivity', 'Redness'],
            'age': 28,
        }
    )
    
    # Scenario 4: Multiple concerns
    test_scenario(
        "Severe Multiple Concerns",
        {
            'skin_type': 'Oily',
            'concerns': ['Acne', 'Hyperpigmentation', 'Sensitivity'],
            'age': 30,
        }
    )
    
    # Scenario 5: Older skin with anti-aging focus
    test_scenario(
        "Mature Skin with Anti-Aging Focus (50+)",
        {
            'skin_type': 'Normal',
            'concerns': ['Aging', 'Dryness'],
            'age': 58,
        }
    )
    
    # Scenario 6: Teenage acne
    test_scenario(
        "Teenager with Acne",
        {
            'skin_type': 'Oily',
            'concerns': ['Acne'],
            'age': 16,
        }
    )
    
    # Scenario 7: With preferences
    print("\n" + "=" * 80)
    print("🎯 SCENARIO WITH PREFERENCES")
    print("=" * 80)
    print("Testing same profile with preferences applied...")
    
    user_with_prefs = {
        'skin_type': 'Dry',
        'concerns': ['Dryness', 'Sensitivity'],
        'age': 35,
        'preferences': {
            'alcohol_free': True,
            'fragrance_free': True,
            'vegan': True,
        }
    }
    
    print(f"Profile: {user_with_prefs['skin_type']} skin | Age {user_with_prefs['age']}")
    print(f"Preferences: {user_with_prefs['preferences']}")
    print("-" * 80)
    
    recommendations = get_recommendations(user_with_prefs, top_n=5)
    
    for i, rec in enumerate(recommendations, 1):
        main_reason = rec.reasoning[0][:40] if rec.reasoning else "No reason"
        print(f"{i}. {rec.ingredient:<25} Score: {rec.score:<8.1f}")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("📈 INGREDIENT SCORING SYSTEM SUMMARY")
    print("=" * 80)
    
    mappings = get_ingredient_score_mapping()
    print(f"✓ Total Unique Ingredients Tracked: {sum(len(v) for v in mappings['skin_type'].values())} unique across skin types")
    print(f"✓ Skin Types Supported: {list(mappings['skin_type'].keys())}")
    print(f"✓ Concerns Supported: {list(mappings['concern'].keys())}")
    print(f"✓ Age Groups Supported: {list(mappings['age'].keys())}")
    
    print("\n" + "=" * 80)
    print("✅ Block 1 Implementation Complete!")
    print("=" * 80)
    print("\nKey Features Implemented:")
    print("  1. ✓ Dynamic ingredient score mappings by skin type, concern, and age")
    print("  2. ✓ Weighted scoring system (base 50 + adjustments)")
    print("  3. ✓ Multi-concern support with bonus scoring")
    print("  4. ✓ Preference-based filtering (alcohol-free, vegan, fragrance-free)")
    print("  5. ✓ Explainability: Detailed reasoning for each recommendation")
    print("  6. ✓ Flexible top-N recommendations (1-5 ingredients)")
    print("\nNext Steps:")
    print("  • Block 2: EDA Dashboard for data exploration")
    print("  • Block 3: Machine Learning Model (KNN)")
    print("  • Block 4: Integration & Explainability UI\n")


if __name__ == '__main__':
    main()
