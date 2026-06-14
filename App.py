import streamlit as st
from Backend import GorevYoneticisi
import datetime

st.set_page_config(page_title="Sprint Board Pro", layout="wide", page_icon="⚡")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
*, *::before, *::after { font-family: 'Plus Jakarta Sans', sans-serif !important; box-sizing: border-box; }

/* Arka plan renkleri ve parlamaları biraz daha açık hale getirildi */
.stApp {
    background:
        radial-gradient(ellipse at 0% 0%, rgba(155,109,255,0.45) 0%, transparent 60%),
        radial-gradient(ellipse at 100% 0%, rgba(96,165,250,0.40) 0%, transparent 60%),
        radial-gradient(ellipse at 50% 100%, rgba(244,114,182,0.35) 0%, transparent 60%),
        linear-gradient(135deg, #181439 0%, #231854 40%, #13243a 100%) !important;
    background-attachment: fixed !important;
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

/* Sütunlar ve Mobil Duyarlılık */
[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    background: rgba(22,15,54,0.65) !important;
    backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 22px !important; padding: 20px 16px !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4) !important;
    margin-bottom: 16px; /* Mobilde alt alta gelince boşluk kalması için */
}

[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="element-container"],
[data-testid="stVerticalBlock"] {
    background: transparent !important; border: none !important; box-shadow: none !important;
}

.col-header {
    font-size: 13px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.8px; padding: 14px 16px; border-radius: 11px;
    margin-bottom: 18px; color: #fff;
    display: flex; align-items: center; justify-content: space-between;
}
.col-badge { background:rgba(255,255,255,0.25); padding:2px 10px; border-radius:18px; font-size:12px; font-weight:700; }

/* KART - Okunabilirlik ve Mobil Uyum Artırıldı */
.task-card {
    border-radius: 14px; padding: 18px; margin-bottom: 0px;
    border: 1px solid transparent; cursor: pointer;
    transition: transform 0.15s ease, filter 0.15s ease;
    user-select: none;
}
.task-card:hover { transform: translateY(-2px); filter: brightness(1.1); }

/* Renkler kontrast için bir tık canlandırıldı */
.task-card.Zor   { background:linear-gradient(135deg,#991b1b,#580a0a); border-color:rgba(239,68,68,0.55); }
.task-card.Orta  { background:linear-gradient(135deg,#92400e,#541c07); border-color:rgba(245,158,11,0.55); }
.task-card.Kolay { background:linear-gradient(135deg,#065f46,#022c22); border-color:rgba(16,185,129,0.50); }

.task-card.acik.Zor   { border-color:rgba(239,68,68,0.95)!important; border-radius:14px 14px 0 0!important; }
.task-card.acik.Orta  { border-color:rgba(245,158,11,0.95)!important; border-radius:14px 14px 0 0!important; }
.task-card.acik.Kolay { border-color:rgba(16,185,129,0.95)!important; border-radius:14px 14px 0 0!important; }

/* Başlık mobilde taşmasın diye wrap eklendi */
.task-title { color:#fff; font-size:16px; font-weight:700; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap: wrap; }
.task-title span:first-child { overflow:hidden; text-overflow:ellipsis; white-space:normal; word-break:break-word; flex:1; min-width:120px; }
.badge { background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.25); color:#fff; padding:4px 10px; border-radius:8px; font-size:11px; font-weight:700; text-transform:uppercase; flex-shrink:0; }
.task-meta { color:rgba(255,255,255,0.8); font-size:13px; display:flex; justify-content:space-between; flex-wrap: wrap; gap: 4px; }
.overdue { color:#fee2e2!important; background: rgba(220,38,38,0.4); padding: 1px 6px; border-radius: 4px; font-weight:700; }

/* TOGGLE BUTON - Mobilde dokunmayı kolaylaştırmak için büyütüldü */
.toggle-btn .stButton > button, .toggle-btn-acik .stButton > button {
    all: unset !important;
    display: block !important;
    width: 100% !important;
    height: 36px !important; /* Dokunma alanı genişletildi */
    cursor: pointer !important;
    background: rgba(255,255,255,0.06) !important;
    text-align: center !important;
    font-size: 14px !important; /* İkonlar büyütüldü */
    color: rgba(255,255,255,0.4) !important;
    letter-spacing: 2px !important;
    transition: background 0.12s, color 0.12s !important;
    line-height: 36px !important;
    box-sizing: border-box !important;
}
.toggle-btn .stButton > button {
    border-radius: 0 0 14px 14px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-top: none !important;
    margin-bottom: 14px !important;
}
.toggle-btn-acik .stButton > button {
    border-radius: 0 !important;
    border-left: 1px solid rgba(255,255,255,0.1) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
    border-top: none !important;
    border-bottom: none !important;
    background: rgba(255,255,255,0.08) !important;
    margin-bottom: 0 !important;
}
.toggle-btn .stButton > button:hover, .toggle-btn-acik .stButton > button:hover { background: rgba(255,255,255,0.12) !important; color: #fff !important; }

/* AÇILIR MENÜ - Dokunma alanları ve okunabilirlik artırıldı */
.action-menu { border-radius:0 0 14px 14px; border:1px solid transparent; border-top:none; overflow:hidden; margin-bottom:14px; }
.action-menu.Zor   { background:rgba(75,10,10,0.95);  border-color:rgba(239,68,68,0.95); }
.action-menu.Orta  { background:rgba(69,26,7,0.95); border-color:rgba(245,158,11,0.95); }
.action-menu.Kolay { background:rgba(4,47,31,0.95); border-color:rgba(16,185,129,0.95); }
.action-menu .stButton > button {
    all: unset !important;
    display:flex!important; align-items:center!important; gap:12px!important;
    width:100%!important; padding:15px 20px!important; /* Parmak dostu genişlik */
    color:rgba(255,255,255,0.9)!important; font-size:15px!important;
    font-weight:600!important; cursor:pointer!important;
    border-bottom:1px solid rgba(255,255,255,0.1)!important;
    transition:background 0.12s ease!important; box-sizing:border-box!important;
}
.action-menu .stButton > button:hover { background:rgba(255,255,255,0.12)!important; color:#fff!important; }
.action-menu .stButton:last-child > button { border-bottom:none!important; }

/* Modal */
div[role="dialog"] { background:linear-gradient(135deg,#241754,#120b2b)!important; border:1px solid rgba(139,92,246,0.45)!important; border-radius:18px!important; }
div[role="dialog"] h1, div[role="dialog"] p { color:#fff!important; }
div[role="dialog"] .stButton button { background:linear-gradient(90deg,#8b5cf6,#a855f7)!important; border:none!important; color:#fff!important; border-radius:8px!important; padding:12px 20px!important; font-weight:600!important; width:100%!important; }
</style>
""", unsafe_allow_html=True)

if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()
if "acik_kart" not in st.session_state:
    st.session_state.acik_kart = None

yon = st.session_state.yonetici


@st.dialog("📝 Görevi Güncelle")
def gorev_duzenle(gorev):
    yeni_ad     = st.text_input("Görev Adı", value=gorev.ad)
    yeni_durum  = st.selectbox("Aşama", ["Yapılacak","Yapılıyor","Tamamlandı"],
                               index=["Yapılacak","Yapılıyor","Tamamlandı"].index(gorev.durum))
    yeni_zorluk = st.selectbox("Öncelik", ["Kolay","Orta","Zor"],
                               index=["Kolay","Orta","Zor"].index(gorev.zorluk))
    mevcut      = datetime.datetime.strptime(gorev.son_tarih, "%d/%m/%Y").date()
    yeni_tarih  = st.date_input("Deadline", value=mevcut)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Kaydet", type="primary"):
        if yeni_ad.strip():
            gorev.ad        = yeni_ad
            gorev.durum     = yeni_durum
            gorev.zorluk    = yeni_zorluk
            gorev.son_tarih = yeni_tarih.strftime("%d/%m/%Y")
            yon.gorevleri_kaydet()
            st.session_state.acik_kart = None
            st.rerun()


toplam     = len(yon.gorevler)
tamamlanan = len([x for x in yon.gorevler if x.durum == "Tamamlandı"])
yapilan    = len([x for x in yon.gorevler if x.durum == "Yapılıyor"])
ilerleme   = (tamamlanan / toplam) if toplam > 0 else 0.0

st.markdown("""
<div style='margin-bottom:22px;'>
  <h1 style='color:#fff;font-weight:800;font-size:28px;margin-bottom:4px;'>
    Workspace / <span style='color:#c084fc;'>Sprint Board Pro</span>
  </h1>
  <p style='color:#94a3b8;margin:0;font-size:14px;'>Görevleri takip et, öncelikleri yönet.</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns([2.5, 1, 1, 1])
with m1:
    st.markdown(f"<p style='color:#cbd5e1;font-size:13px;margin-bottom:5px;font-weight:600;'>Sprint İlerleme: {int(ilerleme*100)}%</p>", unsafe_allow_html=True)
    st.progress(ilerleme)
with m2: st.metric("Toplam", toplam)
with m3: st.metric("Aktif",  yapilan)
with m4: st.metric("Biten",  tamamlanan)
st.markdown("<div style='margin-bottom:28px;'></div>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color:#fff;font-weight:800;font-size:20px;'>Kontrol Merkezi</h2>", unsafe_allow_html=True)
with st.sidebar.form("gorev_ekle", clear_on_submit=True):
    st.markdown("<p style='color:#c084fc;font-weight:600;margin-bottom:4px;'>Yeni Görev Ekle</p>", unsafe_allow_html=True)
    ad      = st.text_input("Görev Tanımı")
    durum   = st.selectbox("Başlangıç Aşaması", ["Yapılacak","Yapılıyor","Tamamlandı"])
    zorluk  = st.selectbox("Öncelik", ["Kolay","Orta","Zor"])
    son_tar = st.date_input("Deadline", min_value=datetime.date.today())
    if st.form_submit_button("🚀 Görevi Ekle"):
        if ad.strip():
            yon.gorev_ekle(ad, durum, zorluk, son_tar.strftime("%d/%m/%Y"))
            st.rerun()

yon.gorevleri_sirala()

s1, s2, s3 = st.columns(3)
kolonlar = {
    "Yapılacak":  (s1, "Yapılacaklar", "linear-gradient(90deg,#5b21b6,#7c3aed)"),
    "Yapılıyor":  (s2, "Yapılıyor",    "linear-gradient(90deg,#b45309,#f97316)"),
    "Tamamlandı": (s3, "Tamamlandı",   "linear-gradient(90deg,#065f46,#10b981)"),
}

for anahtar, (kolon, baslik, renk) in kolonlar.items():
    filtre = [x for x in yon.gorevler if x.durum == anahtar]
    with kolon:
        st.markdown(f"""
        <div class='col-header' style='background:{renk};'>
          <span>{baslik}</span><span class='col-badge'>{len(filtre)}</span>
        </div>""", unsafe_allow_html=True)

        for g in filtre:
            k = g.kalan_gun_hesapla()
            if k < 0:    k_metin, k_cls = f"Gecikti ({abs(k)}g)", "overdue"
            elif k == 0: k_metin, k_cls = "Son Gün", "overdue"
            else:         k_metin, k_cls = f"{k} gün kaldı", ""

            acik     = (st.session_state.acik_kart == g.id)
            acik_cls = "acik" if acik else ""

            # Kart HTML
            st.markdown(f"""
            <div class='task-card {g.zorluk} {acik_cls}'>
              <div class='task-title'>
                <span>{g.ad}</span>
                <span class='badge'>{g.zorluk}</span>
              </div>
              <div class='task-meta'>
                <span>📅 {g.son_tarih}</span>
                <span class='{k_cls}'>{k_metin}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Kartın hemen altında görünmez ince şerit buton (tek tıklama noktası)
            toggle_cls = "toggle-btn-acik" if acik else "toggle-btn"
            st.markdown(f"<div class='{toggle_cls}'>", unsafe_allow_html=True)
            if st.button("• • •" if not acik else "▲", key=f"toggle_{g.id}"):
                st.session_state.acik_kart = None if acik else g.id
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            # Açılır menü
            if acik:
                st.markdown(f"<div class='action-menu {g.zorluk}'>", unsafe_allow_html=True)
                if st.button("✏️   Düzenle", key=f"edit_{g.id}"):
                    gorev_duzenle(g)
                if st.button("🗑️   Sil", key=f"rm_{g.id}"):
                    yon.gorev_sil(g.id)
                    st.session_state.acik_kart = None
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)