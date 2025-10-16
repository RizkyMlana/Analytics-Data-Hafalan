import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Hafalan Mahasiswa", layout="wide")
st.title("Dashboard Hafalan Mahasiswa")

# Load Data
@st.cache_data
def load_data():
    return pd.read_parquet("dataset/data.parquet")

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

# Filter Data
if fakultas_selected == "Semua":
    filtered_data = df
elif prodi_selected == "Semua":
    filtered_data = fac_data
else:
    filtered_data = fac_data[fac_data["Program Studi"] == prodi_selected]

# Statistik
total_mahasiswa = len(filtered_data)
total_Ikhwan = len(filtered_data[filtered_data["Keterangan"] == "Ikhwan"])
total_Akhwat = len(filtered_data[filtered_data["Keterangan"] == "Akhwat"])

col1, col2, col3 = st.columns(3)
col1.metric("Total Mahasiswa", total_mahasiswa)
col2.metric("Ikhwan", total_Ikhwan)
col3.metric("Akhwat", total_Akhwat)

# Pie Chart Gender
st.markdown("### Distribusi Gender")
if fakultas_selected == "Semua":
    data_gender = df
    title_gender = "Distribusi Gender Seluruh Universitas"
    color_seq = px.colors.qualitative.Pastel
elif prodi_selected == "Semua":
    data_gender = fac_data
    title_gender = f"Distribusi Gender {fakultas_selected}"
    color_seq = px.colors.qualitative.Set3
else:
    data_gender = filtered_data
    title_gender = f"Distribusi Gender {prodi_selected}"
    color_seq = px.colors.qualitative.Vivid

gender_counts = data_gender["Keterangan"].value_counts().reset_index()
gender_counts.columns = ["Keterangan", "Jumlah"]

fig_gender = px.pie(
    gender_counts, values="Jumlah", names="Keterangan",
    title=title_gender,
    color_discrete_sequence=color_seq
)
fig_gender.update_traces(textinfo='label+percent+value')
st.plotly_chart(fig_gender, use_container_width=True)

# Distribusi Juz 
st.markdown("### Distribusi Jumlah Mahasiswa per Jumlah Juz")

def plot_juz_distribution(data, title,color_scale=None):
    df_count = data.groupby("Hafalan").size().reset_index(name="Jumlah Mahasiswa")
    if color_scale is None:
        color_scale = ["#004280",  "#3093EC",  "#E4F5FF"]
    fig = px.bar(
        df_count.sort_values("Hafalan"),
        x="Hafalan", y="Jumlah Mahasiswa",
        text_auto=True,
        color="Hafalan",
        title=title,
        color_continuous_scale=color_scale
    )
    fig.update_layout(
        height=400,
        bargap=0.4 if len(df_count) <= 5 else 0.25,
        xaxis_title="Jumlah Juz",
        yaxis_title="Jumlah Mahasiswa",
        margin=dict(l=30, r=30, t=60, b=60)
    )
    st.plotly_chart(fig, use_container_width=True)

if fakultas_selected == "Semua":
    plot_juz_distribution(df, "Distribusi Jumlah Mahasiswa per Jumlah Juz (Universitas)")
elif prodi_selected == "Semua":
    plot_juz_distribution(fac_data, f"Distribusi Jumlah Mahasiswa per Jumlah Juz ({fakultas_selected})")
else:
    plot_juz_distribution(filtered_data, f"Distribusi Jumlah Mahasiswa per Jumlah Juz ({prodi_selected})", color_scale=["#E58606","#5D69B1"])

# Tabel Mahasiswa
st.markdown("### Data Mahasiswa")
st.dataframe(
    filtered_data[["Nama", "Program Studi", "Keterangan", "Hafalan"]],
    use_container_width=True,
    hide_index=True
)
