"""Data formatting utilities for display."""
import pandas as pd
from datetime import datetime


def format_data_for_display(df, target_week=None):
    """
    Format dataframe for user-friendly display with context.
    
    Args:
        df: DataFrame with 'Date' column (datetime)
        target_week: ISO week number to highlight context
    
    Returns:
        DataFrame formatted for display
    """
    if target_week is None:
        target_week = datetime.now().isocalendar()[1]

    display_df = df.copy()
    
    # Add Year and Timeline context
    # Always use the actual year from the date for display to avoid confusion
    # when a week spans across two years (e.g. Dec 25 labeled as next year)
    display_df['Year'] = display_df['Date'].dt.year
    
    def get_timeline(row_date):
        w = row_date.isocalendar().week
        if w == target_week:
            return "This Week"
        
        # Handle year boundary cases
        if target_week == 1:
            if w >= 52: return "Previous Week"
            return "Next Week"
        if target_week >= 52:
            if w == 1: return "Next Week"
            return "Previous Week"
            
        return "Previous Week" if w < target_week else "Next Week"

    display_df['Timeline'] = display_df['Date'].apply(get_timeline)
    
    # Format Date to be shorter (Month Day)
    display_df['Date'] = display_df['Date'].dt.strftime('%b %d')
    
    # Reorder and rename columns for clarity
    cols_to_keep = [
        'Year', 'Timeline', 'Date', 'Weather', 'Temperature',
        'Tomato_Boxes', 'Green_Pepper_Boxes', 'Lettuce_Boxes', 'Cucumber_Boxes',
        'Promotion', 'Holiday'
    ]
    
    # Keep GroupYear if present for styling purposes
    if 'GroupYear' in display_df.columns:
        cols_to_keep.append('GroupYear')
    
    # Rename map for better readability
    rename_map = {
        'Tomato_Boxes': 'Tomato',
        'Green_Pepper_Boxes': 'Green Pepper',
        'Lettuce_Boxes': 'Lettuce',
        'Cucumber_Boxes': 'Cucumber',
        'Temperature': 'Temp',
        'Promotion': 'Promo'
    }
    
    # Filter existing columns
    existing_cols = [c for c in cols_to_keep if c in display_df.columns]
    display_df = display_df[existing_cols].rename(columns=rename_map)
    
    return display_df


def apply_year_highlight(df):
    """
    Apply background color highlighting based on Year.
    
    Args:
        df: DataFrame to style
        
    Returns:
        pandas Styler object
    """
    def get_row_style(row):
        # Use GroupYear for coloring if available to keep triplets visually unified
        year = row['GroupYear'] if 'GroupYear' in row else row['Year']
        # Cycle through soft colors to distinguish years
        colors = [
            '#e6f3ff', # Light Blue
            '#f0f9e8', # Light Green
            '#fff7bc', # Light Yellow
            '#fee0d2', # Light Red/Orange
        ]
        # Use year to pick a color
        color = colors[year % len(colors)]
        # Adding color: black to ensure text is readable against light backgrounds
        return [f'background-color: {color}; color: black' for _ in row]
        
    styler = df.style.apply(get_row_style, axis=1)
    
    # Hide GroupYear column if present
    if 'GroupYear' in df.columns:
        styler.hide(axis='columns', subset=['GroupYear'])
        
    return styler
