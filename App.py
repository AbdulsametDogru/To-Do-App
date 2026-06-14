import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği ve başlık ayarları
st.set_page_config(page_title="Enterprise Task Board Pro", layout="wide", page_icon="⚡")

# --- CSS: RENKLİ KARTLAR VE KANBAN MİMARİSİ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    
    /* 🌌 PREMIUM DEEP SPACE ARKA PLAN EFECTİ */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #161824 0%, #0b0c11 70%, #050507 100%) !important;
        background-attachment: fixed !important;
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0.015;
        pointer-events: none;
        z-index: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }
    
    /* 3 Ana Kanban Sütunu */
    [data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(10, 11, 18, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
        border-radius: 20px !important;
        padding: 22px !important;
        min-height: 72vh !important;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.6) !important;
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
    
    /* 🎨 DİNAMİK VE GÖRÜNÜR KART ARKA PLANLARI (CSS Ezme Uygulandı) */
    
    /* 🔴 ZOR GÖREVLER: Belirgin Koyu Kırmızı */
    div.card-Zor div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, #1c1316 100%) !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.1) !important;
    }
    
    /* 🟡 ORTA GÖREVLER: Belirgin Kehribar/Kahve */
    div.card-Orta div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, #1a1612 100%) !important;
        border: 1px solid rgba(245, 158, 11, 0.35) !important;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.08) !important;
    }
    
    /* 🟢 KOLAY GÖREVLER: Belirgin Koyu Yeşil */
    div.card-Kolay div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, #111614 100%) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.06) !important;
    }
    
    /* Ortak Kart Ayarları */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        margin-bottom: 14px !important;
        padding: 0px !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px) !important;
    }
    div.card-Zor div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: rgba(239, 68, 68, 0.8) !important; }
    div.card-Orta div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: rgba(245, 158, 11, 0.7) !important; }
    div.card-Kolay div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: rgba(16, 185, 129, 0.6) !important; }

    .task-card-content {
        padding: 15px 15px 4px 15px;
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
    .badge-Zor { background: rgba(239, 68, 68, 0.25); color: #f87171; }
    .badge-Orta { background: rgba(245, 158, 11, 0.22); color: #fbbf24; }
    .badge-Kolay { background: rgba(16, 185, 129, 0.2); color: #34d399; }
    
    .task-time-area {
        color: #e5e7eb;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    
    /* Kart İçi Buton Entegrasyon Tasarımları */
    .stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        background-color: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #e5e7eb !important;
        transition: all 0.2s !important;
    }
    
    /* Butonların Hover Durumları */
    div[data-testid="stHorizontalBlock"] button[key^="edit_"]:hover {
        border-color: #3b82f6 !important;
        color: #3b82f6 !important;
        background-color: rgba(59, 130, 246, 0.15) !important;
    }
    div[data-testid="stHorizontalBlock"] button[key^="rm_"]:hover {
        border-color: #ef4444 !important;
        color: #ef4444 !important;
        background-color: rgba(239, 68, 68, 0.15) !important;
    }
    
    /* Kenar Çubuğu Form Elemanları */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #121422 !important;
        border: 1px solid #232742 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] {
        background-color: #090a0e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.02) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum yönetimi hafıza kontrolü
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()

gorev_yoneticisi = st.session_state.yonetici

# --- GÖREV DÜZENLEME MODALI ---
@st.dialog("📝 Görevi Düzenle")
def gorev_duzenle_penceresi(gorev):
    st.markdown(f"**{gorev.ad}** görevine ait güncel bilgileri giriniz:")
    
    yeni_ad = st.text_input("Görev Adı", value=gorev.ad)
    yeni_durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"], index=["Yapılacak", "Yapılıyor", "Tamamlandı"].index(gorev.durum))
    yeni_zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"], index=["Kolay", "Orta", "Zor"].index(gorev.zorluk))
    
    mevcut_tarih = datetime.datetime.strptime(gorev.son_tarih, "%d/%m/%Y").date()
    yeni_son_tarih = st.date_input("Son Tarih", value=mevcut_tarih)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("💾 Değişiklikleri Kaydet", type="primary"):
        if yeni_ad.strip():
            gorev.ad = yeni_ad
            gorev.durum = yeni_durum
            gorev.zorluk = yeni_zorluk
            gorev.son_tarih = yeni_son_tarih.strftime("%d/%m/%Y")
            
            gorev_yoneticisi.gorevleri_kaydet()
            st.rerun()

# --- ÜST PANEL ANALİTİKLERİ ---
toplam_gorev = len(gorev_yoneticisi.gorevler)
tamamlanan_gorev = len([x for x in gorev_yoneticisi.gorevler if x.durum == "Tamamlandı"])
yapilan_gorev = len([x for x in gorev_yoneticisi.gorevler if x.durum == "Yapılıyor"])
ilerleme_orani = (tamamlanan_gorev / toplam_gorev) if toplam_gorev > 0 else 0.0

st.markdown("""
    <div style='margin-bottom: 20px;'>
        <h1 style='color: #fff; font-weight: 700; font-size: 26px; margin-bottom: 5px;'>Workspace / <span style='color: #3b82f6;'>Sprint Board Pro</span></h1>
        <p style='color: #525876; margin: 0; font-size: 13px;'>Zorluk seviyelerine ait belirgin renkli kart arka planları aktifleştirildi.</p>
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

# Sıralama mekanizması
gorev_yoneticisi.gorevleri_sirala()

# --- SÜTUNLARIN OLUŞTURULMASI ---
sutun1, sutun2, sutun3 = st.columns(3)

sutun_ayarlari = {
    "Yapılacak": (sutun1, "Yapılacaklar", "linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%)"),
    "Yapılıyor": (sutun2, "Yapılıyor Olanlar", "linear-gradient(90deg, #9a3412 0%, #c2410c 100%)"),
    "Tamamlandı": (sutun3, "Tamamlananlar", "linear-gradient(90deg, #065f46 0%, #047857 100%)")
}

for anahtar, (st_sutun, baslik, renk) in sutun_ayarlari.items():
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
            
            # Dinamik sınıf enjeksiyonu
            st.markdown(f'<div class="card-{g.zorluk}">', unsafe_allow_html=True)
            
            with st.container(border=True):
                # Kart İçeriği
                st.markdown(f"""
                    <div class="task-card-content">
                        <div class="task-title-area">
                            <span>{g.ad}</span>
                            <span class="badge badge-{g.zorluk}">{g.zorluk}</span>
                        </div>
                        <div class="task-time-area">
                            <span>📅 {g.son_tarih}</span>
                            <span style="font-weight:600; color:{'#f87171' if kalan_gun<=0 else '#a3a9b6'}">{kalan_metin}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Eylemler
                b1, b2 = st.columns([1, 1])
                with b1:
                    if st.button("✏️ Düzenle", key=f"edit_{g.id}"):
                        gorev_duzenle_penceresi(g)
                with b2:
                    if st.button("🗑️ Sil", key=f"rm_{g.id}"):
                        gorev_yoneticisi.gorev_sil(g.id)
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)