from PyQt6.QtWidgets import (
    QApplication
)
import sys
from ConsentWindow import ConsentWindow
from Instructions.InstrUAV import InstrUAV
from SingleTasks.UAVNavigation import UAVNavigation
from SingleTasks.MonitorLevels import MonitorLevels
from SingleTasks.ChatBoxTemp import ChatBox
from ReadInput.singleTaskInput import read_vals
from ReadInput.breakBlockInput import read_break

try:
    read_vals()
    read_break()
except Exception as e:
    print(f"Error in read_vals: {e}")

app = QApplication(sys.argv)

window = ChatBox()
window.show()
app.exec()