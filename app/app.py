# -*- coding: utf-8 -*-
"""GlowGuide - Smart Skincare Recommender with Minimal Color Theme"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

.main {
    background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 1px solid #e5e7eb;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"] {
    padding: 16px 24px;
    font-weight: 500;
    font-size: 15px;
    font-family: 'Space Grotesk', sans-serif;
    border-radius: 8px 8px 0 0;
    color: #6b7280;
    background-color: transparent;
    border-bottom: 3px solid transparent;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #000000;
    background-color: rgba(0, 0, 0, 0.02);
    border-bottom-color: #000000;
    font-weight: 600;
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    color: white;
    border: none;
    border-radius: 8px;
    height: 48px;
    font-weight: 600;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.18);
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.stButton>button:active {
    transform: translateY(-1px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

/* Typography */
h1, h2, h3 {
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.5px;
}

h1 {
    text-align: center;
    margin-bottom: 12px;
    font-size: 44px;
    font-weight: 700;
    animation: fadeIn 0.6s ease-out;
}

h2 {
    font-size: 32px;
    margin-top: 24px;
    margin-bottom: 18px;
    font-weight: 700;
}

h3 {
    font-size: 22px;
    margin-top: 18px;
    margin-bottom: 14px;
    font-weight: 600;
}

p {
    color: #4b5563;
    line-height: 1.7;
    font-family: 'DM Sans', sans-serif;
}

/* Input Styling */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox select {
    border: 2px solid #e5e7eb !important;
    border-radius: 8px !important;
    font-size: 15px !important;
    padding: 14px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    background-color: #fafbfc !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus,
.stSelectbox select:focus {
    border-color: #000000 !important;
    background-color: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.08) !important;
}

/* Checkbox Styling */
.stCheckbox {
    padding: 10px 0;
    transition: all 0.2s ease;
}

.stCheckbox label {
    font-weight: 500;
    color: #1f2937;
    font-family: 'DM Sans', sans-serif;
}

/* Metric Cards */
.metric-card {
    background: white;
    padding: 22px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    border: 1px solid #f3f4f6;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

/* Product Cards */
.product-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin: 12px 0;
    border: 1px solid #f3f4f6;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    transform: translateY(-3px);
    border-color: #e5e7eb;
}

/* Tags */
.ingredient-tag {
    display: inline-block;
    background: #f3f4f6;
    color: #1f2937;
    padding: 8px 14px;
    border-radius: 20px;
    margin: 6px 6px 6px 0;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid #e5e7eb;
    transition: all 0.2s ease;
    cursor: default;
}

.ingredient-tag:hover {
    background: #e5e7eb;
    border-color: #d1d5db;
}

.ingredient-tag.safe {
    background: #ecfdf5;
    color: #065f46;
    border-color: #6ee7b7;
}

.ingredient-tag.active {
    background: #ede9fe;
    color: #6d28d9;
    border-color: #c4b5fd;
}

.ingredient-tag.warning {
    background: #fef3c7;
    color: #92400e;
    border-color: #fcd34d;
}

/* Badges */
.success-badge {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    color: #15803d;
    padding: 16px 20px;
    border-radius: 10px;
    margin: 14px 0;
    font-weight: 500;
    border: 1px solid #86efac;
    animation: slideInLeft 0.5s ease-out;
}

.info-badge {
    background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
    color: #0c4a6e;
    padding: 16px 20px;
    border-radius: 10px;
    margin: 14px 0;
    font-weight: 500;
    border: 1px solid #93c5fd;
    animation: slideInLeft 0.5s ease-out 0.1s both;
}

.warning-badge {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    color: #92400e;
    padding: 16px 20px;
    border-radius: 10px;
    margin: 14px 0;
    font-weight: 500;
    border: 1px solid #fcd34d;
    animation: slideInLeft 0.5s ease-out 0.2s both;
}

/* Divider */
.divider {
    margin: 28px 0;
    border-top: 1px solid #e5e7eb;
}

/* Slider */
.stSlider label {
    font-weight: 600;
    color: #1f2937;
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar Header */
.sidebar-header {
    font-size: 18px;
    font-weight: 700;
    color: #000000;
    font-family: 'Space Grotesk', sans-serif;
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 2px solid #000000;
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
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    border: 1px solid #f3f4f6;
}

</style>
""", unsafe_allow_html=True)

# ========== TITLE & SUBTITLE ==========
col1, col2 = st.columns([1, 5])
with col1:
    st.image(str(logo_path), width=80)
with col2:
    st.markdown("<h1>GlowGuide</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #555555; font-size: 17px; margin-bottom: 24px;'>Find the perfect skincare products based on your unique needs</p>", unsafe_allow_html=True)

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
tab1, tab2, tab3 = st.tabs(["Product Search", "Ingredient Analyzer", "Routine Builder"])

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
    
    search_btn = st.button("Find Similar Products", use_container_width=True, key="tab1_search_btn")
    
    if search_btn:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("## Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Similarity Score", "92%", "+5%")
        with col2:
            st.metric("Safety Score", "88%", "+2%")
        with col3:
            st.metric("Predicted Rating", "4.5/5", "+0.3")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Recommended Products")
        
        products = [
            {"name": "CeraVe Moisturizing Lotion", "brand": "CeraVe", "price": "800", "rating": "4.7", "similarity": "95%"},
            {"name": "Cetaphil Cream", "brand": "Cetaphil", "price": "600", "rating": "4.5", "similarity": "88%"},
            {"name": "Neutrogena Hydro Boost", "brand": "Neutrogena", "price": "450", "rating": "4.3", "similarity": "85%"},
            {"name": "La Roche Posay Lotion", "brand": "La Roche Posay", "price": "1200", "rating": "4.8", "similarity": "92%"},
            {"name": "Avene Cream", "brand": "Avene", "price": "950", "rating": "4.6", "similarity": "87%"}
        ]
        
        for i, prod in enumerate(products):
            st.markdown(f"""
            <div class='product-card'>
                <strong>{prod['name']}</strong> by {prod['brand']}<br>
                Price: Rs. {prod['price']} | Rating: {prod['rating']} | Similarity: {prod['similarity']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### Market Insights")
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
        
        st.markdown("<div class='success-badge'>Found 5 perfect matches for your skin type!</div>", unsafe_allow_html=True)

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

# ========== FOOTER ==========
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #888888; font-size: 13px; margin-top: 24px;'>
    Made with care using Streamlit | GlowGuide v1.0
</p>
""", unsafe_allow_html=True)
