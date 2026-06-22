import requests
import os
import streamlit as st

TASKS_URL = st.secrets.get("SHEETDB_TASKS") or os.getenv("SHEETDB_TASKS")
USERS_URL = st.secrets.get("SHEETDB_USERS") or os.getenv("SHEETDB_USERS")

# Görevler

def db_getir_gorevler():
    try:
        response = requests.get(TASKS_URL)
        return response.json() if response.status_code == 200 else []
    except:
        return []

def db_ekle_gorev(data):
    requests.post(TASKS_URL, json={"data": [data]})

def db_sil_gorev(task_id):
    requests.delete(f"{TASKS_URL}/id/{task_id}")

def db_guncelle_gorev(task_id, data):
    requests.patch(
        f"{TASKS_URL}/id/{task_id}",
        json={"data": [data]}
    )

# Kullanıcılar

def db_getir_kullanicilar():
    try:
        response = requests.get(USERS_URL)
        return response.json() if response.status_code == 200 else []
    except:
        return []

def db_kullanici_ekle(data):
    requests.post(
        USERS_URL,
        json={"data": [data]}
    )