"""
Data Processing Utilities for IDS ML Solution
Handles data loading, cleaning, preprocessing, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import streamlit as st
import os


def load_dataset(uploaded_file=None, file_path=None):
    """Load dataset from uploaded file or file path."""
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, low_memory=False)
        elif file_path is not None:
            df = pd.read_csv(file_path, low_memory=False)
        else:
            return None

        # Clean column names
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None


def get_dataset_info(df):
    """Get comprehensive dataset information."""
    info = {
        "rows": len(df),
        "columns": len(df.columns),
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
        "categorical_columns": len(df.select_dtypes(include=['object']).columns),
        "column_names": list(df.columns),
        "dtypes": df.dtypes.value_counts().to_dict(),
    }
    return info


def detect_label_column(df):
    """Auto-detect the label/target column in IDS datasets."""
    common_label_names = [
        'label', 'Label', 'LABEL',
        'attack_cat', 'Attack', 'attack',
        'class', 'Class', 'CLASS',
        'target', 'Target', 'TARGET',
        'category', 'Category',
        'intrusion', 'is_attack',
        'type', 'Type',
    ]
    for col in common_label_names:
        if col in df.columns:
            return col

    # Check last column as fallback
    last_col = df.columns[-1]
    if df[last_col].nunique() < 20:
        return last_col
    return None


def preprocess_data(df, label_column, test_size=0.3, random_state=42,
                    handle_missing='drop', scaling_method='standard',
                    encode_labels=True):
    """
    Full preprocessing pipeline for IDS data.
    Returns X_train, X_test, y_train, y_test, preprocessing_info
    """
    preprocessing_info = {
        "original_shape": df.shape,
        "steps": []
    }

    df_processed = df.copy()

    # Step 1: Handle infinities
    numeric_cols = df_processed.select_dtypes(include=[np.number]).columns
    inf_count = np.isinf(df_processed[numeric_cols]).sum().sum()
    if inf_count > 0:
        df_processed.replace([np.inf, -np.inf], np.nan, inplace=True)
        preprocessing_info["steps"].append(f"Replaced {inf_count} infinite values with NaN")

    # Step 2: Handle missing values
    missing_count = df_processed.isnull().sum().sum()
    if missing_count > 0:
        if handle_missing == 'drop':
            df_processed.dropna(inplace=True)
            preprocessing_info["steps"].append(f"Dropped {missing_count} rows with missing values")
        elif handle_missing == 'mean':
            for col in numeric_cols:
                if col != label_column:
                    df_processed[col].fillna(df_processed[col].mean(), inplace=True)
            cat_cols = df_processed.select_dtypes(include=['object']).columns
            for col in cat_cols:
                if col != label_column:
                    df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
            preprocessing_info["steps"].append(f"Filled {missing_count} missing values (mean/mode)")
        elif handle_missing == 'median':
            for col in numeric_cols:
                if col != label_column:
                    df_processed[col].fillna(df_processed[col].median(), inplace=True)
            cat_cols = df_processed.select_dtypes(include=['object']).columns
            for col in cat_cols:
                if col != label_column:
                    df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
            preprocessing_info["steps"].append(f"Filled {missing_count} missing values (median/mode)")

    # Step 3: Remove duplicates
    dup_count = df_processed.duplicated().sum()
    if dup_count > 0:
        df_processed.drop_duplicates(inplace=True)
        preprocessing_info["steps"].append(f"Removed {dup_count} duplicate rows")

    # Step 4: Separate features and labels
    y = df_processed[label_column].copy()
    X = df_processed.drop(columns=[label_column])

    # Step 5: Encode categorical features
    label_encoders = {}
    categorical_cols = X.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
    if len(categorical_cols) > 0:
        preprocessing_info["steps"].append(f"Encoded {len(categorical_cols)} categorical features: {list(categorical_cols)}")

    # Step 6: Encode target labels
    target_le = None
    label_mapping = {}
    if encode_labels and y.dtype == 'object':
        target_le = LabelEncoder()
        y = pd.Series(target_le.fit_transform(y), name=label_column)
        label_mapping = dict(zip(target_le.classes_, target_le.transform(target_le.classes_)))
        preprocessing_info["steps"].append(f"Encoded target labels: {label_mapping}")

    # Step 7: Feature scaling
    scaler = None
    numeric_feature_cols = X.select_dtypes(include=[np.number]).columns
    if scaling_method == 'standard':
        scaler = StandardScaler()
        X[numeric_feature_cols] = scaler.fit_transform(X[numeric_feature_cols])
        preprocessing_info["steps"].append("Applied Standard Scaling to numeric features")
    elif scaling_method == 'minmax':
        scaler = MinMaxScaler()
        X[numeric_feature_cols] = scaler.fit_transform(X[numeric_feature_cols])
        preprocessing_info["steps"].append("Applied MinMax Scaling to numeric features")

    # Step 8: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    preprocessing_info["steps"].append(
        f"Split data: Train={len(X_train)} ({(1-test_size)*100:.0f}%), Test={len(X_test)} ({test_size*100:.0f}%)"
    )
    preprocessing_info["final_shape"] = X_train.shape
    preprocessing_info["feature_names"] = list(X.columns)
    preprocessing_info["label_mapping"] = label_mapping
    preprocessing_info["target_encoder"] = target_le
    preprocessing_info["scaler"] = scaler
    preprocessing_info["label_encoders"] = label_encoders

    return X_train, X_test, y_train, y_test, preprocessing_info


def create_binary_labels(y, normal_label='BENIGN'):
    """Convert multi-class labels to binary (Normal vs Attack)."""
    return y.apply(lambda x: 'Normal' if str(x).upper() == normal_label.upper() else 'Attack')


def get_class_distribution(y):
    """Get class distribution as a DataFrame."""
    dist = y.value_counts().reset_index()
    dist.columns = ['Class', 'Count']
    dist['Percentage'] = (dist['Count'] / dist['Count'].sum() * 100).round(2)
    return dist
