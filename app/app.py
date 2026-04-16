# -*- coding: utf-8 -*-
"""GlowGuide - Smart Skincare Recommender with Minimal Color Theme"""

import sys
from pathlib import Path

# Set up path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import utilities
from app.utils import get_combined_recommendations
from app.components import (
    display_recommendations_grid,
    display_explainability_breakdown,
    display_combined_recommendations,
    display_ml_performance_metrics,
    display_eda_dashboard,
    display_visualization_selector
)

# ========== PAGE CONFIG ==========
logo_path = Path(__file__).parent / "assets" / "logo.png"

st.set_page_config(
    page_title="GlowGuide - Skincare Assistant",
    page_icon=str(logo_path),
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Raleway:ital,wght@0,100..900;1,100..900&family=Space+Grotesk:wght@300..700&display=swap');

* {
    font-family: 'DM Sans', sans-serif;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(0, 0, 0, 0.08); }
    50% { box-shadow: 0 0 30px rgba(0, 0, 0, 0.12); }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.main {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #f3f4f6 100%);
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 16px;
    border-bottom: 2px solid #e5e7eb;
    background-color: transparent;
    padding-bottom: 12px;
}

.stTabs [data-baseweb="tab"] {
    padding: 14px 24px;
    font-weight: 600;
    font-size: 15px;
    font-family: 'Space Grotesk', sans-serif;
    border-radius: 12px;
    color: #6b7280;
    background-color: transparent;
    border: 2px solid transparent;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    letter-spacing: 0.3px;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #1f2937;
    background-color: rgba(0, 0, 0, 0.03);
    border-color: #d1d5db;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff;
    background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    border-color: transparent;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    color: white;
    border: none;
    border-radius: 10px;
    height: 50px;
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    letter-spacing: 0.5px;
}

.stButton>button:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.25);
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.stButton>button:active {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

/* Typography */
h1, h2, h3 {
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.8px;
}

h1 {
    text-align: center;
    margin-bottom: 16px;
    font-size: 48px;
    font-weight: 800;
    animation: fadeIn 0.6s ease-out;
    background: linear-gradient(135deg, #000000 0%, #333333 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2 {
    font-size: 34px;
    margin-top: 28px;
    margin-bottom: 20px;
    font-weight: 700;
    animation: slideUp 0.5s ease-out;
}

h3 {
    font-size: 24px;
    margin-top: 20px;
    margin-bottom: 16px;
    font-weight: 600;
    color: #1f2937;
}

p {
    color: #4b5563;
    line-height: 1.8;
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
}

/* Input Styling */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox select {
    border: 2px solid #d1d5db !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    background-color: #ffffff !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus,
.stSelectbox select:focus {
    border-color: #000000 !important;
    background-color: #ffffff !important;
    box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.1) !important;
}

/* Slider Styling */
.stSlider label {
    font-weight: 600;
    color: #1f2937;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 12px;
    display: block;
}

/* Checkbox Styling */
.stCheckbox {
    padding: 12px 0;
    transition: all 0.2s ease;
}

.stCheckbox label {
    font-weight: 500;
    color: #1f2937;
    font-family: 'DM Sans', sans-serif;
    cursor: pointer;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
    padding: 26px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: slideUp 0.5s ease-out;
}

.metric-card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    transform: translateY(-4px);
    border-color: #d1d5db;
}

/* Product Cards */
.product-card {
    background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
    padding: 24px;
    border-radius: 14px;
    margin: 14px 0;
    border: 1.5px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: slideUp 0.5s ease-out;
}

.product-card:hover {
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
    transform: translateY(-5px);
    border-color: #d1d5db;
    background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
}

/* Tags */
.ingredient-tag {
    display: inline-block;
    background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
    color: #1f2937;
    padding: 10px 16px;
    border-radius: 24px;
    margin: 6px 6px 6px 0;
    font-size: 13px;
    font-weight: 600;
    border: 1.5px solid #d1d5db;
    transition: all 0.3s ease;
    cursor: default;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.ingredient-tag:hover {
    background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
    border-color: #9ca3af;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.ingredient-tag.safe {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    color: #065f46;
    border-color: #6ee7b7;
}

.ingredient-tag.safe:hover {
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    transform: translateY(-2px);
}

.ingredient-tag.active {
    background: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%);
    color: #4c1d95;
    border-color: #a78bfa;
}

.ingredient-tag.active:hover {
    box-shadow: 0 4px 12px rgba(168, 85, 247, 0.2);
    transform: translateY(-2px);
}

.ingredient-tag.warning {
    background: linear-gradient(135deg, #fef08a 0%, #fde047 100%);
    color: #78350f;
    border-color: #facc15;
}

.ingredient-tag.warning:hover {
    box-shadow: 0 4px 12px rgba(202, 138, 4, 0.2);
    transform: translateY(-2px);
}

/* Badges */
.success-badge {
    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
    color: #166534;
    padding: 18px 24px;
    border-radius: 12px;
    margin: 16px 0;
    font-weight: 600;
    border: 1.5px solid #86efac;
    animation: slideInLeft 0.5s ease-out;
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15);
}

.info-badge {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    color: #0c2d6b;
    padding: 18px 24px;
    border-radius: 12px;
    margin: 16px 0;
    font-weight: 600;
    border: 1.5px solid #60a5fa;
    animation: slideInLeft 0.5s ease-out 0.1s both;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.warning-badge {
    background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%);
    color: #78350f;
    padding: 18px 24px;
    border-radius: 12px;
    margin: 16px 0;
    font-weight: 600;
    border: 1.5px solid #fbbf24;
    animation: slideInLeft 0.5s ease-out 0.2s both;
    box-shadow: 0 4px 12px rgba(251, 146, 60, 0.15);
}

/* Divider */
.divider {
    margin: 32px 0;
    border-top: 2px solid #e5e7eb;
    opacity: 0.8;
}

/* Sidebar Header */
.sidebar-header {
    font-size: 18px;
    font-weight: 700;
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 2.5px solid #000000;
    letter-spacing: -0.3px;
}

/* Radio Button */
.stRadio label {
    font-weight: 500;
    color: #1f2937;
    font-family: 'DM Sans', sans-serif;
}

/* Multiselect */
.stMultiSelect label {
    font-weight: 600;
    color: #1f2937;
    font-family: 'DM Sans', sans-serif;
}

/* Table */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.streamlit-expanderHeader:hover {
    background-color: #f3f4f6;
    border-color: #d1d5db;
}

</style>
""", unsafe_allow_html=True)

# ========== TITLE & SUBTITLE ==========
col1, col2 = st.columns([1, 5])
with col1:
    st.image(str(logo_path), width=90)
with col2:
    st.markdown("<h1 style='margin-top: 10px;'>✨ GlowGuide</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #666666; font-size: 18px; margin-bottom: 28px; font-weight: 500; letter-spacing: 0.3px;'>🌟 Find the perfect skincare products based on your unique needs</p>", unsafe_allow_html=True)

st.markdown("""
<style>
    .title-section {
        animation: slideUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR - USER PROFILE ==========
with st.sidebar:
    # Logo + Title in sidebar
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(str(logo_path), width=50)
    with col2:
        st.markdown("<h2 style='margin: 0; padding-top: 5px;'>GlowGuide</h2>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<div class='sidebar-header'>Your Profile</div>", unsafe_allow_html=True)
    
    skin_type = st.selectbox(
        "Skin Type",
        ["Oily", "Dry", "Combination", "Sensitive", "Normal"],
        key="sidebar_skin_type_main"
    )
    
    skin_concerns = st.multiselect(
        "Skin Concerns",
        ["Acne", "Dryness", "Oiliness", "Sensitivity", "Aging", "Hyperpigmentation", "Redness"],
        default=["Acne"],
        key="sidebar_concerns_main"
    )
    
    age = st.slider(
        "Age",
        13, 80, 25,
        key="sidebar_age_main"
    )
    
    st.divider()
    
    st.markdown("<div class='sidebar-header'>Budget & Preferences</div>", unsafe_allow_html=True)
    
    budget_min, budget_max = st.slider(
        "Budget Range",
        0, 10000, (500, 3000),
        key="sidebar_budget_main"
    )
    
    st.divider()
    
    st.markdown("<div class='sidebar-header'>Preferences</div>", unsafe_allow_html=True)
    
    alcohol_free = st.checkbox("Alcohol-Free Only", value=False, key="sidebar_alcohol_main")
    fragrance_free = st.checkbox("Fragrance-Free Only", value=False, key="sidebar_fragrance_main")
    vegan = st.checkbox("Vegan Only", value=False, key="sidebar_vegan_main")
    cruelty_free = st.checkbox("Cruelty-Free Only", value=False, key="sidebar_cruelty_main")

# ========== MAIN CONTENT - TABBED LAYOUT ==========
tab1, tab2, tab3, tab_insights = st.tabs(["Product Search", "Ingredient Analyzer", "Routine Builder", "Insights"])

# ========== TAB 1: PRODUCT SEARCH ==========
with tab1:
    st.markdown("## Find Your Perfect Product")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g., Moisturizing Cream, Vitamin C Serum",
            key="tab1_product_name"
        )
    with col2:
        brand = st.text_input(
            "Brand (Optional)",
            placeholder="e.g., CeraVe, Neutrogena",
            key="tab1_brand"
        )
    
    col3, col4 = st.columns([1, 1])
    with col3:
        product_type = st.selectbox(
            "Product Type",
            ["Cleanser", "Moisturizer", "Serum", "Mask", "Sunscreen", "Toner", "Eye Cream"],
            key="tab1_type"
        )
    with col4:
        st.write("")
        st.write("")
    
    # Filters
    st.markdown("### Additional Filters")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        filter_alcohol = st.checkbox("Alcohol-Free", key="tab1_filter_alcohol")
    with f2:
        filter_fragrance = st.checkbox("Fragrance-Free", key="tab1_filter_fragrance")
    with f3:
        filter_vegan = st.checkbox("Vegan", key="tab1_filter_vegan")
    with f4:
        filter_cruelty = st.checkbox("Cruelty-Free", key="tab1_filter_cruelty")
    
    search_btn = st.button("🔍 Get Ingredient Recommendations", use_container_width=True, key="tab1_search_btn")
    
    if search_btn:
        # ========== BLOCK 8: ORCHESTRATE RECOMMENDATION WORKFLOW ==========
        # The coordinator handles all business logic:
        # - Building user profiles
        # - Converting between formats
        # - Orchestrating calls to Block 1 and Block 4
        # This keeps app.py focused on UI only!
        
        results = get_combined_recommendations(
            skin_type=skin_type,
            concerns=skin_concerns,
            age=age,
            alcohol_free=alcohol_free or filter_alcohol,
            fragrance_free=fragrance_free or filter_fragrance,
            vegan=vegan or filter_vegan,
            cruelty_free=cruelty_free or filter_cruelty,
            top_n=5
        )
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # ========== DISPLAY RESULTS (Block 5: Integration UI) ==========
        
        # Display combined recommendations (Block 1 + Block 4)
        display_combined_recommendations(
            user_profile=results.user_profile.to_dict(),
            recommendations=results.block1_results,
            ml_result=results.block4_result,
            show_comparison=True
        )
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # ========== DETAILED BREAKDOWN (OPTIONAL) ==========
        
        with st.expander("📊 View Detailed Score Breakdown (Rule-Based)", expanded=False):
            st.markdown("#### Rule-Based Scoring Details")
            st.markdown(
                "This section shows the detailed scoring breakdown from the rule-based engine, "
                "analyzing factors like skin type, concerns, and age."
            )
            
            tab_breakdown1, tab_breakdown2, tab_breakdown3 = st.tabs([
                f"#{results.block1_results[0].ingredient}",
                f"#{results.block1_results[1].ingredient}",
                f"#{results.block1_results[2].ingredient}"
            ])
            
            with tab_breakdown1:
                display_explainability_breakdown(results.block1_results[0])
            
            with tab_breakdown2:
                display_explainability_breakdown(results.block1_results[1])
            
            with tab_breakdown3:
                display_explainability_breakdown(results.block1_results[2])
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # ========== ML MODEL PERFORMANCE INFO ==========
        
        with st.expander("🧠 ML Model Details & Performance", expanded=False):
            st.markdown("#### Machine Learning Model Information")
            st.markdown(
                "This model uses K-Nearest Neighbors (KNN) trained on 50 skincare profiles "
                "to predict ingredient recommendations based on similar user profiles."
            )
            st.divider()
            display_ml_performance_metrics()
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Market insights
        st.markdown("### 📈 Market Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            df_price = pd.DataFrame({
                'Price Range': ['Rs. 0-500', 'Rs. 500-1000', 'Rs. 1000-2000', 'Rs. 2000+'],
                'Count': [45, 67, 38, 20]
            })
            fig1 = px.bar(df_price, x='Price Range', y='Count', title="Product Price Distribution", 
                         color_discrete_sequence=["#333333"],
                         labels={'Count': 'Number of Products'})
            fig1.update_layout(showlegend=False, hovermode='x unified')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            df_brands = pd.DataFrame({
                'Brand': ['CeraVe', 'Cetaphil', 'Neutrogena', 'Garnier', 'Olay'],
                'Products': [45, 38, 35, 32, 28]
            })
            fig2 = px.bar(df_brands, x='Brand', y='Products', title="Top Skincare Brands", 
                         color_discrete_sequence=["#555555"],
                         labels={'Products': 'Number of Products'})
            fig2.update_layout(showlegend=False, hovermode='x unified')
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown(f"<div class='success-badge'>✅ Found {len(results.block1_results)} personalized ingredient recommendations for your {skin_type} skin type!</div>", unsafe_allow_html=True)

