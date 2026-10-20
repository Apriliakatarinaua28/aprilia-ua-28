import streamlit as st
import pandas as pd
import os
from pathlib import Path

st.set_page_config(
    page_title="Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent

FILES = {
    "clean": "data_bersih_preprocessing.csv",
    "rfm": "rfm_segmen_pelanggan.csv",
    "rules": "aturan_asosiasi_apriori.csv",
    "log": "dokumentasi_preprocessing.csv",
}

def load_csv(key):
    path = ROOT / FILES[key]
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception as e:
            st.warning(f"Tidak dapat membaca {FILES[key]}: {e}")
    return None

def money(v):
    try:
        return "Rp " + f"{float(v):,.0f}".replace(",", ".")
    except Exception:
        return str(v)

st.sidebar.title("📊 Menu Dashboard")
page = st.sidebar.radio(
    "Pilih halaman",
    ["Ringkasan", "Data Preprocessing", "Segmentasi RFM", "Aturan Apriori", "Upload & Pratinjau"]
)
st.sidebar.markdown("---")
st.sidebar.caption("UTS Business Intelligence")
st.sidebar.caption("Aprilia Katarina Ua · NPM 51220076 · Kelas B")

st.title("Dashboard Business Intelligence")
st.write("Integrasi Data Mining dan Business Intelligence pada data transaksi toko.")
st.markdown("---")

clean = load_csv("clean")
rfm = load_csv("rfm")
rules = load_csv("rules")
log = load_csv("log")

if page == "Ringkasan":
    st.subheader("Ringkasan Analisis")
    if clean is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric("Baris data bersih", f"{len(clean):,}".replace(",", "."))
        if "Transaction_ID" in clean.columns:
            c2.metric("Transaksi", f"{clean['Transaction_ID'].nunique():,}".replace(",", "."))
        else:
            c2.metric("Transaksi", "Kolom tidak tersedia")
        if "Customer_ID" in clean.columns:
            c3.metric("Pelanggan", f"{clean['Customer_ID'].nunique():,}".replace(",", "."))
        elif rfm is not None:
            c3.metric("Pelanggan", f"{len(rfm):,}".replace(",", "."))
        else:
            c3.metric("Pelanggan", "Kolom tidak tersedia")

        if "Line_Total" in clean.columns:
            total = pd.to_numeric(clean["Line_Total"], errors="coerce").sum()
            st.metric("Total nilai penjualan", money(total))

        if "Category" in clean.columns and "Line_Total" in clean.columns:
            tmp = clean.copy()
            tmp["Line_Total"] = pd.to_numeric(tmp["Line_Total"], errors="coerce")
            cat = tmp.groupby("Category", dropna=False)["Line_Total"].sum().sort_values(ascending=False)
            left, right = st.columns(2)
            with left:
                st.markdown("#### Penjualan per kategori")
                st.bar_chart(cat)
            with right:
                st.markdown("#### 10 produk dengan penjualan tertinggi")
                if "Product_Name" in tmp.columns:
                    top = tmp.groupby("Product_Name")["Line_Total"].sum().nlargest(10).sort_values()
                    st.bar_chart(top)
    else:
        st.info("File data_bersih_preprocessing.csv belum ditemukan. Unggah file melalui menu Upload & Pratinjau atau tambahkan file tersebut ke repository GitHub.")
    if rfm is not None and "Segmen" in rfm.columns:
        st.markdown("#### Jumlah pelanggan per segmen")
        st.bar_chart(rfm["Segmen"].value_counts())
    st.caption("Dashboard menampilkan data dari file CSV yang tersedia. Pastikan data yang dipublikasikan tidak memuat informasi pribadi atau sensitif.")

elif page == "Data Preprocessing":
    st.subheader("Data Hasil Preprocessing")
    if clean is not None:
        st.write(f"Jumlah baris: **{len(clean):,}** · Jumlah kolom: **{len(clean.columns)}**")
        st.dataframe(clean.head(500), use_container_width=True)
        st.download_button("Unduh data bersih (CSV)", clean.to_csv(index=False).encode("utf-8-sig"),
                           file_name="data_bersih_preprocessing.csv", mime="text/csv")
    else:
        st.warning("File data_bersih_preprocessing.csv belum tersedia.")
    if log is not None:
        st.markdown("#### Dokumentasi preprocessing")
        st.dataframe(log, use_container_width=True)
        st.download_button("Unduh dokumentasi preprocessing", log.to_csv(index=False).encode("utf-8-sig"),
                           file_name="dokumentasi_preprocessing.csv", mime="text/csv")

elif page == "Segmentasi RFM":
    st.subheader("Segmentasi Pelanggan (RFM + K-Means)")
    if rfm is not None:
        if "Segmen" in rfm.columns:
            counts = rfm["Segmen"].value_counts()
            cols = st.columns(min(4, max(1, len(counts))))
            for i, (segment, count) in enumerate(counts.items()):
                cols[i % len(cols)].metric(str(segment), f"{count:,}".replace(",", "."))
            st.bar_chart(counts)
        st.dataframe(rfm.head(500), use_container_width=True)
        st.download_button("Unduh hasil segmentasi RFM", rfm.to_csv(index=False).encode("utf-8-sig"),
                           file_name="rfm_segmen_pelanggan.csv", mime="text/csv")
    else:
        st.warning("File rfm_segmen_pelanggan.csv belum tersedia.")

elif page == "Aturan Apriori":
    st.subheader("Aturan Asosiasi Produk (Apriori)")
    if rules is not None:
        st.write(f"Aturan yang tersedia: **{len(rules):,}**")
        st.dataframe(rules.head(500), use_container_width=True)
        st.download_button("Unduh aturan Apriori", rules.to_csv(index=False).encode("utf-8-sig"),
                           file_name="aturan_asosiasi_apriori.csv", mime="text/csv")
    else:
        st.warning("File aturan_asosiasi_apriori.csv belum tersedia.")

elif page == "Upload & Pratinjau":
    st.subheader("Upload dan Pratinjau File CSV")
    uploaded = st.file_uploader("Pilih file CSV untuk dilihat", type=["csv"])
    if uploaded is not None:
        try:
            data = pd.read_csv(uploaded)
            st.success("File berhasil dibaca.")
            st.write(f"Baris: **{len(data):,}** · Kolom: **{len(data.columns)}**")
            st.dataframe(data.head(1000), use_container_width=True)
            st.download_button("Unduh kembali sebagai CSV", data.to_csv(index=False).encode("utf-8-sig"),
                               file_name=uploaded.name, mime="text/csv")
        except Exception as e:
            st.error(f"File tidak dapat dibaca sebagai CSV: {e}")
    st.info("Upload di halaman ini hanya untuk pratinjau selama sesi aplikasi. File tidak otomatis tersimpan ke GitHub atau server.")

st.markdown("---")
st.caption("Dibuat untuk tugas UTS Business Intelligence · Universitas Timor")
