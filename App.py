import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği ve başlık
st.set_page_config(page_title="Görev Yönetimi", layout="wide", page_icon="to-do.png")
st.title("Görev Yönetimi")
# Kanban tarzında 3 sütunlu CSS stillerini ekle
st.markdown("""
    <style>
        .kanban-column {
            display: inline-block;
            vertical-align: top;
            width: 30%;
            margin-right: 1%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .kanban-column h2 {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Görev yöneticisi nesnesini oluştur
gorev_yoneticisi = GorevYoneticisi()

# Görev ekleme formu
with st.form("gorev_ekle_formu"):
    st.subheader("Yeni Görev Ekle")
    ad = st.text_input("Görev Adı")
    durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
    zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"])
    son_tarih = st.date_input("Son Tarih (GG/AA/YYYY)", min_value=datetime.date.today())
    submit_button = st.form_submit_button(label="Görev Ekle")

    if submit_button:
        # Tarihi GG/AA/YYYY formatına çevir
        son_tarih_str = son_tarih.strftime("%d/%m/%Y")
        gorev_yoneticisi.gorev_ekle(ad, durum, zorluk, son_tarih_str)
        st.success(f"'{ad}' adlı görev eklendi.")

# Görevleri Kanban tarzında göster
st.subheader("Görevler")

# Görevleri duruma göre sütunlara ayır
yapilacaklar = gorev_yoneticisi.gorevleri_getir(durum="Yapılacak")
yapiliyorlar = gorev_yoneticisi.gorevleri_getir(durum="Yapılıyor")
tamamlanmislar = gorev_yoneticisi.gorevleri_getir(durum="Tamamlandı")

# Her bir sütun için görevleri göster
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='kanban-column'><h2>Yapılacak</h2>", unsafe_allow_html=True)
        for gorev in yapilacaklar:
            st.write(f"- {gorev['ad']}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='kanban-column'><h2>Yapılıyor</h2>", unsafe_allow_html=True)
        for gorev in yapiliyorlar:
            st.write(f"- {gorev['ad']}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='kanban-column'><h2>Tamamlandı</h2>", unsafe_allow_html=True)
        for gorev in tamamlanmislar:
            st.write(f"- {gorev['ad']}")
        st.markdown("</div>", unsafe_allow_html=True)




