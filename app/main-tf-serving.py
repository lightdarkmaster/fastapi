from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import requests

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://disease-classification.site",
    "91.108.104.247"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

endpoint = "http://localhost:8501/v1/models/potatoes_model:predict"

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy", "Undefined"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    try:
        # Try to open the image using PIL
        image = np.array(Image.open(BytesIO(data)))
    except Exception as e:
        # If it fails, assume it's a blob and decode it
        try:
            image = np.array(Image.open(BytesIO(bytes(data))))
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid image data")
    return image

@app.post("/predict")
async def predict(
    blob_file: bytes = File(...)
):
    image = read_file_as_image(blob_file)
    img_batch = np.expand_dims(image, 0)

    json_data = {
        "instances": img_batch.tolist()
    }

    response = requests.post(endpoint, json=json_data)
    prediction = np.array(response.json()["predictions"][0])

    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    confidence = np.max(prediction)

    return {
        "class": predicted_class,
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    # uvicorn.run(app, host='localhost', port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")


## create an optimization in the current codebase..
## guess I need to change the port to available port within the server changing the localhost to actual server..