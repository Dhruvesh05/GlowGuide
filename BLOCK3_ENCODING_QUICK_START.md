# 🚀 BLOCK 3: ENCODING - QUICK START

## ⚡ 30-Second Setup

```bash
# Run the encoder
cd c:\Users\dhruv\GlowGuide
python -m app.utils.encoding
```

**Expected Output:**
```
🔷 BLOCK 3: ENCODING

📥 Loading cleaned data from Block 2...
✅ Loaded cleaned data: 1120 rows × 4 columns

🔐 Creating label encoders and encoding data...
🔹 Encoding Skin_Type...
   ✅ Fitted on 5 unique values
🔹 Encoding Sensitivity...
   ✅ Fitted on 2 unique values
🔹 Encoding Concern...
   ✅ Fitted on 10 unique values
🔹 Encoding clean_Ingredients (TARGET)...
   ✅ Fitted on 504 unique values
✅ Encoding complete: 1120 rows × 4 columns

🗂️  ENCODING MAPPINGS

🔹 Skin_Type Encoder (le_skin):
   Classes: ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']
   Mapping:
      0 ← Combination (224 records)
      1 ← Dry (224 records)
      2 ← Normal (224 records)
      3 ← Oily (224 records)
      4 ← Sensitive (224 records)

🔹 Sensitivity Encoder (le_sens):
   Classes: ['No', 'Yes']
   Mapping:
      0 ← No (560 records)
      1 ← Yes (560 records)

🔹 Concern Encoder (le_concern):
   Classes: ['Acne', 'Aging', 'Blackheads', ...]
   Mapping:
      0 ← Acne (160 records)
      1 ← Aging (160 records)
      ...

✨ Block 3 Encoding Complete!
   Ready for Block 4 (Feature Engineering)
```

---

## 📝 3 Usage Options

### Option 1: One-Line Pipeline
```python
from app.utils.encoding import main

df_encoded, manager = main()
```

### Option 2: Step-by-Step
```python
from app.utils.encoding import EncodingManager
from app.utils.preprocessing import clean_dataset
from app.utils.data_loader import load_celestia_dataset

# Load & clean
df_main = load_celestia_dataset()
df_cleaned = clean_dataset(df_main)

# Encode
manager = EncodingManager()
df_encoded = manager.encode_dataset(df_cleaned)

# View mappings
manager.print_mappings()
```

### Option 3: Access Encoders
```python
from app.utils.encoding import main

df_encoded, manager = main()

# Get individual encoders for later use
encoders = manager.get_encoders_dict()
le_skin = encoders['le_skin']
le_sens = encoders['le_sens']
le_concern = encoders['le_concern']
le_target = encoders['le_target']

# Decode values later if needed
original_value = le_skin.inverse_transform([0])  # 'Combination'
```

---

## 🎯 What Block 3 Does

| Step | Operation | Input | Output |
|------|-----------|-------|--------|
| 1 | Load cleaned | Block 2 | DataFrame (1,120 × 4, string) |
| 2 | Create encoders | 4 columns | le_skin, le_sens, le_concern, le_target |
| 3 | Fit & transform | Strings | Integers |
| 4 | Store data | Encoded DF | df_encoded (1,120 × 4, int64) |
| 5 | Report | Mappings | Class-to-number conversion |

---

## 📊 Encoding Results

### Skin_Type (5 classes)
```
0 ← Combination (224 records)
1 ← Dry (224 records)
2 ← Normal (224 records)
3 ← Oily (224 records)
4 ← Sensitive (224 records)
```

### Sensitivity (2 classes)
```
0 ← No (560 records)
1 ← Yes (560 records)
```

### Concern (10 classes)
```
0 ← Acne (160 records)
1 ← Aging (160 records)
2 ← Blackheads (160 records)
3 ← Dryness (160 records)
4 ← Hyperpigmentation (160 records)
5 ← Oiliness (160 records)
6 ← Redness (160 records)
7 ← Scars (160 records)
8 ← Sensitivity (160 records)
9 ← Wrinkles (160 records)
```

