from typing import Dict


DISEASE_KNOWLEDGE_BASE = {
    "healthy": {
        "disease_type": "none",
        "symptoms": ["No visible lesion", "Uniform leaf color", "Vibrant green foliage"],
        "causes": ["No active disease detected"],
        "recommended_solution": ["Continue routine monitoring", "Maintain good irrigation schedule", "Regular fertilization"],
        "prevention_tips": ["Use clean tools", "Apply crop rotation", "Sanitation practices"],
        "plant_care": ["Water weekly", "Full sun 6-8hrs", "Well-drained soil"],
    },
    "early_blight": {
        "disease_type": "fungal",
        "symptoms": ["Brown concentric spots with yellow halo", "Lesions on lower leaves", "Defoliation in advanced stages"],
        "causes": ["Alternaria solani fungus", "High humidity and wet leaves", "Poor air circulation"],
        "recommended_solution": ["Fungicide (chlorothalonil or mancozeb)", "Remove infected leaves immediately", "Mulch to prevent splash"],
        "prevention_tips": ["Avoid overhead watering", "Ensure air circulation", "Rotate crops 2-3 years"],
        "plant_care": ["Water at base", "Stake for airflow", "Fertilize balanced NPK"],
    },
    "powdery_mildew": {
        "disease_type": "fungal",
        "symptoms": ["White powder-like coating on leaves", "Leaf curling and distortion", "Premature leaf drop"],
        "causes": ["Erysiphe spp. fungus", "Dry climate with humid nights", "Dense canopy"],
        "recommended_solution": ["Sulfur or potassium bicarbonate sprays", "Prune crowded foliage", "Milk solution (1:9 dilution)"],
        "prevention_tips": ["Use resistant varieties", "Water soil directly not leaves", "Morning watering for quick dry"],
        "plant_care": ["Partial shade if hot climate", "Space plants 12-18in", "Organic compost"],
    },
    "bacterial_spot": {
        "disease_type": "bacterial",
        "symptoms": ["Small water-soaked spots", "Dark brown lesions with yellow halo", "Leaf shot-hole appearance"],
        "causes": ["Xanthomonas spp.", "Warm wet conditions", "Splash dispersal"],
        "recommended_solution": ["Copper-based bactericide", "Remove debris", "Avoid overhead irrigation"],
        "prevention_tips": ["Disease-free seeds", "Crop rotation", "Control weeds"],
        "plant_care": ["High potassium fertilizer", "Staked plants", "Mulch heavily"],
    },
    "leaf_rust": {
        "disease_type": "fungal",
        "symptoms": ["Orange pustules on underside", "Yellow spots upper surface", "Leaf yellowing"],
        "causes": ["Puccinia spp.", "Cool moist weather", "Alternate host nearby"],
        "recommended_solution": ["Triazole fungicides", "Eradicate barberry", "Resistant varieties"],
        "prevention_tips": ["Early detection", "Sanitation", "Spacing"],
        "plant_care": ["Full sun", "Good airflow", "Avoid excess nitrogen"],
    },
    "tomato_mosaic_virus": {
        "disease_type": "viral",
        "symptoms": ["Mosaic yellowing", "Stunted growth", "Fruit malformation"],
        "causes": ["ToMV virus", "Aphid transmission", "Infected tools"],
        "recommended_solution": ["Remove infected plants", "Control aphids", "No cure - prevent"],
        "prevention_tips": ["Virus-free seeds", "Weed control", "Disinfect tools"],
        "plant_care": ["Reflective mulch", "Stakes", "Balanced nutrition"],
    },
    "late_blight": {
        "disease_type": "oomycete",
        "symptoms": ["Dark lesions", "White fuzzy underside", "Rapid tissue death"],
        "causes": ["Phytophthora infestans", "Wet cool weather"],
        "recommended_solution": ["Mefenoxam + chlorothalonil", "Destroy debris"],
        "prevention_tips": ["Resistant varieties", "No night watering"],
        "plant_care": ["Excellent drainage", "Air circulation"],
    },
    "black_spot_rose": {
        "disease_type": "fungal",
        "symptoms": ["Black spots with yellow halo", "Leaf drop"],
        "causes": ["Diplocarpon rosae", "Wet foliage"],
        "recommended_solution": ["Fungicide every 7-14 days"],
        "prevention_tips": ["Morning watering", "Clean up leaves"],
        "plant_care": ["Roses: Full sun, prune spring"],
    },
    "apple_scab": {
        "disease_type": "fungal",
        "symptoms": ["Olive green velvety spots", "Fruit cracking"],
        "causes": ["Venturia inaequalis"],
        "recommended_solution": ["Captan sprays"],
        "prevention_tips": ["Rake leaves", "Resistant varieties"],
        "plant_care": ["Apples: Prune for light penetration"],
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


def build_recommendation(disease_name: str, severity_pct: float, plant_name: str = "") -> Dict:
    key = disease_name.lower().replace(" ", "_")
    profile = DISEASE_KNOWLEDGE_BASE.get(key, DISEASE_KNOWLEDGE_BASE["healthy"])
    return {
        "disease_type": profile["disease_type"],
        "symptoms": profile["symptoms"],
        "causes": profile["causes"],
        "recommended_solution": profile["recommended_solution"],
        "prevention_tips": profile["prevention_tips"],
        "plant_care": profile["plant_care"],
        "severity_level": severity_to_level(severity_pct),
        "urgency_level": urgency_from_severity(severity_pct),
        "yield_risk": yield_risk_from_severity(severity_pct),
    }
