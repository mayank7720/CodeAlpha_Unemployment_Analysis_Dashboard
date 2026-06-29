from utils.data_loader import clean_html
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Premium Plotly Design Configs
COLOR_PRIMARY = "#6366f1"   # Indigo
COLOR_SECONDARY = "#a855f7" # Purple
COLOR_BG = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255, 255, 255, 0.06)"

def render_trends_tab(df_states, filters):
    """
    Renders the advanced Trend, Seasonality, and Seasonal Decomposition tab.
    """
    st.markdown("### Advanced Trend & Seasonality Analysis")
    st.markdown(
        "Apply smoothing windows, analyze quarterly patterns, and inspect seasonal "
        "decomposition models to separate underlying trends from cyclical patterns."
    )
    
    # Select Metric to Analyze
    col_sel1, col_sel2 = st.columns([2, 2])
    with col_sel1:
        metric = st.selectbox(
            "Select Analysis Metric",
            options=["Unemployment_Rate", "Employed", "Labour_Participation_Rate"],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="trends_metric_choice"
        )
    with col_sel2:
        rolling_window = st.slider(
            "Select Rolling Window (Months)",
            min_value=2,
            max_value=5,
            value=3,
            help="Size of the moving window to compute the Simple Moving Average (SMA) and Exponential Moving Average (EMA)."
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Get national monthly averages
    ts_df = df_states.groupby('Date_iso')[metric].mean().reset_index().sort_values(by='Date_iso')
    ts_df['Date'] = pd.to_datetime(ts_df['Date_iso'])
    ts_df['Month_Label'] = ts_df['Date'].dt.strftime('%b %Y')
    
    # Calculate Rolling Averages
    ts_df['SMA'] = ts_df[metric].rolling(window=rolling_window, min_periods=1).mean()
    ts_df['EMA'] = ts_df[metric].ewm(span=rolling_window, adjust=False).mean()
    
    # 2. Plotly Line Chart: Rolling Averages
    st.markdown(
        clean_html("""
        <div class="section-container">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">Moving & Rolling Averages</h4>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    fig_roll = go.Figure()
    
    # Raw Series
    fig_roll.add_trace(go.Scatter(
        x=ts_df['Month_Label'],
        y=ts_df[metric],
        mode='lines+markers',
        name='Observed (Raw)',
        line=dict(color='rgba(255, 255, 255, 0.3)', width=1.5),
        marker=dict(size=4),
        hovertemplate='Observed: <b>%{y:.2f}</b><extra></extra>'
    ))
    
    # Simple Moving Average
    fig_roll.add_trace(go.Scatter(
        x=ts_df['Month_Label'],
        y=ts_df['SMA'],
        mode='lines',
        name=f'{rolling_window}-Month Simple Moving Average (SMA)',
        line=dict(color=COLOR_PRIMARY, width=3),
        hovertemplate='SMA: <b>%{y:.2f}</b><extra></extra>'
    ))
    
    # Exponential Moving Average
    fig_roll.add_trace(go.Scatter(
        x=ts_df['Month_Label'],
        y=ts_df['EMA'],
        mode='lines',
        name=f'{rolling_window}-Month Exponential Moving Average (EMA)',
        line=dict(color=COLOR_SECONDARY, width=2, dash='dash'),
        hovertemplate='EMA: <b>%{y:.2f}</b><extra></extra>'
    ))
    
    fig_roll.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_roll.update_xaxes(showgrid=True, gridcolor=GRID_COLOR)
    fig_roll.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
    
    st.plotly_chart(fig_roll, use_container_width=True)
    
    # 3. Quarterly and Monthly cyclical patterns side-by-side
    col_pat1, col_pat2 = st.columns(2)
    
    with col_pat1:
        st.markdown(
            clean_html("""
            <div class="section-container">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">Quarterly Performance Trends</h4>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        # Add Quarter Column
        df_states_q = df_states.copy()
        df_states_q['Date_dt'] = pd.to_datetime(df_states_q['Date_iso'])
        df_states_q['Quarter'] = df_states_q['Date_dt'].dt.to_period('Q').astype(str)
        
        q_avg = df_states_q.groupby('Quarter')[metric].mean().reset_index()
        
        fig_q = go.Figure()
        fig_q.add_trace(go.Bar(
            x=q_avg['Quarter'],
            y=q_avg[metric],
            marker=dict(
                color=q_avg[metric],
                colorscale=[[0, 'rgba(99, 102, 241, 0.7)'], [1, 'rgba(168, 85, 247, 0.9)']]
            ),
            hovertemplate='Quarter: %{x}<br>Avg: <b>%{y:.2f}</b><extra></extra>'
        ))
        fig_q.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLOR_BG,
            plot_bgcolor=COLOR_BG,
            font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
            margin=dict(l=40, r=40, t=10, b=40)
        )
        fig_q.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
        st.plotly_chart(fig_q, use_container_width=True)
        
    with col_pat2:
        st.markdown(
            clean_html("""
            <div class="section-container">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">Monthly Cyclical Patterns</h4>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        df_states_m = df_states.copy()
        df_states_m['Date_dt'] = pd.to_datetime(df_states_m['Date_iso'])
        df_states_m['Month_Name'] = df_states_m['Date_dt'].dt.strftime('%b')
        df_states_m['Month_Num'] = df_states_m['Date_dt'].dt.month
        
        # Sort by month number
        m_avg = df_states_m.groupby(['Month_Num', 'Month_Name'])[metric].mean().reset_index().sort_values(by='Month_Num')
        
        fig_m = go.Figure()
        fig_m.add_trace(go.Scatter(
            x=m_avg['Month_Name'],
            y=m_avg[metric],
            mode='lines+markers',
            name='Monthly Pattern',
            line=dict(color=COLOR_SECONDARY, width=3, shape='spline'),
            marker=dict(size=7, color=COLOR_SECONDARY),
            hovertemplate='Month: %{x}<br>Avg: <b>%{y:.2f}</b><extra></extra>'
        ))
        fig_m.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLOR_BG,
            plot_bgcolor=COLOR_BG,
            font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
            margin=dict(l=40, r=40, t=10, b=40)
        )
        fig_m.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
        st.plotly_chart(fig_m, use_container_width=True)
        
    # 4. Seasonal Decomposition Subplots
    st.markdown(
        clean_html("""
        <div class="section-container" style="margin-top: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">Classical Seasonal Decomposition Subplots</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1.5rem;">
                Decomposes the time-series into Observed, 3-Month Central Trend, and Seasonal/Residual combined components.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    # Calculate Decomposition
    # Trend: 3-month center rolling average
    decomp_df = ts_df.copy()
    decomp_df['Trend'] = decomp_df[metric].rolling(window=3, center=True, min_periods=1).mean()
    
    # Seasonal + Residual combined
    decomp_df['Seasonal_Residual'] = decomp_df[metric] - decomp_df['Trend']
    
    # Create 3 subplots stacked vertically
    fig_decomp = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Observed Series", "Trend Component (Smoothed)", "Seasonal & Residual Deviations")
    )
    
    # Trace 1: Observed
    fig_decomp.add_trace(
        go.Scatter(
            x=decomp_df['Month_Label'], y=decomp_df[metric],
            mode='lines+markers', name='Observed',
            line=dict(color='#e2e8f0', width=2),
            hovertemplate='Observed: %{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Trace 2: Trend
    fig_decomp.add_trace(
        go.Scatter(
            x=decomp_df['Month_Label'], y=decomp_df['Trend'],
            mode='lines', name='Trend',
            line=dict(color=COLOR_PRIMARY, width=3),
            hovertemplate='Trend: %{y:.2f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Trace 3: Seasonal/Residual
    fig_decomp.add_trace(
        go.Bar(
            x=decomp_df['Month_Label'], y=decomp_df['Seasonal_Residual'],
            name='Residuals',
            marker=dict(
                color=decomp_df['Seasonal_Residual'],
                colorscale=[[0, '#ef4444'], [0.5, 'rgba(255,255,255,0.05)'], [1, '#22c55e']]
            ),
            hovertemplate='Deviation: %{y:+.2f}<extra></extra>'
        ),
        row=3, col=1
    )
    
    fig_decomp.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
        margin=dict(l=40, r=40, t=40, b=40),
        height=600,
        showlegend=False
    )
    
    # Style axes grids
    for r in range(1, 4):
        fig_decomp.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, row=r, col=1)
        fig_decomp.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, row=r, col=1)
        
    st.plotly_chart(fig_decomp, use_container_width=True)
