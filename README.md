
#  Project Title: LegalExpose


---

## Project Summary:
This project detects tampering in legal document fields using digital forensics and deep learning techniques. Specifically, it focuses on **signature tampering detection** using a fine-tuned CNN (MobileNetV2). The model is integrated into a **Streamlit dashboard** with various forensic modules.

---

##  How to Run the Dashboard (Executable File)

### 1. Clone or Download the Project Folder
Make sure the folder contains the following:
- `main_dashboard.py` (Streamlit dashboard)
- `DL/` (if applicable for structure)
- `train_signature_mobilenet.py` ( model training)
- `requirements.txt` (see below)
-  Model `.keras` file not included due to size — see next section)

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

### 3. Install Required Libraries
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```bash
streamlit run app.py
```

---

##  Model Notes:
- The DL model used is a **fine-tuned MobileNetV2**
- The model file (`signature_field_model_transfer.keras`) is **not included** here due to upload size restrictions.
- To test the dashboard with the model:
  1. Download the `.keras` model file (shared via Drive or other medium)
  2. Place it in the correct path as expected in `app.py`

---

##  Included Forensic Features:
- EXIF metadata extraction
- Timestamp comparison
- Noise & blur analysis
- OCR using EasyOCR
- Hash comparison (MD5, SHA256)
- ELA (Error Level Analysis)
- Steganography detection
- DL model for field-wise tampering (Signature)

---

##  Project Folder Structure (Expected)
```
LegalExpose/
├── app.py
├── train_signature_mobilenet.py
├── requirements.txt
├── README.md

```

---

##  Python Requirements
Here are all the libraries needed (for `requirements.txt`):

```txt
streamlit
tensorflow
numpy
opencv-python
matplotlib
Pillow
scikit-learn
easyocr
h5py
```
