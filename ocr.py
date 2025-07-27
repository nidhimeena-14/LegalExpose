import easyocr

def extract_text(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    text_content = " ".join([result[1] for result in results])
    return text_content
