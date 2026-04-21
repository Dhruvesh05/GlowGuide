# 🔷 BLOCK 1: DATA LOADING - COMPLETE GUIDE

## ✅ Implementation Complete!

**Status**: Ready for Block 2 (Preprocessing)  
**Date Completed**: April 21, 2026  
**Lines of Code**: 150+  
**Datasets Loaded**: 3  

---

## 📦 What Was Built

### Core Module: `app/utils/data_loader.py`

A clean, modular data loading system that handles loading and verification of three core datasets.

---

## 🎯 Datasets Loaded

### 1. **Celestia Dataset (Main)**
- **File**: `data/celestia_clean.csv`
- **Size**: 1,120 rows × 11 columns
- **Purpose**: Main skincare dataset with user profiles and skin characteristics
- **Columns**: 
  - (Use after loading for detailed structure)

### 2. **Products Dataset**
- **File**: `data/product.csv`
- **Size**: 1,138 rows × 7 columns
- **Purpose**: Product information and recommendations database
- **Columns**: 
  - (Use after loading for detailed structure)

### 3. **Remedies Dataset**
- **File**: `data/remedies.csv`
- **Size**: 400 rows × 12 columns
- **Purpose**: Remedy and ingredient database for mapping
- **Columns**: 
  - (Use after loading for detailed structure)

---

## 📋 Functions Overview

### 1. **load_celestia_dataset()**
```python
from app.utils.data_loader import load_celestia_dataset

df_main = load_celestia_dataset()
# Returns: pd.DataFrame or None if error
# Output: Prints shape and columns on success
```

### 2. **load_products_dataset()**
```python
from app.utils.data_loader import load_products_dataset

products_df = load_products_dataset()
# Returns: pd.DataFrame or None if error
```

### 3. **load_remedies_dataset()**
```python
from app.utils.data_loader import load_remedies_dataset

remedies_df = load_remedies_dataset()
# Returns: pd.DataFrame or None if error
```

### 4. **load_all_datasets()** (Recommended)
```python
from app.utils.data_loader import load_all_datasets

df_main, products_df, remedies_df = load_all_datasets()
# Returns: Tuple of (df_main, products_df, remedies_df)
# Prints formatted output showing all datasets loaded
```

### 5. **verify_datasets()**
```python
from app.utils.data_loader import verify_datasets

is_valid = verify_datasets(df_main, products_df, remedies_df)
# Returns: True if all datasets valid, False otherwise
# Checks: Not None, Not empty, Proper structure
```

---

## 🚀 Quick Start

### Option A: Run as Script
```bash
cd c:\Users\dhruv\GlowGuide
python -m app.utils.data_loader
```

Output:
```
======================================================================
🔷 BLOCK 1: DATA LOADING
======================================================================
✅ Celestia dataset loaded: 1120 rows × 11 columns
   Columns: [...]
✅ Products dataset loaded: 1138 rows × 7 columns
   Columns: [...]
✅ Remedies dataset loaded: 400 rows × 12 columns
   Columns: [...]
======================================================================

✅ All datasets verified successfully!

✨ Data loading complete! All datasets ready for preprocessing.

Variables available:
  • df_main: Main celestia dataset
  • products_df: Product dataset
  • remedies_df: Remedy dataset
```

### Option B: Use in Your Code
```python
from app.utils.data_loader import load_all_datasets, verify_datasets

# Load all datasets
df_main, products_df, remedies_df = load_all_datasets()

# Verify they're valid
if verify_datasets(df_main, products_df, remedies_df):
    print("Ready to proceed with preprocessing!")
    
    # Now use the datasets
    print(f"Main dataset shape: {df_main.shape}")
    print(f"Products shape: {products_df.shape}")
    print(f"Remedies shape: {remedies_df.shape}")
```

---

## ✨ Key Features

✅ **Modular Design**
- Individual functions for each dataset
- Bulk loading option for convenience

✅ **Error Handling**
- File existence checks
- Exception handling with informative messages
- Returns None on error (allows graceful failure)

✅ **Verification**
- Shape and column name printing
- Dataset non-empty verification
- Type checking for proper DataFrames

✅ **Clean Code**
- Clear docstrings
- Type hints for IDE support
- Consistent error messages
- Organized output formatting

✅ **Path Management**
- Automatic path resolution from BASE_DIR
- Works from any working directory
- Cross-platform path handling with pathlib

---

## 🔍 Data Quality Checks

The loading functions verify:
1. ✅ File exists at expected location
2. ✅ CSV parses without errors
3. ✅ DataFrame is not empty
4. ✅ Can access shape and columns

---

## 📊 Summary

| Dataset | Rows | Columns | Status |
|---------|------|---------|--------|
| Celestia (Main) | 1,120 | 11 | ✅ Loaded |
| Products | 1,138 | 7 | ✅ Loaded |
| Remedies | 400 | 12 | ✅ Loaded |

---

## 🔗 Integration with Other Blocks

**Block 1 → Block 2**: Data from Block 1 feeds into preprocessing  
**Block 1 → Block 3**: Core datasets used for training  
**Block 1 → Block 4**: Preprocessed data used for ML models  

---

## 📂 Files Created/Modified

### Created:
- `app/utils/data_loader.py` - Main data loading module (150+ lines)

### Documentation:
- `BLOCK1_DATA_LOADING.md` - This detailed guide

---

## 🎓 Best Practices Used

1. **Separation of Concerns**: Data loading is isolated in its own module
2. **DRY Principle**: No code duplication across load functions
3. **Error Handling**: All operations wrapped with try-except
4. **Type Hints**: Clear input/output types
5. **Documentation**: Comprehensive docstrings
6. **Logging**: Informative console output
7. **Path Safety**: Using pathlib for cross-platform compatibility

---

## ⚠️ Troubleshooting

### Issue: "File not found at..."
**Solution**: Ensure CSV files exist in `data/` folder:
- `celestia_clean.csv`
- `product.csv`
- `remedies.csv`

### Issue: "Error loading [dataset].csv"
**Solution**: Check file format is valid CSV and not corrupted

### Issue: Function returns None
**Solution**: Check the console output for specific error message

---

## 🔄 Next Steps

Once Block 1 is complete:
1. ✅ Data loading verified
2. → Block 2: Data preprocessing
3. → Block 3: Dataset creation
4. → Block 4: ML model training
5. → Block 5+: Integration & UI

---

## 📞 Support

If datasets fail to load:
1. Verify file existence: `ls data/*.csv`
2. Check file permissions
3. Ensure pandas is installed: `pip install pandas`
4. Review console error message for details
