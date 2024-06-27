import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Calculate the start_date and end_date for "yesterday"
yesterday = datetime.now() - timedelta(days=1)
start_date = yesterday.strftime('%Y-%m-%d')
end_date = start_date

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 48.8534,
    "longitude": 2.3488,
    "start_date": start_date,
    "end_date": end_date,
    "hourly": [
        "temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation", "rain", "snowfall", "snow_depth", "weather_code", "pressure_msl",
        "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m",
        "wind_speed_100m", "wind_direction_10m", "wind_direction_100m", "wind_gusts_10m", "soil_temperature_0_to_7cm", "soil_temperature_7_to_28cm", "soil_temperature_28_to_100cm",
        "soil_temperature_100_to_255cm", "soil_moisture_0_to_7cm", "soil_moisture_7_to_28cm", "soil_moisture_28_to_100cm", "soil_moisture_100_to_255cm"
    ]
}

# Make the API request
response = openmeteo.request(method='GET', url=url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Process the data and save it to a CSV file
    df = pd.DataFrame(data['hourly'])
    csv_file = 'weather_data.csv'
    df.to_csv(csv_file, index=False)
    print(f"Weather data has been saved to {csv_file}")
else:
    print(f"Failed to fetch weather data: {response.status_code} - {response.text}")
