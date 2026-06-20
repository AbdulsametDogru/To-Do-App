import streamlit as st
from Backend import GorevYoneticisi
import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sprint Board Pro", layout="wide")

# 2. CSS Tasarımı
def render_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #1c183d 0%, #251b5a 40%, #162942 100%) !important; color: white; }
    .col-header { font-size: 14px; font-weight: 800; color: #fff; margin-bottom: 20px; padding: 12px; background: rgba(255,255,255,0.08); border-radius: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
    .task-card { background: rgba(255,255,255,0.05); padding: 16px; border-radius: 14px; margin-bottom: 12px; border: 1px solid rgba(139, 92, 246, 0.5); transition: 0.3s; }
    .task-card:hover { border-color: #a78bfa; }
    .task-title { color: #fff; font-weight: 700; margin-bottom: 8px; font-size: 15px; }
    .task-meta { color: #a78bfa; font-size: 12px; font-weight: 600; display: flex; justify-content: space-between; }
    </style>
    """, unsafe_allow_html=True)

render_css()

# 3. Yönetici Başlatma
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()
yon = st.session_state.yonetici

# 4. Modallar
@st.dialog("📝 Görevi Güncelle")
def gorev_duzenle(gorev):
    yeni_ad = st.text_input("Görev Adı", value=gorev.ad) 
    yeni_durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"], index=["Yapılacak", "Yapılıyor", "Tamamlandı"].index(gorev.durum))
    yeni_zorluk = st.selectbox("Öncelik", ["Kolay", "Orta", "Zor"], index=["Kolay", "Orta", "Zor"].index(gorev.zorluk))
    
    if st.button("💾 Kaydet"):
        gorev.ad = yeni_ad
        gorev.durum = yeni_durum
        gorev.zorluk = yeni_zorluk
        yon.gorev_guncelle(gorev)
        st.rerun()

# 5. Sidebar
with st.sidebar:
    st.title("⚡ Kontrol Merkezi")
    with st.form("gorev_ekle_form", clear_on_submit=True):
        yeni_gorev = st.text_input("Görev Tanımı")
        durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
        zorluk = st.selectbox("Öncelik", ["Kolay", "Orta", "Zor"])
        son_tar = st.date_input("Deadline")
        
        if st.form_submit_button("🚀 Görevi Ekle"):
            if yeni_gorev:
                # Tarih hatasını engellemek için %Y-%m-%d formatı
                yon.gorev_ekle(yeni_gorev, durum, zorluk, son_tar.strftime("%Y-%m-%d"))
                st.rerun()

# 6. Ana Ekran Board
col1, col2, col3 = st.columns(3)

for col, durum_adi in zip([col1, col2, col3], ["Yapılacak", "Yapılıyor", "Tamamlandı"]):
    with col:
        st.markdown(f"<div class='col-header'>{durum_adi.upper()}</div>", unsafe_allow_html=True)
        
        # Sadece ilgili sütuna ait görevleri filtrele
        gorevler = [g for g in yon.gorevler if g.durum == durum_adi]
        
        if gorevler:
            for gorev in gorevler:
                st.markdown(f"""
                    <div class='task-card'>
                        <div class='task-title'>{gorev.ad}</div>
                        <div class='task-meta'>
                            <span>{gorev.zorluk}</span>
                            <span>📅 {gorev.son_tarih}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Butonlar
                b1, b2 = st.columns(2)
                if b1.button("✏️ Düzenle", key=f"edit_{gorev.id}"):
                    gorev_duzenle(gorev)
                if b2.button("🗑️ Sil", key=f"del_{gorev.id}"):
                    yon.gorev_sil(gorev.id)
                    st.rerun()
        else:
            st.info("Görev yok.")