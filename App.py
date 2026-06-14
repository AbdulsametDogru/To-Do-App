import streamlit as st
from Backend import GorevYoneticisi
import datetime

# Sayfa genişliği ve başlık ayarları
st.set_page_config(page_title="Enterprise Task Board Pro", layout="wide", page_icon="⚡")

# Oturum yönetimi hafıza kontrolü
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()

gorev_yoneticisi = st.session_state.yonetici

# --- 🎯 HTML BUTONLARININ AKSİYONLARINI YAKALAMA ALGORİTMASI ---
# Kart içindeki HTML elementlerine tıklandığında URL parametreleri üzerinden veri güncellenir
params = st.query_params

if "action" in params and "id" in params:
    aksiyon = params["action"]
    gorev_id = params["id"]
    
    if aksiyon == "delete":
        gorev_yoneticisi.gorev_sil(gorev_id)
        st.query_params.clear()  # URL'i temizle
        st.rerun()
        
    elif aksiyon == "move" and "target" in params:
        hedef_durum = params["target"]
        for g in gorev_yoneticisi.gorevler:
            if g.id == gorev_id:
                g.durum = hedef_durum
                gorev_yoneticisi.gorevleri_kaydet()
                break
        st.query_params.clear()  # URL'i temizle
        st.rerun()

