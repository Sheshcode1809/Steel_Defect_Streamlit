# model/predict.py

import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load model once
model_path = os.path.join("model", "defect_model.h5")
model = tf.keras.models.load_model(model_path)

# Load class labels from folder names (sorted alphabetically)
class_names = sorted(os.listdir("dataset/train"))  # ['Crazing', 'Inclusion', ..., 'None']

def preprocess_image(image, target_size=(128, 128)):
    image = image.convert("L")  # grayscale
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0
    print(f"[DEBUG] Image shape: {image_array.shape}, max: {image_array.max()}, min: {image_array.min()}")
    return image_array.reshape(1, 128, 128, 1)


def predict_image(image):
    processed = preprocess_image(image)
    preds = model.predict(processed)
    print(f"[DEBUG] Prediction raw output: {preds}")  # Add this
    class_idx = np.argmax(preds)
    confidence = preds[0][class_idx] * 100
    return class_names[class_idx], confidence

    print(f"[DEBUG] Raw predictions: {preds}")
    print(f"[DEBUG] Predicted class: {class_names[class_idx]}, Confidence: {confidence:.2f}%")

    return class_names[class_idx], confidence
