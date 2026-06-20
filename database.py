import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("SHEETDB_URL") # .env dosyanı oluşturmayı unutma!

def db_getir_gorevler():
    try:
        response = requests.get(API_URL)
        return response.json() if response.status_code == 200 else []
    except: return []

def db_ekle_gorev(data):
    requests.post(API_URL, json={"data": [data]})

def db_sil_gorev(task_id):
    requests.delete(f"{API_URL}/id/{task_id}")

def db_guncelle_gorev(task_id, data):
    requests.patch(f"{API_URL}/id/{task_id}", json={"data": [data]})