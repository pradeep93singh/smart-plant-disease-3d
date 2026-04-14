from typing import Dict


DISEASE_KNOWLEDGE_BASE = {
    "healthy": {
        "disease_type": "none",
        "symptoms": ["No visible lesion", "Uniform leaf color"],
        "causes": ["No active disease detected"],
        "recommended_solution": ["Continue routine monitoring", "Maintain good irrigation schedule"],
        "prevention_tips": ["Use clean tools", "Apply crop rotation and sanitation"],
    },
    "early_blight": {
        "disease_type": "fungal",
        "symptoms": ["Brown concentric spots", "Yellowing around lesions"],
        "causes": ["Alternaria fungus", "High humidity and wet leaves"],
        "recommended_solution": ["Use fungicide approved for early blight", "Remove infected leaves immediately"],
        "prevention_tips": ["Avoid overhead watering", "Ensure air circulation between plants"],
    },
    "powdery_mildew": {
        "disease_type": "fungal",
        "symptoms": ["White powder-like coating", "Leaf curling"],
        "causes": ["Dry climate with humid nights", "Dense canopy"],
        "recommended_solution": ["Apply sulfur or potassium bicarbonate sprays", "Prune crowded foliage"],
        "prevention_tips": ["Use resistant varieties", "Water soil directly, not leaves"],
    },
}


def severity_to_level(severity_pct: float) -> str:
    if severity_pct < 15:
        return "low"
    if severity_pct < 40:
        return "medium"
    return "high"


def urgency_from_severity(severity_pct: float) -> str:
    if severity_pct < 15:
        return "monitor"
    if severity_pct < 40:
        return "priority"
    return "critical"


def yield_risk_from_severity(severity_pct: float) -> str:
    if severity_pct < 15:
        return "low risk"
    if severity_pct < 40:
        return "moderate risk"
    return "high risk"


def build_recommendation(disease_name: str, severity_pct: float) -> Dict:
    key = disease_name.lower().replace(" ", "_")
    profile = DISEASE_KNOWLEDGE_BASE.get(key, DISEASE_KNOWLEDGE_BASE["healthy"])
    return {
        "disease_type": profile["disease_type"],
        "symptoms": profile["symptoms"],
        "causes": profile["causes"],
        "recommended_solution": profile["recommended_solution"],
        "prevention_tips": profile["prevention_tips"],
        "severity_level": severity_to_level(severity_pct),
        "urgency_level": urgency_from_severity(severity_pct),
        "yield_risk": yield_risk_from_severity(severity_pct),
    }
