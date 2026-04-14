"""Market insights and data visualization component."""

import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from collections import Counter
from utils.helpers import clean_text


def render_charts(df: pd.DataFrame, vectorizer) -> None:
    """
    Render all market insights visualizations.
    """
    if df is None or vectorizer is None:
        st.warning("Unable to load data for visualizations.")
        return
    
    try:
        # Chart 1: Price Distribution by Category
        fig1 = px.box(
            df,
            x="Label",
            y="Price",
            color="Label",
            title="Price Distribution by Product Category",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Price (USD)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        st.divider()
        
        # Chart 2: Top 20 Most Common Ingredients
        all_ingredients = []
        for ingredients_str in df["Ingredients"].fillna(""):
            if ingredients_str:
                cleaned = clean_text(ingredients_str)
                all_ingredients.extend(cleaned.split())
        
        ingredient_counts = Counter(all_ingredients)
        top_20 = ingredient_counts.most_common(20)
        names, counts = zip(*top_20)
        
        fig2 = px.bar(
            x=counts,
            y=names,
            orientation="h",
            title="Top 20 Most Frequent Ingredients",
            color=counts,
            color_continuous_scale="Purples"
        )
        fig2.update_layout(
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            xaxis_title="Frequency",
            yaxis_title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.divider()
        
        # Chart 3: Product Clusters (PCA 2D)
        all_ingredients_df = df["Ingredients"].fillna("").apply(clean_text)
        all_vectors = vectorizer.transform(all_ingredients_df)
        
        pca = PCA(n_components=2)
        pca_results = pca.fit_transform(all_vectors.toarray() if hasattr(all_vectors, 'toarray') else all_vectors)
        
        cluster_df = pd.DataFrame({
            "Component 1": pca_results[:, 0],
            "Component 2": pca_results[:, 1],
            "Name": df["Name"].values,
            "Label": df["Label"].values,
            "Price": df["Price"].values,
            "Cluster": df["Cluster"].astype(str).values
        })
        
        fig3 = px.scatter(
            cluster_df,
            x="Component 1",
            y="Component 2",
            color="Cluster",
            hover_data=["Name", "Label", "Price"],
            title="Product Clusters (PCA View)",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering charts: {str(e)}")
