from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QCheckBox,
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
        self.log_file = "training_log.txt"

    def run(self):
        try:
            self.progress.emit("Starting training...")
            cmd = "yolo task=detect mode=train"
            for key, value in self.train_config.items():
                cmd += f" {key}={str(value).lower() if isinstance(value, bool) else value}"

            with open(self.log_file, "w") as log:
                process = subprocess.Popen(
                    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

                for line in iter(process.stdout.readline, ''):
                    if self.abort_requested:
                        process.terminate()
                        self.progress.emit("Training aborted.")
                        break
                    self.progress.emit(line.strip())
                    log.write(line)
                    log.flush()

                process.stdout.close()
                process.wait()
                self.finished.emit()

                if process.returncode != 0:
                    self.progress.emit(f"Training failed with exit code {process.returncode}. Check logs in {self.log_file}.")
                else:
                    self.progress.emit("Training completed successfully!")

        except Exception as e:
            self.progress.emit(f"An error occurred during training: {str(e)}")

from PyQt5.QtWidgets import QHBoxLayout

class TrainingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YOLO Training GUI: Object Detection")
        main_layout = QVBoxLayout(self)  # Main layout for the widget

        # Set up the various configuration sections
        self.setup_device_section(main_layout)
        self.setup_model_section(main_layout)
        self.setup_dataset_section(main_layout)
        self.setup_basic_options_section(main_layout)

        # Create a horizontal layout to hold optional settings
        options_layout = QHBoxLayout()

        self.advanced_options = self.setup_advanced_options()
        self.logging_options = self.setup_logging_options()
        self.experimental_options = self.setup_experimental_options()

        # Add the group boxes to the horizontal layout
        options_layout.addWidget(self.advanced_options)
        options_layout.addWidget(self.logging_options)
        options_layout.addWidget(self.experimental_options)

        # Add the horizontal layout to the main vertical layout
        main_layout.addLayout(options_layout)

        # Start/Abort Buttons
        self.start_btn = QPushButton("Start Training")
        self.start_btn.clicked.connect(self.start_training)
        main_layout.addWidget(self.start_btn)

        self.abort_btn = QPushButton("Abort Training")
        self.abort_btn.clicked.connect(self.abort_training)
        self.abort_btn.setEnabled(False)
        main_layout.addWidget(self.abort_btn)

        # Progress Display
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        main_layout.addWidget(self.progress_text)

        self.setLayout(main_layout)  # Set the main layout on the QWidget

    def collect_settings_from_layout(self, layout, config):
        # Assuming the layout argument here refers to a QFormLayout
        for i in range(layout.rowCount()):
            widget = layout.itemAt(i, QFormLayout.FieldRole).widget()
            if widget:
                if isinstance(widget, QLineEdit):
                    try:
                        config[widget.accessibleName()] = float(widget.text())
                    except ValueError:
                        config[widget.accessibleName()] = widget.text()
                elif isinstance(widget, QCheckBox):
                    config[widget.accessibleName()] = widget.isChecked()
    
    def setup_device_section(self, layout):
        # Device Selection
        self.device_dropdown = QComboBox()
        self.device_options = {"CPU (default)": "cpu", "GPU": "0"}  # Add more GPUs if necessary
        for label, value in self.device_options.items():
            self.device_dropdown.addItem(label, value)  # Add both label and value to the dropdown

        self.device_dropdown.setAccessibleName("device")
        self.add_field_with_tooltip(layout, "Device (Choose CPU or GPU for training):",
                                    "Device to use for training. Options include CPU or various GPUs (e.g., GPU 0).",
                                    self.device_dropdown)

    def setup_model_section(self, layout):
        # Model Selection
        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems(["yolo11n.pt", "yolo11s.pt", "yolo11m.pt", "yolo11l.pt", "yolo11x.pt"])
        self.model_dropdown.setAccessibleName("model")
        self.add_field_with_tooltip(layout, "Select Base YOLO Model (Pretrained model to fine-tune):",
                                    "Choose a YOLO model for fine-tuning. Options include models like yolo11n, yolo11s, etc.",
                                    self.model_dropdown)
    def setup_dataset_section(self, layout):
        # Dataset YAML Path with Browse Button
        self.data_input = QLineEdit()
        self.data_input.setAccessibleName("data")
        layout.addWidget(QLabel("Dataset YAML Config Path: (Provide the path to your dataset config file)"))
        layout.addWidget(self.data_input)
        self.browse_data_btn = QPushButton("Browse")
        self.browse_data_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_data_btn)

    def setup_basic_options_section(self, layout):
        # Basic Options
        self.epochs_input = QLineEdit("100")
        self.epochs_input.setAccessibleName("epochs")
        self.batch_input = QLineEdit("16")
        self.batch_input.setAccessibleName("batch")
        self.imgsz_input = QLineEdit("640")
        self.imgsz_input.setAccessibleName("imgsz")
        self.lr0_input = QLineEdit("0.001")
        self.lr0_input.setAccessibleName("lr0")

        self.add_field_with_tooltip(layout, "Epochs (Number of training epochs):",
                                    "Number of full passes through the dataset.", self.epochs_input)
        self.add_field_with_tooltip(layout, "Batch Size (Number of images per training step):",
                                    "Number of images processed in one training step.", self.batch_input)
        self.add_field_with_tooltip(layout, "Image Size (Resize images to this size for training):",
                                    "Target size for resizing input images during training.", self.imgsz_input)

    def setup_advanced_options(self):
        self.advanced_options = QGroupBox("Advanced Options (Optional)")
        self.advanced_options.setCheckable(True)
        self.advanced_options.setChecked(False)
        adv_layout = QFormLayout()

        # Optimizer
        optimizer_input = QLineEdit("AdamW")
        optimizer_input.setAccessibleName("optimizer")
        self.add_advanced_field_with_tooltip(adv_layout, "Optimizer (Algorithm for optimization):",
                                            "Optimizer to use for training (e.g., SGD, AdamW).", optimizer_input)

        # Initial Learning Rate
        lr0_input = QLineEdit("0.001")
        lr0_input.setAccessibleName("lr0")
        self.add_advanced_field_with_tooltip(adv_layout, "Initial Learning Rate (lr0):",
                                            "Starting learning rate for training.", lr0_input)

        # Final Learning Rate Fraction
        lrf_input = QLineEdit("0.01")
        lrf_input.setAccessibleName("lrf")
        self.add_advanced_field_with_tooltip(adv_layout, "Final Learning Rate Fraction (lrf):",
                                            "Final learning rate as a fraction of the initial rate.", lrf_input)

        # Momentum
        momentum_input = QLineEdit("0.937")
        momentum_input.setAccessibleName("momentum")
        self.add_advanced_field_with_tooltip(adv_layout, "Momentum (SGD/Adam momentum):",
                                            "Momentum factor for optimizers.", momentum_input)

        # Weight Decay
        weight_decay_input = QLineEdit("0.0005")
        weight_decay_input.setAccessibleName("weight_decay")
        self.add_advanced_field_with_tooltip(adv_layout, "Weight Decay (L2 regularization):",
                                            "Penalty for large model weights to prevent overfitting.", weight_decay_input)

        # Cosine LR Scheduler
        cosine_lr_checkbox = QCheckBox()
        cosine_lr_checkbox.setAccessibleName("cosine_lr")
        adv_layout.addRow(QLabel("Cosine LR Scheduler:"), cosine_lr_checkbox)

        # Multi-Scale Training
        multi_scale_checkbox = QCheckBox()
        multi_scale_checkbox.setAccessibleName("multi_scale")
        adv_layout.addRow(QLabel("Multi-Scale Training:"), multi_scale_checkbox)

        # Freeze Layers
        freeze_layers_input = QLineEdit("0")
        freeze_layers_input.setAccessibleName("freeze_layers")
        self.add_advanced_field_with_tooltip(adv_layout, "Freeze Layers:",
                                            "Freeze the first N layers of the model to fine-tune higher layers.", freeze_layers_input)

        self.advanced_options.setLayout(adv_layout)
        return self.advanced_options


    def setup_logging_options(self):
        self.logging_options = QGroupBox("Logging and Checkpoints (Optional)")
        self.logging_options.setCheckable(True)
        self.logging_options.setChecked(False)
        logging_layout = QFormLayout()

        # Project Directory
        project_dir_input = QLineEdit("YOLO_Project")
        project_dir_input.setAccessibleName("project_dir")
        self.add_advanced_field_with_tooltip(logging_layout, "Project Directory:",
                                            "Name of the project directory to save training outputs.", project_dir_input)

        # Experiment Name
        experiment_name_input = QLineEdit("Experiment_1")
        experiment_name_input.setAccessibleName("experiment_name")
        self.add_advanced_field_with_tooltip(logging_layout, "Experiment Name:",
                                            "Name of the training run for organized outputs.", experiment_name_input)

        # Save Model Weights
        save_weights_checkbox = QCheckBox()
        save_weights_checkbox.setAccessibleName("save_weights")
        logging_layout.addRow(QLabel("Save Model Weights:"), save_weights_checkbox)

        # Save Period (in epochs)
        save_period_input = QLineEdit("10")
        save_period_input.setAccessibleName("save_period")
        self.add_advanced_field_with_tooltip(logging_layout, "Save Period (in epochs):",
                                            "Save model checkpoints every N epochs.", save_period_input)

        self.logging_options.setLayout(logging_layout)
        return self.logging_options


    def setup_experimental_options(self):
        self.experimental_options = QGroupBox("Experimental Features (Optional)")
        self.experimental_options.setCheckable(True)
        self.experimental_options.setChecked(False)
        exp_layout = QFormLayout()

        # AMP (Automatic Mixed Precision)
        amp_checkbox = QCheckBox()
        amp_checkbox.setAccessibleName("amp")
        exp_layout.addRow(QLabel("AMP (Automatic Mixed Precision):"), amp_checkbox)

        # Resume Training
        resume_training_checkbox = QCheckBox()
        resume_training_checkbox.setAccessibleName("resume")
        exp_layout.addRow(QLabel("Resume Training:"), resume_training_checkbox)

        # Dropout
        dropout_input = QLineEdit("0.0")
        dropout_input.setAccessibleName("dropout")
        self.add_advanced_field_with_tooltip(exp_layout, "Dropout:",
                                            "Dropout rate for regularization, helps prevent overfitting.", dropout_input)

        # Profile Speeds
        profile_speeds_checkbox = QCheckBox()
        profile_speeds_checkbox.setAccessibleName("profile_speeds")
        exp_layout.addRow(QLabel("Profile Speeds:"), profile_speeds_checkbox)

        self.experimental_options.setLayout(exp_layout)
        return self.experimental_options

    def browse_file(self):
        """Opens a file dialog to browse for the dataset YAML file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Dataset Config File", "", "YAML Files (*.yaml);;All Files (*)")
        if file_path:
            self.data_input.setText(file_path)
    def add_advanced_field_with_tooltip(self, layout, label_text, tooltip_text, widget):
        """Adds a labeled advanced input field with a hover-based tooltip."""
        label = QLabel(label_text)
        label.setToolTip(tooltip_text)
        layout.addRow(label, widget)

    def add_field_with_tooltip(self, layout, label_text, tooltip_text, widget):
        """Adds a labeled widget with a hover-based tooltip to the given layout."""
        label = QLabel(label_text)
        label.setToolTip(tooltip_text)
        layout.addWidget(label)
        layout.addWidget(widget)

    def start_training(self):
        train_config = {'device': self.device_dropdown.currentData(),
            'data': self.data_input.text(),
            'epochs': int(self.epochs_input.text()),
            'imgsz': int(self.imgsz_input.text()),
            'batch': int(self.batch_input.text())
        }
        # Collect settings dynamically from all configurable sections
        self.collect_settings_from_layout(self.advanced_options.layout(), train_config)
        self.collect_settings_from_layout(self.logging_options.layout(), train_config)
        self.collect_settings_from_layout(self.experimental_options.layout(), train_config)

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

    def on_training_finished(self):
        self.abort_btn.setEnabled(False)
        self.progress_text.append("Training finished.")