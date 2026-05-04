"""
Page 2: Data Explorer
Deep-dive into the dataset with EDA tools — statistics, distributions, correlations.
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_processing import get_dataset_info, get_class_distribution
from utils.visualization import (
    plot_class_distribution, plot_class_pie,
    plot_correlation_heatmap, plot_feature_distributions
)

st.set_page_config(page_title="Data Explorer • SecureNet IDS", page_icon="🔬", layout="wide")

st.markdown("""
<div style="border-left: 4px solid #1B6EF3; padding-left: 14px; margin-bottom: 24px;">
    <h1 style="margin:0; font-weight:800; font-size:1.8rem;">🔬 Data Explorer</h1>
    <p style="color:#6B7280; margin:4px 0 0 0;">Exploratory Data Analysis — Understand the threats in your data</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.get('dataset') is None:
    st.warning("⚠️ No dataset loaded. Please go to **Dashboard** and upload a dataset first.", icon="⚠️")
    if st.button("← Go to Dashboard"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.dataset
label_col = st.session_state.label_column
info = get_dataset_info(df)

# ── Dataset Statistics ──
tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistics", "📈 Distributions", "🔗 Correlations", "🧹 Data Quality"])

with tab1:
    st.subheader("Dataset Statistics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{info['rows']:,}")
    c2.metric("Columns", info['columns'])
    c3.metric("Numeric", info['numeric_columns'])
    c4.metric("Categorical", info['categorical_columns'])

    st.markdown("##### Descriptive Statistics (Numeric Features)")
    st.dataframe(df.describe().T.style.format("{:.3f}"), use_container_width=True, height=400)

    st.markdown("##### Column Types & Non-Null Counts")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.astype(str).values,
        'Non-Null': df.notnull().sum().values,
        'Null': df.isnull().sum().values,
        'Unique': df.nunique().values,
    })
    st.dataframe(col_info, use_container_width=True, height=400)

    if label_col:
        st.markdown("##### Class Distribution")
        dist = get_class_distribution(df[label_col])
        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(dist, use_container_width=True)
        with c2:
            st.plotly_chart(plot_class_pie(df[label_col]), use_container_width=True)

with tab2:
    st.subheader("Feature Distributions")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        st.info("No numeric columns found.")
    else:
        selected_features = st.multiselect(
            "Select features to visualize",
            options=numeric_cols,
            default=numeric_cols[:4] if len(numeric_cols) >= 4 else numeric_cols,
            max_selections=8
        )
        if selected_features:
            color_by = st.checkbox("Color by target label", value=True if label_col else False)
            figs = plot_feature_distributions(
                df, selected_features,
                label_col=label_col if color_by else None
            )
            cols = st.columns(min(2, len(figs)))
            for i, fig in enumerate(figs):
                with cols[i % 2]:
                    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Feature Correlation Analysis")
    top_n = st.slider("Number of features to include", 5, min(50, len(df.select_dtypes(include=[np.number]).columns)), 20)
    fig = plot_correlation_heatmap(df, top_n=top_n)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Highly Correlated Feature Pairs")
    numeric_df = df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) > 1:
        corr_matrix = numeric_df.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        high_corr = []
        for col in upper.columns:
            for idx in upper.index:
                val = upper.loc[idx, col]
                if pd.notna(val) and val > 0.8:
                    high_corr.append({'Feature 1': idx, 'Feature 2': col, 'Correlation': round(val, 4)})
        if high_corr:
            st.dataframe(pd.DataFrame(high_corr).sort_values('Correlation', ascending=False),
                         use_container_width=True)
        else:
            st.success("No highly correlated pairs (>0.8) found.", icon="✅")

with tab4:
    st.subheader("Data Quality Report")

    c1, c2, c3 = st.columns(3)
    c1.metric("Missing Values", f"{info['missing_values']:,}")
    c2.metric("Duplicate Rows", f"{info['duplicate_rows']:,}")
    c3.metric("Memory Usage", info['memory_usage'])

    # Missing values detail
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if len(missing) > 0:
        st.markdown("##### Columns with Missing Values")
        miss_df = pd.DataFrame({'Column': missing.index, 'Missing': missing.values,
                                'Percentage': (missing.values / len(df) * 100).round(2)})
        st.dataframe(miss_df, use_container_width=True)
    else:
        st.success("✅ No missing values detected!", icon="✅")

    # Check for infinite values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    inf_count = np.isinf(df[numeric_cols]).sum()
    inf_count = inf_count[inf_count > 0]
    if len(inf_count) > 0:
        st.warning(f"⚠️ Found {inf_count.sum()} infinite values in {len(inf_count)} columns")
    else:
        st.success("✅ No infinite values detected!", icon="✅")
