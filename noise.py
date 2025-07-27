import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_noise_residual(input_path, block_size=32, threshold=500, save=True, output_dir="output"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Read input image in grayscale
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not load image from path: {input_path}")

    h, w = img.shape
    var_map = np.zeros((h // block_size, w // block_size))

    # Step 2: Calculate variance block-wise
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = img[i:i + block_size, j:j + block_size]
            if block.shape == (block_size, block_size):
                var = np.var(block)
                var_map[i // block_size, j // block_size] = var

    # Step 3: Save Heatmap (if enabled)
    heatmap_path = os.path.join(output_dir, "variance_heatmap.png")
    if save:
        plt.imshow(var_map, cmap='hot')
        plt.colorbar()
        plt.title("Noise Variance Heatmap")
        plt.tight_layout()
        plt.savefig(heatmap_path)
        plt.close()

    # Step 4: Draw rectangles on regions with high variance
    color_img = cv2.imread(input_path)
    for i in range(var_map.shape[0]):
        for j in range(var_map.shape[1]):
            if var_map[i, j] > threshold:
                y1, y2 = i * block_size, (i + 1) * block_size
                x1, x2 = j * block_size, (j + 1) * block_size
                cv2.rectangle(color_img, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Black border

    highlighted_path = os.path.join(output_dir, "variance_highlighted.png")
    cv2.imwrite(highlighted_path, color_img)

    return var_map, heatmap_path, highlighted_path
