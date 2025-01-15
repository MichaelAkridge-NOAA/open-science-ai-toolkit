from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

class EvalThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, model_path, data_path):
        super().__init__()
        self.model_path = model_path
        self.data_path = data_path

    def run(self):
        try:
            self.progress.emit("Starting evaluation...")
            cmd = f"yolo task=detect mode=val model={self.model_path} data={self.data_path}"
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
            for line in iter(process.stdout.readline, ''):
                self.progress.emit(line.strip())
            process.stdout.close()
            process.wait()
            self.finished.emit()

            if process.returncode == 0:
                self.progress.emit("Evaluation completed successfully!")
            else:
                self.progress.emit("Evaluation failed. Check the log for details.")
        except Exception as e:
            self.progress.emit(f"Error: {str(e)}")

class ModelEvalPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Model Evaluation Page"))

        # Select trained model
        self.model_path_label = QLabel("Select Trained Model:")
        layout.addWidget(self.model_path_label)
        self.model_path_input = QPushButton("Browse Model File")
        self.model_path_input.clicked.connect(self.browse_model)
        layout.addWidget(self.model_path_input)

        # Select dataset YAML
        self.data_path_label = QLabel("Select Dataset YAML:")
        layout.addWidget(self.data_path_label)
        self.data_path_input = QPushButton("Browse Dataset Config")
        self.data_path_input.clicked.connect(self.browse_data)
        layout.addWidget(self.data_path_input)

        # Start evaluation button
        self.start_eval_btn = QPushButton("Start Evaluation")
        self.start_eval_btn.clicked.connect(self.start_evaluation)
        layout.addWidget(self.start_eval_btn)

        # Evaluation progress log
        self.progress_log = QTextEdit()
        self.progress_log.setReadOnly(True)
        layout.addWidget(QLabel("Evaluation Progress:"))
        layout.addWidget(self.progress_log)

        self.setLayout(layout)

    def browse_model(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "Select Model File", "", "Model Files (*.pt)")
        if model_path:
            self.model_path_label.setText(f"Model: {model_path}")

    def browse_data(self):
        data_path, _ = QFileDialog.getOpenFileName(self, "Select Dataset Config File", "", "YAML Files (*.yaml)")
        if data_path:
            self.data_path_label.setText(f"Dataset: {data_path}")

    def start_evaluation(self):
        model_path = self.model_path_label.text().replace("Model: ", "")
        data_path = self.data_path_label.text().replace("Dataset: ", "")
        if not model_path or not data_path:
            self.progress_log.append("Please select both model and dataset YAML files.")
            return

        self.eval_thread = EvalThread(model_path, data_path)
        self.eval_thread.progress.connect(self.update_progress)
        self.eval_thread.finished.connect(self.eval_finished)
        self.eval_thread.start()

    def update_progress(self, message):
        self.progress_log.append(message)
        self.progress_log.ensureCursorVisible()

    def eval_finished(self):
        self.progress_log.append("Evaluation finished.")
