"""Head-to-head product comparison component."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from utils.engine import (
    parse_ingredients, compute_safety_score, format_price,
    get_full_tfidf_matrix, get_tfidf_vector
)
from sklearn.metrics.pairwise import cosine_similarity
from components.product_cards import render_ingredient_chips


def render_comparison(inputs: dict, df, vectorizer) -> None:
    """Head-to-head product comparison."""
    product_a = inputs.get("product_a", "").strip()
    product_b = inputs.get("product_b", "").strip()
    compare_clicked = inputs.get("compare_clicked", False)
    
    if not compare_clicked or not product_a or not product_b:
        st.markdown(
            '<div style="text-align:center;padding:60px 20px;color:#94A3B8;">'
            '<p style="font-size:28px;">⚖️</p>'
            '<p style="font-size:16px;font-weight:500;">Enter two product names to compare</p>'
            '</div>',
            unsafe_allow_html=True
        )
        return
    
    product_a_lower = product_a.lower()
    product_b_lower = product_b.lower()
    
    matching_a = df[df["Name"].str.lower().str.contains(product_a_lower, na=False)]
    matching_b = df[df["Name"].str.lower().str.contains(product_b_lower, na=False)]
    
    if matching_a.empty or matching_b.empty:
        missing = []
        if matching_a.empty:
            missing.append(f"'{product_a}'")
        if matching_b.empty:
            missing.append(f"'{product_b}'")
        st.error(f"Product(s) not found: {', '.join(missing)}")
        return
    
    prod_a = matching_a.iloc[0]
    prod_b = matching_b.iloc[0]
    
    try:
        full_matrix = get_full_tfidf_matrix(df, vectorizer)
        vec_a = get_tfidf_vector(prod_a["Ingredients"], vectorizer)
        vec_b = get_tfidf_vector(prod_b["Ingredients"], vectorizer)
        
        similarity = cosine_similarity(vec_a, vec_b)[0][0]
        
        ings_a = set(parse_ingredients(prod_a["Ingredients"]))
        ings_b = set(parse_ingredients(prod_b["Ingredients"]))
        
        shared = ings_a & ings_b
        only_a = ings_a - ings_b
        only_b = ings_b - ings_a
        
        col1, col2, col3 = st.columns([1, 0.25, 1])
        
        safety_a = compute_safety_score(list(ings_a))
        safety_b = compute_safety_score(list(ings_b))
        
        with col1:
            st.markdown(f"### {prod_a['Name']}")
            st.caption(f"{prod_a['Brand']}")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Price", format_price(prod_a["Price"]))
            with c2:
                st.metric("Rating", f"{prod_a['Rank']:.1f}")
            st.markdown("**Safety Score**")
            st.progress(safety_a / 100, text=f"{safety_a}/100")
        
        with col2:
            sim_pct = int(similarity * 100)
            color = "#10B981" if sim_pct >= 75 else "#F59E0B" if sim_pct >= 50 else "#EF4444"
            st.markdown(
                f'<div style="text-align:center;padding:20px 0;">'
                f'<p style="font-size:32px;font-weight:700;color:{color};">{sim_pct}%</p>'
                f'<p style="font-size:12px;color:#64748B;text-transform:uppercase;letter-spacing:0.04em;">match</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(f"### {prod_b['Name']}")
            st.caption(f"{prod_b['Brand']}")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Price", format_price(prod_b["Price"]))
            with c2:
                st.metric("Rating", f"{prod_b['Rank']:.1f}")
            st.markdown("**Safety Score**")
            st.progress(safety_b / 100, text=f"{safety_b}/100")
        
        st.divider()
        
        st.markdown("**Shared Ingredients**")
        if shared:
            render_ingredient_chips(list(shared))
        else:
            st.caption("No shared ingredients.")
        
        st.markdown("**Unique to A**")
        if only_a:
            render_ingredient_chips(list(only_a))
        else:
            st.caption("None")
        
        st.markdown("**Unique to B**")
        if only_b:
            render_ingredient_chips(list(only_b))
        else:
            st.caption("None")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
