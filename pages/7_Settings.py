"""
Page 7: Settings
Application configuration and about information.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

st.set_page_config(page_title="Settings • SecureNet IDS", page_icon="⚙️", layout="wide")

st.markdown("""
<div style="border-left: 4px solid #1B6EF3; padding-left: 14px; margin-bottom: 24px;">
    <h1 style="margin:0; font-weight:800; font-size:1.8rem;">⚙️ Settings</h1>
    <p style="color:#6B7280; margin:4px 0 0 0;">Application configuration and project information</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["ℹ️ About", "🔧 Configuration", "📚 References"])

with tab1:
    st.markdown("""
    ### 🛡️ SecureNet IDS — AI-Powered Intrusion Detection System

    **Course:** Information Security
    **CLO:** 4 — Create solutions to real-life scenarios using different security related tools

    ---

    #### 📋 Project Overview

    This application is a proof-of-concept Machine Learning-based Network Intrusion Detection System (NIDS)
    designed to automatically classify network traffic as **normal** or **malicious**.

    The system supports multiple ML algorithms and provides:
    - **Data Exploration** — EDA with statistics, distributions, correlations
    - **Model Training** — Multi-algorithm training with hyperparameter tuning
    - **Visualizations** — Confusion matrices, ROC curves, feature importance
    - **Real-Time Predictions** — Manual and batch prediction capabilities
    - **Security Analysis** — Automated threat assessment with actionable insights

    ---

    #### 🛠️ Technology Stack

    | Component | Technology |
    |-----------|-----------|
    | Frontend | Streamlit |
    | ML Framework | scikit-learn, XGBoost |
    | Data Processing | pandas, numpy |
    | Visualization | Plotly, Matplotlib, Seaborn |
    | Model Persistence | joblib |

    ---

    #### 🤖 Supported Algorithms

    | Algorithm | Best For |
    |-----------|----------|
    | Random Forest | Complex feature relationships |
    | Decision Tree | Interpretable classification rules |
    | K-Nearest Neighbors | Instance-based detection |
    | XGBoost | High-performance classification |
    | Naive Bayes | Fast baseline predictions |
    | Logistic Regression | Binary classification |
    """)

with tab2:
    st.markdown("### Application Configuration")

    st.markdown("##### Session State")
    c1, c2, c3 = st.columns(3)
    c1.metric("Dataset Loaded", "✅" if st.session_state.get('dataset') is not None else "❌")
    c2.metric("Models Trained", len(st.session_state.get('trained_models', {})))
    c3.metric("History Entries", len(st.session_state.get('model_history', [])))

    st.markdown("---")

    if st.button("🗑️ Clear All Session Data", type="secondary"):
        for key in ['dataset', 'dataset_name', 'label_column', 'preprocessed',
                     'trained_models', 'evaluation_results', 'model_history', 'preprocessing_info']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Session cleared!")
        st.rerun()

with tab3:
    st.markdown("""
    ### 📚 References & Resources

    #### Datasets
    1. **CIC-IDS2017** — [Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/ids-2017.html)
       - Contains realistic DDoS, Brute-Force, Web Attack, and Infiltration traffic
    2. **UNSW-NB15** — [UNSW Sydney](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
       - Modern hybrid dataset with 9 attack families and 49 features
    3. **NSL-KDD** — [UNB NSL-KDD](https://www.unb.ca/cic/datasets/nsl.html)
       - Improved version of KDD Cup 99 with balanced class distribution

    #### Key Papers
    - Sharafaldin, I., et al. (2018). "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization."
    - Moustafa, N., & Slay, J. (2015). "UNSW-NB15: a comprehensive data set for network intrusion detection systems."

    #### Libraries
    - [scikit-learn Documentation](https://scikit-learn.org/stable/)
    - [XGBoost Documentation](https://xgboost.readthedocs.io/)
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [Plotly Documentation](https://plotly.com/python/)
    """)
