import streamlit as st
from Backend import GorevYoneticisi

st.set_page_config(page_title="Sprint Board Pro", layout="wide")

# CSS - Neon / Modern Tasarım
st.markdown("""
<style>
    .stApp { background-color: #0f1117; color: #ffffff; }
    .task-card { background: #1e1e2e; padding: 15px; border-radius: 12px; border-left: 5px solid #8b5cf6; margin-bottom: 15px; }
    h1, h2, h3 { color: #8b5cf6; }
    div.stButton > button { background-color: #8b5cf6; color: white; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

if "kullanici_adi" not in st.session_state:
    st.title("🚀 Sprint Board - Giriş")
    isim = st.text_input("Kullanıcı Adı:")
    if st.button("Sisteme Giriş Yap"):
        if isim:
            st.session_state.kullanici_adi = isim
            st.rerun()
    st.stop()

yon = GorevYoneticisi(st.session_state.kullanici_adi)

with st.sidebar:
    st.title("Kontrol Paneli")
    st.write(f"Aktif: **{st.session_state.kullanici_adi}**")
    with st.expander("➕ Yeni Görev Ekle", expanded=True):
        with st.form("yeni_gorev_formu"):
            yeni_ad = st.text_input("Görev Adı")
            yeni_durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
            yeni_tarih = st.date_input("Son Tarih")
            if st.form_submit_button("Kaydet"):
                yon.gorev_ekle(yeni_ad, yeni_durum, "Orta", str(yeni_tarih))
                st.rerun()
    if st.button("Çıkış Yap"):
        del st.session_state.kullanici_adi
        st.rerun()

st.title("Board Görünümü")
cols = st.columns(3)
durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]
for i, col in enumerate(cols):
    with col:
        st.subheader(durumlar[i])
        for g in [g for g in yon.gorevler if g.durum == durumlar[i]]:
            st.markdown(f"<div class='task-card'><b>{g.ad}</b><br><small>📅 {g.son_tarih}</small></div>", unsafe_allow_html=True)
            if st.button("Sil", key=f"sil_{g.id}"):
                yon.gorev_sil(g.id)
                st.rerun()