"""GlowGuide Professional Edition — Main Entry Point with Cloud Navbar & Hero Section."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from utils.styles import MASTER_CSS
from utils.loaders import (
    load_dataframe, load_classifier, load_vectorizer,
    load_regressor, load_kmeans, validate_all_assets
)
from components.product_cards import render_classification_card
from components.recommendation_ui import render_recommendations, render_dupe_finder
from components.comparison_ui import render_comparison
from components.charts import render_all_charts


st.set_page_config(
    page_title="GlowGuide — Skincare Intelligence Dashboard",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

st.markdown(f"<style>{MASTER_CSS}</style>", unsafe_allow_html=True)

# ========== CLOUD NAVBAR WITH DARK MODE TOGGLE ==========
navbar_html = f"""
<div class="navbar-container">
    <div class="navbar-content">
        <div class="navbar-brand" onclick="window.location.reload()">GlowGuide</div>
        <div class="navbar-nav">
            <div class="nav-item {'active' if st.session_state.active_page == 'Dashboard' else ''}" 
                 onclick="document.querySelector('[data-testid=\\'stSessionStateRunOnce\\']')?.parentElement?.click()">Dashboard</div>
            <div class="nav-item {'active' if st.session_state.active_page == 'Recommendations' else ''}" 
                 onclick="document.querySelector('[data-testid=\\'stSessionStateRunOnce\\']')?.parentElement?.click()">Recommendations</div>
            <div class="nav-item {'active' if st.session_state.active_page == 'Market Lab' else ''}" 
                 onclick="document.querySelector('[data-testid=\\'stSessionStateRunOnce\\']')?.parentElement?.click()">Market Lab</div>
            <div class="nav-item {'active' if st.session_state.active_page == 'VS Mode' else ''}" 
                 onclick="document.querySelector('[data-testid=\\'stSessionStateRunOnce\\']')?.parentElement?.click()">VS Mode</div>
        </div>
        <div class="nav-controls">
            <button class="theme-toggle" title="Toggle dark mode">🌙</button>
        </div>
    </div>
</div>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

# ========== NAVIGATION BUTTONS ==========
nav_cols = st.columns(4, gap="small")
pages = ["Dashboard", "Recommendations", "Market Lab", "VS Mode"]
page_icons = ["🏠", "💎", "📊", "⚔️"]

for i, (page, icon) in enumerate(zip(pages, page_icons)):
    with nav_cols[i]:
        if st.button(
            f"{icon} {page}",
            key=f"nav_btn_{page}",
            use_container_width=True,
            type="primary" if st.session_state.active_page == page else "secondary"
        ):
            st.session_state.active_page = page
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ========== HERO SECTION ==========
hero_section = """
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">GlowGuide</h1>
        <p class="hero-subtitle">✦ Ingredient-First Skincare Intelligence Dashboard ✦</p>
        <p style="font-size: 16px; color: #64748B; margin-bottom: 32px; font-weight: 500;">
            Analyze ingredients · Get safety scores · Find dupes · Explore market trends
        </p>
    </div>
</div>
"""
st.markdown(hero_section, unsafe_allow_html=True)

if not validate_all_assets():
    st.error("⚠️ Could not load required model files. Ensure all .pkl files are in models/ and cleaned.csv is in data/")
    st.stop()

df = load_dataframe()
classifier = load_classifier()
vectorizer = load_vectorizer()
regressor = load_regressor()
kmeans = load_kmeans()

# ========== DASHBOARD PAGE ==========
if st.session_state.active_page == "Dashboard":
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">Product Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g. CeraVe Moisturizing Cream",
            key="dashboard_product_name"
        )
    with filter_col2:
        skin_type = st.selectbox(
            "Skin Type",
            ["Oily", "Dry", "Combination", "Normal", "Sensitive"],
            key="dashboard_skin_type"
        )
    
    analyze_btn = st.button("🔍 Analyze Product", type="primary", use_container_width=True)
    
    st.divider()
    
    if analyze_btn:
        if not product_name.strip():
            st.warning("Please enter a product name to analyze.")
        else:
            with st.spinner("🔍 Analyzing product..."):
                render_classification_card(
                    product_name,
                    skin_type,
                    df, classifier, vectorizer
                )
    else:
        st.markdown(
            '<div style="text-align:center;padding:80px 40px;color:#94A3B8;background:linear-gradient(135deg, rgba(99, 102, 241, 0.03) 0%, rgba(139, 92, 246, 0.03) 100%);border-radius:20px;margin-top:40px;">'
            '<p style="font-size:48px;margin-bottom:16px;">✦</p>'
            '<p style="font-size:20px;font-weight:600;color:#64748B;margin-bottom:8px;">Ready to Analyze</p>'
            '<p style="font-size:15px;color:#94A3B8;margin:0;">Enter a product name above to begin analysis</p>'
            '</div>',
            unsafe_allow_html=True
        )

