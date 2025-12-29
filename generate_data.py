import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_data():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date

    data = []

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        month = day.month
        weekday = day.weekday() # 0=Monday, 6=Sunday

        # Determine Season
        if month in [12, 1, 2]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Spring'
        elif month in [6, 7, 8]:
            season = 'Summer'
        else:
            season = 'Autumn'

        # Determine Weather and Temp
        weather_options = ['Sunny', 'Cloudy', 'Rainy']
        if season == 'Winter':
            weather_options.append('Snowy')

        # Weight weather based on season
        if season == 'Summer':
            weather = random.choices(weather_options, weights=[0.6, 0.2, 0.2], k=1)[0]
            temp = random.choices(['High', 'Medium'], weights=[0.8, 0.2], k=1)[0]
        elif season == 'Winter':
            weather = random.choices(weather_options, weights=[0.2, 0.3, 0.2, 0.3], k=1)[0]
            temp = random.choices(['Low', 'Medium'], weights=[0.8, 0.2], k=1)[0]
        else:
            weather = random.choice(weather_options)
            temp = random.choice(['Low', 'Medium', 'High'])

        # Long Weekend
        is_long_weekend = False
        if weekday == 4 or weekday == 0: # Friday or Monday
            if random.random() < 0.05: # Occasional long weekend
                is_long_weekend = True

        # Holiday (Simple approximation)
        is_holiday = False
        # New Year
        if month == 1 and day.day == 1: is_holiday = True
        # Christmas
        if month == 12 and day.day == 25: is_holiday = True
        # July 4th
        if month == 7 and day.day == 4: is_holiday = True
        # Thanksgiving (approx late Nov)
        if month == 11 and day.day == 26: is_holiday = True # Fixed date for simplicity

        # Promotion
        is_promotion = random.random() < 0.15

        # Calculate Boxes
        boxes = random.randint(2, 5)

        # Modifiers
        if season == 'Summer' and weather == 'Sunny' and temp == 'High':
            boxes += random.randint(2, 4)

        if is_long_weekend:
            boxes += 2

        if is_promotion:
            boxes += random.randint(2, 3)

        if weather == 'Rainy' or (season != 'Summer' and temp == 'Low'):
            boxes -= random.randint(1, 2)

        if is_holiday:
            boxes += random.randint(5, 10)

        # Ensure boxes is at least 0 (or 1 realistically if opened)
        # Assuming restaurant is open. If holiday and closed? Prompt says "exceptionally high during holidays when other restaurants are closed". So we assume open.
        boxes = max(1, boxes)

        data.append({
            'Date': day.strftime('%Y-%m-%d'),
            'Season': season,
            'Weather': weather,
            'Temperature': temp,
            'Long_Weekend': is_long_weekend,
            'Promotion': is_promotion,
            'Holiday': is_holiday,
            'Boxes_Ordered': boxes
        })

    df = pd.DataFrame(data)
    df.to_csv('tomato_sales_history.csv', index=False)
    print("Data generated and saved to tomato_sales_history.csv")

if __name__ == '__main__':
    generate_data()
