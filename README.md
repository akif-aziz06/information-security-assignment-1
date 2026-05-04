# 🛡️ SecureNet IDS — AI-Powered Intrusion Detection System

> **CLO4 IDS ML Solution** — Machine Learning-based Network Intrusion Detection System with real-time threat classification.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-orange.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1-green.svg)

---

## 📋 Project Overview

**Course:** Information Security  
**CLO:** 4 — Create solutions to real-life scenarios using different security related tools  
**Organization:** SecureNet Corp. (Simulated Scenario)

As a security analyst at SecureNet Corp., this project explores the viability of **Machine Learning as a tool to augment existing Network Intrusion Detection Systems (NIDS)**. The solution automatically classifies network traffic as **normal** or **malicious** using trained ML models, providing real-time threat detection capabilities.

### 🎯 Objective

Design, develop, and evaluate a proof-of-concept ML model that can automatically classify network traffic, supporting security analysts in identifying DDoS attacks, brute-force attempts, web attacks, and other network intrusions.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Dashboard** | Dataset overview with class distribution and quick statistics |
| 🔬 **Data Explorer** | EDA with statistics, distributions, correlations, and data quality reports |
| 🏋️ **Model Training** | Multi-algorithm training with hyperparameter tuning and cross-validation |
| 📈 **Visualizations** | Confusion matrices, ROC curves, feature importance, radar charts |
| 🎯 **Predictions** | Manual input and batch CSV prediction with threat alerts |
| 📜 **Model History** | Track all training runs and compare performance over time |
| 🔒 **Security Analysis** | Automated threat assessment with actionable security insights |

### 🤖 Supported Algorithms

- 🌲 **Random Forest** — Ensemble method for complex feature relationships
- 🌳 **Decision Tree** — Interpretable classification rules
- 🔍 **K-Nearest Neighbors** — Instance-based threat detection
- 🚀 **XGBoost** — High-performance gradient boosting
- 📊 **Naive Bayes** — Fast probabilistic baseline
- 📈 **Logistic Regression** — Linear binary classification

---

## 📂 Dataset Setup

This project supports multiple publicly available IDS datasets:

### Recommended: CIC-IDS2017
1. Visit [CIC-IDS2017 Dataset](https://www.unb.ca/cic/datasets/ids-2017.html)
2. Download the CSV files (e.g., `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`)
3. Upload via the Streamlit dashboard

### Alternative: UNSW-NB15
1. Visit [UNSW-NB15 Dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
2. Download the CSV files
3. Upload via the Streamlit dashboard

### Quick Start: Sample Data
Click **"🧪 Generate Sample Data"** in the dashboard to create a synthetic IDS dataset with 5,000 records and 5 traffic classes (BENIGN, DDoS, PortScan, BruteForce, WebAttack).

---

## 🚀 How to Run

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/CLO4-IDS-ML-Solution.git
cd CLO4-IDS-ML-Solution

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🔄 Workflow

```
1. Upload Dataset → 2. Explore Data (EDA) → 3. Train Models → 4. Evaluate → 5. Predict
```

1. **Upload** a CSV dataset or generate sample data
2. **Explore** the data with statistics, distributions, and correlations
3. **Configure** preprocessing (scaling, missing value handling, train/test split)
4. **Select** and configure ML algorithms with hyperparameters
5. **Train** models and evaluate with accuracy, precision, recall, F1, ROC AUC
6. **Analyze** security implications (attack recall, false positive rates)
7. **Predict** on new traffic (manual input or batch CSV upload)

---

## 📊 Results Summary

The system evaluates models using security-critical metrics:

- **Overall Accuracy** — General classification performance
- **Precision & Recall** — Per-class attack detection rates
- **F1-Score** — Harmonic mean of precision and recall
- **ROC AUC** — Discrimination capability
- **Confusion Matrix** — Detailed error analysis
- **Security Analysis** — Automated threat assessment with actionable insights

> **Key Insight:** High recall for attack classes is crucial to avoid missing real attacks. The security analysis module highlights classes with low recall as critical security risks.

---

## 🗂️ Project Structure

```
CLO4-IDS-ML-Solution/
├── app.py                      # Main Streamlit application (Dashboard)
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml             # Streamlit theme configuration
├── pages/
│   ├── 2_Data_Explorer.py      # EDA and data quality analysis
│   ├── 3_Model_Training.py     # Model training and evaluation
│   ├── 4_Visualizations.py     # Performance visualization dashboard
│   ├── 5_Predictions.py        # Real-time threat detection
│   ├── 6_Model_History.py      # Training history tracker
│   └── 7_Settings.py           # Configuration and references
├── utils/
│   ├── __init__.py
│   ├── data_processing.py      # Data loading, cleaning, preprocessing
│   ├── model_training.py       # Model creation, training, evaluation
│   └── visualization.py        # Plotly chart utilities
├── saved_models/               # Persisted trained models (auto-created)
└── README.md
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.45 |
| **ML Framework** | scikit-learn 1.6, XGBoost 2.1 |
| **Data Processing** | pandas 2.2, numpy 1.26 |
| **Visualization** | Plotly 6.0, Matplotlib, Seaborn |
| **Model Persistence** | joblib |

---

## 👤 Author

**Muhammad Akif Aziz**  
Bahria University Lahore Campus  
8th Semester — Information Security  

---

## 📜 License

This project is developed for academic purposes as part of the Information Security course (CLO4).