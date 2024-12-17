import os
import shutil
import random

# Utility Function: Ensure a directory exists
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

# 1. Filter Images with Labels
def filter_images_with_labels(image_folder, label_folder, output_folder, image_formats=None):
    """
    Filters and copies images that have corresponding YOLO label files.
    """
    if image_formats is None:
        image_formats = ['.jpg', '.jpeg', '.png']

    ensure_dir(output_folder)
    label_files = [f for f in os.listdir(label_folder) if f.endswith(".txt")]

    for label_file in label_files:
        image_name = os.path.splitext(label_file)[0]
        for ext in image_formats:
            image_path = os.path.join(image_folder, image_name + ext)
            if os.path.exists(image_path):
                shutil.copy(image_path, os.path.join(output_folder, os.path.basename(image_path)))
                print(f"Copied: {image_path}")
                break
    print("Image extraction complete!")

# 2. Create Background Images with Empty Labels
def create_background_labels(background_folder, output_image_folder, output_label_folder, image_formats=None):
    """
    Copies background images and creates corresponding empty label files.
    """
    if image_formats is None:
        image_formats = ['.jpg', '.jpeg', '.png']

    ensure_dir(output_image_folder)
    ensure_dir(output_label_folder)

    background_images = [f for f in os.listdir(background_folder) if os.path.splitext(f)[1].lower() in image_formats]
    for bg_image in background_images:
        bg_image_path = os.path.join(background_folder, bg_image)
        shutil.copy(bg_image_path, os.path.join(output_image_folder, bg_image))

        empty_label_path = os.path.join(output_label_folder, os.path.splitext(bg_image)[0] + ".txt")
        with open(empty_label_path, "w") as f:
            pass
        print(f"Created empty label for: {bg_image}")
    print("Background image processing complete!")

# 3. Validate YOLO Format
def validate_yolo_format(labels_folder):
    """
    Checks if YOLO annotation files are properly formatted.
    """
    def is_yolo_format(line):
        try:
            parts = line.strip().split()
            return len(parts) == 5 and all(float(x) for x in parts)
        except ValueError:
            return False

    invalid_files = []
    for filename in os.listdir(labels_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(labels_folder, filename)
            with open(file_path, 'r') as file:
                if any(not is_yolo_format(line) for line in file):
                    invalid_files.append(file_path)
    return invalid_files

# 4. Remap Class IDs
def remap_class_ids(label_dir, old_id, new_id):
    """
    Remaps class IDs in YOLO label files.
    """
    for label_file in os.listdir(label_dir):
        if label_file.endswith(".txt"):
            file_path = os.path.join(label_dir, label_file)
            with open(file_path, "r") as file:
                lines = [line.replace(f"{old_id} ", f"{new_id} ") for line in file]
            with open(file_path, "w") as file:
                file.writelines(lines)
    print(f"Class IDs remapped from {old_id} to {new_id}.")

# 5. Split Dataset
def split_dataset(images_dir, annotations_dir, output_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Splits a dataset into train, validation, and test sets.
    """
    assert train_ratio + val_ratio + test_ratio == 1.0, "Split ratios must sum to 1.0"

    split_dirs = {
        'train': os.path.join(output_dir, 'train'),
        'val': os.path.join(output_dir, 'val'),
        'test': os.path.join(output_dir, 'test')
    }
    for split in split_dirs.values():
        ensure_dir(os.path.join(split, 'images'))
        ensure_dir(os.path.join(split, 'labels'))

    all_images = [f for f in os.listdir(images_dir) if f.lower().endswith('.jpg')]
    random.shuffle(all_images)

    train_idx = int(len(all_images) * train_ratio)
    val_idx = train_idx + int(len(all_images) * val_ratio)
    splits = {'train': all_images[:train_idx], 'val': all_images[train_idx:val_idx], 'test': all_images[val_idx:]}

    def copy_files(image_list, split_name):
        for image in image_list:
            shutil.copy(os.path.join(images_dir, image), os.path.join(split_dirs[split_name], 'images', image))
            label = image.replace('.jpg', '.txt')
            shutil.copy(os.path.join(annotations_dir, label), os.path.join(split_dirs[split_name], 'labels', label))

    for split_name, image_list in splits.items():
        copy_files(image_list, split_name)
        print(f"{split_name.capitalize()} split complete with {len(image_list)} images.")
