from utils.data_loader import clean_html
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def render_data_cleaning_tab(df_states_raw, df_states_clean, df_area_raw, df_area_clean):
    """
    Renders the Data Cleaning module displaying pipeline metrics, issue reports,
    data samples, and before/after comparisons.
    """
    st.markdown("### Preprocessing Pipeline & Data Diagnostics")
    st.markdown(
        "Compare raw datasets directly against the sanitized, typed results of the automated "
        "data-cleaning pipeline. Choose a dataset below to inspect its diagnostics."
    )
    
    # 1. Dataset Selection
    selected_dataset = st.radio(
        "Select Dataset to Diagnose",
        options=["Unemployment in India (Area Splits)", "Unemployment Rate Upto 11/2020 (State Coords)"],
        horizontal=True
    )
    
    if selected_dataset == "Unemployment in India (Area Splits)":
        raw_df = df_area_raw
        clean_df = df_area_clean
        name_str = "Area Splits Dataset"
    else:
        raw_df = df_states_raw
        clean_df = df_states_clean
        name_str = "State Coords Dataset"
        
    # Calculate Metrics
    raw_rows, raw_cols = raw_df.shape
    clean_rows, clean_cols = clean_df.shape
    
    raw_nulls = raw_df.isnull().sum().sum()
    clean_nulls = clean_df.isnull().sum().sum()
    
    raw_dupes = raw_df.duplicated().sum()
    clean_dupes = clean_df.duplicated().sum()
    
    # Render Before/After KPI Metrics
    st.markdown(
        clean_html(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
            
            <!-- Rows Metric -->
            <div class="kpi-card" style="border-left: 4px solid #6366f1;">
                <div class="kpi-title">Data Ingestion Size</div>
                <div class="kpi-value" style="font-size: 1.6rem; margin: 0.5rem 0;">{raw_rows} → {clean_rows}</div>
                <div class="kpi-footer-text">Rows (Dropped {raw_rows - clean_rows} nulls/dupes)</div>
            </div>
            
            <!-- Missing Values Metric -->
            <div class="kpi-card" style="border-left: 4px solid #a855f7;">
                <div class="kpi-title">Missing Cells Detected</div>
                <div class="kpi-value" style="font-size: 1.6rem; margin: 0.5rem 0;">{raw_nulls} → {clean_nulls}</div>
                <div class="kpi-footer-text" style="color: {'#22c55e' if raw_nulls > 0 else '#94a3b8'};">
                    {f'Dropped {raw_nulls} null cell entries' if raw_nulls > 0 else 'Zero missing cells detected'}
                </div>
            </div>
            
            <!-- Duplicates Metric -->
            <div class="kpi-card" style="border-left: 4px solid #ef4444;">
                <div class="kpi-title">Duplicates Detected</div>
                <div class="kpi-value" style="font-size: 1.6rem; margin: 0.5rem 0;">{raw_dupes} → {clean_dupes}</div>
                <div class="kpi-footer-text" style="color: {'#22c55e' if raw_dupes > 0 else '#94a3b8'};">
                    {f'Deduplicated {raw_dupes} duplicate rows' if raw_dupes > 0 else 'Zero duplicates detected'}
                </div>
            </div>
            
        </div>
        """),
        unsafe_allow_html=True
    )
    
    # 2. Side-by-Side Inconsistent Formats & Types Comparison
    st.markdown(
        clean_html("""
        <div class="section-container">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">Schema & Data Type Sanitization</h4>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    # Build columns comparison schema
    schema_data = []
    
    # Match raw columns with clean counterparts
    raw_cols_list = list(raw_df.columns)
    
    # Helper mapping of columns
    mapping_helper = {
        'Region': 'Region (State)',
        'Date': 'Date_iso',
        'Frequency': 'Frequency',
        'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
        'Estimated Employed': 'Employed',
        'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate',
        'Area': 'Area',
        'Region.1': 'Geographic_Region',
        'longitude': 'longitude',
        'latitude': 'latitude'
    }
    
    for raw_c in raw_cols_list:
        stripped_c = raw_c.strip()
        clean_c = mapping_helper.get(stripped_c, stripped_c)
        
        # Check raw type and clean type
        raw_type = str(raw_df[raw_c].dtype)
        clean_type = str(clean_df[clean_c].dtype) if clean_c in clean_df.columns else "N/A"
        
        # Inconsistencies notes
        issues = []
        if raw_c.startswith(' ') or raw_c.endswith(' '):
            issues.append("Leading/trailing spaces in header")
        if raw_df[raw_c].astype(str).str.startswith(' ').any() or raw_df[raw_c].astype(str).str.endswith(' ').any():
            issues.append("Leading spaces in string values")
        if raw_type != clean_type and clean_type != "N/A":
            issues.append(f"Type coercion: {raw_type} → {clean_type}")
        if stripped_c == 'Date':
            issues.append("Date format parsed (DD-MM-YYYY → YYYY-MM-DD)")
            
        schema_data.append({
            "Raw Column Name": f"'{raw_c}'",
            "Raw Type": raw_type,
            "Clean Column Name": f"'{clean_c}'" if clean_c in clean_df.columns else "Dropped",
            "Clean Type": clean_type,
            "Sanitization Actions": ", ".join(issues) if issues else "None (Clean)"
        })
        
    st.table(pd.DataFrame(schema_data))
    
    # 3. Before/After Interactive Sample Explorer
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("##### ❌ Before: Uncleaned Raw Sample (First 8 Rows)")
        # Display raw sample as a data frame with string conversions to keep leading spaces visible
        raw_sample = raw_df.head(8).copy()
        # Add visual highlighting to help spot trailing space issues
        st.dataframe(raw_sample, use_container_width=True)
        
    with col_t2:
        st.markdown("#####  Before: Sanitized Clean Sample (First 8 Rows)")
        clean_sample = clean_df.head(8).copy()
        st.dataframe(clean_sample, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. Before/After Visualizations
    st.markdown(
        clean_html("""
        <div class="section-container">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #ffffff;">Data Distribution Audit Chart</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">
                This chart verifies that dropping nulls and sanitizing types did not distort the dataset's overall statistical properties.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    # Let's plot distribution comparison: Unemployment rate distribution (raw vs clean)
    # Filter out NaNs from raw for plotting
    raw_rate_clean = raw_df[raw_df.iloc[:, 3].notnull()].iloc[:, 3]
    clean_rate = clean_df['Unemployment_Rate']
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=raw_rate_clean,
        name='Raw Rates (excl. Nulls)',
        marker_color='rgba(168, 85, 247, 0.4)',
        nbinsx=30,
        hovertemplate='Unemployment Rate: %{x}%<br>Count: %{y}<extra></extra>'
    ))
    fig.add_trace(go.Histogram(
        x=clean_rate,
        name='Cleaned Rates',
        marker_color='rgba(99, 102, 241, 0.7)',
        nbinsx=30,
        hovertemplate='Unemployment Rate: %{x}%<br>Count: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='overlay',
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit, Inter, sans-serif", color="#e2e8f0"),
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis_title="Unemployment Rate (%)",
        yaxis_title="Count of Records",
        legend=dict(x=0.8, y=0.9, bgcolor="rgba(15,23,42,0.8)")
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(
        clean_html("""
        <div class="section-container" style="margin-top: 1rem;">
            <h5 style="margin: 0; color: #ffffff;">Pipeline Execution Flow</h5>
            <p style="margin: 0.5rem 0 0 0; color: #94a3b8; font-size: 0.85rem; line-height: 1.5;">
                1. <b>File Ingestion:</b> Read CSV raw headers -> 2. <b>Header Trim:</b> Strip trailing/leading spaces from headers -> 
                3. <b>Empty Row Truncation:</b> Drop fully null rows -> 4. <b>Categorical Trim:</b> Strip trailing spaces in text fields -> 
                5. <b>DateTime Conversion:</b> Parse Date text from format <code>DD-MM-YYYY</code> to ISO strings -> 
                6. <b>Numeric Cast:</b> Force numeric data types (integer for Employed, float for rate/participation) -> 
                7. <b>Geographic Enrichment:</b> Left-join longitude, latitude, and region boundaries from state references.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )
