import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import requests
from dotenv import load_dotenv

# The following is an example of how I would solve the assessment provided for the position of data engineer




# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    raise Exception("API Key not found! Please check your .env file")

API_BASE_URL = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
COORDINATES = [(41.3112, -111.9689), (38.9122, -77.0177), (37.7786, -122.4892)]

class WeatherAPIException(Exception):
    pass

def fetch_weather_data(lat, lon, api_key):
    # Fetching weather data from openweathermap.org for last five days
    updated_weather_data = []
    timezone = ZoneInfo("America/Denver")

    for day in range(5):
        #converting current time to UTC time and looping through previous five days
        dt = int((datetime.now(tz=timezone) - timedelta(days=day)).timestamp())
        params = {
            "lat": lat,
            "lon": lon,
            "dt": dt,
            "appid": api_key,
            "units": "imperial"
        }
        response = requests.get(API_BASE_URL, params=params)
        if response.status_code != 200:
            raise WeatherAPIException(f"API request failed with status code {response.status_code}")
        data = response.json()
        data['current'].pop('weather', None)
        #removing "weather" section from each response
        updated_weather_data.append(data)
    return updated_weather_data

def process_weather_data(coordinates, api_key):
    processed_data = []
    for lat, lon in coordinates:
        location_data = fetch_weather_data(lat, lon, api_key)
        all_hourly_data = []

        for daily_data in location_data:
            # Flatten 'current' data
            flattened_current = {f"current.{key}": value for key, value in daily_data['current'].items()}

            # Append this day's hourly data to the container
            all_hourly_data.extend(daily_data["hourly"])

        # Construct the data for the location
        # Using the first day's data for 'current' and timezone information
        flattened_data = {
            "lat": lat,
            "lon": lon,
            "timezone": location_data[0]["timezone"],
            "timezone_offset": location_data[0]["timezone_offset"],
            **flattened_current,
            "hourly": all_hourly_data
        }

        # Append this location's data to processed_data
        processed_data.append(flattened_data)

    return processed_data



def main():
    try:
        weather_data = process_weather_data(COORDINATES, API_KEY)
        df = pd.DataFrame(weather_data)

        # Compute 'average_temp' and perform additional dataframe operations
        df['average_temp'] = df.apply(lambda row: sum(hourly['temp'] for hourly in row['hourly']) / len(row['hourly']) if row['hourly'] else None, axis=1)

        # Drop the 'hourly' column
        df.drop(columns='hourly', inplace=True)

        # Write data to files
        df.to_csv('weather_data.csv', index=False)
        df.to_json('weather_data.json', orient='records')
    except WeatherAPIException as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
