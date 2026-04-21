# 🚀 BLOCK 2: DATA CLEANING - QUICK START

## ⚡ 30-Second Setup

```bash
# Run the data cleaning
cd c:\Users\dhruv\GlowGuide
python -m app.utils.preprocessing
```

**Expected Output:**
```
🔷 BLOCK 2: DATA CLEANING & PREPROCESSING

📥 Loading data from Block 1...
✅ Loaded: 1120 rows × 11 columns

🧹 Cleaning dataset...
✅ No missing values found - all 1120 rows retained
✅ Selected columns: ['Skin_Type', 'Sensitivity', 'Concern', 'clean_Ingredients']
✅ Shape after column selection: (1120, 4)
✅ Converted all values to strings and stripped whitespace

📊 UNIQUE VALUES

🔹 Skin_Type:
   Count: 5
      • Combination (224 records)
      • Dry (224 records)
      • Normal (224 records)
      • Oily (224 records)
      • Sensitive (224 records)

🔹 Sensitivity:
   Count: 2
      • No (560 records)
      • Yes (560 records)

🔹 Concern:
   Count: 7
      • Acne (160 records)
      • Aging (160 records)
      • Dryness (160 records)
      • Hyperpigmentation (160 records)
      • Oiliness (160 records)
      • Redness (160 records)
      • Sensitivity (160 records)

✨ Block 2 Data Cleaning Complete!
```

---

## 📝 3 Usage Options

### Option 1: Simple One-Liner
```python
from app.utils.preprocessing import main

df_cleaned = main()
```

### Option 2: Step-by-Step
```python
from app.utils.preprocessing import clean_dataset, print_unique_values
from app.utils.data_loader import load_celestia_dataset

# Step 1: Load
df_main = load_celestia_dataset()

# Step 2: Clean
df_cleaned = clean_dataset(df_main)

# Step 3: Inspect
print_unique_values(df_cleaned)
```

### Option 3: Custom Processing
```python
from app.utils.preprocessing import (
    clean_dataset, 
    print_unique_values,
    get_dataset_info
)
from app.utils.data_loader import load_celestia_dataset

df_main = load_celestia_dataset()
df_cleaned = clean_dataset(df_main)

# Get all details
get_dataset_info(df_cleaned)

# See unique values
print_unique_values(df_cleaned)

# Now use df_cleaned for next block
```

---

## 🎯 What Block 2 Does

| Step | Operation | Input | Output |
|------|-----------|-------|--------|
| 1 | Load data | Block 1 | DataFrame (1,120 × 11) |
| 2 | Remove nulls | dropna() | DataFrame (1,120 × 11) |
| 3 | Select cols | 4 columns | DataFrame (1,120 × 4) |
| 4 | Convert types | str() | All string type |
| 5 | Normalize | strip() | Clean values |
| 6 | Report | Print stats | Unique value counts |

---

## 📊 Input vs Output

### Input (from Block 1)
```
celestia_clean.csv
├─ 1,120 rows
├─ 11 columns
├─ Columns: Age_Group, Skin_Type, Skin_Subtype, 
│           Sensitivity, Concern, Internal_Type, 
│           Ingredients, Concentrations, Effects,
│           Ingredients_list, clean_Ingredients
└─ No missing values
```

### Output (Block 2 Result)
```
df_cleaned
├─ 1,120 rows
├─ 4 columns (selected)
├─ Columns: Skin_Type, Sensitivity, Concern, clean_Ingredients
├─ All values: string type
├─ No missing values
└─ Ready for: Block 3
```

---

## ✅ Block 2 Checklist

- ✅ **Step 1**: Null values removed with dropna()
- ✅ **Step 2**: 4 columns selected
- ✅ **Step 3**: All values converted to strings
- ✅ **Step 4**: Whitespace stripped for consistency
- ✅ **Step 5**: Unique values printed for verification
- ✅ **Step 6**: No encoding applied (reserved for Block 3)

---

## 🔗 Data Flow

```
Block 1: Load Data
    ↓
celestia_clean.csv (1,120 × 11)
    ↓
Block 2: Clean Data ← You are here
    ↓
Steps:
  1. dropna() - Remove missing
  2. Select 4 columns
  3. Convert to string
  4. Strip whitespace
  5. Print unique values
    ↓
Cleaned Data (1,120 × 4)
    ↓
Block 3: Create Dataset
    ↓
Features for ML training
```

---

## 💡 Tips

**Tip 1**: Block 2 ONLY cleans - encoding is in Block 3
```python
# Don't do this in Block 2:
# ❌ df['Skin_Type'] = le.fit_transform(df['Skin_Type'])

# Block 2 just cleans:
# ✅ df['Skin_Type'] = df['Skin_Type'].astype(str).str.strip()
```

**Tip 2**: Check unique values before next block
```python
from app.utils.preprocessing import print_unique_values
print_unique_values(df_cleaned)
# Helps understand the data distribution
```

**Tip 3**: Use get_dataset_info() for full details
```python
from app.utils.preprocessing import get_dataset_info
get_dataset_info(df_cleaned)
# Shows types, nulls, memory usage, shape
```

---

## 🎯 Key Numbers

| Metric | Value |
|--------|-------|
| **Rows processed** | 1,120 |
| **Rows removed** | 0 |
| **Rows kept** | 1,120 |
| **Columns selected** | 4 |
| **Columns removed** | 7 |
| **Missing values after clean** | 0 |
| **Data types** | All string (object) |
| **Ready for next block** | ✅ Yes |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Import error | Make sure you're in GlowGuide directory |
| Module not found | Run: `cd c:\Users\dhruv\GlowGuide` |
| DataFrame is None | Check Block 1 loads successfully first |
| Missing columns | Verify celestia_clean.csv has required columns |

---

## 📞 Get Help

```python
# Check if your data cleaned correctly:
from app.utils.preprocessing import get_dataset_info
get_dataset_info(df_cleaned)

# See the unique values in each column:
from app.utils.preprocessing import print_unique_values
print_unique_values(df_cleaned)
```

---

## 🔗 Next Steps

1. ✅ Block 1: Data Loading
2. ✅ **Block 2: Data Cleaning** (You are here)
3. → **Block 3: Dataset Creation** - Feature engineering & preparation
4. → Block 4: ML Model Training
5. → Block 5+: Integration & UI

Ready to move to Block 3? The cleaned data is ready!

---

**Status**: ✅ Block 2 Complete  
**Ready for**: Block 3 (Dataset Creation)  
**Created**: April 21, 2026
