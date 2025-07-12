import streamlit as st
from PIL import Image
import zipfile
import os
import io
import matplotlib.pyplot as plt
from model.predict import predict_image
from utils.db import save_history
from fpdf import FPDF
import tempfile
import plotly.graph_objects as go
from utils.auth_db import create_tables

create_tables()

# 🔒 Login check
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login_signup.py")

if "logged_in" not in st.session_state:
    st.warning("Please login to use the app.")
    st.stop()

# Page config
st.set_page_config(
    page_title="Steel Defect Detection",
    page_icon="assets/emoji.png",
    layout="wide"
)

# Header
col1, col2 = st.columns([1, 12])
with col1:
    st.image("assets/logo_emoji.png", width=600)
with col2:
    st.markdown("<h1 style='margin-top: 10px;'>Surface Defect Detection on Hot-Rolled Steel Strips</h1>", unsafe_allow_html=True)

# Session state
if 'recent_predictions' not in st.session_state:
    st.session_state.recent_predictions = []

# Upload UI
with st.expander("📥 Upload Image(s) or ZIP", expanded=True):
    uploaded_files = st.file_uploader(
        "Upload one or more images or ZIP file(s)",
        type=["png", "jpg", "jpeg", "zip", "bmp"],
        accept_multiple_files=True
    )

if uploaded_files:
    st.session_state.recent_predictions = []
    images = []

    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(".zip"):
            with zipfile.ZipFile(uploaded_file) as archive:
                for file in archive.namelist():
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                        img_data = archive.read(file)
                        img = Image.open(io.BytesIO(img_data)).convert("RGB").copy()
                        images.append((file, img))
        else:
            img = Image.open(uploaded_file).convert("RGB").copy()
            images.append((uploaded_file.name, img))

    batch_results = []

    for filename, img in images:
        st.markdown("---")
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img, caption=f"🖼 {filename}", width=300)
            with col2:
                with st.spinner("🔍 Predicting..."):
                    label, confidence = predict_image(img)
                    from utils.auth_db import save_user_prediction

                if label.lower() == "none":
                    st.markdown("### ❌ Not a Steel Strip Image")
                    st.info("This image does not appear to be a valid hot-rolled steel strip.")
                    continue

                if "username" in st.session_state:
                    save_user_prediction(st.session_state.username, filename, label, confidence)

                st.session_state.recent_predictions.append({
                    "Image": filename,
                    "Label": label,
                    "Confidence": f"{confidence:.2f}%"
                })
                batch_results.append((filename, label, confidence, img))

                emoji = "✅" if confidence >= 60 else "⚠"
                st.markdown(f"### {emoji} Prediction: {label}")
                st.markdown(f"Confidence: {confidence:.2f}%")

                # Bar chart
                fig = go.Figure(go.Bar(
                    x=[confidence],
                    y=["Confidence Level"],
                    orientation='h',
                    text=[f"{confidence:.2f}%"],
                    textposition='outside',
                    marker=dict(
                        color="green" if confidence >= 80 else "orange" if confidence >= 60 else "red",
                        line=dict(color='white', width=1)
                    )
                ))

                fig.update_layout(
                    xaxis=dict(range=[0, 100]),
                    yaxis=dict(showticklabels=False),
                    height=120,
                    margin=dict(l=10, r=10, t=10, b=10),
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )

                st.plotly_chart(fig, use_container_width=True, key=f"{filename}_confidence_chart")

                if confidence < 60:
                    st.warning("⚠ Low confidence result. This prediction may not be reliable.")

    # ✅ Export PDF if there are valid predictions
    if len(batch_results) > 1:
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for filename, label, confidence, pil_img in batch_results:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Prediction Report", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", size=11)
            pdf.cell(0, 10, f"Image: {filename}", ln=True)
            pdf.cell(0, 10, f"Prediction: {label}", ln=True)
            pdf.cell(0, 10, f"Confidence: {confidence:.2f}%", ln=True)
            pdf.ln(5)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                pil_img.save(tmp.name)
                pdf.image(tmp.name, x=10, y=None, w=100)

        pdf_buffer = io.BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin-1')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)

        st.markdown("""
        <style>
        .stDownloadButton button {
            background-color: #0099ff;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
        .stDownloadButton button:hover {
            background-color: #007acc;
        }
        </style>
        """, unsafe_allow_html=True)

        st.download_button(
            "📥 Download",
            data=pdf_buffer,
            file_name="batch_prediction_report.pdf",
            mime="application/pdf"
        )
