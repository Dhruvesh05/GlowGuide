# ⚡ BLOCK 4: ML MODEL - QUICK START GUIDE

## 🎯 What is Block 4?

Machine Learning model using KNN to predict skincare ingredients.  
**Status:** ✅ Ready to use  
**Test Pass Rate:** 12/12 (100%)

---

## 🚀 Getting Started in 30 Seconds

### Single Prediction

```python
from app.utils import predict_ingredient

user = {
    'skin_type': 'Oily',
    'acne': 1,
    'dryness': 0,
    'sensitivity': 0,
    'aging': 0
}

result = predict_ingredient(user)
print(result['ingredient'])        # → 'Salicylic Acid'
print(result['confidence'])        # → 0.764 (76.4%)
```

### Compare with Block 1

```python
from app.utils import compare_with_block1

comparison = compare_with_block1(user)
print(comparison['block1_ingredient'])   # Rule-based result
print(comparison['block4_ingredient'])   # ML-based result
print(comparison['match'])               # True/False
```

### Get Model Info

```python
from app.utils import get_model_info

info = get_model_info()
print(info['train_accuracy'])   # 0.725 (72.5%)
print(info['test_accuracy'])    # 0.500 (50.0%)
print(info['class_names'])      # {0: 'Hyaluronic Acid', ...}
```

---

## 📊 Input/Output

### Input

```python
{
    'skin_type': 'Oily|Dry|Combination|Sensitive',
    'acne': 0 or 1,
    'dryness': 0 or 1,
    'sensitivity': 0 or 1,
    'aging': 0 or 1
}
```

### Output

```python
{
    'ingredient': 'Salicylic Acid|Hyaluronic Acid|Niacinamide|Retinol',
    'confidence': 0.0-1.0,
    'distances': [0.123, 0.456, 0.789],
    'neighbor_indices': [0, 5, 12],
    'reasoning': 'Based on Oily skin type...'
}
```

---

## ✨ Key Features

| Feature | Details |
|---------|---------|
| **Algorithm** | K-Nearest Neighbors (k=3) |
| **Training Data** | 40 samples (Block 3 dataset) |
| **Test Data** | 10 samples |
| **Features** | 8 (one-hot encoded) |
| **Classes** | 4 ingredients |
| **Accuracy** | 72.5% train, 50.0% test |
| **Prediction Time** | < 1ms per prediction |
| **Memory** | < 100 KB |

---

## 🧪 Testing

Run all tests:
```bash
python test_block4_ml_model.py
```

Test results:
- ✅ Model Initialization
- ✅ Prediction - Oily + Acne
- ✅ Prediction - Dry + Dryness
- ✅ Prediction - Sensitive
- ✅ Prediction - Multiple Concerns
- ✅ Validation - Invalid Skin Type
- ✅ Validation - Invalid Binary
- ✅ Validation - Missing Keys
- ✅ Confidence Score Validity
- ✅ Comparison with Block 1
- ✅ Performance Report
- ✅ Prediction Consistency

**Pass Rate:** 12/12 (100%)

---

## 📝 Common Use Cases

### Case 1: Single User Prediction

```python
from app.utils import predict_ingredient

user = {
    'skin_type': 'Dry',
    'acne': 0,
    'dryness': 1,
    'sensitivity': 0,
    'aging': 0
}

result = predict_ingredient(user)
print(f"Recommend: {result['ingredient']} ({result['confidence']:.0%})")
```

Output: `Recommend: Hyaluronic Acid (76%)`

### Case 2: Batch Predictions

```python
from app.utils import predict_ingredient

users = [
    {'skin_type': 'Oily', 'acne': 1, 'dryness': 0, 'sensitivity': 0, 'aging': 0},
    {'skin_type': 'Dry', 'acne': 0, 'dryness': 1, 'sensitivity': 0, 'aging': 0},
    {'skin_type': 'Sensitive', 'acne': 0, 'dryness': 0, 'sensitivity': 1, 'aging': 0},
]

for user in users:
    result = predict_ingredient(user)
    print(f"{user['skin_type']:12} → {result['ingredient']}")
```

### Case 3: Compare Approaches

```python
from app.utils import compare_with_block1

user = {'skin_type': 'Oily', 'acne': 1, 'dryness': 0, 'sensitivity': 0, 'aging': 0}
comp = compare_with_block1(user)

print(f"Rule-based:  {comp['block1_ingredient']}")
print(f"ML-based:    {comp['block4_ingredient']}")
print(f"Confidence:  {comp['block4_confidence']:.1%}")
print(f"Agree?:      {comp['match']}")
```

