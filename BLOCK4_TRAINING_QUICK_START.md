# 🚀 BLOCK 4: MODEL TRAINING - QUICK START

## ⚡ 30-Second Setup

```bash
# Run the model training
cd c:\Users\dhruv\GlowGuide
python -m app.utils.training
```

**Expected Output:**
```
🔷 BLOCK 4: MODEL TRAINING (CLASSIFICATION)

📥 Loading data from Block 1...

🧹 Cleaning data from Block 2...
✅ No missing values found - all 1120 rows retained
✅ Selected columns: ['Skin_Type', 'Sensitivity', 'Concern', 'clean_Ingredients']
✅ Shape after column selection: (1120, 4)
✅ Converted all values to strings and stripped whitespace

🔐 Encoding data from Block 3...
🔹 Encoding Skin_Type...
   ✅ Fitted on 5 unique values
🔹 Encoding Sensitivity...
   ✅ Fitted on 2 unique values
🔹 Encoding Concern...
   ✅ Fitted on 10 unique values
🔹 Encoding clean_Ingredients (TARGET)...
   ✅ Fitted on 504 unique values
✅ Encoded dataset ready: 1120 rows × 4 columns

🎯 Creating and training KNN model...

📊 Preparing features and target...
✅ Features (X) prepared: (1120, 3)
   Columns: ['Skin_Type', 'Sensitivity', 'Concern']
✅ Target (y) prepared: 1120 samples
   Unique classes: 504

🤖 Training KNN model (n_neighbors=3)...
✅ Model trained successfully!
   Training samples: 1120
   Features: 3
   Classes: 504

🤖 MODEL SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Model Details:
   Algorithm: KNeighborsClassifier
   n_neighbors: 3
   Training samples: 1120
   Feature count: 3
   Feature names: ['Skin_Type', 'Sensitivity', 'Concern']
   Classes: 504
   Status: Model trained

🎯 Target Classes (504 total):
   (First 10 shown...)

✨ Block 4 Model Training Complete!
   Ready for Block 5 (Model Evaluation & Predictions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📝 3 Usage Options

### Option 1: One-Line Training
```python
from app.utils.training import main

model, trainer = main()
# Model is now trained and ready!
```

### Option 2: Step-by-Step
```python
from app.utils.training import ModelTrainer
from app.utils.encoding import EncodingManager
from app.utils.preprocessing import clean_dataset
from app.utils.data_loader import load_celestia_dataset

# Load and prepare
df_main = load_celestia_dataset()
df_cleaned = clean_dataset(df_main)

manager = EncodingManager()
df_encoded = manager.encode_dataset(df_cleaned)

# Train
trainer = ModelTrainer(n_neighbors=3)
X, y = trainer.prepare_data(df_encoded)
trainer.train()

# Get model
model = trainer.get_model()
```

### Option 3: Get Model Info
```python
from app.utils.training import main

model, trainer = main()

# Get info
info = trainer.get_model_info()
print(info)

# Print summary
trainer.print_model_summary()
```

---

## 🎯 What Block 4 Does

| Step | Operation | Input | Output |
|------|-----------|-------|--------|
| 1 | Load data | Block 1 | DataFrame (1,120 × 11) |
| 2 | Clean data | Block 2 | DataFrame (1,120 × 4, string) |
| 3 | Encode data | Block 3 | DataFrame (1,120 × 4, int64) |
| 4 | Prepare X & y | Encoded DF | X: (1,120 × 3), y: (1,120,) |
| 5 | Train KNN | X & y | Fitted KNeighborsClassifier |
| 6 | Report | Model | Model summary printed |

---

## 📊 Model Architecture

### Input Features (X)
```
Feature 1: Skin_Type (encoded 0-4)
           - 5 categories (Combination, Dry, Normal, Oily, Sensitive)

Feature 2: Sensitivity (encoded 0-1)
           - 2 categories (No, Yes)

