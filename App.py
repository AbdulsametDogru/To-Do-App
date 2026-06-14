import streamlit as st
from Backend import GorevYoneticisi
import datetime

st.set_page_config(page_title="Sprint Board Pro", layout="wide", page_icon="⚡")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

*, *::before, *::after {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-sizing: border-box;
}

/* Ana arka plan */
.stApp {
    background:
        radial-gradient(ellipse at 15% 10%, rgba(239,68,68,0.09) 0%, transparent 45%),
        radial-gradient(ellipse at 85% 15%, rgba(59,130,246,0.11) 0%, transparent 45%),
        radial-gradient(ellipse at 50% 85%, rgba(16,185,129,0.07) 0%, transparent 50%),
        linear-gradient(150deg, #07080f 0%, #10121e 55%, #040508 100%) !important;
    background-attachment: fixed !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1020 0%, #060709 100%) !important;
    border-right: 1px solid rgba(59,130,246,0.18) !important;
}
[data-testid="stSidebar"] .stForm {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    padding: 18px !important;
}
[data-testid="stSidebar"] button[kind="primaryFormSubmit"] {
    background: linear-gradient(90deg,#1d4ed8,#3b82f6) !important;
    border: none !important;
    box-shadow: 0 0 18px rgba(59,130,246,0.35) !important;
}

/* Kanban sütunlar */
[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    background: rgba(5,7,12,0.65) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 22px !important;
    padding: 22px 18px !important;
    box-shadow: 0 18px 45px rgba(0,0,0,0.6) !important;
}

/* Genel arka plan temizliği */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="element-container"],
[data-testid="stVerticalBlock"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Kolon başlığı */
.col-header {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.6px;
    padding: 12px 16px;
    border-radius: 11px;
    margin-bottom: 20px;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.col-badge {
    background: rgba(255,255,255,0.18);
    padding: 2px 9px;
    border-radius: 18px;
    font-size: 11px;
}

/* Görev kartı — sade, pozisyon hack'i yok */
.task-card {
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 4px;          /* butonlarla minimal boşluk */
    border: 1px solid transparent;
}
.task-card.Zor  { background: linear-gradient(135deg,#7f1d1d,#3f0707); border-color: rgba(239,68,68,0.38); }
.task-card.Orta { background: linear-gradient(135deg,#7c2d12,#3b0f04); border-color: rgba(245,158,11,0.38); }
.task-card.Kolay{ background: linear-gradient(135deg,#064e3b,#01201a); border-color: rgba(16,185,129,0.33); }

.task-title {
    color: #fff;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
}
.task-title span:first-child {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
}
.badge {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.18);
    color: #fff;
    padding: 3px 9px;
    border-radius: 7px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    flex-shrink: 0;
}
.task-meta {
    color: rgba(255,255,255,0.78);
    font-size: 12px;
    display: flex;
    justify-content: space-between;
}
.overdue { color: #ff8585; font-weight: 700; }

/* Kart altı butonlar */
.stButton > button {
    width: 100% !important;
    border-radius: 8px !important;
    background: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    padding: 5px 4px !important;
    transition: background 0.15s ease !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.22) !important;
}

/* Düzenleme modali */
div[role="dialog"] {
    background: linear-gradient(135deg,#131722,#090a0f) !important;
    border: 1px solid rgba(59,130,246,0.28) !important;
    border-radius: 18px !important;
}
div[role="dialog"] h1, div[role="dialog"] p { color: #fff !important; }
div[role="dialog"] .stButton button {
    background: linear-gradient(90deg,#059669,#10b981) !important;
    box-shadow: 0 0 14px rgba(16,185,129,0.28) !important;
    border: none !important;
}

/* Buton satırının üstünde gereksiz boşluk engeli */
div[data-testid="stHorizontalBlock"] {
    margin-top: 0 !important;
    gap: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# --- Oturum başlat ---
if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()

yon = st.session_state.yonetici


# --- Düzenleme modali ---
@st.dialog("📝 Görevi Güncelle")
def gorev_duzenle(gorev):
    st.markdown(f"**{gorev.ad}** görevini güncelle:")
    yeni_ad      = st.text_input("Görev Adı", value=gorev.ad)
    yeni_durum   = st.selectbox("Aşama", ["Yapılacak","Yapılıyor","Tamamlandı"],
                                index=["Yapılacak","Yapılıyor","Tamamlandı"].index(gorev.durum))
    yeni_zorluk  = st.selectbox("Öncelik", ["Kolay","Orta","Zor"],
                                index=["Kolay","Orta","Zor"].index(gorev.zorluk))
    mevcut       = datetime.datetime.strptime(gorev.son_tarih, "%d/%m/%Y").date()
    yeni_tarih   = st.date_input("Deadline", value=mevcut)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Kaydet", type="primary"):
        if yeni_ad.strip():
            gorev.ad       = yeni_ad
            gorev.durum    = yeni_durum
            gorev.zorluk   = yeni_zorluk
            gorev.son_tarih = yeni_tarih.strftime("%d/%m/%Y")
            yon.gorevleri_kaydet()
            st.rerun()


# --- Üst metrik şeridi ---
toplam     = len(yon.gorevler)
tamamlanan = len([x for x in yon.gorevler if x.durum == "Tamamlandı"])
yapilan    = len([x for x in yon.gorevler if x.durum == "Yapılıyor"])
ilerleme   = (tamamlanan / toplam) if toplam > 0 else 0.0

st.markdown("""
<div style='margin-bottom:22px;'>
  <h1 style='color:#fff;font-weight:800;font-size:26px;margin-bottom:4px;'>
    Workspace / <span style='color:#3b82f6;'>Sprint Board Pro</span>
  </h1>
  <p style='color:#475569;margin:0;font-size:13px;'>Görevleri takip et, öncelikleri yönet.</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns([2.5, 1, 1, 1])
with m1:
    st.markdown(f"<p style='color:#94a3b8;font-size:12px;margin-bottom:5px;'>Sprint İlerleme: {int(ilerleme*100)}%</p>",
                unsafe_allow_html=True)
    st.progress(ilerleme)
with m2: st.metric("Toplam",  toplam)
with m3: st.metric("Aktif",   yapilan)
with m4: st.metric("Biten",   tamamlanan)

st.markdown("<div style='margin-bottom:28px;'></div>", unsafe_allow_html=True)


# --- Sidebar: görev ekle ---
st.sidebar.markdown("<h2 style='color:#fff;font-weight:800;font-size:20px;'>Kontrol Merkezi</h2>",
                    unsafe_allow_html=True)
with st.sidebar.form("gorev_ekle", clear_on_submit=True):
    st.markdown("<p style='color:#3b82f6;font-weight:600;margin-bottom:4px;'>Yeni Görev Ekle</p>",
                unsafe_allow_html=True)
    ad       = st.text_input("Görev Tanımı")
    durum    = st.selectbox("Başlangıç Aşaması", ["Yapılacak","Yapılıyor","Tamamlandı"])
    zorluk   = st.selectbox("Öncelik", ["Kolay","Orta","Zor"])
    son_tar  = st.date_input("Deadline", min_value=datetime.date.today())
    if st.form_submit_button("🚀 Görevi Ekle"):
        if ad.strip():
            yon.gorev_ekle(ad, durum, zorluk, son_tar.strftime("%d/%m/%Y"))
            st.rerun()

yon.gorevleri_sirala()


# --- Kanban tahtası ---
s1, s2, s3 = st.columns(3)
kolonlar = {
    "Yapılacak":  (s1, "Yapılacaklar",    "linear-gradient(90deg,#1e3a8a,#1d4ed8)"),
    "Yapılıyor":  (s2, "Yapılıyor",       "linear-gradient(90deg,#9a3412,#c2410c)"),
    "Tamamlandı": (s3, "Tamamlandı",      "linear-gradient(90deg,#065f46,#047857)"),
}

for anahtar, (kolon, baslik, renk) in kolonlar.items():
    filtre = [x for x in yon.gorevler if x.durum == anahtar]
    with kolon:
        # Kolon başlığı
        st.markdown(f"""
        <div class='col-header' style='background:{renk};'>
          <span>{baslik}</span>
          <span class='col-badge'>{len(filtre)}</span>
        </div>
        """, unsafe_allow_html=True)

        for g in filtre:
            k = g.kalan_gun_hesapla()
            if k < 0:
                k_metin = f"Gecikti ({abs(k)}g)"
                renk_cls = "overdue"
            elif k == 0:
                k_metin = "Son Gün"
                renk_cls = "overdue"
            else:
                k_metin = f"{k} gün kaldı"
                renk_cls = ""

            # Kart HTML — sade, absolute yok
            st.markdown(f"""
            <div class='task-card {g.zorluk}'>
              <div class='task-title'>
                <span>{g.ad}</span>
                <span class='badge'>{g.zorluk}</span>
              </div>
              <div class='task-meta'>
                <span>📅 {g.son_tarih}</span>
                <span class='{renk_cls}'>{k_metin}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Butonlar kartın hemen altında, normal akışta
            b1, b2 = st.columns(2)
            with b1:
                if st.button("✏️ Düzenle", key=f"edit_{g.id}"):
                    gorev_duzenle(g)
            with b2:
                if st.button("🗑️ Sil", key=f"rm_{g.id}"):
                    yon.gorev_sil(g.id)
                    st.rerun()

            # Kartlar arası görsel ayraç
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)