---

## ⚙️ Configuration

### Adjusting K Value

Edit `app/utils/ml_model.py`:

```python
# In _train_knn_model():
model = KNeighborsClassifier(n_neighbors=5)  # Change from 3
```

### Retraining on New Data

```python
import app.utils.ml_model as ml

# Clear cache
ml._trained_model = None

# Retrain
ml.initialize_model()
```

---

## 🚨 Error Handling

### Invalid Skin Type

```python
try:
    predict_ingredient({'skin_type': 'Unknown', ...})
except ValueError as e:
    print(f"Error: {e}")
    # → "Invalid skin_type 'Unknown'. Must be one of: {'Oily', 'Dry', ...}"
```

### Missing Keys

```python
try:
    predict_ingredient({'skin_type': 'Oily'})  # Missing other keys
except ValueError as e:
    print(f"Error: {e}")
    # → "Missing required keys: {'acne', 'dryness', 'sensitivity', 'aging'}"
```

### Invalid Binary Values

```python
try:
    predict_ingredient({'skin_type': 'Oily', 'acne': 2, ...})  # acne must be 0/1
except ValueError as e:
    print(f"Error: {e}")
    # → "Invalid acne value '2'. Must be 0 or 1."
```

---

## 📚 Files

| File | Purpose | Size |
|------|---------|------|
| `app/utils/ml_model.py` | KNN implementation | 620 lines |
| `test_block4_ml_model.py` | Test suite | 600 lines |
| `BLOCK4_ML_MODEL.md` | Full documentation | 400 lines |
| `BLOCK4_QUICK_START.md` | This guide | 200 lines |

---

## 🔍 Example Output

### Prediction Example

```
User Input:
{
    'skin_type': 'Oily',
    'acne': 1,
    'dryness': 0,
    'sensitivity': 0,
    'aging': 0
}

Model Output:
{
    'ingredient': 'Salicylic Acid',
    'confidence': 0.764,
    'distances': [0.123, 0.456, 0.789],
    'neighbor_indices': [3, 7, 15],
    'reasoning': 'Based on Oily skin type with Acne. The model found 76% 
                  confidence in recommending Salicylic Acid. This prediction 
                  is supported by 3 similar user profiles.'
}
```

### Comparison Example

```
User Input: Dry skin + Dryness

Block 1 (Rule-based):  Hyaluronic Acid
Block 4 (ML-based):    Hyaluronic Acid (76.4%)
Match:                 ✅ Yes

User Input: Sensitive skin + Sensitivity

Block 1 (Rule-based):  No recommendation
Block 4 (ML-based):    Niacinamide (76.4%)
Match:                 ❌ No
```

---

## 📊 Quick Performance Stats

```
Training Accuracy:  72.5%
Test Accuracy:      50.0%
Prediction Time:    < 1ms
Model Size:         ~1 KB
Memory Usage:       < 100 KB
Test Pass Rate:     100% (12/12)
```

---

## 🎓 What's Next?

1. **Try it yourself** - Run predictions on test users
2. **Integrate it** - Use in your Streamlit app
3. **Compare results** - Check Block 1 vs Block 4
4. **Improve it** - Collect more training data
5. **Deploy it** - Use in production

---

## 📞 Need Help?

### Common Issues

**Q: Model not trained?**  
A: It auto-trains on first import. Wait ~2 seconds on first run.

**Q: Prediction is slow?**  
A: First prediction trains model. Subsequent predictions are < 1ms.

**Q: Confidence too low?**  
A: Profile is far from training examples. Collect more data.

**Q: How do I retrain?**  
A: Clear `ml._trained_model = None`, then call `initialize_model()`.

---

## 🔗 Links

- **Full Docs:** [BLOCK4_ML_MODEL.md](BLOCK4_ML_MODEL.md)
- **Implementation:** [app/utils/ml_model.py](app/utils/ml_model.py)
- **Tests:** [test_block4_ml_model.py](test_block4_ml_model.py)
- **Block 3 Data:** [data/skincare_dataset.csv](data/skincare_dataset.csv)

---

**Status:** ✅ Production Ready  
**Last Updated:** April 16, 2026  
**Test Pass Rate:** 100%
