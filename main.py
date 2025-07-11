import os
import cv2
import numpy as np
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras import layers, models

# Constants
IMG_SIZE = 128
DATA_DIR = "dataset"
BATCH_SIZE = 32

def load_images_from_folder(folder_path, class_names):
    X, y = [], []
    for label, class_name in enumerate(class_names):
        class_dir = os.path.join(folder_path, class_name)
        if not os.path.isdir(class_dir):
            continue
        for file in os.listdir(class_dir):
            file_path = os.path.join(class_dir, file)
            if os.path.isfile(file_path):
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                    X.append(img / 255.0)
                    y.append(label)
                else:
                    print(f"[WARNING] Could not read image: {file_path}")
    return np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1), np.array(y)

def build_model(num_classes):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# MAIN
train_dir = os.path.join(DATA_DIR, "train")
valid_dir = os.path.join(DATA_DIR, "valid")
test_dir  = os.path.join(DATA_DIR, "test")

# Get class names from train folder
class_names = sorted([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))])
print(f"[INFO] Classes: {class_names}")

# Load data
print("[INFO] Loading training data...")
X_train, y_train = load_images_from_folder(train_dir, class_names)
print(f"[INFO] Training samples: {len(X_train)}")

print("[INFO] Loading validation data...")
X_valid, y_valid = load_images_from_folder(valid_dir, class_names)
print(f"[INFO] Validation samples: {len(X_valid)}")

print("[INFO] Loading test data...")
X_test, y_test = load_images_from_folder(test_dir, class_names)
print(f"[INFO] Test samples: {len(X_test)}")

# Build and train model
model = build_model(num_classes=len(class_names))
model.fit(X_train, y_train, epochs=10, validation_data=(X_valid, y_valid), batch_size=BATCH_SIZE)

# Evaluate
print("[INFO] Evaluating on test set...")
preds = model.predict(X_test)
pred_labels = np.argmax(preds, axis=1)
print(classification_report(y_test, pred_labels, target_names=class_names))

# Save model
os.makedirs("model", exist_ok=True)
model.save("model/defect_model.h5")
print("[INFO] Model saved to model/defect_model.h5")