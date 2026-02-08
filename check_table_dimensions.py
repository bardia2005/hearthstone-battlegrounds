"""Check Table_Main_Big.png dimensions"""
from PIL import Image

img = Image.open("Designs/Table_Main_Big.png")
width, height = img.size
print(f"Table_Main_Big.png dimensions: {width}x{height}")
print(f"Aspect ratio: {width/height:.3f}")
print(f"Has alpha channel: {img.mode}")
