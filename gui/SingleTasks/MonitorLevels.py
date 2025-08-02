from PyQt6.QtWidgets import (
    QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QPlainTextEdit,
    QGraphicsScene, QGraphicsView
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QBrush, QPen, QColor
#from .GenerateLevel import GenerateLevel
from SingleTaskSummaries.SumMonitor import SumMonitor
from participant import PARTICIPANT_ID
import singleTaskInput
import random
import datetime
from DataLogging.LogMonitor import LogMonitor, MonitorCSV

base_width = 125
base_height = 300
border_thickness = 4

summary = []
gauges = []
total_oob = 0
total_reset = 0

class MonitorLevels(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Use in Multitasking Contexts")

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        title = Title("Task: Monitor Levels")
        main_layout.addWidget(title)
        main_layout.addSpacing(50)

        game_form = QHBoxLayout()
        game_form.addStretch()
        game_form.addStretch()

        colors = ["#FF7F7F", "#FFEE8c", "#88E788", "#90D5FF"]
        idx = 0
        for color in colors:
            gauge = GenerateLevel(color, idx)
            idx = idx + 1
            gauges.append(gauge)
            game_form.addLayout(gauge.form)

        game_form.addStretch()
        game_form.addStretch()

        main_layout.addLayout(game_form)

        main_layout.addStretch()
        self.showMaximized()

        QTimer.singleShot(singleTaskInput.gauge_duration*1000, lambda: self.StartSummary())

    def StartSummary(self):
        summary = [total_reset, total_oob]
        self.showSum = SumMonitor(summary)
        MonitorCSV()
        self.showSum.show()
        self.close()    

class GenerateLevel(QWidget):
    def __init__(self, color_hex: str, idx: int):
        super().__init__()

        self.oob = False
        self.reset = False
        self.monitor_level = random.randint(singleTaskInput.gauge_mean[idx] - singleTaskInput.gauge_dist[idx], singleTaskInput.gauge_mean[idx] + singleTaskInput.gauge_dist[idx])
        self.oob_time = None

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(lambda: self.Animate())
        self.animation_duration = 500
        self.animation_interval = 16
        self.animation_start_time = None
        self.animation_start_height = self.monitor_level
        self.animation_end_height = self.monitor_level

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.ChangeHeight(idx))
    
        self.form = QVBoxLayout()

        level = QGraphicsScene(0, 0, base_width + border_thickness, base_height + border_thickness)

        base = level.addRect(0, 0, base_width, base_height)
        base.setPos(border_thickness/2, border_thickness/2)
        brush = QBrush(QColor(color_hex))
        base.setBrush(brush)

        self.inner_level = level.addRect(0, 0, base_width, self.monitor_level)
        self.inner_level.setPos(border_thickness/2, border_thickness/2)
        brush = QBrush(Qt.GlobalColor.white)
        self.inner_level.setBrush(brush)
        no_pen = QPen(Qt.GlobalColor.white)
        no_pen.setWidth(0)
        self.inner_level.setPen(no_pen)

        outline = level.addRect(0, 0, base_width, base_height)
        outline.setPos(border_thickness/2, border_thickness/2)
        outline_brush = QBrush(Qt.GlobalColor.transparent)
        outline.setBrush(outline_brush)
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(border_thickness)
        outline.setPen(pen)

        top_bar = level.addRect(0, 0, 40, 0)
        top_bar.setPos(0, singleTaskInput.gauge_mean[idx] - singleTaskInput.gauge_dist[idx])
        top_bar.setPen(pen)

        low_bar = level.addRect(0, 0, 40, 0)
        low_bar.setPos(0, singleTaskInput.gauge_mean[idx] + singleTaskInput.gauge_dist[idx])
        low_bar.setPen(pen)

        form_view = QGraphicsView(level)
        self.form.addWidget(form_view)
        self.form.addSpacing(5)

        reset_button = QPushButton("Reset")
        reset_button.setFont(QFont("Times New Roman", 16))
        reset_button.clicked.connect(lambda: self.ResetLevel(idx))
        reset_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 6px;
                padding: 6px 25px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

        self.form.addWidget(reset_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.TimerDelay()

    def ResetLevel(self, idx:int):
        #self.inner_level.setRect(0, 0, base_width, mean_level)
        self.AnimateHeight(singleTaskInput.gauge_mean[idx])
        self.monitor_level = singleTaskInput.gauge_mean[idx]
        self.reset = True

        if self.oob:
            global total_reset 
            total_reset = total_reset + 1
            self.oob = False
            LogGauges()

        self.oob_time = None
        self.TimerDelay()
        pass

    def TimerDelay(self):
        delay = random.randint(singleTaskInput.gauge_timer[0]*1000, singleTaskInput.gauge_timer[1]*1000)
        self.reset = False
        self.timer.start(delay)

    def ChangeHeight(self, idx: int):
        new_height = max(10, min(290, int(random.normalvariate(singleTaskInput.gauge_mean[idx], singleTaskInput.gauge_sd[idx]))))
        
        self.AnimateHeight(new_height)
        self.monitor_level = new_height

        self.CheckOOB(new_height, idx)
        self.inner_level.setRect(0, 0, base_width, new_height)

        if self.oob:
            global total_oob
            total_oob = total_oob + 1
            self.oob_time = datetime.datetime.now()
            LogGauges()

        self.TimerDelay()

    def CheckOOB(self, new_height, idx):
        if new_height < (singleTaskInput.gauge_mean[idx] - singleTaskInput.gauge_dist[idx]) or new_height > (singleTaskInput.gauge_mean[idx] + singleTaskInput.gauge_dist[idx]):
            self.oob = True
        else:
            self.oob = False
        return
    
    def AnimateHeight(self, new_height):
        self.animation_timer.stop()
        self.animation_start_time = datetime.datetime.now()
        self.animation_start_height = self.monitor_level
        self.animation_end_height = new_height
        self.animation_timer.start(self.animation_interval)
        pass

    def Animate(self):
        elapsed = (datetime.datetime.now() - self.animation_start_time).total_seconds() * 1000  # ms
        progress = min(1.0, elapsed / self.animation_duration)

        interpolated_height = (
            self.animation_start_height +
            (self.animation_end_height - self.animation_start_height) * progress
        )

        self.monitor_level = interpolated_height
        self.inner_level.setRect(0, 0, base_width, interpolated_height)

        if progress >= 1.0:
            self.monitor_level = self.animation_end_height
            self.animation_timer.stop()
 
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

def LogGauges():
    # block, trial, gauges, auto, auto_type, total_oob, total_reset
    block = 1
    trial = 1
    auto = str(False)
    auto_type = "None"

    LogMonitor(block, trial, gauges, auto, auto_type, total_oob, total_reset)
    pass
