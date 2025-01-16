import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton, QLabel, QHBoxLayout, QMainWindow, QToolButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QImage, QFont
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtSvg import QSvgRenderer
from qdarktheme import setup_theme

def get_colored_svg_icon(path, color):
    renderer = QSvgRenderer(path)
    image = QImage(renderer.defaultSize(), QImage.Format_ARGB32)
    image.fill(Qt.transparent)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    colored_image = QImage(image.size(), QImage.Format_ARGB32)
    colored_image.fill(color)
    painter = QPainter(colored_image)
    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawImage(0, 0, image)
    painter.end()
    return QIcon(QPixmap.fromImage(colored_image))


class CustomTitleBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomTitleBar, self).__init__(parent)
        self.parent = parent
        self.setFixedHeight(45)
        self.setMouseTracking(True)
        self._startPos = None

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("./icons/logo.png").scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setFixedSize(45, 45)
        self.layout.addWidget(self.logo)

        self.title = QLabel(parent.windowTitle(), self)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setStyleSheet("QLabel { font-size: 14pt; font-weight: bold; color: white; margin-left: 8px; }")
        self.layout.addWidget(self.title, stretch=1)

        self.min_button = QToolButton(self)
        self.min_button.setIcon(get_colored_svg_icon("./icons/circle.svg", Qt.green))
        self.min_button.setFixedSize(QSize(24, 24))
        self.min_button.clicked.connect(parent.showMinimized)

        self.max_button = QToolButton(self)
        self.max_button.setIcon(get_colored_svg_icon("./icons/circle.svg", Qt.yellow))
        self.max_button.setFixedSize(QSize(24, 24))
        self.max_button.clicked.connect(self.toggleMaximizeRestore)

        self.close_button = QToolButton(self)
        self.close_button.setIcon(get_colored_svg_icon("./icons/circle.svg", Qt.red))
        self.close_button.setFixedSize(QSize(24, 24))
        self.close_button.clicked.connect(parent.close)

        buttons = [self.min_button, self.max_button, self.close_button]
        for button in buttons:
            button.setFocusPolicy(Qt.NoFocus)
            button.setStyleSheet("QToolButton { border: none; background-color: transparent; } QToolButton:hover { background-color: rgba(255, 255, 255, 0.1); }")
            self.layout.addWidget(button)

    def toggleMaximizeRestore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._startPos:
            self.parent.move(event.globalPos() - self._startPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._startPos = None
        event.accept()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Open Science AI Toolbox")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("MainContainer")
        self.setCentralWidget(self.central_widget)
        self.initUI()
        # Apply styles for rounded corners
        self.central_widget.setStyleSheet(
            """
            #MainContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e3c72, stop:1 #2a5298);
                border-radius: 20px; /* Rounded corners */
            }
            """
        )
        # Size grip with customized styling
        self.sizeGripBR = QtWidgets.QSizeGrip(self.central_widget)
        self.sizeGripBR.setStyleSheet("QSizeGrip { width: 15px; height: 15px; background: transparent; }")
        self.sizeGripBR.setGeometry(self.width() - 20, self.height() - 20, 15, 15)

        # Ensure the size grip moves with the window resizing
        self.central_widget.resizeEvent = self.onResize

    def onResize(self, event):
        self.sizeGripBR.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
        super().resizeEvent(event)

    def initUI(self):
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        self.titleBar = CustomTitleBar(self)
        layout.addWidget(self.titleBar)

        # Assuming IntroPage and other pages are properly defined elsewhere in your application
        self.introPage = IntroPage(self)
        layout.addWidget(self.introPage)

        self.tabs = QTabWidget()
        icon_size = QSize(40, 40)
        self.tabs.addTab(TrainingPage(), get_colored_svg_icon("./icons/gears.svg", Qt.white), "Training")
        self.tabs.addTab(DataPrepPage(), get_colored_svg_icon("./icons/images.svg", Qt.white), "Data Preparation")
        self.tabs.addTab(DatasetViewerPage(), get_colored_svg_icon("./icons/magnifying-glass.svg", Qt.white), "Dataset Viewer")
        self.tabs.addTab(ModelEvalPage(), get_colored_svg_icon("./icons/chart-pie.svg", Qt.white), "Model Evaluation")
        self.tabs.setIconSize(icon_size)
        self.tabs.setVisible(False)
        layout.addWidget(self.tabs)
    def navigateTo(self, index):
        self.introPage.setVisible(False)
        self.tabs.setVisible(True)
        self.tabs.setCurrentIndex(index)

        


class IntroPage(QWidget):
    
    def __init__(self, main_app):
        super().__init__()
        layout = QVBoxLayout()
        welcome_text = """
        <h1>Welcome to the Open Science AI Toolbox!</h1>
        Choose a module to get started.<br>
        <a href='https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit'>GitHub Repository</a> | Version: v2025
        """
        welcome_label = QLabel(welcome_text)
        welcome_label.setOpenExternalLinks(True)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setTextFormat(Qt.RichText)
        welcome_label.setWordWrap(True)
        welcome_label.setFont(QFont('Arial', 16))
        layout.addWidget(welcome_label)
        icon_size = QSize(100, 100)
        font_buttons = QFont('Arial', 14, QFont.Bold)

        btn_training = QPushButton("Training")
        btn_training.setIcon(get_colored_svg_icon("./icons/gears.svg", Qt.white))
        btn_training.setIconSize(icon_size)
        btn_training.setFont(font_buttons)
        btn_training.clicked.connect(lambda: main_app.navigateTo(0))

        btn_data_prep = QPushButton("Data Preparation")
        btn_data_prep.setIcon(get_colored_svg_icon("./icons/images.svg", Qt.white))
        btn_data_prep.setIconSize(icon_size)
        btn_data_prep.setFont(font_buttons)
        btn_data_prep.clicked.connect(lambda: main_app.navigateTo(1))

        btn_dataset_viewer = QPushButton("Dataset Viewer")
        btn_dataset_viewer.setIcon(get_colored_svg_icon("./icons/magnifying-glass.svg", Qt.white))
        btn_dataset_viewer.setIconSize(icon_size)
        btn_dataset_viewer.setFont(font_buttons)
        btn_dataset_viewer.clicked.connect(lambda: main_app.navigateTo(2))

        btn_model_eval = QPushButton("Model Evaluation")
        btn_model_eval.setIcon(get_colored_svg_icon("./icons/chart-pie.svg", Qt.white))
        btn_model_eval.setIconSize(icon_size)
        btn_model_eval.setFont(font_buttons)
        btn_model_eval.clicked.connect(lambda: main_app.navigateTo(3))

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_training)
        button_layout.addWidget(btn_data_prep)
        button_layout.addWidget(btn_dataset_viewer)
        button_layout.addWidget(btn_model_eval)

        layout.addLayout(button_layout)
        self.setLayout(layout)

if __name__ == "__main__" and __package__ is None:
    from model_training.train import TrainingPage
    from data_prep.data_prep import DataPrepPage
    from dataset_viewer.dataset_viewer import DatasetViewerPage
    from model_evaluation.model_eval import ModelEvalPage
else:
    from .model_training.train import TrainingPage
    from .data_prep.data_prep import DataPrepPage
    from .dataset_viewer.dataset_viewer import DatasetViewerPage
    from .model_evaluation.model_eval import ModelEvalPage

def main():
    app = QApplication(sys.argv)
    setup_theme("dark")
    main_app = MainApp()
    main_app.show()
    app.exec_()
if __name__ == "__main__":
    main()