import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime
from model_utils import get_season, TEMPERATURE_CATEGORIES

# Load data
@st.cache_data
def load_data():
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

        weather = st.selectbox("Weather", ['Sunny', 'Cloudy', 'Rainy', 'Snowy'])

        # User selects temperature category
        temperature_category = st.selectbox("Temperature Category", TEMPERATURE_CATEGORIES)

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
