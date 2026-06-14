import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği ve başlık ayarları
st.set_page_config(page_title="Enterprise Task Board Pro", layout="wide", page_icon="⚡")

# --- 🔥 ULTRA CAFCAFLI HIGH-TECH CSS & TAMAMEN RENKLİ KARTLAR MİMARİSİ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    
    /* 🌌 OYUNCU/HIGH-TECH TARZI CAFCAFLI ARKA PLAN */
    .stApp {
        background: 
            radial-gradient(circle at 20% 20%, rgba(239, 68, 68, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
            linear-gradient(135deg, #090a10 0%, #121420 50%, #050508 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Canlılık hissi için ince nokta deseni ve üst parıltı */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0.02;
        pointer-events: none;
        z-index: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }
    
    /* 3 Ana Kanban Sütunu - Saydam Buzlu Cam Tasarımı */
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
    
    /* Sütun Başlıkları */
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
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    /* 🎨 STREAMLIT'İN İÇ KUTULARINI SIFIRLAMA (Ezme Operasyonu) */
    /* Streamlit'in kendi gri kutu arka planlarını tamamen yok ediyoruz ki bizim renklerimiz parlasın */
    [data-testid="stVerticalBlockBorderWrapper"], div[data-testid="element-container"] .stElementContainer {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* 🎯 TAMAMEN BOYALI, PARLAK VE CAZİBELİ KARTLARIMIZ */
    .custom-task-card {
        border-radius: 16px !important;
        padding: 16px 18px !important;
        margin-bottom: 0px !important; /* Altındaki buton sarmalayıcısı ile birleşecek */
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4) !important;
        transition: transform 0.2s ease !important;
        border: 1px solid transparent;
    }
    
    /* 🔴 ZOR: Kıpkırmızı Gradyan ve Kor Neon Işıltı */
    .card-glow-Zor {
        background: linear-gradient(135deg, #7f1d1d 0%, #450a0a 100%) !important;
        border-color: rgba(239, 68, 68, 0.5) !important;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.2), 0 10px 25px rgba(0,0,0,0.5) !important;
    }
    
    /* 🟡 ORTA: Canlı Turuncu/Kehribar Gradyan */
    .card-glow-Orta {
        background: linear-gradient(135deg, #7c2d12 0%, #431407 100%) !important;
        border-color: rgba(245, 158, 11, 0.5) !important;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.18), 0 10px 25px rgba(0,0,0,0.5) !important;
    }
    
    /* 🟢 KOLAY: Yemyeşil Zümrüt Gradyan */
    .card-glow-Kolay {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%) !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.15), 0 10px 25px rgba(0,0,0,0.5) !important;
    }
    
    /* Hover Efekti (Kartlar havaya kalksın) */
    .custom-task-card:hover {
        transform: translateY(-4px) !important;
    }
    
    /* Kart İçi Metin Mimarisi */
    .task-title-area {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    
    .task-time-area {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 13.5px !important;
        display: flex !important;
        justify-content: space-between !important;
        font-weight: 500 !important;
    }
    
    /* Kart Rozetleri (Cam Görünümlü Beyaz) */
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
    
    /* 🎛️ BUTON ALANI SARMALAYICISI (Kartın altına tam mühürleme) */
    .action-container-box {
        background: rgba(0, 0, 0, 0.25) !important;
        border-bottom-left-radius: 16px;
        border-bottom-right-radius: 16px;
        padding: 8px 12px;
        margin-bottom: 18px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-top: none;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Streamlit İç Buton Tasarımları */
    .stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.2s !important;
    }
    
    div[data-testid="stHorizontalBlock"] button[key^="edit_"]:hover {
        border-color: #3b82f6 !important;
        color: #3b82f6 !important;
        background-color: rgba(59, 130, 246, 0.15) !important;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
    }
    div[data-testid="stHorizontalBlock"] button[key^="rm_"]:hover {
        border-color: #ef4444 !important;
        color: #ef4444 !important;
        background-color: rgba(239, 68, 68, 0.15) !important;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    
    /* Kenar Çubuğu Giriş Alanları */
    .stSelectbox div[data-baseweb="select"], .stTextInput input {
        background-color: #0d0f1a !important;
        border: 1px solid #1e2238 !important;
        border-radius: 10px !important;
        color: #fff !important;
    }
    [data-testid="stSidebar"] {
        background-color: #06070a !important;
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
    <div style='margin-bottom: 25px;'>
        <h1 style='color: #fff; font-weight: 800; font-size: 28px; margin-bottom: 5px; letter-spacing: -0.5px;'>Workspace / <span style='color: #3b82f6; text-shadow: 0 0 15px rgba(59,130,246,0.4);'>Sprint Board Pro</span></h1>
        <p style='color: #64748b; margin: 0; font-size: 13.5px; font-weight: 500;'>Tümüyle renklendirilmiş ultra parlak kartlar ve siber punk radyal arka plan aktif.</p>
    </div>
""", unsafe_allow_html=True)

# Üst Metrik Çubukları
m1, m2, m3, m4 = st.columns([2, 1, 1, 1])
with m1:
    st.markdown(f"<p style='color:#94a3b8; font-size:12px; margin-bottom:6px; font-weight:600;'>Sprint İlerleme Durumu: {int(ilerleme_orani*100)}%</p>", unsafe_allow_html=True)
    st.progress(ilerleme_orani)
with m2:
    st.metric("Toplam Görev", toplam_gorev)
with m3:
    st.metric("Yapılıyor", yapilan_gorev)
with m4:
    st.metric("Tamamlandı", tamamlanan_gorev)

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

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
            
            # 🔥 ADIM 1: KART GÖVDESİNİ SAF HTML VE RENKLİ GRADYANLARLA BASIYORUZ
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
            
            # 🎛️ ADIM 2: BUTONLARI KARTIN ALTINA YERLEŞTİRİP TEK BİR BLOK GİBİ SARMALIYORUZ
            st.markdown('<div class="action-container-box">', unsafe_allow_html=True)
            b1, b2 = st.columns([1, 1])
            with b1:
                if st.button("✏️ Düzenle", key=f"edit_{g.id}"):
                    gorev_duzenle_penceresi(g)
            with b2:
                if st.button("🗑️ Sil", key=f"rm_{g.id}"):
                    gorev_yoneticisi.gorev_sil(g.id)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)