import requests
import os
from dotenv import load_dotenv

load_dotenv()

def buscar_classificacao_brasileirao():
    url = "https://api.football-data.org/v4/competitions/BSA/standings"
    headers = {
        "X-Auth-Token": os.getenv("API_FUTEBOL_KEY")
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro da API: {response.status_code}")
        return None

if __name__ == "__main__":
    resultado = buscar_classificacao_brasileirao()
    if resultado:
        print("Tudo certo com a API!")