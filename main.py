from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("https://drive.google.com/drive/folders/1FOvLG0fTL2SxjxGPIeSHe_whnZypkuJI?usp=sharing")
##model change from local value
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
    file: UploadFile = File(None),
    blob_file: bytes = Form(None)
):
    if not file and not blob_file:
        raise HTTPException(status_code=400, detail="No file provided")

    if file:
        image = read_file_as_image(await file.read())
    elif blob_file:
        image = read_file_as_image(blob_file)

    img_batch = np.expand_dims(image, 0)
    
    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
