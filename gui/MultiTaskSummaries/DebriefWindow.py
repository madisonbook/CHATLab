from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QGroupBox,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QPlainTextEdit,
    QStackedLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class DebriefWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Use in Multitasking Contexts")

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        title_label = Title("Debrief Form: Automation Use in Multitasking Contexts")
        main_layout.addWidget(title_label)
        #main_layout.addSpacing(10)

        subtitle_study = Subtitle("Title of Study: Automation Use in Multitasking Contexts")
        main_layout.addWidget(subtitle_study)
        subtitle_irb = Subtitle("IRB Protocol: 28230")
        main_layout.addWidget(subtitle_irb)
        subtitle_pi = Subtitle("Principal Investigator: Dr. Colleen Patton; cpatton4@ncsu.edu")
        main_layout.addWidget(subtitle_pi)

        text_block = TextBlock()

        body_layout = QVBoxLayout()
        body_layout.addSpacing(5)
        body_layout.addWidget(text_block, alignment=Qt.AlignmentFlag.AlignCenter)

        #self.stacked_questions = QStackedLayout()
        #questions = QWidget()
        #questions.setLayout(self.stacked_questions)

        #self.q_employment = QWidget()
        #q1 = QVBoxLayout()
        #self.group1_title = GroupTitle("Are you currently employed by NC State?")
        #group1, self.radio1_1, self.radio1_2 = EmployedGroup()
        #button_layout, self.button_employed = SubmitEmployeed(self, self.radio1_1, self.radio1_2)

        #q1.addWidget(self.group1_title)
        #q1.addLayout(group1)
        #q1.addLayout(button_layout)
        #self.q_employment.setLayout(q1)

        #self.stacked_questions.addWidget(self.q_employment)
        #self.stacked_questions.addWidget(self.q_consent)

        #body_layout.addWidget(questions)
        main_layout.addLayout(body_layout)
        main_layout.addSpacing(10)

        self.showMaximized()

def Title(str: str):
    title_label = QLabel(str)
    title_label.setFont(QFont("Times New Roman", 24, QFont.Weight.Bold))
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return title_label

def Subtitle(str: str):
    subtitle_label = QLabel(str)
    subtitle_label.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
    subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return subtitle_label

def TextBlock():
    text_block = QPlainTextEdit()
    text_block.setPlainText("""In general terms, in our experiments we are looking at how you decide to use and agree with automation. We are studying fundamental human cognition and perception with a long-term goal of helping people make better decisions surrounding automation use. 
 
In this experiment, both your success at the task and the way that you responded were collected, and these will be used to determine performance on different aspects of the task. However, we are not looking at any individual’s performance, but rather try to determine whether differences between groups of people performing under different conditions can be explained by factors like the type of automated support you received or how you perceived the task and your own performance.
 
Note that your data will be identified using an arbitrary subject number. At no time will your name be connected with your data. 
 
These studies advance both basic science in Psychology, adding to our understanding of human capacities and limitations. They also contribute to the potential future application of Psychology to real-world situations; for example, by providing insight into how to present information or automated assistance to improve decision making. 
  
If you have any questions or concerns about this research, or would like to discuss the results after the experiment has been completed, please contact Colleen Patton using the following information: 
 
Colleen Patton
colleen_patton@ncsu.edu 
(919) 515 1721
Department of Psychology 
North Carolina State University
Raleigh, NC
                            
Thank you for participating!""")
    
    text_block.setReadOnly(True)
    text_block.setFixedHeight(560)
    text_block.setFont(QFont("Times New Roman", 14, QFont.Weight.Normal))
    text_block.setFixedWidth(1300)

    return text_block

def GroupTitle(str: str):
    group_title = QLabel(str)
    group_title.setFont(QFont("Times New Roman", 14, QFont.Weight.DemiBold))
    group_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return group_title
