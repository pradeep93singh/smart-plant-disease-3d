# Smart Plant Disease Detection - Advanced 3D App 🌿

## 🚀 Quick Start (Local)
```
.\\run.bat
```
- Backend: http://localhost:8010/docs
- Frontend 3D UI: http://localhost:8501

## ☁️ Free Hosting

### 1. Streamlit Cloud (Frontend + Backend)
1. `git add . && git commit -m \"Deploy\" && git push`
2. [streamlit.io](https://streamlit.io/cloud) → New app → GitHub repo → `frontend_streamlit/app.py` → Deploy
3. Public URL ready!

2. Render.com (Backend API - Free Tier)\n1. Go to [render.com](https://render.com) → Connect GitHub repo → New Web Service\n2. Root Directory: `backend/`\n3. Runtime: Python 3.12.3 (auto from runtime.txt)\n4. Build Command: `pip install -r requirements.txt`\n5. Start Command: `Procfile` (auto)\n6. Get public URL: https://your-app.onrender.com/docs\n\nUpdate frontend_streamlit/app.py API_URL to Render URL.

## 🐳 Docker Deploy
```
docker build -t plant3d .
docker run -p 8501:8501 -p 8010:8010 plant3d
```

## Features
- **3D Interactive**: Mesh3d lesions, volumetric plots, animations
- **Error-Proof**: Full validation/handling
- **IoT**: Real-time risk dashboard

Enjoy your hosted 3D plant app! 🔬
