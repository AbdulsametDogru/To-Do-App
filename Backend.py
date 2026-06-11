import uuid
import json
import os
import datetime

class Gorev:
    """Gorev sınıfı görevlerin özelliklerini tanımlar"""
    def __init__(self, ad, durum, zorluk, son_tarih, id=None):
        self.id = str(uuid.uuid4())
        self.ad = ad
        self.durum = durum
        self.zorluk = zorluk
        self.son_tarih = son_tarih #GG/AA/YYYY formatında

    def kalan_gun(self):
        """Görevin kalan gün sayısını hesaplar"""
        try:
            son_tarih_dt = datetime.datetime.strptime(self.son_tarih, "%d/%m/%Y")
            bugun = datetime.datetime.now()
            kalan = (son_tarih_dt - bugun).days
            return kalan
        except ValueError:
            return "Geçersiz tarih formatı. GG/AA/YYYY formatında olmalıdır."
        
    def to_dict(self):
        """Görevi sözlük formatına çevirir"""
        return {
            "id": self.id,
            "ad": self.ad,
            "durum": self.durum,
            "zorluk": self.zorluk,
            "son_tarih": self.son_tarih
        }
    @classmethod
    def from_dict(cls, data):
        """Sözlükten Görev nesnesi oluşturur"""
        return cls(
            id=data["id"],
            ad=data["ad"],
            durum=data["durum"],
            zorluk=data["zorluk"],
            son_tarih=data["son_tarih"]
        )