"""Ingredient Ordering AI - Main Streamlit Application."""
import streamlit as st
import pandas as pd
from datetime import datetime
from model_utils import get_season, TEMPERATURE_CATEGORIES, get_temperature_category
from data_loader import load_data
from data_filter import filter_by_week
from data_formatter import format_data_for_display, apply_year_highlight
from weather_service import fetch_weather_data
from model_trainer import train_model, predict_orders
from shap_explainer import create_explainer, plot_waterfall


def main():
    st.title('🥗 Ingredient Ordering AI')
    st.markdown("Use this tool to predict how many boxes of ingredients you need to order.")

    df = load_data()
    model, metrics = train_model(df)
    
    # Prepare training data for SHAP explainer
    X_train = df[['Season', 'Weather', 'Temperature', 'Long_Weekend', 'Promotion', 'Holiday']]
    explainer = create_explainer(model, X_train)

    st.header("Historical Data")
    
    # Get current week number for filtering and formatting
    current_week = datetime.now().isocalendar()[1]
    
    preview_df = filter_by_week(df, current_week)
    display_df = format_data_for_display(preview_df, current_week)
    
    # Apply styling
    styled_df = apply_year_highlight(display_df)
    st.dataframe(styled_df, hide_index=True)

    st.header("Model Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mean Absolute Error (Avg)", f"{metrics['overall_mae']:.2f}")
    with col2:
        st.metric("R² Score (Avg)", f"{metrics['overall_r2']:.2f}")

    with st.expander("Detailed Performance by Ingredient"):
        cols = st.columns(4)
        ingredients = ['Tomato', 'Green Pepper', 'Lettuce', 'Cucumber']
        for i, ingredient in enumerate(ingredients):
            with cols[i]:
                st.write(f"**{ingredient}**")
                st.write(f"MAE: {metrics[f'{ingredient}_mae']:.2f}")
                st.write(f"R²: {metrics[f'{ingredient}_r2']:.2f}")

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
            
            # SHAP Explainability Section
            st.header("Why These Predictions?")
            st.markdown("The visualizations below show how each factor influenced the recommended order quantities.")
            
            # Prepare input data for SHAP
            input_data = pd.DataFrame({
                'Season': [season],
                'Weather': [weather],
                'Temperature': [temperature_category],
                'Long_Weekend': [is_long_weekend],
                'Promotion': [is_promotion],
                'Holiday': [is_holiday]
            })
            
            # Create tabs for each ingredient
            tabs = st.tabs(ingredients)
            
            for i, (tab, ingredient) in enumerate(zip(tabs, ingredients)):
                with tab:
                    try:
                        # Get base values (expected value from model)
                        preprocessor = model.named_steps['preprocessor']
                        X_train_preprocessed = preprocessor.transform(X_train)
                        regressor = model.named_steps['regressor']
                        base_values = regressor.predict(X_train_preprocessed).mean(axis=0)
                        
                        # Create and display waterfall plot
                        fig = plot_waterfall(
                            explainer, model, input_data,
                            ingredient, i, base_values
                        )
                        st.pyplot(fig)
                        
                        st.markdown(f"""
                        **How to read this chart:**
                        - The chart shows how different factors push the predicted {ingredient} boxes up (red) or down (blue)
                        - Start from the base value (expected average) on the left
                        - Each factor adds or subtracts from the prediction
                        - The final prediction is shown on the right
                        """)
                    except Exception as e:
                        st.warning(f"Could not generate explanation for {ingredient}: {str(e)}")


if __name__ == '__main__':
    main()
