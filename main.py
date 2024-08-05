import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

api_key = "61e0f873c175e7d7b269d09c767e423c"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

class ClimaResponse(BaseModel):
    city: str
    temperature: float
    pressure: int
    humidity: int
    description: str

@app.get('/weather', response_model=ClimaResponse)
def get_weather(city_name: str):
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()

    if response.status_code == 200:
        if "main" in data and "weather" in data:
            main = data["main"]
            weather = data["weather"][0]

            temperature = main["temp"] - 273.15  # Convert Kelvin to Celsius
            pressure = main["pressure"]
            humidity = main["humidity"]
            description = weather["description"]

            return ClimaResponse(
                city=city_name,
                temperature=temperature,
                pressure=pressure,
                humidity=humidity,
                description=description
            )
        else:
            raise HTTPException(status_code=404, detail="Informações meteorológicas não encontradas.")
    else:
        raise HTTPException(status_code=response.status_code, detail=data.get('message', 'Nenhuma mensagem de erro fornecida'))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
