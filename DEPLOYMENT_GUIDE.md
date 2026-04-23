# GlowGuide Streamlit Cloud Deployment Guide

## Overview
This guide ensures GlowGuide datasets and ML models load correctly on Streamlit Cloud and work locally.

---

## ✅ Fixed Issues

### 1. ✓ `.gitignore` Updated
**Before:** Blocked data and models from GitHub  
**After:** Only ignores development files (`__pycache__/`, `.venv/`, etc.)

```diff
- *.pkl           # ❌ Was blocking model files
- *.csv           # ❌ Was blocking datasets
```

**What was removed:**
- `*.pkl` - Was preventing model files from being pushed
- `*.csv` - Was preventing dataset files from being pushed

---

### 2. ✓ Folder Structure Reorganized

```
GlowGuide/
│
├── app/                          # Application code
│   ├── app.py                    # Main Streamlit app
│   ├── utils/
│   │   ├── model_loader.py      # ✅ Updated to load from models/
│   │   └── data_loader.py       # Loads from data/
│   └── components/
│
├── data/                         # ✅ Datasets (tracked in git)
│   ├── celestia_clean.csv       # Main skincare dataset
│   ├── product.csv              # Product database
│   ├── remedies.csv             # Remedy database
│   └── skincare_dataset.csv     # Additional dataset
│
├── models/                       # ✅ ML Models (tracked in git)
│   ├── knn_model.pkl            # KNN classifier
│   ├── kmeans_model.pkl         # KMeans clustering
│   ├── le_skin.pkl              # Skin type encoder
│   ├── le_sens.pkl              # Sensitivity encoder
│   ├── le_concern.pkl           # Concern encoder
│   └── le_target.pkl            # Target encoder
│
└── requirements.txt              # Python dependencies
```

---

### 3. ✓ Path Handling Fixed

#### Using Relative Paths (NOT absolute paths)

**`app/utils/model_loader.py`** - Now loads from `models/` folder:
```python
def __init__(self, data_dir: Optional[str] = None):
    if data_dir is None:
        base_dir = Path(__file__).parent.parent.parent  # Project root
        data_dir = base_dir / "models"  # ✅ Relative path
```

**`app/utils/data_loader.py`** - Already using relative paths:
```python
BASE_DIR = Path(__file__).parent.parent.parent  # Project root
DATA_DIR = BASE_DIR / "data"                    # ✅ Relative path

def load_celestia_dataset():
    file_path = DATA_DIR / "celestia_clean.csv"
```

---

### 4. ✓ File Path Validation Added

**`app/app.py`** now includes startup validation:

```python
def verify_required_files():
    """
    Verify that all required data and model files exist.
    Uses relative paths for Streamlit Cloud compatibility.
    """
    # Checks for:
    # - data/celestia_clean.csv
    # - data/product.csv
    # - data/remedies.csv
    # - models/knn_model.pkl
    # - models/kmeans_model.pkl
    # - models/le_*.pkl (4 encoders)
```

---

### 5. ✓ Error Handling Enhanced

**Load function now includes:**
- Pre-load file validation
- Detailed error messages
- Helpful tips for troubleshooting

```python
@st.cache_resource
def load_ml_models():
    files_ok, status_msg = verify_required_files()
    if not files_ok:
        st.error(status_msg)  # Shows what's missing
        return None
```

---

## 🚀 Deployment Steps

### Local Testing (Before Deployment)

1. **Verify structure:**
   ```bash
   ls -la data/       # Should show: celestia_clean.csv, product.csv, remedies.csv
   ls -la models/     # Should show: 6 .pkl files
   ```

2. **Test the app:**
   ```bash
   streamlit run app/app.py
   ```
   
   Expected: App loads without "Failed to load" errors

3. **Run tests:**
   ```bash
   python -m pytest test_*.py
   ```

---

### Push to GitHub

1. **Remove old ignores (already done in .gitignore):**
   ```bash
   git status  # Should show data/ and models/ as untracked
   ```

2. **Add files to git:**
   ```bash
   git add data/
   git add models/
   git status  # Should show both as "new file"
   ```

