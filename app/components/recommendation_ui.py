"""Recommendation and dupe finder display components."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from utils.engine import (
    parse_ingredients, get_full_tfidf_matrix, get_top_similar,
    find_dupes, format_price, clean_text, get_tfidf_vector
)
from utils.styles import SECTION_HEADER, CARD_OPEN, CARD_CLOSE
from components.product_cards import render_ingredient_chips


def render_recommendations(inputs: dict, df, vectorizer) -> None:
    """Top-5 similar products section."""
    product_name = inputs.get("product_name", "").strip()
    skin_type = inputs.get("skin_type", "Normal")
    
    if not product_name:
        st.info("Enter a product name to find recommendations.")
        return
    
    product_name_lower = product_name.lower()
    matching = df[df["Name"].str.lower().str.contains(product_name_lower, na=False)]
    
    st.markdown(SECTION_HEADER.format(label="Similar Products"), unsafe_allow_html=True)
    
    if matching.empty:
        skin_col = skin_type.capitalize() if skin_type.capitalize() in df.columns else "Normal"
        filtered = df[df[skin_col] == 1].nlargest(5, "Rank")
        st.caption("Showing top-rated products for your skin type (product not found)")
        
        for _, row in filtered.iterrows():
            st.markdown(CARD_OPEN, unsafe_allow_html=True)
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"**{row['Name']}**")
                st.caption(f"{row['Brand']}")
            with c2:
                st.metric("Price", format_price(row["Price"]))
            with c3:
                st.metric("Rating", f"⭐ {row['Rank']:.1f}")
            st.markdown(CARD_CLOSE, unsafe_allow_html=True)
    else:
        product = matching.iloc[0]
        ings = product.get("Ingredients", "")
        
        try:
            full_matrix = get_full_tfidf_matrix(df, vectorizer)
            query_vec = get_tfidf_vector(ings, vectorizer)
            recs = get_top_similar(query_vec, full_matrix, df, exclude_name=product_name, top_n=5)
            
            for _, row in recs.iterrows():
                st.markdown(CARD_OPEN, unsafe_allow_html=True)
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.markdown(f"**{row['Name']}**")
                    st.caption(f"{row['Brand']}")
                with c2:
                    st.metric("Price", format_price(row["Price"]))
                with c3:
                    sim_pct = int(row.get("similarity_score", 0) * 100)
                    st.markdown(
                        f'<div style="background:#EEF2FF;color:#3730A3;padding:4px 8px;border-radius:6px;font-size:12px;font-weight:600;">{sim_pct}% match</div>',
                        unsafe_allow_html=True
                    )
                st.markdown(CARD_CLOSE, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")


def render_dupe_finder(inputs: dict, df, vectorizer) -> None:
    """Budget dupe finder section."""
    product_name = inputs.get("product_name", "").strip()
    budget = inputs.get("budget", 50)
    
    if not product_name:
        st.info("Enter a product name to find dupes.")
        return
    
    product_name_lower = product_name.lower()
    matching = df[df["Name"].str.lower().str.contains(product_name_lower, na=False)]
    
    st.markdown(SECTION_HEADER.format(label="Budget Dupe Finder"), unsafe_allow_html=True)
    
    if matching.empty:
        st.info("Enter a valid product name to find dupes.")
        return
    
    product = matching.iloc[0]
    ings = product.get("Ingredients", "")
    
    try:
        full_matrix = get_full_tfidf_matrix(df, vectorizer)
        query_vec = get_tfidf_vector(ings, vectorizer)
        dupes = find_dupes(query_vec, full_matrix, df, exclude_name=product_name, budget=budget)
        
        if dupes.empty:
            st.info(f"No dupes found under {format_price(budget)}. Try increasing your budget.")
        else:
            st.markdown(f"**{len(dupes)} dupe(s) found under {format_price(budget)}**")
            for _, row in dupes.iterrows():
                st.markdown(CARD_OPEN, unsafe_allow_html=True)
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.markdown(f"**{row['Name']}**")
                    st.caption(f"{row['Brand']}")
                with c2:
                    savings = product["Price"] - row["Price"]
                    if savings > 0:
                        st.markdown(f'<p style="color:#10B981;font-weight:600;">Save {format_price(savings)}</p>', unsafe_allow_html=True)
                    st.metric("Price", format_price(row["Price"]))
                with c3:
                    sim_pct = int(row.get("similarity_score", 0) * 100)
                    st.markdown(
                        f'<div style="background:#EEF2FF;color:#3730A3;padding:4px 8px;border-radius:6px;font-size:12px;font-weight:600;">{sim_pct}% match</div>',
                        unsafe_allow_html=True
                    )
                st.markdown(CARD_CLOSE, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {str(e)}")
