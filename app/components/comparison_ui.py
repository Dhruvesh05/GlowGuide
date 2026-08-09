"""Head-to-head product comparison component."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.engine import (
    parse_ingredients, compute_safety_score, format_price, get_tfidf_vector
)
from components.product_cards import render_ingredient_chips


def _find_best_product_match(df: pd.DataFrame, search_term: str):
    """
    Finds the most accurate matching product from the DataFrame using a tiered approach:
    1. Exact Match
    2. Starts-with Match
    3. Contains Substring Match
    """
    term_clean = search_term.lower().strip()
    names_lower = df["Name"].str.lower().str.strip()

    # Tier 1: Exact match
    exact = df[names_lower == term_clean]
    if not exact.empty:
        return exact.iloc[0]

    # Tier 2: Name starts with search term
    starts_with = df[names_lower.str.startswith(term_clean, na=False)]
    if not starts_with.empty:
        return starts_with.iloc[0]

    # Tier 3: Substring match
    contains = df[names_lower.str.contains(term_clean, regex=False, na=False)]
    if not contains.empty:
        return contains.iloc[0]

    return None


def _normalize_ingredients(raw_ingredients: str) -> dict:
    """
    Parses and normalizes ingredient lists to ensure accurate set comparisons.
    Returns a dict mapping normalized lowercase keys to formatted display strings.
    """
    parsed = parse_ingredients(raw_ingredients)
    normalized = {}
    for ing in parsed:
        cleaned = ing.strip()
        key = cleaned.lower()
        if key and key not in normalized:
            normalized[key] = cleaned.title()
    return normalized


def render_comparison(inputs: dict, df: pd.DataFrame, vectorizer) -> None:
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

    # Find closest matching products
    prod_a = _find_best_product_match(df, product_a)
    prod_b = _find_best_product_match(df, product_b)

    missing = []
    if prod_a is None:
        missing.append(f"'{product_a}'")
    if prod_b is None:
        missing.append(f"'{product_b}'")

    if missing:
        st.error(f"Product(s) not found: {', '.join(missing)}")
        return

    # Check for identical product selection
    if prod_a.name == prod_b.name:
        st.info("ℹ️ Both search terms resolved to the same product.")

    try:
        # Calculate Cosine Similarity via TF-IDF Vectors
        vec_a = get_tfidf_vector(prod_a.get("Ingredients", ""), vectorizer)
        vec_b = get_tfidf_vector(prod_b.get("Ingredients", ""), vectorizer)
        similarity = float(cosine_similarity(vec_a, vec_b)[0][0])

        # Normalize ingredient sets for precise intersection and difference operations
        dict_a = _normalize_ingredients(prod_a.get("Ingredients", ""))
        dict_b = _normalize_ingredients(prod_b.get("Ingredients", ""))

        keys_a, keys_b = set(dict_a.keys()), set(dict_b.keys())

        shared_keys = keys_a & keys_b
        only_a_keys = keys_a - keys_b
        only_b_keys = keys_b - keys_a

        shared = [dict_a[k] for k in sorted(shared_keys)]
        only_a = [dict_a[k] for k in sorted(only_a_keys)]
        only_b = [dict_b[k] for k in sorted(only_b_keys)]

        # Calculate Safety Scores
        safety_a = compute_safety_score(list(dict_a.values()))
        safety_b = compute_safety_score(list(dict_b.values()))

        # Layout Rendering
        col1, col2, col3 = st.columns([1, 0.25, 1])

        # Product A Details
        with col1:
            st.markdown(f"### {prod_a['Name']}")
            st.caption(f"{prod_a.get('Brand', 'Unknown Brand')}")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Price", format_price(prod_a.get("Price", 0)))
            with c2:
                rank_val = prod_a.get("Rank", np.nan)
                rank_str = f"{rank_val:.1f}" if pd.notna(rank_val) else "N/A"
                st.metric("Rating", rank_str)
            st.markdown("**Safety Score**")
            st.progress(min(max(safety_a, 0), 100) / 100, text=f"{safety_a}/100")

        # Similarity Score Metric
        with col2:
            sim_pct = int(round(similarity * 100))
            color = "#10B981" if sim_pct >= 75 else "#F59E0B" if sim_pct >= 50 else "#EF4444"
            st.markdown(
                f'<div style="text-align:center;padding:20px 0;">'
                f'<p style="font-size:32px;font-weight:700;color:{color};">{sim_pct}%</p>'
                f'<p style="font-size:12px;color:#64748B;text-transform:uppercase;letter-spacing:0.04em;">match</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Product B Details
        with col3:
            st.markdown(f"### {prod_b['Name']}")
            st.caption(f"{prod_b.get('Brand', 'Unknown Brand')}")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Price", format_price(prod_b.get("Price", 0)))
            with c2:
                rank_val = prod_b.get("Rank", np.nan)
                rank_str = f"{rank_val:.1f}" if pd.notna(rank_val) else "N/A"
                st.metric("Rating", rank_str)
            st.markdown("**Safety Score**")
            st.progress(min(max(safety_b, 0), 100) / 100, text=f"{safety_b}/100")

        st.divider()

        # Detailed Ingredient Breakdown
        st.markdown("**Shared Ingredients**")
        if shared:
            render_ingredient_chips(shared)
        else:
            st.caption("No shared ingredients found.")

        st.markdown(f"**Unique to {prod_a['Name']}**")
        if only_a:
            render_ingredient_chips(only_a)
        else:
            st.caption("None")

        st.markdown(f"**Unique to {prod_b['Name']}**")
        if only_b:
            render_ingredient_chips(only_b)
        else:
            st.caption("None")

    except Exception as e:
        st.error(f"Error executing comparison: {str(e)}")
