import uuid
import database
from datetime import datetime
import streamlit as st

class Gorev:
    def __init__(self, ad, durum, zorluk, son_tarih, user_id, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.ad = ad
        self.durum = durum
        self.zorluk = zorluk
        self.son_tarih = son_tarih
        self.user_id = user_id

class GorevYoneticisi:
    def __init__(self, kullanici_adi):
        self.kullanici = kullanici_adi
        # Veriyi her seferinde taze çekmesi için ttl=0 kullanıyoruz
        data = self.get_data_with_refresh()
        self.gorevler = [Gorev(**d) for d in data if d.get("user_id") == kullanici_adi]
        self.gorevleri_sirala()
        
    def gorevleri_sirala(self):
        zorluk_oncelik = {
            "Zor": 0,
            "Orta": 1,
            "Kolay": 2
        }

        self.gorevler.sort(
            key=lambda g: (
                datetime.strptime(g.son_tarih, "%Y-%m-%d"),
                zorluk_oncelik.get(g.zorluk, 99)
            )
        )

    @st.cache_data(ttl=0) # ttl=0, verinin asla cache'lenmemesini sağlar
    def get_data_with_refresh(_self):
        return database.db_getir_gorevler()
    
    def gorev_ekle(self, ad, durum, zorluk, son_tarih):
        if not ad.strip(): raise ValueError("Görev adı boş olamaz.")
        yeni_data = {
            "id": str(uuid.uuid4()), "ad": ad, "durum": durum,
            "zorluk": zorluk, "son_tarih": son_tarih, "user_id": self.kullanici
        }
        database.db_ekle_gorev(yeni_data)
        self.gorevler.append(Gorev(**yeni_data))

    def gorev_sil(self, task_id):
        database.db_sil_gorev(task_id)
        self.gorevler = [g for g in self.gorevler if g.id != task_id]

    def gorev_guncelle(self, task_id, yeni_data):
        database.db_guncelle_gorev(task_id, yeni_data)
        for g in self.gorevler:
            if g.id == task_id:
                g.ad = yeni_data.get("ad", g.ad)
                g.durum = yeni_data.get("durum", g.durum)
                g.zorluk = yeni_data.get("zorluk", g.zorluk)
                g.son_tarih = yeni_data.get("son_tarih", g.son_tarih)
                break