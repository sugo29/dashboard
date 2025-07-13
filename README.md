# Dashboard Project

This project contains two fully functional Streamlit dashboards for data analysis.

## Dashboards

### 1. Kitchen Dashboard (`kitchen_dashboard.py`)
- **Purpose**: Kitchen-level P&L analysis dashboard
- **Data Source**: `dummy_data.xlsx`
- **Run Command**: Use VS Code task "Run Kitchen Dashboard" or `streamlit run kitchen_dashboard.py`

### 2. Variance Dashboard (`vardashboard.py`)
- **Purpose**: Variance analysis with dynamic matrix views
- **Data Source**: `dummy_data.xlsx`
- **Run Command**: Use VS Code task "Run Variance Dashboard" or `run_vardashboard.bat`
- **Features**:
  - Variance filtering (High, Medium, Low, Custom ranges)
  - Dynamic matrix configuration (Revenue Cohort, Store, Zone, CM Cohort, EBITDA Category)
  - Toggle between Count and Percentage views
  - Interactive heatmaps and statistical analysis

## Quick Start

1. **Using VS Code Tasks** (Recommended):
   - Press `Ctrl+Shift+P`
   - Type "Tasks: Run Task"
   - Select either "Run Kitchen Dashboard" or "Run Variance Dashboard"

2. **Using Batch File**:
   - Double-click `run_vardashboard.bat` for the variance dashboard

3. **Manual Command**:
   ```bash
   streamlit run kitchen_dashboard.py
   # or
   streamlit run vardashboard.py
   ```

## Dependencies
All required packages are listed in `requirements.txt` and should be installed in the `.venv` virtual environment.

## Data
Both dashboards use `dummy_data.xlsx` as the data source.

## Access
- **Kitchen Dashboard**: http://localhost:8501
- **Variance Dashboard**: http://localhost:8502 (if running both simultaneously)

Both dashboards are optimized for wide-screen viewing and feature responsive, interactive visualizations.
