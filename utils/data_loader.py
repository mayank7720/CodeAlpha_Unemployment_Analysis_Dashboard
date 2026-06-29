import pandas as pd
import streamlit as st
import os

# Production-ready data loading and preprocessing pipeline for the Unemployment datasets

@st.cache_data
def load_state_data():
    """
    Ingests and preprocesses data/raw/Unemployment_Rate_upto_11_2020.csv.
    Covers Jan 2020 to Oct 2020 at the state level with coordinates.
    """
    file_path = 'data/raw/Unemployment_Rate_upto_11_2020.csv'
    if not os.path.exists(file_path):
        # Fallback to local data directory if run from reports folder or notebooks
        file_path = '../data/raw/Unemployment_Rate_upto_11_2020.csv'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Raw state dataset not found at {file_path}")

    # Ingest CSV
    df = pd.read_csv(file_path)
    
    # 1. Clean Column Names: Strip whitespace
    df.columns = df.columns.str.strip()
    
    # 2. Drop duplicates and fully null rows
    df = df.dropna(how='all')
    df = df.drop_duplicates()
    
    # 3. Clean Categorical Data: Strip whitespaces
    for col in ['Region', 'Frequency', 'Region.1']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    # 4. Standardize Date column
    df['Date'] = df['Date'].str.strip()
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Date_iso'] = df['Date_parsed'].dt.strftime('%Y-%m-%d')
    
    # 5. Rename Columns to standardize structure
    df = df.rename(columns={
        'Region.1': 'Geographic_Region',
        'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
        'Estimated Employed': 'Employed',
        'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate'
    })
    
    # 6. Ensure Correct Data Types
    df['Unemployment_Rate'] = df['Unemployment_Rate'].astype(float)
    df['Labour_Participation_Rate'] = df['Labour_Participation_Rate'].astype(float)
    df['Employed'] = df['Employed'].astype(int)
    df['longitude'] = df['longitude'].astype(float)
    df['latitude'] = df['latitude'].astype(float)
    df['Frequency'] = 'Monthly' # Standardize frequency text
    
    # Select clean columns
    clean_cols = [
        'Region', 'Date_iso', 'Frequency', 'Unemployment_Rate', 
        'Employed', 'Labour_Participation_Rate', 'Geographic_Region', 
        'longitude', 'latitude'
    ]
    return df[clean_cols].sort_values(by=['Date_iso', 'Region']).reset_index(drop=True)


@st.cache_data
def load_area_data():
    """
    Ingests and preprocesses data/raw/Unemployment_in_India.csv.
    Covers May 2019 to June 2020 and includes Rural/Urban split.
    Enriches with coordinates and geographic region mapping.
    """
    file_path = 'data/raw/Unemployment_in_India.csv'
    if not os.path.exists(file_path):
        # Fallback to local data directory
        file_path = '../data/raw/Unemployment_in_India.csv'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Raw area dataset not found at {file_path}")

    # Ingest CSV
    df = pd.read_csv(file_path)
    
    # 1. Clean Column Names: Strip whitespace
    df.columns = df.columns.str.strip()
    
    # 2. Drop duplicates and fully null rows (this resolves the 28 missing rows & 27 duplicate nulls)
    df = df.dropna(how='all')
    df = df.drop_duplicates()
    
    # 3. Clean Categorical Data: Strip whitespaces
    for col in ['Region', 'Frequency', 'Area']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    # 4. Standardize Date column
    df['Date'] = df['Date'].str.strip()
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Date_iso'] = df['Date_parsed'].dt.strftime('%Y-%m-%d')
    
    # 5. Rename Columns to standardize structure
    df = df.rename(columns={
        'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
        'Estimated Employed': 'Employed',
        'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate'
    })
    
    # 6. Ensure Correct Data Types
    df['Unemployment_Rate'] = df['Unemployment_Rate'].astype(float)
    df['Labour_Participation_Rate'] = df['Labour_Participation_Rate'].astype(float)
    df['Employed'] = df['Employed'].astype(int)
    df['Frequency'] = 'Monthly' # Standardize frequency text
    
    # 7. Enrichment: Map Geographic Region, Longitude, and Latitude from State data
    # Load state data to extract the mapping
    df_state_clean = load_state_data()
    coords_map = df_state_clean.groupby('Region')[['Geographic_Region', 'longitude', 'latitude']].first().to_dict(orient='index')
    
    # Chandigarh is only in df_area, so map manually
    coords_map['Chandigarh'] = {
        'Geographic_Region': 'North',
        'longitude': 76.7794,
        'latitude': 30.7333
    }
    
    def enrich_region_info(row):
        region = row['Region']
        info = coords_map.get(region, {'Geographic_Region': 'Unknown', 'longitude': 0.0, 'latitude': 0.0})
        return pd.Series([info['Geographic_Region'], info['longitude'], info['latitude']])
        
    df[['Geographic_Region', 'longitude', 'latitude']] = df.apply(enrich_region_info, axis=1)
    
    # Select clean columns
    clean_cols = [
        'Region', 'Date_iso', 'Frequency', 'Unemployment_Rate', 
        'Employed', 'Labour_Participation_Rate', 'Area', 
        'Geographic_Region', 'longitude', 'latitude'
    ]
    return df[clean_cols].sort_values(by=['Date_iso', 'Region', 'Area']).reset_index(drop=True)


@st.cache_data
def load_raw_state_data():
    """
    Ingests raw state dataset unmodified.
    """
    file_path = 'data/raw/Unemployment_Rate_upto_11_2020.csv'
    if not os.path.exists(file_path):
        file_path = '../data/raw/Unemployment_Rate_upto_11_2020.csv'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Raw state dataset not found at {file_path}")
    return pd.read_csv(file_path)


@st.cache_data
def load_raw_area_data():
    """
    Ingests raw area dataset unmodified.
    """
    file_path = 'data/raw/Unemployment_in_India.csv'
    if not os.path.exists(file_path):
        file_path = '../data/raw/Unemployment_in_India.csv'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Raw area dataset not found at {file_path}")
    return pd.read_csv(file_path)


def clean_html(html_str):
    """
    Strips all leading and trailing whitespace from each line of an HTML string.
    This prevents the Streamlit Markdown parser from treating indented HTML tags
    as markdown code blocks.
    """
    return "\n".join([line.strip() for line in html_str.split("\n") if line.strip()])


