from fastapi import FastAPI
from satelite.get_satelite_img import app as satellite_app
from weather.api import app as weather_app

app = FastAPI()

# Incluir os roteadores das outras aplicações
app.include_router(satellite_app.router, prefix="/satellite")
app.include_router(weather_app.router, prefix="/weather")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
