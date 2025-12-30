import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from model_utils import get_season, get_temperature_category

def generate_data():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date

    data = []

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        weekday = day.weekday() # 0=Monday, 6=Sunday

        # Determine Season
        season = get_season(day)

        # Determine Weather
        weather_options = ['Sunny', 'Cloudy', 'Rainy']
        if season == 'Winter':
            weather_options.append('Snowy')

        # Generate Temperature (Celsius) and Weather based on season
        if season == 'Winter':
            # Vancouver Winter: ~4C, sometimes < 0, sometimes > 10
            temp_c = random.gauss(4, 4)
            weather = random.choices(weather_options, weights=[0.2, 0.3, 0.3, 0.2], k=1)[0]
        elif season == 'Spring':
            # Vancouver Spring: ~13C
            temp_c = random.gauss(13, 4)
            weather = random.choices(weather_options, weights=[0.4, 0.3, 0.3], k=1)[0]
        elif season == 'Summer':
            # Vancouver Summer: ~22C, can reach 30+
            temp_c = random.gauss(22, 4)
            weather = random.choices(weather_options, weights=[0.6, 0.2, 0.2], k=1)[0]
        else: # Autumn
            # Vancouver Autumn: ~11C
            temp_c = random.gauss(11, 4)
            weather = random.choices(weather_options, weights=[0.3, 0.3, 0.4], k=1)[0]

        temp_category = get_temperature_category(temp_c)

        # Consistency checks (e.g. Snowy only if cold enough)
        if weather == 'Snowy' and temp_c > 5:
            weather = 'Rainy'
        if weather == 'Rainy' and temp_c < -1:
            weather = 'Snowy'

        # Long Weekend
        is_long_weekend = False
        if weekday == 4 or weekday == 0: # Friday or Monday
            if random.random() < 0.05: # Occasional long weekend
                is_long_weekend = True

        # Holiday (Simple approximation)
        is_holiday = False
        month = day.month
        # New Year
        if month == 1 and day.day == 1: is_holiday = True
        # Christmas
        if month == 12 and day.day == 25: is_holiday = True
        # Canada Day (July 1st) - using July 4th in original code but Vancouver implies Canada Day
        if month == 7 and day.day == 1: is_holiday = True
        # Thanksgiving (Canada is 2nd Mon in Oct) - approximations
        if month == 10 and 8 <= day.day <= 14 and weekday == 0: is_holiday = True

        # Promotion
        is_promotion = random.random() < 0.15

        # Base Orders
        tomato_boxes = random.randint(2, 5)
        green_pepper_boxes = random.randint(1, 3)
        lettuce_boxes = random.randint(2, 4)
        cucumber_boxes = random.randint(1, 4)

        # Modifiers using new categories
        # High sales on nice summer days
        if season == 'Summer' and weather == 'Sunny' and temp_category in ['Warm', 'Hot']:
            tomato_boxes += random.randint(2, 4)
            green_pepper_boxes += random.randint(1, 3)
            lettuce_boxes += random.randint(2, 5)
            cucumber_boxes += random.randint(2, 4)

        if is_long_weekend:
            tomato_boxes += 2
            green_pepper_boxes += 1
            lettuce_boxes += 2
            cucumber_boxes += 1

        if is_promotion:
            tomato_boxes += random.randint(2, 3)
            green_pepper_boxes += random.randint(1, 2)
            lettuce_boxes += random.randint(2, 4)
            cucumber_boxes += random.randint(1, 3)

        # Low sales on bad weather days
        if weather == 'Rainy' or (season != 'Summer' and temp_category in ['Cold', 'Very cold']):
            tomato_boxes -= random.randint(1, 2)
            green_pepper_boxes -= 1
            lettuce_boxes -= random.randint(1, 2)
            cucumber_boxes -= 1

        if is_holiday:
            tomato_boxes += random.randint(5, 10)
            green_pepper_boxes += random.randint(3, 6)
            lettuce_boxes += random.randint(5, 10)
            cucumber_boxes += random.randint(4, 8)

        # Ensure boxes is at least 1 (or 0 if that makes sense, but let's say 1 minimum for operation)
        tomato_boxes = max(1, tomato_boxes)
        green_pepper_boxes = max(1, green_pepper_boxes)
        lettuce_boxes = max(1, lettuce_boxes)
        cucumber_boxes = max(1, cucumber_boxes)

        data.append({
            'Date': day.strftime('%Y-%m-%d'),
            'Season': season,
            'Weather': weather,
            'Temperature': temp_category,
            'Long_Weekend': is_long_weekend,
            'Promotion': is_promotion,
            'Holiday': is_holiday,
            'Tomato_Boxes': tomato_boxes,
            'Green_Pepper_Boxes': green_pepper_boxes,
            'Lettuce_Boxes': lettuce_boxes,
            'Cucumber_Boxes': cucumber_boxes
        })

    df = pd.DataFrame(data)
    df.to_csv('tomato_sales_history.csv', index=False)
    print("Data generated and saved to tomato_sales_history.csv")

if __name__ == '__main__':
    generate_data()
