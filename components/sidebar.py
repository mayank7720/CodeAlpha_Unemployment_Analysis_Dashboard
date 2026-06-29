from utils.data_loader import clean_html
import streamlit as st
import pandas as pd

def render_sidebar(df_states, df_area):
    """
    Renders the sidebar navigation and filter controls.
    Returns the selected filters as a dictionary.
    """
    st.sidebar.markdown(
        clean_html("""
        <div style="text-align: center; margin-bottom: 2rem; margin-top: 1rem;">
            <h2 style="color: #6366f1; font-weight: 700; font-size: 1.6rem; letter-spacing: -0.03em; margin: 0;">
                🇮🇳 IND-ANALYTICS
            </h2>
            <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.2rem;">Unemployment Intelligence Suite</p>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    st.sidebar.subheader("Global Filters")
    
    # 1. Region Filter
    regions = sorted(df_states['Geographic_Region'].unique())
    selected_region = st.sidebar.selectbox(
        "Geographic Region",
        options=["All Regions"] + regions,
        index=0
    )
    
    # 2. State Filter (dynamically filtered by Region)
    if selected_region != "All Regions":
        filtered_states = sorted(df_states[df_states['Geographic_Region'] == selected_region]['Region'].unique())
    else:
        filtered_states = sorted(df_states['Region'].unique())
        
    selected_states = st.sidebar.multiselect(
        "States / UTs",
        options=filtered_states,
        default=[]
    )
    
    # 3. Area Filter (Rural / Urban / Both)
    area_type = st.sidebar.radio(
        "Demographic Area",
        options=["Rural & Urban", "Rural Only", "Urban Only"],
        index=0
    )
    
    # 4. Year Filter
    years_available = sorted(list(
        set(pd.to_datetime(df_states['Date_iso']).dt.year.unique()) | 
        set(pd.to_datetime(df_area['Date_iso']).dt.year.unique())
    ))
    selected_year = st.sidebar.selectbox(
        "Year",
        options=["All Years"] + [str(y) for y in years_available],
        index=0
    )
    
    # 5. Month Filter
    months_list = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    selected_months = st.sidebar.multiselect(
        "Months Filter",
        options=months_list,
        default=[],
        help="Select specific months to filter. If none are selected, all months are included."
    )
    
    # 6. Date Range Filter
    # Merge dates from both datasets to get the full span
    all_dates = sorted(list(set(df_states['Date_iso'].unique()) | set(df_area['Date_iso'].unique())))
    
    selected_date_range = st.sidebar.select_slider(
        "Date Range Slider",
        options=all_dates,
        value=(all_dates[0], all_dates[-1])
    )
    
    st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 1.5rem 0;' />", unsafe_allow_html=True)
    
    # 7. Slope Skill Toggle
    st.sidebar.subheader("Advanced Analysis")
    show_slope = st.sidebar.toggle(
        "Calculate OLS Trend Slopes",
        value=True,
        help="Enable Ordinary Least Squares (OLS) regression line and mathematical slope calculation on line charts (Slope Skill)."
    )
    
    return {
        'region': selected_region,
        'states': selected_states,
        'area': area_type,
        'year': selected_year,
        'months': selected_months,
        'date_range': selected_date_range,
        'show_slope': show_slope
    }
