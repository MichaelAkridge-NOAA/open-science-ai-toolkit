from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class DatasetViewerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dataset Viewer Page - PLACEHOLDER"))
        
        # Viewer text area
        self.viewer_text = QTextEdit("PLACEHOLDER | Dataset details for QA/QC will appear here. | PLACEHOLDER")
        layout.addWidget(self.viewer_text)

        self.setLayout(layout)
