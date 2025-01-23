import os
import yaml
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QGridLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem, QComboBox, QFrame, QSpacerItem, QSizePolicy,QGroupBox)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QColor,QDragEnterEvent, QDropEvent,QImage
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QUrl
from PyQt5.QtSvg import QSvgRenderer


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

class ThumbnailLabel(QLabel):
    clicked = pyqtSignal(str)  # Signal to emit the image path

    def __init__(self, image_path, label_path=None, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.label_path = label_path
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print("Failed to load image at:", image_path)
            pixmap = QPixmap(100, 100)  # Create a blank pixmap if loading fails
            pixmap.fill(Qt.gray)
        elif label_path and os.path.exists(label_path):
            pixmap = self.parent().draw_bounding_boxes(pixmap, label_path)

        self.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setFrameStyle(QFrame.StyledPanel)
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.image_path)  # Emit the path of the image when clicked

class DatasetViewerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.dataset_splits = {}
        self.current_page = 0
        self.items_per_page = 10
        self.total_images = []
        self.init_ui()
        self.setAcceptDrops(True)  # Enable drag and drop

    def init_ui(self):
        main_layout = QHBoxLayout(self)  # Main layout for the entire widget

        # Left Column: Controls for file selection and dataset splitting
        control_layout = QVBoxLayout()
        
        # Customized Browse Button with SVG Icon
        self.browse_button = QPushButton(" Drag and Drop Dataset YAML\n or Click to browse for file")
        self.browse_button.setIcon(get_colored_svg_icon("./icons/file-arrow-up.svg", Qt.white))
        self.browse_button.setIconSize(QSize(35, 35))  # Correctly adjust the icon size
        self.browse_button.clicked.connect(self.browse_file)
        self.browse_button.setFixedSize(220, 60)  # Adjust size as needed to fit text and icon
        control_layout.addWidget(self.browse_button)

        # Label and ComboBox for dataset split selection
        self.instruction_label = QLabel("Select Dataset Split")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setVisible(False)
        control_layout.addWidget(self.instruction_label)
        
        self.split_selector = QComboBox()
        self.split_selector.addItems(['Train', 'Validation', 'Test'])
        self.split_selector.currentTextChanged.connect(self.load_images)
        self.split_selector.setFixedSize(200, 50)
        self.split_selector.setVisible(False)
        control_layout.addWidget(self.split_selector)
        # Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        control_layout.addSpacerItem(spacer)
        main_layout.addLayout(control_layout)

        # Right Column: Group Box for Thumbnail Grid and Navigation Buttons
        self.thumbnail_group_box = QGroupBox("Select Thumbnail")
        thumbnail_layout = QVBoxLayout(self.thumbnail_group_box)
        self.thumbnail_group_box.setVisible(False)
        # Thumbnail widget and grid
        self.thumbnail_widget = QWidget()
        self.thumbnail_grid = QGridLayout(self.thumbnail_widget)
        thumbnail_layout.addWidget(self.thumbnail_widget)

        # Navigation buttons setup
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.go_previous)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_button)

        thumbnail_layout.addLayout(nav_layout)
        main_layout.addWidget(self.thumbnail_group_box)

        # Image Viewer (made larger)
        self.image_viewer = QGraphicsView()
        self.image_viewer.setMinimumSize(800, 600)
        main_layout.addWidget(self.image_viewer)

        self.setLayout(main_layout)


    def go_previous(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_grid()

    def go_next(self):
        if (self.current_page + 1) * self.items_per_page < len(self.total_images):
            self.current_page += 1
            self.update_grid()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.endswith('.yaml'):
            self.load_dataset_info(file_path)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Dataset Config File", "", "YAML Files (*.yaml);;All Files (*)")
        if file_path:
            self.load_dataset_info(file_path)

    def load_dataset_info(self, file_path):
        with open(file_path, 'r') as file:
            dataset_config = yaml.safe_load(file)
        base_path = os.path.dirname(file_path)
        self.dataset_splits = {
            'Train': os.path.join(base_path, dataset_config['train']),
            'Validation': os.path.join(base_path, dataset_config['val']),
            'Test': os.path.join(base_path, dataset_config.get('test', ''))
        }
        self.load_images()

    def load_images(self):
        path = self.dataset_splits.get(self.split_selector.currentText())
        if path and os.path.exists(path):
            self.total_images = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.png'))]
            self.thumbnail_group_box.setVisible(True)
            self.split_selector.setVisible(True)
            self.instruction_label.setVisible(True)
        else:
            self.total_images = []
            self.thumbnail_group_box.setVisible(False)
            self.split_selector.setVisible(False)
            self.instruction_label.setVisible(False)
        self.update_grid()


    def update_grid(self):
        for i in reversed(range(self.thumbnail_grid.count())):
            widget = self.thumbnail_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        start = self.current_page * self.items_per_page
        end = min(start + self.items_per_page, len(self.total_images))
        row = col = 0
        for idx in range(start, end):
            image_path = self.total_images[idx]
            label_path = image_path.replace('images', 'labels').replace('.jpg', '.txt').replace('.png', '.txt')
            thumbnail = ThumbnailLabel(image_path, label_path, self)
            thumbnail.clicked.connect(self.display_image)
            self.thumbnail_grid.addWidget(thumbnail, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def draw_bounding_boxes(self, pixmap, label_path):
        painter = QPainter(pixmap)
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)

        if os.path.exists(label_path):
            with open(label_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    class_id, x_center, y_center, width, height = map(float, line.split())
                    x_center *= pixmap.width()
                    y_center *= pixmap.height()
                    width *= pixmap.width()
                    height *= pixmap.height()

                    top_left_x = int(x_center - width / 2)
                    top_left_y = int(y_center - height / 2)
                    painter.drawRect(top_left_x, top_left_y, int(width), int(height))
        painter.end()
        return pixmap

    def display_image(self, image_path):
        original_pixmap = QPixmap(image_path)

        # Assuming labels are stored in a parallel 'labels' directory instead of 'images'
        base_path = os.path.dirname(image_path)
        file_name = os.path.basename(image_path).replace('.jpg', '.txt').replace('.png', '.txt')
        label_path = os.path.join(base_path.replace('images', 'labels'), file_name)

        # Convert path to a consistent format (optional, helps in debugging path issues on Windows)
        label_path = os.path.normpath(label_path)

        #print("Display Image Path:", image_path)
        #print("Display Label Path:", label_path)

        if os.path.exists(label_path):
            self.draw_bounding_boxes(original_pixmap, label_path)
        else:
            print("Label file not found:", label_path)  # Additional debugging information

        scaled_pixmap = original_pixmap.scaled(self.image_viewer.width(), self.image_viewer.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        scene = QGraphicsScene()
        if not scaled_pixmap.isNull():
            item = QGraphicsPixmapItem(scaled_pixmap)
            scene.addItem(item)
        else:
            placeholder_text = QGraphicsTextItem("Image cannot be displayed or is missing.")
            placeholder_text.setDefaultTextColor(Qt.gray)
            scene.addItem(placeholder_text)
            QMessageBox.critical(self, "Error", "Cannot display the image, it may be corrupt or missing.")

        self.image_viewer.setScene(scene)
