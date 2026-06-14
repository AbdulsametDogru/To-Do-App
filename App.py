import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği, başlık ve tema sabitleme
st.set_page_config(page_title="Enterprise Task Board Pro", layout="wide", page_icon="⚡")

# --- ULTRA PREMIUM CAFCAFLI CSS (RENKLİ KARTLAR VE HIGH-TECH ARKA PLAN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    
    /* 🌌 HIGH-TECH ARKA PLAN EFECTİ */
    .stApp {
        background: 
            radial-gradient(circle at 10% 10%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 90%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, #0d0e15 0%, #050507 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Arka plana şık bir gren/noise ve ışıltı katmak */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0.02;
        pointer-events: none;
        z-index: 0;
        background-image: 
            url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E"),
            radial-gradient(circle at 50% -20%, rgba(255, 255, 255, 0.03) 0%, transparent 50%);
    }
    
    /* 3 Ana Kanban Sütunu - Buzlu cam etkisi (Glassmorphism) */
    [data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(13, 15, 24, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 20px !important;
        padding: 22px !important;
        min-height: 72vh !important;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5) !important;
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
    
    /* 🎨 TAMAMEN RENKLENDİRİLMİŞ KART Container Algoritması */
    /* Streamlit Container'larını zorluk sınıflarına göre boyuyoruz. 
       `border=True` kullanmayı bıraktığımız için artık bu CSS sınıfları kartın ana gövdesini oluşturacak. */
    
    /* 🔴 ZOR GÖREVLER: Belirgin Koyu Kırmızı ve Kor Işıltı */
    .card-Zor {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(28, 19, 22, 0.95) 100%) !important;
        border: 1px solid rgba(239, 68, 68, 0.35) !important;
        border-radius: 14px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.08) !important;
        transition: transform 0.2s, border-color 0.2s !important;
    }
    
    /* 🟡 ORTA GÖREVLER: Belirgin Kehribar/Turuncu */
    .card-Orta {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(26, 22, 18, 0.95) 100%) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 14px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.06) !important;
        transition: transform 0.2s, border-color 0.2s !important;
    }
    
    /* 🟢 KOLAY GÖREVLER: Belirgin Koyu Zümrüt Yeşili */
    .card-Kolay {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(17, 22, 20, 0.95) 100%) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 14px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.05) !important;
        transition: transform 0.2s, border-color 0.2s !important;
    }
    
    /* Kartların Hover Durumları (Işıltı güçlendirilmiş) */
    .card-Zor:hover { border-color: rgba(239, 68, 68, 0.7) !important; transform: translateY(-2px); }
    .card-Orta:hover { border-color: rgba(245, 158, 11, 0.6) !important; transform: translateY(-2px); }
    .card-Kolay:hover { border-color: rgba(16, 185, 129, 0.5) !important; transform: translateY(-2px); }

    .task-card-content {
        padding: 18px 18px 8px 18px;
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
    
    /* Form Elemanları ve Buton Özelleştirmeleri (Sidebar ve Dialog) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #121422 !important;
        border: 1px solid #232742 !important;
        border-radius: 8px !important;
    }
    
    /* Butonların Genel Tasarımı */
    .stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        background-color: #121422 !important;
        border: 1px solid #232742 !important;
        color: #f3f4f6 !important;
        transition: all 0.2s !important;
    }
    
    /* Düzenle Butonu Hover */
    div[data-testid="stHorizontalBlock"] button[key^="edit_"]:hover {
        border-color: #3b82f6 !important;
        color: #3b82f6 !important;
        background-color: rgba(59, 130, 246, 0.05) !important;
    }
    
    /* Sil Butonu Hover */
    div[data-testid="stHorizontalBlock"] button[key^="rm_"]:hover {
        border-color: #ef4444 !important;
        color: #ef4444 !important;
        background-color: rgba(239, 68, 68, 0.05) !important;
    }
    
    /* Kenar Çubuğu (Sidebar) Cafcaflı Arka Plan Uyumu */
    [data-testid="stSidebar"] {
        background-color: #0b0c12 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.03) !important;
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
        <p style='color: #525876; margin: 0; font-size: 13px;'>Cafcaflı High-Tech arka plan ve zorluk rengine mühürlenmiş kart sürümü.</p>
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
            
            # 🔥 ÇÖZÜM: RESMİ CONTAINER'I KALDIRDIK. KENDİ HTML KARTIMIZI OLUŞTURUYORUZ.
            # Böylece `unsafe_allow_html=True` parametresi sayesinde kartın arka planı tam istediğin renk olur.
            # (Kartın başına dinamik CSS sınıfını basıyoruz: class="card-{g.zorluk}")
            st.markdown(f'<div class="card-{g.zorluk}">', unsafe_allow_html=True)
            
            # Kartın Üst Metin Alanı (HTML)
            st.markdown(f"""
                <div class="task-card-content">
                    <div class="task-title-area">
                        <span>{g.ad}</span>
                        <span class="badge badge-{g.zorluk}">{g.zorluk}</span>
                    </div>
                    <div class="task-time-area">
                        <span>📅 {g.son_tarih}</span>
                        <span style="font-weight:600; color:{'#f87171' if kalan_gun<=0 else '#e5e7eb'}">{kalan_metin}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Kart Altı Kontrol Alanı (Güvenli Yerel Elemanlar)
            # Kartın altındaki butonları kartın içine hapsetmek için st.container'ı sarmalıyoruz
            # AMA border parametresi kullanmıyoruz, böylece arka plan HTML'imize uyum sağlıyor.
            with st.container():
                b1, b2 = st.columns([1, 1])
                with b1:
                    if st.button("✏️ Düzenle", key=f"edit_{g.id}"):
                        gorev_duzenle_penceresi(g)
                with b2:
                    if st.button("🗑️ Sil", key=f"rm_{g.id}"):
                        gorev_yoneticisi.gorev_sil(g.id)
                        st.rerun()
            
            # Dinamik etiketi kapatıyoruz
            st.markdown('</div>', unsafe_allow_html=True)