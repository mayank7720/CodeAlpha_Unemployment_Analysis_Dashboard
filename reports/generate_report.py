import pandas as pd
import os

def generate_static_report():
    """
    Reads the raw datasets in data/raw, compiles key statistics,
    and generates a static markdown report in the reports directory.
    """
    raw_state_path = 'data/raw/Unemployment_Rate_upto_11_2020.csv'
    raw_area_path = 'data/raw/Unemployment_in_India.csv'
    
    if not os.path.exists(raw_state_path) or not os.path.exists(raw_area_path):
        print("Raw datasets not found in data/raw/. Run the organizer first.")
        return
        
    print("Generating statistical analysis report...")
    
    # 1. Load Data
    df_state = pd.read_csv(raw_state_path)
    df_state.columns = df_state.columns.str.strip()
    df_state['Region'] = df_state['Region'].str.strip()
    df_state['Date'] = pd.to_datetime(df_state['Date'].str.strip(), format='%d-%m-%Y')
    
    df_area = pd.read_csv(raw_area_path)
    df_area.columns = df_area.columns.str.strip()
    df_area = df_area.dropna()
    df_area['Region'] = df_area['Region'].str.strip()
    df_area['Date'] = pd.to_datetime(df_area['Date'].str.strip(), format='%d-%m-%Y')
    
    # 2. Compute Statistics
    overall_avg_unemp = df_state['Estimated Unemployment Rate (%)'].mean()
    overall_avg_part = df_state['Estimated Labour Participation Rate (%)'].mean()
    overall_avg_emp = df_state['Estimated Employed'].mean()
    
    # Max unemployment rate record
    max_rate_row = df_state.loc[df_state['Estimated Unemployment Rate (%)'].idxmax()]
    
    # COVID Lockdown Stats
    covid_lockdown = df_state[(df_state['Date'] >= '2020-03-01') & (df_state['Date'] <= '2020-05-31')]
    covid_avg_unemp = covid_lockdown['Estimated Unemployment Rate (%)'].mean()
    
    # Pre-COVID Stats
    pre_covid = df_state[df_state['Date'] < '2020-03-01']
    pre_covid_avg = pre_covid['Estimated Unemployment Rate (%)'].mean()
    
    # Top 5 states by average unemployment rate in 2020
    top_states = df_state.groupby('Region')['Estimated Unemployment Rate (%)'].mean().sort_values(ascending=False).head(5)
    
    # Rural vs Urban comparison
    rural_avg = df_area[df_area['Area'] == 'Rural']['Estimated Unemployment Rate (%)'].mean()
    urban_avg = df_area[df_area['Area'] == 'Urban']['Estimated Unemployment Rate (%)'].mean()
    
    # 3. Create Report Content
    report_md = f"""# Unemployment in India: Statistical Summary Report

This report summarizes key insights compiled from labor force surveys across India during the 2019-2020 period.

## Executive Summary

- **Overall Average Unemployment Rate (2020):** {overall_avg_unemp:.2f}%
- **Average Labour Force Participation Rate (2020):** {overall_avg_part:.2f}%
- **Average Estimated Employed (2020):** {overall_avg_emp:,.0f}

---

## Key Findings

### 1. COVID-19 Pandemic Shock
A dramatic surge in unemployment was observed during the national lockdown months (March - May 2020).
- **Pre-COVID Average Unemployment Rate:** {pre_covid_avg:.2f}%
- **Lockdown Period Average Unemployment Rate:** {covid_avg_unemp:.2f}% (An increase of **{((covid_avg_unemp - pre_covid_avg) / pre_covid_avg)*100:.1f}%**)
- **Peak Single Record:** **{max_rate_row['Estimated Unemployment Rate (%)']:.2f}%** in **{max_rate_row['Region']}** on **{max_rate_row['Date'].strftime('%d-%m-%Y')}**.

### 2. State-wise Vulnerability (2020 Averages)
The following states recorded the highest average unemployment rates in 2020:
{chr(10).join([f"- **{state}:** {rate:.2f}%" for state, rate in top_states.items()])}

### 3. Rural vs Urban Labor Segments (2019-2020)
Urban areas recorded consistently higher average unemployment rates than rural areas:
- **Urban Average Unemployment Rate:** {urban_avg:.2f}%
- **Rural Average Unemployment Rate:** {rural_avg:.2f}%

---

*Report generated automatically by `reports/generate_report.py`.*
"""
    
    # 4. Write to File
    report_path = 'reports/summary_report.md'
    with open(report_path, 'w') as f:
        f.write(report_md)
        
    print(f"Report written successfully to {report_path}!")

if __name__ == "__main__":
    generate_static_report()
