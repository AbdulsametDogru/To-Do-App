import streamlit as st
from Backend import GorevYoneticisi
import database
import datetime

# 1. Sayfa ayarları
st.set_page_config(page_title="Sprint Board Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Kısmı
def render_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    *, *::before, *::after { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #1c183d 0%, #251b5a 40%, #162942 100%) !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1b1347 0%, #100c24 100%) !important; border-right: 1px solid rgba(139,92,246,0.35) !important; }
    .col-header { font-size: 14px; font-weight: 800; color: #fff; margin-bottom: 20px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; text-align: center; }
    .task-card { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1); }
    .task-title { color: #fff; font-weight: 600; margin-bottom: 5px; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

render_css()

# 3. Yönetici Başlatma
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()
yon = st.session_state.yonetici

# 4. Sidebar Formu
with st.sidebar:
    st.title("⚡ Kontrol Merkezi")
    with st.form("gorev_ekle_form", clear_on_submit=True):
        yeni_gorev = st.text_input("Görev Tanımı")
        durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
        zorluk = st.selectbox("Öncelik", ["Kolay", "Orta", "Zor"])
        son_tar = st.date_input("Deadline")
        
        if st.form_submit_button("🚀 Görevi Ekle"):
            if yeni_gorev:
                yon.gorev_ekle(yeni_gorev, durum, zorluk, son_tar.strftime("%d/%m/%Y"))
                st.rerun()
            else:
                st.error("Görev adı boş olamaz!")

# 5. Ana Ekran Board
col1, col2, col3 = st.columns(3)

# Sütunları döngüyle temiz bir şekilde oluştur
for col, durum_adi in zip([col1, col2, col3], ["Yapılacak", "Yapılıyor", "Tamamlandı"]):
    with col:
        st.markdown(f"<div class='col-header'>{durum_adi}</div>", unsafe_allow_html=True)
        
        gorevler = [g for g in yon.gorevler if g.durum == durum_adi]
        
        if gorevler:
            for gorev in gorevler:
                st.markdown(f"""
                    <div class='task-card'>
                        <div class='task-title'>{gorev.ad}</div>
                        <div style='color: #aaa; font-size: 12px;'>{gorev.zorluk} | {gorev.deadline}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Görev yok")

# 6. Fonksiyonlar
@st.dialog("📝 Görevi Güncelle")
def gorev_duzenle(gorev):
    yeni_ad = st.text_input("Görev Adı", value=gorev.ad) 
    yeni_durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"], index=["Yapılacak", "Yapılıyor", "Tamamlandı"].index(gorev.durum))
    if st.button("💾 Kaydet"):
        gorev.ad = yeni_ad
        gorev.durum = yeni_durum
        yon.gorev_guncelle(gorev)
        st.rerun()