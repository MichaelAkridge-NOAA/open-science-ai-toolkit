from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QListWidget, QStackedWidget
from .model_training.train import TrainingPage
from .data_prep.data_prep import DataPrepPage
from .dataset_viewer.dataset_viewer import DatasetViewerPage
from .model_evaluation.model_eval import ModelEvalPage

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLO Multi-Page GUI")
        self.setGeometry(100, 100, 800, 600)

        layout = QHBoxLayout(self)

        # Navigation menu
        self.menu = QListWidget()
        self.menu.addItems(["Training", "Data Preparation", "Dataset Viewer", "Model Evaluation"])
        self.menu.currentRowChanged.connect(self.display_page)
        layout.addWidget(self.menu, 1)

        # Stacked widget for pages
        self.pages = QStackedWidget()
        self.pages.addWidget(TrainingPage())
        self.pages.addWidget(DataPrepPage())
        self.pages.addWidget(DatasetViewerPage())
        self.pages.addWidget(ModelEvalPage())
        layout.addWidget(self.pages, 4)

        self.setLayout(layout)

    def display_page(self, index):
        self.pages.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication([])
    main_app = MainApp()
    main_app.show()
    app.exec_()
