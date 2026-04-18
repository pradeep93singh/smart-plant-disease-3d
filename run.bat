@echo off
cd /d "%~dp0"
if not exist .venv (
    python -m venv .venv
    .venv\Scripts\activate.bat && pip install -r requirements.txt -r frontend_streamlit/requirements.txt -r backend/requirements.txt
)
.venv\Scripts\activate.bat
start "Backend" cmd /k "cd backend && ..\\.venv\Scripts\\uvicorn app.main:app --reload --host 0.0.0.0 --port 8010"
set API_URL=http://127.0.0.1:8010
timeout /t 3 >nul
start "Frontend 3D UI" cmd /k "..\\.venv\Scripts\\streamlit run frontend_streamlit/app.py --server.port 8501 --server.headless true"
echo 🚀 Complete Plant App Suite Launched!
echo Backend API: http://localhost:8010/docs
echo Streamlit Desktop: http://localhost:8501
echo Mobile PWA APK: http://localhost:8080
echo All services auto-running!
pause
