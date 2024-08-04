import streamlit as st
import requests
from PIL import Image
import os
import subprocess

# Função para obter dados climáticos
def get_weather_data(city_name):
    response = requests.get("http://127.0.0.1:8000/weather", params={"city_name": city_name})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro {response.status_code}: {response.json().get('detail', 'Erro desconhecido')}")
        return None

# Função para obter latitude e longitude da cidade
def get_city_coordinates(city_name):
    api_key = "61e0f873c175e7d7b269d09c767e423c"  # Substitua pelo seu API Key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        return latitude, longitude
    else:
        st.error(f"Erro ao obter coordenadas: {data.get('message', 'Erro desconhecido')}")
        return None, None

# Função para gerar e exibir imagem do Sentinel
def generate_image(instance_id, latitude, longitude):
    try:
        # Chama o script de geração da imagem
        subprocess.run(["python", "generate_image.py", str(instance_id), str(latitude), str(longitude)], check=True)
        return "data/sentinel_image.jpg"
    except Exception as e:
        st.error(f"Erro ao gerar a imagem: {e}")
        return None

# Configuração da página
st.set_page_config(page_title="Aplicação Climática", layout="wide")

st.title("Dados Climáticos e Imagem Sentinel")

instance_id = "2e529581-603b-45c1-8c2b-c73f97acd1d1"

# Input dos dados climáticos
city_name = st.text_input("Nome da cidade:", "Salvador")

if st.button("Consultar Dados Climáticos e Imagem"):
    # Obtém dados climáticos
    data = get_weather_data(city_name)
    
    if data:
        # Cria colunas para organizar o layout
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader(f"Clima em {data['city']}")
            st.write(f"**Temperatura:** {data['temperature']:.2f} °C")
            st.write(f"**Pressão:** {data['pressure']} hPa")
            st.write(f"**Umidade:** {data['humidity']} %")
            st.write(f"**Descrição:** {data['description']}")
            st.write(f"**Alerta Climático:** {data['alert']}")
            
            # Obtém coordenadas da cidade
            latitude, longitude = get_city_coordinates(city_name)
            
            if latitude is not None and longitude is not None:
                st.write(f"**Latitude:** {latitude}")
                st.write(f"**Longitude:** {longitude}")

        with col2:
            # Gera a imagem
            image_path = generate_image(instance_id, latitude, longitude)
            
            if image_path and os.path.exists(image_path):
                st.image(image_path, caption="Imagem do Sentinel")
            else:
                st.error("Imagem não encontrada. Verifique a geração da imagem.")
