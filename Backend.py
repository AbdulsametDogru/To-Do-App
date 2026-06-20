import uuid
import database

class Gorev:
    def __init__(self, ad, durum, zorluk, son_tarih, user_id, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.ad, self.durum, self.zorluk, self.son_tarih, self.user_id = ad, durum, zorluk, son_tarih, user_id

class GorevYoneticisi:
    def __init__(self, kullanici_adi):
        self.kullanici = kullanici_adi
        data = database.db_getir_gorevler()
        self.gorevler = [Gorev(**d) for d in data if d.get('user_id') == kullanici_adi]

    def gorev_ekle(self, ad, durum, zorluk, son_tarih):
        yeni_id = str(uuid.uuid4())
        yeni_data = {"id": yeni_id, "ad": ad, "durum": durum, "zorluk": zorluk, "son_tarih": son_tarih, "user_id": self.kullanici}
        database.db_ekle_gorev(yeni_data)
        self.gorevler.append(Gorev(ad, durum, zorluk, son_tarih, self.kullanici, yeni_id))

    def gorev_sil(self, task_id):
        database.db_sil_gorev(task_id)
        self.gorevler = [g for g in self.gorevler if g.id != task_id]