import streamlit as st
import pandas as pd
import plotly.express as px

# 📂 Load Data
file_path = "./worldometer_coronavirus_summary_data.csv"
df = pd.read_csv(file_path)

# 🌍 Page Title
st.title("🌍 COVID-19 Worldometer Dashboard")

# 🔍 Filter by Continent
continents = df["continent"].dropna().unique()
selected_continent = st.selectbox("🌎 Select Continent:", ["All"] + list(continents))

# Filter the data if a continent is selected
if selected_continent != "All":
    df = df[df["continent"] == selected_continent]

# 🏳️ Select a Country
countries = df["country"].unique()
selected_country = st.selectbox("🏳️ Select a Country:", countries)

# 📊 Filter Data for the Selected Country
country_data = df[df["country"] == selected_country].iloc[0]

# 📈 Show Key Metrics
st.metric("Total Confirmed Cases", f"{country_data['total_confirmed']:,}")
st.metric("Total Deaths", f"{country_data['total_deaths']:,}")
st.metric("Total Recovered", f"{country_data['total_recovered']:,}")
st.metric("Active Cases", f"{country_data['active_cases']:,}")
st.metric("Serious/Critical Cases", f"{country_data['serious_or_critical']:,}")

# 📊 Bar Chart: Total Cases, Deaths, and Recoveries
st.subheader("📊 Total Cases Breakdown")
fig_bar = px.bar(
    x=["Total Confirmed", "Total Deaths", "Total Recovered"],
    y=[country_data["total_confirmed"], country_data["total_deaths"], country_data["total_recovered"]],
    labels={"x": "Category", "y": "Count"},
    color=["Total Confirmed", "Total Deaths", "Total Recovered"],
    title=f"COVID-19 Cases Breakdown in {selected_country}",
    template="plotly_dark",
)
st.plotly_chart(fig_bar)

# 📈 Scatter Plot: Total Tests vs. Total Cases
st.subheader("🧪 Testing vs. Cases")
fig_scatter = px.scatter(
    df,
    x="total_tests",
    y="total_confirmed",
    size="population",
    color="continent",
    hover_name="country",
    log_x=True,
    log_y=True,
    title="Total Tests vs. Total Confirmed Cases (Log Scale)",
    template="plotly_dark",
)
st.plotly_chart(fig_scatter)

# 🌍 Map of COVID-19 Cases (Bubble Map)
st.subheader("🗺️ COVID-19 Cases Around the World")
fig_map = px.scatter_geo(
    df,
    locations="country",
    locationmode="country names",
    size="total_confirmed",
    color="continent",
    hover_name="country",
    title="Global COVID-19 Cases",
    template="plotly_dark",
    projection="natural earth",
)
st.plotly_chart(fig_map)
