import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 📂 Load Data
file_path = "./owid-monkeypox-data.csv"  # Replace with your actual path
df = pd.read_csv(file_path)

# Convert date column to datetime format
df["date"] = pd.to_datetime(df["date"])

# 🌍 Page Title
st.title("Monkeypox Data Visualization Dashboard")

# 🏳️ Select a Country
locations = df["location"].unique()
selected_country = st.selectbox("🏳️ Select a Country:", locations)

# 📅 **Date Range Selector**
min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.date_input("📆 Select Date Range:", [min_date, max_date], min_value=min_date, max_value=max_date)

# 📊 **New Cases Threshold Filter**
min_new_cases = int(df["new_cases"].min())
max_new_cases = int(df["new_cases"].max())
new_cases_threshold = st.slider("📈 Minimum New Cases:", min_value=min_new_cases, max_value=max_new_cases, value=min_new_cases)

# 📊 Filter Data for the Selected Country and Apply Filters
filtered_df = df[(df["location"] == selected_country) & 
                 (df["date"] >= pd.to_datetime(date_range[0])) & 
                 (df["date"] <= pd.to_datetime(date_range[1])) & 
                 (df["new_cases"] >= new_cases_threshold)]

if filtered_df.empty:
    st.warning(f"No data available for {selected_country} within the selected range. Try adjusting filters.")
else:
    # 📌 Show Key Metrics
    total_cases = filtered_df["total_cases"].max()
    total_deaths = filtered_df["total_deaths"].max()
    new_cases = filtered_df["new_cases"].sum()

    st.metric("Total Cases", f"{total_cases:,}")
    st.metric("Total Deaths", f"{total_deaths:,}")
    st.metric("New Cases in Selected Period", f"{new_cases:,}")

    # 📊 Bar Chart: Total Cases, Deaths, and Recoveries
    st.subheader("📊 Total Cases Breakdown")
    fig_bar = px.bar(
        x=["Total Cases", "Total Deaths"],
        y=[total_cases, total_deaths],
        labels={"x": "Category", "y": "Count"},
        color=["Total Cases", "Total Deaths"],
        title=f"Monkeypox Cases Breakdown in {selected_country}",
        template="plotly_dark",
    )
    st.plotly_chart(fig_bar)

    # 📈 Scatter Plot: New Cases vs. Total Cases
    st.subheader("📍 New Cases vs. Total Cases")
    fig_scatter = px.scatter(
        filtered_df,
        x="total_cases",
        y="new_cases",
        size="new_cases",
        color="new_cases",
        hover_name="date",
        title="New Cases vs. Total Cases",
        template="plotly_dark",
    )
    st.plotly_chart(fig_scatter)

    # 📉 Carpet Plot: Total Cases Over Time
    st.subheader("📉 Carpet Scatter Plot for Monkeypox Cases")
    filtered_df["date_numeric"] = np.arange(len(filtered_df))  # Convert dates to numeric index

    carpet = go.Carpet(
        a=filtered_df["date_numeric"],
        b=filtered_df["total_cases"],
        carpet="carpet1",
        aaxis=dict(title="Days Since First Case", color="gray"),
        baxis=dict(title="Total Cases", color="gray"),
    )

    scatter = go.Scatter(
        x=filtered_df["date_numeric"],
        y=filtered_df["total_cases"],
        mode='markers',
        marker=dict(size=10, color=filtered_df["new_cases"], colorscale="Viridis", showscale=True),
        name="Monkeypox Cases"
    )

    fig_carpet = go.Figure(data=[carpet, scatter])
    fig_carpet.update_layout(
        title=f"Carpet Scatter Plot for {selected_country}",
        xaxis_title="Days Since First Case",
        yaxis_title="Total Cases",
        template="plotly_dark"
    )
    st.plotly_chart(fig_carpet)

    # 🌍 Map of Monkeypox Cases (Bubble Map)
    st.subheader("🗺️ Monkeypox Cases Around the World")
    fig_map = px.scatter_geo(
        df,
        locations="location",
        locationmode="country names",
        size="total_cases",
        color="new_cases",
        hover_name="location",
        title="Global Monkeypox Cases",
        template="plotly_dark",
        projection="natural earth",
    )
    st.plotly_chart(fig_map)
