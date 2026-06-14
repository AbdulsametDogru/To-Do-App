import streamlit as st
from Backend import GorevYoneticisi
import datetime

st.set_page_config(page_title="Sprint Board Pro", layout="wide", page_icon="⚡")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
*, *::before, *::after { font-family: 'Plus Jakarta Sans', sans-serif !important; box-sizing: border-box; }

.stApp {
    background:
        radial-gradient(ellipse at 0% 0%, rgba(139,92,246,0.35) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 0%, rgba(59,130,246,0.30) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 100%, rgba(236,72,153,0.25) 0%, transparent 55%),
        radial-gradient(ellipse at 80% 60%, rgba(16,185,129,0.15) 0%, transparent 40%),
        linear-gradient(135deg, #0f0c29 0%, #1a1040 40%, #0d1b2a 100%) !important;
    background-attachment: fixed !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #130d35 0%, #0a0718 100%) !important;
    border-right: 1px solid rgba(139,92,246,0.25) !important;
}
[data-testid="stSidebar"] .stForm {
    background: rgba(139,92,246,0.06) !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 14px !important; padding: 18px !important;
}
[data-testid="stSidebar"] button[kind="primaryFormSubmit"] {
    background: linear-gradient(90deg,#7c3aed,#a855f7) !important;
    border: none !important; box-shadow: 0 0 20px rgba(139,92,246,0.45) !important;
}
[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    background: rgba(15,10,40,0.55) !important;
    backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 22px !important; padding: 22px 18px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5) !important;
}
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="element-container"],
[data-testid="stVerticalBlock"] {
    background: transparent !important; border: none !important; box-shadow: none !important;
}
.col-header {
    font-size: 12px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.8px; padding: 12px 16px; border-radius: 11px;
    margin-bottom: 18px; color: #fff;
    display: flex; align-items: center; justify-content: space-between;
}
.col-badge { background:rgba(255,255,255,0.2); padding:2px 10px; border-radius:18px; font-size:11px; }

