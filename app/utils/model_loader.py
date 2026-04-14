"""Centralized model and data loading with Streamlit caching."""

import joblib
import streamlit as st
from pathlib import Path
import pandas as pd

# Resolve base directory for models
BASE_DIR = Path(__file__).parent.parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent.parent / "data"


@st.cache_resource
def load_classifier():
    """
    Load the Random Forest classifier model.
    """
    try:
        path = BASE_DIR / "classifier_rf.pkl"
        if not path.exists():
            st.error(f"Classifier not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading classifier: {str(e)}")
        return None


@st.cache_resource
def load_recommender():
    """
    Load the TF-IDF vectorizer for recommendation engine.
    """
    try:
        path = BASE_DIR / "tfidf_vectorizer.pkl"
        if not path.exists():
            st.error(f"TF-IDF vectorizer not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading vectorizer: {str(e)}")
        return None


@st.cache_resource
def load_regressor():
    """
    Load the Random Forest regressor for price prediction.
    """
    try:
        path = BASE_DIR / "regressor.pkl"
        if not path.exists():
            st.error(f"Regressor not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading regressor: {str(e)}")
        return None


@st.cache_resource
def load_kmeans():
    """
    Load the K-Means clustering model.
    """
    try:
        path = BASE_DIR / "kmeans_model.pkl"
        if not path.exists():
            st.error(f"K-Means model not found at {path}")
            return None
        return joblib.load(path)
    except Exception as e:
        st.error(f"Error loading K-Means model: {str(e)}")
        return None


@st.cache_data
def load_dataframe():
    """
    Load the cleaned CSV dataset into a pandas DataFrame.
    """
    try:
        path = DATA_DIR / "cleaned.csv"
        if not path.exists():
            st.error(f"Data file not found at {path}")
            return None
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None
