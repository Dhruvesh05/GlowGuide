# ⚡ QUICK START: Run Integrated GlowGuide

## 🚀 Start the App in 30 Seconds

```bash
cd c:\Users\dhruv\GlowGuide
python -m streamlit run app/app.py
```

The app opens at: `http://localhost:8502`

---

## 📋 How to Use

### 1. Fill Your Profile (Sidebar)
```
Skin Type:        Choose one (Combination, Dry, Normal, Oily)
Sensitivity:      Choose one (Yes, No)
Primary Concern:  Choose one of 10 concerns
```

### 2. Click "Get Recommendations"
```
Button: "🔍 Get Ingredient Recommendations" in Product Search tab
```

### 3. View Results
```
✅ Ingredient recommendation
✅ Your skin cluster (Acne-Prone, Dry Skin, or Sensitive Skin)
✅ Top 3 products with prices
✅ Top 2 home remedies with usage
```

---

## ✨ What It Does

| Component | Source | Output |
|-----------|--------|--------|
| **Prediction** | Block 8 (KNN) | Ingredient + Cluster |
| **Products** | Block 9 (Search) | Top 3 with prices |
| **Remedies** | Block 10 (Search) | Top 2 with usage |
| **Integration** | Block 11 | Combined result |

---

## 📊 Speed

- **First Load**: ~2-3 seconds (models load)
- **Each Recommendation**: < 700ms
- **Cached**: ~50ms after first load

---

## 🎨 Features

✅ Modern UI with minimal design  
✅ Real-time ML predictions  
✅ Product recommendations  
✅ Home remedy suggestions  
✅ No data storage  
✅ Fast, responsive interface  

---

## 🔧 Requirements

- Python 3.7+
- Streamlit
- pandas, scikit-learn
- All models in `data/` folder

---

## 📚 Full Documentation

See `INTEGRATION_GUIDE.md` for:
- Detailed configuration
- Architecture explanation
- Troubleshooting guide
- Performance metrics
- Security information

---

**Ready to use!** Run the command above and start getting skincare recommendations. 🌟
