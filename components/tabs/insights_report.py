from utils.data_loader import clean_html
import streamlit as st
import pandas as pd
import numpy as np
import datetime

def render_insights_tab(df_states, df_area):
    """
    Renders the Automated Reports & Insights tab.
    Calculates macro stats, anomalies, regional differences, and OLS slopes dynamically
    and presents them in a formatted executive report.
    """
    st.markdown("### Automated Executive Reports & Insights")
    st.markdown(
        "This module automatically compiles key statistical insights and patterns based on your current "
        "sidebar filters. You can review the executive summary below and export the report."
    )
    
    # 1. Dynamic Calculations on Filtered Data
    # Overall Averages
    overall_avg_unemp = df_states['Unemployment_Rate'].mean()
    overall_avg_part = df_states['Labour_Participation_Rate'].mean()
    overall_avg_emp = df_states['Employed'].mean()
    
    # Extreme Anomalies
    max_idx = df_states['Unemployment_Rate'].idxmax()
    min_idx = df_states['Unemployment_Rate'].idxmin()
    
    max_record = df_states.loc[max_idx]
    min_record = df_states.loc[min_idx]
    
    # COVID Lockdown Impact (Baseline Jan-Feb 2020 vs Peak Apr-May 2020)
    baseline_df = df_states[df_states['Date_iso'] < '2020-03-01']
    lockdown_df = df_states[(df_states['Date_iso'] >= '2020-03-01') & (df_states['Date_iso'] <= '2020-05-31')]
    
    has_covid_data = not baseline_df.empty and not lockdown_df.empty
    if has_covid_data:
        avg_base = baseline_df['Unemployment_Rate'].mean()
        avg_peak = lockdown_df['Unemployment_Rate'].mean()
        covid_spike = avg_peak - avg_base
        covid_spike_pct = (covid_spike / avg_base) * 100
    else:
        avg_base, avg_peak, covid_spike, covid_spike_pct = 0, 0, 0, 0
        
    # Regional Differences
    region_grouped = df_states.groupby('Geographic_Region')['Unemployment_Rate'].mean().reset_index()
    region_grouped = region_grouped.sort_values(by='Unemployment_Rate', ascending=False)
    highest_region = region_grouped.iloc[0]
    lowest_region = region_grouped.iloc[-1]
    
    # Cohort splits (Rural vs. Urban)
    if 'Area' in df_area.columns and not df_area.empty:
        area_grouped = df_area.groupby('Area')[['Unemployment_Rate', 'Labour_Participation_Rate']].mean()
        rural_rate = area_grouped.loc['Rural', 'Unemployment_Rate'] if 'Rural' in area_grouped.index else 0
        urban_rate = area_grouped.loc['Urban', 'Unemployment_Rate'] if 'Urban' in area_grouped.index else 0
    else:
        rural_rate, urban_rate = 0, 0
        
    # OLS Slope Trend (Slope Skill)
    ts_df = df_states.groupby('Date_iso')['Unemployment_Rate'].mean().reset_index().sort_values(by='Date_iso')
    if len(ts_df) > 1:
        x = np.arange(len(ts_df))
        y = ts_df['Unemployment_Rate'].values
        slope, _ = np.polyfit(x, y, 1)
        trend_direction = "Increasing ↗" if slope > 0 else "Decreasing ↘"
        slope_text = f"{slope:+.2f}% change per month ({trend_direction})"
    else:
        slope_text = "Insufficient date points for trend analysis"
        
    # 2. Compile Report Markdown String
    report_md = f"""# EXECUTIVE REPORT: LABOR DYNAMICS & UNEMPLOYMENT ANALYSIS

**Report Generated:** {datetime.datetime.now().strftime('%d-%B-%Y')}
**Scope of Analysis:** Region: {df_states['Geographic_Region'].unique()}, Date Range: {df_states['Date_iso'].min()} to {df_states['Date_iso'].max()}

---

## 📊 Executive Summary Table
| Metric Name | Calculated Value | Reference / Context |
| :--- | :--- | :--- |
| **Overall Avg Unemployment Rate** | {overall_avg_unemp:.2f}% | Period mean across selected regions |
| **Avg Labour Force Participation** | {overall_avg_part:.2f}% | Workforce activity index |
| **Avg Estimated Employed** | {overall_avg_emp:,.0f} | Total active labor count |
| **Trend Trajectory (OLS Slope)** | {slope_text} | Monthly rate of change |

---

## 🔍 Key Structural Insights

### 1. Extreme Anomalies (Min/Max Records)
- **Highest Unemployment Record:** **{max_record['Unemployment_Rate']:.2f}%** recorded in **{max_record['Region']}** on **{max_record['Date_iso']}**.
- **Lowest Unemployment Record:** **{min_record['Unemployment_Rate']:.2f}%** recorded in **{min_record['Region']}** on **{min_record['Date_iso']}**.

{"### 2. COVID-19 Lockdown Shock Analysis" if has_covid_data else ""}
{"During the national lockdown period, unemployment surged as non-essential business closures went into effect:" if has_covid_data else ""}
- {"**Pre-COVID Baseline Average:** " + f"{avg_base:.2f}%" if has_covid_data else ""}
- {"**Lockdown Peak Average:** " + f"{avg_peak:.2f}%" if has_covid_data else ""}
- {"**Net Percentage Increase:** " + f"{covid_spike_pct:+.1f}%" if has_covid_data else ""}

### 3. Regional Disparities
Labor conditions vary significantly across geographic regions:
- **Highest Unemployment Region:** **{highest_region['Geographic_Region']}** region averaging **{highest_region['Unemployment_Rate']:.2f}%**.
- **Lowest Unemployment Region:** **{lowest_region['Geographic_Region']}** region averaging **{lowest_region['Unemployment_Rate']:.2f}%**.

### 4. Cohort Differences (Rural vs. Urban)
- **Urban Average Unemployment:** **{urban_rate:.2f}%** (characterized by higher susceptibility to service closures).
- **Rural Average Unemployment:** **{rural_rate:.2f}%** (cushioned by agricultural buffer demands).

---

*This report is generated dynamically by the IND-ANALYTICS engine.*
"""
    
    # 3. Render Report inside a Styled Glass Container
    st.markdown(
        clean_html("""
        <div class="section-container" style="border-top: 4px solid #6366f1;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.2rem; color: #ffffff; display: flex; align-items: center; gap: 0.5rem;">
                📜 Compiled Executive Briefing
            </h4>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    st.markdown(report_md)
    
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);' /><br>", unsafe_allow_html=True)
    
    # Export / Download Button
    st.download_button(
        label="📥 Download Executive Report (.md)",
        data=report_md,
        file_name=f"unemployment_executive_report_{datetime.datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    )
