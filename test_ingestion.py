import os
import requests
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.environ["OLHOVIVO_TOKEN"]
BASE_URL = "https://api.olhovivo.sptrans.com.br/v2.1"

session = requests.Session()

headers = {"Content-Length": "0"}
auth = session.post(f"{BASE_URL}/Login/Autenticar?token={TOKEN}", headers=headers)
print("Status HTTP:", auth.status_code)
print("Resposta da API:", auth.text)
print(f"Token utilizado: {TOKEN}")

if auth.text != "true":
    print("Autenticação falhou. A sessão pode estar 'em uso' — aguarde alguns minutos.")
else:
    print("Autenticação: OK")
    resp = session.get(f"{BASE_URL}/Posicao")
    dados = resp.json()
    print("Horário da coleta:", dados.get("hr"))
    linhas = dados.get("l", [])
    print("Número de linhas retornadas:", len(linhas))
    if linhas:
        primeira = linhas[0]
        print("\nAmostra — Linha:", primeira.get("c"))
        print("Ônibus nesta linha agora:", len(primeira.get("vs", [])))
        if primeira.get("vs"):
            onibus = primeira["vs"][0]
            print(
                "Exemplo — prefixo:",
                onibus.get("p"),
                "| lat:",
                onibus.get("py"),
                "| lon:",
                onibus.get("px"),
            )
