import streamlit as st
from utils.data_loader import clean_html

def render_kpi_cards(avg_unemp, total_emp, avg_part):
    """
    Renders floating, glassmorphic KPI cards using custom HTML and CSS styled in assets/styles.css.
    """
    # SVG Paths for icons
    icon_unemp = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 12-6-6-6 6"/><path d="M12 6v14"/></svg>""" # arrow-up
    icon_emp = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""" # users
    icon_part = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/><circle cx="12" cy="12" r="4"/></svg>""" # target / participation

    # Format numbers
    emp_str = f"{total_emp / 1e6:.2f}M" if total_emp >= 1e6 else f"{total_emp:,.0f}"
    
    # Render KPI Cards in custom columns via Streamlit HTML injection
    kpi_html = f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; width: 100%;">
        
        <!-- Card 1: Avg Unemployment Rate -->
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Avg Unemployment Rate</span>
                <div class="kpi-icon" style="color: #6366f1;">
                    {icon_unemp}
                </div>
            </div>
            <div class="kpi-value">{avg_unemp:.2f}%</div>
            <div class="kpi-footer">
                <span class="trend-badge trend-up">
                    +1.2%
                </span>
                <span class="kpi-footer-text">vs previous period</span>
            </div>
        </div>
        
        <!-- Card 2: Total Estimated Employed -->
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Avg Estimated Employed</span>
                <div class="kpi-icon" style="color: #a855f7;">
                    {icon_emp}
                </div>
            </div>
            <div class="kpi-value">{emp_str}</div>
            <div class="kpi-footer">
                <span class="trend-badge trend-down" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">
                    -0.8%
                </span>
                <span class="kpi-footer-text">vs previous period</span>
            </div>
        </div>
        
        <!-- Card 3: Labour Participation Rate -->
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Labour Participation</span>
                <div class="kpi-icon" style="color: #22c55e;">
                    {icon_part}
                </div>
            </div>
            <div class="kpi-value">{avg_part:.2f}%</div>
            <div class="kpi-footer">
                <span class="trend-badge trend-down" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">
                    -0.4%
                </span>
                <span class="kpi-footer-text">vs previous period</span>
            </div>
        </div>
        
    </div>
    """
    st.markdown(clean_html(kpi_html), unsafe_allow_html=True)