# ========== RECOMMENDATIONS PAGE ==========
elif st.session_state.active_page == "Recommendations":
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">Product Recommendations</h2>
    </div>
    """, unsafe_allow_html=True)
    
    filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 0.5])
    with filter_col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g. CeraVe Moisturizing Cream",
            key="rec_product_name"
        )
    with filter_col2:
        skin_type = st.selectbox(
            "Skin Type",
            ["Oily", "Dry", "Combination", "Normal", "Sensitive"],
            key="rec_skin_type"
        )
    with filter_col3:
        budget = st.number_input("Max Budget", min_value=1, max_value=200, value=50, key="rec_budget")
    
    search_btn = st.button("💎 Find Recommendations", type="primary", use_container_width=True)
    st.divider()
    
    inputs = {
        "skin_type": skin_type,
        "product_name": product_name,
        "budget": budget,
        "search_clicked": search_btn
    }
    
    col1, col2 = st.columns([1.3, 0.7], gap="large")
    with col1:
        st.markdown('<h3 style="font-size:24px;font-weight:700;">🎯 Similar Products</h3>', unsafe_allow_html=True)
        render_recommendations(inputs, df, vectorizer)
    with col2:
        st.markdown('<h3 style="font-size:24px;font-weight:700;">💰 Budget Dupes</h3>', unsafe_allow_html=True)
        render_dupe_finder(inputs, df, vectorizer)

# ========== MARKET LAB PAGE ==========
elif st.session_state.active_page == "Market Lab":
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">Market Intelligence</h2>
    </div>
    """, unsafe_allow_html=True)
    
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        selected_labels = st.multiselect(
            "Product Categories",
            ["Moisturizer", "Serum", "Cleanser", "Eye cream", "Sun protect"],
            default=["Moisturizer", "Serum", "Cleanser", "Eye cream", "Sun protect"],
            key="market_labels"
        )
    with filter_col2:
        price_range = st.slider("Price Range (USD)", 0, 300, (0, 150), key="market_price")
    
    st.divider()
    
    render_all_charts(df, selected_labels, price_range)

# ========== VS MODE PAGE ==========
elif st.session_state.active_page == "VS Mode":
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 24px;">Head-to-Head Comparison</h2>
    </div>
    """, unsafe_allow_html=True)
    
    filter_col1, filter_col2 = st.columns([1, 1])
    with filter_col1:
        product_a = st.text_input(
            "Product A",
            placeholder="e.g. CeraVe SA Cleanser",
            key="vs_product_a"
        )
    with filter_col2:
        product_b = st.text_input(
            "Product B",
            placeholder="e.g. Neutrogena Oil-Free",
            key="vs_product_b"
        )
    
    compare_btn = st.button("⚔️ Compare Products", type="primary", use_container_width=True)
    st.divider()
    
    inputs = {
        "product_a": product_a,
        "product_b": product_b,
        "compare_clicked": compare_btn
    }
    
    if inputs.get("compare_clicked"):
        render_comparison(inputs, df, vectorizer)
    else:
        st.markdown(
            '<div style="text-align:center;padding:80px 40px;color:#94A3B8;background:linear-gradient(135deg, rgba(99, 102, 241, 0.03) 0%, rgba(139, 92, 246, 0.03) 100%);border-radius:20px;margin-top:40px;">'
            '<p style="font-size:48px;margin-bottom:16px;">⚔️</p>'
            '<p style="font-size:20px;font-weight:600;color:#64748B;margin-bottom:8px;">Select Two Products</p>'
            '<p style="font-size:15px;color:#94A3B8;margin:0;">Enter two product names above to compare</p>'
            '</div>',
            unsafe_allow_html=True
        )

st.markdown("<br><br>", unsafe_allow_html=True)
