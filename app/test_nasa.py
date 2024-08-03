import os
import requests

def create_data_folder():
    if not os.path.exists('data'):
        os.makedirs('data')

def get_sentinel_data(instance_id, latitude, longitude, count=1, dim=0.02):
    url = f"https://services.sentinel-hub.com/ogc/wms/{instance_id}"
    params = {
        "SERVICE": "WMS",
        "REQUEST": "GetMap",
        "VERSION": "1.1.1",
        "LAYERS": "TRUE-COLOR-S2L2A",  # Camada corrigida
        "MAXCC": "20",
        "FORMAT": "image/jpeg",
        "WIDTH": "512",
        "HEIGHT": "512",
        "CRS": "EPSG:4326",
        "DIM": dim  # Adicionado parâmetro de dimensão para mais detalhes
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

# Exemplo de uso
instance_id = "2e529581-603b-45c1-8c2b-c73f97acd1d1"
latitude = -12.97111  # Latitude de São Paulo
longitude = -38.51083  # Longitude de São Paulo

get_sentinel_data(instance_id, latitude, longitude)
