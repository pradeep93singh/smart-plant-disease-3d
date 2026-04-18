FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501 8010

CMD ["bash", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port 8010 & streamlit run frontend_streamlit/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true"]

