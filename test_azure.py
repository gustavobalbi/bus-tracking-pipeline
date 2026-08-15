import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

conn_str = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{os.environ['AZURE_SERVER']},1433;"
    f"Database={os.environ['AZURE_DATABASE']};"
    f"Uid={os.environ['AZURE_USER']};"
    f"Pwd={os.environ['AZURE_PASSWORD']};"
    f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT schema_name FROM information_schema.schemata")
    print("CONECTOU! Schemas encontrados:")
    for row in cursor.fetchall():
        print(" -", row[0])
    conn.close()
except Exception as e:
    print("FALHOU:", e)
