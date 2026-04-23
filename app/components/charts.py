"""Data visualization components for market intelligence - Premium Styling."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.engine import get_top_ingredients, get_full_tfidf_matrix, get_pca_coords
from utils.styles import SECTION_HEADER


def render_price_distribution(df: pd.DataFrame, selected_labels: list, price_range: tuple) -> None:
    """Box plot of price distribution by product category - Premium Styling."""
    filtered = df[
        (df["Label"].isin(selected_labels)) &
        (df["Price"] >= price_range[0]) &
        (df["Price"] <= price_range[1])
    ]
    
    if filtered.empty:
        st.info("No products match current filters.")
        return
    
    fig = px.box(
        filtered, x="Label", y="Price", color="Label",
        title="Price Distribution by Category",
        color_discrete_sequence=["#1f2937", "#374151", "#4b5563", "#6b7280", "#9ca3af"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#1f2937", size=13),
        showlegend=False,
        xaxis_title="Product Category",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        title_font_size=18,
        title_font_color="#000000",
        height=400,
        margin=dict(l=60, r=40, t=60, b=50)
    )
    fig.update_traces(marker=dict(line=dict(color="#ffffff", width=1)))
    st.plotly_chart(fig, use_container_width=True)


def render_ingredient_frequency(df: pd.DataFrame) -> None:
    """Horizontal bar chart of top 20 ingredients - Premium Styling."""
    names, counts = get_top_ingredients(df, 20)
    
    if not names:
        st.info("No ingredient data available.")
        return
    
    fig = px.bar(
        x=counts, y=names, orientation="h",
        title="Top 20 Most Frequent Ingredients",
        color=counts,
        color_continuous_scale=["#e5e7eb", "#1f2937"],
        labels={"x": "Frequency", "y": ""}
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#1f2937", size=13),
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
        hovermode="y",
        xaxis_title="Frequency Count",
        yaxis_title="Ingredient",
        title_font_size=18,
        title_font_color="#000000",
        height=400,
        margin=dict(l=150, r=40, t=60, b=50)
    )
    fig.update_traces(textposition='auto')
    st.plotly_chart(fig, use_container_width=True)


def render_cluster_map(df: pd.DataFrame, vectorizer) -> None:
    """PCA 2D scatter of product clusters - Premium Styling."""
    try:
        full_matrix = get_full_tfidf_matrix(df, vectorizer)
        x_coords, y_coords = get_pca_coords(full_matrix)
        
        pca_df = pd.DataFrame({
            "pca_x": x_coords,
            "pca_y": y_coords,
            "Name": df["Name"].values,
            "Brand": df["Brand"].values,
            "Price": df["Price"].values,
            "Label": df["Label"].values,
            "Cluster": df["Cluster"].astype(str).values
        })
        
        fig = px.scatter(
            pca_df, x="pca_x", y="pca_y",
            color="Cluster",
            hover_data=["Name", "Brand", "Price", "Label"],
            title="Product Clusters (PCA View)",
            color_discrete_sequence=["#1f2937", "#374151", "#4b5563", "#6b7280", "#9ca3af"],
            labels={"pca_x": "Principal Component 1", "pca_y": "Principal Component 2"}
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#1f2937", size=13),
            hovermode="closest",
            title_font_size=18,
            title_font_color="#000000",
            height=450,
            margin=dict(l=80, r=40, t=60, b=80)
        )
        fig.update_traces(
            marker=dict(size=8, line=dict(color="#ffffff", width=1), opacity=0.8)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering cluster map: {str(e)}")


def render_rating_vs_price(df: pd.DataFrame) -> None:
    """Scatter: price on X, rating on Y, colored by category."""
    fig = px.scatter(
        df, x="Price", y="Rank", color="Label",
        hover_data=["Name", "Brand"],
        title="Rating vs Price",
        opacity=0.65,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#0F172A"),
        xaxis_title="Price (USD)",
        yaxis_title="Rating (0-5)",
        hovermode="closest"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_all_charts(df, vectorizer, selected_labels, price_range) -> None:
    """Entry point — renders all 4 charts in a 2x2 grid."""
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Price Distribution")
        fig_price = steel_histogram(filtered, x="Price", title="Price Distribution")
        st.plotly_chart(fig_price, use_container_width=True)
    with c2:
        st.markdown("### Ingredient Clusters (PCA)")
        fig_pca = steel_scatter(filtered, x="PCA1", y="PCA2", title="Ingredient Clusters")
        st.plotly_chart(fig_pca, use_container_width=True)
    
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("### Market Trends")
        st.info("Cluster analysis visualization will appear here")
    with c4:
        st.markdown("### Rating vs Price")
        st.info("Price-rating correlation will appear here")
