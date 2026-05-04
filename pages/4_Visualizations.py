"""
Page 4: Visualizations Dashboard
Comprehensive visualization of model performance and comparisons.
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.model_training import ALGORITHMS
from utils.visualization import (
    plot_confusion_matrix, plot_roc_curve, plot_feature_importance,
    plot_accuracy_comparison, plot_metrics_radar, plot_per_class_metrics,
    plot_class_distribution, PLOTLY_LAYOUT, COLORS
)
import plotly.graph_objects as go

st.set_page_config(page_title="Visualizations • SecureNet IDS", page_icon="📊", layout="wide")

st.markdown("""
<div style="border-left: 4px solid #1B6EF3; padding-left: 14px; margin-bottom: 24px;">
    <h1 style="margin:0; font-weight:800; font-size:1.8rem;">📊 Visualization Dashboard</h1>
    <p style="color:#6B7280; margin:4px 0 0 0;">Compare and analyze model performance across all trained algorithms</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get('evaluation_results'):
    st.warning("⚠️ No trained models yet. Go to **Model Training** to train models first.", icon="⚠️")
    if st.button("← Go to Model Training"):
        st.switch_page("pages/3_Model_Training.py")
    st.stop()

results = st.session_state.evaluation_results
model_names = list(results.keys())

# ══════════════════════════════════════════
# Model Accuracy Comparison
# ══════════════════════════════════════════
st.markdown('<div class="section-header">🏆 Model Accuracy Comparison</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    fig = plot_accuracy_comparison(results, "Model Accuracy Comparison")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Best model highlight
    best_model = max(results.items(), key=lambda x: x[1]['accuracy'])
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0,200,83,0.1), rgba(0,200,83,0.02));
                border: 1px solid rgba(0,200,83,0.3); border-radius: 14px; padding: 24px; text-align: center;">
        <div style="font-size: 2.5rem;">🏆</div>
        <div style="color: #00C853; font-weight: 700; font-size: 1rem; margin-top: 8px;">BEST MODEL</div>
        <div style="color: #E0E0E0; font-weight: 800; font-size: 1.4rem; margin-top: 4px;">
            {best_model[0]}
        </div>
        <div style="color: #00C853; font-weight: 700; font-size: 2rem; margin-top: 8px;">
            {best_model[1]['accuracy']*100:.2f}%
        </div>
        <div style="color: #6B7280; font-size: 0.85rem; margin-top: 4px;">accuracy</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# Comprehensive Metrics Table
# ══════════════════════════════════════════
st.markdown('<div class="section-header">📋 Metrics Comparison Table</div>', unsafe_allow_html=True)

metrics_data = []
for name, res in results.items():
    row = {
        'Model': f"{ALGORITHMS.get(name, {}).get('icon', '🤖')} {name}",
        'Accuracy': f"{res['accuracy']*100:.2f}%",
        'Precision': f"{res['precision_weighted']*100:.2f}%",
        'Recall': f"{res['recall_weighted']*100:.2f}%",
        'F1-Score': f"{res['f1_weighted']*100:.2f}%",
        'ROC AUC': f"{res.get('roc_auc', 0)*100:.2f}%" if res.get('roc_auc') else "N/A",
        'Train Time': f"{res.get('training_time', 0):.3f}s",
    }
    if 'cv' in res:
        row['CV Score'] = f"{res['cv']['mean']*100:.2f}% ± {res['cv']['std']*100:.2f}%"
    metrics_data.append(row)

st.dataframe(pd.DataFrame(metrics_data), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════
# Side-by-side Comparisons
# ══════════════════════════════════════════
st.markdown('<div class="section-header">🔄 Side-by-Side Comparison</div>', unsafe_allow_html=True)

if len(model_names) >= 2:
    comp_cols = st.columns(2)
    with comp_cols[0]:
        model_a = st.selectbox("Model A", model_names, index=0, key="comp_a")
    with comp_cols[1]:
        model_b = st.selectbox("Model B", model_names,
                               index=min(1, len(model_names)-1), key="comp_b")

    cmp1, cmp2 = st.columns(2)
    with cmp1:
        st.markdown(f"**{ALGORITHMS.get(model_a, {}).get('icon', '🤖')} {model_a}**")
        fig_a = plot_confusion_matrix(
            results[model_a]['confusion_matrix'],
            results[model_a]['label_names'],
            title=f"{model_a}"
        )
        st.plotly_chart(fig_a, use_container_width=True)
    with cmp2:
        st.markdown(f"**{ALGORITHMS.get(model_b, {}).get('icon', '🤖')} {model_b}**")
        fig_b = plot_confusion_matrix(
            results[model_b]['confusion_matrix'],
            results[model_b]['label_names'],
            title=f"{model_b}"
        )
        st.plotly_chart(fig_b, use_container_width=True)

    # Radar comparison
    st.markdown("##### Performance Radar Comparison")
    categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score']

    fig_radar = go.Figure()
    for name, color in zip([model_a, model_b], [COLORS["primary"], COLORS["success"]]):
        r = results[name]
        values = [r['accuracy'], r['precision_weighted'], r['recall_weighted'], r['f1_weighted']]
        values.append(values[0])
        fig_radar.add_trace(go.Scatterpolar(
            r=values, theta=categories + [categories[0]],
            fill='toself', name=name, line=dict(color=color, width=2)
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")
        ),
        title="Performance Radar — Head to Head",
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ══════════════════════════════════════════
# Feature Importance Comparison
# ══════════════════════════════════════════
st.markdown('<div class="section-header">🎯 Feature Importance</div>', unsafe_allow_html=True)

fi_model = st.selectbox("Select model for feature importance", model_names, key="fi_select")
fi = results[fi_model].get('feature_importance')
if fi is not None:
    top_n = st.slider("Top N features", 5, min(30, len(fi)), 15)
    fig = plot_feature_importance(fi, top_n=top_n, title=f"{fi_model} — Top {top_n} Features")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Feature importance not available for this algorithm.")

# ══════════════════════════════════════════
# Per-Class Metrics
# ══════════════════════════════════════════
st.markdown('<div class="section-header">📈 Per-Class Performance</div>', unsafe_allow_html=True)

pcm_model = st.selectbox("Select model", model_names, key="pcm_select")
fig_pcm = plot_per_class_metrics(
    results[pcm_model]['classification_report'],
    results[pcm_model]['label_names']
)
st.plotly_chart(fig_pcm, use_container_width=True)

# ROC Curve
if results[pcm_model].get('roc_curve'):
    fig_roc = plot_roc_curve(
        results[pcm_model]['roc_curve']['fpr'],
        results[pcm_model]['roc_curve']['tpr'],
        results[pcm_model].get('roc_auc', 0),
        title=f"{pcm_model} — ROC Curve"
    )
    st.plotly_chart(fig_roc, use_container_width=True)
