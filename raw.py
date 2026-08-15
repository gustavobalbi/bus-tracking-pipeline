import os
import json
import requests
import pyodbc
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["OLHOVIVO_TOKEN"]
BASE_URL = "http://api.olhovivo.sptrans.com.br/v2.1"

session = requests.Session()
auth = session.post(f"{BASE_URL}/Login/Autenticar?token={TOKEN}")
if auth.text != "true":
    print("Autenticação falhou.")
    exit()

resp = session.get(f"{BASE_URL}/Posicao")
dados = resp.json()
api_ts = dados.get("hr")
payload_json = json.dumps(dados)
print(f"Coletado: {len(dados.get('l', []))} linhas às {api_ts}")

conn_str = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{os.environ['AZURE_SERVER']},1433;"
    f"Database={os.environ['AZURE_DATABASE']};"
    f"Uid={os.environ['AZURE_USER']};"
    f"Pwd={os.environ['AZURE_PASSWORD']};"
    f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO bronze.RAW_BUS_POSITIONS (API_TIMESTAMP, JSON) VALUES (?, ?)",
    api_ts,
    payload_json,
)
conn.commit()
conn.close()
print("Gravado na bronze com sucesso!")
