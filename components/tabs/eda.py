from utils.data_loader import clean_html
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Premium Plotly Design Configs
COLOR_PRIMARY = "#6366f1"   # Indigo
COLOR_SECONDARY = "#a855f7" # Purple
COLOR_BG = "rgba(0,0,0,0)"   # Transparent
GRID_COLOR = "rgba(255, 255, 255, 0.06)"

def apply_eda_layout(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font=dict(family="Outfit, Inter, sans-serif", color="#e2e8f0"),
        margin=dict(l=40, r=40, t=50, b=40),
        hoverlabel=dict(bgcolor="#151c2c", font_size=13, font_family="Outfit")
    )
    fig.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(color="#94a3b8"))
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(color="#94a3b8"))
    return fig

def render_eda_tab(df_states, df_area):
    """
    Renders the Interactive EDA module containing histograms, box plots,
    violin plots, scatter plots, correlation heatmaps, and grid summaries.
    """
    st.markdown("### Interactive Exploratory Data Analysis")
    st.markdown(
        "Explore distributions, statistical summaries, relationships, and correlation matrices "
        "across states, regions, and demographics. Adjust the charts using the filters in each section."
    )
    
    # 1. Section: Univariate Distributions
    st.markdown(
        clean_html("""
        <div class="section-container">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.15rem; color: #ffffff;">1. Univariate Statistical Distributions</h4>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        dist_metric = st.selectbox(
            "Select Distribution Metric",
            options=["Unemployment_Rate", "Employed", "Labour_Participation_Rate"],
            format_func=lambda x: x.replace('_', ' ').title()
        )
    with col_e2:
        dist_type = st.selectbox(
            "Select Chart Type",
            options=["Histogram", "Box Plot", "Violin Plot"]
        )
    with col_e3:
        dist_group = st.selectbox(
            "Group / Color By",
            options=["None", "Area", "Geographic_Region"]
        )
        
    # Pick source dataset: if grouping by Area, we MUST use df_area. Otherwise, df_states has more months
    plot_df = df_area if (dist_group == "Area" or "Area" in df_states.columns) else df_states
    
    fig_dist = None
    color_col = None if dist_group == "None" else dist_group
    
    # Plotly distribution generation
    if dist_type == "Histogram":
        fig_dist = px.histogram(
            plot_df,
            x=dist_metric,
            color=color_col,
            marginal="box", # Adds small boxplot on top
            barmode="overlay",
            color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY, "#22c55e"],
            labels={dist_metric: dist_metric.replace('_', ' ').title()}
        )
    elif dist_type == "Box Plot":
        fig_dist = px.box(
            plot_df,
            y=dist_metric,
            x=color_col,
            color=color_col,
            points="outliers",
            color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY, "#22c55e"],
            labels={dist_metric: dist_metric.replace('_', ' ').title()}
        )
    else: # Violin Plot
        fig_dist = px.violin(
            plot_df,
            y=dist_metric,
            x=color_col,
            color=color_col,
            box=True, # Add boxplot inside violin
            points="outliers",
            color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY, "#22c55e"],
            labels={dist_metric: dist_metric.replace('_', ' ').title()}
        )
        
    st.plotly_chart(apply_eda_layout(fig_dist), use_container_width=True)
    
    # 2. Section: Bivariate Scatter & Correlation
    col_div1, col_div2 = st.columns([3, 2])
    
    with col_div1:
        st.markdown(
            clean_html("""
            <div class="section-container">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.15rem; color: #ffffff;">2. Bivariate Relationship Explorer</h4>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        col_sc1, col_sc2 = st.columns(2)
        with col_sc1:
            x_metric = st.selectbox(
                "X-Axis Metric",
                options=["Unemployment_Rate", "Employed", "Labour_Participation_Rate"],
                index=0,
                key="x_met"
            )
        with col_sc2:
            y_metric = st.selectbox(
                "Y-Axis Metric",
                options=["Labour_Participation_Rate", "Unemployment_Rate", "Employed"],
                index=0,
                key="y_met"
            )
            
        fig_scatter = px.scatter(
            plot_df,
            x=x_metric,
            y=y_metric,
            color=color_col,
            trendline="ols" if color_col is None else None, # Add OLS line for single series
            trendline_color_override="#ef4444",
            color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY, "#22c55e"],
            hover_name="Region",
            labels={
                x_metric: x_metric.replace('_', ' ').title(),
                y_metric: y_metric.replace('_', ' ').title()
            }
        )
        st.plotly_chart(apply_eda_layout(fig_scatter), use_container_width=True)
        
    with col_div2:
        st.markdown(
            clean_html("""
            <div class="section-container">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.15rem; color: #ffffff;">3. Feature Correlation Matrix</h4>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        # Calculate correlation matrix
        corr_cols = ['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate', 'latitude', 'longitude']
        corr_matrix = plot_df[corr_cols].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=[c.replace('_', ' ').title() for c in corr_cols],
            y=[c.replace('_', ' ').title() for c in corr_cols],
            colorscale=[[0, '#ef4444'], [0.5, '#151c2c'], [1, '#22c55e']],
            zmin=-1.0, zmax=1.0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            hovertemplate='X: %{x}<br>Y: %{y}<br>Correlation: <b>%{z:.2f}</b><extra></extra>'
        ))
        
        fig_corr.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLOR_BG,
            plot_bgcolor=COLOR_BG,
            font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
            margin=dict(l=40, r=40, t=20, b=40),
            height=380
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
    # 3. Section: State-wise Monthly Heatmap (Tableau Style Heat grid)
    st.markdown(
        clean_html("""
        <div class="section-container" style="margin-top: 1.5rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.15rem; color: #ffffff;">4. State-wise Monthly Heatmap Matrix</h4>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    # Pivot state data: Region vs. Date_iso
    heatmap_df = df_states.pivot_table(
        index='Region',
        columns='Date_iso',
        values='Unemployment_Rate',
        aggfunc='mean'
    )
    
    # Format dates for cleaner heatmap columns (e.g. "Jan 2020", "Feb 2020")
    formatted_months = pd.to_datetime(heatmap_df.columns).strftime('%b %Y')
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_df.values,
        x=formatted_months,
        y=heatmap_df.index,
        colorscale=[[0, '#22c55e'], [0.2, '#6366f1'], [0.5, '#a855f7'], [1, '#ef4444']],
        zmin=0, zmax=40,
        hovertemplate='State: %{y}<br>Month: %{x}<br>Unemployment Rate: <b>%{z:.2f}%</b><extra></extra>'
    ))
    
    fig_heat.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font=dict(family="Outfit, sans-serif", color="#e2e8f0"),
        margin=dict(l=100, r=40, t=10, b=40),
        height=550
    )
    fig_heat.update_xaxes(side="bottom", tickangle=-45)
    
    st.plotly_chart(fig_heat, use_container_width=True)
