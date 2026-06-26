#!/usr/bin/env python3
"""
Fetch weather data for Garissa using pyowm.
"""
import argparse
import os
import csv
from pyowm import OWM
from datetime import datetime

def fetch_weather(api_key, output_file='OUTPUT/weather_garissa.csv'):
    owm = OWM(api_key)
    mgr = owm.weather_manager()
    
    # Garissa Coordinates
    lat, lon = -0.4532, 39.6461
    
    print(f"Fetching current weather for Garissa ({lat}, {lon})...")
    observation = mgr.weather_at_coords(lat, lon)
    w = observation.weather
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'status': w.detailed_status,
        'temp_c': w.temperature('celsius').get('temp'),
        'humidity': w.humidity,
        'wind_speed': w.wind().get('speed'),
        'rain_1h': w.rain.get('1h', 0)
    }
    
    print(f"Current weather: {data}")
    
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    file_exists = os.path.isfile(output_file)
    
    with open(output_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
        
    print(f"Appended weather data to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', required=True, help='OpenWeatherMap API Key')
    parser.add_argument('--output', default='OUTPUT/weather_garissa.csv')
    args = parser.parse_args()
    
    try:
        fetch_weather(args.key, args.output)
    except Exception as e:
        print(f"Error fetching weather: {e}")
