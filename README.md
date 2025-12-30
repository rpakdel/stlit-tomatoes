# Tomato Ordering AI

This is a Streamlit application designed to help a restaurant owner determine how many boxes of tomatoes to order. It uses historical data and machine learning to predict demand based on various factors.

## Features

- **Historical Data Analysis**: visualized sales history.
- **AI Prediction**: Predicts the number of boxes needed based on:
    - Weather conditions
    - Season
    - Holidays / Long Weekends
    - Promotional campaigns
- **User Friendly Interface**: Simple inputs to get a quick recommendation.

## Running Locally

### Using Dev Container (Recommended)
Open this project in VS Code with the Dev Containers extension. The container will be automatically set up with all dependencies.

### Using Docker
Build and run the app using the provided Dockerfile:
```bash
docker-compose up
```

Or build manually:
```bash
docker build -t tomato-ordering-ai .
docker run -p 8501:8501 tomato-ordering-ai
```

## Deployment

This app is ready to be deployed on Streamlit Cloud.
