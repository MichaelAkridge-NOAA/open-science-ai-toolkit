from ultralytics import YOLO

class ModelManager:
    def __init__(self, model_path, device):
        """
        Initialize the model with a given model path and device.
        """
        self.model = YOLO(model_path)
        self.device = device
        self.model.to(self.device)

    def train(self, config):
        """
        Train the model using a provided configuration dictionary.
        """
        print("Starting training with the following configuration:", config)
        self.model.train(
            data=config['data'],
            epochs=config['epochs'],
            imgsz=config['imgsz'],
            batch=config['batch'],
            lr0=config['lr0'],
            lrf=config.get('lrf', 0.01),
            optimizer=config.get('optimizer', 'SGD'),
            device=self.device,
            save_period=config.get('save_period', 10),
            patience=config.get('patience', 5),
            augment=config.get('augment', True),
            mosaic=config.get('mosaic', True),
            mixup=config.get('mixup', True),
            cos_lr=config.get('cos_lr', False),
            project=config.get('project', 'runs/train'),
        )
        print("Training complete!")

    def save_model(self, save_path):
        """
        Save the trained model at the specified path.
        """
        self.model.export(save_dir=save_path)
        print(f"Model saved to {save_path}")

    def validate(self, data_path):
        """
        Validate the model using the specified validation dataset.
        """
        metrics = self.model.val(data=data_path, device=self.device)
        print("Validation metrics:", metrics)
        return metrics
