"""SHAP explainer module for model interpretability."""
import shap
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


@st.cache_resource
def create_explainer(_model, _X_train):
    """
    Create a SHAP TreeExplainer for the trained Random Forest model.
    
    Args:
        _model: Trained scikit-learn Pipeline model
        _X_train: Training data (preprocessed features)
    
    Returns:
        SHAP TreeExplainer object
    """
    # Extract the regressor from the pipeline
    regressor = _model.named_steps['regressor']
    
    # Create TreeExplainer
    explainer = shap.TreeExplainer(regressor)
    return explainer


def explain_prediction(model, explainer, input_data, ingredient_index):
    """
    Generate SHAP explanation for a single prediction.
    
    Args:
        model: Trained scikit-learn Pipeline model
        explainer: SHAP TreeExplainer object
        input_data: DataFrame with single row of input features
        ingredient_index: Index of ingredient (0=Tomato, 1=Green Pepper, 2=Lettuce, 3=Cucumber)
    
    Returns:
        SHAP values for the prediction
    """
    # Preprocess input data using the pipeline's preprocessor
    preprocessor = model.named_steps['preprocessor']
    X_preprocessed = preprocessor.transform(input_data)
    
    # Get SHAP values for this input
    shap_values = explainer.shap_values(X_preprocessed)
    
    # Return SHAP values for the specific ingredient
    return shap_values[ingredient_index]


def plot_waterfall(explainer, model, input_data, ingredient_name, ingredient_index, base_value):
    """
    Create a SHAP waterfall plot showing feature contributions.
    
    Args:
        explainer: SHAP TreeExplainer object
        model: Trained scikit-learn Pipeline model
        input_data: DataFrame with single row of input features
        ingredient_name: Name of ingredient being predicted
        ingredient_index: Index of ingredient (0=Tomato, 1=Green Pepper, 2=Lettuce, 3=Cucumber)
        base_value: Expected value (base prediction) for the model
    """
    # Preprocess input data
    preprocessor = model.named_steps['preprocessor']
    X_preprocessed = preprocessor.transform(input_data)
    
    # Get SHAP values (returns array of shape (1, n_features, n_outputs) for single sample)
    shap_values = explainer.shap_values(X_preprocessed)
    
    # Create feature names after preprocessing
    feature_names = []
    # Get one-hot encoded feature names from the preprocessor
    cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out(
        input_features=['Season', 'Weather', 'Temperature']
    ).tolist()
    feature_names.extend(cat_features)
    # Add passthrough features (Long_Weekend, Promotion, Holiday)
    feature_names.extend(['Long_Weekend', 'Promotion', 'Holiday'])
    
    # Extract SHAP values for the specific ingredient and sample
    # shap_values[0] gives (n_features, n_outputs), then [:, ingredient_index] gives 1D array
    ingredient_shap = shap_values[0][:, ingredient_index]
    
    # Create SHAP explanation object
    explanation = shap.Explanation(
        values=ingredient_shap,
        base_values=base_value[ingredient_index],
        data=X_preprocessed[0],
        feature_names=feature_names
    )
    
    # Create waterfall plot
    fig = plt.figure(figsize=(10, 6))
    shap.plots.waterfall(explanation, show=False)
    
    return fig


def plot_force(explainer, model, input_data, ingredient_name, ingredient_index, base_value):
    """
    Create a SHAP force plot showing feature contributions.
    
    Args:
        explainer: SHAP TreeExplainer object
        model: Trained scikit-learn Pipeline model
        input_data: DataFrame with single row of input features
        ingredient_name: Name of ingredient being predicted
        ingredient_index: Index of ingredient
        base_value: Expected value (base prediction) for the model
    """
    # Preprocess input data
    preprocessor = model.named_steps['preprocessor']
    X_preprocessed = preprocessor.transform(input_data)
    
    # Get SHAP values (returns array of shape (1, n_features, n_outputs) for single sample)
    shap_values = explainer.shap_values(X_preprocessed)
    
    # Create feature names
    feature_names = []
    cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out(
        input_features=['Season', 'Weather', 'Temperature']
    ).tolist()
    feature_names.extend(cat_features)
    feature_names.extend(['Long_Weekend', 'Promotion', 'Holiday'])
    
    # Extract SHAP values for the specific ingredient and sample
    ingredient_shap = shap_values[0][:, ingredient_index]
    
    # Create SHAP explanation object
    explanation = shap.Explanation(
        values=ingredient_shap,
        base_values=base_value[ingredient_index],
        data=X_preprocessed[0],
        feature_names=feature_names
    )
    
    # Return the explanation object for force plot
    return explanation
