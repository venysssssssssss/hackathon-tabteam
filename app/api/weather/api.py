from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime

app = FastAPI()

api_key = "61e0f873c175e7d7b269d09c767e423c"
base_weather_url = "http://api.openweathermap.org/data/2.5/weather?"
base_onecall_url = "http://api.openweathermap.org/data/2.5/onecall?"
default_lat = 0  # Latitude padrão
default_lon = 0  # Longitude padrão

class ClimaResponse(BaseModel):
    city: str
    latitude: float
    longitude: float
    temperature: float
    pressure: int
    humidity: int
    description: str
    alert: str = None

def get_lat_lon(city_name: str):
    complete_url = base_weather_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()

    if response.status_code == 200 and "coord" in data:
        return data["coord"]["lat"], data["coord"]["lon"]
    else:
        raise HTTPException(status_code=404, detail="Cidade não encontrada.")

def fetch_alerts(lat: float, lon: float):
    complete_url = f'{base_onecall_url}lat={lat}&lon={lon}&exclude=minutely,hourly,daily&appid={api_key}&lang=pt'
    response = requests.get(complete_url)
    data = response.json()

    if response.status_code == 200 and 'alerts' in data:
        alerts = data['alerts']
        if alerts:
            alert = alerts[0]
            start_time = datetime.fromtimestamp(alert['start']).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.fromtimestamp(alert['end']).strftime('%Y-%m-%d %H:%M:%S')
            return f"{alert['event']}: {alert['description']} (Início: {start_time}, Fim: {end_time})"
    return "Nenhum alerta climático no momento."

@app.get('/weather', response_model=ClimaResponse)
def get_weather(city_name: str):
    lat, lon = get_lat_lon(city_name)
    
    complete_url = base_weather_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()

    if response.status_code == 200 and "main" in data and "weather" in data:
        main = data["main"]
        weather = data["weather"][0]

        temperature = main["temp"] - 273.15
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]

        alert = fetch_alerts(lat, lon)

        return ClimaResponse(
            city=city_name,
            latitude=lat,
            longitude=lon,
            temperature=temperature,
            pressure=pressure,
            humidity=humidity,
            description=description,
            alert=alert
        )
    else:
        raise HTTPException(status_code=response.status_code, detail=data.get('message', 'Nenhuma mensagem de erro fornecida'))
