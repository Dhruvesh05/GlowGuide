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
from app.utils.products import get_product_link
from app.components import (
    display_recommendations_grid,
    display_explainability_breakdown,
    display_combined_recommendations,
    display_ml_performance_metrics,
    display_eda_dashboard,
    display_visualization_selector
)

# Import ML backend functions
from app.utils.integration import generate_full_recommendation
from app.utils.model_loader import ModelLoader
from app.utils.routine_builder import (
    generate_personalized_routine,
    generate_routine_insights
)

# ========== PAGE CONFIG ==========
logo_path = Path(__file__).parent / "assets" / "logo.png"

st.set_page_config(
    page_title="GlowGuide - Skincare Assistant",
    page_icon=str(logo_path),
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== LOAD ML MODELS (CACHED) ==========
@st.cache_resource
def load_ml_models():
    """Load all pre-trained ML models and encoders once (cached)."""
    try:
        model_loader = ModelLoader()
        model_loader.load_all()  # ✅ LOAD ALL MODELS FROM DISK
        if not model_loader.is_ready():
            raise Exception("Failed to load all required models")
        return model_loader
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None

model_loader = load_ml_models()

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
    st.markdown("<h1 style='margin-top: 10px;'>GlowGuide</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #666666; font-size: 18px; margin-bottom: 28px; font-weight: 500; letter-spacing: 0.3px;'>Find the perfect skincare products based on your unique needs</p>", unsafe_allow_html=True)

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
    
    # ML Backend compatible skin type selector
    skin_type = st.selectbox(
        "Skin Type",
        ["Combination", "Dry", "Normal", "Oily"],
        key="sidebar_skin_type_main"
    )
    
    # Sensitivity level for ML model
    sensitivity = st.radio(
        "Skin Sensitivity",
        ["No", "Yes"],
        horizontal=True,
        key="sidebar_sensitivity_main"
    )
    
    # Primary skin concern for ML model (single selection for prediction)
    primary_concern = st.selectbox(
        "Primary Skin Concern",
        ["Acne", "Dark Circles", "Dark Spots", "Dullness", "Hyperpigmentation", 
         "Open Pores", "Redness", "Sun Tan", "Whiteheads/Blackheads", "Wrinkles"],
        key="sidebar_concern_main"
    )
    
    # Additional concerns (for reference)
    skin_concerns = st.multiselect(
        "Additional Concerns (Optional)",
        ["Dryness", "Oiliness", "Aging", "Sensitivity", "Texture"],
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
    
    search_btn = st.button("Get Ingredient Recommendations", use_container_width=True, key="tab1_search_btn")
    
    if search_btn:
        # ========== BLOCK 11: ML BACKEND INTEGRATION ==========
        # Call the master integration function that combines:
        # - Block 8: Predictions (ingredient + cluster)
        # - Block 9: Products (top 3)
        # - Block 10: Remedies (top 2)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("## Your Personalized Skincare Recommendation")
        
        with st.spinner("Analyzing your skin profile and finding recommendations..."):
            result = generate_full_recommendation(
                skin=skin_type,
                sensitivity=sensitivity,
                concern=primary_concern,
                model_loader=model_loader
            )
        
        if result and result['success']:
            # ===== DISPLAY INGREDIENT PREDICTION =====
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                            padding: 20px; border-radius: 12px; border: 1.5px solid #d1d5db; text-align: center;'>
                    <p style='color: #666666; font-size: 14px; margin: 0; font-weight: 500;'>RECOMMENDED INGREDIENT</p>
                    <p style='color: #000000; font-size: 24px; margin: 10px 0; font-weight: 700;'>{}</p>
                </div>
                """.format(result['ingredient']), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                            padding: 20px; border-radius: 12px; border: 1.5px solid #60a5fa; text-align: center;'>
                    <p style='color: #0c2d6b; font-size: 14px; margin: 0; font-weight: 500;'>YOUR SKIN CLUSTER</p>
                    <p style='color: #0c2d6b; font-size: 22px; margin: 10px 0; font-weight: 700;'>{}</p>
                </div>
                """.format(result['cluster_label']), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                            padding: 20px; border-radius: 12px; border: 1.5px solid #86efac; text-align: center;'>
                    <p style='color: #166534; font-size: 14px; margin: 0; font-weight: 500;'>STATUS</p>
                    <p style='color: #166534; font-size: 22px; margin: 10px 0; font-weight: 700;'>✅ Ready</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # ===== DISPLAY PRODUCTS =====
            # ✅ STEP 3-4: DYNAMIC PRODUCT CARDS WITH SEARCH LINKS & IMAGES
            products = result.get('products', [])
            if products and len(products) > 0:
                st.markdown("### Top Products with This Ingredient")
                
                # Create clickable product cards in a grid
                cols = st.columns(len(products[:3]))
                for idx, product in enumerate(products[:3]):
                    with cols[idx]:
                        product_name = product.get('product_name', 'Unknown Product')
                        price = product.get('price', 0)
                        image_url = product.get('image_url', 'https://via.placeholder.com/150?text=Product')
                        
                        # Get search link (hybrid system: curated or dynamic)
                        search_link = get_product_link(product_name)
                        
                        # Display product card with image
                        st.markdown(f"""
                        <a href="{search_link}" target="_blank" style="text-decoration: none; cursor: pointer;">
                            <div style="
                                border: 1px solid #e5e7eb;
                                padding: 16px;
                                border-radius: 12px;
                                margin-bottom: 12px;
                                background: #ffffff;
                                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
                                transition: all 0.2s ease-in-out;
                                text-align: center;
                            ">
                                <img src="{image_url}" style="
                                    width: 120px;
                                    height: 120px;
                                    object-fit: contain;
                                    margin-bottom: 10px;
                                    border-radius: 8px;
                                " alt="{product_name}"/>
                                
                                <h4 style="
                                    margin: 0;
                                    color: #111827;
                                    font-size: 16px;
                                    font-weight: 600;
                                    margin-bottom: 6px;
                                    line-height: 1.4;
                                ">
                                    {product_name}
                                </h4>
                                
                                <p style="
                                    margin: 0;
                                    color: #6b7280;
                                    font-size: 14px;
                                    margin-bottom: 8px;
                                ">
                                    ₹{price:.0f}
                                </p>
                                
                                <p style="
                                    margin: 0;
                                    font-size: 13px;
                                    color: #2563eb;
                                    font-weight: 600;
                                ">
                                    🔍 Click to view product
                                </p>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
            else:
                # ✅ GRACEFUL FALLBACK MESSAGE
                st.info(f"ℹ️ Limited product data available for **{result.get('ingredient', 'this ingredient')}**. "
                        "Consider searching for alternative products with similar key ingredients.")
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # ===== DISPLAY REMEDIES =====
            # ✅ STEP 6: OUTPUT HANDLING
            remedies = result.get('remedies', [])
            if remedies and len(remedies) > 0:
                st.markdown("### Home Remedies for Your Skin Concern")
                
                for idx, remedy in enumerate(remedies, 1):
                    with st.expander(f"Remedy {idx}: {remedy.get('Problem', 'Unknown')}", expanded=(idx == 1)):
                        st.markdown(f"**Problem:** {remedy.get('Problem', 'N/A')}")
                        st.markdown(f"**Category:** {remedy.get('Category', 'N/A')}")
                        st.markdown(f"**Ingredients:** {remedy.get('Ingredients', 'N/A')}")
                        st.markdown(f"**Usage:** {remedy.get('Usage', 'N/A')}")
                        st.markdown(f"**Frequency:** {remedy.get('Frequency', 'N/A')}")
            else:
                # ✅ GRACEFUL FALLBACK MESSAGE
                st.info(f"ℹ️ Limited remedy data available for **{result.get('ingredient', 'this ingredient')}**. "
                        "Consult with a dermatologist for personalized home remedy recommendations.")
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # Summary
            st.markdown("<div class='success-badge'>✅ Complete recommendation generated! Share with your dermatologist for personalized advice.</div>", unsafe_allow_html=True)
        
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'Failed to generate recommendation'
            st.error(f"❌ Could not generate recommendation: {error_msg}")
            st.info("Please check your input values and try again.")

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
    st.markdown("## Your Personalized Skincare Routine")
    st.markdown("Based on your skin profile and ML analysis, we'll create a routine using trained dataset recommendations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        routine_type = st.radio(
            "Choose routine time",
            ["Morning Routine", "Night Routine"],
            horizontal=True,
            key="tab3_routine_type"
        )
    
    with col2:
        routine_focus = st.selectbox(
            "Focus Area",
            ["Hydration", "Anti-aging", "Acne Control", "Brightening", "Sensitive Care"],
            key="tab3_focus"
        )
    
    generate_btn = st.button("Generate Personalized Routine", use_container_width=True, key="tab3_generate_btn")
    
    if generate_btn:
        with st.spinner("Analyzing your profile and generating personalized routine..."):
            # Step 1: Get ML prediction using user's profile
            ml_result = generate_full_recommendation(
                skin=skin_type,
                sensitivity=sensitivity,
                concern=primary_concern,
                model_loader=model_loader
            )
            
            if ml_result and ml_result['success']:
                # Step 2: Generate routine based on ML prediction
                user_profile = {
                    'skin_type': skin_type,
                    'sensitivity': sensitivity,
                    'primary_concern': primary_concern,
                    'age': age,
                    'skin_concerns': skin_concerns,
                    'budget_min': budget_min
                }
                
                routine_type_label = "Morning" if "Morning" in routine_type else "Night"
                
                routine = generate_personalized_routine(
                    user_profile=user_profile,
                    ml_prediction=ml_result,
                    routine_type=routine_type_label,
                    routine_focus=routine_focus
                )
                
                # Step 3: Generate detailed insights
                insights = generate_routine_insights(
                    user_profile=user_profile,
                    ml_prediction=ml_result,
                    routine=routine
                )
                
                if routine['success']:
                    # ===== DISPLAY ROUTINE OVERVIEW =====
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    st.markdown(f"## Your {routine_type}")
                    
                    # Display routine summary cards
                    summary_col1, summary_col2, summary_col3 = st.columns(3)
                    
                    with summary_col1:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                    padding: 20px; border-radius: 12px; border: 1.5px solid #60a5fa; text-align: center;'>
                            <p style='color: #0c2d6b; font-size: 14px; margin: 0; font-weight: 500;'>RECOMMENDED INGREDIENT</p>
                            <p style='color: #0c2d6b; font-size: 24px; margin: 10px 0; font-weight: 700;'>{ml_result['ingredient']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with summary_col2:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                                    padding: 20px; border-radius: 12px; border: 1.5px solid #d1d5db; text-align: center;'>
                            <p style='color: #374151; font-size: 14px; margin: 0; font-weight: 500;'>ROUTINE LENGTH</p>
                            <p style='color: #111827; font-size: 24px; margin: 10px 0; font-weight: 700;'>{routine['total_time']} min</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with summary_col3:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                                    padding: 20px; border-radius: 12px; border: 1.5px solid #86efac; text-align: center;'>
                            <p style='color: #166534; font-size: 14px; margin: 0; font-weight: 500;'>SKIN TYPE</p>
                            <p style='color: #166534; font-size: 24px; margin: 10px 0; font-weight: 700;'>{skin_type}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== VISUALIZATION 1: ROUTINE TIMELINE =====
                    st.markdown("### Routine Timeline - Time Allocation per Step")
                    
                    timeline_data = []
                    for step in routine['steps']:
                        timeline_data.append({
                            'Step': f"{step['step_num']}. {step['product_type']}",
                            'Time': step['time'],
                            'Product': step['name'][:30]
                        })
                    
                    timeline_df = pd.DataFrame(timeline_data)
                    fig_timeline = px.bar(
                        timeline_df,
                        x='Time',
                        y='Step',
                        orientation='h',
                        title='Time Commitment per Step',
                        labels={'Time': 'Minutes', 'Step': 'Routine Step'},
                        color='Time',
                        color_continuous_scale='Blues',
                        text='Time'
                    )
                    fig_timeline.update_traces(textposition='auto')
                    fig_timeline.update_layout(
                        height=300,
                        showlegend=False,
                        xaxis_title='Minutes',
                        yaxis_title='',
                        hovermode='y unified'
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== DISPLAY ROUTINE STEPS TABLE =====
                    st.markdown("### Routine Steps (In Order)")
                    
                    routine_table_data = []
                    for step in routine['steps']:
                        routine_table_data.append({
                            'Step': f"{step['step_num']}. {step['product_type']}",
                            'Product': step['name'],
                            'Time (min)': step['time'],
                            'Benefit': step['benefit']
                        })
                    
                    routine_df = pd.DataFrame(routine_table_data)
                    st.dataframe(routine_df, use_container_width=True, hide_index=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== VISUALIZATION 2: PRODUCT BENEFITS DISTRIBUTION =====
                    st.markdown("### Skin Concern Coverage - How This Routine Addresses Your Needs")
                    
                    concern_mapping = {
                        'Acne': 0,
                        'Dark Circles': 0,
                        'Dark Spots': 0,
                        'Dullness': 0,
                        'Hyperpigmentation': 0,
                        'Open Pores': 0,
                        'Redness': 0,
                        'Sun Tan': 0,
                        'Whiteheads/Blackheads': 0,
                        'Wrinkles': 0
                    }
                    
                    benefit_keywords = {
                        'Acne': ['clarifying', 'breakout', 'acne', 'pore', 'control'],
                        'Dark Circles': ['dark circle', 'eye', 'fine line'],
                        'Dark Spots': ['brightening', 'dark', 'spot', 'hyperpigmentation'],
                        'Dullness': ['brightening', 'glow', 'radiant'],
                        'Wrinkles': ['anti-aging', 'firming', 'collagen', 'fine line'],
                        'Redness': ['soothing', 'calming', 'sensitive'],
                    }
                    
                    for step in routine['steps']:
                        benefit_lower = step['benefit'].lower()
                        for concern, keywords in benefit_keywords.items():
                            if any(kw in benefit_lower for kw in keywords):
                                if concern in concern_mapping:
                                    concern_mapping[concern] += 1
                    
                    concern_data = pd.DataFrame([
                        {'Concern': k, 'Coverage': v} 
                        for k, v in concern_mapping.items() 
                        if v > 0
                    ])
                    
                    if len(concern_data) > 0:
                        fig_concerns = px.bar(
                            concern_data,
                            x='Concern',
                            y='Coverage',
                            title='Skin Concern Coverage by This Routine',
                            labels={'Coverage': 'Number of Steps Addressing'},
                            color='Coverage',
                            color_continuous_scale='Greens',
                            text='Coverage'
                        )
                        fig_concerns.update_traces(textposition='auto')
                        fig_concerns.update_layout(
                            height=350,
                            showlegend=False,
                            xaxis_tickangle=-45,
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_concerns, use_container_width=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== VISUALIZATION 3: ROUTINE COMPOSITION =====
                    st.markdown("### Routine Composition - Product Types Distribution")
                    
                    product_types = [step['product_type'] for step in routine['steps']]
                    product_type_counts = pd.Series(product_types).value_counts().reset_index()
                    product_type_counts.columns = ['Product Type', 'Count']
                    
                    fig_composition = px.pie(
                        product_type_counts,
                        names='Product Type',
                        values='Count',
                        title='Product Types in Your Routine',
                        color_discrete_sequence=['#3B82F6', '#8B5CF6', '#EC4899', '#F59E0B', '#10B981']
                    )
                    fig_composition.update_layout(height=350)
                    st.plotly_chart(fig_composition, use_container_width=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== DISPLAY DETAILED STEP BREAKDOWN =====
                    st.markdown("### Step-by-Step Breakdown")
                    
                    for step in routine['steps']:
                        with st.expander(
                            f"Step {step['step_num']}: {step['product_type']} - {step['name']}",
                            expanded=(step['step_num'] == 1)
                        ):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"**Why This Product?**")
                                st.markdown(f"{step['reason']}")
                                st.markdown(f"\n**Key Benefit:** {step['benefit']}")
                            
                            with col2:
                                st.markdown(f"**Application Time:** {step['time']} minutes")
                                st.markdown(f"**Product Type:** {step['product_type']}")
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== DISPLAY TIPS =====
                    st.markdown("### Tips for Better Results")
                    
                    tips_html = "<div class='info-badge'>"
                    for idx, tip in enumerate(routine['tips'], 1):
                        tips_html += f"<strong>Tip {idx}:</strong> {tip}<br><br>"
                    tips_html += "</div>"
                    
                    st.markdown(tips_html, unsafe_allow_html=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== VISUALIZATION 4: ML CONFIDENCE & PERSONALIZATION FACTORS =====
                    st.markdown("### Personalization Analysis - ML Model Insights")
                    
                    col_viz1, col_viz2 = st.columns(2)
                    
                    with col_viz1:
                        st.markdown("#### ML Model Confidence")
                        
                        confidence_data = pd.DataFrame({
                            'Metric': ['Ingredient Accuracy', 'Cluster Assignment', 'Overall Recommendation'],
                            'Score': [
                                ml_result.get('ingredient_confidence', 0),
                                ml_result.get('cluster_confidence', 0),
                                ml_result.get('overall_confidence', 0)
                            ]
                        })
                        
                        fig_confidence = px.bar(
                            confidence_data,
                            x='Score',
                            y='Metric',
                            orientation='h',
                            title='Model Performance Metrics',
                            color='Score',
                            color_continuous_scale='Viridis',
                            text='Score'
                        )
                        fig_confidence.update_traces(textposition='auto')
                        fig_confidence.update_layout(
                            height=300,
                            showlegend=False,
                            xaxis_title='Confidence Score (%)',
                            yaxis_title=''
                        )
                        st.plotly_chart(fig_confidence, use_container_width=True)
                    
                    with col_viz2:
                        st.markdown("#### Input Profile Summary")
                        
                        profile_metrics = {
                            'Skin Type': skin_type,
                            'Sensitivity': sensitivity,
                            'Primary Concern': primary_concern,
                            'Age': str(age),
                            'Skin Cluster': ml_result['cluster_label']
                        }
                        
                        profile_text = "<div style='padding: 15px; background: #f9fafb; border-radius: 8px; border: 1px solid #e5e7eb;'>"
                        for key, value in profile_metrics.items():
                            profile_text += f"<p style='margin: 8px 0;'><strong>{key}:</strong> {value}</p>"
                        profile_text += "</div>"
                        
                        st.markdown(profile_text, unsafe_allow_html=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # ===== DISPLAY DETAILED INSIGHTS =====
                    st.markdown("### Routine Personalization Details")
                    
                    # Input Summary
                    with st.expander("Your Input Profile", expanded=True):
                        input_cols = st.columns(2)
                        with input_cols[0]:
                            st.markdown("**Skin Profile:**")
                            for key, value in insights['input_summary'].items():
                                st.markdown(f"• **{key.replace('_', ' ').title()}:** {value}")
                        
                        with input_cols[1]:
                            st.markdown("**ML Analysis:**")
                            for key, value in insights['ml_analysis'].items():
                                st.markdown(f"• **{key.replace('_', ' ').title()}:** {value}")
                    
                    # Personalization Factors
                    with st.expander("Personalization Factors", expanded=True):
                        for factor in insights['personalization_factors']:
                            st.markdown(f"{factor}")
                    
                    # Routine Rationale
                    with st.expander("Why This Routine?", expanded=True):
                        st.markdown(insights['routine_rationale'])
                    
                    # Effectiveness Timeline
                    with st.expander("Expected Results Timeline", expanded=False):
                        st.markdown(f"**You can expect to see changes in:** {insights['effectiveness_timeline']}")
                        st.markdown(
                            "\n**Note:** Consistency is key. Use this routine daily for best results. "
                            "Skin typically needs 4-6 weeks of consistent care to show visible improvements."
                        )
                    
                    # Key Insights
                    with st.expander("Key Insights & Data Points", expanded=True):
                        for insight in insights['key_insights']:
                            st.markdown(f"\n{insight}")
                    
                    st.markdown("<div class='success-badge'>Routine created successfully! Save this page for reference and start using your personalized routine today.</div>", unsafe_allow_html=True)
                
                else:
                    st.error(f"Failed to generate routine: {routine.get('error', 'Unknown error')}")
            else:
                st.error(f"Could not analyze your profile. Error: {ml_result.get('error', 'Unknown error') if ml_result else 'Model not loaded'}")

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
