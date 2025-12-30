"""Data formatting utilities for display."""
import pandas as pd


def format_dates_for_display(df):
    """
    Format dataframe dates for user-friendly display.
    
    Args:
        df: DataFrame with 'Date' column (datetime)
    
    Returns:
        DataFrame copy with dates formatted as 'Month day, year'
    """
    display_df = df.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%B %d, %Y')
    return display_df
