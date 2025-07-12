"""
Test script to verify month ordering is working correctly.
"""

import pandas as pd
import plotly.express as px

def test_month_ordering():
    """Test the month ordering in various dashboard functions."""
    
    # Load and process data same way as dashboard
    df = pd.read_excel('dummy_data.xlsx', header=0)
    if df.iloc[0, 0] == 'MONTH':
        df.columns = df.iloc[0]
        df = df.drop(df.index[0]).reset_index(drop=True)
        df.columns.name = None
    
    # Add required columns
    df['MONTH_DATE'] = pd.to_datetime(df['MONTH'], format='%b-%Y')
    df = df.sort_values('MONTH_DATE')
    
    # Calculate EBITDA_PERCENT for heatmap test
    for col in ['NET REVENUE', 'KITCHEN EBITDA']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['EBITDA_PERCENT'] = (df['KITCHEN EBITDA'] / df['NET REVENUE'] * 100).round(2)
    
    print("=== Month Ordering Test Results ===\n")
    
    # Test 1: Month filter ordering
    months_with_dates = df[['MONTH', 'MONTH_DATE']].drop_duplicates().sort_values('MONTH_DATE')
    print("1. Month Filter Order (should be chronological):")
    print(months_with_dates['MONTH'].tolist())
    print()
    
    # Test 2: Trend chart ordering
    trend_data = df.groupby(['MONTH', 'MONTH_DATE']).agg({
        'NET REVENUE': 'sum',
        'KITCHEN EBITDA': 'sum'
    }).reset_index()
    trend_data = trend_data.sort_values('MONTH_DATE')
    
    print("2. Trend Chart Month Order:")
    print(trend_data['MONTH'].tolist())
    print()
    
    # Test 3: Heat map column ordering
    heatmap_data = df.groupby(['CITY', 'MONTH', 'MONTH_DATE'])['EBITDA_PERCENT'].mean().reset_index()
    heatmap_data = heatmap_data.sort_values('MONTH_DATE')
    
    heatmap_matrix = heatmap_data.pivot(index='CITY', columns='MONTH', values='EBITDA_PERCENT')
    month_order = heatmap_data['MONTH'].unique()
    heatmap_matrix = heatmap_matrix.reindex(columns=month_order)
    
    print("3. Heat Map Column Order:")
    print(list(heatmap_matrix.columns))
    print()
    
    # Test 4: Verify chronological progression
    expected_order = ['Oct-2023', 'Nov-2023', 'Dec-2023', 'Jan-2024', 'Feb-2024', 'Mar-2024']
    actual_order = months_with_dates['MONTH'].tolist()
    
    print("4. Verification:")
    print(f"Expected: {expected_order}")
    print(f"Actual:   {actual_order}")
    print(f"Match: {expected_order == actual_order}")
    
    if expected_order == actual_order:
        print("\n✅ SUCCESS: Month ordering is working correctly!")
    else:
        print("\n❌ ERROR: Month ordering is still incorrect!")

if __name__ == "__main__":
    test_month_ordering()
