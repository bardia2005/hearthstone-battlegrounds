"""Remove checkerboard pattern from Table_Main_Big.png and make it truly transparent"""
from PIL import Image
import numpy as np

# Load the image
img = Image.open("Designs/Table_Main_Big.png").convert("RGBA")
data = np.array(img)

# Checkerboard pattern colors (light gray and white)
# Light gray: around (204, 204, 204) or (192, 192, 192)
# White: (255, 255, 255)
# We'll make these transparent

# Create mask for checkerboard colors
# Check for light gray and white pixels
light_gray_mask = (
    (data[:, :, 0] >= 190) & (data[:, :, 0] <= 210) &
    (data[:, :, 1] >= 190) & (data[:, :, 1] <= 210) &
    (data[:, :, 2] >= 190) & (data[:, :, 2] <= 210)
)

white_mask = (
    (data[:, :, 0] >= 250) &
    (data[:, :, 1] >= 250) &
    (data[:, :, 2] >= 250)
)

# Combine masks
checkerboard_mask = light_gray_mask | white_mask

# Set alpha to 0 for checkerboard pixels
data[checkerboard_mask, 3] = 0

# Save the cleaned image
result = Image.fromarray(data, 'RGBA')
result.save("Designs/Table_Main_Big_Clean.png")
print("Checkerboard removed! Saved as Table_Main_Big_Clean.png")
print(f"Transparent pixels: {np.sum(checkerboard_mask)}")
