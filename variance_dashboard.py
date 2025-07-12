import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page config
st.set_page_config(
    page_title="Variance-Level P&L Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling - cleaner and more corporate
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Global styling - clean, corporate look */
    .stApp {
        font-family: 'Roboto', sans-serif;
        background-color: #f7f9fc;
        color: #000000;
    }
    
    /* Force all text to be black */
    *, p, span, div, h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #000000 !important;
    }
    
    /* Clean container styling */
    .main .block-container {
        padding: 1rem;
        max-width: 1400px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Professional header styling */
    .dashboard-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #000000;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e0e4e8;
    }
    
    .dashboard-subtitle {
        font-size: 1rem;
        color: #000000;
        margin-bottom: 2rem;
    }
    
    /* Professional section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 500;
        color: #000000;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e0e4e8;
    }
    
    /* Clean card styling */
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #e0e4e8;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .metric-number {
        font-size: 1.8rem;
        font-weight: 600;
        color: #000000;
        margin-bottom: 0.3rem;
    }
    
    .metric-label {
        color: #000000;
        font-size: 0.85rem;
        font-weight: 400;
    }
    
    /* Sub-header styling */
    .sub-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #000000;
        margin: 2rem 0 1rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
    }
    
    /* Insight card styling */
    .insight-card {
        background: white;
        border: 1px solid #e0e4e8;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .insight-card.success {
        border-left-color: #10b981;
    }
    
    .insight-title {
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        color: #000000;
    }
    
    .insight-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #000000;
    }
    
    /* Success and warning messages */
    .success-message {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: #065f46;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
        font-weight: 500;
    }
    
    .warning-message {
        background: linear-gradient(135deg, #fef3c7, #fed7aa);
        color: #92400e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #f59e0b;
        font-weight: 500;
    }
    
    /* Clean table styling */
    .dataframe {
        border: 1px solid #e0e4e8;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe th {
        background-color: #f1f4f8;
        color: #000000;
        font-weight: 500;
        text-align: left;
        padding: 12px;
    }
    
    .dataframe td {
        padding: 10px 12px;
        border-top: 1px solid #e0e4e8;
        color: #000000;
    }
    
    /* Clean tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f1f4f8;
        border-radius: 4px;
        padding: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 4px;
        color: #000000;
        font-weight: 400;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #000000 !important;
        font-weight: 500;
    }
    
    /* Clean sidebar styling */
    .css-1d391kg, .css-163ttbj, .css-1r6slb0 {
        background-color: white;
        border-right: 1px solid #e0e4e8;
    }
    
    /* Filter styling - similar to reference image */
    .filter-container {
        background-color: #fbfcfe;
        border: 1px solid #e0e4e8;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .filter-header {
        font-size: 1rem;
        font-weight: 500;
        color: #000000;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
    }
    
    /* Checkbox styling similar to reference */
    .stCheckbox {
        padding: 0.2rem 0;
    }
    
    .stCheckbox label p {
        font-size: 0.9rem;
        color: #000000;
    }
    
    /* Table container like reference */
    .table-container {
        border: 1px solid #e0e4e8;
        border-radius: 8px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .table-header {
        background-color: #f1f4f8;
        padding: 0.8rem 1rem;
        font-weight: 500;
        color: #000000;
        border-bottom: 1px solid #e0e4e8;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the dataset"""
    try:
        # Load the actual Excel file (with the typo in filename)
        df = pd.read_excel('dashborad_data.xlsx')
        st.success(f"✅ Successfully loaded data with {len(df)} rows and {len(df.columns)} columns")
        return df
    except FileNotFoundError:
        st.error("❌ File 'dashborad_data.xlsx' not found in the current directory!")
        st.info("📁 Please ensure your Excel file is named 'dashborad_data.xlsx' and is in the same folder as this script.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading Excel file: {e}")
        st.info("Please check that your Excel file is not corrupted and contains valid data.")
        return None

def get_numeric_columns(df):
    """Get columns that are numeric or can be converted to numeric"""
    numeric_cols = []
    for col in df.columns:
        try:
            numeric_count = pd.to_numeric(df[col], errors='coerce').count()
            total_count = len(df[col])
            if numeric_count / total_count > 0.8:  # More than 80% can be converted
                numeric_cols.append(col)
        except:
            continue
    return numeric_cols

def get_date_columns(df):
    """Identify potential date columns"""
    date_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['date', 'month', 'time', 'period']):
            date_cols.append(col)
    return date_cols

def create_revenue_cohorts(df, revenue_col):
    """Create revenue cohorts based on specified ranges"""
    if revenue_col not in df.columns:
        st.error(f"Column '{revenue_col}' not found in dataset")
        return df
    
    # Convert revenue column to numeric
    try:
        df_copy = df.copy()
        df_copy[revenue_col] = pd.to_numeric(df_copy[revenue_col], errors='coerce')
        df_copy = df_copy.dropna(subset=[revenue_col])
        
        if len(df_copy) == 0:
            st.error(f"No valid numeric data found in column '{revenue_col}'.")
            return df
            
        df = df_copy
    except Exception as e:
        st.error(f"Error converting '{revenue_col}' to numeric: {e}")
        return df
    
    # Create revenue categories matching the requested ranges (in lacs)
    def assign_revenue_category(revenue):
        if revenue < 15:
            return "Below INR 15 lacs"
        elif revenue < 25:
            return "INR 15 to 25 lacs"
        elif revenue < 35:
            return "INR 25 to 35 lacs"
        elif revenue < 45:
            return "INR 35 to 45 lacs"
        else:
            return "Above INR 45 lacs"
    
    df['Revenue_Category'] = df[revenue_col].apply(assign_revenue_category)
    return df

def create_variance_buckets(df, variance_col):
    """Create variance buckets based on specified ranges"""
    if variance_col not in df.columns:
        st.error(f"Column '{variance_col}' not found in dataset")
        return df
    
    # Convert variance column to numeric, handling non-numeric values
    try:
        df_copy = df.copy()
        df_copy[variance_col] = pd.to_numeric(df_copy[variance_col], errors='coerce')
        df_copy = df_copy.dropna(subset=[variance_col])
        
        if len(df_copy) == 0:
            st.error(f"No valid numeric data found in column '{variance_col}'.")
            return df
            
        df = df_copy
    except Exception as e:
        st.error(f"Error converting '{variance_col}' to numeric: {e}")
        return df
    
    # Create variance buckets matching the requested ranges
    def assign_variance_bucket(variance):
        abs_variance = abs(variance)
        if abs_variance < 2:
            return "Var < 2%"
        elif abs_variance < 3:
            return "Var 2% to 3%"
        elif abs_variance < 5:
            return "Var 3% to 5%"
        else:
            return "Var > 5%"
    
    df['Variance_Bucket'] = df[variance_col].apply(assign_variance_bucket)
    return df

def sub_dashboard_1(df, revenue_col, variance_col):
    """Sub-dashboard 1: Avg Variance % by Revenue Category"""
    st.markdown("## VARIANCE BY REVENUE CATEGORY")
    st.markdown("The table below summarizes the average variance % of kitchens under revenue categories")
    
    if revenue_col not in df.columns or variance_col not in df.columns:
        st.error("Required columns not found in dataset")
        return
    
    # Process data
    df_processed = create_revenue_cohorts(df, revenue_col)
    
    # Check if Revenue_Category column was created successfully
    if 'Revenue_Category' not in df_processed.columns:
        st.error("Could not create revenue categories. Please check your revenue data.")
        return
    
    # Convert variance column to numeric
    df_processed[variance_col] = pd.to_numeric(df_processed[variance_col], errors='coerce')
    
    # Calculate average variance by revenue category
    avg_variance_by_category = df_processed.groupby('Revenue_Category')[variance_col].mean().reset_index()
    
    # Order revenue categories
    revenue_order = [
        "Below INR 15 lacs", 
        "INR 15 to 25 lacs", 
        "INR 25 to 35 lacs", 
        "INR 35 to 45 lacs", 
        "Above INR 45 lacs"
    ]
    
    # Create the data for the summary table
    summary_data = {}
    
    # Process date column if available to get months
    if 'Month' in df_processed.columns:
        # Group by revenue category and month
        months = sorted(df_processed['Month'].unique())
        
        for month in months:
            month_data = df_processed[df_processed['Month'] == month]
            month_avgs = []
            
            for category in revenue_order:
                cat_data = month_data[month_data['Revenue_Category'] == category]
                if len(cat_data) > 0:
                    avg_var = cat_data[variance_col].mean()
                    month_avgs.append(f"{avg_var:.1f}%")
                else:
                    month_avgs.append("N/A")
            
            summary_data[month] = month_avgs
    else:
        # Just show overall averages
        overall_data = {}
        overall_data['Overall'] = []
        
        for category in revenue_order:
            cat_data = df_processed[df_processed['Revenue_Category'] == category]
            if len(cat_data) > 0:
                avg_var = cat_data[variance_col].mean()
                overall_data['Overall'].append(f"{avg_var:.1f}%")
            else:
                overall_data['Overall'].append("N/A")
        
        summary_data = overall_data
    
    # Create DataFrame for display
    summary_df = pd.DataFrame(summary_data, index=revenue_order)
    summary_df.index.name = "Revenue category"
    
    # Add grand total row
    grand_totals = []
    for col in summary_df.columns:
        values = [float(x.strip('%')) for x in summary_df[col].tolist() if x != "N/A"]
        if values:
            grand_totals.append(f"{sum(values)/len(values):.1f}%")
        else:
            grand_totals.append("N/A")
            
    summary_df.loc["Grand total"] = grand_totals
    
    # Display the styled table
    st.markdown("### Average Variance % by Revenue Category")
    st.dataframe(summary_df, use_container_width=True)

def sub_dashboard_2(df, revenue_col, variance_col, date_col=None, store_col='STORE'):
    """Sub-dashboard 2: Store Count by Variance Bucket and Revenue Category"""
    st.markdown("## STORE COUNT BY VARIANCE AND REVENUE")
    st.markdown("The table below shows the count of kitchen stores by variance buckets and revenue categories")
    
    if revenue_col not in df.columns or variance_col not in df.columns:
        st.error("Required columns not found in dataset")
        return
    
    # Process data
    df_processed = create_revenue_cohorts(df, revenue_col)
    
    # Check if Revenue_Category column was created successfully
    if 'Revenue_Category' not in df_processed.columns:
        st.error("Could not create revenue categories. Please check your revenue data.")
        return
    
    df_processed = create_variance_buckets(df_processed, variance_col)
    
    # Check if Variance_Bucket column was created successfully
    if 'Variance_Bucket' not in df_processed.columns:
        st.error("Could not create variance buckets. Please check your variance data.")
        return
    
    # Process date column to extract months
    has_date = False
    if date_col and date_col in df_processed.columns:
        try:
            # Try to convert to datetime
            df_processed[date_col] = pd.to_datetime(df_processed[date_col], errors='coerce')
            # Extract month
            df_processed['Month'] = df_processed[date_col].dt.strftime('%Y-%m')
            has_date = True
        except:
            st.warning(f"Could not convert '{date_col}' to date format.")
    
    # Add a dummy column for counting
    df_processed['Count'] = 1
    
    # Revenue categories order
    revenue_order = [
        "Below INR 15 lacs", 
        "INR 15 to 25 lacs", 
        "INR 25 to 35 lacs", 
        "INR 35 to 45 lacs", 
        "Above INR 45 lacs"
    ]
    
    # Create store count table
    st.markdown("### Count of Stores by Revenue Category")
    
    if has_date:
        # Group by month, revenue category, and variance bucket
        store_counts = pd.pivot_table(
            df_processed,
            values='Count',
            index=['Month', 'Revenue_Category'],
            columns=['Variance_Bucket'],
            aggfunc='sum',
            fill_value=0
        )
        
        # Format and display the table
        st.dataframe(store_counts.reset_index(), use_container_width=True)
        
        # Also show a simplified view with just month and revenue categories
        st.markdown("### Monthly Store Count by Revenue Category")
        monthly_counts = pd.pivot_table(
            df_processed,
            values='Count',
            index=['Month'],
            columns=['Revenue_Category'],
            aggfunc='sum',
            fill_value=0
        )
        
        st.dataframe(monthly_counts.reset_index(), use_container_width=True)
    else:
        # Simple pivot without month
        store_counts = pd.pivot_table(
            df_processed,
            values='Count',
            index=['Revenue_Category'],
            columns=['Variance_Bucket'],
            aggfunc='sum',
            fill_value=0
        )
        
        st.dataframe(store_counts.reset_index(), use_container_width=True)

def main():
    """Main function to run the dashboard"""
    # Professional header
    st.markdown('<div class="dashboard-header">Variance-Level P&L Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Analyze wastage (variance) and how it affects performance</div>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("❌ Failed to load data. Please check the following:")
        st.markdown("""
        1. **File exists**: Ensure 'dashborad_data.xlsx' is in the current directory
        2. **File format**: Make sure it's a valid Excel file (.xlsx)
        3. **File permissions**: Check that the file is not open in another application
        4. **File content**: Ensure the Excel file contains data
        """)
        return
    
    # Show data preview
    with st.expander("📊 Data Preview", expanded=False):
        st.write(f"**Dataset Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        st.write("**Column Names:**", list(df.columns))
        st.write("**First 5 rows:**")
        st.dataframe(df.head(), use_container_width=True)
    
    # Sidebar for column selection
    st.sidebar.header("Column Selection")
    
    # Get numeric columns
    numeric_cols = get_numeric_columns(df)
    date_cols = get_date_columns(df)
    
    # Column selection
    revenue_col = st.sidebar.selectbox(
        "Select NET_REVENUE Column",
        options=numeric_cols,
        help="Column containing revenue data"
    )
    
    variance_col = st.sidebar.selectbox(
        "Select VARIANCE Column",
        options=numeric_cols,
        help="Column containing variance percentage data"
    )
    
    store_col = st.sidebar.selectbox(
        "Select STORE Column",
        options=df.columns,
        help="Column containing store identifiers"
    )
    
    date_col = None
    if date_cols:
        date_col = st.sidebar.selectbox(
            "Select Date Column",
            options=["None"] + date_cols,
            help="Column containing date information"
        )
        if date_col == "None":
            date_col = None
    
    # Variance filters
    st.sidebar.header("Variance Filters")
    
    var_filters = {
        "var_below_2": st.sidebar.checkbox("Var < 2%", value=True),
        "var_2_to_3": st.sidebar.checkbox("Var 2% to 3%", value=True),
        "var_3_to_5": st.sidebar.checkbox("Var 3% to 5%", value=True),
        "var_above_5": st.sidebar.checkbox("Var > 5%", value=True)
    }
    
    # Check if required columns are selected
    if revenue_col and variance_col:
        # Main content - tabs for the two sub-dashboards
        tab1, tab2 = st.tabs(["Average Variance by Revenue", "Store Count Analysis"])
        
        with tab1:
            sub_dashboard_1(df, revenue_col, variance_col)
        
        with tab2:
            sub_dashboard_2(df, revenue_col, variance_col, date_col, store_col)
        
        # Enhanced footer with professional styling
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #f8fafc, #e2e8f0); border-radius: 16px; border: 1px solid #e2e8f0;">
            <h4 style="color: #000000; margin-bottom: 1rem;">📊 Analysis Summary</h4>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
                <div style="text-align: center;">
                    <strong style="color: #000000;">Variance Definition</strong><br>
                    <span style="color: #000000; font-size: 0.9rem;">Food material wastage percentage</span>
                </div>
                <div style="text-align: center;">
                    <strong style="color: #000000;">Revenue Cohorts</strong><br>
                    <span style="color: #000000; font-size: 0.9rem;">Quartile-based categorization</span>
                </div>
                <div style="text-align: center;">
                    <strong style="color: #000000;">Variance Buckets</strong><br>
                    <span style="color: #000000; font-size: 0.9rem;">Low (<2%), Medium (2-5%), High (>5%)</span>
                </div>
            </div>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #cbd5e1; color: #000000; font-style: italic;">
                Built for optimizing cloud kitchen operations and reducing food wastage
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Enhanced error state with actionable guidance
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #fef3c7, #fed7aa); border-radius: 16px; margin: 2rem 0;">
            <h3 style="color: #000000; margin-bottom: 1rem;">⚠️ Configuration Required</h3>
            <p style="color: #000000; margin-bottom: 1.5rem;">Please select valid revenue and variance columns to begin your analysis.</p>
            <div style="background: rgba(255, 255, 255, 0.7); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <strong style="color: #000000;">Quick Guide:</strong><br>
                <span style="color: #000000; font-size: 0.9rem;">1. Select a numeric revenue column<br>2. Select a variance percentage column<br>3. Optionally add a date column for trends</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
