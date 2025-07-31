import os
from stegano import lsb
from PIL import Image

def detect_steganography(folder_path):
    results = []
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".jpg")]

    for filename in image_files:
        image_path = os.path.join(folder_path, filename)

        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")

            message = lsb.reveal(image_path)

            if message:
                results.append({
                    "filename": filename,
                    "status": "✅ Hidden message found",
                    "message": message
                })
            else:
                results.append({
                    "filename": filename,
                    "status": "❌ No message",
                    "message": None
                })

        except Exception as e:
            results.append({
                "filename": filename,
                "status": f"⚠️ Error: {e}",
                "message": None
            })
    return results
