"""Model training module."""
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


@st.cache_resource
def train_model(df):
    """
    Train a RandomForest model to predict ingredient box orders.
    
    Args:
        df: DataFrame with historical sales data
    
    Returns:
        Trained scikit-learn Pipeline model
    """
    X = df[['Season', 'Weather', 'Temperature', 'Long_Weekend', 'Promotion', 'Holiday']]
    # Predict all ingredient box counts
    y = df[['Tomato_Boxes', 'Green_Pepper_Boxes', 'Lettuce_Boxes', 'Cucumber_Boxes']]

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

    model.fit(X, y)
    return model


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
