import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Premium Plotly Design Configs aligning with UI-UX Pro Max
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_PRIMARY = "#6366f1"   # Indigo
COLOR_SECONDARY = "#a855f7" # Purple
COLOR_ACCENT = "#22c55e"    # Green
COLOR_MUTED = "#94a3b8"     # Slate Gray
COLOR_BG = "rgba(0,0,0,0)"   # Transparent
GRID_COLOR = "rgba(255, 255, 255, 0.06)"

def apply_premium_layout(fig):
    """
    Applies custom styling overrides to standard Plotly charts for a premium appearance.
    """
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font=dict(family="Outfit, Inter, sans-serif", color="#e2e8f0"),
        margin=dict(l=40, r=40, t=60, b=40),
        hoverlabel=dict(
            bgcolor="#151c2c",
            font_size=13,
            font_family="Outfit, sans-serif",
            bordercolor="rgba(255, 255, 255, 0.08)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=12, color="#94a3b8")
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        tickfont=dict(color="#94a3b8"),
        linecolor="rgba(255,255,255,0.1)"
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        tickfont=dict(color="#94a3b8"),
        linecolor="rgba(255,255,255,0.1)"
    )
    return fig

def plot_unemployment_trend(df, date_col, rate_col, show_slope=False, title="Unemployment Rate Trend"):
    """
    Plots a line chart of the unemployment rate over time.
    If show_slope is True, calculates and displays the regression line (slope) - implementing Slope Skill.
    """
    # Group by date to get national/aggregated average
    monthly_avg = df.groupby(date_col)[rate_col].mean().reset_index()
    monthly_avg = monthly_avg.sort_values(by=date_col)
    
    fig = go.Figure()
    
    # Actual Trend Line
    fig.add_trace(go.Scatter(
        x=monthly_avg[date_col],
        y=monthly_avg[rate_col],
        mode='lines+markers',
        name='Unemployment Rate (%)',
        line=dict(color=COLOR_PRIMARY, width=3, shape='spline'),
        marker=dict(size=8, color=COLOR_PRIMARY, line=dict(color='#ffffff', width=1.5)),
        hovertemplate='Date: %{x}<br>Unemployment Rate: <b>%{y:.2f}%</b><extra></extra>'
    ))
    
    # Slope Skill Implementation: Ordinary Least Squares (OLS) Regression
    if show_slope and len(monthly_avg) > 1:
        # Convert dates to numeric indices for regression
        x_indices = np.arange(len(monthly_avg))
        y_values = monthly_avg[rate_col].values
        
        # Fit line: y = mx + c
        slope, intercept = np.polyfit(x_indices, y_values, 1)
        regression_y = slope * x_indices + intercept
        
        # Determine color of trendline
        trendline_color = "#ef4444" if slope > 0 else "#22c55e" # red if increasing, green if decreasing
        direction_text = "Increasing ↗" if slope > 0 else "Decreasing ↘"
        
        # Add regression line
        fig.add_trace(go.Scatter(
            x=monthly_avg[date_col],
            y=regression_y,
            mode='lines',
            name=f'Trendline ({direction_text})',
            line=dict(color=trendline_color, width=2, dash='dash'),
            hovertemplate='Trend (OLS): <b>%{y:.2f}%</b><extra></extra>'
        ))
        
        # Add annotation for slope value
        # Slope represents % change per month
        slope_percentage_str = f"{slope:+.2f}% / month"
        fig.add_annotation(
            xref="paper", yref="paper",
            x=0.05, y=0.95,
            text=f"<b>Trend Slope:</b> {slope_percentage_str}<br><b>Direction:</b> {direction_text}",
            showarrow=False,
            align="left",
            font=dict(size=12, color="#ffffff"),
            bgcolor="rgba(21, 28, 44, 0.8)",
            bordercolor=trendline_color,
            borderwidth=1,
            borderpad=8,
            bordercolor_opacity=0.5
        )
        
    fig.update_layout(title=title)
    return apply_premium_layout(fig)

def plot_state_rankings(df, state_col, rate_col, top_n=10, ascending=False, title="State Rankings"):
    """
    Plots a premium horizontal bar chart showing the highest or lowest unemployment states.
    """
    state_avg = df.groupby(state_col)[rate_col].mean().reset_index()
    state_avg = state_avg.sort_values(by=rate_col, ascending=ascending).head(top_n)
    
    # Sort for horizontal rendering (top item at the top of the chart)
    state_avg = state_avg.sort_values(by=rate_col, ascending=not ascending)
    
    # Color scale from secondary (purple) to primary (indigo)
    colors = [COLOR_PRIMARY if i < top_n // 2 else COLOR_SECONDARY for i in range(len(state_avg))]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=state_avg[rate_col],
        y=state_avg[state_col],
        orientation='h',
        marker=dict(
            color=state_avg[rate_col],
            colorscale=[[0, 'rgba(99, 102, 241, 0.6)'], [1, 'rgba(168, 85, 247, 0.9)']],
            line=dict(color='rgba(255,255,255,0.1)', width=1)
        ),
        hovertemplate='State: %{y}<br>Avg Unemployment: <b>%{x:.2f}%</b><extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Average Unemployment Rate (%)",
        yaxis_title=""
    )
    return apply_premium_layout(fig)

def plot_rural_vs_urban(df, date_col, rate_col, area_col, title="Rural vs Urban Unemployment Rate"):
    """
    Plots a side-by-side comparison of rural and urban trends over time.
    """
    # Group by date and area
    grouped = df.groupby([date_col, area_col])[rate_col].mean().reset_index()
    
    fig = go.Figure()
    
    for area in ['Rural', 'Urban']:
        area_df = grouped[grouped[area_col] == area].sort_values(by=date_col)
        color = COLOR_PRIMARY if area == 'Rural' else COLOR_SECONDARY
        
        fig.add_trace(go.Scatter(
            x=area_df[date_col],
            y=area_df[rate_col],
            mode='lines+markers',
            name=f'{area} Areas',
            line=dict(color=color, width=3, shape='spline'),
            marker=dict(size=7, color=color),
            hovertemplate=f'{area} - %{{x}}<br>Rate: <b>%{{y:.2f}}%</b><extra></extra>'
        ))
        
    fig.update_layout(
        title=title,
        yaxis_title="Unemployment Rate (%)"
    )
    return apply_premium_layout(fig)

def plot_participation_vs_unemployment(df, rate_col, part_col, state_col, title="Participation Rate vs Unemployment Rate"):
    """
    Plots a scatter plot comparing Unemployment Rate (X) vs Labour Participation Rate (Y) across states.
    Helpful for identifying regional patterns.
    """
    state_avg = df.groupby(state_col)[[rate_col, part_col]].mean().reset_index()
    
    fig = px.scatter(
        state_avg,
        x=rate_col,
        y=part_col,
        text=state_col,
        color=rate_col,
        color_continuous_scale=[[0, '#22c55e'], [0.5, '#6366f1'], [1, '#ef4444']],
        labels={
            rate_col: "Unemployment Rate (%)",
            part_col: "Labour Participation Rate (%)"
        }
    )
    
    fig.update_traces(
        marker=dict(size=14, line=dict(color='rgba(255,255,255,0.2)', width=1)),
        textposition='top center',
        hovertemplate='State: <b>%{text}</b><br>Unemployment: %{x:.2f}%<br>Participation: %{y:.2f}%<extra></extra>'
    )
    
    fig.update_layout(
        title=title,
        coloraxis_showscale=False
    )
    return apply_premium_layout(fig)
