@echo off
echo ====================================
echo Starting Variance Level P&L Dashboard
echo ====================================

echo Activating virtual environment...
if exist "venv_dashboard\Scripts\activate.bat" (
    call venv_dashboard\Scripts\activate.bat
    echo Virtual environment activated successfully!
) else (
    echo Virtual environment not found. Please run setup_venv.bat first.
    pause
    exit /b 1
)

echo.
echo Checking dataset...
if exist "dashborad_data.xlsx" (
    echo Dataset found: dashborad_data.xlsx
) else (
    echo WARNING: Dataset file 'dashborad_data.xlsx' not found in current directory.
    echo Please make sure your data file is in the same folder as this script.
)

echo.
echo Starting Streamlit dashboard...
echo Dashboard will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run variance_dashboard.py
