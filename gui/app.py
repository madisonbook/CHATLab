from PyQt6.QtWidgets import (
    QApplication
)
import sys
from ConsentWindow import ConsentWindow
from SingleTasks.UAVNavigation import UAVNavigation
from SingleTasks.MonitorLevels import MonitorLevels
from SingleTasks.ChatBox import ChatBox
from singleTaskInput import read_vals

try:
    read_vals()
except Exception as e:
    print(f"Error in read_vals: {e}")

app = QApplication(sys.argv)

window = ChatBox()
window.show()
app.exec()