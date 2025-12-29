def get_season(date_obj):
    """
    Determines the season based on the date for Vancouver, Canada.
    Spring: March 20 - June 19
    Summer: June 20 - Sep 19
    Autumn: Sep 20 - Dec 19
    Winter: Dec 20 - March 19
    """
    # Create a tuple (month, day) for comparison
    md = (date_obj.month, date_obj.day)

    if (3, 20) <= md <= (6, 19):
        return 'Spring'
    elif (6, 20) <= md <= (9, 19):
        return 'Summer'
    elif (9, 20) <= md <= (12, 19):
        return 'Autumn'
    else:
        return 'Winter'

def get_temperature_category(temp):
    """
    Categorizes temperature (Celsius) into ranges.
    Very cold: -3C and lower
    Cold: -3C until 10C
    Normal: 10 until 17
    Warm: 17 until 27
    Hot: 27C and above
    """
    if temp <= -3:
        return 'Very cold'
    elif temp < 10:
        return 'Cold'
    elif temp < 17:
        return 'Normal'
    elif temp < 27:
        return 'Warm'
    else:
        return 'Hot'
