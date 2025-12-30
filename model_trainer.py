"""Model training module."""
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


@st.cache_resource
def train_model(df):
    """
    Train a RandomForest model to predict ingredient box orders.
    
    Args:
        df: DataFrame with historical sales data
    
    Returns:
        tuple: (Trained scikit-learn Pipeline model, dict of metrics)
    """
    X = df[['Season', 'Weather', 'Temperature', 'Long_Weekend', 'Promotion', 'Holiday']]
    # Predict all ingredient box counts
    y = df[['Tomato_Boxes', 'Green_Pepper_Boxes', 'Lettuce_Boxes', 'Cucumber_Boxes']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Categorical features must match what is in the CSV and what is produced by inputs
    categorical_features = ['Season', 'Weather', 'Temperature']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {}
    target_names = ['Tomato', 'Green Pepper', 'Lettuce', 'Cucumber']

    # Overall metrics
    metrics['overall_mae'] = mean_absolute_error(y_test, y_pred)
    metrics['overall_r2'] = r2_score(y_test, y_pred)

    # Per-target metrics
    mae_per_target = mean_absolute_error(y_test, y_pred, multioutput='raw_values')
    r2_per_target = r2_score(y_test, y_pred, multioutput='raw_values')

    for i, target in enumerate(target_names):
        metrics[f'{target}_mae'] = mae_per_target[i]
        metrics[f'{target}_r2'] = r2_per_target[i]

    return model, metrics


def predict_orders(model, season, weather, temperature, is_long_weekend, is_promotion, is_holiday):
    """
    Predict ingredient box orders using the trained model.
    
    Args:
        model: Trained model
        season: Season string
        weather: Weather category string
        temperature: Temperature category string
        is_long_weekend: Boolean
        is_promotion: Boolean
        is_holiday: Boolean
    
    Returns:
        Array of predictions [Tomato, Green Pepper, Lettuce, Cucumber]
    """
    input_data = pd.DataFrame({
        'Season': [season],
        'Weather': [weather],
        'Temperature': [temperature],
        'Long_Weekend': [is_long_weekend],
        'Promotion': [is_promotion],
        'Holiday': [is_holiday]
    })

    prediction = model.predict(input_data)[0]
    return prediction
