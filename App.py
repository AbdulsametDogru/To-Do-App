import streamlit as st
from Backend import GorevYoneticisi
from datetime import date, datetime
from auth import Auth

st.set_page_config(page_title="Neon Sprint Board Pro", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
/* Modern Font İçe Aktarımı */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

.stApp {
    background: radial-gradient(circle at 70% 30%, #581c87, #0f172a),
                radial-gradient(circle at 20% 80%, #991b1b, #0f172a);
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

/* Başlıkları Modernize Et */
h1, h2, h3 {
    font-weight: 700 !important;
    letter-spacing: -0.025em;
    color: #ffffff;
}

/* Kartlar - Daha Modern ve Yumuşak */
.task-card { 
    padding: 20px; 
    border-radius: 16px; 
    margin-bottom: 16px; 
    background: rgba(30, 41, 59, 0.4); 
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.task-card:hover { 
    transform: translateY(-5px);
    background: rgba(30, 41, 59, 0.6);
}

/* Zorluk Renkleri - Neon Tonları */
.difficulty-easy { border-left: 6px solid #10b981; box-shadow: 5px 0 15px -5px #10b981; }
.difficulty-medium { border-left: 6px solid #f59e0b; box-shadow: 5px 0 15px -5px #f59e0b; }
.difficulty-hard { border-left: 6px solid #ef4444; box-shadow: 5px 0 15px -5px #ef4444; }

/* Rozet ve Yazı Tipi */
.badge { 
    display: inline-block; 
    padding: 4px 12px; 
    border-radius: 8px; 
    font-size: 11px; 
    font-weight: 600; 
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.title { font-size: 17px; font-weight: 600; color: #ffffff; }
.info { font-size: 12px; color: #94a3b8; margin-top: 6px; }

/* Progress Bar Modernizasyonu */
.stProgress > div > div > div > div {
    background-image: linear-gradient(90deg, #8b5cf6, #ec4899);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if "kullanici_adi" not in st.session_state:
    st.markdown("<h1 style='text-align:center;color:#8b5cf6;margin-top:80px;'>⚡ Cyber Sprint Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab1, tab2 = st.tabs(["Giriş", "Kayıt"])
        with tab1:
            user = st.text_input("Kullanıcı", key="login_user")
            pw = st.text_input("Şifre", type="password", key="login_pw")

            if st.button("Giriş"):
                if not user or not pw:
                    st.error("Lütfen kullanıcı adı ve şifre giriniz.")
                else:
                    try:
                        if Auth.giris(user, pw):
                            st.session_state.kullanici_adi = user
                            st.rerun()
                        else:
                            st.error("Hatalı kullanıcı adı veya şifre.")
                    except Exception as e:
                        st.error("Sistemsel bir hata oluştu, lütfen daha sonra tekrar deneyin.")
        with tab2:
            u = st.text_input("Yeni kullanıcı", key="reg_user")
            p = st.text_input("Şifre", type="password", key="reg_pw")
            if st.button("Kayıt"):
                if Auth.kayit(u, p):
                    st.success("Kayıt başarılı, giriş yapabilirsiniz.")
                else:
                    st.warning("Bu kullanıcı zaten var.")
    st.stop()

# ---------------- LOGIC ----------------
yon = GorevYoneticisi(st.session_state.kullanici_adi)

def kalan_gun(t):
    try: return (datetime.strptime(t, "%Y-%m-%d").date() - date.today()).days
    except: return 0

def zorluk_class(z): return {"Kolay": "easy", "Orta": "medium", "Zor": "hard"}.get(z, "medium")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.kullanici_adi}")
    with st.form("add_form", clear_on_submit=True):
        ad = st.text_input("Görev")
        durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
        zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"])
        tarih = st.date_input("Tarih", min_value=date.today())
        
        # Görev ekleme mantığını try-except içine alıyoruz
        if st.form_submit_button("Ekle"):
            if not ad or ad.strip() == "":
                st.error("⚠️ Lütfen bir görev adı girin.")
            else:
                try:
                    yon.gorev_ekle(ad, durum, zorluk, str(tarih))
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")

    if st.button("Çıkış"):
        del st.session_state.kullanici_adi
        st.rerun()

# ---------------- METRİKLER VE İLERLEME ----------------
# Verileri hesaplayalım
toplam_gorev = len(yon.gorevler)
yapilacak = len([g for g in yon.gorevler if g.durum == "Yapılacak"])
yapiliyor = len([g for g in yon.gorevler if g.durum == "Yapılıyor"])
tamamlanan = len([g for g in yon.gorevler if g.durum == "Tamamlandı"])

# İlerleme oranı (0 ile 1 arası)
ilerleme = tamamlanan / toplam_gorev if toplam_gorev > 0 else 0

st.markdown("### 📊 Sprint Özeti")
m1, m2, m3 = st.columns(3)
m1.metric("Yapılacak", yapilacak)
m2.metric("Yapılıyor", yapiliyor)
m3.metric("Tamamlanan", tamamlanan)

st.write(f"**Sprint Tamamlanma Oranı: %{int(ilerleme * 100)}**")
st.progress(ilerleme)
st.divider() # Görsel ayrım çizgisi

# ---------------- BOARD ----------------
st.title("SPRINT CONTROL CENTER")
cols = st.columns(3)
durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]

for i, col in enumerate(cols):
    with col:
        st.subheader(durumlar[i])
        for g in [x for x in yon.gorevler if x.durum == durumlar[i]]:
            kalan = kalan_gun(g.son_tarih)
            diff = zorluk_class(g.zorluk)
            st.markdown(f"""
            <div class="task-card difficulty-{diff}">
                <div class="title">{g.ad}</div>
                <div class="info">📅 {g.son_tarih}</div>
                <div class="info">⏳ {kalan if kalan >= 0 else "Gecikti"} gün</div>
                <div style="margin-top:6px"><span class="badge badge-{diff}">{g.zorluk}</span></div>
            </div>""", unsafe_allow_html=True)
            
            with st.expander("İşlemler"):
                new_ad = st.text_input("Ad", g.ad, key=f"a{g.id}")
                new_durum = st.selectbox("Durum", durumlar, index=durumlar.index(g.durum), key=f"d{g.id}")
                new_zorluk = st.selectbox("Zorluk", ["Kolay","Orta","Zor"], index=["Kolay","Orta","Zor"].index(g.zorluk), key=f"z{g.id}")
                new_tarih = st.date_input("Tarih", datetime.strptime(g.son_tarih, "%Y-%m-%d"), key=f"t{g.id}")
                c1, c2 = st.columns(2)
                if c1.button("Güncelle", key=f"u{g.id}"):
                    yon.gorev_guncelle(g.id, {"ad": new_ad, "durum": new_durum, "zorluk": new_zorluk, "son_tarih": str(new_tarih)})
                    st.rerun()
                if c2.button("Sil", key=f"s{g.id}"):
                    yon.gorev_sil(g.id)
                    st.rerun()