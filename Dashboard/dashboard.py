import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt

st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")
sns.set(style='dark')

# --- MEMUAT DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

all_df = load_data()

# --- FILTER INTERAKTIF DI SIDEBAR ---
min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    st.title("🛒 E-Commerce Analyzer")
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Menambahkan Filter Waktu (Time-bound)
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu Transaksi',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# --- MEMFILTER DATA BERDASARKAN INPUT USER ---
main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                 (all_df["order_purchase_timestamp"].dt.date <= end_date)]

st.title("E-Commerce Public Dataset Dashboard 🛍️")
st.write(f"Menampilkan data dari **{start_date}** hingga **{end_date}**")

# =========================================================
# PERTANYAAN 1: REVENUE KATEGORI PRODUK
# =========================================================
st.header("1. Performa Kategori Produk (Revenue)")

category_revenue = main_df.groupby("product_category_name_english")["price"].sum().reset_index()
category_revenue.rename(columns={"price": "total_revenue"}, inplace=True)
category_revenue = category_revenue.sort_values(by="total_revenue", ascending=False)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="total_revenue", y="product_category_name_english", data=category_revenue.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Pendapatan", fontsize=12)
ax[0].set_title("Kategori Produk dengan Revenue Tertinggi", loc="center", fontsize=15)

bottom_categories = category_revenue.tail(5).sort_values(by="total_revenue", ascending=True)
sns.barplot(x="total_revenue", y="product_category_name_english", data=bottom_categories, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Pendapatan", fontsize=12)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Kategori Produk dengan Revenue Terendah", loc="center", fontsize=15)

st.pyplot(fig)

# =========================================================
# PERTANYAAN 2: RFM ANALYSIS
# =========================================================
st.header("2. Segmentasi Pelanggan (RFM Analysis)")

recent_date = main_df["order_purchase_timestamp"].max() + dt.timedelta(days=1)
rfm_df = main_df.groupby("customer_id").agg({
    "order_purchase_timestamp": lambda x: (recent_date - x.max()).days,
    "order_id": "nunique",
    "price": "sum"
}).reset_index()
rfm_df.columns = ["customer_id", "recency", "frequency", "monetary"]
rfm_df['short_id'] = rfm_df['customer_id'].apply(lambda x: x[:8])

fig2, ax2 = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

sns.barplot(y="recency", x="short_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax2[0])
ax2[0].set_title("Berdasarkan Recency (Hari)", loc="center", fontsize=18)

sns.barplot(y="frequency", x="short_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax2[1])
ax2[1].set_title("Berdasarkan Frequency", loc="center", fontsize=18)

sns.barplot(y="monetary", x="short_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax2[2])
ax2[2].set_title("Berdasarkan Monetary", loc="center", fontsize=18)

st.pyplot(fig2)
st.caption("Copyright (c) 2026")