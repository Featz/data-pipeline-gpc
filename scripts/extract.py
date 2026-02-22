import requests
import json
import pandas as pd

url = 'https://archive-api.open-meteo.com/v1/archive'
parameters = {
    "latitude": -36.7,
    "longitude": -71.9,
    "start_date": "2024-01-01",
    "end_date": "2024-01-05",
    "daily": ["temperature_2m_max", "precipitation_sum"],
    "timezone": "auto"
}

print('Connecting to API')
answer = requests.get(url, params=parameters)
print(f"Status Code: {answer.status_code}")

if answer.status_code == 200:
    raw_data = answer.json()
    daily_data = raw_data['daily']
    df = pd.DataFrame(raw_data['daily'])
    print('Data to Table')
    print(df.head())  
    print('-'*50)

    print('datatypes')
    print(df.dtypes)
    print('-'*50)
else:
    print(f"Error: {answer.status_code}")


