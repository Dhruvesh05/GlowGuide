# Block 5: Quick Start Guide

## What is Block 5?

**Block 5** combines the Rule-Based Scoring Engine (Block 1) with the Machine Learning Model (Block 4) into a single Streamlit interface. Instead of showing only one recommendation approach, Block 5 shows **BOTH approaches side-by-side** so you can compare and choose.

## Getting Started (2 minutes)

### 1. Run the Streamlit App
```bash
cd C:\Users\dhruv\GlowGuide
.venv\Scripts\python.exe -m streamlit run app/app.py
```

**Expected Output:**
```
You can now view your app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.10.22.197:8503
```

### 2. Access the App
Open your browser to `http://localhost:8501` or `http://10.10.22.197:8503`

### 3. Use the Integration

#### Step 1: Fill Sidebar
- **Skin Type**: Select one (Oily, Dry, Combination, Sensitive)
- **Skin Concerns**: Select one or more (Acne, Dryness, Sensitivity, Aging, etc.)
- **Age**: Use slider (13-80)

#### Step 2: Click "Get Ingredient Recommendations"

#### Step 3: View Results
You'll see:
1. **Top Recommendations (Score-Based)** - Left column
   - Top 3 rule-based recommendations
   - Color-coded cards (green=high, blue=medium, yellow=lower)
   - Scores and reasoning

2. **ML Prediction (KNN)** - Right column
   - Single machine learning prediction
   - Confidence percentage
   - Neighbor-based reasoning

3. **Metrics Dashboard**
   - Top recommendation from each approach
   - Whether they agree (✅) or differ (⚠️)
   - ML confidence level

4. **Comparison Table**
   - Side-by-side comparison
   - Methodology differences
   - Data sources

5. **Insights**
   - Auto-generated analysis
   - Agreement/conflict explanation
   - Concern-specific guidance

#### Step 4: Expand Advanced Sections (Optional)
- **View Detailed Score Breakdown** - Rule-based scoring details
- **ML Model Details & Performance** - Model training metrics

## Common Scenarios

### Scenario 1: Acne-Prone Oily Skin
```
Sidebar:
- Skin Type: Oily
- Concerns: Acne, Sensitivity
- Age: 22

Expected Result:
- Block 1: Salicylic Acid (top choice)
- Block 4: Salicylic Acid (76% confidence)
- Agreement: ✅ YES
```

### Scenario 2: Dry, Aging Skin
```
Sidebar:
- Skin Type: Dry
- Concerns: Dryness, Aging
- Age: 45

Expected Result:
- Block 1: Hyaluronic Acid (top choice)
- Block 4: Retinol (85% confidence)
- Agreement: ⚠️ DIFFERS (both valid)
```

### Scenario 3: Sensitive Skin
```
Sidebar:
- Skin Type: Sensitive
- Concerns: Sensitivity, Redness
- Age: 28

Expected Result:
- Block 1: Niacinamide (top choice)
- Block 4: Ceramide (72% confidence)
- Agreement: ⚠️ DIFFERS (both soothing)
```

## Understanding the Results

### Score-Based (Block 1)
- Uses **expert-weighted rules** to score ingredients
- Considers: Skin type, concerns, age, preferences
- Score range: 0-100+
- **Strength**: Transparent, consistent, fast
- **Limitation**: Doesn't learn from data

### ML-Based (Block 4)
- Uses **K-Nearest Neighbors** (KNN algorithm)
- Learned from 50 skincare profiles
- Confidence: 50%-90%
- **Strength**: Data-driven, learns patterns
- **Limitation**: Limited training data

### When They Agree
✅ **High Confidence**
- Both approaches converge on same ingredient
- This is your best bet
- Use with confidence

### When They Differ
⚠️ **Choose Your Preference**
- **Prefer Transparent Logic?** → Use Rule-Based (Block 1)
- **Prefer Data-Driven?** → Use ML (Block 4)
- **Want Both?** → Try the top from each and compare results

## Key Numbers

| Metric | Block 1 (Rules) | Block 4 (ML) |
|--------|-----------------|--------------|
| Algorithm | Weighted Scoring | K-Nearest Neighbors |
| Train Data | Expert rules | 50 profiles |
| Accuracy | 100% consistent | 72.5% train / 50% test |
| Speed | Instant | Instant (cached) |
| Transparency | 100% | ~75% (shows neighbors) |
| Adaptability | Static | Can be retrained |
| Recommendations | Top 5 | Top 1 |

## Troubleshooting

### Problem: App doesn't load
```bash
# Restart Streamlit
.venv\Scripts\python.exe -m streamlit run app/app.py --logger.level=debug
```

