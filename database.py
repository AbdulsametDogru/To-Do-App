import requests

# SheetDB'den aldığın o uzun "Endpoint URL" linkini buraya yapıştır
API_URL = "https://sheetdb.io/api/v1/buraya_aldigin_linki_yaz"

def db_getir_gorevler(user_id):
    # API'ye bağlanıp tüm verileri çekiyoruz
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return []

def db_ekle_gorev(data):
    # Yeni görevi Sheets'e gönderiyoruz
    requests.post(API_URL, json={"data": [data]})

def db_sil_gorev(task_id):
    # ID kullanarak ilgili satırı siliyoruz
    requests.delete(f"{API_URL}/id/{task_id}")

def db_guncelle_gorev(task_id, data):
    # ID kullanarak ilgili satırı güncelliyoruz
    requests.patch(f"{API_URL}/id/{task_id}", json={"data": [data]})