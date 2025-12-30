# AGENTS.md

This repository contains the source code for the Tomato Ordering AI app.

## Project Goal
Build a Streamlit application that uses AI and heuristics to help a restaurant owner order the correct amount of tomato boxes based on historical data and external factors (weather, holidays, promotions).

## Guidelines
- **Framework**: Use Streamlit for the frontend.
- **Language**: Python.
- **Data**: Mock data should be realistic and reflect the specified patterns.
- **AI**: Use scikit-learn for the prediction model.
- **Deployment**: The app is intended for Streamlit Cloud. Ensure `requirements.txt` is present and up-to-date.

## Heuristics for Data Generation
- Base order: 2-5 boxes.
- Summer + Sunny/Warm: Increase order.
- Long Weekends: Increase order.
- Promotions: Increase order.
- Cold/Rainy: Decrease order.
- Winter + Snow + Weekend: Increase order.
- Holidays: Exceptionally high order.

## Progress
- **Refined App UX**: Automate Season selection based on the Date input and filter Weather options.
- **Input Refinement**: Changed Temperature input from numerical to categorical (Very cold, Cold, Normal, Warm, Hot) for better user experience.
- **Data Automation**: Implemented `generate_data.py` to automatically create realistic mock sales history (`tomato_sales_history.csv`) if missing.
- **Code Organization**: Refactored shared logic into `model_utils.py` and configured `.gitignore` for generated files.
- **Feature Cleanup**: Removed `Is_Weekend` feature as orders are strictly placed on Wednesdays.
