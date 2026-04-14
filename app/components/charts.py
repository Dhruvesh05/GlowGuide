"""Data visualization components for market intelligence."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.engine import get_top_ingredients, get_full_tfidf_matrix, get_pca_coords
from utils.styles import SECTION_HEADER


def render_price_distribution(df: pd.DataFrame, selected_labels: list, price_range: tuple) -> None:
    """Box plot of price distribution by product category."""
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
        color_discrete_sequence=["#6366F1", "#8B5CF6", "#A78BFA", "#C4B5FD", "#DDD6FE"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#0F172A"),
        showlegend=False,
        xaxis_title="",
        yaxis_title="Price (USD)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_ingredient_frequency(df: pd.DataFrame) -> None:
    """Horizontal bar chart of top 20 ingredients."""
    names, counts = get_top_ingredients(df, 20)
    
    if not names:
        st.info("No ingredient data available.")
        return
    
    fig = px.bar(
        x=counts, y=names, orientation="h",
        title="Top 20 Ingredients",
        color=counts,
        color_continuous_scale=["#EEF2FF", "#6366F1"],
        labels={"x": "Frequency", "y": ""}
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#0F172A"),
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
        hovermode="y"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_cluster_map(df: pd.DataFrame, vectorizer) -> None:
    """PCA 2D scatter of product clusters."""
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
            color_discrete_sequence=px.colors.qualitative.Safe,
            labels={"pca_x": "Component 1", "pca_y": "Component 2"}
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#0F172A"),
            hovermode="closest"
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
