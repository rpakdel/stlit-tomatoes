"""Data loading and generation module."""
import os
import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """Load historical sales data, generating it if it doesn't exist."""
    if not os.path.exists('tomato_sales_history.csv'):
        st.info("Generating initial data file...")
        from generate_data import generate_data
        generate_data()
    
    df = pd.read_csv('tomato_sales_history.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df
