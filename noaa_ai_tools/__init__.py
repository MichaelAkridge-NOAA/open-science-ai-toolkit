# __init__.py for noaa_ai_tools package

__all__ = [
    "DeviceManager", "ModelManager", "ModelExporter",  # Core components
    "ensure_dir", "filter_images_with_labels", "create_background_labels",  # Data preparation utilities
    "validate_yolo_format", "remap_class_ids", "split_dataset"  # More data utilities
]

# Import from the device management module
from .device_manager import DeviceManager  # Handles device configurations and setup

# Import from the data preparation module
from .dataprep import (
    ensure_dir,  # Ensure directories exist for output
    filter_images_with_labels,  # Filter and copy labeled images
    create_background_labels,  # Create background images and labels
    validate_yolo_format,  # Check label formats for compliance
    remap_class_ids,  # Change class IDs in labels
    split_dataset  # Divide datasets into training, validation, and test splits
)

# Import from the model management module
from .model_manager import ModelManager  # Manages model training and saving

# Import from the model export module
from .exporter import ModelExporter  # Handles exporting models to various formats
