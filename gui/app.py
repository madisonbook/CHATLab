from PyQt6.QtWidgets import (
    QApplication
)
import sys
from ConsentWindow import ConsentWindow
from Instructions.InstrPracChat import InstrPracChat
from SingleTasks.ChatBoxTemp import ChatBox
from MultiTasks.multi_auto1 import Multi_Auto1
from MultiTasks.multi1 import MultiTask1
from PracticeTrials.PracMtrAuto import PracMtrAuto
from ReadInput.singleTaskInput import read_single
from ReadInput.practiceInput import read_practice
from ReadInput.practiceMultiInput import read_practice_multi
from ReadInput.practiceMultiAuto import read_practice_multiauto
from ReadInput.multi1Input import read_multi1
from ReadInput.multi2Input import read_multi2
from ReadInput.multiauto1Input import read_multiauto1
from ReadInput.multiauto2Input import read_multiauto2
from ReadInput.breakBlockInput import read_break

try:
    read_practice()
    read_practice_multi()
    read_single()
    read_multi1()
    read_multi2()
    read_practice_multiauto()
    read_multiauto1()
    read_multiauto2()
    read_break()
except Exception as e:
    print(f"Error in read_vals: {e}")

app = QApplication(sys.argv)

window = PracMtrAuto()
window.show()
app.exec()