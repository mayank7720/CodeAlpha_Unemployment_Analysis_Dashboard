from utils.data_loader import clean_html
import streamlit as st
import os
import pandas as pd

# Import modular components and visualization functions
from utils.data_loader import load_state_data, load_area_data, load_raw_state_data, load_raw_area_data
from components.sidebar import render_sidebar
from components.tabs.overview import render_overview_tab
from components.tabs.trends import render_trends_tab
from components.tabs.rural_urban import render_rural_urban_tab
from components.tabs.geo_map import render_geo_map_tab
from components.tabs.data_cleaning import render_data_cleaning_tab
from components.tabs.eda import render_eda_tab
from components.tabs.covid_analysis import render_covid_analysis_tab
from components.tabs.insights_report import render_insights_tab
from components.tabs.policy_recommendations import render_policy_tab

# 1. Page Configuration (inspired by Power BI & Stripe)
st.set_page_config(
    page_title="Unemployment Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Premium Custom Styling
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found at {file_name}")

local_css("assets/styles.css")

# 3. Load Connected Datasets (Processed via pipeline)
df_states_raw = load_state_data()
df_area_raw = load_area_data()

# Load uncleaned raw data for diagnostics tab
df_states_raw_uncleaned = load_raw_state_data()
df_area_raw_uncleaned = load_raw_area_data()

# 4. Render Sidebar and Capture Filters
filters = render_sidebar(df_states_raw, df_area_raw)

# 5. Apply Global Filters to Datasets
df_states = df_states_raw.copy()
df_area = df_area_raw.copy()

# Apply Region filter
if filters['region'] != "All Regions":
    df_states = df_states[df_states['Geographic_Region'] == filters['region']]
    df_area = df_area[df_area['Geographic_Region'] == filters['region']]

# Apply State filter (if any selected)
if filters['states']:
    df_states = df_states[df_states['Region'].isin(filters['states'])]
    df_area = df_area[df_area['Region'].isin(filters['states'])]

# Apply Area filter to df_area
if filters['area'] == "Rural Only":
    df_area = df_area[df_area['Area'] == "Rural"]
elif filters['area'] == "Urban Only":
    df_area = df_area[df_area['Area'] == "Urban"]

# Apply Year Filter
if filters['year'] != "All Years":
    year_val = int(filters['year'])
    df_states = df_states[pd.to_datetime(df_states['Date_iso']).dt.year == year_val]
    df_area = df_area[pd.to_datetime(df_area['Date_iso']).dt.year == year_val]

# Apply Month Filter
if filters['months']:
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    month_nums = [month_map[m] for m in filters['months']]
    df_states = df_states[pd.to_datetime(df_states['Date_iso']).dt.month.isin(month_nums)]
    df_area = df_area[pd.to_datetime(df_area['Date_iso']).dt.month.isin(month_nums)]

# Apply Date Range filter
start_date, end_date = filters['date_range']
df_states = df_states[(df_states['Date_iso'] >= start_date) & (df_states['Date_iso'] <= end_date)]
df_area = df_area[(df_area['Date_iso'] >= start_date) & (df_area['Date_iso'] <= end_date)]

# Safety Check: Empty Dataframe Guard
if df_states.empty or df_area.empty:
    st.markdown(
        clean_html("""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-weight: 800; font-size: 2.5rem; color: #ffffff; letter-spacing: -0.04em; margin: 0;">
                Unemployment Analysis Dashboard
            </h1>
            <p style="color: #94a3b8; font-size: 1.05rem; margin-top: 0.25rem;">
                Interactive socio-economic insights & labor force dynamics in India (2019-2020)
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )
    st.warning("⚠️ **No data matches the selected filters.** Please adjust your Year, Month, State, or Date Range parameters in the sidebar.")
    st.stop()

# 6. Main Panel Layout
st.markdown(
    clean_html("""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-weight: 800; font-size: 2.5rem; color: #ffffff; letter-spacing: -0.04em; margin: 0;">
            Unemployment Analysis Dashboard
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem; margin-top: 0.25rem;">
            Interactive socio-economic insights & labor force dynamics in India (2019-2020)
        </p>
    </div>
    """),
    unsafe_allow_html=True
)

# Create premium navigation tabs
tabs = st.tabs([
    "📂 Executive Overview",
    "🦠 COVID-19 Impact Analysis",
    "📈 Temporal Trends & Slopes",
    "🏘️ Rural vs Urban Analysis",
    "🌍 Geographical Distribution",
    "📊 Exploratory Analysis (EDA)",
    "📜 Automated Reports & Insights",
    "📋 Policy Recommendations",
    "🛠️ Data Cleaning Module",
    "🔍 Raw Data Explorer"
])

# Render each tab
with tabs[0]:
    with st.spinner("Analyzing executive KPIs..."):
        render_overview_tab(df_states, filters)

with tabs[1]:
    with st.spinner("Compiling COVID-19 timeline shifts..."):
        render_covid_analysis_tab(df_states, df_area)

with tabs[2]:
    with st.spinner("Decomposing trend & seasonality components..."):
        render_trends_tab(df_states, filters)

with tabs[3]:
    with st.spinner("Structuring rural vs urban ratios..."):
        render_rural_urban_tab(df_area, filters)

with tabs[4]:
    with st.spinner("Loading geographical spatial boundaries..."):
        render_geo_map_tab(df_states, filters)

with tabs[5]:
    with st.spinner("Generating statistical distributions & correlation matrix..."):
        render_eda_tab(df_states, df_area)

with tabs[6]:
    with st.spinner("Compiling automated reports & anomalies..."):
        render_insights_tab(df_states, df_area)

with tabs[7]:
    with st.spinner("Formatting economic policy options..."):
        render_policy_tab(df_states, df_area)

with tabs[8]:
    with st.spinner("Auditing data sanitization pipeline..."):
        render_data_cleaning_tab(df_states_raw_uncleaned, df_states_raw, df_area_raw_uncleaned, df_area_raw)

with tabs[9]:
    st.markdown("### Raw Data Explorer")
    st.markdown(
        "Search, filter, and inspect records directly. This dataset is compiled from India's labor force statistics."
    )
    
    # Text Search Filter
    search_query = st.text_input("Search by State (Region)", placeholder="Enter state name (e.g. Andhra Pradesh, Haryana)")
    
    df_table = df_states.copy()
    if search_query:
        df_table = df_table[df_table['Region'].str.contains(search_query, case=False)]
        
    # Table Options
    cols_to_show = [
        'Region', 'Geographic_Region', 'Date_iso', 'Unemployment_Rate', 
        'Employed', 'Labour_Participation_Rate'
    ]
    
    st.dataframe(
        df_table[cols_to_show].rename(columns={
            'Region': 'State',
            'Geographic_Region': 'Region',
            'Date_iso': 'Reporting Date',
            'Unemployment_Rate': 'Unemployment Rate (%)',
            'Employed': 'Estimated Employed',
            'Labour_Participation_Rate': 'Labour Participation (%)'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Download Button
    csv_data = df_table[cols_to_show].to_csv(index=False)
    st.download_button(
        label="📥 Export Filtered Data as CSV",
        data=csv_data,
        file_name="unemployment_filtered_data.csv",
        mime="text/csv"
    )
