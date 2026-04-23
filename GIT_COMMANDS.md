# Quick Git Commands for GlowGuide Deployment

Run these commands to push your fixed GlowGuide app to GitHub:

```bash
# Navigate to project directory
cd GlowGuide

# Check git status (should show data/ and models/ as untracked)
git status

# Add data and models folders
git add data/
git add models/

# Add modified files
git add .gitignore
git add app/app.py
git add app/utils/model_loader.py

# Commit changes
git commit -m "Fix Streamlit Cloud deployment: organize models/data, update paths, add verification"

# Push to GitHub
git push origin main

# Verify on GitHub
# Go to: https://github.com/YOUR_USERNAME/GlowGuide
# Check: data/ folder has *.csv files
# Check: models/ folder has *.pkl files
```

---

## Verify Push Succeeded

```bash
# List tracked files in data/ and models/
git ls-tree -r main data/
git ls-tree -r main models/

# Should show all CSV and PKL files
```

---

## Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "Create app"
3. Select your GitHub repository
4. Set main file path to: `app/app.py`
5. Click "Deploy"
6. Wait 2-3 minutes for deployment
7. Test the app

---

## If Something Goes Wrong

```bash
# Check git status
git status

# Check what would be committed
git diff --cached

# View files in data/ folder
ls data/

# View files in models/ folder
ls models/

# Run verification script
python VERIFY_DEPLOYMENT.py
```

---

## Expected Results After Deployment

✅ App starts without errors  
✅ Models load successfully  
✅ No "FileNotFoundError"  
✅ No "Failed to load" messages  
✅ Recommendations work correctly  

If you see errors, check DEPLOYMENT_GUIDE.md for troubleshooting.
