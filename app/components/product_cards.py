"""Product card components with ingredient analysis."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from utils.engine import (
    parse_ingredients, compute_safety_score, categorize_score,
    IRRITANTS, ACTIVES, clean_text, get_tfidf_vector
)
from utils.styles import SECTION_HEADER, CARD_OPEN, CARD_CLOSE, BADGE_SAFE, BADGE_CAUTION, BADGE_RISK
import math


def render_ingredient_chips(ingredient_list: list) -> None:
    """Render ingredients as colored HTML pill chips."""
    if not ingredient_list:
        st.caption("No ingredients data available.")
        return
    
    html_chips = '<div style="display:flex;flex-wrap:wrap;gap:8px;">'
    
    for ing in ingredient_list:
        ing_lower = ing.lower()
        
        if any(irr in ing_lower for irr in IRRITANTS):
            bg, fg = "#FEF2F2", "#991B1B"
            label = ing
        elif any(act in ing_lower for act in ACTIVES):
            bg, fg = "#EEF2FF", "#3730A3"
            label = ing
        else:
            bg, fg = "#F1F5F9", "#475569"
            label = ing
        
        html_chips += f'<span style="background:{bg};color:{fg};padding:4px 12px;border-radius:999px;font-size:12px;font-weight:500;">{label}</span>'
    
    html_chips += '</div>'
    st.markdown(html_chips, unsafe_allow_html=True)


def render_safety_gauge(score: int) -> None:
    """Render an SVG circular progress gauge for safety score."""
    category, _ = categorize_score(score)
    
    if score >= 70:
        arc_color = "#10B981"
    elif score >= 40:
        arc_color = "#F59E0B"
    else:
        arc_color = "#EF4444"
    
    r = 50
    circumference = 2 * math.pi * r
    dash = (score / 100.0) * circumference
    gap = circumference - dash
    
    svg = f'''
    <div style="display:flex;flex-direction:column;align-items:center;">
        <svg width="120" height="120" viewBox="0 0 120 120" style="transform:rotate(-90deg);">
            <circle cx="60" cy="60" r="{r}" fill="none" stroke="#E2E8F0" stroke-width="8" />
            <circle cx="60" cy="60" r="{r}" fill="none" stroke="{arc_color}" stroke-width="8"
                    stroke-dasharray="{dash},{gap}" stroke-linecap="round" />
            <text x="60" y="70" text-anchor="middle" font-size="24" font-weight="bold" fill="#0F172A">{score}</text>
        </svg>
        <p style="font-size:12px;font-weight:600;color:#64748B;margin-top:8px;text-transform:uppercase;letter-spacing:0.04em;">{category}</p>
    </div>
    '''
    st.markdown(svg, unsafe_allow_html=True)


def render_classification_card(product_name: str, skin_type: str, df, classifier, vectorizer) -> None:
    """Full classification result card."""
    product_name_lower = product_name.lower()
    matching = df[df["Name"].str.lower().str.contains(product_name_lower, na=False)]
    
    if matching.empty:
        st.warning("Product not found in database. Using skin type for analysis.")
        try:
            skin_vec = [[1 if skin_type.lower() == col.lower() else 0 
                        for col in ["Oily", "Dry", "Combination", "Normal", "Sensitive"]]]
            prediction = classifier.predict(skin_vec)[0]
            proba = classifier.predict_proba(skin_vec)[0]
            confidence = max(proba)
            safety_score = 60
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return
    else:
        product = matching.iloc[0]
        ings = product.get("Ingredients", "")
        try:
            cleaned = clean_text(ings)
            vec = get_tfidf_vector(ings, vectorizer)
            prediction = classifier.predict(vec)[0]
            proba = classifier.predict_proba(vec)[0]
            confidence = max(proba)
            ing_list = parse_ingredients(ings)
            safety_score = compute_safety_score(ing_list)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Category", prediction)
    with col2:
        st.metric("Confidence", f"{confidence:.1%}")
    with col3:
        render_safety_gauge(safety_score)
    
    st.divider()
    
    if safety_score >= 70:
        st.markdown(BADGE_SAFE, unsafe_allow_html=True)
    elif safety_score >= 40:
        st.markdown(BADGE_CAUTION, unsafe_allow_html=True)
    else:
        st.markdown(BADGE_RISK, unsafe_allow_html=True)
    
    if not matching.empty:
        st.markdown("**Ingredient Analysis**")
        product = matching.iloc[0]
        ings = product.get("Ingredients", "")
        ing_list = parse_ingredients(ings)
        render_ingredient_chips(ing_list)
