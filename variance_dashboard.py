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
        background-color: white !important;
        border-right: 1px solid #e0e4e8;
    }
    
    /* Comprehensive sidebar styling - ensure all content is white background */
    .stSidebar, .stSidebar > div, .stSidebar .element-container {
        background-color: white !important;
        color: #000000 !important;
    }
    
    /* Sidebar headers */
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* Sidebar form elements */
    .stSidebar .stSelectbox, .stSidebar .stCheckbox, .stSidebar .stRadio {
        background-color: white !important;
    }
    
    /* Sidebar selectbox styling */
    .stSidebar .stSelectbox > div > div, 
    .stSidebar .stSelectbox label,
    .stSidebar .stSelectbox > label > div {
        background-color: white !important;
        color: #000000 !important;
    }
    
    /* Sidebar checkbox styling */
    .stSidebar .stCheckbox > label,
    .stSidebar .stCheckbox > label > div,
    .stSidebar .stCheckbox label p {
        background-color: white !important;
        color: #000000 !important;
    }
    
    /* Enhanced checkbox styling for variance filters */
    .stSidebar .stCheckbox {
        margin: 0.3rem 0;
        padding: 0.4rem;
        border-radius: 4px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
    }
    
    .stSidebar .stCheckbox:hover {
        background-color: #f1f5f9;
        border-color: #cbd5e1;
    }
    
    /* Sidebar collapse/expand button and container */
    .stSidebar .css-1lcbmhc, 
    .stSidebar .css-1v0mbdj,
    .stSidebar .css-17eq0hr {
        background-color: white !important;
    }
    
    /* When sidebar is collapsed, ensure it maintains white background */
    .stApp[data-sidebar-state="collapsed"] .stSidebar,
    .stApp[data-sidebar-state="collapsed"] .stSidebar > div {
        background-color: white !important;
    }
    
    /* Sidebar scrollable area */
    .stSidebar .css-1cypcdb, .stSidebar .css-1d391kg {
        background-color: white !important;
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
        # Load the dummy data Excel file with proper header handling
        df = pd.read_excel('dummy_data.xlsx', header=0)
        
        # The actual headers are in the first row, so we need to fix this
        df.columns = df.iloc[0]  # Set the first row as column names
        df = df.drop(df.index[0]).reset_index(drop=True)  # Remove the header row
        
        # Clean up column names (remove any extra spaces)
        df.columns = df.columns.str.strip()
        
        st.success(f"✅ Successfully loaded data with {len(df)} rows and {len(df.columns)} columns")
        return df
    except FileNotFoundError:
        st.error("❌ File 'dummy_data.xlsx' not found in the current directory!")
        st.info("📁 Please ensure your Excel file is named 'dummy_data.xlsx' and is in the same folder as this script.")
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
        
        # Handle different formats - remove currency symbols, commas, etc.
        if df_copy[revenue_col].dtype == 'object':
            # Clean the revenue column - remove any non-numeric characters except decimal points
            df_copy[revenue_col] = df_copy[revenue_col].astype(str).str.replace(',', '').str.replace('₹', '').str.replace('INR', '').str.replace(' ', '')
        
        df_copy[revenue_col] = pd.to_numeric(df_copy[revenue_col], errors='coerce')
        df_copy = df_copy.dropna(subset=[revenue_col])
        
        if len(df_copy) == 0:
            st.error(f"No valid numeric data found in column '{revenue_col}'.")
            return df
            
        df = df_copy
    except Exception as e:
        st.error(f"Error converting '{revenue_col}' to numeric: {e}")
        return df
    
    # Check if the data is already in lakhs or needs conversion
    max_revenue = df[revenue_col].max()
    
    # If the revenue values are very large (>100000), they might be in actual currency units
    # Convert to lakhs for easier categorization
    if max_revenue > 100000:
        df[revenue_col] = df[revenue_col] / 100000  # Convert to lakhs
    
    # Create revenue categories matching the requested ranges (in lacs)
    def assign_revenue_category(revenue):
        if pd.isna(revenue):
            return "Unknown"
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

def create_variance_buckets(df, revenue_col):
    """Create variance buckets based on calculated variance from revenue data"""
    if revenue_col not in df.columns:
        st.error(f"Column '{revenue_col}' not found in dataset")
        return df
    
    try:
        df_copy = df.copy()
        
        # Convert revenue column to numeric
        if df_copy[revenue_col].dtype == 'object':
            # Clean the revenue column - remove any non-numeric characters except decimal points
            df_copy[revenue_col] = df_copy[revenue_col].astype(str).str.replace(',', '').str.replace('₹', '').str.replace('INR', '').str.replace(' ', '')
        
        df_copy[revenue_col] = pd.to_numeric(df_copy[revenue_col], errors='coerce')
        df_copy = df_copy.dropna(subset=[revenue_col])
        
        if len(df_copy) == 0:
            st.error(f"No valid numeric data found in column '{revenue_col}'.")
            return df
        
        # Calculate variance percentage
        # Assuming we need to calculate variance as deviation from expected/target revenue
        # For each store, calculate variance as percentage deviation from store's mean revenue
        
        if 'STORE' in df_copy.columns:
            # Calculate mean revenue per store
            store_means = df_copy.groupby('STORE')[revenue_col].mean()
            
            # Calculate variance for each record as percentage deviation from store mean
            def calculate_variance_percentage(row):
                store = row['STORE']
                actual_revenue = row[revenue_col]
                expected_revenue = store_means[store]
                
                if expected_revenue == 0:
                    return 0
                
                variance_pct = ((actual_revenue - expected_revenue) / expected_revenue) * 100
                return abs(variance_pct)  # Use absolute value for variance buckets
            
            df_copy['Variance_Percentage'] = df_copy.apply(calculate_variance_percentage, axis=1)
        else:
            # If no STORE column, calculate variance from overall mean
            overall_mean = df_copy[revenue_col].mean()
            df_copy['Variance_Percentage'] = ((df_copy[revenue_col] - overall_mean) / overall_mean * 100).abs()
        
        df = df_copy
        
    except Exception as e:
        st.error(f"Error calculating variance from '{revenue_col}': {e}")
        return df
    
    # Create variance buckets based on calculated variance percentage
    def assign_variance_bucket(variance_pct):
        if pd.isna(variance_pct):
            return "Unknown"
        if variance_pct < 2:
            return "Var < 2%"
        elif variance_pct < 3:
            return "Var 2% to 3%"
        elif variance_pct < 5:
            return "Var 3% to 5%"
        else:
            return "Var > 5%"
    
    df['Variance_Bucket'] = df['Variance_Percentage'].apply(assign_variance_bucket)
    return df

def sub_dashboard_1(df, revenue_col, variance_col, var_filters, selected_stores=None):
    """Sub-dashboard 1: Stores by Revenue Category and Month based on Variance Filter"""
    st.markdown("## STORES BY REVENUE CATEGORY AND VARIANCE FILTER")
    st.markdown("The table below shows stores that meet the selected variance criteria, organized by revenue categories and months")
    
    if revenue_col not in df.columns:
        st.error("Required revenue column not found in dataset")
        return
    
    # Handle case where var_filters might be None
    if var_filters is None:
        st.error("Variance filters not properly initialized. Please refresh the page.")
        return
    
    # Filter by selected stores first if provided
    if selected_stores and len(selected_stores) > 0:
        store_col = 'STORE'  # Assuming STORE is the column name
        if store_col in df.columns:
            df = df[df[store_col].isin(selected_stores)]
            if len(df) == 0:
                st.warning("No data found for the selected stores.")
                return
        else:
            st.error(f"Store column '{store_col}' not found in dataset")
            return
    
    # Process data
    df_processed = create_revenue_cohorts(df, revenue_col)
    
    # Check if Revenue_Category column was created successfully
    if 'Revenue_Category' not in df_processed.columns:
        st.error("Could not create revenue categories. Please check your revenue data.")
        return
    
    # Convert variance column to numeric and create buckets
    df_processed = create_variance_buckets(df_processed, revenue_col)
    
    # Check if Variance_Bucket column was created successfully
    if 'Variance_Bucket' not in df_processed.columns:
        st.error("Could not create variance buckets. Please check your variance data.")
        return
    
    # Apply variance filters
    filtered_buckets = []
    if var_filters.get("var_below_2", False):
        filtered_buckets.append("Var < 2%")
    if var_filters.get("var_2_to_3", False):
        filtered_buckets.append("Var 2% to 3%")
    if var_filters.get("var_3_to_5", False):
        filtered_buckets.append("Var 3% to 5%")
    if var_filters.get("var_above_5", False):
        filtered_buckets.append("Var > 5%")
    
    if not filtered_buckets:
        st.warning("⚠️ Please select at least one variance filter to see results.")
        return
    
    # Calculate totals BEFORE filtering
    total_stores_all = df_processed['STORE'].nunique()
    total_records_all = len(df_processed)
    
    # Filter data based on selected variance buckets
    df_filtered = df_processed[df_processed['Variance_Bucket'].isin(filtered_buckets)]
    
    if len(df_filtered) == 0:
        st.warning("No stores found matching the selected variance criteria.")
        return
    
    # Calculate filtered totals
    total_stores_filtered = df_filtered['STORE'].nunique()
    total_records_filtered = len(df_filtered)
    
    # Calculate percentages
    store_percentage = (total_stores_filtered / total_stores_all) * 100
    record_percentage = (total_records_filtered / total_records_all) * 100
    
    # Show active filters with percentages
    st.info(f"📊 Showing **{total_stores_filtered}** stores (**{store_percentage:.1f}%** of {total_stores_all} total) with variance: {', '.join(filtered_buckets)}")
    st.info(f"📈 **{total_records_filtered}** records (**{record_percentage:.1f}%** of {total_records_all} total) match the selected criteria")
    
    # Show store selection info if stores were filtered
    if selected_stores:
        original_store_count = len([store for store in selected_stores if store in df_processed['STORE'].values])
        if len(selected_stores) < df_processed['STORE'].nunique():
            all_stores_count = df_processed['STORE'].nunique() 
            st.info(f"🏪 Analysis limited to **{len(selected_stores)}** selected stores out of **{all_stores_count}** total stores in dataset")
    
    # Column names
    store_col = 'STORE'
    month_col = 'MONTH'
    
    # Order revenue categories
    revenue_order = [
        "Below INR 15 lacs", 
        "INR 15 to 25 lacs", 
        "INR 25 to 35 lacs", 
        "INR 35 to 45 lacs", 
        "Above INR 45 lacs"
    ]
    
    # Get unique stores for columns (instead of months)
    unique_stores_in_data = sorted(df_filtered[store_col].unique())
    
    # Create summary table showing revenue vs stores with presence indicators
    st.markdown("### 📊 Summary: Store Analysis by Revenue Category and Store")
    st.markdown("*Format: ✓ (Present) / - (Not Present) for each store*")
    
    try:
        # Create summary table data
        summary_table_data = []
        
        for category in revenue_order:
            # Get data for this revenue category
            category_all_data = df_processed[df_processed['Revenue_Category'] == category]
            category_filtered_data = df_filtered[df_filtered['Revenue_Category'] == category]
            
            row_data = {'Revenue Category': category}
            
            # For each store, check if it appears in this revenue category
            for store in unique_stores_in_data:
                store_all_data = category_all_data[category_all_data[store_col] == store]
                store_filtered_data = category_filtered_data[category_filtered_data[store_col] == store]
                
                if len(store_filtered_data) > 0:
                    # Store is present in this category with the selected variance filters
                    avg_variance = store_filtered_data['Variance_Percentage'].mean()
                    row_data[store] = f"✓ ({avg_variance:.1f}%)"
                elif len(store_all_data) > 0:
                    # Store exists in this category but doesn't match variance filters
                    row_data[store] = "○ (filtered out)"
                else:
                    # Store doesn't exist in this revenue category
                    row_data[store] = "-"
            
            # Add total for this category
            total_category_all = category_all_data[store_col].nunique() if len(category_all_data) > 0 else 0
            total_category_filtered = category_filtered_data[store_col].nunique() if len(category_filtered_data) > 0 else 0
            row_data['Total Stores'] = f"{total_category_filtered}/{total_category_all}"
            
            summary_table_data.append(row_data)
        
        # Add overall total row
        total_row = {'Revenue Category': '🏪 TOTAL ALL CATEGORIES'}
        for store in unique_stores_in_data:
            store_all_data = df_processed[df_processed[store_col] == store]
            store_filtered_data = df_filtered[df_filtered[store_col] == store]
            
            if len(store_filtered_data) > 0:
                avg_variance = store_filtered_data['Variance_Percentage'].mean()
                total_row[store] = f"✓ ({avg_variance:.1f}%)"
            elif len(store_all_data) > 0:
                total_row[store] = "○ (filtered out)"
            else:
                total_row[store] = "-"
        
        total_row['Total Stores'] = f"{total_stores_filtered}/{total_stores_all}"
        summary_table_data.append(total_row)
        
        # Create and display summary DataFrame
        if summary_table_data:
            summary_df = pd.DataFrame(summary_table_data)
            st.dataframe(summary_df.set_index('Revenue Category'), use_container_width=True)
            
            # Show variance filter impact
            st.markdown("### 🎯 Variance Filter Impact")
            impact_data = []
            for bucket in filtered_buckets:
                bucket_data = df_filtered[df_filtered['Variance_Bucket'] == bucket]
                bucket_stores = bucket_data[store_col].nunique()
                bucket_percentage = (bucket_stores / total_stores_all) * 100
                
                impact_data.append({
                    'Variance Bucket': bucket,
                    'Stores': bucket_stores,
                    'Percentage': f"{bucket_percentage:.1f}%"
                })
            
            if impact_data:
                impact_df = pd.DataFrame(impact_data)
                st.dataframe(impact_df.set_index('Variance Bucket'), use_container_width=True)
    
    except Exception as e:
        st.error(f"Error creating summary table: {e}")
    
    st.markdown("### 📋 Detailed Analysis: Individual Store Breakdown")
    
    try:
        # Create the table structure - each store in its own row
        table_data = []
        
        for category in revenue_order:
            # Get total stores in this category (all data)
            category_all_data = df_processed[df_processed['Revenue_Category'] == category]
            total_stores_category = category_all_data[store_col].nunique() if len(category_all_data) > 0 else 0
            
            # Get filtered stores in this category
            category_data = df_filtered[df_filtered['Revenue_Category'] == category]
            
            if len(category_data) == 0 and total_stores_category == 0:
                continue  # Skip categories with no data at all
            
            # Get unique stores in this category
            unique_stores = category_data[store_col].unique()
            
            if len(unique_stores) == 0:
                # If no stores match the filters, show a summary row
                row_data = {
                    'Revenue Category': category, 
                    'Store': 'No stores match filters',
                    'Total Records': 0,
                    'Variance %': "-"
                }
                table_data.append(row_data)
                continue
            
            # Create a row for each store
            for store in unique_stores:
                store_data = category_data[category_data[store_col] == store]
                
                row_data = {
                    'Revenue Category': category,
                    'Store': store
                }
                
                # Calculate average variance for this store
                avg_variance = store_data['Variance_Percentage'].mean()
                row_data['Variance %'] = f"{avg_variance:.1f}%"
                
                # No need for month-wise breakdown since we're showing stores as columns
                # Just show total records for this store in this category
                row_data['Total Records'] = len(store_data)
                
                table_data.append(row_data)
            
            # Add category summary row
            unique_stores_count = len(unique_stores)
            category_percentage = (unique_stores_count / total_stores_category) * 100 if total_stores_category > 0 else 0
            
            summary_row = {
                'Revenue Category': f"📊 {category} SUMMARY",
                'Store': f"{unique_stores_count} stores total",
                'Variance %': f"{category_data['Variance_Percentage'].mean():.1f}% avg",
                'Total Records': len(category_data)
            }
            
            table_data.append(summary_row)
        
        if table_data:
            # Create DataFrame
            summary_df = pd.DataFrame(table_data)
            
            # Calculate totals for all stores
            total_row = {'Revenue Category': 'TOTAL', 'Store': 'All Stores', 'Variance %': f"{df_filtered['Variance_Percentage'].mean():.1f}%", 'Total Records': len(df_filtered)}
            
            total_row['Total Stores'] = f"{total_stores_filtered}/{total_stores_all} ({store_percentage:.1f}%)"
            
            # Add total row
            summary_df = pd.concat([summary_df, pd.DataFrame([total_row])], ignore_index=True)
            
            # Display the table
            st.dataframe(summary_df.set_index(['Revenue Category', 'Store']), use_container_width=True)
            
            # Show detailed breakdown for each variance bucket - individual stores
            st.markdown("### Detailed Store-by-Store Breakdown by Variance Bucket")
            
            for bucket in filtered_buckets:
                bucket_data = df_filtered[df_filtered['Variance_Bucket'] == bucket]
                
                if len(bucket_data) == 0:
                    continue
                
                bucket_stores = bucket_data[store_col].nunique()
                bucket_percentage = (bucket_stores / total_stores_all) * 100
                
                st.markdown(f"#### {bucket} - {bucket_stores}/{total_stores_all} stores ({bucket_percentage:.1f}%)")
                
                # Create breakdown table for this variance bucket - one row per store
                bucket_table_data = []
                
                for category in revenue_order:
                    category_bucket_data = bucket_data[bucket_data['Revenue_Category'] == category]
                    
                    if len(category_bucket_data) == 0:
                        continue
                    
                    # Get unique stores in this category for this variance bucket
                    unique_stores = category_bucket_data[store_col].unique()
                    
                    for store in unique_stores:
                        store_data = category_bucket_data[category_bucket_data[store_col] == store]
                        
                        row_data = {
                            'Revenue Category': category,
                            'Store': store,
                            'Avg Variance': f"{store_data['Variance_Percentage'].mean():.1f}%",
                            'Total Records': len(store_data)
                        }
                        
                        bucket_table_data.append(row_data)
                
                if bucket_table_data:
                    bucket_df = pd.DataFrame(bucket_table_data)
                    st.dataframe(bucket_df.set_index(['Revenue Category', 'Store']), use_container_width=True)
            
            # Show enhanced summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Filtered Stores", 
                    value=f"{total_stores_filtered}/{total_stores_all}",
                    delta=f"{store_percentage:.1f}%"
                )
            
            with col2:
                active_stores = len(unique_stores_in_data)
                st.metric(
                    label="Active Stores", 
                    value=active_stores
                )
            
            with col3:
                avg_variance = df_filtered['Variance_Percentage'].mean()
                st.metric(
                    label="Average Variance", 
                    value=f"{avg_variance:.1f}%"
                )
            
            with col4:
                st.metric(
                    label="Records", 
                    value=f"{total_records_filtered}/{total_records_all}",
                    delta=f"{record_percentage:.1f}%"
                )
        
        else:
            st.warning("No data found for the selected filters and revenue categories.")
            
    except Exception as e:
        st.error(f"Error creating analysis: {e}")
        st.write("Debug info:")
        st.write(f"Available columns: {df_filtered.columns.tolist()}")
        st.write(f"Data shape: {df_filtered.shape}")
        st.write("Sample data:")
        st.write(df_filtered.head())

