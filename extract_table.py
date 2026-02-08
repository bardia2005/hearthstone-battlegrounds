"""
Extract the table portion from Table3.webp with maximum precision
"""
import pygame
from PIL import Image
import numpy as np

def extract_table_from_image(input_path, output_path):
    """
    Extract the table portion from the Hearthstone screenshot
    Uses edge detection and color analysis to find table boundaries
    """
    # Load image with PIL for better processing
    img = Image.open(input_path)
    img_array = np.array(img)
    
    # Convert to RGB if needed
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    
    height, width = img_array.shape[:2]
    
    # Hearthstone table characteristics:
    # - Wooden brown/tan colors
    # - Ornate border with gold trim
    # - Center playing area
    # - Typically occupies middle 60-70% of screen height
    
    # Find table boundaries by analyzing color patterns
    # Table has distinct brown/tan colors (R: 120-180, G: 90-140, B: 70-120)
    
    # Scan from top to find where table starts
    table_top = 0
    for y in range(height):
        row = img_array[y, width//2-100:width//2+100]  # Sample center area
        # Check if this row has table-like colors
        brown_pixels = np.sum(
            (row[:, 0] > 100) & (row[:, 0] < 200) &  # R
            (row[:, 1] > 70) & (row[:, 1] < 160) &   # G
            (row[:, 2] > 50) & (row[:, 2] < 140)     # B
        )
        if brown_pixels > len(row) * 0.3:  # 30% of pixels are table-colored
            table_top = y
            break
    
    # Scan from bottom to find where table ends
    table_bottom = height
    for y in range(height-1, 0, -1):
        row = img_array[y, width//2-100:width//2+100]
        brown_pixels = np.sum(
            (row[:, 0] > 100) & (row[:, 0] < 200) &
            (row[:, 1] > 70) & (row[:, 1] < 160) &
            (row[:, 2] > 50) & (row[:, 2] < 140)
        )
        if brown_pixels > len(row) * 0.3:
            table_bottom = y + 1
            break
    
    # Scan from left to find table edge
    table_left = 0
    for x in range(width):
        col = img_array[height//2-50:height//2+50, x]
        brown_pixels = np.sum(
            (col[:, 0] > 100) & (col[:, 0] < 200) &
            (col[:, 1] > 70) & (col[:, 1] < 160) &
            (col[:, 2] > 50) & (col[:, 2] < 140)
        )
        if brown_pixels > len(col) * 0.3:
            table_left = x
            break
    
    # Scan from right to find table edge
    table_right = width
    for x in range(width-1, 0, -1):
        col = img_array[height//2-50:height//2+50, x]
        brown_pixels = np.sum(
            (col[:, 0] > 100) & (col[:, 0] < 200) &
            (col[:, 1] > 70) & (col[:, 1] < 160) &
            (col[:, 2] > 50) & (col[:, 2] < 140)
        )
        if brown_pixels > len(col) * 0.3:
            table_right = x + 1
            break
    
    # Add some padding to ensure we get the full ornate border
    padding = 10
    table_top = max(0, table_top - padding)
    table_bottom = min(height, table_bottom + padding)
    table_left = max(0, table_left - padding)
    table_right = min(width, table_right + padding)
    
    # Extract the table region
    table_region = img_array[table_top:table_bottom, table_left:table_right]
    
    # Save the extracted table
    table_img = Image.fromarray(table_region.astype('uint8'))
    table_img.save(output_path, quality=95)
    
    print(f"Table extracted successfully!")
    print(f"Original image: {width}x{height}")
    print(f"Table bounds: left={table_left}, top={table_top}, right={table_right}, bottom={table_bottom}")
    print(f"Table size: {table_right-table_left}x{table_bottom-table_top}")
    print(f"Saved to: {output_path}")
    
    return table_left, table_top, table_right, table_bottom

if __name__ == "__main__":
    try:
        extract_table_from_image("Designs/Table3.webp", "Designs/Table_Extracted.png")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
