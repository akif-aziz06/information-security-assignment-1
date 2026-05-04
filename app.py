"""
SecureNet IDS — AI-Powered Intrusion Detection System
Main Streamlit Application Entry Point
"""
import streamlit as st

# ── Page Config ──
st.set_page_config(
    page_title="SecureNet IDS • AI-Powered Intrusion Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #111827 100%);
    border-right: 1px solid rgba(27, 110, 243, 0.15);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #E0E0E0;
}

/* ── Metric Cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a1f2e 0%, #141929 100%);
    border: 1px solid rgba(27, 110, 243, 0.2);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(27, 110, 243, 0.15);
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1B6EF3 0%, #6C63FF 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 28px;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(27, 110, 243, 0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(27, 110, 243, 0.5);
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(26, 31, 46, 0.5);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1B6EF3 0%, #6C63FF 100%);
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(27, 110, 243, 0.15);
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: rgba(26, 31, 46, 0.6);
    border-radius: 10px;
    font-weight: 600;
}

/* ── Selectbox / Inputs ── */
.stSelectbox, .stMultiSelect, .stTextInput, .stNumberInput {
    border-radius: 10px;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(27, 110, 243, 0.3);
    border-radius: 12px;
    padding: 10px;
    transition: border-color 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(27, 110, 243, 0.6);
}

/* ── Success / Error / Warning ── */
.stAlert {
    border-radius: 10px;
}

