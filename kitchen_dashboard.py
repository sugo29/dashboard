import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Kitchen-Level P&L Dashboard",
    page_icon="🏪",
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the dashboard data."""
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
    
    # Calculate derived metrics
    df['GM_PERCENT'] = (df['GROSS MARGIN'] / df['NET REVENUE'] * 100).round(2)
    df['CM_PERCENT'] = (df['GROSS MARGIN'] / df['NET REVENUE'] * 100).round(2)  # Using GM as CM proxy
    df['EBITDA_PERCENT'] = (df['KITCHEN EBITDA'] / df['NET REVENUE'] * 100).round(2)
    
    # Convert MONTH to datetime for better sorting
    df['MONTH_DATE'] = pd.to_datetime(df['MONTH'], format='%b-%Y')
    df = df.sort_values('MONTH_DATE')
    
    return df

def create_filters(df):
    """Create sidebar filters."""
    st.sidebar.markdown("## 📊 Dashboard Filters")
    
    # Store filter
    stores = ['All'] + sorted(df['STORE'].unique().tolist())
    selected_store = st.sidebar.selectbox("Select Store", stores)
    
    # Month filter - sorted chronologically
    months_with_dates = df[['MONTH', 'MONTH_DATE']].drop_duplicates().sort_values('MONTH_DATE')
    months = ['All'] + months_with_dates['MONTH'].tolist()
    selected_month = st.sidebar.selectbox("Select Month", months)
    
    # Zone filter
    zones = ['All'] + sorted(df['ZONE MAPPING'].unique().tolist())
    selected_zone = st.sidebar.selectbox("Select Zone", zones)
    
    # Revenue Cohort filter
    revenue_cohorts = ['All'] + sorted(df['REVENUE COHORT'].unique().tolist())
    selected_revenue_cohort = st.sidebar.selectbox("Select Revenue Cohort", revenue_cohorts)
    
    # CM Cohort filter
    cm_cohorts = ['All'] + sorted(df['CM COHORT'].unique().tolist())
    selected_cm_cohort = st.sidebar.selectbox("Select CM Cohort", cm_cohorts)
    
    # EBITDA Category filter
    ebitda_categories = ['All'] + sorted(df['EBITDA CATEGORY'].unique().tolist())
    selected_ebitda_category = st.sidebar.selectbox("Select EBITDA Category", ebitda_categories)
    
    # EBITDA Range slider
    min_ebitda = float(df['EBITDA_PERCENT'].min())
    max_ebitda = float(df['EBITDA_PERCENT'].max())
    ebitda_range = st.sidebar.slider(
        "Select EBITDA % Range",
        min_value=min_ebitda,
        max_value=max_ebitda,
        value=(min_ebitda, max_ebitda),
        step=0.1
    )
    
    return {
        'store': selected_store,
        'month': selected_month,
        'zone': selected_zone,
        'revenue_cohort': selected_revenue_cohort,
        'cm_cohort': selected_cm_cohort,
        'ebitda_category': selected_ebitda_category,
        'ebitda_range': ebitda_range
    }

def filter_data(df, filters):
    """Apply filters to the dataframe."""
    filtered_df = df.copy()
    
    if filters['store'] != 'All':
        filtered_df = filtered_df[filtered_df['STORE'] == filters['store']]
    
    if filters['month'] != 'All':
        filtered_df = filtered_df[filtered_df['MONTH'] == filters['month']]
    
    if filters['zone'] != 'All':
        filtered_df = filtered_df[filtered_df['ZONE MAPPING'] == filters['zone']]
    
    if filters['revenue_cohort'] != 'All':
        filtered_df = filtered_df[filtered_df['REVENUE COHORT'] == filters['revenue_cohort']]
    
    if filters['cm_cohort'] != 'All':
        filtered_df = filtered_df[filtered_df['CM COHORT'] == filters['cm_cohort']]
    
    if filters['ebitda_category'] != 'All':
        filtered_df = filtered_df[filtered_df['EBITDA CATEGORY'] == filters['ebitda_category']]
    
    # Apply EBITDA range filter
    filtered_df = filtered_df[
        (filtered_df['EBITDA_PERCENT'] >= filters['ebitda_range'][0]) &
        (filtered_df['EBITDA_PERCENT'] <= filters['ebitda_range'][1])
    ]
    
    return filtered_df

def create_kitchen_snapshot_table(df):
    """Create the kitchen snapshot table using Plotly."""
    # Aggregate data by store for the table
    table_data = df.groupby('STORE').agg({
        'ZONE MAPPING': 'first',  # Get the zone for each store
        'NET REVENUE': 'sum',
        'GM_PERCENT': 'mean',
        'CM_PERCENT': 'mean',
        'KITCHEN EBITDA': 'sum',
        'EBITDA_PERCENT': 'mean'
    }).round(2).reset_index()
    
    # Format currency values
    table_data['NET REVENUE'] = table_data['NET REVENUE'].apply(lambda x: f"₹{x:,.0f}")
    table_data['KITCHEN EBITDA'] = table_data['KITCHEN EBITDA'].apply(lambda x: f"₹{x:,.0f}")
    
    # Create Plotly table
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Store', 'Zone', 'Net Revenue', 'GM %', 'CM %', 'EBITDA (₹)', 'EBITDA %'],
            fill_color='#1f77b4',
            font=dict(color='white', size=12),
            align='center'
        ),
        cells=dict(
            values=[
                table_data['STORE'],
                table_data['ZONE MAPPING'],
                table_data['NET REVENUE'],
                table_data['GM_PERCENT'],
                table_data['CM_PERCENT'],
                table_data['KITCHEN EBITDA'],
                table_data['EBITDA_PERCENT']
            ],
            fill_color=[['#f8f9fa', '#e9ecef'] * len(table_data)],
            align='center',
            font=dict(size=11)
        )
    )])
    
    fig.update_layout(
        title="📋 Kitchen Snapshot Table",
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_top_kitchens_ebitda(df):
    """Create top 3 kitchens by EBITDA chart."""
    top_kitchens = df.groupby('STORE')['KITCHEN EBITDA'].sum().nlargest(3).reset_index()
    
    fig = px.bar(
        top_kitchens,
        x='STORE',
        y='KITCHEN EBITDA',
        title='🏆 Top 3 Kitchens by EBITDA',
        color='KITCHEN EBITDA',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        xaxis_title="Store",
        yaxis_title="Kitchen EBITDA (₹)",
        showlegend=False,
        height=400
    )
    
    # Format y-axis to show currency
    fig.update_traces(
        texttemplate='₹%{y:,.0f}',
        textposition='outside'
    )
    
    return fig

def create_bottom_kitchens_cm(df):
    """Create bottom 3 kitchens by CM% chart."""
    bottom_kitchens = df.groupby('STORE')['CM_PERCENT'].mean().nsmallest(3).reset_index()
    
    fig = px.bar(
        bottom_kitchens,
        x='STORE',
        y='CM_PERCENT',
        title='📉 Bottom 3 Kitchens by CM %',
        color='CM_PERCENT',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        xaxis_title="Store",
        yaxis_title="Contribution Margin %",
        showlegend=False,
        height=400
    )
    
    # Add percentage formatting
    fig.update_traces(
        texttemplate='%{y:.1f}%',
        textposition='outside'
    )
    
    return fig

def create_revenue_ebitda_trend(df):
    """Create Revenue vs EBITDA trend over time."""
    # Aggregate by month, preserving chronological order
    trend_data = df.groupby(['MONTH', 'MONTH_DATE']).agg({
        'NET REVENUE': 'sum',
        'KITCHEN EBITDA': 'sum'
    }).reset_index()
    
    # Sort by date to ensure proper chronological order
    trend_data = trend_data.sort_values('MONTH_DATE')
    
    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add revenue line
    fig.add_trace(
        go.Scatter(
            x=trend_data['MONTH'],
            y=trend_data['NET REVENUE'],
            mode='lines+markers',
            name='Net Revenue',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ),
        secondary_y=False,
    )
    
    # Add EBITDA line
    fig.add_trace(
        go.Scatter(
            x=trend_data['MONTH'],
            y=trend_data['KITCHEN EBITDA'],
            mode='lines+markers',
            name='Kitchen EBITDA',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8)
        ),
        secondary_y=True,
    )
    
    # Set x-axis title
    fig.update_xaxes(title_text="Month")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Net Revenue (₹)", secondary_y=False)
    fig.update_yaxes(title_text="Kitchen EBITDA (₹)", secondary_y=True)
    
    fig.update_layout(
        title="📈 Revenue vs EBITDA Trend Over Time",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_city_performance_heatmap(df):
    """Create a heat map showing city performance over months."""
    # Aggregate data by city and month, preserving chronological order
    heatmap_data = df.groupby(['CITY', 'MONTH', 'MONTH_DATE'])['EBITDA_PERCENT'].mean().reset_index()
    
    # Sort by date to ensure proper chronological order
    heatmap_data = heatmap_data.sort_values('MONTH_DATE')
    
    # Pivot to create matrix for heatmap (using the sorted data)
    heatmap_matrix = heatmap_data.pivot(index='CITY', columns='MONTH', values='EBITDA_PERCENT')
    
    # Get the correct month order from the sorted data
    month_order = heatmap_data['MONTH'].unique()
    heatmap_matrix = heatmap_matrix.reindex(columns=month_order)
    
    # Create heatmap
    fig = px.imshow(
        heatmap_matrix,
        labels=dict(x="Month", y="City", color="EBITDA %"),
        title="🗺️ City Performance Heat Map - EBITDA % by Month",
        color_continuous_scale="RdYlGn",
        aspect="auto"
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Month",
        yaxis_title="City"
    )
    
    return fig

def create_india_map_visualization(df):
    """Create India map visualization showing city-wise performance."""
    # Define coordinates for major Indian cities (approximate)
    city_coordinates = {
        'Mumbai': [19.0760, 72.8777],
        'Delhi': [28.6139, 77.2090],
        'Bangalore': [12.9716, 77.5946],
        'Hyderabad': [17.3850, 78.4867],
        'Ahmedabad': [23.0225, 72.5714],
        'Chennai': [13.0827, 80.2707],
        'Kolkata': [22.5726, 88.3639],
        'Pune': [18.5204, 73.8567],
        'Jaipur': [26.9124, 75.7873],
        'Surat': [21.1702, 72.8311],
        'Lucknow': [26.8467, 80.9462],
        'Kanpur': [26.4499, 80.3319],
        'Nagpur': [21.1458, 79.0882],
        'Indore': [22.7196, 75.8577],
        'Thane': [19.2183, 72.9781],
        'Bhopal': [23.2599, 77.4126],
        'Visakhapatnam': [17.6868, 83.2185],
        'Patna': [25.5941, 85.1376],
        'Vadodara': [22.3072, 73.1812],
        'Ghaziabad': [28.6692, 77.4538],
        'Ludhiana': [30.9000, 75.8573],
        'Agra': [27.1767, 78.0081],
        'Nashik': [19.9975, 73.7898],
        'Faridabad': [28.4089, 77.3178],
        'Meerut': [28.9845, 77.7064],
        'Rajkot': [22.3039, 70.8022],
        'Kalyan': [19.2437, 73.1355],
        'Vasai': [19.4326, 72.8397],
        'Varanasi': [25.3176, 82.9739],
        'Srinagar': [34.0837, 74.7973],
        'Aurangabad': [19.8762, 75.3433],
        'Dhanbad': [23.7957, 86.4304],
        'Amritsar': [31.6340, 74.8723],
        'Allahabad': [25.4358, 81.8463],
        'Ranchi': [23.3441, 85.3096],
        'Howrah': [22.5958, 88.2636],
        'Coimbatore': [11.0168, 76.9558],
        'Jabalpur': [23.1815, 79.9864],
        'Gwalior': [26.2183, 78.1828],
        'Vijayawada': [16.5062, 80.6480],
        'Jodhpur': [26.2389, 73.0243],
        'Madurai': [9.9252, 78.1198],
        'Raipur': [21.2514, 81.6296],
        'Kota': [25.2138, 75.8648],
        'Guwahati': [26.1445, 91.7362],
        'Chandigarh': [30.7333, 76.7794],
        'Solapur': [17.6599, 75.9064],
        'Hubli': [15.3647, 75.1240],
        'Tiruchirappalli': [10.7905, 78.7047],
        'Bareilly': [28.3670, 79.4304]
    }
    
    # Aggregate data by city
    city_data = df.groupby('CITY').agg({
        'EBITDA_PERCENT': 'mean',
        'NET REVENUE': 'sum',
        'KITCHEN EBITDA': 'sum',
        'STORE': 'nunique'
    }).round(2).reset_index()
    
    # Add coordinates to city data
    city_data['lat'] = city_data['CITY'].map(lambda x: city_coordinates.get(x, [0, 0])[0])
    city_data['lon'] = city_data['CITY'].map(lambda x: city_coordinates.get(x, [0, 0])[1])
    
    # Filter out cities without coordinates
    city_data = city_data[(city_data['lat'] != 0) & (city_data['lon'] != 0)]
    
    # Create India map
    fig = px.scatter_geo(
        city_data,
        lat='lat',
        lon='lon',
        size='NET REVENUE',
        color='EBITDA_PERCENT',
        hover_name='CITY',
        hover_data={
            'EBITDA_PERCENT': ':.1f',
            'NET REVENUE': ':,.0f',
            'KITCHEN EBITDA': ':,.0f',
            'STORE': True,
            'lat': False,
            'lon': False
        },
        color_continuous_scale="RdYlGn",
        size_max=50,
        title="🇮🇳 India Map - City Performance Overview"
    )
    
    # Focus on India
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
        showcountries=True,
        countrycolor="white",
        lataxis_range=[6, 37],  # India's latitude range
        lonaxis_range=[68, 97]  # India's longitude range
    )
    
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_insights(df):
    """Generate insights based on the filtered data."""
    insights = []
    
    # Store metrics breakdown
    total_unique_stores = df['STORE'].nunique()
    total_active_records = len(df[df['STATUS'] == 'Active'])
    total_inactive_records = len(df[df['STATUS'] == 'Inactive'])
    active_unique_stores = df[df['STATUS'] == 'Active']['STORE'].nunique()
    inactive_unique_stores = df[df['STATUS'] == 'Inactive']['STORE'].nunique()
    
    insights.append(f"🏪 **Store Overview**: {total_unique_stores} total unique stores ({active_unique_stores} active, {inactive_unique_stores} inactive)")
    insights.append(f"📊 **Records**: {total_active_records} active records, {total_inactive_records} inactive records")
    
    # Count negative EBITDA kitchens
    negative_ebitda_count = len(df[df['KITCHEN EBITDA'] < 0]['STORE'].unique())
    insights.append(f"🔴 {negative_ebitda_count} kitchens have negative EBITDA")
    
    # High revenue stores CM%
    high_revenue_stores = df[df['REVENUE COHORT'] == '>40 L']
    if not high_revenue_stores.empty:
        avg_cm_high_revenue = high_revenue_stores['CM_PERCENT'].mean()
        insights.append(f"📊 Average CM% for high-revenue stores (>40L): {avg_cm_high_revenue:.1f}%")
    
    # Best performing store
    if not df.empty:
        best_store = df.groupby('STORE')['KITCHEN EBITDA'].sum().idxmax()
        best_ebitda = df.groupby('STORE')['KITCHEN EBITDA'].sum().max()
        insights.append(f"🏆 Best performing store: {best_store} (₹{best_ebitda:,.0f} EBITDA)")
    
    # Zone performance
    zone_performance = df.groupby('ZONE MAPPING')['EBITDA_PERCENT'].mean().idxmax()
    insights.append(f"🎯 Best performing zone: {zone_performance}")
    
    return insights

def main():
    """Main dashboard function."""
    # Load data
    df = load_data()
    
    # Header
    st.markdown('<div class="main-header">🏪 Kitchen-Level Profit & Loss Dashboard</div>', unsafe_allow_html=True)
    
    # Create filters
    filters = create_filters(df)
    
    # Apply filters
    filtered_df = filter_data(df, filters)
    
    # Check if filtered data is empty
    if filtered_df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
        return
    
    # Display key metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        total_revenue = filtered_df['NET REVENUE'].sum()
        st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
    
    with col2:
        total_ebitda = filtered_df['KITCHEN EBITDA'].sum()
        st.metric("📊 Total EBITDA", f"₹{total_ebitda:,.0f}")
    
    with col3:
        avg_ebitda_percent = filtered_df['EBITDA_PERCENT'].mean()
        st.metric("📈 Avg EBITDA %", f"{avg_ebitda_percent:.1f}%")
    
    with col4:
        unique_active_stores = filtered_df['STORE'].nunique()
        st.metric("🏪 Unique Active Stores", unique_active_stores)
    
    with col5:
        total_active_records = len(filtered_df[filtered_df['STATUS'] == 'Active'])
        st.metric("📊 Total Active Records", total_active_records)
    
    with col6:
        # Calculate total active store-months (each store per month counts as 1)
        total_store_months = len(filtered_df)
        st.metric("📈 Total Store-Months", total_store_months)
    
    st.markdown("---")
    
    # Add explanatory section for store metrics
    with st.expander("📖 Understanding Store Metrics & Data Info"):
        # Get original dataset stats
        original_total_stores = df['STORE'].nunique()
        original_active_stores = df[df['STATUS'] == 'Active']['STORE'].nunique()
        original_inactive_stores = df[df['STATUS'] == 'Inactive']['STORE'].nunique()
        
        st.markdown(f"""
        **Current Dataset Overview:**
        - **Total Stores in Dataset**: {original_total_stores} distinct stores
        - **Active Stores in Dataset**: {original_active_stores} distinct stores  
        - **Inactive Stores in Dataset**: {original_inactive_stores} distinct stores
        - **Total Records**: {len(df)} rows
        
        **Filtered Results (based on your current filters):**
        - **Unique Active Stores**: Number of distinct store names in your filtered dataset
        - **Total Active Records**: Count of records where STATUS = 'Active' 
        - **Total Store-Months**: Total number of data points (each store per month = 1 record)
        
        *Note: If you expect 300+ stores, this dataset might be a sample or subset of your full data.*
        """)
        
        # Show month breakdown
        month_breakdown = df.groupby('MONTH')['STORE'].nunique().reset_index()
        month_breakdown.columns = ['Month', 'Unique Stores']
        st.markdown("**Stores per Month:**")
        st.dataframe(month_breakdown, use_container_width=True)
    
    # Kitchen Snapshot Table
    st.plotly_chart(create_kitchen_snapshot_table(filtered_df), use_container_width=True)
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_top_kitchens_ebitda(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_bottom_kitchens_cm(filtered_df), use_container_width=True)
    
    # Revenue vs EBITDA trend
    st.plotly_chart(create_revenue_ebitda_trend(filtered_df), use_container_width=True)
    
    # Heat Map and India Map visualizations
    st.markdown("## 🗺️ Geographical Performance Analysis")
    
    # Charts row 2 - Heat maps
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_city_performance_heatmap(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_india_map_visualization(filtered_df), use_container_width=True)
    
    # Insights section
    st.markdown("## 💡 Key Insights")
    insights = create_insights(filtered_df)
    
    for insight in insights:
        st.markdown(f"- {insight}")
    
    # Footer
    st.markdown("---")
    st.markdown("**Dashboard built with Streamlit & Plotly** | Data refreshed in real-time based on filters")

if __name__ == "__main__":
    main()
