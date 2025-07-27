import os
from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif_metadata(image_path):
    """
    Extracts metadata from an image file.
    Returns a dictionary of metadata.
    """
    metadata = {}
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                metadata[tag_name] = value
        else:
            metadata["Error"] = "No EXIF data found"

    except Exception as e:
        metadata["Error"] = f"Failed to extract metadata: {str(e)}"
    
    return metadata


# Optional: Run this as a standalone test
if __name__ == "__main__":
    test_image = "sample.jpg"  # Change this to your test image path
    if os.path.exists(test_image):
        result = extract_exif_metadata(test_image)
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print(f"Image not found: {test_image}")
