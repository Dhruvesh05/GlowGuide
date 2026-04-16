"""
Block 6: EDA Dashboard (Exploratory Data Analysis)

Provides data visualization and insights into the skincare dataset.
Includes:
- Skin type distribution
- Ingredient recommendation frequency
- Concern frequency analysis
- Dataset statistics and summary

Functions:
- display_dataset_overview() - High-level dataset info
- display_skin_type_distribution() - Visualization of skin types
- display_ingredient_distribution() - Visualization of ingredients
- display_concern_frequency() - Visualization of concerns
- display_dataset_statistics() - Statistical summary
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Tuple

# Import data loaders
from app.utils import (
    load_skincare_dataset,
    get_dataset_summary,
    get_dataset_statistics
)


def display_eda_dashboard():
    """
    Main EDA dashboard display function.
    Shows comprehensive data visualizations and statistics.
    """
    
    st.markdown("## 📊 Data Science Insights")
    st.markdown(
        "<p style='font-size: 14px; color: #666; margin-bottom: 20px;'>"
        "Explore the skincare dataset: Ingredient recommendations, skin type distribution, "
        "and concern patterns from 50 analyzed skincare profiles."
        "</p>",
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Load dataset once
    try:
        df = load_skincare_dataset()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return
    
    # ====================================================================
    # SECTION 1: DATASET OVERVIEW
    # ====================================================================
    
    st.markdown("### 📋 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Samples", len(df), "skincare profiles")
    
    with col2:
        st.metric("Unique Ingredients", df['RecommendedIngredient'].nunique(), "ingredient classes")
    
    with col3:
        st.metric("Skin Types", df['SkinType'].nunique(), "categories")
    
    with col4:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("Data Quality", f"{100-missing_pct:.0f}%", "complete data")
    
    st.divider()
    
    # ====================================================================
    # SECTION 2: MAIN VISUALIZATIONS (3 columns)
    # ====================================================================
    
    st.markdown("### 📈 Key Distributions")
    
    col1, col2, col3 = st.columns(3)
    
    # Column 1: Skin Type Distribution
    with col1:
        st.markdown("#### Skin Type Distribution")
        skin_type_dist = df['SkinType'].value_counts().reset_index()
        skin_type_dist.columns = ['Skin Type', 'Count']
        
        fig1 = px.bar(
            skin_type_dist,
            x='Skin Type',
            y='Count',
            title="Distribution of Skin Types",
            color='Count',
            color_continuous_scale='Blues',
            labels={'Count': 'Number of Profiles'},
            text='Count'
        )
        fig1.update_traces(textposition='auto')
        fig1.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="Skin Type",
            yaxis_title="Count",
            hovermode='x unified'
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Stats
        with st.expander("View Stats", expanded=False):
            st.write(skin_type_dist.sort_values('Count', ascending=False))
    
    # Column 2: Ingredient Distribution
    with col2:
        st.markdown("#### Ingredient Recommendations")
        ingredient_dist = df['RecommendedIngredient'].value_counts().reset_index()
        ingredient_dist.columns = ['Ingredient', 'Count']
        
        fig2 = px.bar(
            ingredient_dist,
            x='Ingredient',
            y='Count',
            title="Count of Each Ingredient",
            color='Count',
            color_continuous_scale='Greens',
            labels={'Count': 'Frequency'},
            text='Count'
        )
        fig2.update_traces(textposition='auto')
        fig2.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="Ingredient",
            yaxis_title="Count",
            hovermode='x unified'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Stats
        with st.expander("View Stats", expanded=False):
            st.write(ingredient_dist.sort_values('Count', ascending=False))
    
    # Column 3: Concern Frequency
    with col3:
        st.markdown("#### Concern Frequency")
        
        # Count occurrences of each concern (Acne, Dryness, Sensitivity, Aging)
        concerns_data = {
            'Acne': df['Acne'].sum(),
            'Dryness': df['Dryness'].sum(),
            'Sensitivity': df['Sensitivity'].sum(),
            'Aging': df['Aging'].sum(),
        }
        
        concerns_df = pd.DataFrame(list(concerns_data.items()), columns=['Concern', 'Count'])
        
        fig3 = px.bar(
            concerns_df,
            x='Concern',
            y='Count',
            title="Skin Concern Frequency",
            color='Count',
            color_continuous_scale='Reds',
            labels={'Count': 'Number of Profiles'},
            text='Count'
        )
        fig3.update_traces(textposition='auto')
        fig3.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="Concern Type",
            yaxis_title="Count",
            hovermode='x unified'
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Stats
        with st.expander("View Stats", expanded=False):
            st.write(concerns_df.sort_values('Count', ascending=False))
    
    st.divider()
    
    # ====================================================================
    # SECTION 3: ADVANCED ANALYSIS
    # ====================================================================
    
    st.markdown("### 🔍 Advanced Analysis")
    
    analysis_cols = st.columns(2)
    
    # Left: Ingredient by Skin Type Heatmap
    with analysis_cols[0]:
        st.markdown("#### Ingredient Recommendations by Skin Type")
        
        # Create cross-tabulation
        crosstab = pd.crosstab(df['SkinType'], df['RecommendedIngredient'])
        
        fig_heat = px.imshow(
            crosstab,
            labels=dict(x="Ingredient", y="Skin Type", color="Count"),
            title="Recommendation Heatmap",
            color_continuous_scale="YlOrRd",
            text_auto=True
        )
        fig_heat.update_layout(height=350)
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # Right: Concern Distribution Pie Chart
    with analysis_cols[1]:
        st.markdown("#### Overall Concern Breakdown")
        
        # Calculate percentage of profiles with each concern
        concern_pcts = {
            'Has Acne': (df['Acne'].sum() / len(df)) * 100,
            'Has Dryness': (df['Dryness'].sum() / len(df)) * 100,
            'Has Sensitivity': (df['Sensitivity'].sum() / len(df)) * 100,
            'Has Aging': (df['Aging'].sum() / len(df)) * 100,
        }
        
        concern_pcts_df = pd.DataFrame(
            list(concern_pcts.items()),
            columns=['Concern', 'Percentage']
        )
        
        fig_pie = px.pie(
            concern_pcts_df,
            names='Concern',
            values='Percentage',
            title="Profile Distribution by Concern",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.divider()
    
    # ====================================================================
    # SECTION 4: CORRELATION & PATTERNS
    # ====================================================================
    
    st.markdown("### 🎯 Pattern Analysis")
    
    pattern_cols = st.columns(2)
    
    with pattern_cols[0]:
        st.markdown("#### Skin Type & Concern Correlation")
        
        # For each skin type, show average concern frequency
        concern_by_skin = pd.DataFrame({
            'Skin Type': df['SkinType'].unique(),
            'Avg Acne': [df[df['SkinType'] == st]['Acne'].mean() for st in df['SkinType'].unique()],
            'Avg Dryness': [df[df['SkinType'] == st]['Dryness'].mean() for st in df['SkinType'].unique()],
            'Avg Sensitivity': [df[df['SkinType'] == st]['Sensitivity'].mean() for st in df['SkinType'].unique()],
            'Avg Aging': [df[df['SkinType'] == st]['Aging'].mean() for st in df['SkinType'].unique()],
        })
        
        # Melt for grouped bar chart
        concern_by_skin_melted = concern_by_skin.melt(
            id_vars='Skin Type',
            value_vars=['Avg Acne', 'Avg Dryness', 'Avg Sensitivity', 'Avg Aging'],
            var_name='Concern',
            value_name='Frequency'
        )
        
        fig_pattern = px.bar(
            concern_by_skin_melted,
            x='Skin Type',
            y='Frequency',
            color='Concern',
            barmode='group',
            title="Concern Frequency by Skin Type",
            labels={'Frequency': 'Avg Frequency'},
            color_discrete_map={
                'Avg Acne': '#FF6B6B',
                'Avg Dryness': '#4ECDC4',
                'Avg Sensitivity': '#45B7D1',
                'Avg Aging': '#FFA07A'
            }
        )
        fig_pattern.update_layout(height=350, hovermode='x unified')
        st.plotly_chart(fig_pattern, use_container_width=True)
    
    with pattern_cols[1]:
        st.markdown("#### Top Recommendations by Concern")
        
        # Create a multi-concern analysis
        # Find which ingredient is recommended most for profiles with specific concerns
        
        st.markdown("**Most Recommended Ingredient per Concern:**")
        
        for concern, col_name in [
            ('Acne', 'Acne'),
            ('Dryness', 'Dryness'),
            ('Sensitivity', 'Sensitivity'),
            ('Aging', 'Aging')
        ]:
            profiles_with_concern = df[df[col_name] == 1]
            if len(profiles_with_concern) > 0:
                top_ingredient = profiles_with_concern['RecommendedIngredient'].value_counts().index[0]
                count = profiles_with_concern['RecommendedIngredient'].value_counts().values[0]
                percentage = (count / len(profiles_with_concern)) * 100
                
                st.markdown(
                    f"**{concern}**: {top_ingredient} "
                    f"({count}/{len(profiles_with_concern)} profiles, {percentage:.0f}%)"
                )
    
    st.divider()
    
    # ====================================================================
    # SECTION 5: DATASET STATISTICS
    # ====================================================================
    
    st.markdown("### 📊 Detailed Statistics")
    
    with st.expander("View Full Dataset Summary", expanded=False):
        summary = get_dataset_summary(df)
        st.text(summary)
    
    with st.expander("View Dataset Statistics", expanded=False):
        stats = get_dataset_statistics(df)
        st.text(stats)
    
    st.divider()
    
    # ====================================================================
    # SECTION 6: RAW DATA
    # ====================================================================
    
    st.markdown("### 🗂️ Raw Dataset")
    
    with st.expander("View Raw Data", expanded=False):
        st.markdown("**Skincare Dataset (50 samples)**")
        
        # Display with formatting
        display_df = df.copy()
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "SkinType": st.column_config.TextColumn(width=120),
                "Acne": st.column_config.NumberColumn(format="%d"),
                "Dryness": st.column_config.NumberColumn(format="%d"),
                "Sensitivity": st.column_config.NumberColumn(format="%d"),
                "Aging": st.column_config.NumberColumn(format="%d"),
                "RecommendedIngredient": st.column_config.TextColumn(width=200),
            }
        )
        
        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Dataset as CSV",
            data=csv,
            file_name="skincare_dataset.csv",
            mime="text/csv"
        )
    
    st.divider()
    
    # ====================================================================
    # SECTION 7: KEY INSIGHTS
    # ====================================================================
    
    st.markdown("### 💡 Key Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        # Most common concern
        concerns_dict = {
            'Acne': df['Acne'].sum(),
            'Dryness': df['Dryness'].sum(),
            'Sensitivity': df['Sensitivity'].sum(),
            'Aging': df['Aging'].sum(),
        }
        most_common_concern = max(concerns_dict, key=concerns_dict.get)
        most_common_count = concerns_dict[most_common_concern]
        
        st.info(
            f"**Most Common Concern**: {most_common_concern} "
            f"({most_common_count}/{len(df)} profiles, {(most_common_count/len(df)*100):.0f}%)"
        )
        
        # Most recommended ingredient
        top_ingredient = df['RecommendedIngredient'].value_counts().index[0]
        top_count = df['RecommendedIngredient'].value_counts().values[0]
        st.info(
            f"**Most Recommended Ingredient**: {top_ingredient} "
            f"({top_count}/{len(df)} profiles, {(top_count/len(df)*100):.0f}%)"
        )
    
    with insights_col2:
        # Skin type distribution insight
        most_common_skin = df['SkinType'].value_counts().index[0]
        most_common_skin_count = df['SkinType'].value_counts().values[0]
        st.info(
            f"**Most Common Skin Type**: {most_common_skin} "
            f"({most_common_skin_count}/{len(df)} profiles, {(most_common_skin_count/len(df)*100):.0f}%)"
        )
        
        # Average concerns per profile
        avg_concerns = (df['Acne'].sum() + df['Dryness'].sum() + 
                       df['Sensitivity'].sum() + df['Aging'].sum()) / len(df)
        st.info(
            f"**Average Concerns per Profile**: {avg_concerns:.2f} "
            f"(out of 4 possible concerns)"
        )


def display_visualization_selector():
    """
    Allow users to select and view specific visualizations.
    """
    
    st.markdown("### 🎨 Custom Visualization Selector")
    
    # Load dataset
    df = load_skincare_dataset()
    
    viz_type = st.selectbox(
        "Select Visualization",
        [
            "Skin Type Distribution",
            "Ingredient Distribution",
            "Concern Frequency",
            "Ingredient by Skin Type",
            "Concern Breakdown Pie",
            "Concern by Skin Type"
        ]
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if viz_type == "Skin Type Distribution":
            skin_dist = df['SkinType'].value_counts().reset_index()
            skin_dist.columns = ['Skin Type', 'Count']
            fig = px.bar(skin_dist, x='Skin Type', y='Count', 
                        title="Skin Type Distribution", text='Count')
            fig.update_traces(textposition='auto')
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Ingredient Distribution":
            ing_dist = df['RecommendedIngredient'].value_counts().reset_index()
            ing_dist.columns = ['Ingredient', 'Count']
            fig = px.bar(ing_dist, x='Ingredient', y='Count',
                        title="Ingredient Distribution", text='Count')
            fig.update_traces(textposition='auto')
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Concern Frequency":
            concerns = {
                'Acne': df['Acne'].sum(),
                'Dryness': df['Dryness'].sum(),
                'Sensitivity': df['Sensitivity'].sum(),
                'Aging': df['Aging'].sum(),
            }
            concerns_df = pd.DataFrame(list(concerns.items()), columns=['Concern', 'Count'])
            fig = px.bar(concerns_df, x='Concern', y='Count',
                        title="Concern Frequency", text='Count')
            fig.update_traces(textposition='auto')
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Ingredient by Skin Type":
            crosstab = pd.crosstab(df['SkinType'], df['RecommendedIngredient'])
            fig = px.imshow(crosstab, labels=dict(x="Ingredient", y="Skin Type", color="Count"),
                           title="Ingredient Recommendations by Skin Type")
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Concern Breakdown Pie":
            concern_pcts = {
                'Acne': (df['Acne'].sum() / len(df)) * 100,
                'Dryness': (df['Dryness'].sum() / len(df)) * 100,
                'Sensitivity': (df['Sensitivity'].sum() / len(df)) * 100,
                'Aging': (df['Aging'].sum() / len(df)) * 100,
            }
            concern_df = pd.DataFrame(list(concern_pcts.items()), columns=['Concern', 'Percentage'])
            fig = px.pie(concern_df, names='Concern', values='Percentage',
                        title="Concern Breakdown")
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Concern by Skin Type":
            concern_by_skin = pd.DataFrame({
                'Skin Type': df['SkinType'].unique(),
                'Acne': [df[df['SkinType'] == st]['Acne'].mean() for st in df['SkinType'].unique()],
                'Dryness': [df[df['SkinType'] == st]['Dryness'].mean() for st in df['SkinType'].unique()],
                'Sensitivity': [df[df['SkinType'] == st]['Sensitivity'].mean() for st in df['SkinType'].unique()],
                'Aging': [df[df['SkinType'] == st]['Aging'].mean() for st in df['SkinType'].unique()],
            })
            melted = concern_by_skin.melt(id_vars='Skin Type', var_name='Concern', value_name='Frequency')
            fig = px.bar(melted, x='Skin Type', y='Frequency', color='Concern',
                        barmode='group', title="Concern Frequency by Skin Type")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Chart Info**")
        st.write(f"Total Records: {len(df)}")
        st.write(f"Columns: {len(df.columns)}")
