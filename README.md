# 🧠 Surface Defect Detection on Hot-Rolled Steel Strips

This project is a **Streamlit web application** for detecting surface defects in hot-rolled steel strips using a Convolutional Neural Network (CNN). It provides features such as user login, prediction history with SQLite, and PDF report export functionality.

---

## 📁 Project Structure

```
Steel_Defect_Streamlit_final/
│
├── app.py                      # Main Streamlit app
├── model.py                    # CNN model definition
├── database.py                 # SQLite DB functions (users, history)
├── auth.py                     # User authentication logic
├── pdf_export.py               # PDF report generation utility
├── utils.py                    # Preprocessing & helper functions
├── requirements.txt            # Required Python libraries
├── users.db                    # SQLite database for users and history
├── data/
│   └── sample_images/          # Test images for prediction
```

---

## 🚀 Features

- 🔍 **Surface Defect Detection** using deep learning (PyTorch CNN)
- 🔐 **User Authentication** (Sign up and log in)
- 🧠 **Real-time Predictions** on uploaded images
- 🗂️ **Prediction History** stored per user in SQLite
- 📄 **Export to PDF**: Generate downloadable reports

---

## 🛠️ Installation

### 1. Clone or Extract the Project

If you're using the zip file:
```bash
unzip Steel_Defect_Streamlit_final.zip
cd Steel_Defect_Streamlit_final
```

### 2. Set up Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

Use the following command to launch the Streamlit web application:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🖼️ How to Use

1. **Login** or **Sign Up** with your credentials.
2. **Upload an image OR zip file** of a steel strip.
3. The model will detect and classify the defect (if any).
4. You can **view your prediction history** from the sidebar.
5. **Export results as a PDF** for record-keeping.

---

## 🧪 Model Info

- CNN implemented with PyTorch
- Input: Steel surface image (PNG/JPG/JPEG/BMP)
- Output: Defect class label with prediction probability

---

## 📦 Dependencies

Major dependencies include:

- `streamlit`
- `numpy`
- `pandas`
- `opencv-python`
- `Pillow`
- `tensorflow`
- `scikit-learn`
- `matplotlib`
- `plotly`
- `fpdf`

See `requirements.txt` for the complete list.

---

## 🧰 Notes

- The model weights should be loaded within `model.py`. Ensure `model.pth` is placed correctly if loading external weights.
- The `users.db` SQLite database stores user credentials and prediction history.
- Custom CSS (`style.css`) enhances the appearance of the Streamlit interface.

---

## 🧑‍💻 Authors

Developed by **Shesh Kanade**  
For academic purposes and AI-based defect detection research.

---

## 📄 License

This project is licensed for **educational and research use only**.
