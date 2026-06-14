import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği ve başlık ayarları
st.set_page_config(page_title="Enterprise Task Board Pro", layout="wide", page_icon="⚡")

# --- CSS: SADECE ANA PANO SÜTUNLARINI VÖ ÖZEL METİNLERİ HEDEF ALAN TASARIM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .main { background: #090a0f; }
    
    /* Yalnızca en dıştaki 3 ana Kanban sütununu gri kutu yapıyoruz */
    [data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        min-height: 70vh !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Sütun Başlıkları */
    .column-header {
        font-size: 14px;
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
    
    /* Container (Kart) Çerçeve Özelleştirmesi */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #131520 !important;
        border: 1px solid #1f2235 !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        padding: 0px !important;
    }
    
    /* Kart İçeriği Esneklik Ayarları */
    .task-card-content {
        padding: 14px 14px 4px 14px;
        position: relative;
    }
    
    .task-title-area {
        color: #f3f4f6;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Rozetler */
    .badge { padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; }
    .badge-Zor { background: rgba(239, 68, 68, 0.12); color: #f87171; }
    .badge-Orta { background: rgba(245, 158, 11, 0.12); color: #fbbf24; }
    .badge-Kolay { background: rgba(16, 185, 129, 0.12); color: #34d399; }
    
    .task-time-area {
        color: #9ca3af;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    
    /* Streamlit Bileşenlerini Kart Yapısına Sabitleme */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1a1d2e !important;
        border: 1px solid #2d314e !important;
        border-radius: 8px !important;
    }
    .stButton > button {
        width: 100% !important;
        background-color: #1a1d2e !important;
        border: 1px solid #2d314e !important;
        border-radius: 8px !important;
        color: #ef4444 !important;
    }
    .stButton > button:hover {
        border-color: #ef4444 !important;
        background-color: rgba(239, 68, 68, 0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum yönetimi hafıza kontrolü
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()

gorev_yoneticisi = st.session_state.yonetici

# --- ÜST PANEL ANALİTİKLERİ ---
toplam_gorev = len(gorev_yoneticisi.gorevler)
tamamlanan_gorev = len([x for x in gorev_yoneticisi.gorevler if x.durum == "Tamamlandı"])
yapilan_gorev = len([x for x in gorev_yoneticisi.gorevler if x.durum == "Yapılıyor"])
ilerleme_orani = (tamamlanan_gorev / toplam_gorev) if toplam_gorev > 0 else 0.0

st.markdown("""
    <div style='margin-bottom: 20px;'>
        <h1 style='color: #fff; font-weight: 700; font-size: 26px; margin-bottom: 5px;'>Workspace / <span style='color: #3b82f6;'>Sprint Board Pro</span></h1>
        <p style='color: #4b5563; margin: 0; font-size: 13px;'>Bileşenlerin container yapısıyla mühürlendiği sade ve kararlı sürüm.</p>
    </div>
""", unsafe_allow_html=True)

# Üst Metrik Çubukları
m1, m2, m3, m4 = st.columns([2, 1, 1, 1])
with m1:
    st.markdown(f"<p style='color:#9ca3af; font-size:12px; margin-bottom:4px;'>Sprint İlerleme Durumu: {int(ilerleme_orani*100)}%</p>", unsafe_allow_html=True)
    st.progress(ilerleme_orani)
with m2:
    st.metric("Toplam Görev", toplam_gorev)
with m3:
    st.metric("Yapılıyor", yapilan_gorev)
with m4:
    st.metric("Tamamlandı", tamamlanan_gorev)

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# --- PANEL KONTROL MERKEZİ (SIDEBAR) ---
st.sidebar.markdown("<h3 style='color: #fff; font-weight: 700; margin-bottom:20px;'>Kontrol Merkezi</h3>", unsafe_allow_html=True)

with st.sidebar.form("gorev_ekle_formu", clear_on_submit=True):
    ad = st.text_input("Görev Adı")
    durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
    zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"])
    son_tarih = st.date_input("Son Tarih", min_value=datetime.date.today())
    submit_button = st.form_submit_button(label="Görev Ekle")

    if submit_button:
        if ad.strip():
            son_tarih_str = son_tarih.strftime("%d/%m/%Y")
            gorev_yoneticisi.gorev_ekle(ad, durum, zorluk, son_tarih_str)
            st.rerun()

# Görevleri akıllı sıralamaya tabi tutuyoruz
gorev_yoneticisi.gorevleri_sirala()

# --- SÜTUNLARIN OLUŞTURULMASI ---
sutun1, sutun2, sutun3 = st.columns(3)

sutun_ayarlari = {
    "Yapılacak": (sutun1, "Yapılacaklar", "linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%)"),
    "Yapılıyor": (sutun2, "Yapılıyor Olanlar", "linear-gradient(90deg, #9a3412 0%, #c2410c 100%)"),
    "Tamamlandı": (sutun3, "Tamamlananlar", "linear-gradient(90deg, #065f46 0%, #047857 100%)")
}

for anahtar, (st_sutun, baslik, renk) in sutun_ayarlari.items():
    # Doğrudan yöneticideki tüm görevleri filtrelemeden çekiyoruz
    sutun_gorevleri = [x for x in gorev_yoneticisi.gorevler if x.durum == anahtar]
    sayac = len(sutun_gorevleri)
    
    with st_sutun:
        st.markdown(f"""
            <div class="column-header" style="background: {renk};">
                <span>{baslik}</span>
                <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px; font-size: 11px;">{sayac}</span>
            </div>
        """, unsafe_allow_html=True)
        
        for g in sutun_gorevleri:
            kalan_gun = g.kalan_gun_hesapla()
            
            if kalan_gun < 0:
                kalan_metin = f"Süresi Geçti ({abs(kalan_gun)}g)"
            elif kalan_gun == 0:
                kalan_metin = "Son Gün"
            else:
                kalan_metin = f"{kalan_gun} gün kaldı"
            
            # RESMİ BORDER KAPSAYICISI (Elemanları tek kartta kilitler)
            with st.container(border=True):
                
                # Kart Üst Metin Alanı (HTML)
                st.markdown(f"""
                    <div class="task-card-content">
                        <div class="task-title-area">
                            <span>{g.ad}</span>
                            <span class="badge badge-{g.zorluk}">{g.zorluk}</span>
                        </div>
                        <div class="task-time-area">
                            <span>📅 {g.son_tarih}</span>
                            <span style="font-weight:600; color:{'#f87171' if kalan_gun<=0 else '#9ca3af'}">{kalan_metin}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Kart Altı Kontrol Alanı (Güvenli Yerel Elemanlar)
                padding_cols = st.columns([1])[0]
                with padding_cols:
                    tüm_durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]
                    tüm_durumlar.remove(g.durum)
                    
                    yeni_durum = st.selectbox(
                        "Durum Değiştir", [g.durum] + tüm_durumlar, key=f"mv_{g.id}", label_visibility="collapsed"
                    )
                    if yeni_durum != g.durum:
                        g.durum = yeni_durum
                        gorev_yoneticisi.gorevleri_kaydet()
                        st.rerun()
                        
                    if st.button("🗑️ Görevi Sil", key=f"rm_{g.id}"):
                        gorev_yoneticisi.gorev_sil(g.id)
                        st.rerun()