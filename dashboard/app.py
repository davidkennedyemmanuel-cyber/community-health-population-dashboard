import pandas as pd
import streamlit as st
import plotly.express as px

# ------------------- CONFIG -------------------
st.set_page_config(page_title='Community Health Dashboard', layout='wide')

# ------------------- LOAD DATA -------------------
df = pd.read_csv("data/cleaned/health_population_cleaned.csv")

# Fix: ensure 'year' is datetime
df["year"] = pd.to_datetime(df["year"], errors="coerce") 

# ------------------- DASHBOARD TITLE -------------------
st.title('Community Health & Population Dashboard')

# ------------------- FILTERS -------------------
countries = st.multiselect(
    'Select Countries',
    df["country"].unique(),
    df["country"].unique()
)

year_min = int(df["year"].dt.year.min())
year_max = int(df["year"].dt.year.max())
years = st.slider('Select Year Range', year_min, year_max, (2005, 2023))

# Filter dataframe based on selections
fdf = df[(df["country"].isin(countries)) & (df["year"].dt.year.between(years[0], years[1]))]

# ------------------- KEY METRICS -------------------
c1, c2, c3 = st.columns(3)
c1.metric('Avg Life Expectancy', round(fdf["life_expectancy"].mean(), 2))
c2.metric('Avg Mortality Rate', round(fdf["mortality_rate"].mean(), 2))
c3.metric('Avg Health Spending (% GDP)', round(fdf["health_expenditure_pct_gdp"].mean(), 2))

# ------------------- PLOTS -------------------
# Life Expectancy over Time
fig1 = px.line(
    fdf,
    x='year',
    y='life_expectancy',
    color='country',
    title='Life Expectancy Trends by Country'
)
st.plotly_chart(fig1, use_container_width=True)

# Health Expenditure vs Mortality
fig2 = px.scatter(
    fdf,
    x='health_expenditure_pct_gdp',
    y='mortality_rate',
    color='country',
    title='Health Expenditure vs Mortality Rate'
)
st.plotly_chart(fig2, use_container_width=True)
