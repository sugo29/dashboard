@echo off
echo ====================================
echo Setting up Python 3.9.13 Virtual Environment
echo ====================================

echo.
echo Step 1: Checking if Python 3.9.13 is available...
python -c "import sys; print(f'Current Python version: {sys.version}')"

echo.
echo Step 2: Creating virtual environment with Python 3.9.13...
python -m venv venv_dashboard

echo.
echo Step 3: Activating virtual environment...
call venv_dashboard\Scripts\activate.bat

echo.
echo Step 4: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 5: Installing project dependencies...
pip install -r requirements.txt

echo.
echo Step 6: Verifying installation...
python -c "import streamlit, pandas, plotly; print('All packages installed successfully!')"
python -c "import sys; print(f'Virtual environment Python version: {sys.version}')"

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To activate the virtual environment manually:
echo   venv_dashboard\Scripts\activate.bat
echo.
echo To run the dashboard:
echo   streamlit run variance_dashboard.py
echo.
echo To deactivate the virtual environment:
echo   deactivate
echo ====================================

pause
