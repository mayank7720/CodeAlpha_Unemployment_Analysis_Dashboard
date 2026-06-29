from utils.data_loader import clean_html
import streamlit as st
import pandas as pd
from visualizations.charts import plot_rural_vs_urban

def render_rural_urban_tab(df_area, filters):
    """
    Renders the Rural vs Urban comparison tab content.
    """
    st.markdown("### Rural vs Urban Labor Dynamics")
    st.markdown(
        "Analyze differences between Rural and Urban labor sectors. "
        "Historically, Rural sectors display higher participation rates, while Urban sectors show higher unemployment rates."
    )
    
    # 1. Rural vs Urban Trend Line
    fig_comp = plot_rural_vs_urban(
        df_area,
        date_col='Date_iso',
        rate_col='Unemployment_Rate',
        area_col='Area',
        title="Rural vs Urban Unemployment Rate Trends (2019-2020)"
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            clean_html("""
            <div class="section-container">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">Average Metrics comparison</h4>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        # Calculate averages grouped by Area
        avg_metrics = df_area.groupby('Area')[['Unemployment_Rate', 'Labour_Participation_Rate']].mean().reset_index()
        
        # Display as a table using streamlit dataframe or HTML
        st.dataframe(
            avg_metrics.rename(columns={
                'Unemployment_Rate': 'Avg Unemployment (%)',
                'Labour_Participation_Rate': 'Avg Participation (%)'
            }),
            use_container_width=True,
            hide_index=True
        )
        
    with col2:
        st.markdown(
            clean_html("""
            <div class="section-container">
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff;">Cohort Insight</h4>
                <p style="margin: 0; color: #94a3b8; font-size: 0.9rem; line-height: 1.5;">
                    Rural labor markets in India are heavily influenced by seasonal agriculture. 
                    During the April-May 2020 lockdown, urban regions saw an immediate and severe spike 
                    in unemployment due to the closure of service and construction sectors, whereas 
                    rural regions experienced a slightly smaller impact due to agricultural exemptions.
                </p>
            </div>
            """),
            unsafe_allow_html=True
        )
