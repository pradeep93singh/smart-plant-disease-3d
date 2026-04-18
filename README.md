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

### 2. Render.com (Backend Free Tier)
1. [render.com](https://render.com) → New Web Service → GitHub → backend/app/main.py entrypoint.
2. Build: `pip install -r requirements.txt`
3. Public API URL.

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
