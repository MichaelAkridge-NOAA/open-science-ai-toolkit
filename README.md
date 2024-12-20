# Open Science AI Toolkit
Open source suite of tools, workflows, and processes designed to accelerate Open Science AI/ML development.

### Overview
```mermaid
flowchart LR
  subgraph ABC[Data Preparation]
    A1[Data Collection] --> A2[Data Annotation]
    A2 --> A3[Data Preprocessing]
  end
  ABC --> D[Model Training]
  D --> E[Model Evaluation]
  E --> F{Satisfactory Performance?}
  F -->|Yes| G[Model Deployment]
  F -->|No| D
  G --> H[Model Monitoring]
  H --> ABC
```
## Installation
To install the entire toolkit:
```
pip install git+https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit.git
```
## Features
The `noaa_ai_tools` subpackage provides functionalities like:
- **Dataset Preparation**: Easily prepare your datasets for training with functions for filtering and validating annotations.
- - **Filter Images with Labels**
- - **Create Labels for Background Images**
- - **Validate YOLO Format**
- - **Remap Class IDs**
- - **Split Dataset (train, val, test)**
- **Model Training**: Train and manage deep learning models, including support for YOLO models from Ultralytics(https://github.com/ultralytics/ultralytics).
- **Model Exporting**: Export trained models to various formats, including ONNX, TensorFlow Lite, Edge TPU, and NCNN.

## Example
```
from noaa_ai_tools import DeviceManager, ModelManager, ModelExporter

# Initialize the device
# This sets up which GPU (or CPU if no GPU is available) will be used for training.
device = DeviceManager.initialize_device("0")  # "0" is the GPU index; use "0" to select the first GPU. If no GPU it will default to CPU

# Setup and train the model
# ModelManager is responsible for all aspects of model training and handling.
model_manager = ModelManager("yolo11m.pt", device)  # Load the YOLO model specified by name. | Options: "yolo11n.pt", "yolo11s.pt","yolo11m.pt","yolo11l.pt","yolo11x.pt"

# Define training configuration
# This dictionary includes all settings needed for training the YOLO model.
train_config = {
    'data': 'path/to/data.yaml',  # Path to dataset configuration file (required).
    'epochs': 100,               # Total number of training epochs (required).
    'imgsz': 640,                # Image size: dimensions to which the images will be resized (required).
    'batch': 32,                 # Batch size: number of images processed per batch (required).
    'lr0': 0.001,                # Initial learning rate (required).
    'lrf': 0.0001,               # Final learning rate, used in cosine annealing schedule (optional, defaults to a preset value if not provided).
    'optimizer': 'AdamW',        # Type of optimizer to use (required).
    'device': device,            # Device to use for training (required). Default via DeviceManager
    'save_period': 10,           # Frequency of saving the model (in epochs) (optional).
    'patience': 10,              # Patience for early stopping (optional).
    'augment': True,             # Enable data augmentation (optional).
    'mosaic': True,              # Enable mosaic augmentation (optional).
    'mixup': True,               # Enable mixup augmentation (optional).
    'cos_lr': True,              # Use cosine learning rate scheduler (optional).
    'project': 'training_logs'   # Directory for saving training logs (optional).
}
model_manager.train(train_config)  # Start the training process with the specified configurations.

# Save the trained model
# Saves the model weights to the specified path after training is complete.
model_manager.save_model("path/to/save_model.pt")

# Export the trained model
# Exports the model to different formats for deployment or inference on different platforms.
exporter = ModelExporter(model_manager.model)
exporter.export_model(['onnx', 'tflite', 'edgetpu', 'ncnn'])  # List of formats to export.

# Validate the model
# Runs validation using the specified validation dataset and prints out the metrics.
validation_metrics = model_manager.validate('path/to/validation_data.yaml')
print("Validation Completed with Metrics:", validation_metrics)

```
## Example Usage
### 1. Filter Images with Labels
```
from noaa_ai_tools import filter_images_with_labels

filter_images_with_labels(
    image_folder="path/to/images",
    label_folder="path/to/labels",
    output_folder="path/to/output_images"
)
```
### 2. Create Labels for Background Images
```
from noaa_ai_tools import create_background_labels

create_background_labels(
    background_folder="path/to/background_images",
    output_image_folder="path/to/output_images",
    output_label_folder="path/to/output_labels"
)
```
### 3. Validate YOLO Format of dataset

```
from noaa_ai_tools import validate_yolo_format

invalid_files = validate_yolo_format(labels_folder="path/to/labels")
if invalid_files:
    print("Invalid YOLO files found:", invalid_files)
else:
    print("All YOLO files are valid!")
```
### 4. Remap Class IDs
```
from noaa_ai_tools import remap_class_ids

remap_class_ids(
    label_dir="path/to/labels",
    old_id="0",  # Old class ID
    new_id="1"   # New class ID
)
```
### 5. Split Dataset into Train/Val/Test
```
from noaa_ai_tools import split_dataset

split_dataset(
    images_dir="path/to/images",
    annotations_dir="path/to/labels",
    output_dir="path/to/output_splits",
    train_ratio=0.7, val_ratio=0.2, test_ratio=0.1
)
```
## File Structure Example
```
project-dataset-name/
│
├── input/                  # Input images and labels
│   ├── images/             # Original images
│   └── labels/             # YOLO format labels
│
└── output/                 # Outputs from the toolkit
    ├── filtered_images/    # Filtered images with labels
    ├── background_images/  # Background images with empty labels
    ├── splits/             # Train/val/test splits
    └── logs/               # Logs
```
## Apps
*Placeholder for applications that streamline workflows.*

## Notebooks
A collection of Jupyter notebooks for different stages of the AI/ML pipeline:

| Category                                         |  Name                                      | Description                                                                               | Deploy  | 
| ------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------|
| Data Preparation                                  | **Data Prep**                                      | Prepares training and testing datasets, and verifies metadata                             | placeholder| 
| Model Training                                    | **Train YOLO11 Model**                            | Configures parameters and trains YOLOv11 models                                           | placeholder  | 
| Model Training                                    | **Train YOLO11 Segment Model**                    | Configures parameters and trains YOLOv11 segmentation models                              | placeholder | 
| Model Training                                    | **Train YOLOv8 Model**                             | Configures parameters and trains YOLOv8 models                                            |placeholder| 
| Model Evaluation                                  | **Evaluate Models**                                | Generates metrics and performs comprehensive model testing                                | placeholder|
| Model Deployment                                  | **Publish Models**                                 | Publishes trained models to public repositories for community access                       | placeholder  | 

----------
#### Disclaimer
This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project content is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.

#### License
- This code is licensed as detailed in the [LICENSE.md](./LICENSE.md) file.
- For licensing details related to YOLO training, please refer to the [Ultralytics license](https://github.com/ultralytics/ultralytics?tab=readme-ov-file#license)

#### Credits
- https://github.com/ultralytics/ultralytics
