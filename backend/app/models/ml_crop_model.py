import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "app/ml/crop_model.pkl"

try:
    crop_model = joblib.load(MODEL_PATH)
    print("✅ Crop recommendation model loaded successfully")
except Exception as e:
    crop_model = None
    print(f"⚠️ Failed to load crop model: {e}")

# Soil encoding for categorical variable
SOIL_MAP = {
    "sandy": 0,
    "loamy": 1,
    "black": 2,
    "red": 3,
    "clay": 4
}

async def recommend_crop(soil_type: str, temperature: float, humidity: float, rainfall: float) -> str:
    """
    Predict best crop using trained model.
    - soil_type: categorical input (mapped to numeric)
    - temperature, humidity, rainfall: continuous features
    """
    if crop_model is None:
        raise Exception("Model not loaded")

    soil_encoded = SOIL_MAP.get(soil_type.lower())
    if soil_encoded is None:
        raise ValueError(f"Invalid soil type: {soil_type}")

    # Input vector for model prediction
    features = np.array([[soil_encoded, temperature, humidity, rainfall]])
    prediction = crop_model.predict(features)
    return prediction[0]
