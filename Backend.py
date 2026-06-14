import uuid
import json
import os
import datetime

class Gorev:
    """Gorev sınıfı görevlerin özelliklerini tanımlar"""
    def __init__(self, ad, durum, zorluk, son_tarih, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.ad = ad
        self.durum = durum
        self.zorluk = zorluk
        self.son_tarih = son_tarih  # GG/AA/YYYY formatında

    def kalan_gun_hesapla(self):
        """Görevin kalan gün sayısını tam sayı olarak hesaplar"""
        try:
            son_tarih_dt = datetime.datetime.strptime(self.son_tarih, "%d/%m/%Y").date()
            bugun = datetime.date.today()
            return (son_tarih_dt - bugun).days
        except ValueError:
            return 0
        
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
    
class GorevYoneticisi:
    """GorevYoneticisi sınıfı görevleri yönetmek için gerekli metodları içerir"""
    def __init__(self, dosya_adi="gorevler.json"):
        self.dosya_adi = dosya_adi
        self.gorevler = self.gorevleri_yukle()

    def gorevleri_yukle(self):
        """Görevleri JSON dosyasından yükler"""
        try:
            if os.path.exists(self.dosya_adi):
                with open(self.dosya_adi, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [Gorev.from_dict(gorev) for gorev in data]
        except Exception as e:
            print(f"Hata oluştu: {e}")
        return []

    def gorevleri_kaydet(self):
        """Görevleri JSON dosyasına kaydeder"""
        try:
            with open(self.dosya_adi, "w", encoding="utf-8") as f:
                json.dump([gorev.to_dict() for gorev in self.gorevler], f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Hata oluştu: {e}")

    def gorev_ekle(self, ad, durum, zorluk, son_tarih):
        """Yeni bir görev ekler"""
        yeni_gorev = Gorev(ad, durum, zorluk, son_tarih)
        self.gorevler.append(yeni_gorev)
        self.gorevleri_kaydet()
        return yeni_gorev
    
    def gorev_sil(self, gorev_id):
        """Belirtilen ID'ye sahip görevi siler"""
        self.gorevler = [gorev for gorev in self.gorevler if gorev.id != gorev_id]
        self.gorevleri_kaydet()

    def gorevleri_sirala(self):
        """Görevleri önce yakın tarihe, tarihler eşitse zorluk derecesine göre akıllı sıralar"""
        zorluk_map = {"Zor": 3, "Orta": 2, "Kolay": 1}
        self.gorevler.sort(
            key=lambda x: (
                datetime.datetime.strptime(x.son_tarih, "%d/%m/%Y"),
                -zorluk_map.get(x.zorluk, 0)
            )
        )