import joblib
from PIL import Image
import numpy as np
import requests
from io import BytesIO

# Load model once at startup
MODEL_PATH = "app/ml/model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"⚠️ Model not loaded: {e}")

async def predict_disease_from_file(file):
    """Predict disease from uploaded image"""
    if model is None:
        return "Model not loaded"
    img = Image.open(file.file).resize((128, 128))
    arr = np.array(img) / 255.0
    arr = arr.reshape(1, -1)
    result = model.predict(arr)[0]
    return result

async def predict_disease_from_url(image_url: str):
    """Predict disease from image URL"""
    if model is None:
        return "Model not loaded"
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).resize((128, 128))
    arr = np.array(img) / 255.0
    arr = arr.reshape(1, -1)
    result = model.predict(arr)[0]
    return result
