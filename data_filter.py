"""Data filtering utilities."""
import pandas as pd
from datetime import datetime, timedelta


def filter_by_week(df, week_number=None):
    """
    Filter dataframe to show the same week from each year, plus/minus one week.
    
    Args:
        df: DataFrame with 'Date' column (must be datetime)
        week_number: ISO week number to filter by. If None, uses current week.
    
    Returns:
        DataFrame filtered by week number and sorted by date
    """
    if week_number is None:
        week_number = datetime.now().isocalendar()[1]
    
    # Find all dates in the dataset that match the target week number
    target_dates = df[df['Date'].dt.isocalendar().week == week_number]['Date']
    
    if target_dates.empty:
        # Fallback to last 12 entries if no data for the specified week
        return df.tail(12).sort_values('Date', ascending=False)
        
    result_rows = []
    
    # Sort target dates descending to keep year order
    target_dates = target_dates.sort_values(ascending=False)

    for date in target_dates:
        # Define the triplet of dates
        dates_in_group = [
            date + timedelta(days=7), # Next
            date,                     # This
            date - timedelta(days=7)  # Prev
        ]
        
        # Filter out future dates
        dates_in_group = [d for d in dates_in_group if d <= datetime.now()]
        
        # Find these rows in the original df
        group_df = df[df['Date'].isin(dates_in_group)].copy()
        
        # If we found any rows
        if not group_df.empty:
            # Assign the year of the central date (This Week) as the grouping year
            group_df['GroupYear'] = date.year
            result_rows.append(group_df)

    if not result_rows:
         return df.tail(12).sort_values('Date', ascending=False)

    filtered_df = pd.concat(result_rows)
    
    # Sort by GroupYear descending, and then by Date descending within group
    filtered_df = filtered_df.sort_values(['GroupYear', 'Date'], ascending=[False, False])
    
    return filtered_df
