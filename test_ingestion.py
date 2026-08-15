import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("OLHOVIVO_TOKEN")
BASE_URL = "http://api.olhovivo.sptrans.com.br/v2.1"

if not TOKEN:
    raise ValueError(
        "A variável de ambiente OLHOVIVO_TOKEN não foi definida no seu .env!"
    )

session = requests.Session()

# 1. Autenticação na API Olho Vivo
# A biblioteca requests cuida da formatação correta do POST com params
auth = session.post(f"{BASE_URL}/Login/Autenticar", params={"token": TOKEN})

print("Status HTTP:", auth.status_code)
print(
    "Resposta da API:", repr(auth.text)
)  # 'true' indica sucesso, 'false' indica falha

if auth.text.strip().lower() == "true":
    print("Autenticação realizada com sucesso!")

    # 2. Teste de consumo (Busca linhas no sistema)
    resp = session.get(f"{BASE_URL}/Posicao")
    dados = resp.json()

    print("Horário da coleta:", dados.get("hr"))
    linhas = dados.get("l", [])
    print("Número de linhas retornadas:", len(linhas))

    if linhas:
        primeira = linhas[0]
        print("\nAmostra — Linha:", primeira.get("c"))
        print("Ônibus nesta linha agora:", len(primeira.get("vs", [])))
else:
    print("\n[ERRO] A API retornou 'false'.")
    print("Verifique se:")
    print(
        "1. O token no arquivo .env é a 'Chave de Acesso' gerada em 'Meus Aplicativos'."
    )
    print(
        "2. Você aguardou ~10 minutos para encerrar qualquer sessão anterior pendente."
    )
