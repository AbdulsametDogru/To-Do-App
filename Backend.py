import uuid
import database
import datetime

class Gorev:
    def __init__(self, ad, durum, zorluk, son_tarih, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.ad = ad
        self.durum = durum
        self.zorluk = zorluk
        self.son_tarih = son_tarih 

    def to_dict(self):
        return {"id": self.id, "ad": self.ad, "durum": self.durum, "zorluk": self.zorluk, "son_tarih": self.son_tarih}

class GorevYoneticisi:
    def __init__(self, user_id="f31faf1f-6445-49a9-a84a-888227f0597e"):
        self.user_id = user_id
        data = database.db_getir_gorevler(self.user_id)
        self.gorevler = [Gorev(**d) for d in data]

    def gorev_ekle(self, ad, durum, zorluk, son_tarih):
        yeni_id = str(uuid.uuid4())
        yeni_data = {"id": yeni_id, "ad": ad, "durum": durum, "zorluk": zorluk, "son_tarih": son_tarih, "user_id": self.user_id}
        database.db_ekle_gorev(yeni_data)
        self.gorevler.append(Gorev(ad, durum, zorluk, son_tarih, id=yeni_id))

    def gorev_sil(self, id):
        database.db_sil_gorev(id)
        self.gorevler = [g for g in self.gorevler if g.id != id]

    def gorev_guncelle(self, g):
        database.db_guncelle_gorev(g.id, g.to_dict())
        data = database.db_getir_gorevler(self.user_id)
        self.gorevler = [Gorev(**d) for d in data]