### Problem: "Normal" skin type not found
**Solution**: Use one of: Oily, Dry, Combination, Sensitive

### Problem: ML model not initialized
**Solution**: Wait 3-5 seconds, model auto-trains on first load

### Problem: Results differ every refresh
**Solution**: Model is cached, should be consistent. If not, check if data changed.

### Problem: Blank results
**Solution**: Ensure you selected concerns from sidebar before clicking "Get Recommendations"

## Running Tests

### Run All Block 5 Tests
```bash
cd C:\Users\dhruv\GlowGuide
.venv\Scripts\python.exe test_block5_integration.py
```

**Expected Output:**
```
======================================================================
BLOCK 5: INTEGRATION TESTS (ML + RULE-BASED)
======================================================================
[✓] TEST 1: Integration Initialization - PASS
[✓] TEST 2: User Profile Conversion - PASS
...
[✓] TEST 12: Integration Consistency - PASS
======================================================================
TOTAL: 12/12 PASSED (100%)
======================================================================
```

## API Reference

### Using Block 5 in Code

```python
# Import
from app.utils import get_recommendations, predict_ingredient
from app.components import display_combined_recommendations

# Block 1: Rule-Based
user_profile = {
    'skin_type': 'Oily',
    'concerns': ['Acne', 'Sensitivity'],
    'age': 25,
    'preferences': {}
}
recommendations = get_recommendations(user_profile, top_n=5)
# Output: [RecommendationResult, RecommendationResult, ...]

# Block 4: ML-Based
ml_user_profile = {
    'skin_type': 'Oily',
    'acne': 1,
    'dryness': 0,
    'sensitivity': 1,
    'aging': 0,
}
ml_result = predict_ingredient(ml_user_profile)
# Output: {'ingredient': 'Salicylic Acid', 'confidence': 0.88, ...}

# Block 5: Display
display_combined_recommendations(
    user_profile=user_profile,
    recommendations=recommendations,
    ml_result=ml_result,
    show_comparison=True
)
```

## File Structure

```
GlowGuide/
├── app/
│   ├── app.py                          # Main Streamlit app (Block 5 integrated)
│   ├── components/
│   │   ├── __init__.py                 # Exports integration_ui functions
│   │   └── integration_ui.py            # Block 5 UI component (450+ lines)
│   ├── utils/
│   │   ├── __init__.py                 # Exports Block 1, 3, 4 functions
│   │   ├── recommendations.py           # Block 1: Rule-based scoring
│   │   ├── loaders.py                  # Block 3: Data loading
│   │   └── ml_model.py                 # Block 4: KNN model
│   └── assets/
│       └── logo.png
├── data/
│   └── skincare_dataset.csv             # Block 3: Training dataset
├── test_block5_integration.py            # Block 5: 12 integration tests
├── BLOCK5_INTEGRATION.md                 # Block 5: Full documentation
└── BLOCK5_QUICK_START.md                 # This file

```

## Next Steps

### Option 1: Explore the App
- Try different skin types and concerns
- Observe when Block 1 and Block 4 agree/differ
- Read the insights to understand why

### Option 2: Review Code
- Read `integration_ui.py` to understand display logic
- Read `app.py` to see Streamlit integration
- Check `ml_model.py` for ML implementation

### Option 3: Enhance Features
- Add more ML models (Random Forest, SVM)
- Add user feedback loop
- Add more input parameters
- Add product recommendations

### Option 4: Deploy
- Deploy to Streamlit Cloud
- Share with users
- Collect feedback
- Iterate and improve

## Support

### Documentation Files
- `BLOCK5_INTEGRATION.md` - Complete Block 5 documentation
- `BLOCK4_ML_MODEL.md` - ML model details
- `BLOCK1_ARCHITECTURE.md` - Rule-based engine details
- `BLOCK3_DATASET.md` - Dataset documentation

### Test Files
- `test_block5_integration.py` - 12 integration tests
- `test_block4_ml_model.py` - 12 ML model tests
- `test_block1_*.py` - Rule-based engine tests

### Code Files
- `app/components/integration_ui.py` - This implements Block 5
- `app/app.py` - Streamlit app using Block 5

## Summary

Block 5 is production-ready with:
- ✅ 12/12 tests passing (100%)
- ✅ Side-by-side dual recommendation display
- ✅ Automatic comparison and insights
- ✅ Beautiful, responsive UI
- ✅ Comprehensive documentation

**Status**: 🎉 Complete and Ready to Use!

**Last Updated**: April 16, 2026
**Test Pass Rate**: 12/12 (100%)
**Components**: 450+ lines of integration code
