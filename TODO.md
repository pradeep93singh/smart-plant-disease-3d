# Render Deploy Plan - Approved & Implemented ✅

**Completed:**
- [x] backend/runtime.txt created (python-3.12.3)
- [x] backend/Procfile created (uvicorn app.main_deploy:app --port $PORT)
- [x] backend/app/main_deploy.py created (PORT env support)
- [x] README.md updated with exact Render steps

**Next Steps (User):**
1. `git add . && git commit -m "Add Render deploy config (blackboxai/render)" && git push`
2. render.com → New Web Service → GitHub repo → **Root: backend/** → Deploy (auto detects runtime/Procfile)
3. New URL: https://your-app-abc123.onrender.com/docs (free tier)
4. Test POST /analyze, GET /health
5. For frontend: Streamlit Cloud with API_URL=your-render-url

**Local Run:** `.\run.bat` (unchanged)

Deploy ready! 🚀
