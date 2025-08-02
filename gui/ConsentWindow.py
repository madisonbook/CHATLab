from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QGroupBox,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QPlainTextEdit,
    QStackedLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from IneligibleWindow import IneligibleWindow
from Instructions.InstrMonitor import InstrMonitor

class ConsentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Use in Multitasking Contexts")

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        title_label = Title("Consent Form: Automation Use in Multitasking Contexts")
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

        self.stacked_questions = QStackedLayout()
        questions = QWidget()
        questions.setLayout(self.stacked_questions)

        self.q_employment = QWidget()
        q1 = QVBoxLayout()
        self.group1_title = GroupTitle("Are you currently employed by NC State?")
        group1, self.radio1_1, self.radio1_2 = EmployedGroup()
        button_layout, self.button_employed = SubmitEmployeed(self, self.radio1_1, self.radio1_2)

        q1.addWidget(self.group1_title)
        q1.addLayout(group1)
        q1.addLayout(button_layout)
        self.q_employment.setLayout(q1)
        
        self.q_consent = QWidget()
        q2 = QVBoxLayout()
        self.group2_title = GroupTitle("If you consent to participate in this research study, please click the “Yes I consent” button.\nIf you do not consent to participate in this study, please inform your research assistant. ")
        group2, self.radio2_1, self.radio2_2 = ConsentGroup()
        button_layout2, self.button_consent = SubmitConsent(self, self.radio2_1, self.radio2_2)

        q2.addWidget(self.group2_title)
        q2.addLayout(group2)
        q2.addLayout(button_layout2)
        self.q_consent.setLayout(q2)

        self.stacked_questions.addWidget(self.q_employment)
        self.stacked_questions.addWidget(self.q_consent)

        body_layout.addWidget(questions)
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
    text_block.setPlainText("""You are being asked to participate in a research study about using automated systems in multitasking contexts. Participation is strictly voluntary. You must be 18 years of age or older, reside in the United States, have normal or corrected-to-normal vision, and not be an employee of North Carolina State University to participate in this study. 

If you participate in this study, you will engage in a simulated unmanned ariel vehicle (UAV – like a drone) task. You will be asked to monitor gauge levels, choose navigation paths for drones, and respond to incoming intel. You will sometimes have automated systems to help you complete these tasks. You will also complete survey questions about your experience during the tasks. All tasks will occur on this computer. Although your responses in the experiment will be recorded, no photos/videos of you will be recorded. 

You can choose to not participate in the study or stop participating at any time by informing the research assistant. 

Participants will or have their activity in the task recorded during the research activities. If you do not want this information collected, you cannot participate in this research. We would like to use these recordings for data analysis. We will keep these recordings indefinitely, but they will not be linked to you. 

There are minimal risks associated with your participation in this research. There are no direct benefits to you from participating in this research.

You receive 1 credit per half hour (2 credits per hour) for participating in this research. In order to receive full compensation, you must complete all research activities. 

Instead of participating in this research project, you can select another study in SONA to complete for course credit or you can contact your professor for an alternative assignment that will take the same amount of time and effort for the same amount of course credit. 

If you have any questions about the research or how it is implemented, please contact the researcher, Colleen Patton, at cpatton4@ncsu.edu. Please reference study number 28230 when contacting anyone about this project.

If you have questions about your rights as a participant or are concerned with your treatment throughout the research process, please contact the NC State University IRB Director at IRB-Director@ncsu.edu, 919-515-8754, or fill out a confidential form online at https://research.ncsu.edu/administration/compliance/research-compliance/irb/irb-forms-and-templates/participant-concern-and-complaint-form/ 
                            """)
    
    text_block.setReadOnly(True)
    text_block.setFixedHeight(500)
    text_block.setFont(QFont("Times New Roman", 14, QFont.Weight.Normal))
    text_block.setFixedWidth(1300)

    return text_block

def GroupTitle(str: str):
    group_title = QLabel(str)
    group_title.setFont(QFont("Times New Roman", 14, QFont.Weight.DemiBold))
    group_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return group_title

def EmployedGroup():
    group1_layout = QHBoxLayout()

    radio1_1 = QRadioButton("Yes")
    radio1_1.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))
    radio1_2 = QRadioButton("No")
    radio1_2.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))

    group1_layout.addStretch()
    group1_layout.addWidget(radio1_1)
    group1_layout.addSpacing(80)
    group1_layout.addWidget(radio1_2)
    group1_layout.addStretch()
    return group1_layout, radio1_1, radio1_2

def SubmitEmployeed(self, radio1, radio2):
    submit_button = QPushButton("Submit")
    submit_button.setFixedWidth(125)
    submit_button.setFixedHeight(30)
    submit_button.clicked.connect(lambda: HandleSubmitEmployeed(self, radio1, radio2))
    submit_button.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))
    submit_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

    button_layout = QHBoxLayout()
    button_layout.addStretch()
    button_layout.addWidget(submit_button)
    button_layout.addStretch()

    return button_layout, submit_button

def HandleSubmitEmployeed(self, radio1, radio2):
    if radio1.isChecked():
        self.ineligible = IneligibleWindow()
        self.ineligible.show()
        self.close()
    elif radio2.isChecked():
        self.stacked_questions.setCurrentWidget(self.q_consent)
    else:
        print("No selection made.")
    pass

def ConsentGroup():
    group1_layout = QHBoxLayout()

    radio1_1 = QRadioButton("Yes, I consent to participate")
    radio1_1.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))
    radio1_2 = QRadioButton("No, I do not consent to participate")
    radio1_2.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))

    group1_layout.addStretch()
    group1_layout.addWidget(radio1_1)
    group1_layout.addSpacing(5)
    group1_layout.addWidget(radio1_2)
    group1_layout.addStretch()
    return group1_layout, radio1_1, radio1_2

def SubmitConsent(self, radio1, radio2):
    submit_button = QPushButton("Submit")
    submit_button.setFixedWidth(125)
    submit_button.setFixedHeight(30)
    submit_button.clicked.connect(lambda: HandleSubmitConsent(self, radio1, radio2))
    submit_button.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))
    submit_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

    button_layout = QHBoxLayout()
    button_layout.addStretch()
    button_layout.addWidget(submit_button)
    button_layout.addStretch()

    return button_layout, submit_button

def HandleSubmitConsent(self, radio1, radio2):
    if radio1.isChecked():
        self.instructions = InstrMonitor()
        self.instructions.show()
        self.close()
    elif radio2.isChecked():
        self.ineligible = IneligibleWindow()
        self.ineligible.show()
        self.close()
    pass