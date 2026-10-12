import urllib.request
import json

def get_weather():
    """
    Fetches extended current weather data using the free Open-Meteo API.
    Returns temperature, feels-like temperature, humidity, wind speed, and condition.
    """
    # Coordinates for Chennai
    lat = 13.0827
    lon = 80.2707
    
    # We expanded our "order" to the API by adding new data points separated by commas
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"

    stats = {
        "temp": "N/A",
        "feels_like": "N/A",
        "humidity": "N/A",
        "wind": "N/A",
        "condition": "Unknown",
        "error": None
    }

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'EPaper-Dashboard/1.0'})
        with urllib.request.urlopen(req) as response:
            raw_data = response.read()
            
        weather_data = json.loads(raw_data)
        
        # Shortcut to the 'current' dictionary block
        current = weather_data['current']
        
        # Extract all the new specific numbers
        current_temp = current['temperature_2m']
        feels_like = current['apparent_temperature']
        humidity = current['relative_humidity_2m']
        wind_speed = current['wind_speed_10m']
        weather_code = current['weather_code']
        
        # Translate the raw weather code into English
        condition = "Clear"
        if 1 <= weather_code <= 3: condition = "Cloudy"
        elif 45 <= weather_code <= 48: condition = "Fog"
        elif 51 <= weather_code <= 67: condition = "Rain"
        elif 71 <= weather_code <= 77: condition = "Snow"
        elif 95 <= weather_code <= 99: condition = "Thunderstorm"

        # Format everything nicely for the screen
        stats["temp"] = f"{current_temp}°C"
        stats["feels_like"] = f"{feels_like}°C"
        stats["humidity"] = f"{humidity}%"
        stats["wind"] = f"{wind_speed} km/h"
        stats["condition"] = condition

    except Exception as e:
        stats["error"] = f"Failed to fetch weather: {e}"

    return stats

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Testing Extended Weather Fetcher...")
    current_weather = get_weather()
    
    # Print out each item nicely
    for key, value in current_weather.items():
        print(f"{key.capitalize()}: {value}")