### clean_Ingredients (504 classes)
```
0 ← ingredient combo 1
1 ← ingredient combo 2
...
503 ← ingredient combo 504
```

---

## ✅ Block 3 Checklist

- ✅ **Encoder 1**: le_skin for Skin_Type (5 classes)
- ✅ **Encoder 2**: le_sens for Sensitivity (2 classes)
- ✅ **Encoder 3**: le_concern for Concern (10 classes)
- ✅ **Encoder 4**: le_target for clean_Ingredients (504 classes)
- ✅ **Encoded Data**: All 4 columns converted to integers
- ✅ **Mappings**: All class mappings printed
- ✅ **Encoders Stored**: Preserved in manager for later use
- ✅ **No Overwriting**: Original encoders kept safe

---

## 🔗 Data Flow

```
Block 2: Cleaned Data (string)
    ↓
Skin_Type: "Oily", "Dry", ...
Sensitivity: "Yes", "No"
Concern: "Acne", "Aging", ...
clean_Ingredients: "ingredient A B", ...
    ↓
Block 3: Encoding ← You are here
    ↓
Create 4 LabelEncoders:
  - le_skin
  - le_sens
  - le_concern
  - le_target
    ↓
Fit & Transform:
  - Skin_Type → [0, 1, 2, 3, 4]
  - Sensitivity → [0, 1]
  - Concern → [0, 1, ..., 9]
  - clean_Ingredients → [0, 1, ..., 503]
    ↓
Output: Encoded Data (integer)
    ↓
Block 4: Feature Engineering
    ↓
Create features for ML model
```

---

## 💡 Tips

**Tip 1**: Encoders are preserved in the manager object
```python
manager = EncodingManager()
manager.encode_dataset(df_cleaned)

# Access later:
encoders = manager.get_encoders_dict()
le_skin = encoders['le_skin']
```

**Tip 2**: Decode values if needed
```python
# Encode: string → number
encoded_val = manager.le_skin.transform(['Oily'])  # [3]

# Decode: number → string
original_val = manager.le_skin.inverse_transform([3])  # ['Oily']
```

**Tip 3**: View all encoder info
```python
info = manager.get_encoder_info()
print(info['le_skin']['classes'])  # All Skin_Type values
print(info['le_skin']['n_classes'])  # 5
```

---

## 🎯 Key Numbers

| Metric | Value |
|--------|-------|
| **Rows encoded** | 1,120 |
| **Columns encoded** | 4 |
| **Skin_Type classes** | 5 |
| **Sensitivity classes** | 2 |
| **Concern classes** | 10 |
| **Ingredient classes** | 504 |
| **Missing values after encoding** | 0 |
| **Data type after encoding** | int64 |
| **Ready for next block** | ✅ Yes |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| ImportError: LabelEncoder | Install sklearn: `pip install scikit-learn` |
| ModuleNotFoundError | Run from GlowGuide directory |
| DataFrame is None | Check Block 2 output is valid |
| Encoding error | Verify no NaN values in input |

---

## 📞 Get Help

```python
# Check encoder mappings:
manager.print_mappings()

# Check encoded data:
print(manager.get_encoded_dataset().head())

# Check encoder info:
info = manager.get_encoder_info()
print(info)
```

---

## 🔗 Next Steps

1. ✅ Block 1: Data Loading
2. ✅ Block 2: Data Cleaning
3. ✅ **Block 3: Encoding** (You are here)
4. → **Block 4: Feature Engineering** - Create ML features
5. → Block 5+: Model Training & Integration

Ready for Block 4? Encoded data is ready!

---

**Status**: ✅ Block 3 Complete  
**Ready for**: Block 4 (Feature Engineering)  
**Created**: April 21, 2026
