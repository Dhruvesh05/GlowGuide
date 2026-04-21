# 🚀 BLOCK 6: SAVE MODELS - QUICK START

## ⚡ 30-Second Setup

```bash
# Run the model saving
cd c:\Users\dhruv\GlowGuide
python -m app.utils.model_saver
```

**Expected Output:**
```
🔷 BLOCK 6: SAVE MODELS (MODEL PERSISTENCE)

📥 Loading and training models from previous blocks...

🔐 Creating encoders from Block 3...
✅ Encoders ready

🤖 Training KNN model from Block 4...
✅ KNN model trained

🔷 Training KMeans model from Block 5...
✅ KMeans model trained

💾 Creating model persistence manager...

📝 Registering models for saving...
   ✅ Registered: knn_model
   ✅ Registered: kmeans_model
   ✅ Registered: le_skin, le_sens, le_concern, le_target

💾 Saving models and encoders to disk...
   ✅ knn_model.pkl saved (82020 bytes)
   ✅ kmeans_model.pkl saved (5154 bytes)
   ✅ le_skin.pkl saved (279 bytes)
   ✅ le_sens.pkl saved (254 bytes)
   ✅ le_concern.pkl saved (379 bytes)
   ✅ le_target.pkl saved (22307 bytes)

📊 SAVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Save Location:
   c:\Users\dhruv\GlowGuide\data

💾 Models Saved:
   ✅ knn_model.pkl (82020 bytes)
   ✅ kmeans_model.pkl (5154 bytes)
   ✅ le_skin.pkl (279 bytes)
   ✅ le_sens.pkl (254 bytes)
   ✅ le_concern.pkl (379 bytes)
   ✅ le_target.pkl (22307 bytes)

📈 Statistics:
   Files saved: 6
   Total size: 110393 bytes (107.81 KB)

✨ All models persisted successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Block 6 Model Persistence Complete!
   Status: All models saved successfully
   Ready for: Block 7 (Load and use models)
```

---

## 📝 3 Usage Options

### Option 1: One-Line Save
```python
from app.utils.model_saver import main

success, persistence = main()
# All models saved to data/ folder
```

### Option 2: Step-by-Step
```python
from app.utils.model_saver import ModelPersistence
from app.utils.training import ModelTrainer
from app.utils.encoding import EncodingManager

# Train models first
encoder_mgr = EncodingManager()
df_encoded = encoder_mgr.encode_dataset(df_cleaned)

trainer = ModelTrainer()
trainer.prepare_data(df_encoded)
trainer.train()

# Save models
persistence = ModelPersistence(data_dir='data')
persistence.add_model('knn_model', trainer.get_model())
persistence.add_encoder('le_skin', encoder_mgr.get_encoders_dict()['le_skin'])
# ... add other encoders ...
persistence.save_models()
```

### Option 3: Load Saved Models Later
```python
import pickle

# Load KNN model
with open('data/knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)

# Load encoder
with open('data/le_skin.pkl', 'rb') as f:
    le_skin = pickle.load(f)

# Use models
prediction = knn_model.predict([[2, 1, 0]])
```

---

## 🎯 What Block 6 Does

| Step | Operation | Input | Output |
|------|-----------|-------|--------|
| 1 | Load data | Block 1 | DataFrame (1,120 × 11) |
| 2 | Clean data | Block 2 | DataFrame (1,120 × 4, string) |
| 3 | Encode data | Block 3 | 4 LabelEncoders + encoded DF |
| 4 | Train KNN | Block 4 | KNeighborsClassifier (1,120 samples) |
| 5 | Train KMeans | Block 5 | KMeans (1,120 samples, 3 clusters) |
| 6 | Create persistence | Manager | ModelPersistence instance |
| 7 | Register models | Manager | 6 models/encoders registered |
| 8 | Save to disk | Pickle | 6 .pkl files (107.81 KB total) |

---

## 📊 Saved Files Overview

### Models (2 files)
```
knn_model.pkl (82,020 bytes)
  - KNeighborsClassifier
  - Trained on 1,120 samples
  - 3 features, 504 classes

kmeans_model.pkl (5,154 bytes)
  - KMeans clustering
  - Fitted on 1,120 samples
  - 3 clusters
```

