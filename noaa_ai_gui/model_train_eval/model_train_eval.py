from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFileDialog, QLabel, QFrame, QApplication
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPainter, QImage, QIcon, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.ndimage import gaussian_filter1d
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class TrainingEvalPage(QWidget):
    def __init__(self):
        super().__init__()
        self.csv_file = None  # Initialize csv_file to None
        self.init_ui()

    def init_ui(self):
        # Set the background color to gray
        self.setStyleSheet("background-color: #808080;")
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setAcceptDrops(True)  # Enable drag-and-drop functionality

        # Drag-and-drop area with combined functionality
        self.drag_drop_frame = QFrame(self)
        self.drag_drop_frame.setAcceptDrops(True)
        self.drag_drop_frame.setStyleSheet(
            "background-color: #f8f8f8; border: 2px dashed #aaa; padding: 20px;"
        )
        self.drag_drop_frame.setLayout(QVBoxLayout())

        # Instructions and icon
        self.instruction_label = QLabel(
            "Drag and Drop Training results.csv Here\nor Click to Browse"
        )
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("font-size: 18px; color: gray;")
        self.drag_drop_frame.layout().addWidget(self.instruction_label)

        self.drag_drop_frame.mousePressEvent = self.browse_file  # Handle click events to open file dialog

        # Add drag-and-drop frame to the main layout
        self.layout.addWidget(self.drag_drop_frame)

        # Main plot area
        self.web_view = QWebEngineView()
        self.web_view.hide()  # Initially hide the web view
        self.layout.addWidget(self.web_view)

        # Set the initial window size
        #self.resize(1400, 1400)  # Match the size of the Plotly figure

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.endswith(".csv"):
            self.load_dataset_info(file_path)

    def browse_file(self, event=None):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.load_dataset_info(file_path)

    def load_dataset_info(self, file_path):
        self.csv_file = file_path
        logging.info(f"CSV file selected: {file_path}")
        self.drag_drop_frame.hide()  # Hide the drag-and-drop frame when a file is loaded
        self.generate_and_display_plot()  # Automatically generate the plot

    def generate_and_display_plot(self):
        if self.csv_file:
            try:
                plot_html = self.plot_results_interactive(self.csv_file)
                self.web_view.setHtml(plot_html)
                self.web_view.show()  # Show the web view after the plot is loaded
                logging.info("Plot displayed successfully.")
            except Exception as e:
                logging.error(f"Error generating plot: {e}")
        else:
            logging.warning("No CSV file selected.")

    def plot_results_interactive(self, file):
        try:
            data = pd.read_csv(file)
            column_names = data.columns
            rows, cols = 2, 5  # Adjust based on your CSV data structure
            index = range(1, min(len(column_names), rows * cols + 1))  # Dynamically adjust columns

            fig = make_subplots(
                rows=rows,
                cols=cols,
                subplot_titles=[column_names[i] for i in index],
            )

            x = data.iloc[:, 0]  # Assuming the first column is the x-axis
            for i, j in enumerate(index):
                y = data.iloc[:, j]
                smooth_y = gaussian_filter1d(y, sigma=3)
                fig.add_trace(
                    go.Scatter(x=x, y=y, mode="lines+markers", name=column_names[j]),
                    row=(i // cols) + 1,
                    col=(i % cols) + 1,
                )
                fig.add_trace(
                    go.Scatter(x=x, y=smooth_y, mode="lines", showlegend=False),  # Hide smooth legend
                    row=(i // cols) + 1,
                    col=(i % cols) + 1,
                )

            fig.update_layout(
                height=900,
                width=1400,
                title_text="Training Results Overview",
            )
            return fig.to_html(full_html=False, include_plotlyjs="cdn")
        except Exception as e:
            logging.error(f"Error reading or plotting CSV file: {e}")
            raise

