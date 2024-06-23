from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://disease-classification.site",
    "http://89.116.20.192",
    "http://89.116.20.192:8000",
    "http://89.116.20.192:8000/predict",
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "../saved_models/3"
model = load_model(MODEL_PATH)

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy", "Undefined"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    try:
        image = np.array(Image.open(BytesIO(data)))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image data")
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        image = read_file_as_image(image_data)
        img_batch = np.expand_dims(image, 0)

        predictions = model.predict(img_batch)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])

        return {
            "class": predicted_class,
            "confidence": float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
