from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

class DataPrepPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Data Preparation Page"))
        
        # Load dataset button
        self.load_dataset_btn = QPushButton("Load Dataset")
        self.load_dataset_btn.clicked.connect(self.load_dataset)
        layout.addWidget(self.load_dataset_btn)

        self.setLayout(layout)

    def load_dataset(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Dataset Folder")
        if folder:
            print(f"Dataset loaded from: {folder}")
