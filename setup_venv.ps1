# PowerShell script to set up Python 3.9.13 virtual environment
Write-Host "====================================" -ForegroundColor Green
Write-Host "Setting up Python 3.9.13 Virtual Environment" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

Write-Host "`nStep 1: Checking if Python 3.9.13 is available..." -ForegroundColor Yellow
python -c "import sys; print(f'Current Python version: {sys.version}')"

Write-Host "`nStep 2: Creating virtual environment with Python 3.9.13..." -ForegroundColor Yellow
python -m venv venv_dashboard

Write-Host "`nStep 3: Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_dashboard\Scripts\Activate.ps1"

Write-Host "`nStep 4: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host "`nStep 5: Installing project dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`nStep 6: Verifying installation..." -ForegroundColor Yellow
python -c "import streamlit, pandas, plotly; print('All packages installed successfully!')"
python -c "import sys; print(f'Virtual environment Python version: {sys.version}')"

Write-Host "`n====================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

Write-Host "`nTo activate the virtual environment manually:" -ForegroundColor Cyan
Write-Host "  .\venv_dashboard\Scripts\Activate.ps1" -ForegroundColor White

Write-Host "`nTo run the dashboard:" -ForegroundColor Cyan
Write-Host "  streamlit run variance_dashboard.py" -ForegroundColor White

Write-Host "`nTo deactivate the virtual environment:" -ForegroundColor Cyan
Write-Host "  deactivate" -ForegroundColor White

Write-Host "`n====================================" -ForegroundColor Green
