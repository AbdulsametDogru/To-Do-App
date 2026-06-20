import streamlit as st
from Backend import GorevYoneticisi

# Sayfa ayarları
st.set_page_config(page_title="Sprint Board Pro", layout="wide")

# CSS - Neon Tasarım
st.markdown("""
<style>
    .task-card { background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin: 10px 0; }
    .stButton>button { width: 100%; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# 1. Giriş Kontrolü
if "kullanici_adi" not in st.session_state:
    st.title("🚀 Sprint Board - Pro Login")
    isim = st.text_input("Kullanıcı Adı:")
    if st.button("Sisteme Giriş Yap"):
        if isim:
            st.session_state.kullanici_adi = isim
            st.rerun()
    st.stop()

# 2. Görev Yönetimi Nesnesi
yon = GorevYoneticisi(st.session_state.kullanici_adi)

# 3. Sidebar (Kontrol Paneli)
with st.sidebar:
    st.title("Kontrol Paneli")
    st.write(f"Aktif: **{st.session_state.kullanici_adi}**")
    
    with st.expander("➕ Yeni Görev Ekle", expanded=True):
        with st.form("yeni_gorev_formu"):
            yeni_ad = st.text_input("Görev Adı")
            yeni_durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
            yeni_zorluk = st.select_slider("Zorluk", ["Kolay", "Orta", "Zor"])
            yeni_tarih = st.date_input("Son Tarih")
            if st.form_submit_button("Kaydet"):
                yon.gorev_ekle(yeni_ad, yeni_durum, yeni_zorluk, str(yeni_tarih))
                st.success("Görev eklendi!")
                st.rerun()

    if st.button("Çıkış Yap"):
        del st.session_state.kullanici_adi
        st.rerun()

# 4. Ana Board (Kolonlar)
st.title("Board Görünümü")
cols = st.columns(3)
durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]

for i, col in enumerate(cols):
    with col:
        st.subheader(durumlar[i])
        for g in [g for g in yon.gorevler if g.durum == durumlar[i]]:
            with st.container():
                st.markdown(f"<div class='task-card'>", unsafe_allow_html=True)
                st.write(f"**{g.ad}**")
                st.caption(f"Zorluk: {g.zorluk} | Tarih: {g.son_tarih}")
                
                # Güncelleme ve Silme
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Sil", key=f"sil_{g.id}"):
                        yon.gorev_sil(g.id)
                        st.rerun()
                with c2:
                    yeni_durum = st.selectbox("Taşı", durumlar, index=durumlar.index(g.durum), key=f"tasima_{g.id}")
                    if yeni_durum != g.durum:
                        g.durum = yeni_durum
                        yon.gorev_guncelle(g.id, g.__dict__)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)