### Encoders (4 files)
```
le_skin.pkl (279 bytes)
  - Encodes Skin_Type (5 categories)

le_sens.pkl (254 bytes)
  - Encodes Sensitivity (2 categories)

le_concern.pkl (379 bytes)
  - Encodes Concern (10 categories)

le_target.pkl (22,307 bytes)
  - Encodes clean_Ingredients (504 categories)
```

### Total
```
6 files
107.81 KB
Located in: c:\Users\dhruv\GlowGuide\data\
```

---

## ✅ Block 6 Checklist

- ✅ **Step 1**: Load data from Block 1
- ✅ **Step 2**: Clean data from Block 2
- ✅ **Step 3**: Create encoders from Block 3
- ✅ **Step 4**: Train KNN from Block 4
- ✅ **Step 5**: Train KMeans from Block 5
- ✅ **Step 6**: Create ModelPersistence
- ✅ **Step 7**: Register all 6 models/encoders
- ✅ **Step 8**: Save to data/ folder using pickle
- ✅ **Step 9**: Print confirmation with file sizes
- ✅ **Ready for Block 7**: Load and use saved models

---

## 🔗 Data Flow

```
Blocks 1-5: Train Models
    ↓
Block 3 Encoders:
  le_skin, le_sens, le_concern, le_target
    ↓
Block 4 KNN Model:
  KNeighborsClassifier (k=3)
    ↓
Block 5 KMeans Model:
  KMeans (3 clusters)
    ↓
Block 6: Save to Disk ← You are here
    ↓
Create ModelPersistence:
  1. Register 2 models + 4 encoders
  2. Save to data/ folder
  3. Use pickle format
    ↓
Output: 6 .pkl files (107.81 KB)
    ↓
Block 7: Load and Use
```

---

## 💡 Tips

**Tip 1**: Access saved files
```bash
# List all saved files
ls c:\Users\dhruv\GlowGuide\data\*.pkl

# Check file sizes
dir c:\Users\dhruv\GlowGuide\data\*.pkl
```

**Tip 2**: Load without retraining
```python
import pickle

# No need to retrain - just load!
with open('data/knn_model.pkl', 'rb') as f:
    knn = pickle.load(f)

# Ready to make predictions immediately
prediction = knn.predict(X)
```

**Tip 3**: Get save status
```python
from app.utils.model_saver import ModelPersistence

persistence = ModelPersistence()
status = persistence.get_save_status()
for file, info in status.items():
    print(f"{file}: {info['status']}")
```

**Tip 4**: Save custom models
```python
persistence = ModelPersistence(data_dir='data')
persistence.add_model('custom_model', my_model)
persistence.add_encoder('custom_encoder', my_encoder)
persistence.save_models()
```

---

## 🎯 Key Numbers

| Metric | Value |
|--------|-------|
| **Models saved** | 2 (KNN, KMeans) |
| **Encoders saved** | 4 (skin, sens, concern, target) |
| **Total files** | 6 |
| **Total size** | 107.81 KB |
| **Format** | Pickle (.pkl) |
| **Location** | data/ folder |
| **Training samples** | 1,120 |
| **Ready to load** | ✅ Yes |
| **Ready for Block 7** | ✅ Yes |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Permission denied | Ensure write access to data/ folder |
| FileNotFoundError | Run Blocks 1-5 first to train models |
| Pickle error | Ensure Python 3.7+ installed |
| Disk space error | Free up disk space before saving |

---

## 📞 Get Help

```python
# Check save status
persistence = ModelPersistence()
print(persistence.get_save_status())

# Print summary
persistence.print_save_summary()

# Verify files exist
import os
files = os.listdir('data')
print([f for f in files if f.endswith('.pkl')])
```

---

## 🔗 Next Steps

1. ✅ Block 1: Data Loading
2. ✅ Block 2: Data Cleaning
3. ✅ Block 3: Encoding
4. ✅ Block 4: Model Training (KNN)
5. ✅ Block 5: Clustering (KMeans)
6. ✅ **Block 6: Save Models** (You are here)
7. → **Block 7: Load and Use** - Load models without retraining
8. → Block 8+: Integration & UI

Models are now persisted to disk! Next block will load and use them.

---

**Status**: ✅ Block 6 Complete  
**Files Saved**: 6 (.pkl files, 107.81 KB)  
**Ready for**: Block 7 (Load and Use)  
**Created**: April 21, 2026
