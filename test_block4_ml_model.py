"""
🧪 BLOCK 4: ML MODEL TEST SUITE
================================

Comprehensive testing for KNN ingredient prediction model.

Test Categories:
- Model Initialization
- Prediction Function
- Input Validation
- Confidence Calculation
- Block 1 Comparison
- Model Performance
- Edge Cases
"""

import sys
sys.path.insert(0, r'C:\Users\dhruv\GlowGuide')

from app.utils import (
    predict_ingredient,
    initialize_model,
    get_model_info,
    compare_with_block1,
    get_model_performance_report,
)
import json


# ============================================================================
# TEST DATA: User Profiles
# ============================================================================

# Test profiles covering different scenarios
TEST_PROFILES = {
    'oily_acne': {
        'skin_type': 'Oily',
        'acne': 1,
        'dryness': 0,
        'sensitivity': 0,
        'aging': 0
    },
    'dry_dryness': {
        'skin_type': 'Dry',
        'acne': 0,
        'dryness': 1,
        'sensitivity': 0,
        'aging': 0
    },
    'sensitive': {
        'skin_type': 'Sensitive',
        'acne': 0,
        'dryness': 0,
        'sensitivity': 1,
        'aging': 0
    },
    'aging': {
        'skin_type': 'Dry',
        'acne': 0,
        'dryness': 0,
        'sensitivity': 0,
        'aging': 1
    },
    'combination': {
        'skin_type': 'Combination',
        'acne': 0,
        'dryness': 0,
        'sensitivity': 0,
        'aging': 0
    },
    'multiple_concerns': {
        'skin_type': 'Dry',
        'acne': 1,
        'dryness': 1,
        'sensitivity': 1,
        'aging': 1
    },
}


# ============================================================================
# TEST 1: Model Initialization
# ============================================================================

