"""Ingredient analysis engine for skincare products."""

import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from collections import Counter

nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))

IRRITANTS = [
    "alcohol denat", "fragrance", "parfum", "sodium lauryl sulfate",
    "sodium laureth sulfate", "methylisothiazolinone", "formaldehyde",
    "propylene glycol", "butylene glycol", "phenoxyethanol"
]

ACTIVES = [
    "niacinamide", "hyaluronic acid", "retinol", "retinyl palmitate",
    "salicylic acid", "vitamin c", "ascorbic acid", "ceramide",
    "peptide", "glycolic acid", "lactic acid", "ferulic acid",
    "zinc", "kojic acid", "azelaic acid", "tranexamic acid",
    "panthenol", "allantoin", "squalane", "bakuchiol"
]


def clean_text(text: str) -> str:
    """Lowercase, remove punctuation/numbers, strip stopwords."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    words = [w for w in text.split() if w not in STOPWORDS]
    return ' '.join(words)


def parse_ingredients(raw: str) -> list:
    """Split by comma, strip whitespace, lowercase — return list."""
    if not isinstance(raw, str) or not raw:
        return []
    return [ing.strip().lower() for ing in raw.split(',') if ing.strip()]


def compute_safety_score(ingredient_list: list) -> int:
    """Score from 0-100. Base=60. -8 per irritant found. +5 per active found. Clamped."""
    if not ingredient_list:
        return 60
    ingredients_lower = [ing.lower() for ing in ingredient_list]
    score = 60
    for irritant in IRRITANTS:
        if any(irritant in ing for ing in ingredients_lower):
            score -= 8
    for active in ACTIVES:
        if any(active in ing for ing in ingredients_lower):
            score += 5
    return max(0, min(100, score))


def categorize_score(score: int) -> tuple:
    """Return (label, badge_key) where badge_key is 'safe', 'caution', or 'risk'."""
    if score >= 70:
        return ("Safe", "safe")
    elif score >= 40:
        return ("Caution", "caution")
    else:
        return ("High Risk", "risk")


def get_tfidf_vector(ingredients_text: str, vectorizer):
    """Clean and transform a single ingredient string using fitted vectorizer."""
    cleaned = clean_text(ingredients_text)
    return vectorizer.transform([cleaned])


def get_full_tfidf_matrix(df: pd.DataFrame, vectorizer):
    """Transform entire df['Ingredients'] column. Return sparse matrix."""
    ingredients_cleaned = df["Ingredients"].fillna("").apply(clean_text)
    return vectorizer.transform(ingredients_cleaned)


def get_top_similar(query_vector, full_matrix, df: pd.DataFrame,
                    exclude_name: str = None, top_n: int = 5) -> pd.DataFrame:
    """Compute cosine similarity, exclude self, return top_n rows from df."""
    similarities = cosine_similarity(query_vector, full_matrix)[0]
    top_indices = np.argsort(similarities)[::-1]
    
    results = []
    for idx in top_indices:
        if exclude_name and df.iloc[idx]["Name"].lower() == exclude_name.lower():
            continue
        if len(results) < top_n:
            row = df.iloc[idx].copy()
            row["similarity_score"] = similarities[idx]
            results.append(row)
    
    return pd.DataFrame(results)


def find_dupes(query_vector, full_matrix, df: pd.DataFrame,
               exclude_name: str, budget: float,
               threshold: float = 0.85) -> pd.DataFrame:
    """Return products with similarity >= threshold and Price <= budget."""
    similarities = cosine_similarity(query_vector, full_matrix)[0]
    
    dupes = []
    for idx, sim in enumerate(similarities):
        if (sim >= threshold and 
            df.iloc[idx]["Price"] <= budget and
            df.iloc[idx]["Name"].lower() != exclude_name.lower()):
            row = df.iloc[idx].copy()
            row["similarity_score"] = sim
            dupes.append(row)
    
    return pd.DataFrame(dupes).sort_values("similarity_score", ascending=False)


def get_pca_coords(full_matrix) -> tuple:
    """Apply PCA(n_components=2), return (x_coords, y_coords)."""
    matrix_dense = full_matrix.toarray() if hasattr(full_matrix, 'toarray') else full_matrix
    pca = PCA(n_components=2)
    coords = pca.fit_transform(matrix_dense)
    return coords[:, 0], coords[:, 1]


def get_top_ingredients(df: pd.DataFrame, top_n: int = 20) -> tuple:
    """Flatten all ingredients, count occurrences, return (names, counts) for top_n."""
    all_ings = []
    for ing_str in df["Ingredients"].fillna(""):
        if ing_str:
            ings = parse_ingredients(ing_str)
            all_ings.extend(ings)
    
    counts = Counter(all_ings)
    top = counts.most_common(top_n)
    if not top:
        return ([], [])
    names, freqs = zip(*top)
    return list(names), list(freqs)


def format_price(price: float) -> str:
    """Return price formatted as '$12.50'."""
    return f"${price:.2f}"


def skin_type_to_column(skin_type: str) -> str:
    """Map display skin type string to dataframe column name."""
    mapping = {
        "oily": "Oily",
        "dry": "Dry",
        "combination": "Combination",
        "normal": "Normal",
        "sensitive": "Sensitive"
    }
    return mapping.get(skin_type.lower(), "Normal")
