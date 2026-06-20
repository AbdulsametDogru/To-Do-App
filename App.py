import streamlit as st
from Backend import GorevYoneticisi
from datetime import date

# Sayfa Yapılandırması
st.set_page_config(page_title="Neon Sprint Board Pro", layout="wide")

# CSS - Gelişmiş Neon Tasarımı
st.markdown("""
<style>
    /* Arka Plan Gradient */
    .stApp { 
        background: radial-gradient(circle at 70% 30%, #581c87, #0f172a),
                    radial-gradient(circle at 20% 80%, #991b1b, #0f172a);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    /* Yan Panel - Cam Efekti */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid #8b5cf6;
    }

    /* Genel Kart Yapısı */
    .task-card {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 5px;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s;
    }

    /* Duruma Göre Renkli Neon Glow Efektleri */
    .card-todo { box-shadow: 0 0 15px rgba(59, 130, 246, 0.4); border-left: 5px solid #3b82f6; }
    .card-doing { box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); border-left: 5px solid #ef4444; }
    .card-done { box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); border-left: 5px solid #10b981; }
    
    /* Kart Başlıkları */
    .task-title { font-size: 1.2rem; font-weight: bold; margin-bottom: 8px; color: #f8fafc; }
    .task-info { font-size: 0.85rem; color: #94a3b8; margin-bottom: 5px; }

    /* Kolon Başlıkları */
    .col-header {
        text-align: center; font-weight: 800; padding: 12px; border-radius: 10px;
        margin-bottom: 25px; text-transform: uppercase; letter-spacing: 1.5px;
        color: white; font-size: 1.1rem;
    }
    .todo-h { background: linear-gradient(90deg, #1e40af, #3b82f6); box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }
    .doing-h { background: linear-gradient(90deg, #991b1b, #ef4444); box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3); }
    .done-h { background: linear-gradient(90deg, #065f46, #10b981); box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); }

    /* Buton Tasarımları */
    .stButton>button { width: 100%; border-radius: 8px; height: 35px; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# Giriş Kontrolü
if "kullanici_adi" not in st.session_state:
    st.markdown("<h1 style='text-align:center; color:#8b5cf6; margin-top:100px;'>⚡ Cyber-Sprint Login</h1>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 1.5, 1])
    with col_b:
        isim = st.text_input("Kimliğinizi Girin:")
        if st.button("Sisteme Eriş"):
            if isim:
                st.session_state.kullanici_adi = isim
                st.rerun()
    st.stop()

yon = GorevYoneticisi(st.session_state.kullanici_adi)

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.kullanici_adi}")
    st.divider()
    with st.expander("➕ Yeni Görev Tanımla", expanded=True):
        with st.form("yeni_form"):
            ad = st.text_input("Görev İsmi")
            durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
            zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"])
            tarih = st.date_input("Teslim Tarihi")
            if st.form_submit_button("Veritabanına İşle"):
                yon.gorev_ekle(ad, durum, zorluk, str(tarih))
                st.rerun()
    if st.button("Güvenli Çıkış"):
        del st.session_state.kullanici_adi
        st.rerun()

# Ana Board
st.markdown("<h1 style='text-align:center; letter-spacing:2px;'>SPRINT CONTROL CENTER</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

cols = st.columns(3)
durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]
css_headers = ["todo-h", "doing-h", "done-h"]
card_colors = ["card-todo", "card-doing", "card-done"]

for i, col in enumerate(cols):
    with col:
        st.markdown(f"<div class='col-header {css_headers[i]}'>{durumlar[i]}</div>", unsafe_allow_html=True)
        
        # Kullanıcının görevlerini filtrele
        gorevler = [g for g in yon.gorevler if g.durum == durumlar[i]]
        
        for g in gorevler:
            # Kart Görünümü (HTML)
            st.markdown(f"""
            <div class='task-card {card_colors[i]}'>
                <div class='task-title'>{g.ad}</div>
                <div class='task-info'>📅 Son Gün: {g.son_tarih}</div>
                <div class='task-info'>🔥 Zorluk: {g.zorluk}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # İşlem Butonları (Kartın hemen altında)
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                # Güncelleme/Taşıma Dropdown
                yeni_dur = st.selectbox("Taşı", durumlar, index=durumlar.index(g.durum), key=f"m_{g.id}", label_visibility="collapsed")
                if yeni_dur != g.durum:
                    yon.gorev_guncelle(g.id, {"durum": yeni_dur})
                    st.rerun()
            with b_col2:
                # Silme Butonu
                if st.button("🗑️ Sil", key=f"d_{g.id}"):
                    yon.gorev_sil(g.id)
                    st.rerun()
            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)