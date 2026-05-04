"""
Visualization Utilities for IDS ML Solution
"""
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


COLORS = {
    "primary": "#1B6EF3",
    "secondary": "#6C63FF",
    "success": "#00C853",
    "danger": "#FF1744",
    "warning": "#FFD600",
    "info": "#00B0FF",
    "bg_dark": "#0E1117",
    "bg_card": "#1A1F2E",
    "text": "#E0E0E0",
    "gradient": ["#1B6EF3", "#6C63FF", "#00B0FF", "#00C853", "#FFD600", "#FF6D00", "#FF1744"],
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E0E0E0", family="Inter, sans-serif"),
    margin=dict(l=40, r=40, t=50, b=40),
)


def plot_class_distribution(y, title="Class Distribution"):
    dist = y.value_counts().reset_index()
    dist.columns = ['Class', 'Count']
    fig = px.bar(dist, x='Class', y='Count', color='Class',
                 color_discrete_sequence=COLORS["gradient"], title=title,
                 text='Count')
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig.update_traces(textposition='outside')
    fig.update_xaxes(title_text="Traffic Class", gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(title_text="Number of Samples", gridcolor="rgba(255,255,255,0.1)")
    return fig


def plot_class_pie(y, title="Traffic Distribution"):
    dist = y.value_counts().reset_index()
    dist.columns = ['Class', 'Count']
    fig = px.pie(dist, values='Count', names='Class', title=title,
                 color_discrete_sequence=COLORS["gradient"],
                 hole=0.4)
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def plot_confusion_matrix(cm, labels, title="Confusion Matrix"):
    text = [[str(val) for val in row] for row in cm]
    fig = go.Figure(data=go.Heatmap(
        z=cm, x=labels, y=labels, text=text, texttemplate="%{text}",
        colorscale=[[0, '#0E1117'], [0.5, '#1B6EF3'], [1, '#FF1744']],
        showscale=True,
    ))
    fig.update_layout(
        title=title, xaxis_title="Predicted", yaxis_title="Actual",
        **PLOTLY_LAYOUT,
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.1)")
    return fig


def plot_roc_curve(fpr, tpr, auc_score, title="ROC Curve"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines',
                             name=f'Model (AUC = {auc_score:.4f})',
                             line=dict(color=COLORS["primary"], width=3)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
                             name='Random', line=dict(color='gray', dash='dash')))
    fig.update_layout(title=title, xaxis_title="False Positive Rate",
                      yaxis_title="True Positive Rate", **PLOTLY_LAYOUT)
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.1)")
    return fig


def plot_feature_importance(fi_df, top_n=15, title="Feature Importance"):
    top = fi_df.head(top_n)
    fig = px.bar(top, x='Importance', y='Feature', orientation='h',
                 color='Importance', color_continuous_scale=[[0, '#1B6EF3'], [1, '#FF1744']],
                 title=title)
    fig.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"))
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.1)")
    return fig


def plot_accuracy_comparison(model_results, title="Model Accuracy Comparison"):
    names = list(model_results.keys())
    accs = [model_results[n].get("accuracy", 0) * 100 for n in names]
    fig = px.bar(x=accs, y=names, orientation='h', title=title,
                 color=accs, color_continuous_scale=[[0, '#FF1744'], [0.5, '#FFD600'], [1, '#00C853']],
                 text=[f"{a:.1f}%" for a in accs])
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside')
    fig.update_xaxes(title_text="Accuracy (%)", range=[0, 105], gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(title_text="", gridcolor="rgba(255,255,255,0.1)")
    return fig


def plot_metrics_radar(results, model_name="Model"):
    categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    values = [
        results.get("accuracy", 0),
        results.get("precision_weighted", 0),
        results.get("recall_weighted", 0),
        results.get("f1_weighted", 0),
    ]
    values.append(values[0])
    categories.append(categories[0])
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself',
                                   name=model_name, line=dict(color=COLORS["primary"])))
    fig.update_layout(polar=dict(
        bgcolor="rgba(0,0,0,0)",
        radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.1)"),
        angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")
    ), title=f"{model_name} — Performance Radar", **PLOTLY_LAYOUT)
    return fig


def plot_correlation_heatmap(df, top_n=20):
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] > top_n:
        variance = numeric.var().sort_values(ascending=False)
        numeric = numeric[variance.head(top_n).index]
    corr = numeric.corr()
    fig = px.imshow(corr, color_continuous_scale=[[0, '#1B6EF3'], [0.5, '#0E1117'], [1, '#FF1744']],
                    title=f"Feature Correlation (Top {min(top_n, len(corr))} by Variance)")
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


def plot_feature_distributions(df, features, label_col=None, n_cols=3):
    figs = []
    for feat in features:
        if label_col and label_col in df.columns:
            fig = px.histogram(df, x=feat, color=label_col, marginal="box",
                               color_discrete_sequence=COLORS["gradient"],
                               title=f"Distribution: {feat}")
        else:
            fig = px.histogram(df, x=feat, color_discrete_sequence=[COLORS["primary"]],
                               title=f"Distribution: {feat}")
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_xaxes(gridcolor="rgba(255,255,255,0.1)")
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.1)")
        figs.append(fig)
    return figs


def plot_per_class_metrics(report, label_names):
    metrics_data = []
    for label in label_names:
        if label in report:
            metrics_data.append({
                'Class': label,
                'Precision': report[label]['precision'],
                'Recall': report[label]['recall'],
                'F1-Score': report[label]['f1-score'],
            })
    df_m = pd.DataFrame(metrics_data)
    fig = go.Figure()
    for metric, color in zip(['Precision', 'Recall', 'F1-Score'],
                              [COLORS["primary"], COLORS["success"], COLORS["secondary"]]):
        fig.add_trace(go.Bar(name=metric, x=df_m['Class'], y=df_m[metric],
                             marker_color=color, text=df_m[metric].round(3),
                             textposition='outside'))
    fig.update_layout(barmode='group', title="Per-Class Metrics",
                      **PLOTLY_LAYOUT, legend=dict(orientation="h", y=1.12))
    fig.update_xaxes(title_text="Class", gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(title_text="Score", range=[0, 1.15], gridcolor="rgba(255,255,255,0.1)")
    return fig
