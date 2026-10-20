import streamlit as st
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent
PHOTO = BASE / "foto_aprilia.png"

st.set_page_config(
    page_title="UTS Business Intelligence | Universitas Timor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Data helpers ---
def read_csv(filename):
    path = BASE / filename
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception as exc:
            st.warning(f"File {filename} tidak dapat dibaca: {exc}")
    return None

def fmt_int(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except Exception:
        return str(value)

def photo_html():
    if PHOTO.exists():
        st.image(str(PHOTO), use_container_width=True)

# --- Theme ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap');
:root { --navy:#081936; --navy2:#10284d; --orange:#f7931e; --cream:#f6f8fc; }
.stApp { background: #f4f7fb; color:#17233c; font-family:'DM Sans',sans-serif; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#081936,#10284d); }
[data-testid="stSidebar"] * { color:#f5f7ff !important; }
.block-container { padding-top:1.4rem; padding-bottom:2.2rem; max-width:1450px; }
.hero {
  background:linear-gradient(115deg,#07152f 0%,#102b52 65%,#14516a 100%);
  border-radius:24px; padding:36px 38px; color:#fff; position:relative; overflow:hidden;
  box-shadow:0 18px 45px rgba(8,25,54,.16); border:1px solid rgba(255,255,255,.12);
}
.hero:after {content:""; position:absolute; width:300px;height:300px;border:1px solid rgba(255,255,255,.08);
border-radius:50%; right:-70px; top:-90px; box-shadow:0 0 0 35px rgba(255,255,255,.025),0 0 0 70px rgba(255,255,255,.02);}
.eyebrow {letter-spacing:2px;text-transform:uppercase;color:#c5d6ef;font-size:12px;font-weight:700;}
.hero-title {font-family:'Playfair Display',serif;font-size:clamp(36px,5vw,64px);font-weight:800;line-height:1.02;margin:12px 0 16px;}
.orange {color:#ff9a24;}
.hero-desc {font-size:16px;line-height:1.7;color:#d9e5f6;max-width:650px;}
.profile-card {background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:16px 18px;margin-top:20px;max-width:560px;}
.profile-name {font-family:'Playfair Display',serif;font-size:23px;font-weight:700;color:#fff;}
.profile-meta {color:#e5edf8;font-size:14px;line-height:1.7;}
.login-card {background:white;border:1px solid #e3e9f3;border-radius:22px;padding:28px;box-shadow:0 18px 45px rgba(8,25,54,.1);}
.section-title {font-family:'Playfair Display',serif;color:#0b1d3b;font-size:27px;font-weight:700;}
.small-muted {color:#64748b;font-size:13px;}
.metric-card {background:#fff;border:1px solid #e4eaf3;border-radius:16px;padding:18px 20px;box-shadow:0 5px 16px rgba(15,35,70,.04);}
.metric-label {color:#687891;font-size:13px;font-weight:600;}
.metric-value {color:#10284d;font-size:28px;font-weight:800;margin-top:6px;}
div.stButton > button {border-radius:12px;border:0;background:linear-gradient(90deg,#ffad42,#f58a16);color:#10203d;font-weight:700;padding:.65rem 1.1rem;}
div.stButton > button:hover {background:linear-gradient(90deg,#ffc16e,#ff9b25);color:#07152f;border:0;}
div[data-testid="stForm"] {border:0;padding:0;}
div[data-testid="stDataFrame"] {border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;}
hr {border-color:#e2e8f0;}
@media (max-width: 700px) { .hero {padding:24px;} .profile-name{font-size:20px;} }
</style>
""", unsafe_allow_html=True)

# --- State ---
if "page" not in st.session_state:
    st.session_state.page = "cover"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def go(page):
    st.session_state.page = page
    st.rerun()

# --- Cover ---
if st.session_state.page == "cover" and not st.session_state.authenticated:
    left, right = st.columns([1.25, .8], gap="large")
    with left:
        st.markdown("""
        <div class="hero">
          <div class="eyebrow">Universitas Timor · Teknologi Informasi · TIF46212</div>
          <div class="hero-title">UTS<br><span class="orange">Business<br>Intelligence</span></div>
          <div class="hero-desc">Integrasi Data Mining dan Business Intelligence pada Data Transaksi Toko: EDA, Preprocessing, Apriori, K-Means, dan Dashboard.</div>
          <div class="profile-card">
            <div class="profile-name">Aprilia Katarina Ua</div>
            <div class="profile-meta">NPM 51220076<br>Kelas B · Semester IX<br>Dosen: Krisantus Jumarto Tey Seran, S.T., M.T.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Masuk ke sistem  →", key="cover_enter", use_container_width=False):
            go("login")
        st.caption("Dashboard akademik · Business Intelligence")
    with right:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if PHOTO.exists():
            st.image(str(PHOTO), use_container_width=True)
        else:
            st.info("Foto belum ditemukan. Letakkan foto_aprilia.png di folder aplikasi.")
        st.markdown("""
        <div style="background:white;border:1px solid #e4eaf3;border-radius:16px;padding:16px;margin-top:10px;">
          <div style="font-weight:700;color:#10284d;font-size:17px;">Analisis data lebih mudah.</div>
          <div style="color:#64748b;font-size:13px;margin-top:5px;">Data terstruktur, visualisasi informatif, dan hasil analisis siap ditinjau.</div>
        </div>
        """, unsafe_allow_html=True)

# --- Login ---
elif st.session_state.page == "login" and not st.session_state.authenticated:
    _, center, _ = st.columns([.7, 1.5, .7])
    with center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        if PHOTO.exists():
            st.image(str(PHOTO), width=145)
        st.markdown('<div class="section-title">Selamat datang kembali</div>', unsafe_allow_html=True)
        st.markdown('<div class="small-muted">Masuk untuk mengakses sistem Business Intelligence.</div>', unsafe_allow_html=True)
        st.write("")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            remember = st.checkbox("Ingat saya di sesi ini", value=True)
            submitted = st.form_submit_button("Masuk ke dashboard  →", use_container_width=True)
        if submitted:
            if username == "Aprilia" and password == "Aprilia28":
                st.session_state.authenticated = True
                st.session_state.username = username
                go("dashboard")
            else:
                st.error("Username atau password salah. Silakan periksa kembali.")
        st.markdown('<div class="small-muted" style="margin-top:14px;">Universitas Timor · UTS Business Intelligence</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("← Kembali ke cover"):
            go("cover")

# --- Dashboard ---
else:
    with st.sidebar:
        st.markdown("## 📊 UTS BI")
        st.caption("Business Intelligence")
        st.markdown("---")
        page = st.radio(
            "NAVIGASI",
            ["Dashboard", "Data Preprocessing", "Segmentasi Pelanggan", "Aturan Asosiasi Apriori", "Upload Data", "Tentang Sistem"],
            label_visibility="visible",
        )
        st.markdown("---")
        st.caption("Login sebagai")
        st.markdown("**Aprilia Katarina Ua**")
        st.caption("NPM 51220076 · Kelas B")
        if st.button("Keluar dari sistem", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.page = "cover"
            st.rerun()

    clean = read_csv("data_bersih_preprocessing.csv")
    rfm = read_csv("rfm_segmen_pelanggan.csv")
    rules = read_csv("aturan_asosiasi_apriori.csv")
    docs = read_csv("dokumentasi_preprocessing.csv")

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">
      <div><div class="eyebrow" style="color:#f08c18;">UNIVERSITAS TIMOR · BUSINESS INTELLIGENCE</div>
      <div class="section-title">Halo, Aprilia 👋</div>
      <div class="small-muted">Ringkasan analisis dan pengolahan data transaksi toko.</div></div>
      <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:10px 14px;color:#50617b;font-size:13px;">Sistem Analitik · UTS</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    if page == "Dashboard":
        transactions = clean["Transaction_ID"].nunique() if clean is not None and "Transaction_ID" in clean.columns else (len(clean) if clean is not None else 0)
        customers = clean["Customer_ID"].nunique() if clean is not None and "Customer_ID" in clean.columns else (len(rfm) if rfm is not None else 0)
        sales = pd.to_numeric(clean["Line_Total"], errors="coerce").sum() if clean is not None and "Line_Total" in clean.columns else None
        products = clean["Product_Name"].nunique() if clean is not None and "Product_Name" in clean.columns else 0
        m1,m2,m3,m4 = st.columns(4)
        metrics = [(m1,"Baris Data",fmt_int(len(clean) if clean is not None else 0)),
                   (m2,"Transaksi",fmt_int(transactions)),(m3,"Pelanggan",fmt_int(customers)),
                   (m4,"Produk Unik",fmt_int(products))]
        for col,label,value in metrics:
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)
        st.write("")
        if sales is not None:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Total Nilai Penjualan</div><div class="metric-value">Rp {sales:,.0f}</div></div>'.replace(",", "."), unsafe_allow_html=True)
        left,right = st.columns(2, gap="large")
        with left:
            st.markdown("#### Penjualan berdasarkan kategori")
            if clean is not None and {"Category","Line_Total"}.issubset(clean.columns):
                temp = clean.copy()
                temp["Line_Total"] = pd.to_numeric(temp["Line_Total"], errors="coerce")
                st.bar_chart(temp.groupby("Category")["Line_Total"].sum().sort_values(ascending=False))
            else:
                st.info("Grafik kategori akan tampil jika kolom Category dan Line_Total tersedia.")
        with right:
            st.markdown("#### Distribusi segmen pelanggan")
            if rfm is not None and "Segmen" in rfm.columns:
                st.bar_chart(rfm["Segmen"].value_counts())
            else:
                st.info("Data segmen belum tersedia atau kolom Segmen tidak ditemukan.")
        st.markdown("#### Pratinjau data")
        if clean is not None:
            st.dataframe(clean.head(10), use_container_width=True)
            st.download_button("Unduh data bersih CSV", clean.to_csv(index=False).encode("utf-8-sig"),
                               "data_bersih_preprocessing.csv", "text/csv")
        else:
            st.warning("File data_bersih_preprocessing.csv belum ditemukan.")

    elif page == "Data Preprocessing":
        st.markdown("### Data Preprocessing")
        st.write("Lihat hasil pembersihan, transformasi, dan dokumentasi data.")
        if clean is not None:
            st.success(f"Data bersih tersedia: {fmt_int(len(clean))} baris dan {len(clean.columns)} kolom.")
            q = st.text_input("Cari kata pada data (opsional)")
            view = clean
            if q:
                mask = view.astype(str).apply(lambda c: c.str.contains(q, case=False, na=False)).any(axis=1)
                view = view[mask]
            st.dataframe(view, use_container_width=True, height=420)
            st.download_button("⬇ Unduh data bersih", clean.to_csv(index=False).encode("utf-8-sig"),
                               "data_bersih_preprocessing.csv", "text/csv")
        else:
            st.warning("File data bersih belum tersedia.")
        if docs is not None:
            st.markdown("#### Dokumentasi preprocessing")
            st.dataframe(docs, use_container_width=True)
            st.download_button("Unduh dokumentasi", docs.to_csv(index=False).encode("utf-8-sig"),
                               "dokumentasi_preprocessing.csv", "text/csv")

    elif page == "Segmentasi Pelanggan":
        st.markdown("### Segmentasi Pelanggan · RFM / K-Means")
        if rfm is not None:
            if "Segmen" in rfm.columns:
                counts = rfm["Segmen"].value_counts()
                cols = st.columns(max(1, min(4, len(counts))))
                for i,(segment,count) in enumerate(counts.items()):
                    cols[i % len(cols)].metric(str(segment), fmt_int(count) + " pelanggan")
                st.bar_chart(counts)
            st.dataframe(rfm, use_container_width=True, height=420)
            st.download_button("⬇ Unduh hasil segmentasi", rfm.to_csv(index=False).encode("utf-8-sig"),
                               "rfm_segmen_pelanggan.csv", "text/csv")
        else:
            st.warning("File rfm_segmen_pelanggan.csv belum ditemukan.")

    elif page == "Aturan Asosiasi Apriori":
        st.markdown("### Aturan Asosiasi Apriori")
        st.write("Temukan hubungan produk berdasarkan hasil aturan asosiasi yang sudah dihitung.")
        if rules is not None:
            st.metric("Jumlah aturan tersedia", fmt_int(len(rules)))
            st.dataframe(rules, use_container_width=True, height=420)
            st.download_button("⬇ Unduh aturan Apriori", rules.to_csv(index=False).encode("utf-8-sig"),
                               "aturan_asosiasi_apriori.csv", "text/csv")
        else:
            st.warning("File aturan_asosiasi_apriori.csv belum ditemukan.")

    elif page == "Upload Data":
        st.markdown("### Upload & Pratinjau Data")
        uploaded = st.file_uploader("Pilih file CSV", type=["csv"])
        if uploaded is not None:
            try:
                frame = pd.read_csv(uploaded)
                st.success("File berhasil dibaca.")
                a,b = st.columns(2)
                a.metric("Jumlah baris", fmt_int(len(frame)))
                b.metric("Jumlah kolom", fmt_int(len(frame.columns)))
                st.dataframe(frame.head(1000), use_container_width=True)
                st.download_button("Unduh kembali sebagai CSV", frame.to_csv(index=False).encode("utf-8-sig"),
                                   uploaded.name, "text/csv")
            except Exception as exc:
                st.error(f"File tidak dapat dibaca: {exc}")
        st.info("File upload ditampilkan untuk sesi ini dan tidak otomatis disimpan ke server atau repository GitHub.")

    elif page == "Tentang Sistem":
        st.markdown("### Tentang Sistem")
        st.write("""
        Dashboard ini merupakan antarmuka UTS Business Intelligence untuk menampilkan hasil
        preprocessing data, segmentasi pelanggan, dan aturan asosiasi Apriori.
        """)
        st.markdown("""
        **Identitas**
        - Nama: Aprilia Katarina Ua
        - NPM: 51220076
        - Kelas: B · Semester IX
        - Program: Teknologi Informasi
        - Universitas: Universitas Timor
        """)
        st.info("Akun demo untuk tugas: username `Aprilia` dan password `Aprilia28`.")
