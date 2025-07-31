import streamlit as st
import os
from PIL import Image
import numpy as np
import tensorflow as tf
import hashlib
from datetime import datetime
from stegano import lsb
import cv2

from src.report import generate_report
from src.extract_exif import extract_exif
from src.ocr import extract_text
from src.noise import extract_noise_residual

# === CONFIG ===
PROJECT_NAME = "LegalExpose"
MODEL_PATH = "DL_MODEL.keras"  # ✅ updated for same-level model in Streamlit Cloud
IMAGE_SIZE = (128, 128)
NOISE_LOW = 3000
NOISE_HIGH = 9000

# === Ensure Output Directory Exists ===
if not os.path.exists("output"):
    os.makedirs("output")

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

model = load_model()

def compute_noise_variance(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return laplacian.var()

# === UI Title ===
st.title("📄 LegalExpose – Legal Document Tampering Detection")
st.markdown("Upload a scanned legal document image to start the forensic analysis.")

# === File Upload ===
uploaded_file = st.file_uploader("📤 Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="📎 Uploaded Document", use_column_width=True)
    image = Image.open(uploaded_file).convert("RGB")
    file_path = os.path.join("output", "temp_uploaded.jpg")
    image.save(file_path)

    # === EXIF Metadata ===
    st.markdown("---")
    st.subheader("📸 EXIF Metadata")
    exif_data = extract_exif(file_path)
    if exif_data:
        for key, val in exif_data.items():
            st.write(f"- **{key}**: {val}")
    else:
        st.info("No EXIF metadata found. This may indicate that the file was edited, downloaded, or scanned.")

    # === OCR Extraction ===
    st.markdown("---")
    st.subheader("📝 OCR Text")
    ocr_text = extract_text(file_path)
    st.text_area("Extracted Text", ocr_text, height=150)

    # === File Hashing & Metadata ===
    st.markdown("---")
    st.subheader("🧾 File Info & Hash")
    created = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
    modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "rb") as f:
        data = f.read()
        sha256 = hashlib.sha256(data).hexdigest()
        md5 = hashlib.md5(data).hexdigest()

    st.write(f"- **Created:** {created}")
    st.write(f"- **Modified:** {modified}")
    st.write(f"- **SHA256 Hash:** `{sha256}`")
    st.write(f"- **MD5 Hash:** `{md5}`")

    # === Steganography Detection ===
    st.markdown("---")
    st.subheader("🕵️ Steganography Detection")
    try:
        hidden = lsb.reveal(file_path)
        if hidden:
            st.success("✅ Hidden message found:")
            st.code(hidden)
            steg_result = hidden
        else:
            st.info("❌ No hidden message detected.")
            steg_result = "None"
    except Exception as e:
        st.warning("Could not check steganography.")
        steg_result = "Check failed"

    # === DL Prediction ===
    st.markdown("---")
    st.subheader("🤖 Deep Learning Tampering Prediction")
    resized = image.resize(IMAGE_SIZE)
    array = np.array(resized) / 255.0
    array = np.expand_dims(array, axis=0)
    prob = model.predict(array)[0][0]
    label = "Tampered" if prob > 0.5 else "Original"
    confidence = prob if prob > 0.5 else 1 - prob
    st.write(f"- **DL Prediction:** `{label}`")
    st.write(f"- **Confidence:** `{confidence:.4f}`")

    # === Noise Analysis ===
    st.markdown("---")
    st.subheader("📊 Noise Residual & Variance Score")
    noise_score = compute_noise_variance(file_path)
    st.write(f"- **Noise Variance Score:** `{noise_score:.2f}`")

    if noise_score < NOISE_LOW:
        noise_verdict = "Clean"
        st.success("✅ Low noise. Likely original.")
    elif noise_score > NOISE_HIGH:
        noise_verdict = "Noisy"
        st.warning("⚠️ High noise. Possible tampering.")
    else:
        noise_verdict = "Moderate"
        st.info("ℹ️ Moderate noise. Needs manual review.")

    # === Heatmap ===
    try:
        _, heatmap_path, highlight_path = extract_noise_residual(file_path)
        st.image(heatmap_path, caption="🔥 Noise Heatmap", use_column_width=True)
        st.image(highlight_path, caption="📌 Highlighted Tampering Areas", use_column_width=True)
    except:
        st.warning("❌ Failed to generate noise heatmap.")
        heatmap_path = None
        highlight_path = None

    # === Final Verdict ===
    st.markdown("---")
    st.subheader("🔚 Final Verdict")
    if label == "Tampered" or noise_verdict == "Noisy":
        final = "Tampered"
    elif noise_verdict == "Moderate":
        final = "Possibly Tampered"
    else:
        final = "Original"

    st.markdown(f"**🧠 Model Prediction:** `{label}` with `{confidence*100:.2f}%` confidence")
    st.markdown(f"**📈 Noise Score:** `{noise_score:.2f}` → `{noise_verdict}`")
    st.markdown(f"### 🔎 Final Result: **`{final.upper()}`**")

    # === PDF Report ===
    st.markdown("---")
    st.subheader("📥 Generate PDF Forensic Report")
    if st.button("🧾 Download PDF Report"):
        output_pdf = os.path.join("output", "forensic_report.pdf")
        try:
            generate_report(
                ela_result=file_path,
                hashes={"SHA256": sha256, "MD5": md5},
                exif=exif_data,
                extracted_text=ocr_text,
                created=created,
                modified=modified,
                steg_message=steg_result,
                final_label=final,
                confidence=confidence,
                noise_heatmap_path=heatmap_path,
                noise_highlighted_path=highlight_path,
                output_pdf=output_pdf
            )
            with open(output_pdf, "rb") as f:
                st.download_button("📄 Download", f, file_name="forensic_report.pdf")
        except Exception as e:
            st.error(f"Failed to generate report: {e}")
