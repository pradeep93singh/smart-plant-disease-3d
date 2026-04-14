# Smart Plant Disease Detection, Severity Analysis, and Treatment Recommendation System

An advanced end-to-end AI agriculture project template with:

- Disease classification (placeholder for EfficientNet/ResNet50)
- Lesion localization and infected region highlighting
- Severity estimation (% affected area)
- Explainability heatmap (Grad-CAM style placeholder)
- Interactive 3D lesion/severity visualization in dashboard
- Recommendation engine (symptoms, causes, treatment, prevention)
- Optional IoT-based risk scoring (temperature, humidity, soil moisture)
- Scan history and dashboard-ready API endpoints

## Tech stack

- Backend: FastAPI, OpenCV, NumPy, SQLModel (SQLite)
- Frontend: Streamlit
- Models (pluggable): EfficientNet/ResNet50 + YOLO/Mask R-CNN

## Project structure

```text
backend/
  app/
    main.py
    pipeline.py
    recommendations.py
    iot.py
    storage.py
    schemas.py
frontend_streamlit/
  app.py
```

## Setup

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Run backend:

```bash
uvicorn app.main:app --reload --app-dir backend
```

4. Run frontend:

```bash
streamlit run frontend_streamlit/app.py
```

## One-click run (Windows PowerShell)

From project root:

```powershell
.\run.ps1
```

This script:
- Creates `.venv` if missing
- Installs dependencies
- Starts backend on `8010`
- Starts Streamlit on `8502`

To stop both services:

```powershell
.\stop.ps1
```

## API endpoints

- `GET /health` -> service health check
- `POST /analyze` -> leaf image analysis
- `POST /iot/sensor` -> optional IoT sensor ingestion
- `GET /history` -> latest scan records

## Current implementation notes

- `pipeline.py` contains a modular **placeholder pipeline** using OpenCV for quick prototyping.
- Replace `classify_disease()` with a trained EfficientNet/ResNet model.
- Replace `segment_infected_region()` with YOLO/Mask R-CNN lesion detection.
- Replace `generate_gradcam_like_heatmap()` with true Grad-CAM from your classifier.

## Suggested upgrade path

1. Train disease classifier on PlantVillage + field images.
2. Add lesion detection/segmentation model and evaluate IoU + mAP.
3. Add multilingual recommendation content.
4. Add notifications (SMS/WhatsApp/email) for `critical` urgency.
5. Add offline edge inference for rural/low-connectivity use.
