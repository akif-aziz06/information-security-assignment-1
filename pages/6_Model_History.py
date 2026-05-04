"""
Page 6: Model History
Track all training runs with metrics, timestamps, and comparisons.
"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

st.set_page_config(page_title="Model History • SecureNet IDS", page_icon="📜", layout="wide")

st.markdown("""
<div style="border-left: 4px solid #1B6EF3; padding-left: 14px; margin-bottom: 24px;">
    <h1 style="margin:0; font-weight:800; font-size:1.8rem;">📜 Model History</h1>
    <p style="color:#6B7280; margin:4px 0 0 0;">Track all training runs and model performance over time</p>
</div>
""", unsafe_allow_html=True)

history = st.session_state.get('model_history', [])

if not history:
    st.info("No training history yet. Train models to see results here.", icon="📜")
    if st.button("← Go to Model Training"):
        st.switch_page("pages/3_Model_Training.py")
    st.stop()

df_history = pd.DataFrame(history)

# Summary stats
st.markdown('<div class="section-header">📊 Training Summary</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Runs", len(df_history))
c2.metric("Best Accuracy", f"{df_history['accuracy'].max()*100:.2f}%")
c3.metric("Best Model", df_history.loc[df_history['accuracy'].idxmax(), 'algorithm'])
c4.metric("Avg F1-Score", f"{df_history['f1'].mean()*100:.2f}%")

# History table
st.markdown('<div class="section-header">📋 Training History</div>', unsafe_allow_html=True)

display_df = df_history.copy()
display_df['accuracy'] = (display_df['accuracy'] * 100).round(2).astype(str) + '%'
display_df['precision'] = (display_df['precision'] * 100).round(2).astype(str) + '%'
display_df['recall'] = (display_df['recall'] * 100).round(2).astype(str) + '%'
display_df['f1'] = (display_df['f1'] * 100).round(2).astype(str) + '%'
display_df['training_time'] = display_df['training_time'].round(3).astype(str) + 's'

st.dataframe(
    display_df.rename(columns={
        'timestamp': 'Timestamp', 'algorithm': 'Algorithm',
        'accuracy': 'Accuracy', 'precision': 'Precision',
        'recall': 'Recall', 'f1': 'F1-Score',
        'training_time': 'Train Time', 'dataset': 'Dataset',
        'n_features': 'Features'
    }),
    use_container_width=True,
    hide_index=True
)

# Clear history
st.markdown("---")
if st.button("🗑️ Clear History", type="secondary"):
    st.session_state.model_history = []
    st.rerun()
