from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QGroupBox,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QPlainTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from MultiTasks.multi1 import MultiTask1

class InstrMulti1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Use in Multitasking Contexts")

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        main_layout.addStretch()

        title = Title("Instructions: Multitasking")
        main_layout.addWidget(title)
        main_layout.addSpacing(10)

        participate = Subtitle("Multitasking time yippeeeee")
        main_layout.addWidget(participate)

        main_layout.addSpacing(10)

        continue_button = QPushButton("Click Here to Start")
        continue_button.setFont(QFont("Times New Roman", 16))
        continue_button.clicked.connect(lambda: StartMulti(self))
        continue_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        main_layout.addWidget(continue_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch()
        self.showMaximized()
    
def Title(str: str):
    title_label = QLabel(str)
    title_label.setFont(QFont("Times New Roman", 24, QFont.Weight.Bold))
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return title_label

def Subtitle(str: str):
    subtitle_label = QLabel(str)
    subtitle_label.setFont(QFont("Times New Roman", 16, QFont.Weight.DemiBold))
    subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return subtitle_label

def StartMulti(self):
    self.multi = MultiTask1()
    self.multi.show()
    self.close()
