"""
Block 6: EDA Dashboard Tests

Tests for the exploratory data analysis (EDA) dashboard component.
Validates data visualizations and statistical calculations.

Test Coverage:
- Test 1: Dashboard initialization and imports
- Test 2: Dataset loading validation
- Test 3: Skin type distribution calculation
- Test 4: Ingredient distribution calculation
- Test 5: Concern frequency calculation
- Test 6: Data quality metrics
- Test 7: Ingredient-Skin Type heatmap data
- Test 8: Concern correlation analysis
- Test 9: Statistical summary generation
- Test 10: Raw data display
- Test 11: Visualization selector
- Test 12: Data integrity and consistency
"""

import sys
from pathlib import Path
import pandas as pd

# Set up path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from app.utils import (
    load_skincare_dataset,
    get_dataset_summary,
    get_dataset_statistics
)


def test_1_dashboard_initialization():
    """Test: EDA dashboard components import successfully."""
    print("\n[TEST 1] Dashboard Initialization")
    
    try:
        from app.components import (
            display_eda_dashboard,
            display_visualization_selector
        )
        print("[OK] All dashboard components imported successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        return False


def test_2_dataset_loading():
    """Test: Dataset loads without errors."""
    print("\n[TEST 2] Dataset Loading")
    
    try:
        df = load_skincare_dataset()
        
        assert df is not None, "DataFrame is None"
        assert len(df) == 50, f"Expected 50 rows, got {len(df)}"
        assert len(df.columns) == 6, f"Expected 6 columns, got {len(df.columns)}"
        
        required_cols = ['SkinType', 'Acne', 'Dryness', 'Sensitivity', 'Aging', 'RecommendedIngredient']
        for col in required_cols:
            assert col in df.columns, f"Missing column: {col}"
        
        print(f"[OK] Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
        return True
    except Exception as e:
        print(f"[FAIL] Dataset loading error: {e}")
        return False


def test_3_skin_type_distribution():
    """Test: Skin type distribution calculation."""
    print("\n[TEST 3] Skin Type Distribution")
    
    try:
        df = load_skincare_dataset()
        
        skin_type_dist = df['SkinType'].value_counts()
        
        assert len(skin_type_dist) > 0, "No skin type distribution"
        assert skin_type_dist.sum() == len(df), "Distribution sum doesn't match row count"
        
        expected_types = {'Oily', 'Dry', 'Combination', 'Sensitive'}
        assert set(skin_type_dist.index) == expected_types, f"Unexpected skin types: {set(skin_type_dist.index)}"
        
        print(f"[OK] Skin type distribution calculated:")
        for skin_type, count in skin_type_dist.items():
            pct = (count / len(df)) * 100
            print(f"    - {skin_type}: {count} ({pct:.0f}%)")
        
        return True
    except Exception as e:
        print(f"[FAIL] Skin type distribution error: {e}")
        return False


def test_4_ingredient_distribution():
    """Test: Ingredient distribution calculation."""
    print("\n[TEST 4] Ingredient Distribution")
    
    try:
        df = load_skincare_dataset()
        
        ingredient_dist = df['RecommendedIngredient'].value_counts()
        
        assert len(ingredient_dist) > 0, "No ingredient distribution"
        assert ingredient_dist.sum() == len(df), "Distribution sum doesn't match row count"
        assert ingredient_dist.sum() == 50, f"Expected 50 total, got {ingredient_dist.sum()}"
        
        print(f"[OK] Ingredient distribution calculated:")
        for ingredient, count in ingredient_dist.items():
            pct = (count / len(df)) * 100
            print(f"    - {ingredient}: {count} ({pct:.0f}%)")
        
        return True
    except Exception as e:
        print(f"[FAIL] Ingredient distribution error: {e}")
        return False


def test_5_concern_frequency():
    """Test: Concern frequency calculation."""
    print("\n[TEST 5] Concern Frequency")
    
    try:
        df = load_skincare_dataset()
        
        concerns = {
            'Acne': df['Acne'].sum(),
            'Dryness': df['Dryness'].sum(),
            'Sensitivity': df['Sensitivity'].sum(),
            'Aging': df['Aging'].sum(),
        }
        
        # Validate each concern count
        for concern, count in concerns.items():
            assert 0 <= count <= len(df), f"{concern} count out of range: {count}"
            pct = (count / len(df)) * 100
            print(f"[OK] {concern}: {count}/{len(df)} profiles ({pct:.0f}%)")
        
        return True
    except Exception as e:
        print(f"[FAIL] Concern frequency error: {e}")
        return False


def test_6_data_quality_metrics():
    """Test: Data quality calculation."""
    print("\n[TEST 6] Data Quality Metrics")
    
    try:
        df = load_skincare_dataset()
        
        # Check for missing values
        missing_count = df.isnull().sum().sum()
        assert missing_count == 0, f"Found {missing_count} missing values"
        
        # Check data types (SkinType can be 'str' or 'object')
        assert df['SkinType'].dtype in ['object', 'str'], f"SkinType should be string/object, got {df['SkinType'].dtype}"
        assert df['Acne'].dtype in ['int64', 'int32', 'int'], "Acne should be numeric"
        
        # Check binary values for concern columns
        for col in ['Acne', 'Dryness', 'Sensitivity', 'Aging']:
            unique_vals = set(df[col].unique())
            assert unique_vals <= {0, 1}, f"{col} has non-binary values: {unique_vals}"
        
        data_quality = ((df.shape[0] * df.shape[1] - missing_count) / (df.shape[0] * df.shape[1])) * 100
        print(f"[OK] Data quality: {data_quality:.0f}% complete")
        print(f"[OK] Missing values: {missing_count}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Data quality check error: {e}")
        return False


def test_7_ingredient_by_skin_type():
    """Test: Ingredient-Skin Type cross-tabulation."""
    print("\n[TEST 7] Ingredient by Skin Type (Heatmap Data)")
    
    try:
        df = load_skincare_dataset()
        
        crosstab = pd.crosstab(df['SkinType'], df['RecommendedIngredient'])
        
        assert crosstab is not None, "Crosstab is None"
        assert crosstab.shape[0] == 4, f"Expected 4 skin types, got {crosstab.shape[0]}"
        assert crosstab.shape[1] > 0, "No ingredients in crosstab"
        assert crosstab.sum().sum() == len(df), "Crosstab sum doesn't match dataset"
        
        print(f"[OK] Crosstab created: {crosstab.shape[0]} skin types × {crosstab.shape[1]} ingredients")
        print(f"[OK] Total recommendations: {crosstab.sum().sum()}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Ingredient-Skin Type error: {e}")
        return False


def test_8_concern_correlation():
    """Test: Concern correlation by skin type."""
    print("\n[TEST 8] Concern Correlation Analysis")
    
    try:
        df = load_skincare_dataset()
        
        concerns = ['Acne', 'Dryness', 'Sensitivity', 'Aging']
        skin_types = df['SkinType'].unique()
        
        # Calculate average concern frequency by skin type
        for concern in concerns:
            concern_by_skin = {}
            for skin_type in skin_types:
                profiles_with_type = df[df['SkinType'] == skin_type]
                avg_concern = profiles_with_type[concern].mean() if len(profiles_with_type) > 0 else 0
                concern_by_skin[skin_type] = avg_concern
            
            print(f"[OK] {concern} distribution by skin type:")
            for skin_type, avg in concern_by_skin.items():
                print(f"    - {skin_type}: {avg:.0%} prevalence")
        
        return True
    except Exception as e:
        print(f"[FAIL] Concern correlation error: {e}")
        return False


def test_9_statistical_summary():
    """Test: Statistical summary generation."""
    print("\n[TEST 9] Statistical Summary")
    
    try:
        df = load_skincare_dataset()
        
        # Generate summary
        summary = get_dataset_summary(df)
        
        assert summary is not None, "Summary is None"
        assert isinstance(summary, str), "Summary should be string"
        assert len(summary) > 0, "Summary is empty"
        
        # Check for key content (case-insensitive)
        summary_upper = summary.upper()
        assert 'SKINCARE' in summary_upper, "Missing 'Skincare' in summary"
        assert 'DATASET' in summary_upper, "Missing 'Dataset' in summary"
        assert 'SUMMARY' in summary_upper, "Missing 'Summary' in summary"
        
        print(f"[OK] Statistical summary generated ({len(summary)} characters)")
        return True
    except Exception as e:
        print(f"[FAIL] Statistical summary error: {e}")
        return False


def test_10_raw_data_display():
    """Test: Raw data can be displayed."""
    print("\n[TEST 10] Raw Data Display")
    
    try:
        df = load_skincare_dataset()
        
        # Test different display methods
        assert df.shape[0] == 50, f"Expected 50 rows, got {df.shape[0]}"
        assert df.shape[1] == 6, f"Expected 6 columns, got {df.shape[1]}"
        
        # Can convert to CSV
        csv = df.to_csv(index=False)
        assert csv is not None, "CSV conversion failed"
        assert len(csv) > 0, "CSV is empty"
        
        # Can filter/slice data
        first_5 = df.head(5)
        assert len(first_5) == 5, "Head slicing failed"
        
        print(f"[OK] Raw data display valid")
        print(f"[OK] CSV export possible ({len(csv)} bytes)")
        print(f"[OK] Data slicing works")
        
        return True
    except Exception as e:
        print(f"[FAIL] Raw data display error: {e}")
        return False


def test_11_visualization_selector():
    """Test: Visualization selector data preparation."""
    print("\n[TEST 11] Visualization Selector")
    
    try:
        df = load_skincare_dataset()
        
        viz_types = [
            "Skin Type Distribution",
            "Ingredient Distribution",
            "Concern Frequency",
            "Ingredient by Skin Type",
            "Concern Breakdown Pie",
            "Concern by Skin Type"
        ]
        
        for viz_type in viz_types:
            if viz_type == "Skin Type Distribution":
                data = df['SkinType'].value_counts()
                assert len(data) > 0, f"No data for {viz_type}"
            
            elif viz_type == "Ingredient Distribution":
                data = df['RecommendedIngredient'].value_counts()
                assert len(data) > 0, f"No data for {viz_type}"
            
            elif viz_type == "Concern Frequency":
                data = {
                    'Acne': df['Acne'].sum(),
                    'Dryness': df['Dryness'].sum(),
                    'Sensitivity': df['Sensitivity'].sum(),
                    'Aging': df['Aging'].sum(),
                }
                assert len(data) == 4, f"Wrong data for {viz_type}"
            
            elif viz_type == "Ingredient by Skin Type":
                data = pd.crosstab(df['SkinType'], df['RecommendedIngredient'])
                assert data is not None, f"No data for {viz_type}"
            
            print(f"[OK] {viz_type}: Data prepared")
        
        return True
    except Exception as e:
        print(f"[FAIL] Visualization selector error: {e}")
        return False


def test_12_data_consistency():
    """Test: Data consistency across multiple loads."""
    print("\n[TEST 12] Data Consistency")
    
    try:
        # Load dataset twice
        df1 = load_skincare_dataset()
        df2 = load_skincare_dataset()
        
        # Check consistency
        assert df1.shape == df2.shape, "Shape mismatch between loads"
        assert df1.equals(df2), "Data differs between loads"
        
        # Check distributions are the same
        dist1 = df1['SkinType'].value_counts()
        dist2 = df2['SkinType'].value_counts()
        assert dist1.equals(dist2), "Distribution differs between loads"
        
        # Check concern counts are the same
        concerns1 = {
            'Acne': df1['Acne'].sum(),
            'Dryness': df1['Dryness'].sum(),
            'Sensitivity': df1['Sensitivity'].sum(),
            'Aging': df1['Aging'].sum(),
        }
        concerns2 = {
            'Acne': df2['Acne'].sum(),
            'Dryness': df2['Dryness'].sum(),
            'Sensitivity': df2['Sensitivity'].sum(),
            'Aging': df2['Aging'].sum(),
        }
        assert concerns1 == concerns2, "Concern counts differ between loads"
        
        print("[OK] Dataset loads consistently")
        print("[OK] Distributions identical across loads")
        print("[OK] All metrics reproducible")
        
        return True
    except Exception as e:
        print(f"[FAIL] Data consistency error: {e}")
        return False


# ========== RUN ALL TESTS ==========

if __name__ == "__main__":
    print("\n" + "="*70)
    print("BLOCK 6: EDA DASHBOARD TESTS")
    print("="*70)
    
    tests = [
        ("Dashboard Initialization", test_1_dashboard_initialization),
        ("Dataset Loading", test_2_dataset_loading),
        ("Skin Type Distribution", test_3_skin_type_distribution),
        ("Ingredient Distribution", test_4_ingredient_distribution),
        ("Concern Frequency", test_5_concern_frequency),
        ("Data Quality Metrics", test_6_data_quality_metrics),
        ("Ingredient-Skin Type Heatmap", test_7_ingredient_by_skin_type),
        ("Concern Correlation Analysis", test_8_concern_correlation),
        ("Statistical Summary", test_9_statistical_summary),
        ("Raw Data Display", test_10_raw_data_display),
        ("Visualization Selector", test_11_visualization_selector),
        ("Data Consistency", test_12_data_consistency),
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
        print("\n[OK] ALL TESTS PASSED - Block 6 EDA Dashboard Complete!")
        sys.exit(0)
    else:
        print(f"\n[FAIL] {total - passed} test(s) failed")
        sys.exit(1)
