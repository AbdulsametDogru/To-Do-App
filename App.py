import streamlit as st
from Backend import GorevYoneticisi
from datetime import date

st.set_page_config(page_title="Neon Sprint Board", layout="wide")

# Şık Neon CSS Tasarımı
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp { background-color: #0d1117; font-family: 'Inter', sans-serif; }
    
    /* Kolon Başlıkları */
    .column-header {
        padding: 12px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .header-todo { background: linear-gradient(90deg, #1e40af, #3b82f6); border-bottom: 3px solid #60a5fa; }
    .header-doing { background: linear-gradient(90deg, #991b1b, #ef4444); border-bottom: 3px solid #f87171; }
    .header-done { background: linear-gradient(90deg, #065f46, #10b981); border-bottom: 3px solid #34d399; }

    /* Görev Kartları */
    .task-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .task-card:hover { transform: translateY(-3px); border-color: #8b5cf6; }
    
    .task-title { color: #f0f6fc; font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }
    
    /* Rozetler (Badges) */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-right: 5px;
    }
    .badge-date { background: #238636; color: #ffffff; }
    .badge-urgent { background: #da3633; color: #ffffff; }
    .badge-info { background: #1f6feb; color: #ffffff; }

    /* Butonlar */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# Giriş Kontrolü
if "kullanici_adi" not in st.session_state:
    st.title("⚡ Cyber-Sprint Giriş")
    isim = st.text_input("Giriş yapın:")
    if st.button("Başla"):
        if isim:
            st.session_state.kullanici_adi = isim
            st.rerun()
    st.stop()

yon = GorevYoneticisi(st.session_state.kullanici_adi)

# Sidebar - Kontrol Paneli
with st.sidebar:
    st.title("⚙️ Panel")
    st.info(f"Hoş geldin: **{st.session_state.kullanici_adi}**")
    
    with st.expander("➕ Yeni Görev", expanded=True):
        with st.form("yeni_ekle"):
            ad = st.text_input("Görev Adı")
            durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
            zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"])
            tarih = st.date_input("Teslim", value=date.today())
            if st.form_submit_button("Listeye Ekle"):
                yon.gorev_ekle(ad, durum, zorluk, str(tarih))
                st.rerun()
    
    if st.button("Çıkış Yap"):
        del st.session_state.kullanici_adi
        st.rerun()

# Ana Board
st.title("🚀 Proje Takip Dashboard")

cols = st.columns(3)
durum_listesi = ["Yapılacak", "Yapılıyor", "Tamamlandı"]
st_header_classes = ["header-todo", "header-doing", "header-done"]

for i, col in enumerate(cols):
    with col:
        st.markdown(f"<div class='column-header {st_header_classes[i]}'>{durum_listesi[i]}</div>", unsafe_allow_html=True)
        
        filtreli_gorevler = [g for g in yon.gorevler if g.durum == durum_listesi[i]]
        
        for g in filtreli_gorevler:
            kalangun = g.gun_kaldi()
            date_badge = "badge-urgent" if kalangun <= 2 else "badge-date"
            
            with st.container():
                st.markdown(f"""
                <div class='task-card'>
                    <div class='task-title'>{g.ad}</div>
                    <div>
                        <span class='badge {date_badge}'>📅 {g.son_tarih}</span>
                        <span class='badge badge-info'>{kalangun} gün kaldı</span>
                        <span class='badge' style='background:#30363d;'>{g.zorluk}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([1, 1])
                with c1:
                    if st.button("🗑️ Sil", key=f"s_{g.id}"):
                        yon.gorev_sil(g.id)
                        st.rerun()
                with c2:
                    yeni_dur = st.selectbox("➡️", durum_listesi, index=dur_index if (dur_index := durum_listesi.index(g.durum)) else 0, key=f"d_{g.id}", label_visibility="collapsed")
                    if yeni_dur != g.durum:
                        yon.gorev_guncelle(g.id, {"durum": yeni_dur})
                        st.rerun()