# 🚀 BLOCK 1: DATA LOADING - QUICK START

## ⚡ 30-Second Setup

```bash
# Run the data loader
cd c:\Users\dhruv\GlowGuide
python -m app.utils.data_loader
```

**Expected Output:**
```
🔷 BLOCK 1: DATA LOADING
✅ Celestia dataset loaded: 1120 rows × 11 columns
✅ Products dataset loaded: 1138 rows × 7 columns
✅ Remedies dataset loaded: 400 rows × 12 columns
✅ All datasets verified successfully!
✨ Data loading complete!
```

---

## 📝 3 Usage Options

### Option 1: One-Line Load
```python
from app.utils.data_loader import load_all_datasets

df_main, products_df, remedies_df = load_all_datasets()
```

### Option 2: Individual Loads
```python
from app.utils.data_loader import (
    load_celestia_dataset,
    load_products_dataset,
    load_remedies_dataset
)

df_main = load_celestia_dataset()
products_df = load_products_dataset()
remedies_df = load_remedies_dataset()
```

### Option 3: With Verification
```python
from app.utils.data_loader import load_all_datasets, verify_datasets

df_main, products_df, remedies_df = load_all_datasets()

if verify_datasets(df_main, products_df, remedies_df):
    print("✅ All datasets ready!")
    # Proceed with preprocessing
else:
    print("❌ Dataset loading failed!")
```

---

## 🎯 What Each Dataset Contains

| Dataset | File | Rows | Columns | Purpose |
|---------|------|------|---------|---------|
| **Celestia** | celestia_clean.csv | 1,120 | 11 | Main skincare data |
| **Products** | product.csv | 1,138 | 7 | Product database |
| **Remedies** | remedies.csv | 400 | 12 | Remedy/ingredient mapping |

---

## 📊 Check Your Data

```python
from app.utils.data_loader import load_all_datasets

df_main, products_df, remedies_df = load_all_datasets()

# Check celestia dataset
print(df_main.info())  # Column types and non-null counts
print(df_main.describe())  # Statistical summary

# Check products dataset
print(products_df.head())  # First 5 rows

# Check remedies dataset
print(remedies_df.shape)  # Dimensions
```

---

## ✅ Block 1 Checklist

- ✅ **Celestia dataset**: Loaded (1,120 × 11)
- ✅ **Products dataset**: Loaded (1,138 × 7)
- ✅ **Remedies dataset**: Loaded (400 × 12)
- ✅ **Error handling**: Implemented
- ✅ **Verification**: Available
- ✅ **Documentation**: Complete

---

## 🔗 Next Steps

1. Block 1: ✅ **Data Loading** (You are here)
2. Block 2: **Data Preprocessing** → Clean & transform data
3. Block 3: **Dataset Creation** → Prepare for ML
4. Block 4: **ML Model Training** → Train recommendation engine

---

## 💡 Tips

**Tip 1**: Always verify datasets load before using them
```python
if df_main is not None:
    print("Safe to use df_main!")
```

**Tip 2**: Use `load_all_datasets()` for convenience
```python
# One function, three datasets!
df_main, products_df, remedies_df = load_all_datasets()
```

**Tip 3**: Check data structure with info()
```python
df_main.info()  # See all columns and types
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `FileNotFoundError` | Check CSV files exist in `data/` folder |
| `ParserError` | Verify CSV files are not corrupted |
| Returns `None` | Check console for specific error message |
| Permission denied | Check file permissions: `chmod +r data/*.csv` |

---

## 📞 Get Help

Run with verbose output:
```python
from app.utils.data_loader import load_all_datasets
df_main, products_df, remedies_df = load_all_datasets()
# Console will show detailed loading info
```

---

**Status**: ✅ Block 1 Complete  
**Ready for**: Block 2 (Preprocessing)
