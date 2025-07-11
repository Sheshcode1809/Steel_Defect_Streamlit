# utils/pdf_export.py
from fpdf import FPDF
import io
from PIL import Image

def export_pdf(image, label, confidence):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Steel Defect Detection Report", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(100, 10, f"Prediction: {label}", ln=True)
    pdf.cell(100, 10, f"Confidence: {confidence:.2f}%", ln=True)
    
    # Save image temporarily and insert into PDF
    temp_path = "temp_img.jpg"
    image.save(temp_path)
    pdf.image(temp_path, x=10, y=50, w=120)

    # Get PDF as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # Convert to bytes
    return io.BytesIO(pdf_bytes)
