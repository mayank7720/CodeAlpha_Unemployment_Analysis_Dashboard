# Unemployment Analysis Dashboard (India, 2019-2020)

A production-ready, modular Streamlit analytics dashboard designed with premium aesthetics inspired by Power BI, Tableau, and Stripe Analytics. The dashboard offers key insights into labor force dynamics, regional disparities, and the socioeconomic shock of the COVID-19 pandemic.

## 📂 Project Structure

The project follows a modular, clean, and scalable structure:

```
D:\Unemployment Analysis Dashboard\
├── data/                         # Ingested datasets
│   ├── raw/                      # Original CSV files (downloaded)
│   └── processed/                # Cleaned/processed datasets (cached pipelines)
├── assets/                       # Custom styles and CSS overrides
│   └── styles.css                # Premium styling theme overrides for Streamlit
├── notebooks/                    # Jupyter notebooks for initial EDA
│   └── EDA.ipynb                 # EDA and observations
├── reports/                      # Static summaries and automatic report scripts
│   ├── generate_report.py        # CLI script to generate a statistical summary
│   └── summary_report.md         # Generated markdown report (auto-created)
├── utils/                        # Data processing & loader helpers
│   ├── __init__.py
│   └── data_loader.py            # Ingestion, cleaning, and mock/live toggle
├── components/                   # Modular dashboard UI sections
│   ├── __init__.py
│   ├── sidebar.py                # Global sidebar filters
│   ├── kpi_cards.py              # Custom styled floating KPI summaries
│   └── tabs/                     # Dashboard tab components
│       ├── __init__.py
│       ├── overview.py           # Executive Summary & state rankings
│       ├── trends.py             # Rolling averages, seasonality, and decomposition subplots
│       ├── rural_urban.py        # Rural vs. Urban comparison splits
│       ├── geo_map.py            # Geographic bubble maps and boundary choropleths
│       ├── eda.py                # Exploratory Data Analysis & correlation matrix
│       ├── covid_analysis.py     # COVID-19 pandemic shock area/slope comparison charts
│       ├── insights_report.py    # Automated executive briefings & Markdown downloads
│       ├── policy_recommendations.py # Strategic matrices (MSME, youth, women, regional)
│       └── data_cleaning.py      # Preprocessing diagnostic metrics & sample audits
├── visualizations/               # Plotly charting helpers
│   ├── __init__.py
│   ├── charts.py                 # Core chart styles & regression slope formulas
│   └── maps.py                   # Mapbox bubble maps and boundary choropleth fills
├── app.py                        # Streamlit main entrypoint
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation (this file)
```

---

## 🎨 Design Aesthetics & Advanced Analytics

1. **Stripe-like Glassmorphism Cards:** The metric cards use custom HTML structure combined with CSS backdrop blur (`backdrop-filter`) and smooth transformations (`translateY`) upon hover to deliver a premium feel.
2. **Dynamic Dark Theme:** Colors are customized to use Slate and Midnight Blue combinations (`#0b0f19`, `#151c2c`, `#6366f1`) with bright accents, ensuring visual contrast and keyframe fade-in animations on mount.
3. **Slope Skill (OLS Regression):** Under the *Temporal Trends & Slopes* tab, users can toggle a mathematical trend line which calculates the Ordinary Least Squares (OLS) regression line on the fly, outputting trend direction (↗/↘) and rate of change per month directly on the chart.
4. **Interactive Mapbox Choropleths & Bubbles:** State boundaries are mapped using boundary coordinates (loaded from [india_states.geojson](file:///D:/Unemployment%20Analysis%20Dashboard/data/processed/india_states.geojson)) and coordinate bubbles, layered on dark Mapbox themes with play/pause timeline sliders.
5. **Time-Series & Seasonal Decomposition:** Computes SMAs and EMAs with rolling sliders, quarterly aggregations, and subplots decomposing observed series into trend and residual components.
6. **Automated Insights & Policy Briefings:** Synthesizes anomalies, baseline shifts, and region-specific interventions into a downloadable executive briefing.
7. **Caching & Optimization:** Streamlit's `@st.cache_data` is implemented to ensure data processing pipeline computations do not repeat, ensuring instant responsiveness when altering filters.

---

## ⚙️ Installation & Running the Dashboard

### Prerequisites
- Python 3.9 or higher

### 1. Install Dependencies
Navigate to the root directory and install requirements:
```bash
pip install -r requirements.txt
```

### 2. Generate the Statistical Report (Optional CLI)
To compile raw stats and generate a fresh statistical markdown report:
```bash
python reports/generate_report.py
```
This generates a summary document inside the `reports/` folder.

### 3. Run the Streamlit Dashboard
Launch the main application:
```bash
streamlit run app.py
```
This automatically opens the dashboard in your default browser at `http://localhost:8501`.

---

## 🔒 Data Preprocessing Pipeline & Verification

The dashboard is fully connected to the live datasets. During loading, the raw files are run through a robust cleaning pipeline:
1. **Missing Value Treatment:** Detects and drops empty padding rows (e.g. 28 blank rows in the area dataset).
2. **Deduplication:** Identifies and clears duplicate records from ingestion.
3. **Data Type Alignment:** Standardizes column formatting and casts metric columns to explicit numeric types (e.g. converting float representations of employment to integers).
4. **Whitespace & String Standardization:** Standardizes state names, areas, and frequency values by stripping leading/trailing whitespace and mapping values (e.g., `' M'` and `' Monthly'` are standardized to `'Monthly'`).
5. **Geographical Enrichment:** Automatically maps latitude/longitude and geographic region tags from the state dataset to the area dataset, injecting coords manually for Chandigarh.
6. **Caching:** Leverages Streamlit caching to prevent pipeline re-computation, keeping dashboard responses fast.

---

## 👨‍💻 Author

**Mayank Raj**
- **GitHub:** [@mayank7720](https://github.com/mayank7720)
- **LinkedIn:** [Mayank Raj](https://www.linkedin.com/in/mayank-raj-221522381/)


