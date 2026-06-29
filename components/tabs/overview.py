from utils.data_loader import clean_html
import streamlit as st
from components.kpi_cards import render_kpi_cards
from visualizations.charts import plot_state_rankings, plot_participation_vs_unemployment

def render_overview_tab(df_states, filters):
    """
    Renders the Overview tab content.
    """
    st.markdown("### Executive Overview")
    st.markdown(
        "A high-level view of key employment and labor participation metrics across India. "
        "Use the sidebar to filter data by region, state, and date range."
    )
    
    # Calculate KPIs on current filtered dataset
    avg_unemp = df_states['Unemployment_Rate'].mean()
    total_emp = df_states['Employed'].mean() # average employment across the period
    avg_part = df_states['Labour_Participation_Rate'].mean()
    
    # Render premium floating KPI cards
    render_kpi_cards(avg_unemp, total_emp, avg_part)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display Side-by-Side Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            clean_html("""
<div class="section-container">
    <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">State-wise Unemployment Rankings</h4>
</div>
            """),
            unsafe_allow_html=True
        )
        # Select sorting order (Highest/Lowest)
        rank_order = st.radio(
            "Sort Rankings",
            options=["Highest Unemployment States", "Lowest Unemployment States"],
            horizontal=True,
            label_visibility="collapsed"
        )
        ascending_order = True if "Lowest" in rank_order else False
        
        fig_ranking = plot_state_rankings(
            df_states,
            state_col='Region',
            rate_col='Unemployment_Rate',
            top_n=8,
            ascending=ascending_order,
            title=""
        )
        st.plotly_chart(fig_ranking, use_container_width=True)
        
    with col2:
        st.markdown(
            clean_html("""
<div class="section-container">
    <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">Labour Dynamics Analysis</h4>
</div>
            """),
            unsafe_allow_html=True
        )
        fig_scatter = plot_participation_vs_unemployment(
            df_states,
            rate_col='Unemployment_Rate',
            part_col='Labour_Participation_Rate',
            state_col='Region',
            title=""
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    # Extra insights (styled section)
    st.markdown(
        clean_html("""
<div class="section-container" style="margin-top: 1.5rem;">
    <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #ffffff; display: flex; align-items: center; gap: 0.5rem;">
        💡 Key Insights
    </h4>
    <ul style="margin: 0; padding-left: 1.2rem; color: #94a3b8; font-size: 0.9rem; line-height: 1.6;">
        <li>The national unemployment rate experienced significant volatility, heavily influenced by localized economic shifts.</li>
        <li>There is a distinct negative correlation between high unemployment rates and labor force participation rates, indicating the 'discouraged worker' effect.</li>
        <li>States like Haryana and Tripura recorded persistently higher average rates compared to the national average in this period.</li>
    </ul>
</div>
        """),
        unsafe_allow_html=True
    )

