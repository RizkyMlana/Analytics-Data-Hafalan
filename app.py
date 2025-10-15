import pandas as pd
import streamlit as st
import plotly.express as px

data_dir = 'dataset/Kategori_Hafalan_2025_Cleaned.csv'

df = pd.read_csv(data_dir)
print(df.head())