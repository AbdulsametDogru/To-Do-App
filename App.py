import streamlit as st
from Backend import GorevYoneticisi
from datetime import date, datetime
from auth import Auth

st.set_page_config(
    page_title="Neon Sprint Board Pro", 
    layout="centered",
    initial_sidebar_state="auto"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
/* Modern Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

.stApp {
    /* Açık Mavi ve Pembe Gradient */
    background: linear-gradient(135deg, #e0f2fe 0%, #fce7f3 100%);
    color: #1e293b; /* Koyu lacivert yazı */
    font-family: 'Inter', sans-serif;
}

/* Kartlar - Buzlu Cam Etkisi (Glassmorphism) */
.task-card { 
    padding: 20px; 
    border-radius: 16px; 
    margin-bottom: 16px; 
    background: rgba(255, 255, 255, 0.6); 
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    transition: all 0.3s ease;
}

.task-card:hover { 
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.8);
}

/* Zorluk Renkleri - Pastel Neonlar */
.difficulty-easy { border-left: 8px solid #34d399; box-shadow: 2px 0 10px rgba(52, 211, 153, 0.2); }
.difficulty-medium { border-left: 8px solid #fbbf24; box-shadow: 2px 0 10px rgba(251, 191, 36, 0.2); }
.difficulty-hard { border-left: 8px solid #f87171; box-shadow: 2px 0 10px rgba(248, 113, 113, 0.2); }

/* Metin Renkleri */
.title { font-size: 17px; font-weight: 700; color: #0f172a; margin-bottom: 5px; }
.info { font-size: 12px; color: #475569; margin-top: 4px; }

/* Rozetler */
.badge { 
    display: inline-block; padding: 3px 10px; border-radius: 6px; 
    font-size: 9px; font-weight: 800; text-transform: uppercase;
}
.badge-easy { background:#34d399; color: white; }
.badge-medium { background:#fbbf24; color: white; }
.badge-hard { background:#f87171; color: white; }
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


# ---------------- BOARD & METRİKLER ----------------
st.title("🚀 Sprint Dashboard")

# Veri hesaplama
toplam_gorev = len(yon.gorevler)
yapilacak = len([g for g in yon.gorevler if g.durum == "Yapılacak"])
yapiliyor = len([g for g in yon.gorevler if g.durum == "Yapılıyor"])
tamamlanan = len([g for g in yon.gorevler if g.durum == "Tamamlandı"])

# Metrikler ve İlerleme tek satırda
c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
c1.metric("Yapılacak", yapilacak)
c2.metric("Yapılıyor", yapiliyor)
c3.metric("Tamamlanan", tamamlanan)

ilerleme = tamamlanan / toplam_gorev if toplam_gorev > 0 else 0
c4.write(f"**İlerleme: %{int(ilerleme * 100)}**")
c4.progress(ilerleme)

st.divider()

# Board Sütunları
cols = st.columns(3)
durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]

for i, col in enumerate(cols):
    with col:
        st.subheader(durumlar[i])
        
        # Sadece ilgili durumdaki görevleri filtrele
        for g in [x for x in yon.gorevler if x.durum == durumlar[i]]:
            kalan = kalan_gun(g.son_tarih)
            diff = zorluk_class(g.zorluk)
            
            # Kart
            st.markdown(f"""
            <div class="task-card difficulty-{diff}">
                <div class="title">{g.ad}</div>
                <div class="info">📅 {g.son_tarih}</div>
                <div class="info">⏳ {kalan if kalan >= 0 else "Gecikti"} gün</div>
                <div style="margin-top:6px"><span class="badge badge-{diff}">{g.zorluk}</span></div>
            </div>""", unsafe_allow_html=True)
            
            # İşlemler
            with st.expander("Düzenle"):
                new_ad = st.text_input("Ad", g.ad, key=f"a_{g.id}")
                new_durum = st.selectbox("Durum", durumlar, index=durumlar.index(g.durum), key=f"d_{g.id}")
                new_zorluk = st.selectbox("Zorluk", ["Kolay","Orta","Zor"], index=["Kolay","Orta","Zor"].index(g.zorluk), key=f"z_{g.id}")
                new_tarih = st.date_input("Tarih", datetime.strptime(g.son_tarih, "%Y-%m-%d"), key=f"t_{g.id}")
                
                c1, c2 = st.columns(2)
                if c1.button("Güncelle", key=f"u_{g.id}"):
                    yon.gorev_guncelle(g.id, {"ad": new_ad, "durum": new_durum, "zorluk": new_zorluk, "son_tarih": str(new_tarih)})
                    st.rerun()
                if c2.button("Sil", key=f"s_{g.id}"):
                    yon.gorev_sil(g.id)
                    st.rerun()