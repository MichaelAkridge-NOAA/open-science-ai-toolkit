import torch
import os

class DeviceManager:
    @staticmethod
    def initialize_device(gpu_index="0"):
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_index
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {device}")
        if device == 'cuda':
            print(f"Available GPUs: {torch.cuda.device_count()}")
            print(f"Current GPU: {torch.cuda.current_device()}")
            print(f"GPU Name: {torch.cuda.get_device_name(torch.cuda.current_device())}")
        return device
