"""
Script to generate sample pre-trained models for GlowGuide.
Run this once to populate the models/ directory.
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from pathlib import Path

# Paths
data_dir = Path(__file__).parent / "data"
models_dir = Path(__file__).parent / "models"
models_dir.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(data_dir / "cleaned.csv")

print("🔨 Generating sample pre-trained models...")

# 1. TF-IDF Vectorizer
print("  → Creating TF-IDF Vectorizer...")
vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
X_tfidf = vectorizer.fit_transform(df["Ingredients"].fillna("").apply(lambda x: x.lower()))
joblib.dump(vectorizer, models_dir / "tfidf_vectorizer.pkl")
print("    ✓ Saved: tfidf_vectorizer.pkl")

# 2. Random Forest Classifier (product category)
print("  → Creating Random Forest Classifier...")
y_label = df["Label"]
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_tfidf, y_label)
joblib.dump(clf, models_dir / "classifier_rf.pkl")
print("    ✓ Saved: classifier_rf.pkl")

# 3. Random Forest Regressor (price prediction)
print("  → Creating Random Forest Regressor...")
y_price = df["Price"]
regressor = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
regressor.fit(X_tfidf, y_price)
joblib.dump(regressor, models_dir / "regressor.pkl")
print("    ✓ Saved: regressor.pkl")

# 4. K-Means Clustering
print("  → Creating K-Means Clustering Model...")
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
kmeans.fit(X_tfidf)
joblib.dump(kmeans, models_dir / "kmeans_model.pkl")
print("    ✓ Saved: kmeans_model.pkl")

print("\n✅ All models generated successfully!")
print(f"📁 Models saved to: {models_dir}")
print("\nYou can now run: streamlit run app/app.py")
