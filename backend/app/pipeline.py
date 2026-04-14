import base64
from dataclasses import dataclass
from typing import Dict, Tuple

import cv2
import numpy as np


@dataclass
class ClassificationResult:
    plant_name: str
    disease_name: str
    confidence_score: float


def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image input")
    return image


def preprocess_leaf_image(image: np.ndarray) -> np.ndarray:
    image = cv2.resize(image, (512, 512))
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return image


def classify_disease(image: np.ndarray) -> ClassificationResult:
    # Placeholder hybrid output for transfer-learning classifier (EfficientNet/ResNet50).
    green_ratio = float(np.mean(image[:, :, 1]) / 255.0)
    if green_ratio > 0.45:
        return ClassificationResult("Tomato", "Healthy", 0.88)
    if green_ratio > 0.33:
        return ClassificationResult("Tomato", "Early Blight", 0.84)
    return ClassificationResult("Tomato", "Powdery Mildew", 0.81)


def segment_infected_region(image: np.ndarray) -> Tuple[np.ndarray, float]:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_lesion = np.array([5, 50, 30], dtype=np.uint8)
    upper_lesion = np.array([30, 255, 255], dtype=np.uint8)
    lesion_mask = cv2.inRange(hsv, lower_lesion, upper_lesion)
    lesion_mask = cv2.medianBlur(lesion_mask, 5)
    infected_pixels = np.count_nonzero(lesion_mask)
    total_pixels = lesion_mask.shape[0] * lesion_mask.shape[1]
    severity_percentage = (infected_pixels / max(total_pixels, 1)) * 100.0
    return lesion_mask, float(severity_percentage)


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
    lesion_mask, severity_pct = segment_infected_region(preprocessed)
    overlay = generate_overlay(preprocessed, lesion_mask)
    heatmap = generate_gradcam_like_heatmap(preprocessed)
    return {
        "plant_name": cls.plant_name,
        "disease_name": cls.disease_name,
        "confidence_score": round(cls.confidence_score, 4),
        "severity_percentage": round(severity_pct, 2),
        "affected_region_image_b64": to_base64_png(overlay),
        "explainability_heatmap_b64": to_base64_png(heatmap),
    }
