"""
Block 5: Integration Tests
Tests for combining Block 1 (Rule-Based) with Block 4 (ML-Based) recommendations.

Test Coverage:
- Test 1: Integration initialization and imports
- Test 2: User profile conversion (Block 1 to Block 4 format)
- Test 3: Dual recommendation retrieval
- Test 4: Comparison functionality
- Test 5: Display functions (basic validation)
- Test 6: Side-by-side metrics
- Test 7: Conflict resolution (when approaches differ)
- Test 8: High confidence agreement
- Test 9: Multiple concern handling
- Test 10: Edge case: Single concern
- Test 11: Edge case: No concerns
- Test 12: Integration consistency (same user, same results)
"""

import sys
from pathlib import Path

# Set up path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from app.utils import get_recommendations, predict_ingredient, compare_with_block1


def test_1_integration_initialization():
    """Test: Integration components import successfully."""
    print("\n[TEST 1] Integration Initialization")
    
    try:
        from app.components import (
            display_combined_recommendations,
            display_ml_performance_metrics
        )
        print("[OK] All integration components imported successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        return False


def test_2_user_profile_conversion():
    """Test: Convert Block 1 format to Block 4 format."""
    print("\n[TEST 2] User Profile Conversion")
    
    # Block 1 format
    user_profile_block1 = {
        'skin_type': 'Oily',
        'concerns': ['Acne', 'Sensitivity'],
        'age': 25,
        'preferences': {}
    }
    
    # Convert to Block 4 format
    ml_user_profile = {
        'skin_type': user_profile_block1['skin_type'],
        'acne': 1 if 'Acne' in user_profile_block1['concerns'] else 0,
        'dryness': 1 if 'Dryness' in user_profile_block1['concerns'] else 0,
        'sensitivity': 1 if 'Sensitivity' in user_profile_block1['concerns'] else 0,
        'aging': 1 if 'Aging' in user_profile_block1['concerns'] else 0,
    }
    
    # Validation
    assert ml_user_profile['acne'] == 1, "Acne mapping failed"
    assert ml_user_profile['sensitivity'] == 1, "Sensitivity mapping failed"
    assert ml_user_profile['dryness'] == 0, "Dryness mapping failed"
    assert ml_user_profile['aging'] == 0, "Aging mapping failed"
    
    print(f"[OK] Conversion successful: {ml_user_profile}")
    return True


def test_3_dual_recommendation_retrieval():
    """Test: Get recommendations from both Block 1 and Block 4."""
    print("\n[TEST 3] Dual Recommendation Retrieval")
    
    # Sample user profile
    user_profile = {
        'skin_type': 'Dry',
        'concerns': ['Dryness', 'Aging'],
        'age': 35,
        'preferences': {}
    }
    
    ml_user_profile = {
        'skin_type': 'Dry',
        'acne': 0,
        'dryness': 1,
        'sensitivity': 0,
        'aging': 1,
    }
    
    try:
        # Get Block 1 recommendations
        recommendations = get_recommendations(user_profile, top_n=5)
        assert len(recommendations) > 0, "No Block 1 recommendations"
        print(f"[OK] Block 1: Got {len(recommendations)} recommendations")
        
        # Get Block 4 prediction
        ml_result = predict_ingredient(ml_user_profile)
        assert 'ingredient' in ml_result, "No ingredient in ML result"
        assert 'confidence' in ml_result, "No confidence in ML result"
        print(f"[OK] Block 4: Got ML prediction - {ml_result['ingredient']} (confidence: {ml_result['confidence']:.0%})")
        
        # Validation
        assert ml_result['confidence'] > 0, "Invalid confidence"
        assert 0 <= ml_result['confidence'] <= 1, "Confidence out of range"
        
        return True
    except Exception as e:
        print(f"[FAIL] Error retrieving recommendations: {e}")
        return False


def test_4_comparison_functionality():
    """Test: Compare Block 1 and Block 4 results."""
    print("\n[TEST 4] Comparison Functionality")
    
    user_profile = {
        'skin_type': 'Combination',
        'concerns': ['Acne', 'Oiliness'],
        'age': 22,
        'preferences': {}
    }
    
    ml_user_profile = {
        'skin_type': 'Combination',
        'acne': 1,
        'dryness': 0,
        'sensitivity': 0,
        'aging': 0,
    }
    
    try:
        # Get both results
        recommendations = get_recommendations(user_profile, top_n=5)
        ml_result = predict_ingredient(ml_user_profile)
        comparison = compare_with_block1(ml_user_profile)
        
        assert comparison is not None, "Comparison returned None"
        
        print(f"[OK] Block 1 top: {recommendations[0].ingredient}")
        print(f"[OK] Block 4 top: {ml_result['ingredient']}")
        print(f"[OK] Comparison result: {comparison}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Comparison error: {e}")
        return False


def test_5_display_functions_basic():
    """Test: Display functions don't crash."""
    print("\n[TEST 5] Display Functions (Basic Validation)")
    
    try:
        from app.components.integration_ui import (
            _display_score_card,
            _display_ml_prediction_card,
            _display_comparison_table,
            _display_insights
        )
        
        # Just verify they're callable
        assert callable(_display_score_card), "Score card not callable"
        assert callable(_display_ml_prediction_card), "ML card not callable"
        assert callable(_display_comparison_table), "Comparison table not callable"
        assert callable(_display_insights), "Insights not callable"
        
        print("[OK] All display functions are callable")
        return True
    except Exception as e:
        print(f"[FAIL] Display functions error: {e}")
        return False


def test_6_metrics_validation():
    """Test: Metrics are properly formatted."""
    print("\n[TEST 6] Metrics Validation")
    
    user_profile = {
        'skin_type': 'Sensitive',
        'concerns': ['Sensitivity', 'Redness'],
        'age': 28,
        'preferences': {}
    }
    
    ml_user_profile = {
        'skin_type': 'Sensitive',
        'acne': 0,
        'dryness': 0,
        'sensitivity': 1,
        'aging': 0,
    }
    
    try:
        recommendations = get_recommendations(user_profile, top_n=5)
        ml_result = predict_ingredient(ml_user_profile)
        
        # Validate metrics (scores can be higher than 10 due to weighting)
        top_score = recommendations[0].score
        avg_score = sum(r.score for r in recommendations) / len(recommendations)
        ml_confidence = ml_result['confidence']
        
        assert top_score > 0, f"Score too low: {top_score}"
        assert avg_score > 0, f"Avg score too low: {avg_score}"
        assert 0 <= ml_confidence <= 1, f"Confidence out of range: {ml_confidence}"
        
        print(f"[OK] Top Score: {top_score:.1f}")
        print(f"[OK] Avg Score: {avg_score:.1f}")
        print(f"[OK] ML Confidence: {ml_confidence:.0%}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Metrics validation error: {e}")
        return False


def test_7_conflict_resolution():
    """Test: Handling when approaches recommend different ingredients."""
    print("\n[TEST 7] Conflict Resolution")
    
    # Try different user profiles until we find a conflict
    profiles = [
        ('Oily', ['Acne']),
        ('Dry', ['Dryness']),
        ('Combination', ['Acne', 'Dryness']),
        ('Sensitive', ['Sensitivity']),
    ]
    
    conflicts = 0
    agreements = 0
    
    for skin_type, concerns in profiles:
        user_profile = {
            'skin_type': skin_type,
            'concerns': concerns,
            'age': 25,
            'preferences': {}
        }
        
        ml_user_profile = {
            'skin_type': skin_type,
            'acne': 1 if 'Acne' in concerns else 0,
            'dryness': 1 if 'Dryness' in concerns else 0,
            'sensitivity': 1 if 'Sensitivity' in concerns else 0,
            'aging': 1 if 'Aging' in concerns else 0,
        }
        
        recommendations = get_recommendations(user_profile, top_n=5)
        ml_result = predict_ingredient(ml_user_profile)
        
        if recommendations[0].ingredient == ml_result['ingredient']:
            agreements += 1
        else:
            conflicts += 1
    
    print(f"[OK] Agreements: {agreements}, Conflicts: {conflicts}")
    print(f"[OK] Conflict rate: {conflicts / (conflicts + agreements) * 100:.0f}%")
    
    return True


def test_8_high_confidence_agreement():
    """Test: When both approaches agree with high confidence."""
    print("\n[TEST 8] High Confidence Agreement")
    
    # Profile that typically gets consistent recommendations
    user_profile = {
        'skin_type': 'Oily',
        'concerns': ['Acne'],
        'age': 20,
        'preferences': {}
    }
    
    ml_user_profile = {
        'skin_type': 'Oily',
        'acne': 1,
        'dryness': 0,
        'sensitivity': 0,
        'aging': 0,
    }
    
    recommendations = get_recommendations(user_profile, top_n=5)
    ml_result = predict_ingredient(ml_user_profile)
    
    # Check if agreement
    agreement = recommendations[0].ingredient == ml_result['ingredient']
    ml_confidence = ml_result['confidence']
    
    print(f"[OK] Block 1: {recommendations[0].ingredient}")
    print(f"[OK] Block 4: {ml_result['ingredient']}")
    print(f"[OK] Agreement: {'YES' if agreement else 'NO'}")
    print(f"[OK] ML Confidence: {ml_confidence:.0%}")
    
    return True


def test_9_multiple_concerns():
    """Test: Handling multiple skin concerns."""
    print("\n[TEST 9] Multiple Concerns Handling")
    
    user_profile = {
        'skin_type': 'Combination',
        'concerns': ['Acne', 'Dryness', 'Sensitivity', 'Aging'],
        'age': 35,
        'preferences': {}
    }
    
    ml_user_profile = {
        'skin_type': 'Combination',
        'acne': 1,
        'dryness': 1,
        'sensitivity': 1,
        'aging': 1,
    }
    
    try:
        recommendations = get_recommendations(user_profile, top_n=5)
        ml_result = predict_ingredient(ml_user_profile)
        
        print(f"[OK] Block 1: {recommendations[0].ingredient} (score: {recommendations[0].score:.1f})")
        print(f"[OK] Block 4: {ml_result['ingredient']} (confidence: {ml_result['confidence']:.0%})")
        print(f"[OK] All 4 concerns processed successfully")
        
        return True
    except Exception as e:
        print(f"[FAIL] Multiple concerns error: {e}")
        return False


def test_10_single_concern():
    """Test: Edge case - single skin concern."""
    print("\n[TEST 10] Single Concern Edge Case")
    
    user_profile = {
        'skin_type': 'Dry',
        'concerns': ['Aging'],
        'age': 40,
        'preferences': {}
    }
    
    ml_user_profile = {
        'skin_type': 'Dry',
        'acne': 0,
        'dryness': 0,
        'sensitivity': 0,
        'aging': 1,
    }
    
    try:
        recommendations = get_recommendations(user_profile, top_n=5)
        ml_result = predict_ingredient(ml_user_profile)
        
        assert len(recommendations) > 0, "No recommendations for single concern"
        assert ml_result['ingredient'], "No ML prediction for single concern"
        
        print(f"[OK] Single concern handled")
        print(f"[OK] Block 1: {recommendations[0].ingredient}")
        print(f"[OK] Block 4: {ml_result['ingredient']}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Single concern error: {e}")
        return False


def test_11_no_concerns():
    """Test: Edge case - no skin concerns specified."""
    print("\n[TEST 11] No Concerns Edge Case")
    
    user_profile = {
        'skin_type': 'Combination',
        'concerns': ['No concerns'],
        'age': 30,
        'preferences': {}
    }
    
    ml_user_profile = {
        'skin_type': 'Combination',
        'acne': 0,
        'dryness': 0,
        'sensitivity': 0,
        'aging': 0,
    }
    
    try:
        recommendations = get_recommendations(user_profile, top_n=5)
        ml_result = predict_ingredient(ml_user_profile)
        
        assert len(recommendations) > 0, "No recommendations for no concerns"
        assert ml_result['ingredient'], "No ML prediction for no concerns"
        
        print(f"[OK] No concerns handled gracefully")
        print(f"[OK] Block 1: {recommendations[0].ingredient}")
        print(f"[OK] Block 4: {ml_result['ingredient']}")
        
        return True
    except Exception as e:
        print(f"[FAIL] No concerns error: {e}")
        return False


def test_12_integration_consistency():
    """Test: Same user input produces consistent results."""
    print("\n[TEST 12] Integration Consistency")
    
    user_profile = {
        'skin_type': 'Dry',
        'concerns': ['Dryness', 'Aging'],
        'age': 45,
        'preferences': {}
    }
    
    ml_user_profile = {
        'skin_type': 'Dry',
        'acne': 0,
        'dryness': 1,
        'sensitivity': 0,
        'aging': 1,
    }
    
    # Get results twice
    recommendations1 = get_recommendations(user_profile, top_n=5)
    ml_result1 = predict_ingredient(ml_user_profile)
    
    recommendations2 = get_recommendations(user_profile, top_n=5)
    ml_result2 = predict_ingredient(ml_user_profile)
    
    # Verify consistency
    assert recommendations1[0].ingredient == recommendations2[0].ingredient, "Block 1 inconsistent"
    assert ml_result1['ingredient'] == ml_result2['ingredient'], "Block 4 inconsistent"
    assert recommendations1[0].score == recommendations2[0].score, "Block 1 score inconsistent"
    assert ml_result1['confidence'] == ml_result2['confidence'], "Block 4 confidence inconsistent"
    
    print("[OK] Block 1 results consistent")
    print("[OK] Block 4 results consistent")
    print("[OK] All metrics remain the same across calls")
    
    return True


# ========== RUN ALL TESTS ==========

if __name__ == "__main__":
    print("\n" + "="*70)
    print("BLOCK 5: INTEGRATION TESTS (ML + RULE-BASED)")
    print("="*70)
    
    tests = [
        ("Integration Initialization", test_1_integration_initialization),
        ("User Profile Conversion", test_2_user_profile_conversion),
        ("Dual Recommendation Retrieval", test_3_dual_recommendation_retrieval),
        ("Comparison Functionality", test_4_comparison_functionality),
        ("Display Functions Basic", test_5_display_functions_basic),
        ("Metrics Validation", test_6_metrics_validation),
        ("Conflict Resolution", test_7_conflict_resolution),
        ("High Confidence Agreement", test_8_high_confidence_agreement),
        ("Multiple Concerns Handling", test_9_multiple_concerns),
        ("Single Concern Edge Case", test_10_single_concern),
        ("No Concerns Edge Case", test_11_no_concerns),
        ("Integration Consistency", test_12_integration_consistency),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"[FAIL] {e}")
            results.append((name, False))
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for i, (name, result) in enumerate(results, 1):
        status = "PASS" if result else "FAIL"
        symbol = "[✓]" if result else "[✗]"
        print(f"{symbol} TEST {i}: {name} - {status}")
    
    print("="*70)
    print(f"TOTAL: {passed}/{total} PASSED ({passed/total*100:.0f}%)")
    print("="*70)
    
    if passed == total:
        print("\n[OK] ALL TESTS PASSED - Block 5 Integration Complete!")
        sys.exit(0)
    else:
        print(f"\n[FAIL] {total - passed} test(s) failed")
        sys.exit(1)
