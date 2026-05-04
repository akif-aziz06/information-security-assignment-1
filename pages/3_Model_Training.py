"""
Page 3: Model Training
Configure, train, and evaluate ML models for intrusion detection.
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_processing import preprocess_data
from utils.model_training import (
    ALGORITHMS, get_model, train_model, evaluate_model,
    cross_validate_model, get_feature_importance, save_model,
    get_security_analysis
)
from utils.visualization import (
    plot_confusion_matrix, plot_roc_curve,
    plot_feature_importance, plot_metrics_radar, plot_per_class_metrics
)

st.set_page_config(page_title="Model Training • SecureNet IDS", page_icon="🏋️", layout="wide")

st.markdown("""
<div style="border-left: 4px solid #1B6EF3; padding-left: 14px; margin-bottom: 24px;">
    <h1 style="margin:0; font-weight:800; font-size:1.8rem;">🏋️ Model Training</h1>
    <p style="color:#6B7280; margin:4px 0 0 0;">Configure, train, and evaluate ML-based intrusion detection models</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.get('dataset') is None:
    st.warning("⚠️ No dataset loaded. Please go to **Dashboard** and upload a dataset first.", icon="⚠️")
    if st.button("← Go to Dashboard"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.dataset
label_col = st.session_state.label_column

# ══════════════════════════════════════════
# STEP 1: Preprocessing Configuration
# ══════════════════════════════════════════
st.markdown('<div class="section-header">⚙️ Preprocessing Configuration</div>', unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    test_size = st.slider("Test Split (%)", 10, 50, 30, 5) / 100
    handle_missing = st.selectbox("Handle Missing Values", ["drop", "mean", "median"])
with col_p2:
    scaling_method = st.selectbox("Feature Scaling", ["standard", "minmax", "none"])
    random_state = st.number_input("Random Seed", value=42, min_value=0)
with col_p3:
    use_cv = st.checkbox("Cross-Validation", value=True)
    cv_folds = st.slider("CV Folds", 3, 10, 5) if use_cv else 5

# Preprocess button
if st.button("🔧 Preprocess Data", use_container_width=True, type="primary"):
    with st.spinner("Preprocessing data..."):
        try:
            X_train, X_test, y_train, y_test, prep_info = preprocess_data(
                df, label_col, test_size=test_size, random_state=int(random_state),
                handle_missing=handle_missing,
                scaling_method=scaling_method if scaling_method != "none" else None,
            )
            st.session_state.preprocessed = {
                'X_train': X_train, 'X_test': X_test,
                'y_train': y_train, 'y_test': y_test,
            }
            st.session_state.preprocessing_info = prep_info
            st.success(f"✅ Preprocessed! Train: {len(X_train):,} | Test: {len(X_test):,} | Features: {X_train.shape[1]}")

            with st.expander("📋 Preprocessing Steps", expanded=True):
                for step in prep_info['steps']:
                    st.markdown(f"- {step}")
        except Exception as e:
            st.error(f"❌ Preprocessing error: {str(e)}")

if st.session_state.preprocessed is None:
    st.info("👆 Configure and run preprocessing first", icon="ℹ️")
    st.stop()

# ══════════════════════════════════════════
# STEP 2: Algorithm Selection & Configuration
# ══════════════════════════════════════════
st.markdown('<div class="section-header">🤖 Algorithm Selection</div>', unsafe_allow_html=True)

# Algorithm cards
algo_cols = st.columns(len(ALGORITHMS))
selected_algorithms = []
for i, (algo_name, algo_info) in enumerate(ALGORITHMS.items()):
    with algo_cols[i]:
        selected = st.checkbox(
            f"{algo_info['icon']} {algo_name}",
            value=(algo_name in ["Random Forest", "XGBoost"]),
            key=f"algo_{algo_name}"
        )
        if selected:
            selected_algorithms.append(algo_name)
        st.caption(algo_info["description"][:60] + "...")

if not selected_algorithms:
    st.warning("Select at least one algorithm to train.")
    st.stop()

# Algorithm-specific parameters
st.markdown('<div class="section-header">🎛️ Algorithm Configuration</div>', unsafe_allow_html=True)
algo_params = {}
param_cols = st.columns(min(3, len(selected_algorithms)))

for i, algo_name in enumerate(selected_algorithms):
    with param_cols[i % 3]:
        st.markdown(f"**{ALGORITHMS[algo_name]['icon']} {algo_name}**")
        params = {}
        for param_name, param_config in ALGORITHMS[algo_name]["params"].items():
            if param_config["type"] == "slider":
                val = st.slider(
                    param_name, param_config["min"], param_config["max"],
                    param_config["default"], param_config.get("step", 1),
                    key=f"{algo_name}_{param_name}"
                )
                params[param_name] = val
            elif param_config["type"] == "select":
                val = st.selectbox(
                    param_name, param_config["options"],
                    index=param_config["options"].index(param_config["default"]),
                    key=f"{algo_name}_{param_name}"
                )
                params[param_name] = val
        algo_params[algo_name] = params

# ══════════════════════════════════════════
# STEP 3: Train Models
# ══════════════════════════════════════════
st.markdown("---")

if st.button("🚀 Train Selected Models", use_container_width=True, type="primary"):
    data = st.session_state.preprocessed
    X_train, X_test = data['X_train'], data['X_test']
    y_train, y_test = data['y_train'], data['y_test']
    prep_info = st.session_state.preprocessing_info

    progress_bar = st.progress(0, text="Starting training...")

    for idx, algo_name in enumerate(selected_algorithms):
        progress_bar.progress(
            (idx) / len(selected_algorithms),
            text=f"Training {algo_name}..."
        )

        try:
            model = get_model(algo_name, algo_params.get(algo_name, {}))
            model, train_info = train_model(model, X_train, y_train, algo_name)

            # Evaluate
            label_names = None
            if prep_info.get('target_encoder'):
                label_names = list(prep_info['target_encoder'].classes_)
            elif prep_info.get('label_mapping'):
                label_names = list(prep_info['label_mapping'].keys())
            else:
                label_names = [str(c) for c in sorted(y_test.unique())]

            results = evaluate_model(model, X_test, y_test, label_names=label_names)
            results.update(train_info)

            # Feature importance
            fi = get_feature_importance(model, prep_info['feature_names'], algo_name)
            results['feature_importance'] = fi

            # Cross-validation
            if use_cv:
                cv_results = cross_validate_model(model, X_train, y_train, cv=cv_folds)
                results['cv'] = cv_results

            # Store results
            st.session_state.trained_models[algo_name] = model
            st.session_state.evaluation_results[algo_name] = results

            # Add to history
            st.session_state.model_history.append({
                'timestamp': train_info['timestamp'],
                'algorithm': algo_name,
                'accuracy': results['accuracy'],
                'precision': results['precision_weighted'],
                'recall': results['recall_weighted'],
                'f1': results['f1_weighted'],
                'training_time': train_info['training_time'],
                'dataset': st.session_state.dataset_name,
                'n_features': train_info['n_features'],
            })

        except Exception as e:
            st.error(f"❌ Error training {algo_name}: {str(e)}")

    progress_bar.progress(1.0, text="✅ Training complete!")
    st.success(f"🎉 Successfully trained {len(selected_algorithms)} model(s)!")
    st.balloons()

# ══════════════════════════════════════════
# STEP 4: Results Display
# ══════════════════════════════════════════
if st.session_state.evaluation_results:
    st.markdown('<div class="section-header">📊 Training Results</div>', unsafe_allow_html=True)

    # Metrics overview
    metric_cols = st.columns(len(st.session_state.evaluation_results))
    for i, (algo_name, results) in enumerate(st.session_state.evaluation_results.items()):
        with metric_cols[i]:
            st.markdown(f"**{ALGORITHMS[algo_name]['icon']} {algo_name}**")
            st.metric("Accuracy", f"{results['accuracy']*100:.2f}%")
            st.metric("Precision", f"{results['precision_weighted']*100:.2f}%")
            st.metric("Recall", f"{results['recall_weighted']*100:.2f}%")
            st.metric("F1-Score", f"{results['f1_weighted']*100:.2f}%")
            st.metric("Train Time", f"{results['training_time']:.3f}s")
            if 'cv' in results:
                st.metric("CV Score", f"{results['cv']['mean']*100:.2f}% ± {results['cv']['std']*100:.2f}%")

    # Per-model detailed view
    for algo_name, results in st.session_state.evaluation_results.items():
        with st.expander(f"📋 {algo_name} — Detailed Results", expanded=False):
            t1, t2, t3, t4 = st.tabs(["Confusion Matrix", "ROC Curve", "Feature Importance", "Security Analysis"])

            with t1:
                fig = plot_confusion_matrix(
                    results['confusion_matrix'],
                    results['label_names'],
                    title=f"{algo_name} — Confusion Matrix"
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("##### Per-Class Metrics")
                fig2 = plot_per_class_metrics(results['classification_report'], results['label_names'])
                st.plotly_chart(fig2, use_container_width=True)

            with t2:
                if results.get('roc_curve'):
                    fig = plot_roc_curve(
                        results['roc_curve']['fpr'],
                        results['roc_curve']['tpr'],
                        results.get('roc_auc', 0),
                        title=f"{algo_name} — ROC Curve"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                elif results.get('roc_auc'):
                    st.metric("ROC AUC (Weighted)", f"{results['roc_auc']:.4f}")
                else:
                    st.info("ROC curve not available for this model configuration.")

                fig_r = plot_metrics_radar(results, algo_name)
                st.plotly_chart(fig_r, use_container_width=True)

            with t3:
                fi = results.get('feature_importance')
                if fi is not None:
                    fig = plot_feature_importance(fi, top_n=15,
                                                  title=f"{algo_name} — Top 15 Features")
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(fi.head(20), use_container_width=True)
                else:
                    st.info("Feature importance not available for this algorithm.")

            with t4:
                analysis = get_security_analysis(results, results['label_names'])
                for item in analysis:
                    if item['type'] == 'critical':
                        st.error(item['message'])
                    elif item['type'] == 'warning':
                        st.warning(item['message'])
                    elif item['type'] == 'success':
                        st.success(item['message'])
                    else:
                        st.info(item['message'])

    # Save models
    st.markdown("---")
    if st.button("💾 Save All Trained Models", use_container_width=True):
        for algo_name, model in st.session_state.trained_models.items():
            path = save_model(model, algo_name.replace(" ", "_").lower())
            st.success(f"Saved {algo_name} → `{path}`")
