import os
import csv
from PIL import Image, ImageDraw
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
IMAGES_DIR = os.path.join(DATASET_DIR, "images")

CATEGORIES = [
    "correct", "missing_padding", "wrong_orientation", "wrong_box",
    "missing_cover", "visible_damage", "blurry", "occluded"
]

def create_dirs():
    os.makedirs(DATASET_DIR, exist_ok=True)
    for cat in CATEGORIES:
        os.makedirs(os.path.join(IMAGES_DIR, cat), exist_ok=True)

def generate_image(category, index):
    img = Image.new('RGB', (400, 400), color=(200, 200, 200))
    d = ImageDraw.Draw(img)
    
    d.rectangle([50, 50, 350, 350], outline=(100, 100, 100), width=5)
    
    if category != "missing_padding":
        d.rectangle([60, 60, 340, 340], outline=(150, 150, 150), width=3)
        d.rectangle([70, 70, 330, 330], fill=(220, 220, 220))
    
    part_color = (50, 50, 150)
    if category == "wrong_box":
        d.rectangle([50, 50, 350, 350], outline=(200, 50, 50), width=5)
    
    if category == "wrong_orientation":
        d.ellipse([100, 150, 300, 250], fill=part_color)
    else:
        d.ellipse([150, 100, 250, 300], fill=part_color)
        
    if category == "visible_damage":
        d.line([150, 100, 250, 300], fill=(255, 0, 0), width=5)
        
    if category != "missing_cover":
        d.line([50, 50, 200, 200], fill=(100, 100, 100), width=2)
        d.line([350, 50, 200, 200], fill=(100, 100, 100), width=2)

    if category == "blurry":
        img = img.resize((40, 40)).resize((400, 400))
        
    if category == "occluded":
        d.rectangle([100, 100, 200, 200], fill=(0, 0, 0))

    filename = f"{category}_{index:03d}.jpg"
    path = os.path.join(IMAGES_DIR, category, filename)
    img.save(path)
    return path, filename

def main():
    create_dirs()
    metadata_path = os.path.join(DATASET_DIR, "metadata.csv")
    with open(metadata_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "category", "expected_decision"])
        
        count = 0
        for cat in CATEGORIES:
            num_imgs = 20 if cat == "correct" else 15
            for i in range(num_imgs):
                path, filename = generate_image(cat, count)
                decision = "pass" if cat == "correct" else "fail"
                writer.writerow([filename, cat, decision])
                count += 1
                
    print(f"Generated {count} images and metadata at {metadata_path}")

if __name__ == "__main__":
    main()
