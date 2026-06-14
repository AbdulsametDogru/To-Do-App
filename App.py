import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği, başlık ve tema sabitleme
st.set_page_config(page_title="Enterprise Task Board Pro", layout="wide", page_icon="⚡")

# --- 🔥 MUTLAK POZİSYON SABİTLEMELİ AKILLI CSS MİMARİSİ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    
    /* 🌌 ANA ARKA PLAN */
    .stApp {
        background: 
            radial-gradient(circle at 20% 20%, rgba(239, 68, 68, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
            linear-gradient(135deg, #090a10 0%, #121420 50%, #050508 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* 📱 KANBAN SÜTUNLARI */
    [data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(6, 8, 14, 0.6) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 24px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
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
    
    /* 🎨 RENKLİ KONTROL MERKEZİ (SIDEBAR) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d111d 0%, #06070a 100%) !important;
        border-right: 1px solid rgba(59, 130, 246, 0.2) !important;
        box-shadow: 5px 0 30px rgba(0,0,0,0.5) !important;
    }
    [data-testid="stSidebar"] .stForm {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    [data-testid="stSidebar"] button[kind="primaryFormSubmit"] {
        background: linear-gradient(90deg, #1d4ed8 0%, #3b82f6 100%) !important;
        border: none !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4) !important;
    }

    /* Streamlit Gereksiz Boşluk ve Çerçeve Temizliği */
    [data-testid="stVerticalBlockBorderWrapper"], 
    div[data-testid="element-container"] .stElementContainer,
    div[data-testid="stVerticalBlock"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* 🎯 GEOMETRİK OLARAK SABİTLENMİŞ ANA KART YAPISI */
    .custom-task-card-wrapper {
        position: relative !important; /* İçindeki her şeyi buna göre hizalayacağız */
        margin-bottom: 16px !important;
    }

    .custom-task-card {
        border-radius: 16px !important;
        padding: 20px 20px 70px 20px !important; /* Butonlara alt tarafta güvenli bölge */
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4) !important;
        border: 1px solid transparent;
    }
    .card-glow-Zor { background: linear-gradient(135deg, #7f1d1d 0%, #450a0a 100%) !important; border-color: rgba(239, 68, 68, 0.4) !important; }
    .card-glow-Orta { background: linear-gradient(135deg, #7c2d12 0%, #431407 100%) !important; border-color: rgba(245, 158, 11, 0.4) !important; }
    .card-glow-Kolay { background: linear-gradient(135deg, #064e3b 0%, #022c22 100%) !important; border-color: rgba(16, 185, 129, 0.35) !important; }
    
    .task-title-area {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 12px;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    .task-title-text {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .task-time-area {
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 13px;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    .badge-white {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        padding: 4px 10px !important;
        border-radius: 8px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        text-transform: uppercase !important;
        flex-shrink: 0 !important;
    }
    
    /* 🛠️ KAYMAYI ENGELLEYEN ABSOLUTE BUTON KİLİTLEME SİSTEMİ */
    /* Butonları içeren alt Streamlit satırını yakalayıp kartın alt zeminine çiviliyoruz */
    .custom-task-card-wrapper div[data-testid="stHorizontalBlock"] {
        position: absolute !important;
        bottom: 15px !important; /* Kartın altından tam 15px yukarıda sabit dur */
        left: 20px !important;
        right: 20px !important;
        width: calc(100% - 40px) !important;
        z-index: 5 !important;
    }
    
    .stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        font-weight: 600;
        padding: 5px 0px !important;
    }

    /* 📱 MOBİL UYUMLULUK AYARI */
    @media (max-width: 768px) {
        /* Mobilde butonlar alt alta binerse kart otomatik aşağı doğru esnesin diye padding artırıldı */
        .custom-task-card {
            padding-bottom: 105px !important;
        }
    }

    /* 🎨 RENKLİ GÜNCELLEME MODALI */
    div[role="dialog"] {
        background: linear-gradient(135deg, #131722 0%, #090a0f 100%) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 20px !important;
    }
    div[role="dialog"] h1, div[role="dialog"] p { color: #fff !important; }
    div[role="dialog"] .stButton button {
        background: linear-gradient(90deg, #059669 0%, #10b981 100%) !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3) !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum yönetimi hafıza kontrolü
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()

gorev_yoneticisi = st.session_state.yonetici

# --- 📝 GÖREV DÜZENLEME MODALI ---
@st.dialog("📝 Görevi Güncelle")
def gorev_duzenle_penceresi(gorev):
    st.markdown(f"**{gorev.ad}** görevi için yeni teknik parametreleri belirleyin:")
    yeni_ad = st.text_input("Görevin Yeni Adı", value=gorev.ad)
    yeni_durum = st.selectbox("Aşama Değiştir", ["Yapılacak", "Yapılıyor", "Tamamlandı"], index=["Yapılacak", "Yapılıyor", "Tamamlandı"].index(gorev.durum))
    yeni_zorluk = st.selectbox("Öncelik Seviyesi", ["Kolay", "Orta", "Zor"], index=["Kolay", "Orta", "Zor"].index(gorev.zorluk))
    
    mevcut_tarih = datetime.datetime.strptime(gorev.son_tarih, "%d/%m/%Y").date()
    yeni_son_tarih = st.date_input("Deadline", value=mevcut_tarih)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Parametreleri Uygula", type="primary"):
        if yeni_ad.strip():
            gorev.ad = yeni_ad
            gorev.durum = yeni_durum
            gorev.zorluk = yeni_zorluk
            gorev.son_tarih = yeni_son_tarih.strftime("%d/%m/%Y")
            gorev_yoneticisi.gorevleri_kaydet()
            st.rerun()

# --- 📊 ÜST ANALİTİK PANEL ---
toplam = len(gorev_yoneticisi.gorevler)
tamamlanan = len([x for x in gorev_yoneticisi.gorevler if x.durum == "Tamamlandı"])
yapilan = len([x for x in gorev_yoneticisi.gorevler if x.durum == "Yapılıyor"])
ilerleme = (tamamlanan / toplam) if toplam > 0 else 0.0

st.markdown("""
    <div style='margin-bottom: 25px;'>
        <h1 style='color: #fff; font-weight: 800; font-size: 28px; margin-bottom: 5px;'>Workspace / <span style='color: #3b82f6;'>Sprint Board Pro</span></h1>
        <p style='color: #64748b; margin: 0; font-size: 13px;'>Mobil cihazlar ve PC için mutlak konumlandırmalı stabil kart yapısı.</p>
    </div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns([2, 1, 1, 1])
with m1:
    st.markdown(f"<p style='color:#94a3b8; font-size:12px; margin-bottom:6px;'>Sprint İlerleme: {int(ilerleme*100)}%</p>", unsafe_allow_html=True)
    st.progress(ilerleme)
with m2: st.metric("Toplam", toplam)
with m3: st.metric("Aktif", yapilan)
with m4: st.metric("Biten", tamamlanan)

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# --- ⚙️ KONTROL MERKEZİ (SIDEBAR) ---
st.sidebar.markdown("<h2 style='color: #fff; font-weight: 800; font-size: 22px;'>Kontrol Merkezi</h2>", unsafe_allow_html=True)
with st.sidebar.form("gorev_ekle_formu", clear_on_submit=True):
    st.markdown("<p style='color: #3b82f6; font-weight: 600;'>Yeni Görev Ekle</p>", unsafe_allow_html=True)
    ad = st.text_input("Görev Tanımı")
    durum = st.selectbox("Başlangıç Aşaması", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
    zorluk = st.selectbox("Öncelik Derecesi", ["Kolay", "Orta", "Zor"])
    son_tarih = st.date_input("Deadline", min_value=datetime.date.today())
    if st.form_submit_button(label="🚀 GÖREVİ SİSTEME İŞLE"):
        if ad.strip():
            gorev_yoneticisi.gorev_ekle(ad, durum, zorluk, son_tarih.strftime("%d/%m/%Y"))
            st.rerun()

gorev_yoneticisi.gorevleri_sirala()

# --- 🚀 KANBAN SÜRECİ ---
s1, s2, s3 = st.columns(3)
ayarlar = {
    "Yapılacak": (s1, "Yapılacaklar", "linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%)"),
    "Yapılıyor": (s2, "Yapılıyor Olanlar", "linear-gradient(90deg, #9a3412 0%, #c2410c 100%)"),
    "Tamamlandı": (s3, "Tamamlananlar", "linear-gradient(90deg, #065f46 0%, #047857 100%)")
}

for anahtar, (st_sutun, baslik, renk) in ayarlar.items():
    filtre_gorevler = [x for x in gorev_yoneticisi.gorevler if x.durum == anahtar]
    with st_sutun:
        st.markdown(f"<div class='column-header' style='background: {renk};'><span>{baslik}</span><span style='background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px; font-size: 11px;'>{len(filtre_gorevler)}</span></div>", unsafe_allow_html=True)
        
        for g in filtre_gorevler:
            k_gun = g.kalan_gun_hesapla()
            # 🛠️ DÜZELTME: "gün kaldı" ifadesi tam metin haline getirildi
            k_metin = f"Gecikti ({abs(k_gun)}g)" if k_gun < 0 else ("Son Gün" if k_gun == 0 else f"{k_gun} gün kaldı")
            
            # Kart yapısını sarmalayıcı bir ana div (.custom-task-card-wrapper) içine alıyoruz
            st.markdown(f"""
                <div class="custom-task-card-wrapper">
                    <div class="custom-task-card card-glow-{g.zorluk}">
                        <div class="task-title-area">
                            <span class="task-title-text">{g.ad}</span>
                            <span class="badge-white">{g.zorluk}</span>
                        </div>
                        <div class="task-time-area">
                            <span>📅 {g.son_tarih}</span>
                            <span style="font-weight:700; color:{'#ff8585' if k_gun<=0 else '#ffffff'}">{k_metin}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Butonlar bu üstteki wrapper elemanının tam tabanına kilitlenecek
            b1, b2 = st.columns([1, 1])
            with b1:
                if st.button("✏️ Düzenle", key=f"edit_{g.id}"): gorev_duzenle_penceresi(g)
            with b2:
                if st.button("🗑️ Sil", key=f"rm_{g.id}"): gorev_yoneticisi.gorev_sil(g.id); st.rerun()