import plotly.express as px
import pandas as pd

def plot_geographic_map(df, state_col, rate_col, lat_col, lon_col, date_col=None, title="State-wise Unemployment Map"):
    """
    Plots an interactive geographic map of India using Plotly Mapbox scatter.
    If date_col is provided, sets up an animated map. Otherwise, plots the average for the data.
    """
    # Filter rows with zero lat/lon
    df_map = df[(df[lat_col] != 0) & (df[lon_col] != 0)].copy()
    
    if df_map.empty:
        # Return an empty map figure
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(text="No geographic coordinates available", showarrow=False)
        return fig
        
    if date_col and len(df_map[date_col].unique()) > 1:
        # Sort values by date to ensure chronological slider ordering
        df_map = df_map.sort_values(by=[date_col, state_col])
        
        fig = px.scatter_mapbox(
            df_map,
            lat=lat_col,
            lon=lon_col,
            size=rate_col,
            color=rate_col,
            color_continuous_scale=[[0, '#22c55e'], [0.4, '#6366f1'], [1, '#ef4444']],
            hover_name=state_col,
            hover_data={
                rate_col: ':.2f',
                'Employed': ':,',
                lat_col: False,
                lon_col: False,
                date_col: True
            },
            animation_frame=date_col,
            zoom=3.8,
            center=dict(lat=21.7679, lon=78.8718), # Center of India
            mapbox_style="carto-darkmatter",
            title=title,
            size_max=35
        )
    else:
        # Aggregated Map (Average of filtered data)
        agg_df = df_map.groupby(state_col).agg({
            rate_col: 'mean',
            'Employed': 'mean',
            lat_col: 'first',
            lon_col: 'first'
        }).reset_index()
        
        fig = px.scatter_mapbox(
            agg_df,
            lat=lat_col,
            lon=lon_col,
            size=rate_col,
            color=rate_col,
            color_continuous_scale=[[0, '#22c55e'], [0.4, '#6366f1'], [1, '#ef4444']],
            hover_name=state_col,
            hover_data={
                rate_col: ':.2f',
                'Employed': ':,',
                lat_col: False,
                lon_col: False
            },
            zoom=3.8,
            center=dict(lat=21.7679, lon=78.8718), # Center of India
            mapbox_style="carto-darkmatter",
            title=title,
            size_max=35
        )
        
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        height=650,
        font=dict(family="Outfit, Inter, sans-serif", color="#e2e8f0"),
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            title=dict(text="Rate (%)", font=dict(size=11, color="#94a3b8")),
            thicknessmode="pixels", thickness=15,
            lenmode="fraction", len=0.6,
            yanchor="bottom", y=0.05,
            xanchor="left", x=0.02,
            bgcolor="rgba(15, 23, 42, 0.8)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            tickfont=dict(size=10, color="#94a3b8")
        )
    )
    
    # Configure map UI adjustments (zoom/pan constraints)
    fig.update_mapboxes(
        bounds=dict(west=68.0, east=98.0, south=6.0, north=37.0)
    )
    
    # Check if there is animation_opts (for play/pause controls styling)
    if fig.layout.updatemenus:
        # Style the animation buttons
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1200
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 500
        fig.layout.updatemenus[0].font = dict(color="#e2e8f0", size=11)
        fig.layout.updatemenus[0].bgcolor = "rgba(21, 28, 44, 0.8)"
        fig.layout.updatemenus[0].bordercolor = "rgba(255,255,255,0.1)"
        
    return fig


def plot_choropleth_map(df, geojson, state_col, rate_col, date_col=None, title="State-wise Choropleth Map"):
    """
    Plots an interactive choropleth map of India using Plotly Mapbox.
    """
    if date_col and len(df[date_col].unique()) > 1:
        # Sort for slider chronological order
        df_map = df.sort_values(by=[date_col, state_col]).copy()
        
        fig = px.choropleth_mapbox(
            df_map,
            geojson=geojson,
            locations=state_col,
            featureidkey="properties.ST_NM",
            color=rate_col,
            color_continuous_scale=[[0, '#22c55e'], [0.4, '#6366f1'], [1, '#ef4444']],
            mapbox_style="carto-darkmatter",
            zoom=3.8,
            center=dict(lat=21.7679, lon=78.8718),
            opacity=0.65,
            animation_frame=date_col,
            hover_name=state_col,
            hover_data={
                rate_col: ':.2f',
                'Employed': ':,',
                date_col: True
            },
            title=title
        )
    else:
        # Aggregated Map (Average of filtered data)
        agg_df = df.groupby(state_col).agg({
            rate_col: 'mean',
            'Employed': 'mean'
        }).reset_index()
        
        fig = px.choropleth_mapbox(
            agg_df,
            geojson=geojson,
            locations=state_col,
            featureidkey="properties.ST_NM",
            color=rate_col,
            color_continuous_scale=[[0, '#22c55e'], [0.4, '#6366f1'], [1, '#ef4444']],
            mapbox_style="carto-darkmatter",
            zoom=3.8,
            center=dict(lat=21.7679, lon=78.8718),
            opacity=0.65,
            hover_name=state_col,
            hover_data={
                rate_col: ':.2f',
                'Employed': ':,'
            },
            title=title
        )
        
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        height=650,
        font=dict(family="Outfit, Inter, sans-serif", color="#e2e8f0"),
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            title=dict(text="Rate (%)", font=dict(size=11, color="#94a3b8")),
            thicknessmode="pixels", thickness=15,
            lenmode="fraction", len=0.6,
            yanchor="bottom", y=0.05,
            xanchor="left", x=0.02,
            bgcolor="rgba(15, 23, 42, 0.8)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            tickfont=dict(size=10, color="#94a3b8")
        )
    )
    
    fig.update_mapboxes(
        bounds=dict(west=68.0, east=98.0, south=6.0, north=37.0)
    )
    
    if fig.layout.updatemenus:
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1200
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 500
        fig.layout.updatemenus[0].font = dict(color="#e2e8f0", size=11)
        fig.layout.updatemenus[0].bgcolor = "rgba(21, 28, 44, 0.8)"
        fig.layout.updatemenus[0].bordercolor = "rgba(255,255,255,0.1)"
        
    return fig

