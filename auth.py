import hashlib
import database

class Auth:
    """Auth sınıfı, kullanıcı kayıt ve giriş işlemlerini yönetir."""
    @staticmethod
    def sifrele(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def kayit(username, password):
        users = database.db_getir_kullanicilar()
        if any(user["username"] == username for user in users):
            return False
        database.db_kullanici_ekle({
            "username": username, 
            "password": Auth.sifrele(password)
        })
        return True

    @staticmethod
    def giris(username, password):
        users = database.db_getir_kullanicilar()
        sifre_hash = Auth.sifrele(password)
        for user in users:
            if user.get("username") == username and user.get("password") == sifre_hash:
                return True
        return False