import streamlit as st
from Backend import GorevYoneticisi
from datetime import date, datetime
from auth import Auth

st.set_page_config(page_title="Neon Sprint Board Pro", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 70% 30%, #581c87, #0f172a),
                radial-gradient(circle at 20% 80%, #991b1b, #0f172a);
    color: white;
}

/* Card */
.task-card {
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    background: rgba(15, 23, 42, 0.85);
    transition: 0.2s;
}

.task-card:hover {
    transform: scale(1.01);
}

/* Difficulty */
.difficulty-easy {
    border-left: 5px solid #10b981;
    box-shadow: 0 0 10px rgba(16,185,129,0.25);
}

.difficulty-medium {
    border-left: 5px solid #f59e0b;
    box-shadow: 0 0 10px rgba(245,158,11,0.25);
}

.difficulty-hard {
    border-left: 5px solid #ef4444;
    box-shadow: 0 0 10px rgba(239,68,68,0.25);
}

/* Badge */
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
    color: white;
}

.badge-easy { background:#10b981; }
.badge-medium { background:#f59e0b; }
.badge-hard { background:#ef4444; }

.title {
    font-size: 18px;
    font-weight: 600;
}

.info {
    font-size: 13px;
    color: #cbd5e1;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN ----------------
if "kullanici_adi" not in st.session_state:

    st.markdown("""
        <h1 style='text-align:center;color:#8b5cf6;margin-top:80px;'>
        ⚡ Cyber Sprint Login
        </h1>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        tab1, tab2 = st.tabs(["Giriş", "Kayıt"])

        with tab1:
            user = st.text_input("Kullanıcı")
            pw = st.text_input("Şifre", type="password")

            if st.button("Giriş"):
                try:
                    if Auth.giris(user, pw):
                        st.session_state.kullanici_adi = user
                        st.rerun()
                    else:
                        st.warning("Kullanıcı adı veya şifre yanlış")
                except:
                    st.warning("Giriş yapılamadı")

        with tab2:
            u = st.text_input("Yeni kullanıcı")
            p = st.text_input("Şifre", type="password")

            if st.button("Kayıt"):
                try:
                    if Auth.kayit(u, p):
                        st.success("Kayıt başarılı")
                    else:
                        st.warning("Bu kullanıcı zaten var")
                except:
                    st.warning("Kayıt yapılamadı")

    st.stop()


# ---------------- BACKEND ----------------
yon = GorevYoneticisi(st.session_state.kullanici_adi)


def kalan_gun(t):
    try:
        return (datetime.strptime(t, "%Y-%m-%d").date() - date.today()).days
    except:
        return 0


def zorluk_class(z):
    return {
        "Kolay": "easy",
        "Orta": "medium",
        "Zor": "hard"
    }.get(z, "medium")


def kalan_yazi(kalan):
    if kalan < 0:
        return "Gecikti"
    if kalan == 0:
        return "Bugün teslim"
    return f"{kalan} gün kaldı"


def kalan_color(kalan):
    if kalan < 0:
        return "#ef4444"
    if kalan == 0:
        return "#f59e0b"
    return "#10b981"


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.kullanici_adi}")

    with st.form("add"):
        ad = st.text_input("Görev")
        durum = st.selectbox("Durum", ["Yapılacak", "Yapılıyor", "Tamamlandı"])
        zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor"])
        tarih = st.date_input("Tarih", min_value=date.today())

        if st.form_submit_button("Ekle"):
            yon.gorev_ekle(ad, durum, zorluk, str(tarih))
            st.rerun()

    if st.button("Çıkış"):
        del st.session_state.kullanici_adi
        st.rerun()


# ---------------- BOARD ----------------
st.title("SPRINT CONTROL CENTER")

cols = st.columns(3)
durumlar = ["Yapılacak", "Yapılıyor", "Tamamlandı"]

for i, col in enumerate(cols):

    with col:
        st.subheader(durumlar[i])

        gorevler = [g for g in yon.gorevler if g.durum == durumlar[i]]

        for g in gorevler:

            kalan = kalan_gun(g.son_tarih)
            diff = zorluk_class(g.zorluk)

            st.markdown(f"""
            <div class="task-card difficulty-{diff}">

                <div class="title">{g.ad}</div>

                <div class="info">
                    📅 {g.son_tarih}
                </div>

                <div class="info" style="color:{kalan_color(kalan)}; font-weight:500">
                    ⏳ {kalan_yazi(kalan)}
                </div>

                <div style="margin-top:6px">
                    <span class="badge badge-{diff}">
                        {g.zorluk}
                    </span>
                </div>

            </div>
            """, unsafe_allow_html=True)

            # -------- ACTIONS --------
            with st.expander("İşlemler"):

                new_ad = st.text_input("Ad", g.ad, key=f"a{g.id}")
                new_durum = st.selectbox("Durum", durumlar, index=durumlar.index(g.durum), key=f"d{g.id}")
                new_zorluk = st.selectbox("Zorluk", ["Kolay","Orta","Zor"], index=["Kolay","Orta","Zor"].index(g.zorluk), key=f"z{g.id}")
                new_tarih = st.date_input("Tarih", datetime.strptime(g.son_tarih, "%Y-%m-%d"), key=f"t{g.id}")

                c1, c2 = st.columns(2)

                with c1:
                    if st.button("Güncelle", key=f"u{g.id}"):
                        yon.gorev_guncelle(g.id, {
                            "ad": new_ad,
                            "durum": new_durum,
                            "zorluk": new_zorluk,
                            "son_tarih": str(new_tarih)
                        })
                        st.rerun()

                with c2:
                    if st.button("Sil", key=f"s{g.id}"):
                        yon.gorev_sil(g.id)
                        st.rerun()