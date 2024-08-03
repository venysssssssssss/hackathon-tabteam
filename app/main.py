import requests

# Substitua 'YOUR_API_KEY' pela sua chave de API
api_key = "61e0f873c175e7d7b269d09c767e423c"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = "São Paulo"
complete_url = base_url + "q=" + city_name + "&appid=" + api_key

response = requests.get(complete_url)
data = response.json()

if response.status_code == 200:
    if "main" in data:
        main = data["main"]
        weather = data["weather"][0]

        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]

        print(f"Temperature: {temperature}")
        print(f"Pressure: {pressure}")
        print(f"Humidity: {humidity}")
        print(f"Description: {description}")
    else:
        print("Erro: A resposta da API não contém informações meteorológicas.")
else:
    print(f"Erro: Não foi possível obter dados. Código de status HTTP: {response.status_code}")
    print(f"Mensagem: {data.get('message', 'Nenhuma mensagem de erro fornecida')}")
