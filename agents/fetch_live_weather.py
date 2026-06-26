import os
import json
import requests
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load API keys from .env file securely
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

# Target Output Directory
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "OUTPUT"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "live_weather.json"

# Garissa Coordinates
GARISSA_LAT = -0.4532
GARISSA_LON = 39.6461

def fetch_weather():
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    
    # Use fallback data if no API key is provided
    if not api_key:
        print("⚠️ No OPENWEATHER_API_KEY found. Using fallback simulated El Niño data.")
        data = {
            "temperature": 32.5,
            "humidity": 85,
            "wind_speed": 45,
            "precipitation": 120,
            "status": "Simulated (No API Key)",
            "timestamp": datetime.datetime.now().isoformat()
        }
    else:
        print("🌍 Fetching live weather data for Garissa from OpenWeather API...")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={GARISSA_LAT}&lon={GARISSA_LON}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            raw = response.json()
            
            # OpenWeather sends rain in 1h/3h objects if it is raining
            rain = raw.get("rain", {})
            precipitation = rain.get("1h", 0) or rain.get("3h", 0)
            
            data = {
                "temperature": raw["main"]["temp"],
                "humidity": raw["main"]["humidity"],
                "wind_speed": raw["wind"]["speed"] * 3.6, # Convert m/s to km/h
                "precipitation": precipitation,
                "status": "Live",
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error fetching from OpenWeather: {e}")
            print("Falling back to simulated data.")
            data = {
                "temperature": 31.0,
                "humidity": 80,
                "wind_speed": 40,
                "precipitation": 100,
                "status": "Error Fallback",
                "timestamp": datetime.datetime.now().isoformat()
            }

    # Write the data to the JSON file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"✅ Weather data saved to {OUTPUT_FILE}")
    return data

if __name__ == "__main__":
    fetch_weather()
