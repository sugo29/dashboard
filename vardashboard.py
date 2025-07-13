import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Variance Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #e74c3c;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #e74c3c;
    }
    .variance-high {
        color: #e74c3c;
        font-weight: bold;
    }
    .variance-medium {
        color: #f39c12;
        font-weight: bold;
    }
    .variance-low {
        color: #27ae60;
        font-weight: bold;
    }
    /* Compact sidebar styling */
    .css-1d391kg {
        padding-top: 0.5rem;
    }
    .css-1cypcdb {
        padding: 0.1rem 1rem;
    }
    .stSelectbox label {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 0rem !important;
        line-height: 1.1 !important;
    }
    .stSlider label {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 0rem !important;
        line-height: 1.1 !important;
    }
    .stSelectbox > div {
        margin-bottom: 0rem !important;
    }
    .stSlider > div {
        margin-bottom: 0rem !important;
    }
    .stSelectbox > div > div {
        min-height: 32px !important;
        height: 32px !important;
    }
    /* Reduce sidebar width and optimize space */
    .css-1d391kg {
        width: 260px !important;
    }
    section[data-testid="stSidebar"] > div {
        width: 260px !important;
    }
    /* Compact sidebar header */
    .css-1cypcdb h3 {
        margin-top: 0 !important;
        margin-bottom: 0.2rem !important;
        font-size: 1.1rem !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the variance dashboard data."""
    # Load data with first row as headers
    df = pd.read_excel('dummy_data.xlsx', header=0)
    
    # Check if the actual headers are in the first row of data
    if df.iloc[0, 0] == 'MONTH':
        # Use the first row as column names and drop it
        df.columns = df.iloc[0]
        df = df.drop(df.index[0]).reset_index(drop=True)
        
        # Reset column names to remove any index references
        df.columns.name = None
    
    # Ensure numeric columns are properly typed
    numeric_columns = ['ORDER COUNT', 'CART SALES', 'DISCOUNT', 'NET REVENUE', 
                      'IDEAL FOOD COST', 'GROSS MARGIN', 'KITCHEN EBITDA', 'VARIANCE']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculate variance percentage
    df['VARIANCE_PCT'] = (df['VARIANCE'] / df['NET REVENUE'] * 100).round(2)
    
    # Create variance categories
    df['VARIANCE_CATEGORY'] = df['VARIANCE_PCT'].apply(lambda x: 
        'High (>0.8%)' if x > 0.8 else 
        'Medium (0.4-0.8%)' if x > 0.4 else 
        'Low (<0.4%)')
    
    # Convert MONTH to datetime for better sorting
    df['MONTH_DATE'] = pd.to_datetime(df['MONTH'], format='%b-%Y')
    df = df.sort_values('MONTH_DATE')
    
    return df

def create_navigation():
    """Create navigation links between dashboards."""
    st.sidebar.markdown("### 🔗 Navigation")
    
    # Create navigation buttons
    st.sidebar.markdown("📈 **Variance Dashboard** *(Active)*")
    
    # Configuration for deployment URLs
    # You can set these as environment variables or Streamlit secrets when deployed
    KITCHEN_DASHBOARD_URL = st.secrets.get("KITCHEN_DASHBOARD_URL", "http://localhost:8501")
    VARIANCE_DASHBOARD_URL = st.secrets.get("VARIANCE_DASHBOARD_URL", "http://localhost:8502")
    
    # Create navigation link
    kitchen_url = KITCHEN_DASHBOARD_URL
    st.sidebar.markdown(
        f'<a href="{kitchen_url}" target="_blank" style="text-decoration: none;">'
        f'<button style="width: 100%; padding: 0.5rem; background-color: #ff6b6b; color: white; '
        f'border: none; border-radius: 0.5rem; cursor: pointer; font-weight: bold;">'
        f'🍳 Switch to Kitchen Dashboard</button></a>',
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    
    # Quick access info
    with st.sidebar.expander("ℹ️ Dashboard Info"):
        st.write("**Current:** Variance Analysis Dashboard")
        if "localhost" in VARIANCE_DASHBOARD_URL:
            st.write("**Environment:** Local Development")
            st.write("**Port:** 8502")
        else:
            st.write("**Environment:** Production/Deployed")
        st.write(f"**Kitchen Dashboard:** {kitchen_url}")
        st.write(f"**Variance Dashboard:** {VARIANCE_DASHBOARD_URL}")

def create_filters(df):
    """Create compact sidebar filters."""
    st.sidebar.markdown("### 📊 Variance Filters")
    
    # Variance filter options
    variance_options = [
        "All",
        "High Variance (>0.8%)",
        "Medium Variance (0.4-0.8%)", 
        "Low Variance (<0.4%)",
        "Custom Range"
    ]
    
    selected_variance = st.sidebar.selectbox("📈 Variance Filter", variance_options, key="variance_filter")
    
    # Custom variance range if selected
    variance_range = None
    if selected_variance == "Custom Range":
        min_var = float(df['VARIANCE_PCT'].min())
        max_var = float(df['VARIANCE_PCT'].max())
        variance_range = st.sidebar.slider(
            "Custom Variance % Range",
            min_value=min_var,
            max_value=max_var,
            value=(min_var, max_var),
            step=0.01,
            key="custom_variance_range"
        )
    
    # Store filter
    stores = ['All'] + sorted(df['STORE'].unique().tolist())
    selected_store = st.sidebar.selectbox("🏪 Store", stores, key="store")
    
    # City filter
    cities = ['All'] + sorted(df['CITY'].unique().tolist())
    selected_city = st.sidebar.selectbox("🏙️ City", cities, key="city")
    
    st.sidebar.markdown("### 🔧 Matrix Configuration")
    
    # Row selector for matrix
    row_options = [
        "REVENUE COHORT",
        "CM COHORT",
        "EBITDA CATEGORY"
    ]
    selected_row = st.sidebar.selectbox("📊 Matrix Rows", row_options, key="matrix_row")
    
    # Toggle for count vs percentage
    show_percentage = st.sidebar.toggle("Count %", value=False, help="Toggle between Count and Count %")
    
    return {
        'variance_filter': selected_variance,
        'variance_range': variance_range,
        'store': selected_store,
        'city': selected_city,
        'matrix_row': selected_row,
        'show_percentage': show_percentage
    }

def apply_filters(df, filters):
    """Apply selected filters to the dataframe."""
    filtered_df = df.copy()
    
    # Apply variance filter
    if filters['variance_filter'] == "High Variance (>0.8%)":
        filtered_df = filtered_df[filtered_df['VARIANCE_PCT'] > 0.8]
    elif filters['variance_filter'] == "Medium Variance (0.4-0.8%)":
        filtered_df = filtered_df[(filtered_df['VARIANCE_PCT'] >= 0.4) & (filtered_df['VARIANCE_PCT'] <= 0.8)]
    elif filters['variance_filter'] == "Low Variance (<0.4%)":
        filtered_df = filtered_df[filtered_df['VARIANCE_PCT'] < 0.4]
    elif filters['variance_filter'] == "Custom Range" and filters['variance_range']:
        min_var, max_var = filters['variance_range']
        filtered_df = filtered_df[(filtered_df['VARIANCE_PCT'] >= min_var) & (filtered_df['VARIANCE_PCT'] <= max_var)]
    
    # Apply other filters
    if filters['store'] != 'All':
        filtered_df = filtered_df[filtered_df['STORE'] == filters['store']]
    
    if filters['city'] != 'All':
        filtered_df = filtered_df[filtered_df['CITY'] == filters['city']]
    
    return filtered_df

def create_variance_summary_metrics(df):
    """Create summary metrics for variance analysis."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_variance = df['VARIANCE_PCT'].mean()
        st.metric("Average Variance %", f"{avg_variance:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_stores = df['STORE'].nunique()
        st.metric("Total Stores", total_stores)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        high_variance_stores = len(df[df['VARIANCE_PCT'] > 0.8])
        st.metric("High Variance Records", high_variance_stores)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_variance = df['VARIANCE'].sum()
        st.metric("Total Variance", f"₹{total_variance:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)

def create_cohort_month_matrix(df, matrix_row, show_percentage=False):
    """Create a matrix showing store counts by selected row attribute and month."""
    display_type = "Count %" if show_percentage else "Count"
    st.markdown(f"### 📊 Store {display_type} Matrix: {matrix_row} vs Month")
    
    # Create pivot table
    pivot_table = df.groupby([matrix_row, 'MONTH']).size().reset_index(name='Store Count')
    pivot_matrix = pivot_table.pivot(index=matrix_row, columns='MONTH', values='Store Count').fillna(0)
    
    # Convert to percentage if requested
    if show_percentage:
        # Calculate percentage by column (month)
        pivot_matrix_pct = pivot_matrix.div(pivot_matrix.sum(axis=0), axis=1) * 100
        pivot_matrix_display = pivot_matrix_pct.round(1)
        value_suffix = "%"
        color_scale_title = "Count %"
    else:
        pivot_matrix_display = pivot_matrix
        value_suffix = ""
        color_scale_title = "Store Count"
    
    # Reorder columns chronologically
    month_order = df.sort_values('MONTH_DATE')['MONTH'].unique()
    pivot_matrix_display = pivot_matrix_display.reindex(columns=month_order)
    
    # Create heatmap
    fig = px.imshow(
        pivot_matrix_display.values,
        x=pivot_matrix_display.columns,
        y=pivot_matrix_display.index,
        color_continuous_scale='Blues',
        title=f"Store {display_type} Heatmap by {matrix_row} and Month",
        labels={'color': color_scale_title}
    )
    
    # Add text annotations
    for i, row in enumerate(pivot_matrix_display.index):
        for j, col in enumerate(pivot_matrix_display.columns):
            value = pivot_matrix_display.loc[row, col]
            if show_percentage:
                text = f"{value:.1f}%" if value > 0 else "0%"
            else:
                text = str(int(value))
            
            fig.add_annotation(
                x=j, y=i,
                text=text,
                showarrow=False,
                font=dict(color="white" if value > pivot_matrix_display.values.max()/2 else "black")
            )
    
    fig.update_layout(
        height=350,
        xaxis_title="Month",
        yaxis_title=matrix_row
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display the matrix as a table
    st.markdown(f"#### 📋 Store {display_type} Table")
    
    # Format the pivot table for display
    if show_percentage:
        # For percentage table, show percentages with % symbol
        display_table = pivot_matrix_display.round(1)
        # Add Total column for percentages (should sum to 100% for each month)
        display_table['Total'] = pivot_matrix.sum(axis=1)  # Keep absolute counts for total
        
        # Add totals row (absolute counts)
        totals_row = pivot_matrix.sum(axis=0)
        totals_row.name = 'Total'
        
        # Convert the main data to string with % symbol for display
        display_table_str = display_table.copy()
        for col in display_table_str.columns[:-1]:  # All except Total column
            display_table_str[col] = display_table_str[col].apply(lambda x: f"{x:.1f}%" if x > 0 else "0%")
        
        # Add totals row
        display_table_str = pd.concat([display_table_str, totals_row.to_frame().T])
        
        st.dataframe(display_table_str, use_container_width=True)
    else:
        # For count table, show regular integers
        display_table = pivot_matrix_display.astype(int)
        display_table['Total'] = display_table.sum(axis=1)
        
        # Add totals row
        totals_row = display_table.sum(axis=0)
        totals_row.name = 'Total'
        display_table = pd.concat([display_table, totals_row.to_frame().T])
        
        st.dataframe(display_table, use_container_width=True)

def create_revenue_variance_analysis(df, matrix_row):
    """Create variance analysis by selected row attribute."""
    st.markdown(f"### 💰 {matrix_row} vs Variance Analysis")
    
    # Only create box plot if the selected attribute makes sense for variance analysis
    if matrix_row in ['REVENUE COHORT', 'CM COHORT', 'EBITDA CATEGORY', 'ZONE MAPPING']:
        # Box plot of variance by selected attribute
        fig = px.box(
            df, 
            x=matrix_row, 
            y='VARIANCE_PCT',
            title=f"Variance Distribution by {matrix_row}",
            labels={'VARIANCE_PCT': 'Variance %', matrix_row: matrix_row}
        )
        fig.update_layout(height=350)
        fig.update_xaxes(tickangle=45)  # Rotate x-axis labels for better readability
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics by selected attribute
    st.markdown(f"#### 📊 Variance Statistics by {matrix_row}")
    cohort_stats = df.groupby(matrix_row)['VARIANCE_PCT'].agg([
        'count', 'mean', 'median', 'min', 'max', 'std'
    ]).round(2)
    cohort_stats.columns = ['Count', 'Mean %', 'Median %', 'Min %', 'Max %', 'Std Dev %']
    st.dataframe(cohort_stats, use_container_width=True)

def main():
    """Main dashboard function."""
    # Header
    st.markdown('<h1 class="main-header">🎯 Variance Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    try:
        df = load_data()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return
    
    # Create navigation
    create_navigation()
    
    # Create filters
    filters = create_filters(df)
    
    # Apply filters
    filtered_df = apply_filters(df, filters)
    
    # Show filtered data info
    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches the selected filters.")
        return
    
    # Summary metrics
    create_variance_summary_metrics(filtered_df)
    
    st.markdown("---")
    
    # Main matrix view
    create_cohort_month_matrix(filtered_df, filters['matrix_row'], filters['show_percentage'])
    
    st.markdown("---")
    
    # Revenue variance analysis
    create_revenue_variance_analysis(filtered_df, filters['matrix_row'])
    
    # Raw data view
    with st.expander("🔍 View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
