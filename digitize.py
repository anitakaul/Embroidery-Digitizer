import cv2
import numpy as np
from sklearn.metrics import pairwise_distances_argmin
from pyembroidery import EmbPattern, write_pes, STITCH

# Load your image
image_bgr = cv2.imread("your_image.png")
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

# 14 rainbow palette: light and dark of each main color
COLOR_PALETTE = np.array([
    [255, 100, 100], [139, 0, 0],      # red
    [255, 165, 100], [255, 69, 0],     # orange
    [255, 255, 153], [204, 204, 0],    # yellow
    [144, 238, 144], [0, 100, 0],      # green
    [173, 216, 230], [0, 0, 139],      # blue
    [138, 43, 226],  [75, 0, 130],     # indigo
    [216, 191, 216], [148, 0, 211],    # violet
])

def quantize_to_rainbow(image, palette):
    h, w, _ = image.shape
    flat = image.reshape(-1, 3)
    matched_idx = pairwise_distances_argmin(flat, palette)
    quantized = palette[matched_idx]
    return quantized.reshape(h, w, 3).astype(np.uint8)

quantized = quantize_to_rainbow(image_rgb, COLOR_PALETTE)

# Convert to grayscale and find contours
gray = cv2.cvtColor(quantized, cv2.COLOR_RGB2GRAY)
_, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create embroidery pattern
pattern = EmbPattern()
for contour in contours:
    if len(contour) < 2:
        continue
    first = True
    for pt in contour:
        x, y = pt[0]
        if first:
            pattern.add_stitch_absolute(STITCH, x / 10.0, y / 10.0)
            first = False
        else:
            pattern.add_stitch_absolute(STITCH, x / 10.0, y / 10.0)
pattern.end()

# Save to PES
write_pes(pattern, "output_traced.pes")
print("✅ PES file saved: output_traced.pes")
