from utils.data_loader import clean_html
import streamlit as st
import pandas as pd

def render_policy_tab(df_states, df_area):
    """
    Renders the Economic Policy Recommendations tab.
    Offers data-driven policy recommendations tailored to resolving
    unemployment spikes, boosting labor participation, and addressing regional disparities.
    """
    st.markdown("### Economic Policy Recommendations & Strategies")
    st.markdown(
        "Based on labor market behaviors, geographical patterns, and pandemic shock cycles "
        "identified in the datasets, the following economic policy recommendations are proposed."
    )
    
    # Calculate state-level averages to drive regional suggestions
    state_averages = df_states.groupby('Region')['Unemployment_Rate'].mean().reset_index()
    high_unemp_states = state_averages.sort_values(by='Unemployment_Rate', ascending=False).head(5)['Region'].tolist()
    
    # 1. 2x3 Grid of Policy Recommendations
    st.markdown(
        clean_html("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-top: 1rem;">
            
            <!-- Card 1: Employment Generation -->
            <div class="kpi-card" style="border-top: 4px solid #6366f1;">
                <h4 style="color: #ffffff; font-size: 1.1rem; margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    🏗️ Employment Generation Strategies
                </h4>
                <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                    <b>Focus on Rural Infrastructure:</b> Leverage agricultural stability during recessions by expanding public works 
                    programs (like MGNREGA) to construct assets like irrigation channels, cold storage facilities, and rural roads. 
                    This helps absorb seasonal rural labor and mitigates post-harvest crop losses.
                </p>
            </div>
            
            <!-- Card 2: Skill Development -->
            <div class="kpi-card" style="border-top: 4px solid #a855f7;">
                <h4 style="color: #ffffff; font-size: 1.1rem; margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    🎓 Skill Development & Re-skilling
                </h4>
                <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                    <b>Urban Re-skilling Corridors:</b> Set up digital and service-sector vocational institutes in cities to transition 
                    unskilled labor displaced by service contractions into emerging gig-economy and digital-logistics roles. 
                    Standardize apprenticeships to bridge theoretical training with industrial job placement.
                </p>
            </div>
            
            <!-- Card 3: MSME Support -->
            <div class="kpi-card" style="border-top: 4px solid #ef4444;">
                <h4 style="color: #ffffff; font-size: 1.1rem; margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    🏭 MSME Revival & Credit Support
                </h4>
                <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                    <b>Credit Guarantees & Tax Relief:</b> Micro, Small, and Medium Enterprises (MSMEs) are the largest employment 
                    absorbers. Policies should extend collateral-free credit lines, offer temporary GST holidays, and subsidize 
                    digital adoption costs to enable MSMEs to sustain payroll during macroeconomic downturns.
                </p>
            </div>
            
            <!-- Card 4: Youth Employment -->
            <div class="kpi-card" style="border-top: 4px solid #22c55e;">
                <h4 style="color: #ffffff; font-size: 1.1rem; margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    🚀 Youth Employment Programs
                </h4>
                <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                    <b>Startup Subsidies & App-Based Work:</b> Establish regional incubation centers in Tier-2 and Tier-3 cities. 
                    Provide wage subsidies for first-time job seekers (EPF reimbursement schemes) to incentivize corporations 
                    to hire young graduates, reducing the 'experience barrier' for early careers.
                </p>
            </div>
            
            <!-- Card 5: Women Employment -->
            <div class="kpi-card" style="border-top: 4px solid #eab308;">
                <h4 style="color: #ffffff; font-size: 1.1rem; margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    👩 Women Employment Initiatives
                </h4>
                <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                    <b>Flexible Work Options & Safe Transit:</b> Promote hybrid/remote work standards in corporate policies. 
                    Increase labor force participation by establishing public day-care centers in industrial clusters and offering 
                    targeted micro-credit (Self-Help Group models) for women-led cottage industries in rural areas.
                </p>
            </div>
            
            <!-- Card 6: Region-Specific Interventions -->
            <div class="kpi-card" style="border-top: 4px solid #f97316;">
                <h4 style="color: #ffffff; font-size: 1.1rem; margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    🗺️ Region-Specific Targeted Interventions
                </h4>
                <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                    <b>Special Economic Corridors:</b> Establish high-priority employment support programs in states with persistently 
                    high unemployment (e.g. <b>{", ".join(high_unemp_states[:3])}</b>). Promote specialized agro-processing, textile, 
                    and assembly parks in these territories to absorb local surplus labor.
                </p>
            </div>
            
        </div>
        """),
        unsafe_allow_html=True
    )
    
    # 2. Structural Policy Brief
    st.markdown(
        clean_html("""
        <div class="section-container" style="margin-top: 2rem;">
            <h4 style="margin: 0 0 0.8rem 0; font-size: 1.15rem; color: #ffffff;">📋 Policy Implementation Blueprint</h4>
            <p style="margin: 0; color: #94a3b8; font-size: 0.9rem; line-height: 1.6;">
                <b>Summary:</b> The data suggests a two-pronged strategy is required to build labor market resilience in India. 
                First, <b>Urban Safety Nets</b> must be established (similar to rural public works) to shield urban service labor 
                from severe downturns. Second, <b>Agricultural Digitization</b> is essential to optimize participation in rural areas. 
                By combining skill development with structured financial relief for MSMEs, states can accelerate recovery and 
                mitigate spatial inequalities.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )
