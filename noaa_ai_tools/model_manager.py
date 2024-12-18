# model_manager.py

from ultralytics import YOLO
from .device_manager import DeviceManager

class ModelManager:
    def __init__(self, model_path, device):
        """
        Initialize the model with a given model name and device.
        """
        self.model = YOLO(model_path).model.to(device)
        self.device = device

    def train(self, config):
        """
        Train the model using a provided configuration dictionary that includes
        all necessary parameters for the training process.
        """
        print("Starting training with the following configuration:", config)
        # Pass the entire configuration dictionary to the train method
        self.model.train(
            data=config['data'],
            epochs=config['epochs'],
            imgsz=config['imgsz'],
            batch_size=config['batch'],
            lr0=config['lr0'],
            lrf=config.get('lrf', 0.01),  # Use a default if not specified
            optimizer=config['optimizer'],
            device=self.device,
            save_period=config.get('save_period', 5),
            patience=config.get('patience', 3),
            augment=config.get('augment', False),
            mosaic=config.get('mosaic', False),
            mixup=config.get('mixup', False),
            cos_lr=config.get('cos_lr', False),
            project=config.get('project', 'runs/train')
        )
        print("Training complete!")

    def save_model(self, save_path):
        """
        Save the trained model at the specified path.
        """
        self.model.save(save_path)
        print(f"Model saved to {save_path}")

    def validate(self, data_path):
        """
        Validate the model using the specified validation dataset and print the evaluation metrics.
        """
        metrics = self.model.val(data=data_path, device=self.device)
        print("Validation metrics:", metrics)
        return metrics
