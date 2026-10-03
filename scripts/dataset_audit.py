import os
import csv

DATASET_DIR = "dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
METADATA_FILE = os.path.join(DATASET_DIR, "metadata.csv")

def audit_dataset():
    if not os.path.exists(IMAGES_DIR):
        print("Dataset directory not found.")
        return

    categories = os.listdir(IMAGES_DIR)
    category_counts = {}
    total_images = 0

    for cat in categories:
        cat_path = os.path.join(IMAGES_DIR, cat)
        if os.path.isdir(cat_path):
            files = [f for f in os.listdir(cat_path) if f.endswith('.jpg') or f.endswith('.png')]
            count = len(files)
            category_counts[cat] = count
            total_images += count

    metadata_records = []
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            metadata_records = list(reader)

    metadata_count = len(metadata_records)

    print("Dataset Summary:")
    print(f"Total Images: {total_images}")
    print(f"Categories: {len(category_counts)}")
    for k, v in category_counts.items():
        print(f" - {k}: {v} images")
    print(f"Metadata Records: {metadata_count}")

    metadata_filenames = set(row['filename'] for row in metadata_records)
    actual_filenames = set()
    for cat in categories:
        cat_path = os.path.join(IMAGES_DIR, cat)
        if os.path.isdir(cat_path):
            for f in os.listdir(cat_path):
                if f.endswith('.jpg') or f.endswith('.png'):
                    actual_filenames.add(f)

    missing_in_metadata = actual_filenames - metadata_filenames
    missing_on_disk = metadata_filenames - actual_filenames

    print(f"Missing in metadata: {len(missing_in_metadata)}")
    print(f"Missing on disk: {len(missing_on_disk)}")

if __name__ == "__main__":
    audit_dataset()