def sub_dashboard_2(df, revenue_col, variance_col, var_filters, date_col=None, store_col='STORE', selected_stores=None):
    """Sub-dashboard 2: Store Count by Variance Bucket and Revenue Category with Percentages"""
    st.markdown("## STORE COUNT BY VARIANCE AND REVENUE (WITH PERCENTAGES)")
    st.markdown("The table below shows the count and percentage of kitchen stores by variance buckets and revenue categories")
    
    if revenue_col not in df.columns:
        st.error("Required revenue column not found in dataset")
        return
    
    # Handle case where var_filters might be None
    if var_filters is None:
        st.error("Variance filters not properly initialized. Please refresh the page.")
        return
    
    # Filter by selected stores first if provided
    if selected_stores and len(selected_stores) > 0:
        if store_col in df.columns:
            df = df[df[store_col].isin(selected_stores)]
            if len(df) == 0:
                st.warning("No data found for the selected stores.")
                return
        else:
            st.error(f"Store column '{store_col}' not found in dataset")
            return
    
    # Process data
    df_processed = create_revenue_cohorts(df, revenue_col)
    
    # Check if Revenue_Category column was created successfully
    if 'Revenue_Category' not in df_processed.columns:
        st.error("Could not create revenue categories. Please check your revenue data.")
        return
    
    df_processed = create_variance_buckets(df_processed, revenue_col)
    
    # Check if Variance_Bucket column was created successfully
    if 'Variance_Bucket' not in df_processed.columns:
        st.error("Could not create variance buckets. Please check your variance data.")
        return
    
    # Apply variance filters
    filtered_buckets = []
    if var_filters.get("var_below_2", False):
        filtered_buckets.append("Var < 2%")
    if var_filters.get("var_2_to_3", False):
        filtered_buckets.append("Var 2% to 3%")
    if var_filters.get("var_3_to_5", False):
        filtered_buckets.append("Var 3% to 5%")
    if var_filters.get("var_above_5", False):
        filtered_buckets.append("Var > 5%")
    
    if not filtered_buckets:
        st.warning("⚠️ Please select at least one variance filter to see results.")
        return
    
    # Calculate totals BEFORE filtering
    total_stores_all = df_processed[store_col].nunique()
    total_records_all = len(df_processed)
    
    # Filter data based on selected variance buckets
    df_filtered = df_processed[df_processed['Variance_Bucket'].isin(filtered_buckets)]
    
    if len(df_filtered) == 0:
        st.warning("No stores found matching the selected variance criteria.")
        return
    
    # Calculate filtered totals
    total_stores_filtered = df_filtered[store_col].nunique()
    total_records_filtered = len(df_filtered)
    
    # Calculate percentages
    store_percentage = (total_stores_filtered / total_stores_all) * 100
    record_percentage = (total_records_filtered / total_records_all) * 100
    
    # Show active filters with percentages
    st.info(f"📊 Showing **{total_stores_filtered}** stores (**{store_percentage:.1f}%** of {total_stores_all} total) with variance: {', '.join(filtered_buckets)}")
    st.info(f"📈 **{total_records_filtered}** records (**{record_percentage:.1f}%** of {total_records_all} total) match the selected criteria")
    
    # Show store selection info if stores were filtered
    if selected_stores:
        if len(selected_stores) < df_processed[store_col].nunique():
            all_stores_count = df_processed[store_col].nunique()
            st.info(f"🏪 Analysis limited to **{len(selected_stores)}** selected stores out of **{all_stores_count}** total stores in dataset")
    
    # Process date column to extract months
    has_date = False
    if date_col and date_col in df_processed.columns:
        try:
            # Try to convert to datetime
            df_processed[date_col] = pd.to_datetime(df_processed[date_col], errors='coerce')
            df_filtered[date_col] = pd.to_datetime(df_filtered[date_col], errors='coerce')
            # Extract month
            df_processed['Month'] = df_processed[date_col].dt.strftime('%Y-%m')
            df_filtered['Month'] = df_filtered[date_col].dt.strftime('%Y-%m')
            has_date = True
        except:
            st.warning(f"Could not convert '{date_col}' to date format.")
    
    # Add a dummy column for counting
    df_processed['Count'] = 1
    df_filtered['Count'] = 1
    
    # Revenue categories order
    revenue_order = [
        "Below INR 15 lacs", 
        "INR 15 to 25 lacs", 
        "INR 25 to 35 lacs", 
        "INR 35 to 45 lacs", 
        "Above INR 45 lacs"
    ]
    
    # Create summary table at the top
    st.markdown("### 📊 Summary: Store Analysis by Revenue Category and Store")
    st.markdown("*Format: ✓ (Present with variance %) / ○ (Filtered out) / - (Not in category)*")
    
    try:
        # Get unique stores for columns (instead of months)
        unique_stores_in_data = sorted(df_filtered[store_col].unique())
        
        # Create summary with stores as columns
        summary_table_data = []
        
        for category in revenue_order:
            category_all_data = df_processed[df_processed['Revenue_Category'] == category]
            category_filtered_data = df_filtered[df_filtered['Revenue_Category'] == category]
            
            row_data = {'Revenue Category': category}
            
            for store in unique_stores_in_data:
                store_all_data = category_all_data[category_all_data[store_col] == store]
                store_filtered_data = category_filtered_data[category_filtered_data[store_col] == store]
                
                if len(store_filtered_data) > 0:
                    # Store is present in this category with the selected variance filters
                    avg_variance = store_filtered_data['Variance_Percentage'].mean()
                    row_data[store] = f"✓ ({avg_variance:.1f}%)"
                elif len(store_all_data) > 0:
                    # Store exists in this category but doesn't match variance filters
                    row_data[store] = "○ (filtered out)"
                else:
                    # Store doesn't exist in this revenue category
                    row_data[store] = "-"
            
            # Add total for this category
            total_category_all = category_all_data[store_col].nunique() if len(category_all_data) > 0 else 0
            total_category_filtered = category_filtered_data[store_col].nunique() if len(category_filtered_data) > 0 else 0
            row_data['Total Stores'] = f"{total_category_filtered}/{total_category_all}"
            
            summary_table_data.append(row_data)
        
        # Add overall total row
        total_row = {'Revenue Category': '🏪 TOTAL ALL CATEGORIES'}
        for store in unique_stores_in_data:
            store_all_data = df_processed[df_processed[store_col] == store]
            store_filtered_data = df_filtered[df_filtered[store_col] == store]
            
            if len(store_filtered_data) > 0:
                avg_variance = store_filtered_data['Variance_Percentage'].mean()
                total_row[store] = f"✓ ({avg_variance:.1f}%)"
            elif len(store_all_data) > 0:
                total_row[store] = "○ (filtered out)"
            else:
                total_row[store] = "-"
        
        total_row['Total Stores'] = f"{total_stores_filtered}/{total_stores_all}"
        summary_table_data.append(total_row)
            
        # Display summary table
        if summary_table_data:
            summary_df = pd.DataFrame(summary_table_data)
            st.dataframe(summary_df.set_index('Revenue Category'), use_container_width=True)
            
            # Show variance filter breakdown
            st.markdown("### 🎯 Variance Filter Breakdown")
            variance_breakdown = []
            
            for bucket in filtered_buckets:
                bucket_data = df_filtered[df_filtered['Variance_Bucket'] == bucket]
                bucket_stores = bucket_data[store_col].nunique()
                bucket_records = len(bucket_data)
                
                # Count by revenue category for this variance bucket
                category_counts = []
                for category in revenue_order:
                    cat_bucket_data = bucket_data[bucket_data['Revenue_Category'] == category]
                    cat_stores = cat_bucket_data[store_col].nunique() if len(cat_bucket_data) > 0 else 0
                    if cat_stores > 0:
                        category_counts.append(f"{category}: {cat_stores}")
                
                variance_breakdown.append({
                    'Variance Bucket': bucket,
                    'Total Stores': bucket_stores,
                    'Total Records': bucket_records,
                    'Revenue Category Breakdown': ", ".join(category_counts) if category_counts else "No stores"
                })
            
            if variance_breakdown:
                variance_df = pd.DataFrame(variance_breakdown)
                st.dataframe(variance_df.set_index('Variance Bucket'), use_container_width=True)
    
    except Exception as e:
        st.error(f"Error creating summary table: {e}")
    
    # Create store count table with percentages - individual store rows
    st.markdown("### 🏪 Detailed Analysis: Individual Store Breakdown by Revenue and Variance")
    
    try:
        # Create individual store breakdown
        store_analysis_data = []
        
        for category in revenue_order:
            category_data = df_filtered[df_filtered['Revenue_Category'] == category]
            category_all_data = df_processed[df_processed['Revenue_Category'] == category]
            
            if len(category_data) == 0:
                continue
            
            # Get unique stores in this category
            unique_stores = category_data[store_col].unique()
            
            for store in unique_stores:
                store_data = category_data[category_data[store_col] == store]
                
                # Get variance bucket for this store (most common one if multiple)
                variance_bucket = store_data['Variance_Bucket'].mode().iloc[0] if len(store_data) > 0 else "Unknown"
                avg_variance = store_data['Variance_Percentage'].mean()
                
                store_row = {
                    'Revenue Category': category,
                    'Store': store,
                    'Variance Bucket': variance_bucket,
                    'Avg Variance %': f"{avg_variance:.1f}%",
                    'Total Records': len(store_data)
                }
                
                if has_date:
                    # Add month-wise presence
                    months_present = store_data['Month'].unique()
                    store_row['Active Months'] = f"{len(months_present)} months"
                    store_row['Months List'] = ", ".join(sorted(months_present))
                
                store_analysis_data.append(store_row)
        
        if store_analysis_data:
            store_analysis_df = pd.DataFrame(store_analysis_data)
            st.dataframe(store_analysis_df.set_index(['Revenue Category', 'Store']), use_container_width=True)
            
            # Summary by variance bucket
            st.markdown("### Summary by Variance Bucket")
            bucket_summary = []
            
            for bucket in filtered_buckets:
                bucket_stores = store_analysis_df[store_analysis_df['Variance Bucket'] == bucket]
                
                if len(bucket_stores) > 0:
                    bucket_summary.append({
                        'Variance Bucket': bucket,
                        'Store Count': len(bucket_stores),
                        'Avg Variance %': f"{bucket_stores['Avg Variance %'].str.replace('%', '').astype(float).mean():.1f}%",
                        'Total Records': bucket_stores['Total Records'].sum()
                    })
            
            if bucket_summary:
                bucket_summary_df = pd.DataFrame(bucket_summary)
                st.dataframe(bucket_summary_df.set_index('Variance Bucket'), use_container_width=True)
        
        else:
            st.warning("No store data found for the selected filters.")

        # Enhanced store-based analysis
        if has_date:
            st.markdown("### 🗓️ Time-Based Store Analysis Summary")
            st.info("📅 Date information available - showing analysis focused on store performance over time")
        else:
            st.markdown("### 🏪 Store-Based Analysis Summary")
        
        # Enhanced summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Kitchens", 
                value=f"{total_stores_filtered}/{total_stores_all}",
                delta=f"{store_percentage:.1f}%"
            )
        
        with col2:
            variance_buckets_count = len(filtered_buckets)
            total_buckets = 4  # Total variance buckets available
            bucket_percentage = (variance_buckets_count / total_buckets) * 100
            st.metric(
                label="Active Variance Filters", 
                value=f"{variance_buckets_count}/{total_buckets}",
                delta=f"{bucket_percentage:.1f}%"
            )
        
        with col3:
            revenue_categories_with_data = len([cat for cat in revenue_order if cat in df_filtered['Revenue_Category'].values])
            total_categories = len(revenue_order)
            category_percentage = (revenue_categories_with_data / total_categories) * 100
            st.metric(
                label="Revenue Categories", 
                value=f"{revenue_categories_with_data}/{total_categories}",
                delta=f"{category_percentage:.1f}%"
            )
        
        with col4:
            st.metric(
                label="Total Records", 
                value=f"{total_records_filtered}/{total_records_all}",
                delta=f"{record_percentage:.1f}%"
            )
    
    except Exception as e:
        st.error(f"Error creating analysis: {e}")
        st.write("Debug info:")
        st.write(f"Available columns: {df_filtered.columns.tolist()}")
        st.write(f"Data shape: {df_filtered.shape}")


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
        1. **File exists**: Ensure 'dummy_data.xlsx' is in the current directory
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
    
    # Revenue category selection (predefined options)
    revenue_category = st.sidebar.selectbox(
        "Select Revenue Category",
        options=[
            "Below INR 15 lacs",
            "INR 15 to 25 lacs", 
            "INR 25 to 35 lacs",
            "INR 35 to 45 lacs",
            "Above INR 45 lacs"
        ],
        help="Select revenue category to analyze"
    )
    
    # Automatically use ORDER COUNT as revenue column
    revenue_col = "ORDER COUNT" if "ORDER COUNT" in df.columns else None
    
    # Store column selection and store filter
    store_col = st.sidebar.selectbox(
        "Select STORE Column",
        options=df.columns,
        help="Column containing store identifiers"
    )
    
    # Show store filter if store column is selected
    if store_col and store_col in df.columns:
        # Get unique store names
        unique_stores = sorted(df[store_col].dropna().unique())
        
        st.sidebar.markdown("---")
        st.sidebar.header("Store Filter")
        
        # Select all stores by default
        selected_stores = st.sidebar.multiselect(
            "Select Stores to Analyze",
            options=unique_stores,
            default=unique_stores,
            help=f"Choose specific stores to include in analysis. Total: {len(unique_stores)} stores available"
        )
        
        # Show store selection summary
        if len(selected_stores) == len(unique_stores):
            st.sidebar.success(f"✅ All {len(unique_stores)} stores selected")
        elif len(selected_stores) > 0:
            st.sidebar.info(f"📊 {len(selected_stores)}/{len(unique_stores)} stores selected")
        else:
            st.sidebar.warning("⚠️ No stores selected!")
    else:
        selected_stores = []
    
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
    st.sidebar.markdown("Select variance ranges to filter stores:")
    
    var_filters = {
        "var_below_2": st.sidebar.checkbox("Var < 2% (Low Variance)", value=True),
        "var_2_to_3": st.sidebar.checkbox("Var 2% to 3% (Medium-Low)", value=True),
        "var_3_to_5": st.sidebar.checkbox("Var 3% to 5% (Medium-High)", value=True),
        "var_above_5": st.sidebar.checkbox("Var > 5% (High Variance)", value=True)
    }
    
    # Show selected filter summary
    selected_filters = [k.replace("var_", "").replace("_", " ") for k, v in var_filters.items() if v]
    if selected_filters:
        st.sidebar.success(f"✅ Active filters: {len(selected_filters)}")
    else:
        st.sidebar.warning("⚠️ No filters selected!")
    
    # Check if required columns are selected
    if revenue_col:
        st.sidebar.success(f"✅ Using revenue column: {revenue_col}")
        st.sidebar.info("📊 Variance percentage will be calculated from revenue data")
        
        # Show store selection info
        if selected_stores:
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"**Selected Stores:** {len(selected_stores)}")
            if len(selected_stores) <= 5:
                for store in selected_stores:
                    st.sidebar.markdown(f"• {store}")
            else:
                for store in selected_stores[:3]:
                    st.sidebar.markdown(f"• {store}")
                st.sidebar.markdown(f"• ... and {len(selected_stores)-3} more")
        
        # Main content - tabs for the two sub-dashboards
        tab1, tab2 = st.tabs(["Stores by Variance Filter", "Store Count Analysis"])
        
        with tab1:
            sub_dashboard_1(df, revenue_col, None, var_filters, selected_stores)
        
        with tab2:
            sub_dashboard_2(df, revenue_col, None, var_filters, date_col, store_col, selected_stores)
        
        # Enhanced footer with professional styling
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #f8fafc, #e2e8f0); border-radius: 16px; border: 1px solid #e2e8f0;">
            <h4 style="color: #000000; margin-bottom: 1rem;">📊 Analysis Summary</h4>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
                <div style="text-align: center;">
                    <strong style="color: #000000;">Variance Definition</strong><br>
                    <span style="color: #000000; font-size: 0.9rem;">Calculated from revenue deviation</span>
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
        # Enhanced error state when ORDER COUNT column is not found
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #fef3c7, #fed7aa); border-radius: 16px; margin: 2rem 0;">
            <h3 style="color: #000000; margin-bottom: 1rem;">⚠️ ORDER COUNT Column Not Found</h3>
            <p style="color: #000000; margin-bottom: 1.5rem;">The dashboard requires an 'ORDER COUNT' column in your data.</p>
            <div style="background: rgba(255, 255, 255, 0.7); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <strong style="color: #000000;">Available columns:</strong><br>
                <span style="color: #000000; font-size: 0.9rem;">""" + ", ".join(df.columns) + """</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
