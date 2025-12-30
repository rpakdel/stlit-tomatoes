"""Weather fetching and categorization service."""
import requests
from model_utils import get_temperature_category


def get_weather_category(weather_code):
    """
    Convert WMO Weather interpretation code to category.
    
    Args:
        weather_code: WMO weather code (WW)
    
    Returns:
        Weather category string: 'Sunny', 'Cloudy', 'Snowy', or 'Rainy'
    """
    if weather_code == 0:
        return 'Sunny'
    elif weather_code in [1, 2, 3, 45, 48]:
        return 'Cloudy'
    elif weather_code in [71, 73, 75, 77, 85, 86]:
        return 'Snowy'
    else:
        # Everything else is considered Rainy (Drizzle, Rain, Thunderstorm)
        return 'Rainy'


def fetch_weather_data(date, latitude=49.2827, longitude=-123.1207):
    """
    Fetch weather data from Open-Meteo API.
    
    Args:
        date: datetime object for the target date
        latitude: Location latitude (default: Vancouver)
        longitude: Location longitude (default: Vancouver)
    
    Returns:
        Tuple of (weather_category, max_temperature) or (None, None) if unavailable
    """
    date_str = date.strftime('%Y-%m-%d')

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["weather_code", "temperature_2m_max"],
        "timezone": "auto",
        "start_date": date_str,
        "end_date": date_str
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'daily' not in data or not data['daily']['time']:
            return None, None

        weather_code = data['daily']['weather_code'][0]
        max_temp = data['daily']['temperature_2m_max'][0]

        weather_category = get_weather_category(weather_code)

        return weather_category, max_temp
    except Exception as e:
        return None, None
