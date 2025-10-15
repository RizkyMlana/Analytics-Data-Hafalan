import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Hafalan Mahasiswa", layout="wide")

st.title("Dashboard Hafalan Mahasiswa")

# Load Data
@st.cache_data
def load_data():
    return pd.read_parquet("dataset/Kategori_Hafalan_2025.parquet")

df = load_data()

# Selection Box
fakultas_list = ["Semua"] + sorted(df["Fakultas"].unique())
fakultas_selected = st.selectbox("Pilih Fakultas", fakultas_list)

if fakultas_selected != "Semua":
    fac_data = df[df["Fakultas"] == fakultas_selected]
    prodi_list = ["Semua"] + sorted(fac_data["Program Studi"].unique())
    prodi_selected = st.selectbox("Pilih Prodi", prodi_list)
else:
    fac_data = df
    prodi_selected = "Semua"

# Data Filter
if fakultas_selected == "Semua":
    filtered_data = df
elif prodi_selected == "Semua":
    filtered_data = fac_data
else:
    filtered_data = fac_data[fac_data["Program Studi"] == prodi_selected]

# Ringkasan Statistik
total_mahasiswa = len(filtered_data)
total_Ikhwan = len(filtered_data[filtered_data["Keterangan"] == "Ikhwan"])
total_Akhwat = len(filtered_data[filtered_data["Keterangan"] == "Akhwat"])

col1, col2, col3 = st.columns(3)
col1.metric("Total Mahasiswa", total_mahasiswa)
col2.metric("Ikhwan", total_Ikhwan)
col3.metric("Akhwat", total_Akhwat)

# Pie Chart Gender
if fakultas_selected == "Semua":
    st.markdown("### Distribusi Gender (Universitas)")
    gender_counts = df["Keterangan"].value_counts().reset_index()
    gender_counts.columns = ["Keterangan", "Jumlah"]
    fig_gender = px.pie(
        gender_counts, values="Jumlah", names="Keterangan",
        title="Distribusi Gender Seluruh Universitas",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_gender, use_container_width=True)

elif prodi_selected == "Semua":
    st.markdown(f"### Distribusi Gender ({fakultas_selected})")
    gender_counts = fac_data["Keterangan"].value_counts().reset_index()
    gender_counts.columns = ["Keterangan", "Jumlah"]
    fig_gender = px.pie(
        gender_counts, values="Jumlah", names="Keterangan",
        title=f"Distribusi Gender {fakultas_selected}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_gender, use_container_width=True)

else:
    st.markdown(f"### Distribusi Gender ({prodi_selected})")
    gender_counts = filtered_data["Keterangan"].value_counts().reset_index()
    gender_counts.columns = ["Keterangan", "Jumlah"]
    fig_gender = px.pie(
        gender_counts, values="Jumlah", names="Keterangan",
        title=f"Distribusi Gender {prodi_selected}",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig_gender, use_container_width=True)

# Distribusi Hafalan
st.markdown("### Distribusi Kategori Hafalan")

if fakultas_selected == "Semua":
    cat_global = df["Hafalan"].value_counts().reset_index()
    cat_global.columns = ["Kategori Hafalan", "Jumlah"]
    fig_cat_global = px.bar(
        cat_global.sort_values("Kategori Hafalan"),
        x="Kategori Hafalan", y="Jumlah",
        title="Distribusi Kategori Hafalan (Universitas)",
        text_auto=True,
        color="Kategori Hafalan",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_cat_global, use_container_width=True)

elif prodi_selected == "Semua":
    cat_fak = fac_data["Hafalan"].value_counts().reset_index()
    cat_fak.columns = ["Kategori Hafalan", "Jumlah"]
    fig_cat_fak = px.bar(
        cat_fak.sort_values("Kategori Hafalan"),
        x="Kategori Hafalan", y="Jumlah",
        title=f"Distribusi Kategori Hafalan ({fakultas_selected})",
        text_auto=True,
        color="Kategori Hafalan",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_cat_fak, use_container_width=True)

else:
    cat_prodi = filtered_data.groupby(["Hafalan", "Keterangan"]).size().reset_index(name="Jumlah")
    fig_cat_prodi = px.bar(
        cat_prodi.sort_values("Hafalan"),
        x="Hafalan", y="Jumlah", color="Keterangan",
        barmode="group",
        title=f"Distribusi Kategori Hafalan ({prodi_selected}) Berdasarkan Gender",
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig_cat_prodi, use_container_width=True)

# Tabel Mahasiswa
st.markdown("### Data Mahasiswa")

st.dataframe(
    filtered_data[["Nama", "Program Studi", "Keterangan", "Hafalan"]],
    use_container_width=True,
    hide_index=True
)
