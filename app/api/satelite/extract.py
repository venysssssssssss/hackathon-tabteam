from fastapi import FastAPI, HTTPException
from geopy.geocoders import Nominatim
import os
import requests

app = FastAPI()
geolocator = Nominatim(user_agent="geoapiExercises")

def create_data_folder():
    if not os.path.exists('data'):
        os.makedirs('data')

def get_sentinel_data(instance_id, latitude, longitude, count=1, dim=0.02):
    """
    Retrieves satellite data from the Sentinel Hub API and saves the images locally.
    Args:
        instance_id (str): The instance ID for accessing the Sentinel Hub API.
        latitude (float): The latitude coordinate for the desired location.
        longitude (float): The longitude coordinate for the desired location.
        count (int, optional): The number of satellite images to retrieve. Defaults to 1.
        dim (float, optional): The dimension of the bounding box around the location. Defaults to 0.02.
    Returns:
        None
    Raises:
        None
    """
    # Rest of the code...
    url = f"https://services.sentinel-hub.com/ogc/wms/{instance_id}"
    params = {
        "SERVICE": "WMS",
        "REQUEST": "GetMap",
        "VERSION": "1.1.1",
        "LAYERS": "TRUE-COLOR-S2L2A",
        "MAXCC": "20",
        "FORMAT": "image/jpeg",
        "WIDTH": "512",
        "HEIGHT": "512",
        "CRS": "EPSG:4326",
        "DIM": dim
    }
    
    create_data_folder()

    for i in range(count):
        params["BBOX"] = f"{longitude-dim},{latitude-dim},{longitude+dim},{latitude+dim}"
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            file_path = f"data/satellite_image_{i+1}.jpg"
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Imagem {i+1} salva como {file_path}")
        else:
            print(f"Erro: {response.status_code}, {response.text}")

@app.get("/get-data/{country}/{state}/{city}")
async def get_data(country: str, state: str, city: str):
    try:
        # Geocode the location
        loc = geolocator.geocode(f"{city}, {state}, {country}")
        if not loc:
            raise HTTPException(status_code=404, detail="Location not found")

        latitude = loc.latitude
        longitude = loc.longitude

        # Sentinel instance ID (substitua pelo seu ID real)
        instance_id = "2e529581-603b-45c1-8c2b-c73f97acd1d1"
        
        # Get sentinel data
        get_sentinel_data(instance_id, latitude, longitude)
        
        return {"message": "Data fetched and images saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Executar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