/* KART */
.task-card {
    border-radius: 14px; padding: 16px; margin-bottom: 10px;
    border: 1px solid transparent; cursor: pointer;
    transition: transform 0.15s ease, filter 0.15s ease;
    user-select: none;
}
.task-card:hover { transform: translateY(-2px); filter: brightness(1.1); }
.task-card.Zor   { background:linear-gradient(135deg,#7f1d1d,#450a0a); border-color:rgba(239,68,68,0.45); box-shadow:0 8px 25px rgba(239,68,68,0.2); }
.task-card.Orta  { background:linear-gradient(135deg,#78350f,#431407); border-color:rgba(245,158,11,0.45); box-shadow:0 8px 25px rgba(245,158,11,0.15); }
.task-card.Kolay { background:linear-gradient(135deg,#064e3b,#022c22); border-color:rgba(16,185,129,0.40); box-shadow:0 8px 25px rgba(16,185,129,0.15); }
.task-card.acik.Zor   { border-color:rgba(239,68,68,0.9)!important; box-shadow:0 0 22px rgba(239,68,68,0.4)!important; border-radius:14px 14px 0 0!important; margin-bottom:0!important; }
.task-card.acik.Orta  { border-color:rgba(245,158,11,0.9)!important; box-shadow:0 0 22px rgba(245,158,11,0.35)!important; border-radius:14px 14px 0 0!important; margin-bottom:0!important; }
.task-card.acik.Kolay { border-color:rgba(16,185,129,0.9)!important; box-shadow:0 0 22px rgba(16,185,129,0.35)!important; border-radius:14px 14px 0 0!important; margin-bottom:0!important; }

.task-title { color:#fff; font-size:15px; font-weight:700; margin-bottom:10px; display:flex; justify-content:space-between; align-items:flex-start; gap:8px; }
.task-title span:first-child { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1; }
.badge { background:rgba(255,255,255,0.14); border:1px solid rgba(255,255,255,0.2); color:#fff; padding:3px 9px; border-radius:7px; font-size:10px; font-weight:700; text-transform:uppercase; flex-shrink:0; }
.task-meta { color:rgba(255,255,255,0.72); font-size:12px; display:flex; justify-content:space-between; }
.overdue { color:#fca5a5!important; font-weight:700; }
.tap-hint { color:rgba(255,255,255,0.22); font-size:10px; text-align:right; margin-top:10px; }

/* AÇILIR MENÜ */
.action-menu { border-radius:0 0 14px 14px; border:1px solid transparent; border-top:none; overflow:hidden; margin-bottom:10px; }
.action-menu.Zor   { background:rgba(60,5,5,0.88);  border-color:rgba(239,68,68,0.9); }
.action-menu.Orta  { background:rgba(55,18,3,0.88); border-color:rgba(245,158,11,0.9); }
.action-menu.Kolay { background:rgba(2,28,20,0.88); border-color:rgba(16,185,129,0.9); }
.action-menu .stButton > button {
    all: unset !important;
    display:flex!important; align-items:center!important; gap:12px!important;
    width:100%!important; padding:13px 18px!important;
    color:rgba(255,255,255,0.85)!important; font-size:14px!important;
    font-weight:500!important; cursor:pointer!important;
    border-bottom:1px solid rgba(255,255,255,0.07)!important;
    transition:background 0.12s ease!important; box-sizing:border-box!important;
}
.action-menu .stButton > button:hover { background:rgba(255,255,255,0.09)!important; color:#fff!important; }
.action-menu .stButton:last-child > button { border-bottom:none!important; }

/* Toggle buton — ince şerit, karta yapışık */
.toggle-btn .stButton > button {
    all: unset !important;
    display: block !important;
    width: 100% !important;
    height: 28px !important;
    cursor: pointer !important;
    border-radius: 0 0 14px 14px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-top: none !important;
    background: rgba(255,255,255,0.03) !important;
    text-align: center !important;
    font-size: 11px !important;
    color: rgba(255,255,255,0.2) !important;
    letter-spacing: 2px !important;
    transition: background 0.12s !important;
    margin-bottom: 10px !important;
    line-height: 28px !important;
}
.toggle-btn .stButton > button:hover { background: rgba(255,255,255,0.07) !important; color: rgba(255,255,255,0.4) !important; }
/* Açıkken toggle rengi */
.toggle-btn-acik .stButton > button {
    border-radius: 0 !important;
    background: rgba(255,255,255,0.04) !important;
    margin-bottom: 0 !important;
}

/* Modal */
div[role="dialog"] { background:linear-gradient(135deg,#1a1040,#0d0720)!important; border:1px solid rgba(139,92,246,0.35)!important; border-radius:18px!important; }
div[role="dialog"] h1, div[role="dialog"] p { color:#fff!important; }
div[role="dialog"] .stButton button { background:linear-gradient(90deg,#7c3aed,#a855f7)!important; box-shadow:0 0 16px rgba(139,92,246,0.35)!important; border:none!important; color:#fff!important; border-radius:8px!important; padding:10px 20px!important; font-weight:600!important; width:100%!important; }
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
  <h1 style='color:#fff;font-weight:800;font-size:26px;margin-bottom:4px;'>
    Workspace / <span style='color:#a855f7;'>Sprint Board Pro</span>
  </h1>
  <p style='color:#64748b;margin:0;font-size:13px;'>Görevleri takip et, öncelikleri yönet.</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns([2.5, 1, 1, 1])
with m1:
    st.markdown(f"<p style='color:#94a3b8;font-size:12px;margin-bottom:5px;'>Sprint İlerleme: {int(ilerleme*100)}%</p>", unsafe_allow_html=True)
    st.progress(ilerleme)
with m2: st.metric("Toplam", toplam)
with m3: st.metric("Aktif",  yapilan)
with m4: st.metric("Biten",  tamamlanan)
st.markdown("<div style='margin-bottom:28px;'></div>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color:#fff;font-weight:800;font-size:20px;'>Kontrol Merkezi</h2>", unsafe_allow_html=True)
with st.sidebar.form("gorev_ekle", clear_on_submit=True):
    st.markdown("<p style='color:#a855f7;font-weight:600;margin-bottom:4px;'>Yeni Görev Ekle</p>", unsafe_allow_html=True)
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
    "Yapılacak":  (s1, "Yapılacaklar", "linear-gradient(90deg,#4c1d95,#6d28d9)"),
    "Yapılıyor":  (s2, "Yapılıyor",    "linear-gradient(90deg,#9a3412,#ea580c)"),
    "Tamamlandı": (s3, "Tamamlandı",   "linear-gradient(90deg,#065f46,#059669)"),
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