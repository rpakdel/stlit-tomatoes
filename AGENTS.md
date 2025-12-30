# AGENTS.md

This repository contains the source code for the Ingredient Ordering AI app.

## Project Goal
Build a Streamlit application that uses AI and heuristics to help a restaurant owner order the correct amount of ingredient boxes based on historical data and external factors (weather, holidays, promotions).

The app predicts orders for multiple ingredients:
- **Tomatoes**
- **Green Peppers**
- **Lettuce**
- **Cucumbers**

## Guidelines
- **Framework**: Use Streamlit for the frontend.
- **Language**: Python.
- **Data**: Mock data should be realistic and reflect the specified patterns.
- **AI**: Use scikit-learn for the prediction model.
- **Deployment**: The app is intended for Streamlit Cloud. Ensure `requirements.txt` is present and up-to-date.

## Heuristics for Data Generation
**Base orders per ingredient:**
- Tomatoes: 2-5 boxes
- Green Peppers: 1-3 boxes
- Lettuce: 2-4 boxes
- Cucumbers: 1-4 boxes

**Order modifiers:**
- Summer + Sunny/Warm: Increase all ingredient orders significantly.
- Long Weekends: Increase all orders moderately.
- Promotions: Increase all orders.
- Cold/Rainy: Decrease all orders.
- Winter + Snow + Weekend: Increase orders.
- Holidays: Exceptionally high orders for all ingredients.

## Progress
- **Multi-Ingredient Prediction**: Extended the model to predict orders for Tomatoes, Green Peppers, Lettuce, and Cucumbers simultaneously.
- **Auto-Generate Data**: App automatically generates `tomato_sales_history.csv` on first run if the file doesn't exist.
- **Refined App UX**: Automate Season selection based on the Date input and filter Weather options.
- **Input Refinement**: Changed Temperature input from numerical to categorical (Very cold, Cold, Normal, Warm, Hot) for better user experience.
- **Code Organization**: Refactored shared logic into `model_utils.py` and configured `.gitignore` for generated files.
- **Feature Cleanup**: Removed `Is_Weekend` feature as orders are strictly placed on Wednesdays.
- **Deployment Ready**: Added Dockerfile and Dev Container configuration for easy local development and deployment.
