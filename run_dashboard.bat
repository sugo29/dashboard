@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Exploring dataset structure...
python explore_data.py

echo.
echo Starting Streamlit dashboard...
echo Dashboard will open in your browser at http://localhost:8501
streamlit run variance_dashboard.py
