import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["OLHOVIVO_TOKEN"]
BASE_URL = "https://api.olhovivo.sptrans.com.br/v2.1"

session = requests.Session()
# autentica (pra pegar a sessão atual) e depois desloga
session.post(f"{BASE_URL}/Login/Autenticar?token={TOKEN}")
out = session.post(f"{BASE_URL}/Login/Logoff")
print("Logoff status:", out.status_code, "| resposta:", out.text)
