import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime
import requests
import os
from model_utils import get_season, TEMPERATURE_CATEGORIES, get_temperature_category

def get_weather_category(weather_code):
    # WMO Weather interpretation codes (WW)
    if weather_code == 0:
        return 'Sunny'
    elif weather_code in [1, 2, 3, 45, 48]:
        return 'Cloudy'
    elif weather_code in [71, 73, 75, 77, 85, 86]:
        return 'Snowy'
    else:
        # Everything else is considered Rainy (Drizzle, Rain, Thunderstorm)
        return 'Rainy'

def fetch_weather_data(date):
    latitude = 49.2827
    longitude = -123.1207
    date_str = date.strftime('%Y-%m-%d')

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["weather_code", "temperature_2m_max"],
        "timezone": "auto",
        "start_date": date_str,
        "end_date": date_str
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'daily' not in data or not data['daily']['time']:
            return None, None

        weather_code = data['daily']['weather_code'][0]
        max_temp = data['daily']['temperature_2m_max'][0]

        weather_category = get_weather_category(weather_code)

        return weather_category, max_temp
    except Exception as e:
        return None, None

# Load data
@st.cache_data
def load_data():
    # Generate data if file doesn't exist
    if not os.path.exists('tomato_sales_history.csv'):
        st.info("Generating initial data file...")
        from generate_data import generate_data
        generate_data()
    
    df = pd.read_csv('tomato_sales_history.csv')
    return df

# Train model
@st.cache_resource
def train_model(df):
    X = df[['Season', 'Weather', 'Temperature', 'Long_Weekend', 'Promotion', 'Holiday']]
    # Predict all ingredient box counts
    y = df[['Tomato_Boxes', 'Green_Pepper_Boxes', 'Lettuce_Boxes', 'Cucumber_Boxes']]

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
    st.title('🥗 Ingredient Ordering AI')
    st.markdown("Use this tool to predict how many boxes of ingredients you need to order.")

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

        # Fetch weather data
        weather, max_temp = fetch_weather_data(date)

        if weather is None:
            st.warning("Weather report is not available for the selected date. Please enter manually.")
            # Fallback to manual input if weather API fails or no data
            weather = st.selectbox("Weather", ['Sunny', 'Cloudy', 'Rainy', 'Snowy'])
            temperature_category = st.selectbox("Temperature Category", TEMPERATURE_CATEGORIES)
        else:
            temperature_category = get_temperature_category(max_temp)
            st.info(f"Weather: **{weather}**")
            st.info(f"Temperature: **{max_temp}°C ({temperature_category})**")

    with col2:
        is_long_weekend = st.checkbox("Long Weekend?")
        is_promotion = st.checkbox("Promotion?")
        is_holiday = st.checkbox("Holiday?")

    if st.button("Predict"):
        if weather is None or temperature_category is None:
             st.error("Cannot predict without weather data.")
        else:
            input_data = pd.DataFrame({
                'Season': [season],
                'Weather': [weather],
                'Temperature': [temperature_category],
                'Long_Weekend': [is_long_weekend],
                'Promotion': [is_promotion],
                'Holiday': [is_holiday]
            })

            prediction = model.predict(input_data)[0]

            # Prediction is now an array of 4 values: [Tomato, Green Pepper, Lettuce, Cucumber]
            # We need to map them back to the ingredient names
            ingredients = ['Tomato', 'Green Pepper', 'Lettuce', 'Cucumber']

            st.success("Recommended Orders:")

            cols = st.columns(4)
            for i, ingredient in enumerate(ingredients):
                with cols[i]:
                    st.metric(label=f"{ingredient} Boxes", value=int(round(prediction[i])))
                    st.caption(f"Raw: {prediction[i]:.2f}")

if __name__ == '__main__':
    main()
