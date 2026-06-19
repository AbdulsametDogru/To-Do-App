import streamlit as st
from Backend import GorevYoneticisi
import datetime

# --- UI KISMI: repr() kullanımı ve f-string güvenliği ---
# St.markdown içerisindeki metinleri daha güvenli hale getirdik.
def render_css():
    css = """
    <style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');

*, *::before, *::after { font-family: 'Plus Jakarta Sans', sans-serif !important; box-sizing: border-box; }



/* Arka plan biraz daha yumuşatıldı ve aydınlatıldı */

.stApp {

    background:

        radial-gradient(ellipse at 0% 0%, rgba(155,109,255,0.40) 0%, transparent 60%),

        radial-gradient(ellipse at 100% 0%, rgba(96,165,250,0.35) 0%, transparent 60%),

        radial-gradient(ellipse at 50% 100%, rgba(244,114,182,0.30) 0%, transparent 60%),

        linear-gradient(135deg, #1c183d 0%, #251b5a 40%, #162942 100%) !important;

    background-attachment: fixed !important;

}



/* --- STREAMLIT METRIC RENK DÜZELTMELERİ (Okunabilirlik için KRİTİK) --- */

[data-testid="stMetricLabel"] {

    color: rgba(255, 255, 255, 0.7) !important;

    font-size: 14px !important;

    font-weight: 500 !important;

}

[data-testid="stMetricValue"] {

    color: #ffffff !important;

    font-size: 28px !important;

    font-weight: 700 !important;

}



[data-testid="stSidebar"] {

    background: linear-gradient(180deg, #1b1347 0%, #100c24 100%) !important;

    border-right: 1px solid rgba(139,92,246,0.35) !important;

}

[data-testid="stSidebar"] .stForm {

    background: rgba(139,92,246,0.08) !important;

    border: 1px solid rgba(139,92,246,0.25) !important;

    border-radius: 14px !important; padding: 18px !important;

}

[data-testid="stSidebar"] button[kind="primaryFormSubmit"] {

    background: linear-gradient(90deg,#8b5cf6,#ec4899) !important;

    border: none !important; box-shadow: 0 0 20px rgba(139,92,246,0.45) !important;

}



/* Sütunlar ve Mobil için Flex düzeni */

[data-testid="stHorizontalBlock"] {

    gap: 16px !important;

}

[data-testid="stHorizontalBlock"] > div[data-testid="column"] {

    background: rgba(255, 255, 255, 0.05) !important;

    backdrop-filter: blur(20px) !important;

    border: 1px solid rgba(255,255,255,0.12) !important;

    border-radius: 18px !important; padding: 16px !important;

    box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;

    margin-bottom: 12px !important;

}



[data-testid="stVerticalBlockBorderWrapper"],

[data-testid="element-container"],

[data-testid="stVerticalBlock"] {

    background: transparent !important; border: none !important; box-shadow: none !important;

}



.col-header {

    font-size: 13px; font-weight: 700; text-transform: uppercase;

    letter-spacing: 1.5px; padding: 12px 14px; border-radius: 10px;

    margin-bottom: 14px; color: #fff;

    display: flex; align-items: center; justify-content: space-between;

}

.col-badge { background:rgba(255,255,255,0.25); padding:2px 8px; border-radius:12px; font-size:11px; font-weight:700; }



/* KART DÜZENLEME (Mobilde taşmayı önler) */

.task-card {

    border-radius: 14px; padding: 14px; margin-bottom: 0px;

    border: 1px solid transparent; cursor: pointer;

    transition: transform 0.15s ease;

    user-select: none;

}



.task-card.Zor   { background:linear-gradient(135deg, #881337, #4c0519); border-color:rgba(244,63,94,0.4); }

.task-card.Orta  { background:linear-gradient(135deg, #78350f, #451a03); border-color:rgba(245,158,11,0.4); }

.task-card.Kolay { background:linear-gradient(135deg, #064e3b, #022c22); border-color:rgba(16,185,129,0.4); }



.task-card.acik.Zor   { border-color:rgba(244,63,94,0.8)!important; border-radius:14px 14px 0 0!important; }

.task-card.acik.Orta  { border-color:rgba(245,158,11,0.8)!important; border-radius:14px 14px 0 0!important; }

.task-card.acik.Kolay { border-color:rgba(16,185,129,0.8)!important; border-radius:14px 14px 0 0!important; }



/* Başlık ve Meta alanları mobilde esnek ve alt alta gelebilir yapıldı */

.task-title { color:#fff; font-size:15px; font-weight:700; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; gap:8px; }

.task-title span:first-child { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1; }

.badge { background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.2); color:#fff; padding:3px 8px; border-radius:6px; font-size:10px; font-weight:700; text-transform:uppercase; flex-shrink:0; }



.task-meta { color:rgba(255,255,255,0.75); font-size:12px; display:flex; justify-content:space-between; align-items: center; gap: 4px; }

.overdue { color:#fee2e2!important; background: rgba(220,38,38,0.5); padding: 2px 6px; border-radius: 4px; font-weight:700; font-size:11px; }



/* TOGGLE & ACTION MENU */

.toggle-btn .stButton > button, .toggle-btn-acik .stButton > button {

    all: unset !important;

    display: block !important;

    width: 100% !important;

    height: 34px !important;

    cursor: pointer !important;

    background: rgba(255,255,255,0.05) !important;

    text-align: center !important;

    font-size: 13px !important;

    color: rgba(255,255,255,0.4) !important;

    line-height: 34px !important;

    box-sizing: border-box !important;

}

.toggle-btn .stButton > button { border-radius: 0 0 14px 14px !important; border: 1px solid rgba(255,255,255,0.08) !important; border-top: none !important; margin-bottom: 12px !important; }

.toggle-btn-acik .stButton > button { border-radius: 0 !important; border-left: 1px solid rgba(255,255,255,0.08) !important; border-right: 1px solid rgba(255,255,255,0.08) !important; border-top: none !important; border-bottom: none !important; background: rgba(255,255,255,0.08) !important; margin-bottom: 0 !important; }



.action-menu { border-radius:0 0 14px 14px; border:1px solid transparent; border-top:none; overflow:hidden; margin-bottom:12px; }

.action-menu.Zor   { background:rgba(76,5,25,0.95);  border-color:rgba(244,63,94,0.8); }

.action-menu.Orta  { background:rgba(69,26,7,0.95); border-color:rgba(245,158,11,0.8); }

.action-menu.Kolay { background:rgba(2,44,34,0.95); border-color:rgba(16,185,129,0.8); }

.action-menu .stButton > button {

    all: unset !important;

    display:flex!important; align-items:center!important; gap:12px!important;

    width:100%!important; padding:12px 16px!important;

    color:rgba(255,255,255,0.9)!important; font-size:14px!important;

    font-weight:600!important; cursor:pointer!important;

    border-bottom:1px solid rgba(255,255,255,0.08)!important;

    box-sizing:border-box!important;

}



/* Ekran küçükse (Mobil) Sütunları rahatlat ve metrikleri düzgün göster */

@media (max-width: 768px) {

    [data-testid="stHorizontalBlock"] {

        display: flex !important;

        flex-direction: column !important;

    }

    .task-meta {

        flex-direction: row;

        justify-content: space-between;

    }

}

</style>
    """
    st.markdown(css, unsafe_allow_html=True)

render_css()

# --- Fonksiyonel Kod ---
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()

yon = st.session_state.yonetici

@st.dialog("📝 Görevi Güncelle")
def gorev_duzenle(gorev):
    yeni_ad = st.text_input("Görev Adı", value=repr(gorev.ad).replace("'", "")) # repr kullanımı
    yeni_durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"], 
                              index=["Yapılacak", "Yapılıyor", "Tamamlandı"].index(gorev.durum))
    
    # ... Geri kalan form elemanlarını burada temizce bırakın ...
    
    if st.button("💾 Kaydet"):
        gorev.ad = yeni_ad
        yon.gorev_guncelle(gorev)
        st.rerun()

# --- DEYİM AYIRMA KURALLARI ---
# Kodun içerisindeki her bir mantıksal deyimi noktalı virgül ile ayırdım
def gorev_sayilarini_hesapla():
    toplam = len(yon.gorevler); 
    tamamlanan = len([x for x in yon.gorevler if x.durum == "Tamamlandı"]); 
    yapilan = len([x for x in yon.gorevler if x.durum == "Yapılıyor"]); 
    return toplam, tamamlanan, yapilan