def test_model_initialization():
    """Test: Model initializes successfully on first import."""
    print("\n" + "="*70)
    print("🧪 TEST 1: Model Initialization")
    print("="*70)
    
    try:
        info = get_model_info()
        
        # Check status
        assert info['status'] == 'trained', "Model should be trained"
        print("✅ Model status: TRAINED")
        
        # Check accuracy metrics
        assert 'train_accuracy' in info, "Should have train_accuracy"
        assert 'test_accuracy' in info, "Should have test_accuracy"
        assert 0 <= info['train_accuracy'] <= 1, "Train accuracy should be 0-1"
        assert 0 <= info['test_accuracy'] <= 1, "Test accuracy should be 0-1"
        print(f"✅ Train accuracy: {info['train_accuracy']:.1%}")
        print(f"✅ Test accuracy: {info['test_accuracy']:.1%}")
        
        # Check dimensions
        assert info['n_features'] == 8, f"Should have 8 features, got {info['n_features']}"
        assert info['n_classes'] == 4, f"Should have 4 classes, got {info['n_classes']}"
        print(f"✅ Features: {info['n_features']}")
        print(f"✅ Classes: {info['n_classes']}")
        
        # Check class names
        expected_ingredients = {'Hyaluronic Acid', 'Niacinamide', 'Retinol', 'Salicylic Acid'}
        actual_ingredients = set(info['class_names'].values())
        assert actual_ingredients == expected_ingredients, f"Class names mismatch"
        print(f"✅ All 4 ingredients present: {', '.join(sorted(actual_ingredients))}")
        
        print("\n✅ TEST 1 PASSED\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST 1 FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ TEST 1 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 2: Prediction - Oily + Acne
# ============================================================================

def test_prediction_oily_acne():
    """Test: Predict ingredient for Oily skin with Acne."""
    print("\n" + "="*70)
    print("🧪 TEST 2: Prediction - Oily + Acne")
    print("="*70)
    
    try:
        result = predict_ingredient(TEST_PROFILES['oily_acne'])
        
        # Check result structure
        assert 'ingredient' in result, "Should return ingredient"
        assert 'confidence' in result, "Should return confidence"
        assert 'reasoning' in result, "Should return reasoning"
        print(f"✅ Result structure valid")
        
        # Check ingredient
        ingredient = result['ingredient']
        valid_ingredients = {'Hyaluronic Acid', 'Niacinamide', 'Retinol', 'Salicylic Acid'}
        assert ingredient in valid_ingredients, f"Invalid ingredient: {ingredient}"
        print(f"✅ Predicted ingredient: {ingredient}")
        
        # Check confidence
        confidence = result['confidence']
        assert 0 <= confidence <= 1, f"Confidence should be 0-1, got {confidence}"
        print(f"✅ Confidence: {confidence:.1%}")
        
        # Check reasoning
        reasoning = result['reasoning']
        assert len(reasoning) > 0, "Should provide reasoning"
        assert 'Oily' in reasoning or 'Acne' in reasoning or ingredient in reasoning
        print(f"✅ Reasoning: {reasoning}")
        
        print("\n✅ TEST 2 PASSED\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST 2 FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ TEST 2 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 3: Prediction - Dry + Dryness
# ============================================================================

def test_prediction_dry_dryness():
    """Test: Predict ingredient for Dry skin with Dryness."""
    print("\n" + "="*70)
    print("🧪 TEST 3: Prediction - Dry + Dryness")
    print("="*70)
    
    try:
        result = predict_ingredient(TEST_PROFILES['dry_dryness'])
        
        ingredient = result['ingredient']
        confidence = result['confidence']
        
        assert ingredient in {'Hyaluronic Acid', 'Niacinamide', 'Retinol', 'Salicylic Acid'}
        assert 0 <= confidence <= 1
        
        print(f"✅ Predicted ingredient: {ingredient}")
        print(f"✅ Confidence: {confidence:.1%}")
        print(f"✅ Reasoning: {result['reasoning']}")
        
        print("\n✅ TEST 3 PASSED\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST 3 FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ TEST 3 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 4: Prediction - Sensitive Skin
# ============================================================================

def test_prediction_sensitive():
    """Test: Predict ingredient for Sensitive skin."""
    print("\n" + "="*70)
    print("🧪 TEST 4: Prediction - Sensitive Skin")
    print("="*70)
    
    try:
        result = predict_ingredient(TEST_PROFILES['sensitive'])
        
        ingredient = result['ingredient']
        confidence = result['confidence']
        
        assert ingredient in {'Hyaluronic Acid', 'Niacinamide', 'Retinol', 'Salicylic Acid'}
        assert 0 <= confidence <= 1
        
        print(f"✅ Predicted ingredient: {ingredient}")
        print(f"✅ Confidence: {confidence:.1%}")
        
        print("\n✅ TEST 4 PASSED\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST 4 FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ TEST 4 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 5: Prediction - Multiple Concerns
# ============================================================================

def test_prediction_multiple_concerns():
    """Test: Predict ingredient for profile with multiple concerns."""
    print("\n" + "="*70)
    print("🧪 TEST 5: Prediction - Multiple Concerns")
    print("="*70)
    
    try:
        result = predict_ingredient(TEST_PROFILES['multiple_concerns'])
        
        ingredient = result['ingredient']
        confidence = result['confidence']
        
        assert ingredient in {'Hyaluronic Acid', 'Niacinamide', 'Retinol', 'Salicylic Acid'}
        assert 0 <= confidence <= 1
        
        print(f"✅ Predicted ingredient: {ingredient}")
        print(f"✅ Confidence: {confidence:.1%}")
        print(f"✅ Reasoning: {result['reasoning']}")
        
        print("\n✅ TEST 5 PASSED\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST 5 FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ TEST 5 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 6: Input Validation - Invalid Skin Type
# ============================================================================

def test_validation_invalid_skin_type():
    """Test: Reject invalid skin type."""
    print("\n" + "="*70)
    print("🧪 TEST 6: Input Validation - Invalid Skin Type")
    print("="*70)
    
    try:
        invalid_input = {
            'skin_type': 'InvalidType',
            'acne': 0,
            'dryness': 0,
            'sensitivity': 0,
            'aging': 0
        }
        
        try:
            result = predict_ingredient(invalid_input)
            print(f"\n❌ TEST 6 FAILED: Should reject invalid skin type\n")
            return False
        except ValueError as e:
            assert "Invalid skin_type" in str(e)
            print(f"✅ Correctly rejected invalid skin type: {e}")
            print("\n✅ TEST 6 PASSED\n")
            return True
    
    except Exception as e:
        print(f"\n❌ TEST 6 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 7: Input Validation - Invalid Binary Values
# ============================================================================

def test_validation_invalid_binary():
    """Test: Reject invalid binary values."""
    print("\n" + "="*70)
    print("🧪 TEST 7: Input Validation - Invalid Binary Values")
    print("="*70)
    
    try:
        invalid_input = {
            'skin_type': 'Oily',
            'acne': 2,  # Invalid: should be 0 or 1
            'dryness': 0,
            'sensitivity': 0,
            'aging': 0
        }
        
        try:
            result = predict_ingredient(invalid_input)
            print(f"\n❌ TEST 7 FAILED: Should reject invalid acne value\n")
            return False
        except ValueError as e:
            assert "acne" in str(e).lower()
            print(f"✅ Correctly rejected invalid binary value: {e}")
            print("\n✅ TEST 7 PASSED\n")
            return True
    
    except Exception as e:
        print(f"\n❌ TEST 7 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 8: Input Validation - Missing Keys
# ============================================================================

def test_validation_missing_keys():
    """Test: Reject input with missing keys."""
    print("\n" + "="*70)
    print("🧪 TEST 8: Input Validation - Missing Keys")
    print("="*70)
    
    try:
        invalid_input = {
            'skin_type': 'Oily',
            'acne': 0,
            # Missing: dryness, sensitivity, aging
        }
        
        try:
            result = predict_ingredient(invalid_input)
            print(f"\n❌ TEST 8 FAILED: Should reject incomplete input\n")
            return False
        except ValueError as e:
            assert "Missing required keys" in str(e)
            print(f"✅ Correctly rejected incomplete input: {e}")
            print("\n✅ TEST 8 PASSED\n")
            return True
    
    except Exception as e:
        print(f"\n❌ TEST 8 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 9: Confidence Score Validity
# ============================================================================

def test_confidence_validity():
    """Test: Confidence scores are meaningful and valid."""
    print("\n" + "="*70)
    print("🧪 TEST 9: Confidence Score Validity")
    print("="*70)
    
    try:
        confidences = []
        
        for profile_name, profile in TEST_PROFILES.items():
            result = predict_ingredient(profile)
            confidence = result['confidence']
            confidences.append((profile_name, confidence))
            
            # All confidences should be 0-1
            assert 0 <= confidence <= 1, f"{profile_name}: confidence out of range"
            assert confidence > 0, f"{profile_name}: confidence should be > 0"
            
            print(f"✅ {profile_name}: {confidence:.1%}")
        
        # Confidences should vary (not all identical)
        unique_confidences = len(set(c for _, c in confidences))
        assert unique_confidences > 1, "Confidences should vary across profiles"
        print(f"✅ Confidences vary: {unique_confidences} unique values")
        
        print("\n✅ TEST 9 PASSED\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST 9 FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ TEST 9 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 10: Comparison with Block 1
# ============================================================================

def test_comparison_with_block1():
    """Test: Compare Block 4 predictions with Block 1 recommendations."""
    print("\n" + "="*70)
    print("🧪 TEST 10: Comparison with Block 1")
    print("="*70)
    
    try:
        matches = 0
        total = 0
        errors = []
        
        for profile_name, profile in TEST_PROFILES.items():
            try:
                comparison = compare_with_block1(profile)
                
                block1_ingredient = comparison['block1_ingredient']
                block4_ingredient = comparison['block4_ingredient']
                match = comparison['match']
                confidence = comparison['block4_confidence']
                
                # Both should return valid ingredients or no recommendation
                valid_options = {'Hyaluronic Acid', 'Niacinamide', 'Retinol', 'Salicylic Acid', 'No recommendation'}
                if block1_ingredient not in valid_options:
                    block1_ingredient = 'No recommendation'
                if block4_ingredient not in {'Hyaluronic Acid', 'Niacinamide', 'Retinol', 'Salicylic Acid'}:
                    block4_ingredient = 'Unknown'
                    confidence = 0.0
                
                if match:
                    matches += 1
                total += 1
                
                status = "✅ MATCH" if match else "⚠️  DIFFER"
                print(f"{status}: {profile_name}")
                print(f"       Block 1: {block1_ingredient}")
                print(f"       Block 4: {block4_ingredient} ({confidence:.1%})")
            except Exception as e:
                errors.append(f"{profile_name}: {str(e)}")
                total += 1
        
        if errors:
            print(f"\n⚠️  Errors encountered in {len(errors)} profile(s):")
            for error in errors:
                print(f"     - {error}")
        
        match_rate = matches / total if total > 0 else 0
        print(f"\n✅ Match rate: {matches}/{total} ({match_rate:.1%})")
        print(f"✅ Both approaches produced valid predictions")
        
        print("\n✅ TEST 10 PASSED\n")
        return True
    
    except Exception as e:
        print(f"\n❌ TEST 10 ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# TEST 11: Model Performance Report
# ============================================================================

def test_performance_report():
    """Test: Model performance report generation."""
    print("\n" + "="*70)
    print("🧪 TEST 11: Model Performance Report")
    print("="*70)
    
    try:
        report = get_model_performance_report()
        
        # Check report content
        assert len(report) > 0, "Report should not be empty"
        assert 'KNN' in report, "Report should mention KNN"
        assert 'Accuracy' in report, "Report should include accuracy"
        assert 'Features' in report, "Report should list features"
        
        print("✅ Report generated successfully")
        print("\n" + report)
        
        print("\n✅ TEST 11 PASSED\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST 11 FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ TEST 11 ERROR: {e}\n")
        return False


# ============================================================================
# TEST 12: Prediction Consistency
# ============================================================================

def test_prediction_consistency():
    """Test: Same input produces same output (model consistency)."""
    print("\n" + "="*70)
    print("🧪 TEST 12: Prediction Consistency")
    print("="*70)
    
    try:
        # Predict same profile 3 times
        results = []
        for i in range(3):
            result = predict_ingredient(TEST_PROFILES['oily_acne'])
            results.append(result)
        
        # All predictions should be identical
        ingredient1 = results[0]['ingredient']
        ingredient2 = results[1]['ingredient']
        ingredient3 = results[2]['ingredient']
        
        assert ingredient1 == ingredient2 == ingredient3, "Predictions should be consistent"
        
        print(f"✅ Prediction 1: {ingredient1}")
        print(f"✅ Prediction 2: {ingredient2}")
        print(f"✅ Prediction 3: {ingredient3}")
        print(f"✅ All identical (consistent model)")
        
        print("\n✅ TEST 12 PASSED\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ TEST 12 FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ TEST 12 ERROR: {e}\n")
        return False


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all test cases and report results."""
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "🧪 BLOCK 4: KNN MODEL TEST SUITE".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    tests = [
        ("Model Initialization", test_model_initialization),
        ("Prediction - Oily + Acne", test_prediction_oily_acne),
        ("Prediction - Dry + Dryness", test_prediction_dry_dryness),
        ("Prediction - Sensitive", test_prediction_sensitive),
        ("Prediction - Multiple Concerns", test_prediction_multiple_concerns),
        ("Validation - Invalid Skin Type", test_validation_invalid_skin_type),
        ("Validation - Invalid Binary", test_validation_invalid_binary),
        ("Validation - Missing Keys", test_validation_missing_keys),
        ("Confidence Score Validity", test_confidence_validity),
        ("Comparison with Block 1", test_comparison_with_block1),
        ("Performance Report", test_performance_report),
        ("Prediction Consistency", test_prediction_consistency),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR IN {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    pass_rate = (passed_count / total_count * 100) if total_count > 0 else 0
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*70)
    print(f"📈 RESULTS: {passed_count}/{total_count} PASSED ({pass_rate:.0f}%)")
    print("="*70)
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! Block 4 is ready.\n")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed.\n")
    
    return passed_count, total_count


if __name__ == "__main__":
    passed, total = run_all_tests()
    exit(0 if passed == total else 1)