Feature 3: Concern (encoded 0-9)
           - 10 categories (Acne, Aging, Blackheads, ...)
```

### Target Output (y)
```
504 unique ingredient combinations
Encoded as: 0, 1, 2, ..., 503
```

### Algorithm
```
KNeighborsClassifier with k=3
- Finds 3 nearest neighbors
- Returns most common ingredient
```

---

## ✅ Block 4 Checklist

- ✅ **Step 1**: Data loaded from Block 1
- ✅ **Step 2**: Data cleaned by Block 2
- ✅ **Step 3**: Data encoded by Block 3
- ✅ **Step 4**: Features (X) prepared (1,120 × 3)
- ✅ **Step 5**: Target (y) prepared (1,120 samples, 504 classes)
- ✅ **Step 6**: KNN model trained (n_neighbors=3)
- ✅ **Step 7**: Model confirmation printed
- ✅ **Ready for Block 5**: Predictions & evaluation

---

## 🔗 Data Flow

```
Block 1: Load (1,120 × 11)
    ↓
Block 2: Clean (1,120 × 4, string)
    ↓
Block 3: Encode (1,120 × 4, int64)
    ↓
Block 4: Train Model ← You are here
    ↓
Prepare X & y:
  X = Skin_Type, Sensitivity, Concern (1,120 × 3)
  y = clean_Ingredients (1,120 samples, 504 classes)
    ↓
Train KNN (k=3):
  1. Create KNeighborsClassifier(n_neighbors=3)
  2. Fit on 1,120 training samples
  3. Learn the ingredient patterns
    ↓
Output: Trained Model
    ↓
Block 5: Evaluate & Predict
```

---

## 💡 Tips

**Tip 1**: Model is trained on ALL data
```python
# No train/test split in Block 4
# This is intentional - evaluation comes later in Block 5
trainer = ModelTrainer()
trainer.prepare_data(df_encoded)  # 1,120 samples
trainer.train()  # Fit on all 1,120
```

**Tip 2**: Access the trained model
```python
model = trainer.get_model()
# Now you can use it for predictions:
prediction = model.predict([[2, 1, 0]])
```

**Tip 3**: Get model information
```python
info = trainer.get_model_info()
print(f"Training samples: {info['n_training_samples']}")
print(f"Feature count: {info['n_features']}")
print(f"Classes: {info['n_classes']}")
```

---

## 🎯 Key Numbers

| Metric | Value |
|--------|-------|
| **Training samples** | 1,120 |
| **Features** | 3 (Skin_Type, Sensitivity, Concern) |
| **Target classes** | 504 |
| **Algorithm** | KNeighborsClassifier |
| **k (n_neighbors)** | 3 |
| **Training time** | < 1 second |
| **Model trained** | ✅ Yes |
| **Ready for predictions** | ✅ Yes |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| ImportError: KNeighborsClassifier | Install sklearn: `pip install scikit-learn` |
| ModuleNotFoundError | Run from GlowGuide directory |
| Data preparation error | Check Block 3 output is valid |
| Training failed | Verify no NaN values in X or y |

---

## 📞 Get Help

```python
# Check if model trained
trainer = ModelTrainer()
print(trainer.is_trained)  # False initially

# Train
trainer.prepare_data(df_encoded)
trainer.train()
print(trainer.is_trained)  # True now

# Get summary
trainer.print_model_summary()
```

---

## 🔗 Next Steps

1. ✅ Block 1: Data Loading
2. ✅ Block 2: Data Cleaning
3. ✅ Block 3: Encoding
4. ✅ **Block 4: Model Training** (You are here)
5. → **Block 5: Model Evaluation & Predictions** - Evaluate accuracy and make predictions
6. → Block 6+: Integration & UI

The model is trained! Next block will evaluate performance and make predictions.

---

**Status**: ✅ Block 4 Complete  
**Ready for**: Block 5 (Model Evaluation & Predictions)  
**Created**: April 21, 2026
