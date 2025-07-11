import pandas as pd
import streamlit as st

def explore_dataset():
    """Explore the dataset structure"""
    try:
        # Load the dataset
        df = pd.read_excel('dashborad_data.xlsx')
        
        print("=== DATASET EXPLORATION ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\n=== COLUMN DATA TYPES ===")
        print(df.dtypes)
        print("\n=== FIRST FEW ROWS ===")
        print(df.head())
        print("\n=== BASIC STATISTICS ===")
        print(df.describe())
        print("\n=== MISSING VALUES ===")
        print(df.isnull().sum())
        
        # Look for potential variance and revenue columns
        print("\n=== POTENTIAL COLUMN MAPPING ===")
        
        potential_revenue_cols = []
        potential_variance_cols = []
        potential_date_cols = []
        
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['revenue', 'sales', 'income', 'turnover']):
                potential_revenue_cols.append(col)
            if any(keyword in col_lower for keyword in ['variance', 'diff', 'variation', '%', 'percent']):
                potential_variance_cols.append(col)
            if any(keyword in col_lower for keyword in ['date', 'month', 'time', 'period']):
                potential_date_cols.append(col)
        
        print(f"Potential Revenue Columns: {potential_revenue_cols}")
        print(f"Potential Variance Columns: {potential_variance_cols}")
        print(f"Potential Date Columns: {potential_date_cols}")
        
        return df
        
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    explore_dataset()
