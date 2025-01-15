from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QComboBox, QCheckBox,
    QGroupBox, QFormLayout, QTextEdit
)
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess


class TrainingThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, train_config):
        super().__init__()
        self.train_config = train_config
        self.abort_requested = False
        self.log_file = "training_log.txt"  # Log file path

    def run(self):
        try:
            self.progress.emit("Starting training...")
            cmd = (
                f"yolo task=detect mode=train "
                f"data={self.train_config['data']} "
                f"epochs={self.train_config['epochs']} "
                f"imgsz={self.train_config['imgsz']} "
                f"batch={self.train_config['batch']} "
                f"lr0={self.train_config['lr0']} "
                f"optimizer={self.train_config['optimizer']} "
                f"save_period={self.train_config.get('save_period', 10)} "
                f"patience={self.train_config.get('patience', 10)} "
                f"augment={str(self.train_config.get('augment', False)).lower()} "
                f"mosaic={str(self.train_config.get('mosaic', False)).lower()} "
                f"mixup={str(self.train_config.get('mixup', False)).lower()} "
                f"cos_lr={str(self.train_config.get('cos_lr', False)).lower()}"
            )

            with open(self.log_file, "w") as log:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )

                for line in iter(process.stdout.readline, ''):
                    if self.abort_requested:
                        process.terminate()
                        self.progress.emit("Training aborted.")
                        return

                    self.progress.emit(line.strip())
                    log.write(line)
                    log.flush()

                process.stdout.close()
                process.wait()
                self.finished.emit()

                if process.returncode == 0:
                    self.progress.emit("Training completed successfully!")
                else:
                    self.progress.emit(f"Training failed. Check logs in {self.log_file}.")
        except Exception as e:
            self.progress.emit(f"An error occurred: {e}")


class TrainingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YOLO Training GUI: Object Detection")

        layout = QVBoxLayout()

        # Device Selection
        layout.addWidget(QLabel("Device: (Choose CPU or GPU for training)"))
        self.device_dropdown = QComboBox()
        self.device_options = {"CPU (default)": "cpu", "GPU (use GPU 0)": "0"}
        self.device_dropdown.addItems(self.device_options.keys())
        layout.addWidget(self.device_dropdown)

        # Model Selection
        layout.addWidget(QLabel("Select Base YOLO Model for Fine Tuning:"))
        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems(["yolo11n.pt", "yolo11s.pt", "yolo11m.pt", "yolo11l.pt", "yolo11x.pt"])
        layout.addWidget(self.model_dropdown)

        # Dataset Config
        layout.addWidget(QLabel("Dataset YAML Config Path: (Provide the path to your dataset config file)"))
        self.data_input = QLineEdit()
        layout.addWidget(self.data_input)
        self.browse_data_btn = QPushButton("Browse")
        self.browse_data_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_data_btn)

        # Training Parameters
        layout.addWidget(QLabel("Epochs (Number of dataset training passes):"))
        self.epochs_input = QLineEdit("100")
        layout.addWidget(self.epochs_input)

        layout.addWidget(QLabel("Batch Size (Number of images processed per training step):"))
        self.batch_input = QLineEdit("32")
        layout.addWidget(self.batch_input)

        layout.addWidget(QLabel("Image Size (Resize images to this size for training):"))
        self.imgsz_input = QLineEdit("640")
        layout.addWidget(self.imgsz_input)

        layout.addWidget(QLabel("Initial Learning Rate (Starting rate for gradient descent optimization):"))
        self.lr0_input = QLineEdit("0.001")
        layout.addWidget(self.lr0_input)

        # Advanced Options Section
        self.advanced_options = QGroupBox("Advanced Options (Optional)")
        self.advanced_options.setCheckable(True)
        self.advanced_options.setChecked(False)
        adv_layout = QFormLayout()

        adv_layout.addRow(QLabel("Optimizer (Choose optimization algorithm):"), QLineEdit("AdamW"))
        adv_layout.addRow(QLabel("Save Period (Save model weights every N epochs):"), QLineEdit("10"))
        adv_layout.addRow(QLabel("Patience (Early stopping patience for validation):"), QLineEdit("10"))
        adv_layout.addRow(QLabel("Enable Augmentation (Data augmentation during training):"), QCheckBox())
        adv_layout.addRow(QLabel("Enable Mosaic (Mosaic augmentation for YOLO):"), QCheckBox())
        adv_layout.addRow(QLabel("Enable Mixup (Mixup augmentation for YOLO):"), QCheckBox())
        adv_layout.addRow(QLabel("Use Cosine LR Scheduler (Cosine annealing for learning rate):"), QCheckBox())

        self.advanced_options.setLayout(adv_layout)
        layout.addWidget(self.advanced_options)

        # Start Training Button
        self.start_btn = QPushButton("Start Training")
        self.start_btn.clicked.connect(self.start_training)
        layout.addWidget(self.start_btn)

        # Abort Button
        self.abort_btn = QPushButton("Abort Training")
        self.abort_btn.setEnabled(False)
        self.abort_btn.clicked.connect(self.abort_training)
        layout.addWidget(self.abort_btn)

        # Scrollable Progress Text Box
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        layout.addWidget(QLabel("Training Progress:"))
        layout.addWidget(self.progress_text)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Dataset Config File", "", "YAML Files (*.yaml)")
        if file_path:
            self.data_input.setText(file_path)

    def start_training(self):
        train_config = {
            'data': self.data_input.text(),
            'epochs': int(self.epochs_input.text()),
            'imgsz': int(self.imgsz_input.text()),
            'batch': int(self.batch_input.text()),
            'lr0': float(self.lr0_input.text()),
            'optimizer': 'AdamW',
        }

        if self.advanced_options.isChecked():
            adv_widgets = self.advanced_options.layout()
            train_config.update({
                'optimizer': adv_widgets.itemAt(1).widget().text(),
                'save_period': int(adv_widgets.itemAt(3).widget().text()),
                'patience': int(adv_widgets.itemAt(5).widget().text()),
                'augment': adv_widgets.itemAt(7).widget().isChecked(),
                'mosaic': adv_widgets.itemAt(9).widget().isChecked(),
                'mixup': adv_widgets.itemAt(11).widget().isChecked(),
                'cos_lr': adv_widgets.itemAt(13).widget().isChecked(),
            })

        self.training_thread = TrainingThread(train_config)
        self.training_thread.progress.connect(self.update_progress)
        self.training_thread.finished.connect(self.on_training_finished)
        self.abort_btn.setEnabled(True)
        self.training_thread.start()

    def abort_training(self):
        if self.training_thread:
            self.training_thread.abort_requested = True
            self.abort_btn.setEnabled(False)

    def update_progress(self, message):
        self.progress_text.append(message)
        self.progress_text.ensureCursorVisible()

    def on_training_finished(self):
        self.abort_btn.setEnabled(False)
        self.progress_text.append("Training finished.")