3. **Commit with message:**
   ```bash
   git commit -m "Add data and models for Streamlit Cloud deployment"
   ```

4. **Push to repository:**
   ```bash
   git push origin main
   ```

5. **Verify on GitHub:**
   - Go to your repo on github.com
   - Check that `data/` and `models/` folders appear with files

---

### Deploy to Streamlit Cloud

1. **Link repository:**
   - Go to https://share.streamlit.io
   - Click "Create app"
   - Select your GitHub repository
   - Set main file to: `app/app.py`

2. **First deployment:**
   - Streamlit Cloud clones your repo
   - Pulls all files (including data/ and models/)
   - Runs `pip install -r requirements.txt`
   - Starts the app

3. **If deployment fails:**
   - Check that files were pushed to GitHub
   - Check Streamlit Cloud logs for errors
   - Verify folder structure matches documentation

---

## 🔍 Troubleshooting

### ❌ "Failed to load data" error

**Cause:** Files not in GitHub repo

**Fix:**
```bash
git add data/ models/
git commit -m "Add missing files"
git push origin main
# Wait 2-3 minutes for Streamlit Cloud to detect changes
# Then refresh the app
```

---

### ❌ "FileNotFoundError: models/knn_model.pkl"

**Cause:** Models still in wrong location

**Fix:**
```bash
ls models/          # Check files are there
git status models/  # Verify git is tracking them
git push            # Push to GitHub
```

---

### ❌ "ModuleNotFoundError" on Streamlit Cloud

**Cause:** Requirements missing

**Fix:**
1. Verify `requirements.txt` has all dependencies
2. Update it:
   ```bash
   pip freeze > requirements.txt
   git add requirements.txt
   git commit -m "Update requirements"
   git push
   ```

---

### ✅ Testing the app

**Local:**
```bash
streamlit run app/app.py
```
Expected: No "Failed to load" errors

**On Streamlit Cloud:**
- Open your deployed app URL
- Check for error messages in the UI
- Use Streamlit Cloud logs to debug

---

## 📋 Checklist

Before deploying, verify:

- [ ] `.gitignore` no longer blocks `*.pkl` and `*.csv`
- [ ] `data/` folder exists with all CSV files
- [ ] `models/` folder exists with all `.pkl` files
- [ ] `app/app.py` has `verify_required_files()` function
- [ ] `app/utils/model_loader.py` loads from `models/` folder
- [ ] Local test passes: `streamlit run app/app.py`
- [ ] All changes committed to GitHub
- [ ] Files are visible on GitHub repository page
- [ ] Streamlit Cloud app is deployed

---

## 🎯 Expected Results

### Local Execution
✅ App starts without errors  
✅ Models load in < 2 seconds  
✅ All recommendations work  
✅ Charts and visualizations display  

### Streamlit Cloud
✅ App deploys successfully  
✅ No "FileNotFoundError"  
✅ No "Failed to load" messages  
✅ All features work as expected  

---

## 📝 Technical Details

### Why This Works

1. **Relative Paths:** `Path(__file__).parent.parent` works the same on:
   - Your local machine
   - GitHub Actions
   - Streamlit Cloud
   - Any cloud platform

2. **Git Tracking:** By removing `*.pkl` and `*.csv` from `.gitignore`:
   - GitHub stores the actual model and dataset files
   - Streamlit Cloud pulls them during deployment
   - No need for external storage (S3, etc.)

3. **Caching:** Streamlit's `@st.cache_resource` ensures models load once per session:
   - Fast subsequent page interactions
   - Efficient memory usage

---

## 🆘 Getting Help

If deployment still fails:

1. Check Streamlit Cloud app logs
2. Run `git log --oneline` to verify commits
3. Go to GitHub repo → Check `data/` and `models/` folders exist
4. Clear Streamlit Cloud cache: Settings → Reboot app

---

## ✨ Summary

**What was fixed:**
1. ✓ Removed blocking gitignore entries
2. ✓ Reorganized files into `data/` and `models/` folders
3. ✓ Updated ModelLoader to use `models/` folder
4. ✓ Added startup file validation
5. ✓ Enhanced error messages with fixes

**Result:** GlowGuide now works on Streamlit Cloud! 🎉
