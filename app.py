import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime
from model_utils import get_season, get_temperature_category

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('tomato_sales_history.csv')
    return df

# Train model
@st.cache_resource
def train_model(df):
    X = df[['Season', 'Weather', 'Temperature', 'Long_Weekend', 'Promotion', 'Holiday']]
    y = df['Boxes_Ordered']

    # Note: Categorical features must match what is in the CSV and what is produced by inputs
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

def main():
    st.title('🍅 Tomato Ordering AI')
    st.markdown("Use this tool to predict how many boxes of tomatoes you need to order.")

    df = load_data()
    model = train_model(df)

    st.header("Historical Data")
    st.dataframe(df.tail(10))

    st.header("Predict Order")

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date", datetime.now())

        # Automatically calculate season
        season = get_season(date)
        st.write(f"Season: **{season}**")

        weather = st.selectbox("Weather", ['Sunny', 'Cloudy', 'Rainy', 'Snowy'])

        # User inputs numerical temperature
        temperature_c = st.number_input("Temperature (°C)", value=15.0, step=0.5)
        # Convert to category for model
        temperature_category = get_temperature_category(temperature_c)
        st.write(f"Temperature Category: **{temperature_category}**")

    with col2:
        is_long_weekend = st.checkbox("Long Weekend?")
        is_promotion = st.checkbox("Promotion?")
        is_holiday = st.checkbox("Holiday?")

    if st.button("Predict"):
        input_data = pd.DataFrame({
            'Season': [season],
            'Weather': [weather],
            'Temperature': [temperature_category],
            'Long_Weekend': [is_long_weekend],
            'Promotion': [is_promotion],
            'Holiday': [is_holiday]
        })

        prediction = model.predict(input_data)[0]
        st.success(f"Recommended Order: {int(round(prediction))} boxes")
        st.info(f"Raw prediction: {prediction:.2f}")

if __name__ == '__main__':
    main()
