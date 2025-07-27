from fpdf import FPDF

def sanitize_text(text):
    try:
        return str(text).encode("latin-1", "replace").decode("latin-1")
    except:
        return str(text)

def generate_report(
    ela_result, 
    hashes, 
    exif, 
    extracted_text, 
    created, 
    modified, 
    output_pdf, 
    steg_message=None, 
    final_label=None, 
    confidence=None,
    noise_heatmap_path=None,
    noise_highlighted_path=None
):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(0, 10, "Digital Document Forensic Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    # === Uploaded Image ===
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "Uploaded Image:", ln=True)
    pdf.set_font("Arial", size=12)
    try:
        pdf.image(ela_result, x=10, w=180)
    except:
        pdf.cell(0, 10, "(Image could not be loaded)", ln=True)

    pdf.ln(5)

    # === File Hashes ===
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "File Hashes:", ln=True)
    pdf.set_font("Arial", size=12)
    for k, v in hashes.items():
        pdf.multi_cell(0, 10, f"{sanitize_text(k)}: {sanitize_text(v)}")

    pdf.ln(5)

    # === EXIF Metadata ===
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "EXIF Metadata:", ln=True)
    pdf.set_font("Arial", size=12)
    if exif:
        for k, v in exif.items():
            pdf.multi_cell(0, 10, f"{sanitize_text(k)}: {sanitize_text(v)}")
    else:
        pdf.cell(0, 10, "No EXIF metadata found.", ln=True)

    pdf.ln(5)

    # === OCR Text ===
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "OCR Extracted Text:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, sanitize_text(extracted_text))

    pdf.ln(5)

    # === File Timestamps ===
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "File Timestamps:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Created: {sanitize_text(created)}", ln=True)
    pdf.cell(0, 10, f"Modified: {sanitize_text(modified)}", ln=True)

    pdf.ln(5)

    # === Steganography Result ===
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "Steganography Detection:", ln=True)
    pdf.set_font("Arial", size=12)
    if steg_message and "failed" not in steg_message.lower():
        pdf.multi_cell(0, 10, f"Hidden Message: {sanitize_text(steg_message)}")
    else:
        pdf.cell(0, 10, "No hidden message found.", ln=True)

    pdf.ln(5)

    # === DL Model Verdict ===
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "Deep Learning Tampering Prediction:", ln=True)
    pdf.set_font("Arial", size=12)
    if final_label and confidence is not None:
        pdf.cell(0, 10, f"Prediction: {sanitize_text(final_label)}", ln=True)
        pdf.cell(0, 10, f"Confidence: {confidence:.4f}", ln=True)
    else:
        pdf.cell(0, 10, "Model verdict not available.", ln=True)

    pdf.ln(5)

    # === Noise Residual Analysis ===
    if noise_heatmap_path or noise_highlighted_path:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 10, "Noise Residual Analysis (Variance Map):", ln=True)
        pdf.set_font("Arial", size=12)

        if noise_heatmap_path:
            try:
                pdf.cell(0, 10, "Variance Heatmap:", ln=True)
                pdf.image(noise_heatmap_path, x=10, w=180)
            except:
                pdf.cell(0, 10, "(Heatmap image could not be loaded)", ln=True)

        if noise_highlighted_path:
            try:
                pdf.cell(0, 10, "Highlighted Noisy Regions:", ln=True)
                pdf.image(noise_highlighted_path, x=10, w=180)
            except:
                pdf.cell(0, 10, "(Highlighted image could not be loaded)", ln=True)

    # === Save PDF ===
    pdf.output(output_pdf)
