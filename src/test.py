import os
from stegano import lsb
from PIL import Image

# Folder containing your image files
folder_path = "/home/kavita/LegalExpose/type01"  # CHANGE THIS

# List of all files ending in .jpg
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".jpg")]

# Loop through each image file
for filename in image_files:
    image_path = os.path.join(folder_path, filename)

    try:
        # Check if image can be opened and converted to RGB
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Ensure it's in the correct format

        # Try revealing hidden message
        message = lsb.reveal(image_path)

        if message:
            print(f"\n✅ {filename}: Hidden message found!")
            print(f"🔐 Message: {message}")
        else:
            print(f"\n❌ {filename}: No hidden message detected.")

    except Exception as e:
        print(f"\n⚠️ Error reading {filename}: {e}")


