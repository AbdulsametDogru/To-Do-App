import streamlit as st
from Backend import GorevYoneticisi

st.set_page_config(page_title="Sprint Board Pro", layout="wide")

# Neon CSS
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1c183d 0%, #251b5a 40%, #162942 100%) !important; color: white; }
.col-header { font-size: 14px; font-weight: 800; color: #fff; padding: 12px; background: rgba(255,255,255,0.08); border-radius: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
.task-card { background: rgba(255,255,255,0.05); padding: 16px; border-radius: 14px; margin-bottom: 12px; border-left: 6px solid #a78bfa; }
</style>
""", unsafe_allow_html=True)

if "yonetici" not in st.session_state:
    st.session_state.yonetici = GorevYoneticisi()
yon = st.session_state.yonetici

# Düzenleme Modalı
@st.dialog("Düzenle")
def gorev_duzenle(gorev):
    yeni_ad = st.text_input("Ad", value=gorev.ad)
    yeni_durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"], index=["Yapılacak", "Yapılıyor", "Tamamlandı"].index(gorev.durum))
    if st.button("Kaydet"):
        gorev.ad = yeni_ad
        gorev.durum = yeni_durum
        yon.gorev_guncelle(gorev)
        st.rerun()

# Sidebar
with st.sidebar:
    with st.form("ekle", clear_on_submit=True):
        ad = st.text_input("Görev")
        durum = st.selectbox("Aşama", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
        tarih = st.date_input("Deadline")
        if st.form_submit_button("Ekle"):
            yon.gorev_ekle(ad, durum, "Orta", tarih.strftime("%Y-%m-%d"))
            st.rerun()

# Board
col1, col2, col3 = st.columns(3)
for col, durum in zip([col1, col2, col3], ["Yapılacak", "Yapılıyor", "Tamamlandı"]):
    with col:
        st.markdown(f"<div class='col-header'>{durum.upper()}</div>", unsafe_allow_html=True)
        for g in [g for g in yon.gorevler if g.durum == durum]:
            st.markdown(f"<div class='task-card'>{g.ad}<br><small>{g.son_tarih}</small></div>", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            if b1.button("✏️", key=f"e{g.id}"): gorev_duzenle(g)
            if b2.button("🗑️", key=f"d{g.id}"): yon.gorev_sil(g.id); st.rerun()