"""
Page 5: Predictions — Real-Time Threat Detection
Manual input and batch CSV predictions with trained models.
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.model_training import ALGORITHMS

st.set_page_config(page_title="Predictions • SecureNet IDS", page_icon="🎯", layout="wide")

st.markdown("""
<div style="border-left: 4px solid #1B6EF3; padding-left: 14px; margin-bottom: 24px;">
    <h1 style="margin:0; font-weight:800; font-size:1.8rem;">🎯 Real-Time Threat Detection</h1>
    <p style="color:#6B7280; margin:4px 0 0 0;">Make predictions on new network traffic using trained models</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get('trained_models'):
    st.warning("⚠️ No trained models available. Train models first.", icon="⚠️")
    if st.button("← Go to Model Training"):
        st.switch_page("pages/3_Model_Training.py")
    st.stop()

models = st.session_state.trained_models
results = st.session_state.evaluation_results
prep_info = st.session_state.preprocessing_info
feature_names = prep_info['feature_names']

# Model selector
selected_model_name = st.selectbox(
    "🤖 Select Model for Predictions",
    list(models.keys()),
    format_func=lambda x: f"{ALGORITHMS.get(x, {}).get('icon', '🤖')} {x} — Accuracy: {results[x]['accuracy']*100:.2f}%"
)
model = models[selected_model_name]

# ══════════════════════════════════════════
# Tab Layout
# ══════════════════════════════════════════
tab1, tab2 = st.tabs(["✏️ Manual Input", "📁 Batch Prediction (CSV)"])

