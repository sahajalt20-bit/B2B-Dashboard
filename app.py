import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")

st.title("Payment Collection Dashboard")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Invoices", len(df))
col2.metric("Paid Invoices", df[df["Payment_Status"]=="Paid"].shape[0])
col3.metric("Pending Payments", df[df["Payment_Status"]=="Pending"].shape[0])
col4.metric("Average Delay Days", round(df["Delay_Days"].mean(),2))

# Filters
st.sidebar.header("Filters")

region = st.sidebar.selectbox("Region", df["Region"].unique())
status = st.sidebar.selectbox("Payment Status", df["Payment_Status"].unique())
client = st.sidebar.selectbox("Client", df["Client_Name"].unique())

filtered_df = df[
    (df["Region"] == region) &
    (df["Payment_Status"] == status) &
    (df["Client_Name"] == client)
]

# Visualizations
st.subheader("Payments by Region")
st.bar_chart(df.groupby("Region")["Invoice_Amount"].sum())

st.subheader("Delay Trend Analysis")
st.line_chart(df["Delay_Days"])

st.subheader("Invoice Status Distribution")
st.bar_chart(df["Payment_Status"].value_counts())

st.subheader("Revenue Collection Trend")
df["Payment_Date"] = pd.to_datetime(df["Payment_Date"])
st.line_chart(df.groupby(df["Payment_Date"].dt.month)["Invoice_Amount"].sum())

# Filtered Data
st.subheader("Filtered Data")
st.write(filtered_df)