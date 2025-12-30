"""Ingredient Ordering AI - Main Streamlit Application."""
import streamlit as st
import pandas as pd
from datetime import datetime
from model_utils import get_season, TEMPERATURE_CATEGORIES, get_temperature_category
from data_loader import load_data
from data_filter import filter_by_week
from weather_service import fetch_weather_data
from model_trainer import train_model, predict_orders


def main():
    st.title('🥗 Ingredient Ordering AI')
    st.markdown("Use this tool to predict how many boxes of ingredients you need to order.")

    df = load_data()
    model = train_model(df)

    st.header("Historical Data")
    preview_df = filter_by_week(df)
    st.dataframe(preview_df)

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
            prediction = predict_orders(
                model, season, weather, temperature_category,
                is_long_weekend, is_promotion, is_holiday
            )

            ingredients = ['Tomato', 'Green Pepper', 'Lettuce', 'Cucumber']

            st.success("Recommended Orders:")

            cols = st.columns(4)
            for i, ingredient in enumerate(ingredients):
                with cols[i]:
                    st.metric(label=f"{ingredient} Boxes", value=int(round(prediction[i])))
                    st.caption(f"Raw: {prediction[i]:.2f}")


if __name__ == '__main__':
    main()
