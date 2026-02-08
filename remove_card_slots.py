"""
Script to remove the two card slots on the right side of Table_Main.png
This will paint over them with the surrounding table color
"""

from PIL import Image, ImageDraw
import os

def remove_card_slots():
    """Remove the card slots from the right side of the table image"""
    
    # Load the table image
    table_path = "Designs/Table_Main.png"
    
    if not os.path.exists(table_path):
        print(f"Error: {table_path} not found!")
        return
    
    print(f"Loading {table_path}...")
    img = Image.open(table_path)
    width, height = img.size
    print(f"Image size: {width}x{height}")
    
    # Create a drawing context
    draw = ImageDraw.Draw(img)
    
    # Sample the table color from a neutral area (middle-right area)
    # Get average color from a small region
    sample_x = int(width * 0.85)
    sample_y = int(height * 0.5)
    sample_region = img.crop((sample_x - 10, sample_y - 10, sample_x + 10, sample_y + 10))
    
    # Calculate average color
    pixels = list(sample_region.getdata())
    avg_r = sum(p[0] for p in pixels) // len(pixels)
    avg_g = sum(p[1] for p in pixels) // len(pixels)
    avg_b = sum(p[2] for p in pixels) // len(pixels)
    table_color = (avg_r, avg_g, avg_b)
    
    print(f"Sampled table color: {table_color}")
    
    # Define the regions where the card slots are (right side of table)
    # Top card slot (approximately)
    top_slot_x = int(width * 0.85)  # Right 15% of image
    top_slot_y = int(height * 0.15)  # Top area
    top_slot_width = int(width * 0.12)
    top_slot_height = int(height * 0.25)
    
    # Bottom card slot (approximately)
    bottom_slot_x = int(width * 0.85)
    bottom_slot_y = int(height * 0.60)  # Bottom area
    bottom_slot_width = int(width * 0.12)
    bottom_slot_height = int(height * 0.25)
    
    print("Painting over top card slot...")
    draw.rectangle(
        [top_slot_x, top_slot_y, top_slot_x + top_slot_width, top_slot_y + top_slot_height],
        fill=table_color
    )
    
    print("Painting over bottom card slot...")
    draw.rectangle(
        [bottom_slot_x, bottom_slot_y, bottom_slot_x + bottom_slot_width, bottom_slot_y + bottom_slot_height],
        fill=table_color
    )
    
    # Save the modified image
    output_path = "Designs/Table_Main_NoSlots.png"
    img.save(output_path)
    print(f"Saved modified image to {output_path}")
    
    # Also overwrite the original
    img.save(table_path)
    print(f"Updated original image at {table_path}")
    
    print("Done! Card slots removed.")

if __name__ == "__main__":
    remove_card_slots()
