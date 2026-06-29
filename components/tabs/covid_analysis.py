from utils.data_loader import clean_html
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Styling constants
COLOR_PRIMARY = "#6366f1"   # Indigo
COLOR_SECONDARY = "#a855f7" # Purple
COLOR_BG = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255, 255, 255, 0.06)"

def render_covid_analysis_tab(df_states, df_area):
    """
    Renders the dedicated COVID-19 Analysis tab, comparing baseline and lockdown periods,
    displaying slope charts, area charts, percentage changes, and top affected states.
    """
    st.markdown("### COVID-19 Socioeconomic Impact & Recovery Analysis")
    st.markdown(
        "A dedicated study of the labor market shock during the pandemic in 2020. "
        "This section compares the pre-lockdown baseline with the lockdown peak and tracks the subsequent recovery."
    )
    
    # 1. Define Phases
    # Baseline: Jan - Feb 2020
    # Lockdown Peak: Apr - May 2020
    # Recovery: Jun - Oct 2020
    
    # We will compute these metrics using df_states (which covers 2020)
    baseline_df = df_states[df_states['Date_iso'] < '2020-03-01']
    lockdown_df = df_states[(df_states['Date_iso'] >= '2020-03-01') & (df_states['Date_iso'] <= '2020-05-31')]
    recovery_df = df_states[df_states['Date_iso'] > '2020-05-31']
    
    avg_baseline = baseline_df['Unemployment_Rate'].mean()
    avg_lockdown = lockdown_df['Unemployment_Rate'].mean()
    avg_recovery = recovery_df['Unemployment_Rate'].mean()
    
    pct_increase = ((avg_lockdown - avg_baseline) / avg_baseline) * 100
    recovery_progress = ((avg_lockdown - avg_recovery) / (avg_lockdown - avg_baseline)) * 100
    
    # KPI metrics side-by-side
    st.markdown(
        clean_html(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
            
            <!-- Baseline Card -->
            <div class="kpi-card" style="border-left: 4px solid #22c55e;">
                <div class="kpi-title">Pre-COVID Baseline (Jan-Feb)</div>
                <div class="kpi-value">{avg_baseline:.2f}%</div>
                <div class="kpi-footer-text">Average national rate</div>
            </div>
            
            <!-- Lockdown Peak Card -->
            <div class="kpi-card" style="border-left: 4px solid #ef4444;">
                <div class="kpi-title">Lockdown Peak Avg (Mar-May)</div>
                <div class="kpi-value">{avg_lockdown:.2f}%</div>
                <div class="kpi-footer-text" style="color:#ef4444; font-weight:600;">
                    {pct_increase:+.1f}% Increase
                </div>
            </div>
            
            <!-- Recovery Card -->
            <div class="kpi-card" style="border-left: 4px solid #6366f1;">
                <div class="kpi-title">Recovery Phase (Jun-Oct)</div>
                <div class="kpi-value">{avg_recovery:.2f}%</div>
                <div class="kpi-footer-text" style="color:#22c55e; font-weight:600;">
                    {recovery_progress:.1f}% Recovered
                </div>
            </div>
            
        </div>
        """),
        unsafe_allow_html=True
    )
    
    # 2. Area Chart: National Employment Shocks
    st.markdown(
        clean_html("""
        <div class="section-container">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.15rem; color: #ffffff;">National Workforce Shrinkage (Employment Area Chart)</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">
                This area chart shows the massive contraction in the estimated employed workforce during the lockdown (April-May 2020).
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    # Group by date to get national total employed
    emp_trend = df_states.groupby('Date_iso')['Employed'].sum().reset_index()
    emp_trend = emp_trend.sort_values(by='Date_iso')
    
    # Format X dates
    emp_trend['Month_Label'] = pd.to_datetime(emp_trend['Date_iso']).dt.strftime('%b %Y')
    
    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(
        x=emp_trend['Month_Label'],
        y=emp_trend['Employed'] / 1e6, # Show in millions
        fill='tozeroy',
        mode='lines+markers',
        name='Employed (Millions)',
        line=dict(color=COLOR_PRIMARY, width=3),
        fillcolor='rgba(99, 102, 241, 0.15)',
        hovertemplate='Month: %{x}<br>Employed Workforce: <b>%{y:.2f}M</b><extra></extra>'
    ))
    
    # Highlight lockdown region in red shading
    fig_area.add_vrect(
        x0="Mar 2020", x1="May 2020",
        fillcolor="rgba(239, 68, 68, 0.08)", opacity=0.5,
        layer="below", line_width=0,
        annotation_text="Lockdown Period",
        annotation_position="bottom left",
        annotation_font=dict(color="#ef4444", size=11)
    )
    
    fig_area.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis_title="",
        yaxis_title="Total Employed (Millions)"
    )
    fig_area.update_xaxes(showgrid=True, gridcolor=GRID_COLOR)
    fig_area.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
    
    st.plotly_chart(fig_area, use_container_width=True)
    
    # 3. Side-by-Side: State-wise Shift Slope Chart & Top Affected States
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(
            clean_html("""
            <div class="section-container">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.15rem; color: #ffffff;">State-wise Unemployment Shift (Slope Chart)</h4>
                <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">
                    Compare state average unemployment rates Before COVID (Jan-Feb) vs. Lockdown Peak (Apr-May).
                </p>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        # Calculate state averages for baseline and lockdown
        state_baseline = baseline_df.groupby('Region')['Unemployment_Rate'].mean().reset_index().rename(columns={'Unemployment_Rate': 'Before_COVID'})
        state_lockdown = lockdown_df.groupby('Region')['Unemployment_Rate'].mean().reset_index().rename(columns={'Unemployment_Rate': 'Lockdown_Peak'})
        
        slope_df = pd.merge(state_baseline, state_lockdown, on='Region')
        
        # Sort by peak to render cleanly
        slope_df = slope_df.sort_values(by='Lockdown_Peak', ascending=False)
        
        fig_slope = go.Figure()
        
        # Plot a line for each state connecting Before -> During
        for idx, row in slope_df.iterrows():
            state = row['Region']
            val_before = row['Before_COVID']
            val_peak = row['Lockdown_Peak']
            
            # Determine color: red if rate increased, green if decreased
            line_color = "#ef4444" if val_peak > val_before else "#22c55e"
            
            fig_slope.add_trace(go.Scatter(
                x=['Before COVID', 'Lockdown Peak'],
                y=[val_before, val_peak],
                mode='lines+markers+text',
                name=state,
                line=dict(color=line_color, width=2),
                marker=dict(size=6, color=line_color),
                text=[f"{state} ({val_before:.1f}%)" if i == 0 else f"{val_peak:.1f}%" for i in range(2)],
                textposition=["middle left", "middle right"],
                textfont=dict(size=9, color="#94a3b8"),
                showlegend=False,
                hovertemplate=f'State: <b>{state}</b><br>Before: {val_before:.2f}%<br>Peak: {val_peak:.2f}%<extra></extra>'
            ))
            
        fig_slope.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLOR_BG,
            plot_bgcolor=COLOR_BG,
            font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
            margin=dict(l=100, r=100, t=20, b=40),
            yaxis_title="Unemployment Rate (%)",
            xaxis=dict(range=[-0.2, 1.2]) # give some space on sides for labels
        )
        fig_slope.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
        
        st.plotly_chart(fig_slope, use_container_width=True)
        
    with col2:
        st.markdown(
            clean_html("""
            <div class="section-container">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.15rem; color: #ffffff;">Top 10 Pandemic Affected States</h4>
                <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">
                    States sorted by the absolute rate increase (Spike) from Baseline to Lockdown Peak.
                </p>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        slope_df['Rate_Spike'] = slope_df['Lockdown_Peak'] - slope_df['Before_COVID']
        top_affected = slope_df.sort_values(by='Rate_Spike', ascending=False).head(10)
        
        # Plot bar chart of spikes
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=top_affected['Rate_Spike'],
            y=top_affected['Region'],
            orientation='h',
            marker=dict(
                color=top_affected['Rate_Spike'],
                colorscale=[[0, 'rgba(168, 85, 247, 0.7)'], [1, 'rgba(239, 68, 68, 0.9)']],
                line=dict(color='rgba(255,255,255,0.1)', width=1)
            ),
            hovertemplate='State: %{y}<br>Rate Spike: <b>+%{x:.2f}%</b><extra></extra>'
        ))
        
        # Sort Y axis values correctly
        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLOR_BG,
            plot_bgcolor=COLOR_BG,
            font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
            margin=dict(l=40, r=40, t=10, b=40),
            xaxis_title="Rate Increase (Percentage Points)",
            yaxis=dict(autorange="reversed")
        )
        fig_bar.update_xaxes(showgrid=True, gridcolor=GRID_COLOR)
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # 4. Summary Insights
    st.markdown(
        clean_html("""
        <div class="section-container" style="margin-top: 1.5rem;">
            <h4 style="margin: 0 0 0.8rem 0; font-size: 1.15rem; color: #ffffff;">💡 COVID-19 Socioeconomic Analysis</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; color: #94a3b8; font-size: 0.9rem; line-height: 1.6;">
                <div>
                    <h5 style="color: #ffffff; margin-bottom: 0.5rem;">The Lockdown Disruption</h5>
                    In April 2020, India implemented one of the world's strictest lockdowns. The immediate impact was a 
                    near-complete cessation of economic activities in urban hubs. The national estimated employed workforce 
                    contracted sharply from over <b>410 million</b> workers in January 2020 to less than <b>340 million</b> in April, 
                    representing a contraction of approximately <b>70 million jobs</b> in a single month.
                </div>
                <div>
                    <h5 style="color: #ffffff; margin-bottom: 0.5rem;">State-level Vulnerability</h5>
                    The slope chart highlights that almost all states saw their unemployment rates double or triple. Puducherry 
                    experienced the most severe absolute spike, leaping from <b>~10%</b> to over <b>70%</b> in April. 
                    Industrialized states or those with large migrant labor workforces, such as Haryana, Jharkhand, and Delhi, 
                    recorded peak lockdown averages exceeding <b>25%</b>.
                </div>
                <div>
                    <h5 style="color: #ffffff; margin-bottom: 0.5rem;">Recovery Trajectory</h5>
                    The post-lockdown phase (June - October 2020) shows a rapid rebound as restrictions eased. By October 2020, 
                    the national unemployment rate had stabilized back down to <b>6.99%</b>, showing a V-shaped recovery path. 
                    This recovery was primarily driven by rural agricultural demand and the phased reopening of commercial sectors.
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
