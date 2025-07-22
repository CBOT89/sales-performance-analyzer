
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Sales Performance Analysis App")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Rename columns for consistency
    df.rename(columns={
        "FY 25 Quota": "FY25 Quota",
        "FY 25 Credit": "FY25 Credit",
        "FY25 Attainment  ": "FY25 Attainment",
        "FY24 Attainment2": "FY24 Attainment",
        "FY23 Attainment": "FY23 Attainment"
    }, inplace=True)

    # Convert numeric columns
    for col in ["FY25 Quota", "FY25 Credit", "FY25 Attainment", "Tenure (Years)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    st.subheader("1️⃣ Quota vs Attainment by Region")
    quota_attainment = df.groupby("BU")[["FY25 Quota", "FY25 Credit"]].sum().sort_values("FY25 Quota", ascending=False)
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    quota_attainment.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Amount")
    ax1.set_title("FY25 Quota vs Credit by Business Unit")
    st.pyplot(fig1)

    st.subheader("2️⃣ Performance per Tenure by Region")
    df["Performance per Tenure"] = df["FY25 Attainment"] / df["Tenure (Years)"]
    perf_by_bu = df.groupby("BU")["Performance per Tenure"].mean().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    perf_by_bu.plot(kind="bar", ax=ax2, color="green")
    ax2.set_ylabel("Avg Attainment / Tenure")
    ax2.set_title("FY25 Performance per Tenure by Business Unit")
    st.pyplot(fig2)

    st.subheader("3️⃣ Top Managers for Hiring")
    manager_perf = df.groupby(["BU", "Manager"]).agg({
        "FY25 Attainment": "mean",
        "Tenure (Years)": "mean",
        "Name": "count"
    }).rename(columns={"Name": "Team Size"}).reset_index()
    manager_perf["Performance per Tenure"] = manager_perf["FY25 Attainment"] / manager_perf["Tenure (Years)"]
    top_managers = manager_perf.sort_values("Performance per Tenure", ascending=False).head(10)
    st.dataframe(top_managers)

    csv = top_managers.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Top Managers CSV", csv, "top_managers.csv", "text/csv")

    st.subheader("4️⃣ Quota Achievement % by Region")
    quota_attainment["Quota Achievement %"] = (quota_attainment["FY25 Credit"] / quota_attainment["FY25 Quota"]) * 100
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    quota_attainment["Quota Achievement %"].sort_values(ascending=False).plot(kind="bar", ax=ax3, color="orange")
    ax3.set_ylabel("Percentage")
    ax3.set_title("FY25 Quota Achievement % by Business Unit")
    st.pyplot(fig3)
else:
    st.info("Please upload an Excel file to begin analysis.")
