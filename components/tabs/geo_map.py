from utils.data_loader import clean_html
import streamlit as st
import pandas as pd
import json
import os
from visualizations.maps import plot_geographic_map, plot_choropleth_map

def render_geo_map_tab(df_states, filters):
    """
    Renders the Geographic Map tab content, allowing toggle between bubble map
    and choropleth map, with static or animated timeline options.
    """
    st.markdown("### State-wise Geographic Spread")
    st.markdown(
        "Geographical distribution of the unemployment rate in India. "
        "Analyze spatial clusters using coordinates (Bubble Map) or boundary fills (Choropleth Map)."
    )
    
    # Load GeoJSON boundaries for Choropleth
    geojson_path = 'data/processed/india_states.geojson'
    if not os.path.exists(geojson_path):
        geojson_path = '../data/processed/india_states.geojson'
        
    try:
        with open(geojson_path, 'r') as f:
            geojson = json.load(f)
    except Exception as e:
        st.error(f"Failed to load India states boundary GeoJSON: {e}")
        geojson = None
        
    # Selection Controls
    col_sel1, col_sel2, col_sel3 = st.columns([1.5, 1.5, 2])
    with col_sel1:
        map_type = st.radio(
            "Select Map Style",
            options=["Choropleth (Boundaries)", "Bubble Map (Coordinates)"],
            horizontal=True
        )
    with col_sel2:
        map_mode = st.radio(
            "Select Map Mode",
            options=["Static Average Map", "Animated Timeline Slider"],
            horizontal=True
        )
    with col_sel3:
        st.markdown(
            "<span style='color:#94a3b8;font-size:0.85rem;'>*Map projection is customized for India. Zoom and pan to inspect specific regions. Use the play/pause slider below the chart in Animated mode.</span>",
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Map rendering
    date_col = 'Date_iso' if map_mode == "Animated Timeline Slider" else None
    
    if map_type == "Choropleth (Boundaries)":
        if geojson:
            fig_map = plot_choropleth_map(
                df=df_states,
                geojson=geojson,
                state_col='Region',
                rate_col='Unemployment_Rate',
                date_col=date_col,
                title="State-wise Unemployment Rate Choropleth"
            )
        else:
            st.warning("GeoJSON boundary file missing. Falling back to bubble map.")
            fig_map = plot_geographic_map(
                df=df_states,
                state_col='Region',
                rate_col='Unemployment_Rate',
                lat_col='latitude',
                lon_col='longitude',
                date_col=date_col,
                title="State-wise Unemployment Rate Bubble Map"
            )
    else:
        fig_map = plot_geographic_map(
            df=df_states,
            state_col='Region',
            rate_col='Unemployment_Rate',
            lat_col='latitude',
            lon_col='longitude',
            date_col=date_col,
            title="State-wise Unemployment Rate Bubble Map"
        )
        
    # Render Plotly Chart
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Map observations
    st.markdown(
        clean_html("""
        <div class="section-container" style="margin-top: 1rem;">
            <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">Geographic Observations</h4>
            <ul style="margin: 0; padding-left: 1.2rem; color: #94a3b8; font-size: 0.9rem; line-height: 1.6;">
                <li><b>Northern Region:</b> Persistent high unemployment clusters are concentrated in Haryana, Himachal Pradesh, and Jammu & Kashmir.</li>
                <li><b>Southern Region:</b> States like Puducherry showed temporary sharp increases during the lockdown months, stabilizing quickly thereafter.</li>
                <li><b>Eastern Region:</b> States like Jharkhand and Bihar experienced prolonged elevated levels, matching high labor participation.</li>
            </ul>
        </div>
        """),
        unsafe_allow_html=True
    )
