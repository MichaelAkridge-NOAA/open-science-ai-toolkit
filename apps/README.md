# YOLO Object Detection Training GUI Application
![app](./docs/screenshot.png)
## Requirements
```
PyQt5
torch
ultralytics
```
Installation Instructions
1. Install Python / Conda and/or Anaconda
Ensure Python 3.10 or later 

2. Set Up a Virtual Environment
It is recommended to use a virtual environment to avoid conflicts with system packages.

3. Install Requirements
```
pip install -r requirements.txt
```


Running the Application
0. Clone Repo & Open App Dir

1. Launch the GUI 
Run the following command to start the YOLO Training GUI:
```
python main.py
```
2. Using the GUI
Device: Select CPU or GPU.
Model: Choose a YOLO model (e.g., yolo11n.pt).
Dataset Config Path: Browse to your dataset YAML file.
Training Parameters: Set epochs, batch size, and image size.
Advanced Options: Optionally configure optimizer, save period, augmentation, etc.
Start Training: Click the button to begin.
Monitor Progress: View real-time logs in the scrollable progress text box.
Abort Training: Click the abort button to stop training.
Troubleshooting
Common Issues:
CUDA Not Found (GPU): Ensure the correct version of CUDA is installed for your PyTorch version. Check the PyTorch installation guide.

Missing Dataset Config: Ensure the data path in your YAML file is correct.
Example: urchin_dataset.yaml
```
train: images/train
val: images/val
test: images/test

nc: 1
names: ['urchin']
```
Training Logs: If training fails, check training_log.txt for detailed error messages.