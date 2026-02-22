import requests
import json

url = 'https://archive-api.open-meteo.com/v1/archive'
parameters = {
    "latitude": 40.4168,
    "longitude": -3.7038,
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
    print("Data structure:")
    print(json.dumps(raw_data, indent=2))    
else:
    print(f"Error: {answer.status_code}")


