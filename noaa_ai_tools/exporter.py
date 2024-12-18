class ModelExporter:
    def __init__(self, model):
        self.model = model

    def export_model(self, formats=['onnx', 'tflite', 'edgetpu', 'ncnn']):
        for format in formats:
            try:
                self.model.export(format=format)
                print(f"{format.upper()} model exported successfully!")
            except Exception as e:
                print(f"Failed to export model in {format.upper()} format: {e}")