/* ── Progress bars ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #1B6EF3, #6C63FF);
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0a1628 0%, #1a1f3e 50%, #0a1628 100%);
    border: 1px solid rgba(27, 110, 243, 0.2);
    border-radius: 16px;
    padding: 40px;
    text-align: center;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(27, 110, 243, 0.08) 0%, transparent 50%);
    animation: pulse 6s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}
.hero-banner h1 {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #1B6EF3, #6C63FF, #00B0FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.hero-banner p {
    color: #9CA3AF;
    font-size: 1.05rem;
}

/* ── Stat card ── */
.stat-card {
    background: linear-gradient(135deg, #1a1f2e 0%, #141929 100%);
    border: 1px solid rgba(27, 110, 243, 0.15);
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(27, 110, 243, 0.12);
}
.stat-card .stat-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #1B6EF3, #00B0FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-card .stat-label {
    color: #9CA3AF;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* ── Section header ── */
.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #E0E0E0;
    border-left: 4px solid #1B6EF3;
    padding-left: 14px;
    margin: 28px 0 16px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Initialize Session State ──
if 'dataset' not in st.session_state:
    st.session_state.dataset = None
if 'dataset_name' not in st.session_state:
    st.session_state.dataset_name = None
if 'label_column' not in st.session_state:
    st.session_state.label_column = None
if 'preprocessed' not in st.session_state:
    st.session_state.preprocessed = None
if 'trained_models' not in st.session_state:
    st.session_state.trained_models = {}
if 'evaluation_results' not in st.session_state:
    st.session_state.evaluation_results = {}
if 'model_history' not in st.session_state:
    st.session_state.model_history = []
if 'preprocessing_info' not in st.session_state:
    st.session_state.preprocessing_info = None

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 8px 0;">
        <span style="font-size:2.5rem;">🛡️</span>
        <h2 style="margin:4px 0; font-weight:800;
                   background: linear-gradient(135deg, #1B6EF3, #00B0FF);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;">SecureNet IDS</h2>
        <p style="color:#6B7280; font-size:0.82rem; margin:0;">
            AI-Powered Intrusion Detection<br/>v2.0 • Streamlit
        </p>
    </div>
    <hr style="border-color: rgba(27,110,243,0.15); margin: 12px 0;">
    """, unsafe_allow_html=True)

    # Dataset status
    if st.session_state.dataset is not None:
        df = st.session_state.dataset
        st.markdown(f"""
        <div style="background: rgba(27,110,243,0.08); border: 1px solid rgba(27,110,243,0.2);
                    border-radius: 10px; padding: 12px; margin-bottom: 12px;">
            <div style="color: #1B6EF3; font-weight: 600; font-size: 0.8rem;">📊 CURRENT DATASET</div>
            <div style="color: #E0E0E0; font-weight: 600; margin-top: 4px;">{st.session_state.dataset_name}</div>
            <div style="color: #6B7280; font-size: 0.78rem; margin-top: 4px;">
                Rows: {len(df):,} • Features: {len(df.columns)} • Classes: {df[st.session_state.label_column].nunique() if st.session_state.label_column else 'N/A'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        n_models = len(st.session_state.trained_models)
        if n_models > 0:
            st.markdown(f"""
            <div style="background: rgba(0,200,83,0.08); border: 1px solid rgba(0,200,83,0.2);
                        border-radius: 10px; padding: 12px; margin-bottom: 12px;">
                <div style="color: #00C853; font-weight: 600; font-size: 0.8rem;">🤖 TRAINED MODELS</div>
                <div style="color: #E0E0E0; font-weight: 600; margin-top: 4px;">{n_models} model(s) ready</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Upload a dataset to begin →", icon="📂")

    st.markdown("""
    <hr style="border-color: rgba(27,110,243,0.15); margin: 12px 0;">
    <div style="text-align:center; padding: 8px 0; color: #4B5563; font-size: 0.72rem;">
        SecureNet Corp. • CLO4 IDS Solution<br/>
        Bahria University Lahore
    </div>
    """, unsafe_allow_html=True)


# ── Main Page — Dashboard ──
st.markdown("""
<div class="hero-banner">
    <h1>🛡️ SecureNet IDS Dashboard</h1>
    <p>AI-Powered Network Intrusion Detection System • Real-Time Threat Classification</p>
</div>
""", unsafe_allow_html=True)

from utils.data_processing import load_dataset, get_dataset_info, detect_label_column

# Dataset Upload
st.markdown('<div class="section-header">📂 Dataset Upload</div>', unsafe_allow_html=True)

col_up1, col_up2 = st.columns([3, 1])
with col_up1:
    uploaded_file = st.file_uploader(
        "Upload your IDS dataset (CSV format)",
        type=["csv"],
        help="Supported: CIC-IDS2017, UNSW-NB15, NSL-KDD, or any CSV with labeled network traffic"
    )
with col_up2:
    st.markdown("<br>", unsafe_allow_html=True)
    use_sample = st.button("🧪 Generate Sample Data", use_container_width=True)

if uploaded_file is not None:
    with st.spinner("Loading dataset..."):
        df = load_dataset(uploaded_file=uploaded_file)
        if df is not None:
            st.session_state.dataset = df
            st.session_state.dataset_name = uploaded_file.name
            label_col = detect_label_column(df)
            st.session_state.label_column = label_col
            st.success(f"✅ Loaded **{uploaded_file.name}** — {len(df):,} rows × {len(df.columns)} columns", icon="✅")

if use_sample:
    import numpy as np
    np.random.seed(42)
    n = 5000
    sample = pd.DataFrame({
        'duration': np.random.exponential(50, n),
        'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], n, p=[0.7, 0.2, 0.1]),
        'service': np.random.choice(['http', 'ftp', 'smtp', 'ssh', 'dns', 'other'], n),
        'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTR', 'SH'], n),
        'src_bytes': np.random.exponential(3000, n).astype(int),
        'dst_bytes': np.random.exponential(2000, n).astype(int),
        'count': np.random.randint(1, 600, n),
        'srv_count': np.random.randint(1, 600, n),
        'serror_rate': np.random.beta(0.5, 5, n),
        'rerror_rate': np.random.beta(0.3, 5, n),
        'same_srv_rate': np.random.beta(5, 1, n),
        'diff_srv_rate': np.random.beta(0.5, 5, n),
        'dst_host_count': np.random.randint(0, 256, n),
        'dst_host_srv_count': np.random.randint(0, 256, n),
        'dst_host_same_srv_rate': np.random.beta(5, 1, n),
        'dst_host_diff_srv_rate': np.random.beta(0.5, 5, n),
        'Label': np.random.choice(['BENIGN', 'DDoS', 'PortScan', 'BruteForce', 'WebAttack'],
                                   n, p=[0.55, 0.15, 0.12, 0.10, 0.08]),
    })
    import pandas as pd
    st.session_state.dataset = sample
    st.session_state.dataset_name = "sample_ids_data.csv"
    st.session_state.label_column = "Label"
    st.success("✅ Generated sample IDS dataset with 5,000 records and 5 traffic classes", icon="🧪")

# Dashboard stats
if st.session_state.dataset is not None:
    df = st.session_state.dataset
    info = get_dataset_info(df)

    st.markdown('<div class="section-header">📊 Dataset Overview</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total Samples", f"{info['rows']:,}")
    with c2:
        st.metric("Features", info['columns'])
    with c3:
        st.metric("Missing Values", f"{info['missing_values']:,}")
    with c4:
        st.metric("Duplicates", f"{info['duplicate_rows']:,}")
    with c5:
        lc = st.session_state.label_column
        n_classes = df[lc].nunique() if lc else "N/A"
        st.metric("Traffic Classes", n_classes)

    # Label column selector
    lc = st.session_state.label_column
    selected_label = st.selectbox(
        "🏷️ Select Target / Label Column",
        options=df.columns.tolist(),
        index=df.columns.tolist().index(lc) if lc and lc in df.columns else len(df.columns) - 1,
    )
    st.session_state.label_column = selected_label

    # Preview
    st.markdown('<div class="section-header">🔎 Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True, height=300)

    # Quick class distribution
    from utils.visualization import plot_class_distribution, plot_class_pie
    st.markdown('<div class="section-header">📈 Class Distribution</div>', unsafe_allow_html=True)
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.plotly_chart(plot_class_distribution(df[selected_label]), use_container_width=True)
    with col_d2:
        st.plotly_chart(plot_class_pie(df[selected_label]), use_container_width=True)

    # Quick actions
    st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
    qa1, qa2, qa3, qa4 = st.columns(4)
    with qa1:
        if st.button("🔬 Explore Data", use_container_width=True):
            st.switch_page("pages/2_Data_Explorer.py")
    with qa2:
        if st.button("🏋️ Train Models", use_container_width=True):
            st.switch_page("pages/3_Model_Training.py")
    with qa3:
        if st.button("📊 Visualizations", use_container_width=True):
            st.switch_page("pages/4_Visualizations.py")
    with qa4:
        if st.button("🎯 Predictions", use_container_width=True):
            st.switch_page("pages/5_Predictions.py")
else:
    # Welcome screen when no data loaded
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <p style="font-size: 4rem; margin-bottom: 16px;">📂</p>
        <h3 style="color: #E0E0E0; font-weight: 700;">Upload a Dataset to Get Started</h3>
        <p style="color: #6B7280; max-width: 600px; margin: 12px auto;">
            Upload a CSV file from a publicly available intrusion detection dataset
            (CIC-IDS2017, UNSW-NB15, NSL-KDD) or generate sample data to explore the platform.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Recommended datasets
    st.markdown('<div class="section-header">📚 Recommended Datasets</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2rem;">🌐</div>
            <div class="stat-value" style="font-size: 1.2rem;">CIC-IDS2017</div>
            <div class="stat-label">DDoS, Brute Force, Web Attacks</div>
            <p style="color: #6B7280; font-size: 0.78rem; margin-top: 8px;">
                Realistic traffic from the Canadian Institute for Cybersecurity. Contains benign + 7 attack types.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2rem;">🔒</div>
            <div class="stat-value" style="font-size: 1.2rem;">UNSW-NB15</div>
            <div class="stat-label">Fuzzers, Analysis, Backdoors, DoS</div>
            <p style="color: #6B7280; font-size: 0.78rem; margin-top: 8px;">
                Modern hybrid dataset with 9 attack families and 49 features from raw network packets.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2rem;">📡</div>
            <div class="stat-value" style="font-size: 1.2rem;">NSL-KDD</div>
            <div class="stat-label">DoS, Probe, R2L, U2R</div>
            <p style="color: #6B7280; font-size: 0.78rem; margin-top: 8px;">
                Classic benchmark dataset with improved labeling. Widely used for IDS research comparisons.
            </p>
        </div>
        """, unsafe_allow_html=True)
