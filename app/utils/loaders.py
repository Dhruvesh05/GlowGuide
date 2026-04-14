"""Model and data loading with Streamlit caching."""

import joblib
import streamlit as st
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent.parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"


@st.cache_resource
def load_classifier():
    """Load Random Forest classifier from models/classifier_rf.pkl."""
    try:
        path = MODELS_DIR / "classifier_rf.pkl"
        if not path.exists():
            st.error(f"Classifier not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading classifier: {str(e)}")
        return None


@st.cache_resource
def load_vectorizer():
    """Load TF-IDF vectorizer from models/tfidf_vectorizer.pkl."""
    try:
        path = MODELS_DIR / "tfidf_vectorizer.pkl"
        if not path.exists():
            st.error(f"TF-IDF vectorizer not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading vectorizer: {str(e)}")
        return None


@st.cache_resource
def load_regressor():
    """Load price regressor from models/regressor.pkl."""
    try:
        path = MODELS_DIR / "regressor.pkl"
        if not path.exists():
            st.error(f"Regressor not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading regressor: {str(e)}")
        return None


@st.cache_resource
def load_kmeans():
    """Load K-Means model from models/kmeans_model.pkl."""
    try:
        path = MODELS_DIR / "kmeans_model.pkl"
        if not path.exists():
            st.error(f"K-Means model not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading K-Means model: {str(e)}")
        return None


@st.cache_data
def load_dataframe():
    """Load and validate cleaned.csv from data/cleaned.csv."""
    try:
        path = DATA_DIR / "cleaned.csv"
        if not path.exists():
            st.error(f"Data file not found at {path}")
            return None
        df = pd.read_csv(path)
        
        required_cols = ["Name", "Brand", "Price", "Rank", "Ingredients", "Label", "Cluster",
                        "Combination", "Dry", "Normal", "Oily", "Sensitive"]
        assert all(col in df.columns for col in required_cols), \
            f"Missing columns: {[c for c in required_cols if c not in df.columns]}"
        
        return df
    except AssertionError as e:
        st.error(f"Invalid data schema: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None


def validate_all_assets() -> bool:
    """Return True only if all models and dataframe loaded successfully."""
    clf = load_classifier()
    vec = load_vectorizer()
    reg = load_regressor()
    km = load_kmeans()
    df = load_dataframe()
    return all(x is not None for x in [clf, vec, reg, km, df])
