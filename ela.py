from PIL import Image, ImageChops, ImageEnhance
import os
import cv2
import numpy as np

def perform_ela(input_path, output_path):
    original = Image.open(input_path).convert('RGB')
    resaved_path = output_path.replace('.jpg', '_resaved.jpg')
    ela_path = output_path.replace('.jpg', '_ELA.jpg')
    ela_highlighted_path = output_path.replace('.jpg', '_ELA_highlighted.jpg')

    # Resave
    original.save(resaved_path, 'JPEG', quality=90)
    resaved = Image.open(resaved_path)

    # Diff
    diff = ImageChops.difference(original, resaved)
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff if max_diff != 0 else 1

    diff = ImageEnhance.Brightness(diff).enhance(scale)
    diff.save(ela_path)

    # Highlight
    diff_cv = cv2.cvtColor(np.array(diff), cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(diff_cv, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    orig_cv = cv2.cvtColor(np.array(original), cv2.COLOR_RGB2BGR)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 50:
            cv2.rectangle(orig_cv, (x, y), (x + w, y + h), (0, 0, 0), 2)  # Black box

    cv2.imwrite(ela_highlighted_path, orig_cv)

    return ela_path, ela_highlighted_path
