from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class DatasetViewerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dataset Viewer Page"))
        
        # Viewer text area
        self.viewer_text = QTextEdit("Dataset details will appear here.")
        layout.addWidget(self.viewer_text)

        self.setLayout(layout)