# --- 🎨 KUSURSUZ INTERACTIVE KANBAN CSS mimarisi ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .main { background: #090a0f; }
    
    /* 3 Ana Pano Sütunu */
    [data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        min-height: 70vh !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Pano Başlıkları */
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
    
    /* TASARIMI ASLA KOPMAYAN TEK PARÇA KART YAPISI */
    .premium-task-card {
        background: #131520;
        border: 1px solid #1f2235;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s, border-color 0.2s;
    }
    .premium-task-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
    }
    
    /* Sol Öncelik Çizgileri */
    .indicator-Zor { background: #ef4444; width: 4px; position: absolute; left: 0; top: 0; bottom: 0; }
    .indicator-Orta { background: #f59e0b; width: 4px; position: absolute; left: 0; top: 0; bottom: 0; }
    .indicator-Kolay { background: #10b981; width: 4px; position: absolute; left: 0; top: 0; bottom: 0; }
    
    .task-title { color: #f3f4f6; font-size: 15px; font-weight: 600; margin-bottom: 8px; display: flex; align-items: center; }
    
    .badge { display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; margin-left: 8px; }
    .badge-Zor { background: rgba(239, 68, 68, 0.12); color: #f87171; }
    .badge-Orta { background: rgba(245, 158, 11, 0.12); color: #fbbf24; }
    .badge-Kolay { background: rgba(16, 185, 129, 0.12); color: #34d399; }
    
    .task-time { color: #9ca3af; font-size: 12px; display: flex; justify-content: space-between; margin-bottom: 16px; }
    
    /* Kart İçindeki İnteraktif HTML Kontrolleri */
    .card-controls {
        display: flex;
        gap: 8px;
        align-items: center;
        margin-top: 12px;
    }
    
    .html-dropdown {
        flex: 1;
        background: #1a1d2e;
        color: #f3f4f6;
        border: 1px solid #2d314e;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        outline: none;
        cursor: pointer;
        height: 38px;
    }
    
    .html-delete-button {
        background: #1a1d2e;
        color: #ef4444;
        border: 1px solid #2d314e;
        border-radius: 8px;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .html-delete-button:hover {
        background: rgba(239, 68, 68, 0.1);
        border-color: #ef4444;
    }
    </style>
""", unsafe_allow_html=True)

# --- ÜST PANEL ANALİTİKLERİ ---
toplam_gorev = len(gorev_yoneticisi.gorevler)
tamamlanan_gorev = len([x for x in gorev_yoneticisi.gorevler if x.durum == "Tamamlandı"])
yapilan_gorev = len([x for x in gorev_yoneticisi.gorevler if x.durum == "Yapılıyor"])
ilerleme_orani = (tamamlanan_gorev / toplam_gorev) if toplam_gorev > 0 else 0.0

st.markdown("""
    <div style='margin-bottom: 20px;'>
        <h1 style='color: #fff; font-weight: 700; font-size: 26px; margin-bottom: 5px;'>Workspace / <span style='color: #3b82f6;'>Sprint Board Pro</span></h1>
        <p style='color: #4b5563; margin: 0; font-size: 13px;'>Tüm kontrol bileşenlerinin tek bir kart yapısında mühürlendiği kusursuz arayüz.</p>
    </div>
""", unsafe_allow_html=True)

# Üst Metrikler
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
arama_sorgusu = st.sidebar.text_input("Görevlerde ara...", value="", placeholder="Kelime yazın...").strip().lower()
filtre_zorluk = st.sidebar.multiselect("Önceliğe Göre Filtrele", ["Kolay", "Orta", "Zor"], default=["Kolay", "Orta", "Zor"])

st.sidebar.markdown("<hr style='border-color: #1f2235; margin:20px 0;'>", unsafe_allow_html=True)

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

# --- FİLTRELEME İŞLEMLERİ ---
gorev_yoneticisi.gorevleri_sirala()
gosterilecek_gorevler = []
for g in gorev_yoneticisi.gorevler:
    if (arama_sorgusu in g.ad.lower()) and (g.zorluk in filtre_zorluk):
        gosterilecek_gorevler.append(g)

# --- KANBAN SÜTUNLARINI OLUŞTURMA ---
sutun1, sutun2, sutun3 = st.columns(3)

sutun_ayarlari = {
    "Yapılacak": (sutun1, "Yapılacaklar", "linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%)"),
    "Yapılıyor": (sutun2, "Yapılıyor Olanlar", "linear-gradient(90deg, #9a3412 0%, #c2410c 100%)"),
    "Tamamlandı": (sutun3, "Tamamlananlar", "linear-gradient(90deg, #065f46 0%, #047857 100%)")
}

for anahtar, (st_sutun, baslik, renk) in sutun_ayarlari.items():
    sutun_gorevleri = [x for x in gosterilecek_gorevler if x.durum == anahtar]
    sayac = len(sutun_gorevleri)
    
    with st_sutun:
        # Sütun Başlığı
        st.markdown(f"""
            <div class="column-header" style="background: {renk};">
                <span>{baslik}</span>
                <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px; font-size: 11px;">{sayac}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Görev Kartları Döngüsü
        for g in sutun_gorevleri:
            kalan_gun = g.kalan_gun_hesapla()
            
            if kalan_gun < 0:
                kalan_metin = f"Süresi Geçti ({abs(kalan_gun)}g)"
            elif kalan_gun == 0:
                kalan_metin = "Son Gün"
            else:
                kalan_metin = f"{kalan_gun} gün kaldı"
            
            # Seçim kutusu (Dropdown) opsiyon listesini hazırlama
            tüm_durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]
            options_html = f'<option value="{g.durum}" selected disabled>{g.durum}</option>'
            for d in tüm_durumlar:
                if d != g.durum:
                    options_html += f'<option value="{d}">{d}</option>'

            # 🔥 HER ŞEYİ İÇİNE ALAN, ASLA BÖLÜNMEYEN TEK PARÇA KART HTML'İ
            # (En alttaki unsafe_allow_html=True parametresi sayesinde kod olarak basılmak yerine tam render edilir)
            st.markdown(f"""
                <div class="premium-task-card">
                    <div class="indicator-{g.zorluk}"></div>
                    
                    <div class="task-title">
                        {g.ad}
                        <span class="badge badge-{g.zorluk}">{g.zorluk}</span>
                    </div>
                    
                    <div class="task-time">
                        <span>📅 {g.son_tarih}</span>
                        <span style="font-weight:600; color:{'#f87171' if kalan_gun<=0 else '#9ca3af'}">{kalan_metin}</span>
                    </div>
                    
                    <div class="card-controls">
                        <select class="html-dropdown" onchange="window.location.href='?action=move&id={g.id}&target=' + this.value">
                            {options_html}
                        </select>
                        <a class="html-delete-button" href="?action=delete&id={g.id}" title="Görevi Sil">🗑️</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)