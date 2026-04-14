"""Utility functions for text processing, ingredient analysis, and data formatting."""

import re
import string
from typing import List, Dict
import nltk
from nltk.corpus import stopwords

# Download required NLTK data on first import
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def clean_text(text: str) -> str:
    """
    Clean text by lowercasing, removing punctuation, numbers, and stopwords.
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in text.split() if word not in stop_words]
    
    return ' '.join(words)


def parse_ingredients(raw: str) -> List[str]:
    """
    Parse ingredient string by splitting on commas and cleaning each token.
    """
    if not isinstance(raw, str) or not raw:
        return []
    
    ingredients = [ing.strip().lower() for ing in raw.split(',')]
    return [ing for ing in ingredients if ing]  # Filter empty strings


def compute_safety_score(ingredient_list: List[str]) -> int:
    """
    Calculate a safety score (0-100) based on irritants and active ingredients.
    """
    IRRITANTS = [
        "alcohol denat",
        "fragrance",
        "parfum",
        "sodium lauryl sulfate",
        "sodium laureth sulfate",
        "methylisothiazolinone",
        "formaldehyde"
    ]
    
    ACTIVES = [
        "niacinamide",
        "hyaluronic acid",
        "retinol",
        "salicylic acid",
        "vitamin c",
        "ascorbic acid",
        "ceramide",
        "peptide",
        "glycolic acid",
        "lactic acid",
        "ferulic acid",
        "zinc"
    ]
    
    if not ingredient_list:
        return 60
    
    # Convert to lowercase for matching
    ingredients_lower = [ing.lower() for ing in ingredient_list]
    
    score = 60
    
    # Deduct for irritants
    for irritant in IRRITANTS:
        if any(irritant in ing for ing in ingredients_lower):
            score -= 8
    
    # Add for actives
    for active in ACTIVES:
        if any(active in ing for ing in ingredients_lower):
            score += 5
    
    # Clamp to [0, 100]
    return max(0, min(100, score))


def get_skin_type_columns() -> List[str]:
    """
    Return list of skin type column names in the DataFrame.
    """
    return ["Combination", "Dry", "Normal", "Oily", "Sensitive"]


def format_price(price: float) -> str:
    """
    Format price as a USD currency string.
    """
    return f"${price:.2f}"


def get_skin_type_vector(skin_type: str) -> Dict[str, int]:
    """
    Convert a skin type string to a binary feature vector.
    """
    columns = get_skin_type_columns()
    return {col: (1 if col.lower() == skin_type.lower() else 0) for col in columns}
