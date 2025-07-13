@echo off
echo Installing dependencies...
.venv\Scripts\pip.exe install -r requirements.txt

echo.
echo Starting Variance Analysis Dashboard...
echo Dashboard will open in your browser at http://localhost:8502
.venv\Scripts\streamlit.exe run vardashboard.py --server.port 8502
