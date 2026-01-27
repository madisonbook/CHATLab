from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QGroupBox,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QGuiApplication
from PracticeTrials.PracUAVNavigation import UAVNavigation
from ReadInput import breakBlockInput

class InstrPracUAV(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Use in Multitasking Contexts")

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        main_layout.addStretch()

        title = Title("Instructions: Practice UAV Navigation")
        main_layout.addWidget(title)
        main_layout.addSpacing(10)

        if breakBlockInput.break3:
            participate = Subtitle(breakBlockInput.break3)
        else: 
            participate = Subtitle("Please let your research assistant know that you've reached a break point.")

        main_layout.addWidget(participate, 0, Qt.AlignmentFlag.AlignHCenter)
        main_layout.addSpacing(10)

        continue_button = QPushButton("Click Here to Start")
        continue_button.setFont(QFont("Times New Roman", 16))
        continue_button.clicked.connect(lambda: StartUAV(self))
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
    subtitle_label.setFont(QFont("Times New Roman", 18, QFont.Weight.Medium))
    subtitle_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    subtitle_label.setWordWrap(True)

    screen = QGuiApplication.primaryScreen().geometry()
    screen_width = screen.width()
    subtitle_label.setMaximumWidth(int(screen_width * 0.75))
    subtitle_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    return subtitle_label

def StartUAV(self):
    self.monitor = UAVNavigation()
    self.monitor.show()
    self.close()
