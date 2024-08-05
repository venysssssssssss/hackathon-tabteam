from fastapi import FastAPI, HTTPException, Query
from geopy.geocoders import Nominatim
import os
import requests
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()
geolocator = Nominatim(user_agent="your_app_name")

def create_data_folder():
    if not os.path.exists('data'):
        os.makedirs('data')
    logger.info("Pasta 'data' criada/verificada com sucesso.")

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
        HTTPException: If the API request fails.
    """
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
        "BBOX": f"{longitude-dim},{latitude-dim},{longitude+dim},{latitude+dim}"
    }
    headers = {
        "Authorization": f"Bearer {instance_id}"
    }

    create_data_folder()

    for i in range(min(count, 5)):
        logger.info(f"Enviando requisição {i+1} com os parâmetros: {params}")
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            file_path = f"data/satellite_image_{i+1}.jpg"
            with open(file_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Imagem {i+1} salva como {file_path}")
        else:
            error_msg = f"Erro: {response.status_code}, {response.text}"
            logger.error(f"Detalhes do erro: {response.text}")
            logger.error(f"Headers da resposta: {response.headers}")
            raise HTTPException(status_code=response.status_code, detail=error_msg)

@app.get("/get-data/{country}/{state}/{city}")
async def get_data(country: str, state: str, city: str, count: int = Query(1, ge=1, le=5)):
    try:
        logger.info(f"Geocodificando localização: {city}, {state}, {country}")
        loc = geolocator.geocode(f"{city}, {state}, {country}")
        if not loc:
            error_msg = "Localização não encontrada"
            logger.error(error_msg)
            raise HTTPException(status_code=404, detail=error_msg)

        latitude = loc.latitude
        longitude = loc.longitude

        logger.info(f"Localização geocodificada: latitude={latitude}, longitude={longitude}")

        # Sentinel instance ID from environment variable
        instance_id = os.getenv("INSTANCE_ID")
        if not instance_id:
            error_msg = "ID da Instância não configurado"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

        logger.info(f"Usando INSTANCE_ID: {instance_id}")

        # Get sentinel data
        get_sentinel_data(instance_id, latitude, longitude, count)

        success_msg = "Dados buscados e imagens salvas com sucesso."
        logger.info(success_msg)
        return {"message": success_msg}
    except Exception as e:
        error_msg = f"Erro no processamento: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

# Executar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
