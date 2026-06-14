import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği ve başlık ayarları
st.set_page_config(page_title="Enterprise Task Board Pro", layout="wide", page_icon="⚡")

# --- 🔥 GÖMÜLÜ BUTONLAR VE POZİSYON SABİTLEME CSS MİMARİSİ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    
    /* 🌌 CAFCAFLI HIGH-TECH ARKA PLAN */
    .stApp {
        background: 
            radial-gradient(circle at 20% 20%, rgba(239, 68, 68, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
            linear-gradient(135deg, #090a10 0%, #121420 50%, #050508 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Kanban Sütunları Tasarımı */
    [data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(6, 8, 14, 0.6) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 24px !important;
        padding: 24px !important;
        min-height: 75vh !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7) !important;
    }
    
    .column-header {
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 22px;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Streamlit İç Çerçeve Temizliği */
    [data-testid="stVerticalBlockBorderWrapper"], 
    div[data-testid="element-container"] .stElementContainer,
    div[data-testid="stVerticalBlock"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* 🎯 HEM BUTONLARI İÇEREN HEM DE ALT BOŞLUĞU AYARLANMIŞ ANA KART YAPISI */
    /* position: relative; kurduk ki alttaki butonları bu kartın sınırlarına göre konumlandırabilelim */
    .custom-task-card {
        position: relative !important;
        border-radius: 16px !important;
        padding: 20px 20px 70px 20px !important; /* Alt kısma butonlar için 70px koruyucu boşluk bıraktık */
        margin-bottom: -50px !important; /* Streamlit'in butonları aşağı atma boşluğunu absorbe ediyoruz */
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4) !important;
        transition: transform 0.2s ease !important;
        border: 1px solid transparent;
    }
    
    /* Zorluk Derecesi Renkleri */
    .card-glow-Zor {
        background: linear-gradient(135deg, #7f1d1d 0%, #450a0a 100%) !important;
        border-color: rgba(239, 68, 68, 0.4) !important;
    }
    .card-glow-Orta {
        background: linear-gradient(135deg, #7c2d12 0%, #431407 100%) !important;
        border-color: rgba(245, 158, 11, 0.4) !important;
    }
    .card-glow-Kolay {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%) !important;
        border-color: rgba(16, 185, 129, 0.35) !important;
    }
    
    .custom-task-card:hover { transform: translateY(-4px) !important; }
    
    .task-title-area {
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .task-time-area {
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        font-weight: 500;
    }
    
    .badge-white {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-transform: uppercase;
    }
    
    /* 🛠️ MUTLAK KONUMLANDIRMA İLE BUTONLARI KARTIN İÇİNE ÇEKME */
    /* Streamlit'in butonları oluşturduğu alanı yakalayıp, üstteki renkli kartın içine zorla sokuyoruz */
    div[data-testid="stHorizontalBlock"] div.element-container:has(button[key^="edit_"]),
    div[data-testid="stHorizontalBlock"] div.element-container:has(button[key^="rm_"]) {
        position: relative !important;
        top: -55px !important; /* Butonları renkli kartın alt boşluğuna yukarı çekerek yerleştiriyoruz */
        z-index: 10 !important;
    }
    
    /* Butonların Tasarımları */
    .stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        background-color: rgba(0, 0, 0, 0.3) !important; /* Cam efekti için yarı saydam koyu taban */
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
        padding: 5px 0px !important;
        transition: all 0.2s ease !important;
    }
    
    /* Düzenle Butonu Hover */
    .stButton > button[key^="edit_"]:hover {
        border-color: #3b82f6 !important;
        background-color: #3b82f6 !important;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
    }
    
    /* Sil Butonu Hover */
    .stButton > button[key^="rm_"]:hover {
        border-color: #ef4444 !important;
        background-color: #ef4444 !important;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.4);
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
    <div style='margin-bottom: 25px;'>
        <h1 style='color: #fff; font-weight: 800; font-size: 28px; margin-bottom: 5px;'>Workspace / <span style='color: #3b82f6;'>Sprint Board Pro</span></h1>
        <p style='color: #64748b; margin: 0; font-size: 13.5px;'>Butonları kart yapısına tamamen kenetlenmiş pürüzsüz yerleşim.</p>
    </div>
""", unsafe_allow_html=True)

# Üst Metrikler
m1, m2, m3, m4 = st.columns([2, 1, 1, 1])
with m1:
    st.markdown(f"<p style='color:#94a3b8; font-size:12px; margin-bottom:6px;'>Sprint İlerleme Durumu: {int(ilerleme_orani*100)}%</p>", unsafe_allow_html=True)
    st.progress(ilerleme_orani)
with m2: st.metric("Toplam Görev", toplam_gorev)
with m3: st.metric("Yapılıyor", yapilan_gorev)
with m4: st.metric("Tamamlandı", tamamlanan_gorev)

# --- SIDEBAR KONTROL MERKEZİ ---
st.sidebar.markdown("<h3 style='color: #fff; font-weight: 700;'>Kontrol Merkezi</h3>", unsafe_allow_html=True)
with st.sidebar.form("gorev_ekle_formu", clear_on_submit=True):
    ad = st.text_input("Görev Adı")
    durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
    zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"])
    son_tarih = st.date_input("Son Tarih", min_value=datetime.date.today())
    if st.form_submit_button(label="Görev Ekle"):
        if ad.strip():
            gorev_yoneticisi.gorev_ekle(ad, durum, zorluk, son_tarih.strftime("%d/%m/%Y"))
            st.rerun()

gorev_yoneticisi.gorevleri_sirala()

# --- SÜTUNLARIN YÜRÜTÜLMESİ ---
sutun1, sutun2, sutun3 = st.columns(3)
sutun_ayarlari = {
    "Yapılacak": (sutun1, "Yapılacaklar", "linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%)"),
    "Yapılıyor": (sutun2, "Yapılıyor Olanlar", "linear-gradient(90deg, #9a3412 0%, #c2410c 100%)"),
    "Tamamlandı": (sutun3, "Tamamlananlar", "linear-gradient(90deg, #065f46 0%, #047857 100%)")
}

for anahtar, (st_sutun, baslik, renk) in sutun_ayarlari.items():
    sutun_gorevleri = [x for x in gorev_yoneticisi.gorevler if x.durum == anahtar]
    
    with st_sutun:
        st.markdown(f"""
            <div class="column-header" style="background: {renk};">
                <span>{baslik}</span>
                <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px; font-size: 11px;">{len(sutun_gorevleri)}</span>
            </div>
        """, unsafe_allow_html=True)
        
        for g in sutun_gorevleri:
            kalan_gun = g.kalan_gun_hesapla()
            kalan_metin = f"Süresi Geçti ({abs(kalan_gun)}g)" if kalan_gun < 0 else ("Son Gün" if kalan_gun == 0 else f"{kalan_gun} gün kaldı")
            
            # 1. Adım: Kartın üst gövdesini ve metin alanını basıyoruz. (Alt tarafa padding-bottom: 70px ekledik)
            st.markdown(f"""
                <div class="custom-task-card card-glow-{g.zorluk}">
                    <div class="task-title-area">
                        <span>{g.ad}</span>
                        <span class="badge-white">{g.zorluk}</span>
                    </div>
                    <div class="task-time-area">
                        <span>📅 {g.son_tarih}</span>
                        <span style="font-weight:700; color:{'#ff8585' if kalan_gun<=0 else '#ffffff'}">{kalan_metin}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 2. Adım: Butonlar yan yana dursun diye st.columns kullanıyoruz, CSS'teki top: -55px kuralı bunları kartın içine çekecek.
            btn_col1, btn_col2 = st.columns([1, 1])
            with btn_col1:
                if st.button("✏️ Düzenle", key=f"edit_{g.id}"):
                    gorev_duzenle_penceresi(g)
            with btn_col2:
                if st.button("🗑️ Sil", key=f"rm_{g.id}"):
                    gorev_yoneticisi.gorev_sil(g.id)
                    st.rerun()