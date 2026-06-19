import streamlit as st
from Backend import GorevYoneticisi
import database
import datetime

# 1. Sayfa ayarları
st.set_page_config(page_title="Sprint Board Pro", layout="wide", initial_sidebar_state="expanded")

# 2. Hata ayıklama
def debug_panel():
    st.write("--- HATA AYIKLAMA PANELİ ---")
    try:
        data = database.db_getir_gorevler("f31faf1f-6445-49a9-a84a-888227f0597e")
        st.write(f"Veritabanından çekilen veri sayısı: {len(data)}")
    except Exception as e:
        st.error(f"Veritabanı bağlantı hatası: {e}")

debug_panel()

# 3. CSS Kısmı (Düzeltilmiş: f-string yerine düz string kullanıldı)
def render_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    *, *::before, *::after { font-family: 'Plus Jakarta Sans', sans-serif !important; box-sizing: border-box; }
    
    .stApp {
        background: linear-gradient(135deg, #1c183d 0%, #251b5a 40%, #162942 100%) !important;
        background-attachment: fixed !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b1347 0%, #100c24 100%) !important;
        border-right: 1px solid rgba(139,92,246,0.35) !important;
    }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 28px !important; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

render_css()

# 4. Fonksiyonel Kod
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()

yon = st.session_state.yonetici

@st.dialog("📝 Görevi Güncelle")
def gorev_duzenle(gorev):
    yeni_ad = st.text_input("Görev Adı", value=gorev.ad) 
    yeni_durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"], 
                              index=["Yapılacak", "Yapılıyor", "Tamamlandı"].index(gorev.durum))
    
    if st.button("💾 Kaydet"):
        gorev.ad = yeni_ad
        gorev.durum = yeni_durum
        yon.gorev_guncelle(gorev)
        st.rerun()

def gorev_sayilarini_hesapla():
    toplam = len(yon.gorevler)
    tamamlanan = len([x for x in yon.gorevler if x.durum == "Tamamlandı"])
    yapilan = len([x for x in yon.gorevler if x.durum == "Yapılıyor"])
    return toplam, tamamlanan, yapilan