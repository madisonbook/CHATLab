from PyQt6.QtWidgets import (
    QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QPlainTextEdit,
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem,
    QGraphicsTextItem, QGroupBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt6.QtGui import QFont, QBrush, QPen, QColor, QPixmap, QPainter, QPolygonF, QPainterPath
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsRectItem, QStackedWidget, QGraphicsProxyWidget
import math
from Instructions.InstrUAV import InstrUAV
from .PracUAVItem import UAVItem
from SingleTasks.NavItems import GoalItem, StormItem
from participant import PARTICIPANT_ID
from ReadInput import practiceInput
from DataLogging.LogNavigation import LogNavigation

summary = []
UAVs = []
total_path = 0
total_correct = 0

img_size = 800

class UAVNavigation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Use in Multitasking Contexts")
        self.curr_uav = None
        self.card_update_timer = QTimer()
        self.card_update_timer.setInterval(1000)  # 1000 ms = 1 second
        self.card_update_timer.timeout.connect(self.TimerUpdateCards)

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        title = Title("Task: Practice UAV Navigation")
        main_layout.addWidget(title)
        main_layout.addSpacing(25)

        game_form = QHBoxLayout()
        left_nav = QGraphicsScene()

        pix = QPixmap("images/UAVnav.jpg").scaled(img_size, img_size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        sat_img = QGraphicsPixmapItem(pix)
        left_nav.addItem(sat_img)

        view = QGraphicsView(left_nav)
        view.setSceneRect(QRectF(pix.rect()))
        view.setFixedSize(img_size, img_size)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)

        home_base = self.CreateHomeBase()
        left_nav.addItem(home_base[0])
        left_nav.addItem(home_base[1])

        storm_items = [StormItem(1, practiceInput.nav_storm_x[0], practiceInput.nav_storm_y[0]),
                      StormItem(2, practiceInput.nav_storm_x[1], practiceInput.nav_storm_y[1]),
                      StormItem(3, practiceInput.nav_storm_x[2], practiceInput.nav_storm_y[2]),
                      StormItem(4, practiceInput.nav_storm_x[3], practiceInput.nav_storm_y[3])]

        for item in storm_items:
            left_nav.addItem(item.pixmap_item)

        goal_items = [GoalItem(1, practiceInput.nav_goal_x[0], practiceInput.nav_goal_y[0]),
                      GoalItem(2, practiceInput.nav_goal_x[1], practiceInput.nav_goal_y[1]),
                      GoalItem(3, practiceInput.nav_goal_x[2], practiceInput.nav_goal_y[2]),
                      GoalItem(4, practiceInput.nav_goal_x[3], practiceInput.nav_goal_y[3])]
        
        #(self, idx, color_hex, color_text, x_pos, y_pos, curr_goal, goals_list, fuel, speed, angle, on_click_callback):
        uav_blue = UAVItem(1, "#90D5FF", "BLUE", practiceInput.nav_uav_x[0], practiceInput.nav_uav_y[0],
                           goal_items[0], goal_items, storm_items, practiceInput.nav_uav_fuel[0], 
                           practiceInput.nav_uav_speed[0], practiceInput.nav_path_angle[0], self.HandleClick, left_nav)
        UAVs.append(uav_blue)
        uav_blue.uav_item.setZValue(3)
        uav_blue.goal_item.setZValue(2)
        uav_blue.hyp_label.setZValue(1)
        uav_blue.hyp_path.setZValue(0)
        uav_blue.ra_label.setZValue(1)
        uav_blue.ra_path.setZValue(0)

        left_nav.addItem(uav_blue.hyp_path)
        left_nav.addItem(uav_blue.hyp_label)
        left_nav.addItem(uav_blue.ra_path)
        left_nav.addItem(uav_blue.ra_label)
        left_nav.addItem(uav_blue.goal_item)
        left_nav.addItem(uav_blue.uav_item)

        uav_blue.hyp_path.setVisible(False)
        uav_blue.hyp_label.setVisible(False)
        uav_blue.ra_path.setVisible(False)
        uav_blue.ra_label.setVisible(False)
   
        uav_red = UAVItem(2, "#FF7F7F", "RED", practiceInput.nav_uav_x[1], practiceInput.nav_uav_y[1],
                          goal_items[1], goal_items, storm_items, practiceInput.nav_uav_fuel[1], 
                           practiceInput.nav_uav_speed[1], practiceInput.nav_path_angle[1], self.HandleClick, left_nav)
        UAVs.append(uav_red)
        uav_red.uav_item.setZValue(3)
        uav_red.goal_item.setZValue(2)
        uav_red.hyp_label.setZValue(1)
        uav_red.hyp_path.setZValue(0)
        uav_red.ra_label.setZValue(1)
        uav_red.ra_path.setZValue(0)

        left_nav.addItem(uav_red.hyp_path)
        left_nav.addItem(uav_red.hyp_label)
        left_nav.addItem(uav_red.ra_path)
        left_nav.addItem(uav_red.ra_label)
        left_nav.addItem(uav_red.goal_item)
        left_nav.addItem(uav_red.uav_item)

        uav_red.hyp_path.setVisible(False)
        uav_red.hyp_label.setVisible(False)
        uav_red.ra_path.setVisible(False)
        uav_red.ra_label.setVisible(False)

        uav_green = UAVItem(3, "#88E788", "GREEN", practiceInput.nav_uav_x[2], practiceInput.nav_uav_y[2],
                           goal_items[2], goal_items, storm_items, practiceInput.nav_uav_fuel[2], 
                           practiceInput.nav_uav_speed[2], practiceInput.nav_path_angle[2], self.HandleClick, left_nav)
        UAVs.append(uav_green)
        uav_green.uav_item.setZValue(3)
        uav_green.goal_item.setZValue(2)
        uav_green.hyp_label.setZValue(1)
        uav_green.hyp_path.setZValue(0)
        uav_green.ra_label.setZValue(1)
        uav_green.ra_path.setZValue(0)

        left_nav.addItem(uav_green.hyp_path)
        left_nav.addItem(uav_green.hyp_label)
        left_nav.addItem(uav_green.ra_path)
        left_nav.addItem(uav_green.ra_label)
        left_nav.addItem(uav_green.goal_item)
        left_nav.addItem(uav_green.uav_item)

        uav_green.hyp_path.setVisible(False)
        uav_green.hyp_label.setVisible(False)
        uav_green.ra_path.setVisible(False)
        uav_green.ra_label.setVisible(False)

        uav_yellow = UAVItem(4, "#FFEE8c", "YELLOW", practiceInput.nav_uav_x[3], practiceInput.nav_uav_y[3], 
                           goal_items[3], goal_items, storm_items, practiceInput.nav_uav_fuel[3], 
                           practiceInput.nav_uav_speed[3], practiceInput.nav_path_angle[3], self.HandleClick, left_nav)
        UAVs.append(uav_yellow)
        uav_yellow.uav_item.setZValue(3)
        uav_yellow.goal_item.setZValue(2)
        uav_yellow.hyp_label.setZValue(1)
        uav_yellow.hyp_path.setZValue(0)
        uav_yellow.ra_label.setZValue(1)
        uav_yellow.ra_path.setZValue(0)

        left_nav.addItem(uav_yellow.hyp_path)
        left_nav.addItem(uav_yellow.hyp_label)
        left_nav.addItem(uav_yellow.ra_path)
        left_nav.addItem(uav_yellow.ra_label)
        left_nav.addItem(uav_yellow.goal_item)
        left_nav.addItem(uav_yellow.uav_item)

        uav_yellow.hyp_path.setVisible(False)
        uav_yellow.hyp_label.setVisible(False)
        uav_yellow.ra_path.setVisible(False)
        uav_yellow.ra_label.setVisible(False)

        self.path_proxy = self.CreatePathChooser()
        left_nav.addItem(self.path_proxy)
        self.path_stack.setCurrentIndex(0)

        self.path_proxy.setVisible(True)
        self.path_stack.setCurrentIndex(0)

        game_form.addWidget(view)

        self.uav_info_stack = QStackedWidget()

        self.uav_info_widget = self.CreateUAVInfoWidget()
        self.uav_info_stack.addWidget(self.uav_info_widget)
        self.uav_info_stack.setCurrentWidget(self.uav_info_widget)


        right_content = QVBoxLayout()
        right_content.addWidget(self.uav_info_stack)
        game_form.addLayout(right_content)

        main_layout.addLayout(game_form)

        main_layout.addStretch()
        self.showMaximized()

        QTimer.singleShot(practiceInput.nav_duration*1000, lambda: self.StartSummary())

    def CreatePathChooser(self):
        self.path_stack = QStackedWidget()
        self.path_stack.setStyleSheet("background: transparent; border: none;")

        initial_prompt = QWidget()
        initial_layout = QVBoxLayout()
        initial_layout.setContentsMargins(0, 0, 0, 0)
        initial_label = QLabel("Please select a UAV to choose a path")
        initial_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        initial_label.setFont(QFont("Times New Roman", 16, QFont.Weight.DemiBold))
        initial_layout.addWidget(initial_label)
        initial_prompt.setLayout(initial_layout)

        self.path_prompt = QWidget()
        path_layout = QVBoxLayout()
        path_layout.setContentsMargins(10, 10, 10, 10)

        self.prompt_label = QLabel("Select Path")
        self.prompt_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.prompt_label.setFont(QFont("Times New Roman", 16, QFont.Weight.DemiBold))
        self.prompt_label.setStyleSheet("color: black;")

        buttons = QHBoxLayout()
        buttons.setContentsMargins(0, 0, 0, 0)

        a_button = QPushButton("Path A")
        a_button.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))
        a_button.clicked.connect(lambda: self.ClickPathA())
        a_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        b_button = QPushButton("Path B")
        b_button.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))
        b_button.clicked.connect(lambda: self.ClickPathB())
        b_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        home_button = QPushButton("Home Base")
        home_button.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))
        home_button.clicked.connect(lambda: self.ClickHomeBase())
        home_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        cancel_button = QPushButton("Cancel")
        cancel_button.setFont(QFont("Times New Roman", 12, QFont.Weight.Normal))
        cancel_button.clicked.connect(lambda: self.ClickCancel())
        cancel_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        a_button.setVisible(True)
        b_button.setVisible(True)
        #home_button.setVisible(True)
        cancel_button.setVisible(True)

        buttons.addStretch()
        buttons.addWidget(a_button)
        buttons.addWidget(b_button)
        #buttons.addWidget(home_button)
        buttons.addWidget(cancel_button)
        buttons.addStretch()

        path_layout.addWidget(self.prompt_label)
        path_layout.addLayout(buttons)
        path_layout.addStretch()
        self.path_prompt.setLayout(path_layout)

        self.path_stack.addWidget(initial_prompt)
        self.path_stack.addWidget(self.path_prompt)

        wrapper = QWidget()
        wrapper.setFixedWidth(550)
        wrapper.setFixedHeight(125)
        wrapper.setStyleSheet("background-color: white;")
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(5, 5, 5, 5)
        wrapper_layout.addWidget(self.path_stack)
        wrapper.setLayout(wrapper_layout)

        proxy = QGraphicsProxyWidget()
        proxy.setWidget(wrapper)

        proxy.setPos(0, 625)

        return proxy
    
    def CreateUAVInfoWidget(self):
        widget = QWidget()
        widget.setFixedHeight(200)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.card_uav = self.CreateUAVCard()
        self.card_a = self.CreateInfoCard("Path A")
        self.card_b = self.CreateInfoCard("Path B")

        layout.addWidget(self.card_uav)
        inner = QHBoxLayout()
        inner.addWidget(self.card_a)
        inner.addWidget(self.card_b)
        layout.addLayout(inner)
        widget.setLayout(layout)
        widget.card_a = self.card_a
        widget.card_b = self.card_b

        return widget
    
    def CreateUAVCard(self):
        group = QGroupBox()
        group.setFixedHeight(60)
        layout = QHBoxLayout()

        font = QFont("Times New Roman", 18, QFont.Weight.DemiBold)
        uav_name = QLabel("UAV: ---")
        fuel = QLabel("Fuel: ---")
        target = QLabel("Target: ---")
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        uav_name.setFont(font)
        fuel.setFont(font)
        target.setFont(font)
        layout.addWidget(uav_name)
        layout.addSpacing(15)
        layout.addWidget(fuel)
        layout.addSpacing(15)
        layout.addWidget(target)

        group.setLayout(layout)
        group.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 5px; margin-top: 10px; }"
                            "QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
        
        group.uav_name = uav_name
        group.fuel = fuel
        group.target = target
        
        return group
    
    def UpdateUAVCard(self, uav):
        color = uav.color_hex

        self.card_uav.setStyleSheet(f"""
            QGroupBox {{
                border: 4px solid {color};
                border-radius: 5px;
                margin-top: 10px;
            }}
        """)

        self.card_uav.uav_name.setText(f"UAV: {uav.color_text}")
        self.card_uav.fuel.setText(f"Fuel: {int(uav.fuel)} km")
        self.card_uav.target.setText(f"Target: {uav.goal_item.idx}")

    def CreateInfoCard(self, title):
        group = QGroupBox(title)
        layout = QVBoxLayout()

        group = QGroupBox(title)
    
        title_font = QFont("Times New Roman", 14)
        title_font.setBold(True)
        group.setFont(title_font)

        font = QFont("Times New Roman", 14)

        distance = QLabel("Distance to target: ---")
        fuel = QLabel("Fuel Usage: ---")
        warnings = QLabel("Hazard Probability: ---")

        for label in (distance, fuel, warnings):
            label.setFont(font)
            layout.addWidget(label)

        group.setLayout(layout)
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid gray;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                font-family: "Times New Roman";
                font-size: 14pt;
                font-weight: bold;
            }
        """)

        group.distance = distance
        group.fuel = fuel
        group.warnings = warnings
        return group
    
    def UpdateInfoCards(self, uav: UAVItem):
        color = uav.color_hex

        self.card_a.setStyleSheet(f"""
            QGroupBox {{
                border: 4px solid {color};
                border-radius: 5px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                font-family: "Times New Roman";
                font-size: 14pt;
                font-weight: bold;
            }}
        """)
        self.card_b.setStyleSheet(f"""
            QGroupBox {{
                border: 4px solid {color};
                border-radius: 5px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                font-family: "Times New Roman";
                font-size: 14pt;
                font-weight: bold;
            }}
        """)

        self.card_a.distance.setText(f"Distance to target: {uav.hyp_length} km")

        fuel_usea = round((uav.hyp_length / uav.starting_fuel) * 100)
        self.card_a.fuel.setText(f"Fuel Usage: {fuel_usea}%")

        uav.GetStormHitChance()

        self.card_a.warnings.setText(f"Warnings: {uav.hit_chancea}%")

        self.card_b.distance.setText(f"Distance to target: {uav.ra_length} km")

        fuel_useb = round((uav.ra_length / uav.starting_fuel) * 100)
        self.card_b.fuel.setText(f"Fuel Usage: {fuel_useb}%")

        self.card_b.warnings.setText(f"Warnings: {uav.hit_chanceb}%")

    def TimerUpdateCards(self):
        if self.curr_uav:
            self.UpdateInfoCards(self.curr_uav)
            self.UpdateUAVCard(self.curr_uav)

    def ClearUAVCards(self):
        self.card_uav.setStyleSheet("""
            QGroupBox {
                border: 2px solid gray;
                border-radius: 5px;
                margin-top: 10px;
            }
        """)
        self.card_uav.uav_name.setText("UAV: ---")
        self.card_uav.fuel.setText("Fuel: ---")
        self.card_uav.target.setText("Target: ---")

        self.card_a.setStyleSheet(f"""
            QGroupBox {{
                border: 2px solid gray;
                border-radius: 5px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                font-family: "Times New Roman";
                font-size: 14pt;
                font-weight: bold;
            }}
        """)
        self.card_a.distance.setText("Distance to target: ---")
        self.card_a.fuel.setText("Fuel Usage: ---")
        self.card_a.warnings.setText("Hazard Probability: ---")

        self.card_b.setStyleSheet(f"""
            QGroupBox {{
                border: 2px solid gray;
                border-radius: 5px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                font-family: "Times New Roman";
                font-size: 14pt;
                font-weight: bold;
            }}
        """)
        self.card_b.distance.setText("Distance to target: ---")
        self.card_b.fuel.setText("Fuel Usage: ---")
        self.card_b.warnings.setText("Hazard Probability: ---")

        self.curr_uav = None
    
    def ClickCancel(self):
        self.path_stack.setCurrentIndex(0)

        for uav in UAVs:
            uav.hyp_path.setVisible(False)
            uav.hyp_label.setVisible(False)
            uav.ra_path.setVisible(False)
            uav.ra_label.setVisible(False)

        #self.ClearUAVCards()
        pass

    def ClickPathA(self):
        if not hasattr(self, "curr_uav") or self.curr_uav is None:
            return
        
        self.curr_uav.MoveToGoalA()
        self.ClickCancel()
        

    def ClickPathB(self):
        if not hasattr(self, "curr_uav") or self.curr_uav is None:
            return
        
        self.curr_uav.MoveToGoalB()
        self.ClickCancel()
        pass

    def CreateHomeBase(self):
        width = 130
        height = 30
        rect = QGraphicsRectItem(800 - width - 10 , 10, width, height)
        rect.setBrush(Qt.GlobalColor.white)
        rect.setPen(QPen(Qt.GlobalColor.black, 3))

        text = QGraphicsTextItem("Home Base")
        font = QFont("Times New Roman", 14, QFont.Weight.Bold)
        text.setFont(font)
        text.setDefaultTextColor(Qt.GlobalColor.black)

        text_rect = text.boundingRect()
        text.setPos(800 - width - 10 + (width - text_rect.width()) / 2,
                    10 + (height - text_rect.height()) / 2)
        
        rect.setZValue(2)
        text.setZValue(2)
        
        return rect, text
    
    def HandleClick(self, color_text, goal_idx):
        self.prompt_label.setText(f"Select the best path for UAV {color_text} to reach POINT {goal_idx}")
        self.path_stack.setCurrentIndex(1)

        for uav in UAVs:
            if uav.idx == goal_idx:
                self.curr_uav = uav
                break

        if self.curr_uav:
            self.UpdateInfoCards(self.curr_uav)
            self.UpdateUAVCard(self.curr_uav)
            self.card_update_timer.start()
            #self.uav_info_stack.setCurrentWidget(self.uav_info_widgets[self.curr_uav.idx])

    def StartSummary(self):
        from DataLogging.LogNavigation import NavigationCSV

        self.showSum = InstrUAV()
        NavigationCSV()
        self.showSum.show()
        self.close()   

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

def LogNav():
    # block, trial, UAVs, auto, auto_type,
    block = 1
    trial = 2
    auto = str(False)
    auto_type = "None"

    LogNavigation(block, trial, UAVs, auto, auto_type)

    pass