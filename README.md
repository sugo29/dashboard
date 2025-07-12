# Variance Level P&L Dashboard

A comprehensive Streamlit dashboard for analyzing kitchen variance performance across revenue cohorts.

## 🎯 Dashboard Overview

This dashboard provides two main analytical views:

### 📈 Sub-Dashboard 1: Average Variance % by Revenue Cohort
- Groups kitchens by revenue quartiles (Q1-Q4)
- Calculates average variance percentage for each cohort
- Answers: **"Are high-revenue kitchens more efficient or more wasteful?"**
- Visual insights through bar charts and box plots

### 🏪 Sub-Dashboard 2: Store Count by Variance Bucket
- Creates variance buckets: Low (0-5%), Medium (5-15%), High (15%+)
- Shows distribution of kitchens across variance levels
- Cross-analysis with revenue cohorts and time trends
- Answers: **"How many kitchens fall into each efficiency category?"**

## 🛠️ Technical Approach

### Step 1: Data Processing
1. **Load Excel Dataset**: Read `dashborad_data.xlsx` using pandas
2. **Revenue Cohorts**: Create quartile-based revenue groups
3. **Variance Buckets**: Categorize variance into Low/Medium/High bands
4. **Data Validation**: Handle missing values and data type conversions

### Step 2: Interactive Analysis
1. **Column Mapping**: Dynamic column selection for flexibility
2. **Filtering**: Date range and other filters for focused analysis
3. **Real-time Updates**: Interactive visualizations with Plotly

### Step 3: Visualization Strategy
1. **Bar Charts**: Average variance by cohort comparison
2. **Pie Charts**: Overall distribution visualization
3. **Heatmaps**: Cross-tabulation analysis
4. **Box Plots**: Variance distribution insights
5. **Trend Lines**: Time-series analysis (if date data available)

## 🚀 Quick Start

### Prerequisites
- **Python 3.9.13** installed on your system
- Your dataset file `dashborad_data.xlsx` in the project directory

### Option 1: Automated Setup with Virtual Environment (Recommended)
```bash
# For Command Prompt/Batch
./setup_venv.bat

# For PowerShell (if you prefer)
./setup_venv.ps1
```

### Option 2: Manual Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv_dashboard

# Activate virtual environment
# On Windows Command Prompt:
venv_dashboard\Scripts\activate.bat
# On Windows PowerShell:
.\venv_dashboard\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run variance_dashboard.py
```

### Option 3: Quick Run (if environment already set up)
```bash
# Double-click this file or run in Command Prompt
./run_dashboard_venv.bat
```

### Option 4: Global Installation (not recommended)
```bash
# Install dependencies globally
pip install -r requirements.txt

# Explore your dataset structure
python explore_data.py

# Run the dashboard
streamlit run variance_dashboard.py
```

## 📊 Expected Data Structure

Your `dashborad_data.xlsx` should contain columns for:

| Column Type | Examples | Required |
|-------------|----------|----------|
| **Revenue** | `Revenue`, `Sales`, `Monthly_Revenue` | ✅ Yes |
| **Variance** | `Variance_%`, `P&L_Variance`, `Budget_Diff` | ✅ Yes |
| **Store ID** | `Kitchen_ID`, `Store_Code`, `Location` | ⚠️ Recommended |
| **Date** | `Month`, `Date`, `Period` | ⚪ Optional |

## 📈 Key Features

### Interactive Elements
- **Column Mapping**: Select your data columns dynamically
- **Date Filtering**: Focus on specific time periods
- **Data Preview**: Examine raw data structure
- **Export Options**: Download insights and charts

### Business Insights
- **Efficiency Analysis**: Identify top and bottom performers
- **Revenue Correlation**: Understand scale vs efficiency relationship
- **Trend Detection**: Seasonal patterns and improvement tracking
- **Actionable Recommendations**: Data-driven next steps

### Visual Analytics
- **Multi-dimensional Analysis**: Revenue × Variance × Time
- **Color-coded Performance**: Intuitive red/green efficiency indicators
- **Statistical Summaries**: Mean, standard deviation, quartiles
- **Comparative Views**: Side-by-side cohort comparison

## 🔍 Business Questions Answered

1. **Efficiency vs Scale**: Do larger revenue kitchens operate more efficiently?
2. **Performance Distribution**: What percentage of kitchens are underperforming?
3. **Improvement Targets**: Which kitchens need immediate attention?
4. **Best Practices**: What can top performers teach others?
5. **Trend Analysis**: Are we improving or declining over time?

## 💡 Usage Tips

### Data Preparation
- Ensure variance data is in percentage format (e.g., 5.2 for 5.2%)
- Include unique identifiers for each kitchen/store
- Date columns should be in standard format (YYYY-MM-DD)

### Analysis Workflow
1. **Start with Overview**: Check overall distribution patterns
2. **Drill Down**: Focus on high-variance segments
3. **Compare Cohorts**: Analyze revenue vs efficiency relationship
4. **Time Analysis**: Look for seasonal or trend patterns
5. **Action Planning**: Use insights for operational improvements

### Customization
The dashboard automatically detects potential column mappings but allows manual override:
- Revenue columns: Look for keywords like "revenue", "sales", "income"
- Variance columns: Look for "variance", "diff", "%", "percent"
- Date columns: Look for "date", "month", "time", "period"

## 🎨 Dashboard Layout

```
┌─────────────────────────────────────────────────┐
│                MAIN HEADER                      │
├─────────────┬───────────────────────────────────┤
│  SIDEBAR    │        SUB-DASHBOARD 1            │
│             │    Revenue Cohort Analysis        │
│ - Column    ├───────────────────────────────────┤
│   Mapping   │        SUB-DASHBOARD 2            │
│ - Filters   │    Variance Bucket Analysis       │
│ - Data      ├───────────────────────────────────┤
│   Preview   │      BUSINESS INSIGHTS            │
│             │    & Recommendations              │
└─────────────┴───────────────────────────────────┘
```

## 📋 File Structure

```
dashboard/
├── variance_dashboard.py       # Main dashboard application
├── explore_data.py            # Dataset exploration utility
├── requirements.txt           # Python dependencies (compatible with 3.9.13)
├── setup_venv.bat            # Automated virtual environment setup (Batch)
├── setup_venv.ps1            # Automated virtual environment setup (PowerShell)
├── run_dashboard_venv.bat    # Quick start with virtual environment
├── run_dashboard.bat         # Legacy run script (global installation)
├── dashborad_data.xlsx       # Your dataset
├── venv_dashboard/           # Virtual environment folder (created after setup)
└── README.md                 # This documentation
```

## 🤝 Support

If you encounter issues:
1. Run `python explore_data.py` to check your data structure
2. Ensure all required columns are present
3. Check that the Excel file is in the correct directory
4. Verify Python and pip are properly installed

## 🎯 Next Steps

After running the dashboard:
1. **Identify Patterns**: Look for correlation between revenue and efficiency
2. **Flag Outliers**: Focus on high-variance, high-revenue kitchens
3. **Benchmark Best**: Study practices of efficient kitchens
4. **Track Progress**: Monitor improvements over time
5. **Scale Solutions**: Apply learnings across kitchen network
