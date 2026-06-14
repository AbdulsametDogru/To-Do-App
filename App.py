import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği ve başlık
st.set_page_config(page_title="Görev Yönetimi", layout="wide", page_icon="to-do.png")
st.title("Görev Yönetimi")
# Kanban tarzında 3 sütunlu CSS stillerini ekle
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .main { background: #090a0f; }
    
    /* Kanban Sütun Yapısı */
    .kanban-column {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        min-height: 65vh;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Sütun Başlıkları */
    .column-header {
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        padding: 12px 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Premium Kart Tasarımları */
    .task-card {
        background: #131520;
        border: 1px solid #1f2235;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 15px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .task-card:hover {
        border-color: #3b82f6;
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5);
    }
    
    /* Sol Renk İndikatörleri */
    .indicator-Zor { background: #ef4444; width: 4px; position: absolute; left: 0; top: 0; bottom: 0; }
    .indicator-Orta { background: #f59e0b; width: 4px; position: absolute; left: 0; top: 0; bottom: 0; }
    .indicator-Kolay { background: #10b981; width: 4px; position: absolute; left: 0; top: 0; bottom: 0; }
    
    .task-title { color: #f3f4f6; font-size: 15px; font-weight: 600; margin-bottom: 8px; }
    
    /* Rozet Tasarımları */
    .badge { display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; margin-left: 6px; }
    .badge-Zor { background: rgba(239, 68, 68, 0.12); color: #f87171; }
    .badge-Orta { background: rgba(245, 158, 11, 0.12); color: #fbbf24; }
    .badge-Kolay { background: rgba(16, 185, 129, 0.12); color: #34d399; }
    
    .task-time { color: #9ca3af; font-size: 12px; margin-top: 14px; display: flex; justify-content: space-between; }
    hr { border: 0; height: 1px; background: #1f2235; margin: 15px 0 5px 0; }
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




