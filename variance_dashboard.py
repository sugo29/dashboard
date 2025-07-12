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
        color: #1a3353;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e0e4e8;
    }
    
    .dashboard-subtitle {
        font-size: 1rem;
        color: #5a6474;
        margin-bottom: 2rem;
    }
    
    /* Professional section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 500;
        color: #1a3353;
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
        color: #1a3353;
        margin-bottom: 0.3rem;
    }
    
    .metric-label {
        color: #5a6474;
        font-size: 0.85rem;
        font-weight: 400;
    }
    
    /* Sub-header styling */
    .sub-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1a3353;
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
        color: #1e293b;
    }
    
    .insight-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #3b82f6;
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
        color: #1a3353;
        font-weight: 500;
        text-align: left;
        padding: 12px;
    }
    
    .dataframe td {
        padding: 10px 12px;
        border-top: 1px solid #e0e4e8;
        color: #444;
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
        color: #5a6474;
        font-weight: 400;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #1a3353 !important;
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
        color: #1a3353;
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
        color: #444;
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
        color: #1a3353;
        border-bottom: 1px solid #e0e4e8;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the dataset"""
    try:
        # Load the Excel file
        df = pd.read_excel('dashborad_data.xlsx')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
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
    """Create revenue cohorts based on quartiles"""
    if revenue_col not in df.columns:
        st.error(f"Column '{revenue_col}' not found in dataset")
        return df
    
    # Convert revenue column to numeric, handling non-numeric values
    try:
        df_copy = df.copy()
        df_copy[revenue_col] = pd.to_numeric(df_copy[revenue_col], errors='coerce')
        # Remove rows with NaN values (non-convertible data)
        df_copy = df_copy.dropna(subset=[revenue_col])
        
        if len(df_copy) == 0:
            st.error(f"No valid numeric data found in column '{revenue_col}'. Please select a column with numeric revenue data.")
            st.write("Sample data from this column:", df[revenue_col].head())
            return df
            
        df = df_copy
    except Exception as e:
        st.error(f"Error converting '{revenue_col}' to numeric: {e}")
        return df
    
    # Calculate quartiles
    q1 = df[revenue_col].quantile(0.25)
    q2 = df[revenue_col].quantile(0.50)
    q3 = df[revenue_col].quantile(0.75)
    
    # Create cohorts
    def assign_cohort(revenue):
        if revenue <= q1:
            return "Low Revenue"
        elif revenue <= q2:
            return "Medium-Low Revenue"
        elif revenue <= q3:
            return "Medium-High Revenue"
        else:
            return "High Revenue"
    
    df['Revenue_Cohort'] = df[revenue_col].apply(assign_cohort)
    return df

def create_variance_buckets(df, variance_col):
    """Create variance buckets"""
    if variance_col not in df.columns:
        st.error(f"Column '{variance_col}' not found in dataset")
        return df
    
    # Convert variance column to numeric, handling non-numeric values
    try:
        df_copy = df.copy()
        df_copy[variance_col] = pd.to_numeric(df_copy[variance_col], errors='coerce')
        # Remove rows with NaN values (non-convertible data)
        df_copy = df_copy.dropna(subset=[variance_col])
        
        if len(df_copy) == 0:
            st.error(f"No valid numeric data found in column '{variance_col}'. Please select a column with numeric variance data.")
            st.write("Sample data from this column:", df[variance_col].head())
            return df
            
        df = df_copy
    except Exception as e:
        st.error(f"Error converting '{variance_col}' to numeric: {e}")
        return df
    
    # Create variance buckets
    def assign_variance_bucket(variance):
        abs_variance = abs(variance)
        if abs_variance <= 5:
            return "Low (0-5%)"
        elif abs_variance <= 15:
            return "Medium (5-15%)"
        else:
            return "High (15%+)"
    
    df['Variance_Bucket'] = df[variance_col].apply(assign_variance_bucket)
    return df

def sub_dashboard_1(df, revenue_col, variance_col):
    """Sub-dashboard 1: Avg Variance % by Revenue Category"""
    st.markdown('<div class="sub-header">📊 Sub-Dashboard 1: Average Variance % by Revenue Cohort</div>', unsafe_allow_html=True)
    st.markdown("**Objective:** Analyze whether low-revenue or high-revenue kitchens are wasting more food.")
    
    if revenue_col not in df.columns or variance_col not in df.columns:
        st.error("Required columns not found in dataset")
        return
    
    # Process data
    df_processed = create_revenue_cohorts(df, revenue_col)
    
    # Check if Revenue_Cohort column was created successfully
    if 'Revenue_Cohort' not in df_processed.columns:
        st.error("❌ Could not create revenue cohorts. Please select a column with valid numeric revenue data.")
        return
    
    # Convert variance column to numeric
    df_processed[variance_col] = pd.to_numeric(df_processed[variance_col], errors='coerce')
    
    # Calculate average variance by cohort
    avg_variance_by_cohort = df_processed.groupby('Revenue_Cohort')[variance_col].agg([
        'mean', 'count', 'std'
    ]).round(2)
    avg_variance_by_cohort.columns = ['Avg_Variance_%', 'Store_Count', 'Std_Dev']
    avg_variance_by_cohort = avg_variance_by_cohort.reset_index()
    
    # Custom order for revenue cohorts
    cohort_order = ["Low Revenue", "Medium-Low Revenue", "Medium-High Revenue", "High Revenue"]
    avg_variance_by_cohort['Revenue_Cohort'] = pd.Categorical(
        avg_variance_by_cohort['Revenue_Cohort'], 
        categories=cohort_order, 
        ordered=True
    )
    avg_variance_by_cohort = avg_variance_by_cohort.sort_values('Revenue_Cohort')
    
    # Create enhanced visualization
    col1, col2 = st.columns([8, 4])
    
    with col1:
        # Modern bar chart with better styling
        fig = px.bar(
            avg_variance_by_cohort,
            x='Revenue_Cohort',
            y='Avg_Variance_%',
            title='Average Food Wastage by Revenue Cohort',
            labels={'Avg_Variance_%': 'Average Variance %', 'Revenue_Cohort': 'Revenue Cohort'},
            color='Avg_Variance_%',
            color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
            text='Avg_Variance_%'
        )
        
        # Enhanced styling
        fig.update_traces(
            texttemplate='%{text:.1f}%', 
            textposition='outside',
            textfont_size=14,
            textfont_color='#1e293b'
        )
        
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Revenue Cohort",
            yaxis_title="Average Variance %",
            title_font_size=20,
            title_font_color='#1e293b',
            xaxis=dict(
                tickfont_size=12,
                title_font_size=14,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            yaxis=dict(
                tickfont_size=12,
                title_font_size=14,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            height=500,
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Enhanced summary section
        st.markdown("#### 📊 Key Metrics")
        
        total_avg = df_processed[variance_col].mean()
        total_stores = len(df_processed)
        
        # Modern metric cards
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_avg:.1f}%</div>
            <div class="metric-label">Overall Average</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_stores:,}</div>
            <div class="metric-label">Total Stores</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced data table
        st.markdown("#### 📋 Detailed Results")
        display_df = avg_variance_by_cohort[['Revenue_Cohort', 'Avg_Variance_%', 'Store_Count']].copy()
        display_df['Avg_Variance_%'] = display_df['Avg_Variance_%'].round(1)
        display_df.columns = ['Cohort', 'Avg %', 'Stores']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Enhanced insights
        st.markdown("#### 💡 Key Insights")
        max_cohort = avg_variance_by_cohort.loc[avg_variance_by_cohort['Avg_Variance_%'].idxmax()]
        min_cohort = avg_variance_by_cohort.loc[avg_variance_by_cohort['Avg_Variance_%'].idxmin()]
        
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">🔴 Highest Wastage</div>
            <div class="insight-value">{max_cohort['Revenue_Cohort']}</div>
            <div style="color: #64748b; margin-top: 0.5rem;">{max_cohort['Avg_Variance_%']:.1f}% average wastage</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-card success">
            <div class="insight-title">🟢 Lowest Wastage</div>
            <div class="insight-value">{min_cohort['Revenue_Cohort']}</div>
            <div style="color: #64748b; margin-top: 0.5rem;">{min_cohort['Avg_Variance_%']:.1f}% average wastage</div>
        </div>
        """, unsafe_allow_html=True)

def sub_dashboard_2(df, revenue_col, variance_col, date_col=None):
    """Sub-dashboard 2: Store Count by Variance Bucket"""
    st.markdown('<div class="sub-header">📊 Sub-Dashboard 2: Store Count by Variance Buckets</div>', unsafe_allow_html=True)
    st.markdown("**Objective:** Analyze how food wastage is distributed across revenue levels and time periods.")
    
    if revenue_col not in df.columns or variance_col not in df.columns:
        st.error("Required columns not found in dataset")
        return
    
    # Process data
    df_processed = create_revenue_cohorts(df, revenue_col)
    
    # Check if Revenue_Cohort column was created successfully
    if 'Revenue_Cohort' not in df_processed.columns:
        st.error("❌ Could not create revenue cohorts. Please select a column with valid numeric revenue data.")
        return
    
    df_processed = create_variance_buckets(df_processed, variance_col)
    
    # Check if Variance_Bucket column was created successfully
    if 'Variance_Bucket' not in df_processed.columns:
        st.error("❌ Could not create variance buckets. Please select a column with valid numeric variance data.")
        return
    
    # Process date column if available
    has_date = False
    if date_col and date_col in df_processed.columns:
        try:
            # Try to convert to datetime
            df_processed[date_col] = pd.to_datetime(df_processed[date_col], errors='coerce')
            # Extract month
            df_processed['Month'] = df_processed[date_col].dt.strftime('%Y-%m')
            has_date = True
        except:
            st.warning(f"Could not convert '{date_col}' to date format. Proceeding without month analysis.")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Pivot Table", "📊 Visualization", "📈 Monthly Trends"])
    
    with tab1:
        st.markdown("### Store Count by Variance Bucket and Revenue Cohort")
        
        # Add a dummy column for counting
        df_processed['Count'] = 1
        
        # Create pivot table
        if has_date:
            pivot = pd.pivot_table(
                df_processed,
                values='Count',  # Use Count instead of Variance_Bucket
                index=['Month'],
                columns=['Variance_Bucket', 'Revenue_Cohort'],
                aggfunc='sum',  # Changed to sum from count since we're using a dummy column
                fill_value=0
            )
            
            # Format pivot table for display
            pivot = pivot.reset_index()
            st.dataframe(pivot, use_container_width=True)
            
            # Allow download of pivot data
            csv = pivot.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Pivot Data as CSV",
                csv,
                "variance_pivot.csv",
                "text/csv",
                key='download-pivot'
            )
        else:
            # Create pivot without month
            pivot = pd.pivot_table(
                df_processed,
                values='Count',  # Use Count instead of Variance_Bucket
                index=['Revenue_Cohort'],
                columns=['Variance_Bucket'],
                aggfunc='sum',  # Changed to sum from count
                fill_value=0
            )
            
            # Format pivot table for display
            pivot = pivot.reset_index()
            st.dataframe(pivot, use_container_width=True)
    
    with tab2:
        st.markdown("### Visualization of Store Count by Variance Bucket")
        
        # Count by variance bucket and revenue cohort
        counts = df_processed.groupby(['Variance_Bucket', 'Revenue_Cohort']).size().reset_index(name='Count')
        
        # Order for variance buckets and revenue cohorts
        variance_order = ["Low (0-5%)", "Medium (5-15%)", "High (15%+)"]
        revenue_order = ["Low Revenue", "Medium-Low Revenue", "Medium-High Revenue", "High Revenue"]
        
        # Set categorical order
        counts['Variance_Bucket'] = pd.Categorical(counts['Variance_Bucket'], categories=variance_order, ordered=True)
        counts['Revenue_Cohort'] = pd.Categorical(counts['Revenue_Cohort'], categories=revenue_order, ordered=True)
        
        # Sort by the ordered categories
        counts = counts.sort_values(['Variance_Bucket', 'Revenue_Cohort'])
        
        # Create enhanced stacked bar chart
        fig = px.bar(
            counts,
            x='Variance_Bucket',
            y='Count',
            color='Revenue_Cohort',
            title='Store Distribution by Variance Bucket and Revenue Cohort',
            labels={'Count': 'Number of Stores', 'Variance_Bucket': 'Variance Bucket'},
            category_orders={"Variance_Bucket": variance_order, "Revenue_Cohort": revenue_order},
            color_discrete_sequence=['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
        )
        
        fig.update_layout(
            xaxis_title="Variance Bucket",
            yaxis_title="Number of Stores",
            legend_title="Revenue Cohort",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=18,
            title_font_color='#1e293b',
            xaxis=dict(
                tickfont_size=12,
                title_font_size=14,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            yaxis=dict(
                tickfont_size=12,
                title_font_size=14,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.1)',
                borderwidth=1
            ),
            height=500,
            margin=dict(t=60, b=60, l=60, r=60)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if has_date:
            st.markdown("### Monthly Trends in Variance Distribution")
            
            # Group by month and variance bucket
            monthly_counts = df_processed.groupby(['Month', 'Variance_Bucket']).size().reset_index(name='Count')
            
            # Order months chronologically
            monthly_counts['Month'] = pd.Categorical(monthly_counts['Month'], ordered=True)
            monthly_counts = monthly_counts.sort_values('Month')
            
            # Set categorical order for variance buckets
            monthly_counts['Variance_Bucket'] = pd.Categorical(
                monthly_counts['Variance_Bucket'], 
                categories=variance_order, 
                ordered=True
            )
            
            # Create enhanced line chart
            fig = px.line(
                monthly_counts,
                x='Month',
                y='Count',
                color='Variance_Bucket',
                title='Monthly Trends in Variance Distribution',
                labels={'Count': 'Number of Stores', 'Month': 'Month'},
                markers=True,
                category_orders={"Variance_Bucket": variance_order},
                color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'],
            )
            
            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Number of Stores",
                legend_title="Variance Bucket",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_size=18,
                title_font_color='#1e293b',
                xaxis=dict(
                    tickfont_size=12,
                    title_font_size=14,
                    gridcolor='rgba(0,0,0,0.1)',
                    tickangle=45
                ),
                yaxis=dict(
                    tickfont_size=12,
                    title_font_size=14,
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                legend=dict(
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                height=500,
                margin=dict(t=60, b=80, l=60, r=60)
            )
            
            fig.update_traces(
                line_width=3,
                marker_size=8
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Date column not selected or could not be processed. Monthly trends are not available.")

def main():
    """Main function to run the dashboard"""
    # Professional header
    st.markdown('<div class="dashboard-header">📊 Variance-Level P&L Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Food Material Wastage Analysis for Cloud Kitchen Operations</div>', unsafe_allow_html=True)
    
    # Simple overview cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">📈</div>
            <div class="metric-label">Revenue Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">🗑️</div>
            <div class="metric-label">Wastage Tracking</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">📊</div>
            <div class="metric-label">Performance Metrics</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">📅</div>
            <div class="metric-label">Trend Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Load data with enhanced error handling
    df = load_data()
    
    if df is None:
        st.markdown("""
        <div class="warning-message">
            ⚠️ Failed to load data. Please check if 'dashborad_data.xlsx' exists in the current directory.
        </div>
        """, unsafe_allow_html=True)
        st.info("""
        **📋 Expected Data Structure:**
        - **Revenue Column**: Store revenue data for categorization
        - **Variance Column**: Food wastage percentage (variance %)
        - **Store ID**: Unique identifier for each store
        - **Date Column** (Optional): For time-based analysis
        """)
        return
    else:
        st.markdown("""
        <div class="success-message">
            ✅ Data loaded successfully! Ready for analysis.
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced sidebar with better styling
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <h2 style="color: #1e293b; margin: 0; font-weight: 700;">🔧 Configuration</h2>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Configure your analysis parameters</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset info with enhanced styling
    if df is not None:
        st.sidebar.markdown("### 📊 Dataset Overview")
        
        # Create two columns for metrics
        col_a, col_b = st.sidebar.columns(2)
        
        with col_a:
            st.sidebar.markdown(f"""
            <div class="metric-card" style="margin: 0.5rem 0;">
                <div class="metric-number" style="font-size: 1.8rem;">{len(df):,}</div>
                <div class="metric-label" style="font-size: 0.8rem;">Records</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.sidebar.markdown(f"""
            <div class="metric-card" style="margin: 0.5rem 0;">
                <div class="metric-number" style="font-size: 1.8rem;">{len(df.columns)}</div>
                <div class="metric-label" style="font-size: 0.8rem;">Columns</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 🎯 Column Selection")
    st.sidebar.markdown("*Choose the appropriate columns for analysis*")
    
    # Get numeric columns
    numeric_cols = get_numeric_columns(df)
    date_cols = get_date_columns(df)
    
    # Simple column selection
    revenue_col = st.sidebar.selectbox(
        "💰 Revenue Column",
        options=numeric_cols,
        help="Column containing store revenue data"
    )
    
    variance_col = st.sidebar.selectbox(
        "📊 Variance (%) Column",
        options=numeric_cols,
        help="Column containing food wastage percentage"
    )
    
    date_col = None
    if date_cols:
        date_col = st.sidebar.selectbox(
            "📅 Date Column (Optional)",
            options=["None"] + date_cols,
            help="Column containing date information for trends"
        )
        if date_col == "None":
            date_col = None
    
    # Simple validation
    if revenue_col and variance_col:
        st.sidebar.success("✅ Configuration complete")
    else:
        st.sidebar.warning("⚠️ Please select required columns")
    
    # Main analysis content
    if revenue_col and variance_col and not df[revenue_col].isna().all() and not df[variance_col].isna().all():
        
        # Create tabs for sub-dashboards
        tab1, tab2 = st.tabs(["Avg Variance by Revenue Cohort", "Store Count by Variance Bucket"])
        
        with tab1:
            sub_dashboard_1(df, revenue_col, variance_col)
        
        with tab2:
            sub_dashboard_2(df, revenue_col, variance_col, date_col)
        
        # Enhanced footer with professional styling
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #f8fafc, #e2e8f0); border-radius: 16px; border: 1px solid #e2e8f0;">
            <h4 style="color: #1e293b; margin-bottom: 1rem;">📊 Analysis Summary</h4>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
                <div style="text-align: center;">
                    <strong style="color: #667eea;">Variance Definition</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Food material wastage percentage</span>
                </div>
                <div style="text-align: center;">
                    <strong style="color: #667eea;">Revenue Cohorts</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Quartile-based categorization</span>
                </div>
                <div style="text-align: center;">
                    <strong style="color: #667eea;">Variance Buckets</strong><br>
                    <span style="color: #64748b; font-size: 0.9rem;">Low (0-5%), Medium (5-15%), High (15%+)</span>
                </div>
            </div>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #cbd5e1; color: #64748b; font-style: italic;">
                Built for optimizing cloud kitchen operations and reducing food wastage
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Enhanced error state with actionable guidance
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #fef3c7, #fed7aa); border-radius: 16px; margin: 2rem 0;">
            <h3 style="color: #92400e; margin-bottom: 1rem;">⚠️ Configuration Required</h3>
            <p style="color: #92400e; margin-bottom: 1.5rem;">Please select valid revenue and variance columns to begin your analysis.</p>
            <div style="background: rgba(255, 255, 255, 0.7); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <strong style="color: #92400e;">Quick Guide:</strong><br>
                <span style="color: #92400e; font-size: 0.9rem;">1. Select a numeric revenue column<br>2. Select a variance percentage column<br>3. Optionally add a date column for trends</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
