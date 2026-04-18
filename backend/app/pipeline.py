import base64
from dataclasses import dataclass
from typing import Dict, Tuple, List

import cv2
import numpy as np

@dataclass
class ClassificationResult:
    plant_name: str
    disease_name: str
    confidence_score: float

def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    if len(image_bytes) == 0 or len(image_bytes) > 10*1024*1024:  # Max 10MB
        raise ValueError("Invalid image size")
    arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None or len(image.shape) != 3:
        raise ValueError("Invalid image input")
    return image

def preprocess_leaf_image(image: np.ndarray) -> np.ndarray:
    if image.shape[0] < 32 or image.shape[1] < 32:
        raise ValueError("Image too small")
    image = cv2.resize(image, (512, 512))
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return image

def classify_disease(image: np.ndarray) -> ClassificationResult:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size
    
    green_ratio = np.mean(image[:, :, 1]) / 255.0
    red_ratio = np.mean(image[:, :, 2]) / 255.0
    variance = np.var(gray)
    
    # Multi-plant classification based on texture/color stats
    if edge_density < 0.05 and green_ratio > 0.45:
        return ClassificationResult("Healthy Tomato", "healthy", 0.92)
    elif variance < 1000 and green_ratio > 0.4:
        return ClassificationResult("Rose", "black_spot_rose", 0.87)
    elif red_ratio > 0.35 and edge_density > 0.08:
        return ClassificationResult("Apple", "apple_scab", 0.85)
    elif edge_density > 0.12 and green_ratio < 0.3:
        return ClassificationResult("Potato", "late_blight", 0.83)
    elif green_ratio > 0.35 and 0.2 < edge_density < 0.1:
        return ClassificationResult("Tomato", "early_blight", 0.84)
    elif green_ratio > 0.25 and variance > 2000:
        return ClassificationResult("Tomato", "bacterial_spot", 0.82)
    elif green_ratio > 0.3 and edge_density < 0.07:
        return ClassificationResult("Cucumber", "powdery_mildew", 0.81)
    elif red_ratio > 0.4:
        return ClassificationResult("Pepper", "leaf_rust", 0.80)
    elif edge_density > 0.15:
        return ClassificationResult("Tomato", "tomato_mosaic_virus", 0.79)
    else:
        return ClassificationResult("Unknown Plant", "healthy", 0.70)

def segment_infected_region(image: np.ndarray) -> Tuple[np.ndarray, float, List[List[float]]]:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_lesion = np.array([5, 50, 30], dtype=np.uint8)
    upper_lesion = np.array([30, 255, 255], dtype=np.uint8)
    lesion_mask = cv2.inRange(hsv, lower_lesion, upper_lesion)
    lesion_mask = cv2.medianBlur(lesion_mask, 5)
    contours, _ = cv2.findContours(lesion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_list = [contour.flatten().tolist() for contour in contours[:3]]  # Top 3
    infected_pixels = np.count_nonzero(lesion_mask)
    total_pixels = lesion_mask.shape[0] * lesion_mask.shape[1]
    severity_percentage = (infected_pixels / max(total_pixels, 1)) * 100.0
    return lesion_mask, float(severity_percentage), contours_list

def generate_overlay(image: np.ndarray, lesion_mask: np.ndarray) -> np.ndarray:
    overlay = image.copy()
    red = np.zeros_like(image)
    red[:, :, 2] = 255
    overlay = np.where(lesion_mask[:, :, None] > 0, cv2.addWeighted(image, 0.4, red, 0.6, 0), overlay)
    return overlay

def generate_gradcam_like_heatmap(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    heat = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    return cv2.addWeighted(image, 0.5, heat, 0.5, 0)

def to_base64_png(image: np.ndarray) -> str:
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError("Failed to encode visualization")
    return base64.b64encode(buffer.tobytes()).decode("utf-8")

def run_analysis(image_bytes: bytes) -> Dict:
    image = decode_image_bytes(image_bytes)
    preprocessed = preprocess_leaf_image(image)
    cls = classify_disease(preprocessed)
    lesion_mask, severity_pct, lesion_contours = segment_infected_region(preprocessed)
    overlay = generate_overlay(preprocessed, lesion_mask)
    heatmap = generate_gradcam_like_heatmap(preprocessed)
    return {
        "plant_name": cls.plant_name,
        "disease_name": cls.disease_name,
        "confidence_score": round(cls.confidence_score, 4),
        "severity_percentage": round(severity_pct, 2),
        "lesion_contours": lesion_contours,
        "affected_region_image_b64": to_base64_png(overlay),
        "explainability_heatmap_b64": to_base64_png(heatmap),
    }
