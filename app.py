import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="B2B Dashboard", layout="wide")

# Load data
df = pd.read_csv("data.csv")

# Title
st.markdown("<h1 style='text-align: center;'>B2B Payment Collection Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- KPI CARDS ----------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

paid = df[df["Payment_Status"]=="Paid"].shape[0]
pending = df[df["Payment_Status"]=="Pending"].shape[0]
overdue = df[df["Payment_Status"]=="Overdue"].shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Invoices", len(df))
col2.metric("Paid Invoices", paid)
col3.metric("Pending Payments", pending)
col4.metric("Overdue Payments", overdue)

st.markdown("---")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

region = st.sidebar.selectbox("Region", df["Region"].unique())
status = st.sidebar.selectbox("Payment Status", df["Payment_Status"].unique())
client = st.sidebar.selectbox("Client", df["Client_Name"].unique())

filtered_df = df[
    (df["Region"] == region) &
    (df["Payment_Status"] == status) &
    (df["Client_Name"] == client)
]

# ---------------- VISUALIZATIONS ----------------

col1, col2 = st.columns(2)

# Payments by Region
with col1:
    st.subheader("Payments by Region")
    st.bar_chart(df.groupby("Region")["Invoice_Amount"].sum())

# Delay Trend
with col2:
    st.subheader("Delay Trend Analysis")
    st.line_chart(df["Delay_Days"])

col3, col4 = st.columns(2)

# Status Distribution
with col3:
    st.subheader("Invoice Status Distribution")
    st.bar_chart(df["Payment_Status"].value_counts())

# Revenue Trend
with col4:
    st.subheader("Revenue Collection Trend")
    df["Payment_Date"] = pd.to_datetime(df["Payment_Date"])
    st.line_chart(df.groupby(df["Payment_Date"].dt.month)["Invoice_Amount"].sum())

st.markdown("---")

# ---------------- FILTERED DATA ----------------
st.subheader("Filtered Data View")
st.dataframe(filtered_df)