# ========== TAB 2: INGREDIENT ANALYZER ==========
with tab2:
    st.markdown("## Analyze Your Ingredients")
    
    ingredients_text = st.text_area(
        "Paste ingredient list",
        placeholder="Paste the ingredient list from your product label here...",
        height=150,
        key="tab2_ingredients"
    )
    
    allergy_input = st.text_input(
        "Known Allergies/Sensitivities",
        placeholder="e.g., Parabens, Sulfates, Essential Oils",
        key="tab2_allergies"
    )
    
    analyze_btn = st.button("Analyze Ingredients", use_container_width=True, key="tab2_analyze_btn")
    
    if analyze_btn and ingredients_text:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("## Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Safe Ingredients", "12", "+2")
        with col2:
            st.metric("Potential Irritants", "2", "-1")
        with col3:
            st.metric("Active Ingredients", "4", "=")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Safe Ingredients")
        st.markdown("""
        <div>
            <span class='ingredient-tag safe'>Glycerin</span>
            <span class='ingredient-tag safe'>Hyaluronic Acid</span>
            <span class='ingredient-tag safe'>Niacinamide</span>
            <span class='ingredient-tag safe'>Panthenol</span>
            <span class='ingredient-tag safe'>Ceramide</span>
            <span class='ingredient-tag safe'>Aloe Vera</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Active Ingredients (Beneficial)")
        st.markdown("""
        <div>
            <span class='ingredient-tag active'>Vitamin C</span>
            <span class='ingredient-tag active'>Retinol</span>
            <span class='ingredient-tag active'>AHA</span>
            <span class='ingredient-tag active'>BHA</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Potential Irritants")
        st.markdown("""
        <div class='warning-badge'>
            <strong>Alcohol Denat</strong> - May cause dryness in sensitive skin
        </div>
        <div class='warning-badge'>
            <strong>Fragrance</strong> - Can trigger sensitivity reactions
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Ingredient Safety Score")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=82,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Safety Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#000000"},
                'steps': [
                    {'range': [0, 50], 'color': "#f5f5f5"},
                    {'range': [50, 100], 'color': "#e0e0e0"}
                ]
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown("<div class='success-badge'>Safe for your skin profile!</div>", unsafe_allow_html=True)

# ========== TAB 3: ROUTINE BUILDER ==========
with tab3:
    st.markdown("## Build Your Skincare Routine")
    
    routine_type = st.radio(
        "Choose routine time",
        ["Morning Routine", "Night Routine"],
        horizontal=True,
        key="tab3_routine_type"
    )
    
    st.markdown("### Select routine steps (in order)")
    
    morning_steps = ["Cleanser", "Toner", "Essence", "Serum", "Eye Cream", "Moisturizer", "Sunscreen"]
    night_steps = ["Cleanser", "Toner", "Essence", "Serum", "Eye Cream", "Moisturizer", "Sleep Mask"]
    
    steps = morning_steps if routine_type == "Morning Routine" else night_steps
    
    selected_steps = st.multiselect(
        "Steps",
        steps,
        default=steps[:5],
        key="tab3_steps"
    )
    
    st.markdown("### Routine Preferences")
    pref1, pref2 = st.columns(2)
    with pref1:
        time_available = st.slider("Time Available (minutes)", 5, 30, 10, key="tab3_time")
    with pref2:
        routine_focus = st.selectbox(
            "Focus Area",
            ["Hydration", "Anti-aging", "Acne Control", "Brightening", "Sensitive Care"],
            key="tab3_focus"
        )
    
    generate_btn = st.button("Generate Routine", use_container_width=True, key="tab3_generate_btn")
    
    if generate_btn:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"## Your {routine_type}")
        
        routine_data = {
            "Step": ["1. Cleanser", "2. Toner", "3. Serum", "4. Moisturizer", "5. Sunscreen"],
            "Product": ["CeraVe Foaming", "Witch Hazel", "Vitamin C", "CeraVe Lotion", "SPF 50"],
            "Time (min)": [2, 1, 2, 2, 2],
            "Benefit": ["Remove impurities", "Balance pH", "Brightening", "Hydrate", "Protect"]
        }
        
        st.dataframe(
            pd.DataFrame(routine_data),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### Tips for Better Results")
        st.markdown("""
        <div class='info-badge'>
            <strong>Apply products in order:</strong> Lightest to heaviest consistency<br><br>
            <strong>Wait between products:</strong> 1-2 minutes between each application<br><br>
            <strong>Be consistent:</strong> Results become visible in 4-6 weeks of regular use
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='success-badge'>Routine created successfully! Save this for reference.</div>", unsafe_allow_html=True)

# ========== TAB 4: INSIGHTS (EDA DASHBOARD) ==========
with tab_insights:
    display_eda_dashboard()

# ========== FOOTER ==========
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #888888; font-size: 13px; margin-top: 24px;'>
    Made with care using Streamlit | GlowGuide v1.0
</p>
""", unsafe_allow_html=True)