with tab1:
    st.markdown("##### Enter Network Traffic Features")
    st.caption(f"Model expects {len(feature_names)} features. Fill in values below:")

    # Create input form dynamically based on features
    n_cols = 4
    input_values = {}

    cols = st.columns(n_cols)
    for i, feat in enumerate(feature_names):
        with cols[i % n_cols]:
            val = st.number_input(
                feat, value=0.0, format="%.4f",
                key=f"manual_{feat}",
                help=f"Feature: {feat}"
            )
            input_values[feat] = val

    if st.button("🔮 Predict", use_container_width=True, type="primary"):
        input_df = pd.DataFrame([input_values])

        # Apply scaling if available
        scaler = prep_info.get('scaler')
        if scaler:
            numeric_cols = input_df.select_dtypes(include=[np.number]).columns
            input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

        prediction = model.predict(input_df)
        pred_label = prediction[0]

        # Decode label
        target_encoder = prep_info.get('target_encoder')
        if target_encoder:
            pred_label = target_encoder.inverse_transform([pred_label])[0]

        # Confidence
        confidence = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(input_df)
            confidence = proba.max() * 100

        # Display result
        is_attack = str(pred_label).upper() not in ['BENIGN', 'NORMAL', '0', 'LEGITIMATE']

        if is_attack:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255,23,68,0.15), rgba(255,23,68,0.05));
                        border: 2px solid rgba(255,23,68,0.5); border-radius: 14px; padding: 24px;
                        text-align: center; margin-top: 16px;">
                <div style="font-size: 3rem;">🚨</div>
                <div style="color: #FF1744; font-weight: 800; font-size: 1.5rem; margin-top: 8px;">
                    THREAT DETECTED
                </div>
                <div style="color: #E0E0E0; font-weight: 600; font-size: 1.2rem; margin-top: 4px;">
                    Classification: {pred_label}
                </div>
                {"<div style='color: #FF8A80; margin-top: 8px;'>Confidence: " + f"{confidence:.1f}%" + "</div>" if confidence else ""}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0,200,83,0.15), rgba(0,200,83,0.05));
                        border: 2px solid rgba(0,200,83,0.5); border-radius: 14px; padding: 24px;
                        text-align: center; margin-top: 16px;">
                <div style="font-size: 3rem;">✅</div>
                <div style="color: #00C853; font-weight: 800; font-size: 1.5rem; margin-top: 8px;">
                    NORMAL TRAFFIC
                </div>
                <div style="color: #E0E0E0; font-weight: 600; font-size: 1.2rem; margin-top: 4px;">
                    Classification: {pred_label}
                </div>
                {"<div style='color: #A5D6A7; margin-top: 8px;'>Confidence: " + f"{confidence:.1f}%" + "</div>" if confidence else ""}
            </div>
            """, unsafe_allow_html=True)

        # Show all model predictions
        if len(models) > 1:
            st.markdown("##### All Model Predictions")
            all_preds = {}
            for mn, m in models.items():
                p = m.predict(input_df)[0]
                if target_encoder:
                    p = target_encoder.inverse_transform([p])[0]
                conf = ""
                if hasattr(m, 'predict_proba'):
                    conf = f" ({m.predict_proba(input_df).max()*100:.1f}%)"
                all_preds[mn] = f"{p}{conf}"

            pred_df = pd.DataFrame([all_preds]).T
            pred_df.columns = ['Prediction']
            st.dataframe(pred_df, use_container_width=True)

with tab2:
    st.markdown("##### Upload CSV for Batch Prediction")
    st.caption("Upload a CSV file with the same features as the training data (without the label column).")

    batch_file = st.file_uploader("Upload CSV", type=["csv"], key="batch_upload")

    if batch_file is not None:
        batch_df = pd.read_csv(batch_file)
        batch_df.columns = batch_df.columns.str.strip()

        st.markdown(f"**Loaded:** {len(batch_df)} rows × {len(batch_df.columns)} columns")
        st.dataframe(batch_df.head(), use_container_width=True)

        if st.button("🔮 Predict Batch", use_container_width=True, type="primary"):
            with st.spinner("Running predictions..."):
                try:
                    # Ensure columns match
                    missing_cols = set(feature_names) - set(batch_df.columns)
                    extra_cols = set(batch_df.columns) - set(feature_names)

                    if missing_cols:
                        st.warning(f"⚠️ Missing features: {missing_cols}")

                    # Encode categorical columns if needed
                    label_encoders = prep_info.get('label_encoders', {})
                    for col, le in label_encoders.items():
                        if col in batch_df.columns:
                            batch_df[col] = le.transform(batch_df[col].astype(str))

                    # Select only needed features
                    pred_df = batch_df[[c for c in feature_names if c in batch_df.columns]]

                    # Scale
                    scaler = prep_info.get('scaler')
                    if scaler:
                        numeric_cols = pred_df.select_dtypes(include=[np.number]).columns
                        pred_df[numeric_cols] = scaler.transform(pred_df[numeric_cols])

                    predictions = model.predict(pred_df)
                    target_encoder = prep_info.get('target_encoder')
                    if target_encoder:
                        predictions = target_encoder.inverse_transform(predictions)

                    result_df = batch_df.copy()
                    result_df['Prediction'] = predictions

                    if hasattr(model, 'predict_proba'):
                        probas = model.predict_proba(pred_df)
                        result_df['Confidence'] = (probas.max(axis=1) * 100).round(2)

                    st.success(f"✅ Predictions complete for {len(result_df)} samples!")

                    # Summary
                    pred_dist = pd.Series(predictions).value_counts()
                    st.markdown("##### Prediction Summary")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.dataframe(pred_dist.reset_index().rename(
                            columns={'index': 'Class', 0: 'Count'}), use_container_width=True)
                    with c2:
                        n_attacks = sum(1 for p in predictions if str(p).upper() not in ['BENIGN', 'NORMAL', '0'])
                        st.metric("🚨 Threats Detected", f"{n_attacks} / {len(predictions)}")
                        st.metric("Detection Rate", f"{n_attacks/len(predictions)*100:.1f}%")

                    st.markdown("##### Full Results")
                    st.dataframe(result_df, use_container_width=True, height=400)

                    # Download
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results CSV",
                        csv,
                        file_name="ids_predictions.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"❌ Prediction error: {str(e)}")
