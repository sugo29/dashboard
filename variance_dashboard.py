import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page config
st.set_page_config(
    page_title="Variance-Level P&L Dashboard - Food Wastage Analysis",
    page_icon="🗑️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data():
    """Load and process the dataset"""
    try:
        # Load the Excel file
        df = pd.read_excel('dashborad_data.xlsx')
        
        # Display basic info about the dataset
        st.sidebar.write("Dataset Info:")
        st.sidebar.write(f"Rows: {len(df)}")
        st.sidebar.write(f"Columns: {len(df.columns)}")
        st.sidebar.write("Columns:", list(df.columns))
        
        # Show data types to help user select appropriate columns
        st.sidebar.write("Column Data Types:")
        for col in df.columns:
            dtype = str(df[col].dtype)
            # Check if column contains mostly numeric data
            numeric_count = pd.to_numeric(df[col], errors='coerce').count()
            total_count = len(df[col])
            numeric_ratio = numeric_count / total_count if total_count > 0 else 0
            
            if numeric_ratio > 0.8:  # More than 80% numeric
                st.sidebar.write(f"📊 {col}: {dtype} (Numeric-like)")
            else:
                st.sidebar.write(f"📝 {col}: {dtype}")
        
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

def create_revenue_cohorts(df, revenue_col):
    """Create revenue cohorts based on quartiles"""
    if revenue_col not in df.columns:
        return df
    
    # Convert revenue column to numeric, handling non-numeric values
    try:
        original_count = len(df)
        df_copy = df.copy()
        df_copy[revenue_col] = pd.to_numeric(df_copy[revenue_col], errors='coerce')
        # Remove rows with NaN values (non-convertible data)
        df_copy = df_copy.dropna(subset=[revenue_col])
        
        if len(df_copy) == 0:
            st.error(f"❌ No valid numeric data found in column '{revenue_col}'.")
            st.error(f"📋 Sample values from '{revenue_col}': {list(df[revenue_col].head(5))}")
            st.error("💡 Please select a column that contains actual revenue numbers (like sales amounts, revenue figures, etc.)")
            return df  # Return original df to avoid KeyError
            
        if len(df_copy) < original_count * 0.5:  # Lost more than 50% of data
            st.warning(f"⚠️ Warning: Only {len(df_copy)} out of {original_count} rows contain valid numeric data in '{revenue_col}' column.")
            
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
            return "Low Revenue (Q1)"
        elif revenue <= q2:
            return "Medium-Low Revenue (Q2)"
        elif revenue <= q3:
            return "Medium-High Revenue (Q3)"
        else:
            return "High Revenue (Q4)"
    
    df['Revenue_Cohort'] = df[revenue_col].apply(assign_cohort)
    return df

def create_variance_buckets(df, variance_col):
    """Create variance buckets"""
    if variance_col not in df.columns:
        return df
    
    # Convert variance column to numeric, handling non-numeric values
    try:
        df[variance_col] = pd.to_numeric(df[variance_col], errors='coerce')
        # Remove rows with NaN values (non-convertible data)
        df = df.dropna(subset=[variance_col])
        
        if len(df) == 0:
            st.error(f"No valid numeric data found in column '{variance_col}'. Please select a column with numeric variance data.")
            return df
            
    except Exception as e:
        st.error(f"Error converting '{variance_col}' to numeric: {e}")
        return df
    
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
    st.markdown('<div class="sub-header">📊 Sub-Dashboard 1: Average Variance % by Revenue Category</div>', unsafe_allow_html=True)
    st.markdown("**Purpose:** Analyze food material wastage by revenue cohorts")
    st.markdown("**Key Question:** Do low-revenue stores waste more food?")
    
    if revenue_col not in df.columns or variance_col not in df.columns:
        st.error("Required columns not found in dataset")
        return
    
    # Process data
    df_processed = create_revenue_cohorts(df, revenue_col)
    
    # Check if Revenue_Cohort column was created successfully
    if 'Revenue_Cohort' not in df_processed.columns:
        st.error("❌ Could not create revenue cohorts. Please select a column with valid numeric revenue data.")
        st.info("💡 Look for columns marked with 📊 in the sidebar - these contain numeric-like data suitable for analysis.")
        return
    
    # Calculate average variance by cohort
    avg_variance_by_cohort = df_processed.groupby('Revenue_Cohort')[variance_col].agg([
        'mean', 'count', 'std'
    ]).round(2)
    avg_variance_by_cohort.columns = ['Avg_Variance_%', 'Store_Count', 'Std_Dev']
    avg_variance_by_cohort = avg_variance_by_cohort.reset_index()
    
    # Sort by revenue level for better visualization
    cohort_order = ["Low Revenue (Q1)", "Medium-Low Revenue (Q2)", "Medium-High Revenue (Q3)", "High Revenue (Q4)"]
    avg_variance_by_cohort['Revenue_Cohort'] = pd.Categorical(avg_variance_by_cohort['Revenue_Cohort'], categories=cohort_order, ordered=True)
    avg_variance_by_cohort = avg_variance_by_cohort.sort_values('Revenue_Cohort')
    
    # Create columns for visualization
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Bar chart showing average variance by revenue category
        fig1 = px.bar(
            avg_variance_by_cohort,
            x='Revenue_Cohort',
            y='Avg_Variance_%',
            title='Average Food Wastage (Variance %) by Revenue Category',
            color='Avg_Variance_%',
            color_continuous_scale='Reds',
            text='Avg_Variance_%',
            labels={
                'Revenue_Cohort': 'Revenue Category',
                'Avg_Variance_%': 'Average Wastage %'
            }
        )
        fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig1.update_layout(
            height=500, 
            showlegend=False,
            xaxis_title="Revenue Category",
            yaxis_title="Average Wastage %"
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Summary table
        st.markdown("### 📊 Summary Table")
        summary_table = avg_variance_by_cohort[['Revenue_Cohort', 'Avg_Variance_%', 'Store_Count']].copy()
        summary_table.columns = ['Revenue Category', 'Avg Wastage %', 'Store Count']
        st.dataframe(summary_table, hide_index=True, use_container_width=True)
        
        # Key insights
        st.markdown("### 💡 Key Insights")
        highest_waste = avg_variance_by_cohort.loc[avg_variance_by_cohort['Avg_Variance_%'].idxmax()]
        lowest_waste = avg_variance_by_cohort.loc[avg_variance_by_cohort['Avg_Variance_%'].idxmin()]
        
        st.markdown(f"""
        <div class="metric-card">
            <strong>🔴 Highest Wastage:</strong><br>
            {highest_waste['Revenue_Cohort']}<br>
            <span style="color: red; font-size: 1.1em;">{highest_waste['Avg_Variance_%']:.1f}% wastage</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <strong>🟢 Lowest Wastage:</strong><br>
            {lowest_waste['Revenue_Cohort']}<br>
            <span style="color: green; font-size: 1.1em;">{lowest_waste['Avg_Variance_%']:.1f}% wastage</span>
        </div>
        """, unsafe_allow_html=True)

def sub_dashboard_2(df, revenue_col, variance_col, date_col=None):
    """Sub-dashboard 2: Store Count by Variance Buckets"""
    st.markdown('<div class="sub-header">🔹 Sub-Dashboard 2: Store Count by Variance Buckets</div>', unsafe_allow_html=True)
    st.markdown("**Purpose:** Show distribution of stores across variance levels by revenue and time")
    
    if revenue_col not in df.columns or variance_col not in df.columns:
        st.error("Required columns not found in dataset")
        return
    
    # Process data
    df_processed = create_revenue_cohorts(df, revenue_col)
    
    # Check if Revenue_Cohort column was created successfully
    if 'Revenue_Cohort' not in df_processed.columns:
        st.error("❌ Could not create revenue cohorts. Please select a column with valid numeric revenue data.")
        st.info("💡 Look for columns marked with 📊 in the sidebar - these contain numeric-like data suitable for analysis.")
        return
        
    df_processed = create_variance_buckets(df_processed, variance_col)
    
    # Add month column if date is available
    if date_col and date_col in df.columns:
        try:
            df_processed[date_col] = pd.to_datetime(df_processed[date_col])
            df_processed['Month'] = df_processed[date_col].dt.strftime('%Y-%m')
        except:
            st.warning("Could not parse date column. Proceeding without time analysis.")
            date_col = None
    
    # Main pivot table: Rows = Months, Columns = Revenue buckets, Values = Count of stores
    if date_col and 'Month' in df_processed.columns:
        st.markdown("### 📋 Main Analysis Table: Store Count by Month and Revenue Category")
        st.markdown("**Rows:** Months | **Columns:** Revenue Categories | **Values:** Store Count")
        
        # Create the main pivot table
        main_pivot = df_processed.pivot_table(
            index='Month',
            columns='Revenue_Cohort',
            values=variance_col,  # We just need to count, so any column works
            aggfunc='count',
            fill_value=0
        )
        
        # Reorder columns for better display
        cohort_order = ["Low Revenue (Q1)", "Medium-Low Revenue (Q2)", "Medium-High Revenue (Q3)", "High Revenue (Q4)"]
        main_pivot = main_pivot.reindex(columns=cohort_order, fill_value=0)
        
        # Display the table with styling
        st.dataframe(
            main_pivot.style.background_gradient(cmap='Blues'),
            use_container_width=True
        )
        
        # Additional analysis by variance buckets
        st.markdown("### 📊 Variance Bucket Analysis by Month and Revenue")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["By Variance Buckets", "Monthly Trends", "Summary Stats"])
        
        with tab1:
            st.markdown("**Table: Store count by Variance Buckets and Revenue Categories**")
            variance_revenue_pivot = df_processed.pivot_table(
                index='Revenue_Cohort',
                columns='Variance_Bucket',
                values=variance_col,
                aggfunc='count',
                fill_value=0
            )
            
            # Reorder variance buckets
            bucket_order = ["Low (0-5%)", "Medium (5-15%)", "High (15%+)"]
            variance_revenue_pivot = variance_revenue_pivot.reindex(columns=bucket_order, fill_value=0)
            
            st.dataframe(
                variance_revenue_pivot.style.background_gradient(cmap='Reds'),
                use_container_width=True
            )
        
        with tab2:
            st.markdown("**Monthly Trend: Store Count by Variance Bucket**")
            monthly_variance_pivot = df_processed.pivot_table(
                index='Month',
                columns='Variance_Bucket',
                values=variance_col,
                aggfunc='count',
                fill_value=0
            )
            monthly_variance_pivot = monthly_variance_pivot.reindex(columns=bucket_order, fill_value=0)
            
            # Line chart for trends
            fig_trend = px.line(
                monthly_variance_pivot.reset_index(),
                x='Month',
                y=bucket_order,
                title='Monthly Trend: Store Count by Variance Bucket',
                labels={'value': 'Store Count', 'Month': 'Month'},
                color_discrete_map={
                    'Low (0-5%)': '#2ecc71',
                    'Medium (5-15%)': '#f39c12', 
                    'High (15%+)': '#e74c3c'
                }
            )
            fig_trend.update_layout(height=400)
            st.plotly_chart(fig_trend, use_container_width=True)
            
            st.dataframe(
                monthly_variance_pivot.style.background_gradient(cmap='Oranges'),
                use_container_width=True
            )
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Total Store Distribution by Variance Bucket**")
                total_by_bucket = df_processed['Variance_Bucket'].value_counts()
                for bucket in bucket_order:
                    if bucket in total_by_bucket.index:
                        count = total_by_bucket[bucket]
                        pct = (count / len(df_processed)) * 100
                        color = {'Low (0-5%)': 'green', 'Medium (5-15%)': 'orange', 'High (15%+)': 'red'}[bucket]
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong>{bucket}</strong><br>
                            <span style="color: {color}; font-size: 1.1em;">{count} stores ({pct:.1f}%)</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Store Distribution by Revenue Category**")
                total_by_revenue = df_processed['Revenue_Cohort'].value_counts()
                for cohort in cohort_order:
                    if cohort in total_by_revenue.index:
                        count = total_by_revenue[cohort]
                        pct = (count / len(df_processed)) * 100
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong>{cohort.replace(' (Q', ' Q').replace(')', '')}</strong><br>
                            <span style="color: #1f77b4; font-size: 1.1em;">{count} stores ({pct:.1f}%)</span>
                        </div>
                        """, unsafe_allow_html=True)
    
    else:
        # If no date column, show simplified analysis
        st.markdown("### 📊 Store Count Analysis (No Time Data Available)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Store Count by Variance Buckets and Revenue Categories**")
            variance_revenue_pivot = df_processed.pivot_table(
                index='Revenue_Cohort',
                columns='Variance_Bucket',
                values=variance_col,
                aggfunc='count',
                fill_value=0
            )
            
            bucket_order = ["Low (0-5%)", "Medium (5-15%)", "High (15%+)"]
            variance_revenue_pivot = variance_revenue_pivot.reindex(columns=bucket_order, fill_value=0)
            
            st.dataframe(
                variance_revenue_pivot.style.background_gradient(cmap='Reds'),
                use_container_width=True
            )
        
        with col2:
            # Pie chart for overall distribution
            fig_pie = px.pie(
                values=df_processed['Variance_Bucket'].value_counts().values,
                names=df_processed['Variance_Bucket'].value_counts().index,
                title='Overall Store Distribution by Variance Bucket',
                color_discrete_map={
                    'Low (0-5%)': '#2ecc71',
                    'Medium (5-15%)': '#f39c12', 
                    'High (15%+)': '#e74c3c'
                }
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

def main():
    """Main function to run the dashboard"""
    st.markdown('<div class="main-header">🗑️ Variance-Level P&L Dashboard - Food Wastage Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Purpose: Analyze Food Material Wastage and Performance Impact
    **Note:** "Variance" = Food Material Wastage = Loss
    
    This dashboard helps answer key questions:
    - 📊 Do low-revenue stores waste more food?
    - 📈 How are stores distributed across wastage levels?
    - 📅 Are there seasonal patterns in food wastage?
    """)
    
    # Load data
    df = load_and_process_data()
    
    if df is None:
        st.error("Could not load the dataset. Please check if 'dashborad_data.xlsx' exists in the current directory.")
        st.info("""
        **Expected data structure:**
        - **Revenue Column**: Store revenue data for categorization
        - **Variance Column**: Food wastage percentage (variance %)
        - **Store ID**: Unique identifier for each store
        - **Date Column** (Optional): For time-based analysis
        """)
        return
    
    # Sidebar for column selection
    st.sidebar.markdown("## 🔧 Column Mapping")
    st.sidebar.markdown("Map your dataset columns to the required fields:")
    
    # Column selection
    available_columns = list(df.columns)
    numeric_columns = get_numeric_columns(df)
    
    st.sidebar.markdown("**💡 Tip:** Look for columns marked with 📊 (numeric-like data)")
    
    revenue_col = st.sidebar.selectbox(
        "📈 Select Revenue Column:",
        options=available_columns,
        help="Column containing revenue data for creating revenue categories. Should contain numeric values."
    )
    
    # Show warning if selected column is not numeric-like
    if revenue_col not in numeric_columns:
        st.sidebar.warning(f"⚠️ '{revenue_col}' may not contain numeric data. Consider selecting a different column.")
    
    variance_col = st.sidebar.selectbox(
        "🗑️ Select Variance/Wastage % Column:",
        options=available_columns,
        help="Column containing food wastage percentage data. Should contain numeric values."
    )
    
    # Show warning if selected column is not numeric-like
    if variance_col not in numeric_columns:
        st.sidebar.warning(f"⚠️ '{variance_col}' may not contain numeric data. Consider selecting a different column.")
    
    date_col = st.sidebar.selectbox(
        "📅 Select Date Column (Optional):",
        options=['None'] + available_columns,
        help="Column containing date/month data for trend analysis"
    )
    date_col = None if date_col == 'None' else date_col
    
    # Data preview
    st.sidebar.markdown("## 📋 Data Preview")
    if st.sidebar.checkbox("Show Raw Data"):
        st.markdown("### Raw Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
    
    # Filter options
    st.sidebar.markdown("## 🔍 Filters")
    
    # Date filter if date column is available
    if date_col and date_col in df.columns:
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            date_range = st.sidebar.date_input(
                "Select Date Range:",
                value=(df[date_col].min().date(), df[date_col].max().date()),
                min_value=df[date_col].min().date(),
                max_value=df[date_col].max().date()
            )
            if len(date_range) == 2:
                df = df[(df[date_col].dt.date >= date_range[0]) & (df[date_col].dt.date <= date_range[1])]
        except:
            st.sidebar.warning("Could not parse date column")
    
    # Show dashboards
    if revenue_col and variance_col:
        # Sub-dashboard 1
        sub_dashboard_1(df, revenue_col, variance_col)
        
        st.markdown("---")
        
        # Sub-dashboard 2
        sub_dashboard_2(df, revenue_col, variance_col, date_col)
        
        # Business insights
        st.markdown("---")
        st.markdown("## 💡 Actionable Business Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🔍 Key Questions Answered:
            
            1. **📊 Revenue vs Wastage Correlation**
               - Do low-revenue stores waste more food?
               - Which revenue category has highest/lowest wastage?
            
            2. **📈 Wastage Distribution Analysis**
               - How many stores fall into each wastage bucket?
               - What's the overall wastage profile?
            
            3. **📅 Temporal Patterns**
               - Are there seasonal wastage trends?
               - Which months show higher food wastage?
            """)
        
        with col2:
            st.markdown("""
            ### 🎯 Recommended Actions:
            
            - **🔴 High Wastage Stores**: Immediate intervention needed
              - Implement portion control
              - Review inventory management
              - Staff training on food handling
            
            - **🟢 Low Wastage Stores**: Learn best practices
              - Document successful processes
              - Share learnings across network
              - Use as benchmark stores
            
            - **📈 Performance Monitoring**
              - Weekly wastage tracking
              - Monthly trend analysis
              - Revenue impact assessment
            """)
    else:
        st.warning("⚠️ Please select the required columns from the sidebar to generate the dashboard.")

if __name__ == "__main__":
    main()
