# dataprep.py

import os
import shutil
import random

def ensure_dir(path):
    """
    Create a directory if it does not exist.
    """
    os.makedirs(path, exist_ok=True)

def filter_images_with_labels(image_folder, label_folder, output_folder, image_formats=None):
    """
    Copy images to the output folder if their corresponding label files exist.
    """
    if image_formats is None:
        image_formats = ['.jpg', '.jpeg', '.png']

    ensure_dir(output_folder)
    label_files = [f[:-4] for f in os.listdir(label_folder) if f.endswith(".txt")]

    for label_file in label_files:
        copied = False
        for ext in image_formats:
            image_path = os.path.join(image_folder, label_file + ext)
            if os.path.exists(image_path):
                shutil.copy(image_path, os.path.join(output_folder, os.path.basename(image_path)))
                print(f"Copied: {image_path}")
                copied = True
                break
        if not copied:
            print(f"No matching image found for {label_file}")

def create_background_labels(background_folder, output_image_folder, output_label_folder, image_formats=None):
    """
    Copy background images and create corresponding empty label files.
    """
    if image_formats is None:
        image_formats = ['.jpg', '.jpeg', '.png']

    ensure_dir(output_image_folder)
    ensure_dir(output_label_folder)

    for bg_image in os.listdir(background_folder):
        ext = os.path.splitext(bg_image)[1].lower()
        if ext in image_formats:
            shutil.copy(os.path.join(background_folder, bg_image), os.path.join(output_image_folder, bg_image))
            empty_label_path = os.path.join(output_label_folder, os.path.splitext(bg_image)[0] + ".txt")
            open(empty_label_path, 'w').close()
            print(f"Created empty label for: {bg_image}")

def validate_yolo_format(labels_folder):
    """
    Validate that label files conform to the YOLO format.
    """
    invalid_files = []
    for label_file in os.listdir(labels_folder):
        if label_file.endswith(".txt"):
            with open(os.path.join(labels_folder, label_file), 'r') as file:
                lines = file.readlines()
                if not all(len(line.strip().split()) == 5 for line in lines if line.strip()):
                    invalid_files.append(label_file)
    
    if invalid_files:
        print("Invalid label files:", invalid_files)
    else:
        print("All label files are valid.")

def remap_class_ids(label_dir, old_id, new_id):
    """
    Remap class IDs in label files from old_id to new_id.
    """
    for label_file in os.listdir(label_dir):
        if label_file.endswith(".txt"):
            with open(os.path.join(label_dir, label_file), 'r') as file:
                lines = file.readlines()

            with open(os.path.join(label_dir, label_file), 'w') as file:
                for line in lines:
                    parts = line.strip().split()
                    if parts[0] == str(old_id):
                        parts[0] = str(new_id)
                    file.write(" ".join(parts) + "\n")

            print(f"Remapped class IDs in {label_file} from {old_id} to {new_id}")

def split_dataset(images_dir, annotations_dir, output_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Split dataset into training, validation, and test sets based on specified ratios.
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

    num_train = int(len(all_images) * train_ratio)
    num_val = int(len(all_images) * val_ratio)

    splits = {
        'train': all_images[:num_train],
        'val': all_images[num_train:num_train + num_val],
        'test': all_images[num_train + num_val:]
    }

    for split_name, images in splits.items():
        for image in images:
            shutil.copy(os.path.join(images_dir, image), os.path.join(split_dirs[split_name], 'images', image))
            label = os.path.splitext(image)[0] + '.txt'
            shutil.copy(os.path.join(annotations_dir, label), os.path.join(split_dirs[split_name], 'labels', label))
        print(f"Copied {len(images)} images to {split_name} directory.")
