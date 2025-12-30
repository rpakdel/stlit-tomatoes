"""Data filtering utilities."""
import pandas as pd
from datetime import datetime


def filter_by_week(df, week_number=None):
    """
    Filter dataframe to show the same week from each year.
    
    Args:
        df: DataFrame with 'Date' column (must be datetime)
        week_number: ISO week number to filter by. If None, uses current week.
    
    Returns:
        DataFrame filtered by week number and sorted by date
    """
    if week_number is None:
        week_number = datetime.now().isocalendar()[1]
    
    filtered_df = df[df['Date'].dt.isocalendar().week == week_number].sort_values('Date')
    
    # Fallback to last 4 entries if no data for the specified week
    if filtered_df.empty:
        filtered_df = df.tail(4)
    
    return filtered_df
