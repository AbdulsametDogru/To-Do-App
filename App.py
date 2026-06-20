import streamlit as st
from Backend import GorevYoneticisi
from datetime import date

# Sayfa Yapılandırması
st.set_page_config(page_title="Neon Sprint Board", layout="wide")

# CSS - Cyber-Neon Tasarımı
st.markdown("""
<style>
    /* Arka Plan: Mor-Mavi-Kırmızı Derinlikli Gradient */
    .stApp { 
        background: radial-gradient(circle at 70% 30%, #581c87, #0f172a),
                    radial-gradient(circle at 20% 80%, #991b1b, #0f172a);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    /* Yan Panel - Cam Efekti */
    [data-testid="stSidebar"] {
        background: rgba(30, 30, 46, 0.4) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid #8b5cf6;
    }

    /* Görev Kartları - Neon Glow */
    .task-card {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.2);
        transition: 0.3s;
    }
    .task-card:hover { box-shadow: 0 0 25px rgba(139, 92, 246, 0.5); border-color: #8b5cf6; }
    
    /* Sütun Başlıkları */
    .col-header {
        text-align: center; font-weight: 800; padding: 12px; border-radius: 10px;
        margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1.5px;
        color: white; font-size: 1.1rem;
    }
    .todo-header { background: linear-gradient(90deg, #1e40af, #3b82f6); }
    .doing-header { background: linear-gradient(90deg, #991b1b, #ef4444); }
    .done-header { background: linear-gradient(90deg, #065f46, #10b981); }
</style>
""", unsafe_allow_html=True)

# 1. Giriş Kontrolü
if "kullanici_adi" not in st.session_state:
    st.markdown("<h1 style='text-align:center; color:#8b5cf6;'>⚡ Cyber-Sprint Giriş</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        isim = st.text_input("Kullanıcı Adı:")
        if st.button("Sisteme Giriş Yap"):
            if isim:
                st.session_state.kullanici_adi = isim
                st.rerun()
    st.stop()

# 2. Yöneticiyi Başlat
yon = GorevYoneticisi(st.session_state.kullanici_adi)

# 3. Sidebar
with st.sidebar:
    st.header("Kontrol Paneli")
    st.write(f"Aktif Kullanıcı: **{st.session_state.kullanici_adi}**")
    st.divider()
    
    with st.expander("➕ Yeni Görev Ekle", expanded=True):
        with st.form("yeni_form"):
            ad = st.text_input("Görev Adı")
            durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
            zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"])
            tarih = st.date_input("Son Gün", value=date.today())
            if st.form_submit_button("Kaydet"):
                yon.gorev_ekle(ad, durum, zorluk, str(tarih))
                st.rerun()
    
    if st.button("Çıkış Yap"):
        del st.session_state.kullanici_adi
        st.rerun()

# 4. Ana Board
st.markdown("<h1 style='text-align:center;'>Board Görünümü</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

cols = st.columns(3)
durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]
st_styles = ["todo-header", "doing-header", "done-header"]

for i, col in enumerate(cols):
    with col:
        st.markdown(f"<div class='col-header {st_styles[i]}'>{durumlar[i]}</div>", unsafe_allow_html=True)
        
        for g in [g for g in yon.gorevler if g.durum == durumlar[i]]:
            st.markdown(f"""
            <div class='task-card'>
                <h3 style='margin:0; font-size:1.2rem'>{g.ad}</h3>
                <p style='color:#a1a1aa; margin:10px 0;'>📅 {g.son_tarih} | {g.zorluk}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Sil", key=f"del_{g.id}"):
                    yon.gorev_sil(g.id)
                    st.rerun()
            with c2:
                yeni_dur = st.selectbox("Taşı", durumlar, index=durumlar.index(g.durum), key=f"move_{g.id}", label_visibility="collapsed")
                if yeni_dur != g.durum:
                    yon.gorev_guncelle(g.id, {"durum": yeni_dur})
                    st.rerun()