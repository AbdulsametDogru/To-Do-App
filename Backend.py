import uuid
import database
from datetime import datetime

class Gorev:
    def __init__(self, ad, durum, zorluk, son_tarih, user_id, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.ad = ad
        self.durum = durum
        self.zorluk = zorluk
        self.son_tarih = son_tarih
        self.user_id = user_id

    def gun_kaldi(self):
        try:
            hedef = datetime.strptime(self.son_tarih, "%Y-%m-%d")
            bugun = datetime.now()
            fark = (hedef - bugun).days + 1
            return fark
        except:
            return 0

class GorevYoneticisi:
    def __init__(self, kullanici_adi):
        self.kullanici = kullanici_adi
        data = database.db_getir_gorevler()
        self.gorevler = [Gorev(**d) for d in data if d.get('user_id') == kullanici_adi]

    def gorev_ekle(self, ad, durum, zorluk, son_tarih):
        yeni_id = str(uuid.uuid4())
        yeni_data = {
            "id": yeni_id, 
            "ad": ad, 
            "durum": durum, 
            "zorluk": zorluk, 
            "son_tarih": son_tarih, 
            "user_id": self.kullanici
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
                g.durum = yeni_data.get('durum', g.durum)
                break