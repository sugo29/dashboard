# Kitchen Dashboard Configuration
# Run this dashboard with: streamlit run kitchen_dashboard.py

## Features Included:
✅ **Filter Panel (Sidebar Controls)**
- Store selection
- Month selection  
- Zone selection
- Revenue Cohort selection
- CM Cohort selection
- EBITDA Category selection
- EBITDA Range slider

✅ **Kitchen Snapshot Table (Plotly Table)**
- Store-wise aggregated metrics
- Net Revenue, GM%, CM%, EBITDA values
- Professionally styled with color coding

✅ **Interactive Visualizations**
- Top 3 Kitchens by EBITDA (Bar Chart)
- Bottom 3 Kitchens by CM% (Bar Chart) 
- Revenue vs EBITDA Trend Over Time (Line Chart)

✅ **Derived Metrics**
- GM% = (Gross Margin / Net Revenue) × 100
- CM% = (Gross Margin / Net Revenue) × 100
- EBITDA% = (Kitchen EBITDA / Net Revenue) × 100

✅ **Key Insights Section**
- Negative EBITDA kitchen count
- High-revenue store performance
- Best performing store and zone
- Dynamic insights based on filters

✅ **Additional Features**
- Responsive design for all screen sizes
- Real-time filter updates
- Professional styling with custom CSS
- Currency formatting (₹)
- Conditional highlighting for performance metrics

## How to Run:
1. Install dependencies: pip install -r requirements.txt
2. Run dashboard: streamlit run kitchen_dashboard.py
3. Open browser at: http://localhost:8501
