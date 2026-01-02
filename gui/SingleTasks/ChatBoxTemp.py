from PyQt6.QtWidgets import (
    QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QScrollArea,
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QTextEdit, QLineEdit,
    QGraphicsTextItem, QGroupBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt6.QtGui import QFont, QBrush, QPen, QColor, QPixmap, QPainter, QPolygonF, QPainterPath
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsRectItem, QStackedWidget, QGraphicsProxyWidget
import math
from PracticeTrials.PracUAVItem import UAVItem
from .NavItems import GoalItem, StormItem
from participant import PARTICIPANT_ID
from ReadInput import singleTaskInput
from DataLogging.LogChatBox import LogChatBox, ChatBoxCSV
from SingleTaskSummaries.SumChat import SumChat
import random
import datetime

base_width = 115
base_height = 250
border_thickness = 4

summary = []
gauges = []
UAVs = []
total_path = 0
total_correct = 0

img_size = 800

chat_box = ["N/A", "N/A"]
msg_time = None
answer = None

class ChatBox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Use in Multitasking Contexts")
        self.curr_uav = None
        self.card_update_timer = QTimer()
        self.card_update_timer.setInterval(1000)  # 1000 ms = 1 second
        #self.card_update_timer.timeout.connect(self.TimerUpdateCards)

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        title = Title("Task: Chat Box")
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

        storm_items = [StormItem(1, singleTaskInput.nav_storm_x[0], singleTaskInput.nav_storm_y[0]),
                      StormItem(2, singleTaskInput.nav_storm_x[1], singleTaskInput.nav_storm_y[1]),
                      StormItem(3, singleTaskInput.nav_storm_x[2], singleTaskInput.nav_storm_y[2]),
                      StormItem(4, singleTaskInput.nav_storm_x[3], singleTaskInput.nav_storm_y[3])]

        for item in storm_items:
            left_nav.addItem(item.pixmap_item)

        goal_items = [GoalItem(1, singleTaskInput.nav_goal_x[0], singleTaskInput.nav_goal_y[0]),
                      GoalItem(2, singleTaskInput.nav_goal_x[1], singleTaskInput.nav_goal_y[1]),
                      GoalItem(3, singleTaskInput.nav_goal_x[2], singleTaskInput.nav_goal_y[2]),
                      GoalItem(4, singleTaskInput.nav_goal_x[3], singleTaskInput.nav_goal_y[3])]
        
        #(self, idx, color_hex, color_text, x_pos, y_pos, curr_goal, goals_list, fuel, speed, angle, on_click_callback):
        uav_blue = UAVItem(1, "#90D5FF", "BLUE", singleTaskInput.nav_uav_x[0], singleTaskInput.nav_uav_y[0],
                           goal_items[0], goal_items, storm_items, singleTaskInput.nav_uav_fuel[0], 
                           singleTaskInput.nav_uav_speed[0], singleTaskInput.nav_path_angle[0], self.HandleClick, left_nav)
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
   
        uav_red = UAVItem(2, "#FF7F7F", "RED", singleTaskInput.nav_uav_x[1], singleTaskInput.nav_uav_y[1],
                          goal_items[1], goal_items, storm_items, singleTaskInput.nav_uav_fuel[1], 
                           singleTaskInput.nav_uav_speed[1], singleTaskInput.nav_path_angle[1], self.HandleClick, left_nav)
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

        uav_green = UAVItem(3, "#88E788", "GREEN", singleTaskInput.nav_uav_x[2], singleTaskInput.nav_uav_y[2],
                           goal_items[2], goal_items, storm_items, singleTaskInput.nav_uav_fuel[2], 
                           singleTaskInput.nav_uav_speed[2], singleTaskInput.nav_path_angle[2], self.HandleClick, left_nav)
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

        uav_yellow = UAVItem(4, "#FFEE8c", "YELLOW", singleTaskInput.nav_uav_x[3], singleTaskInput.nav_uav_y[3], 
                           goal_items[3], goal_items, storm_items, singleTaskInput.nav_uav_fuel[3], 
                           singleTaskInput.nav_uav_speed[3], singleTaskInput.nav_path_angle[3], self.HandleClick, left_nav)
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

        # Create right content with fixed sizes
        right_content = QVBoxLayout()
        
        # Fixed-size UAV info section
        self.uav_info_stack = QStackedWidget()
        self.uav_info_widget = self.CreateUAVInfoWidget()
        self.uav_info_stack.addWidget(self.uav_info_widget)
        self.uav_info_stack.setCurrentWidget(self.uav_info_widget)
        self.uav_info_stack.setFixedHeight(200)
        self.uav_info_stack.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        # Fixed-size chat box
        items_on_screen = ["UAV BLUE", "UAV GREEN", "UAV RED", "UAV YELLOW", "GAUGE RED", "GAUGE YELLOW", "GAUGE GREEN", "GAUGE BLUE"]
        self.chat_box = ChatWidget(context_items=items_on_screen)
        self.chat_box.setFixedHeight(140)
        self.chat_box.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        # Fixed-size gauges section
        monitor_levels = QHBoxLayout()
        monitor_levels.addStretch()

        colors = ["#FF7F7F", "#FFEE8c", "#88E788", "#90D5FF"]
        color_text = ["RED", "YELLOW", "GREEN", "BLUE"]
        idx = 0
        for color in colors:
            gauge = GenerateLevel(color, idx, color_text[idx])
            idx = idx + 1

            global gauges
            gauges.append(gauge)

            monitor_levels.addLayout(gauge.form)
            monitor_levels.addSpacing(5)

        monitor_levels.addStretch()
        
        # Create a widget for gauges with fixed height
        gauges_widget = QWidget()
        gauges_widget.setLayout(monitor_levels)
        gauges_widget.setFixedHeight(360)  # Slightly larger than gauge height + button
        gauges_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        # Add all components with fixed sizes
        right_content.addWidget(gauges_widget)
        right_content.addWidget(self.uav_info_stack)
        right_content.addWidget(self.chat_box)
        right_content.addStretch()
        right_content.addStretch()
    
        game_form.addLayout(right_content)

        main_layout.addLayout(game_form)

        main_layout.addStretch()
        self.showMaximized()

        QTimer.singleShot(singleTaskInput.chat_duration*1000, lambda: self.StartSummary())

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
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        widget.setFixedHeight(200)  # Set fixed height
        layout = QVBoxLayout()

        self.card_uav = self.CreateUAVCard()
        self.card_a = self.CreateInfoCard("Path A")
        self.card_b = self.CreateInfoCard("Path B")

        layout.addWidget(self.card_uav)
        inner = QHBoxLayout()
        inner.addWidget(self.card_a)
        inner.addWidget(self.card_b)
        layout.addLayout(inner)
        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        widget.card_a = self.card_a
        widget.card_b = self.card_b

        return widget
    
    def CreateUAVCard(self):
        group = QGroupBox()
        group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        group.setFixedHeight(60)  # Set fixed height for UAV card
        layout = QHBoxLayout()

        font = QFont("Times New Roman", 18, QFont.Weight.DemiBold)
        # Use fixed-width text to prevent layout shifts
        uav_name = QLabel("UAV: -------")  # Longer placeholder
        fuel = QLabel("Fuel: ----- km")    # Include units in placeholder
        target = QLabel("Target: -")        # Single digit placeholder
        
        uav_name.setFont(font)
        fuel.setFont(font)
        target.setFont(font)
        
        # Set minimum widths to prevent layout shifts
        uav_name.setMinimumWidth(150)
        fuel.setMinimumWidth(130)
        target.setMinimumWidth(80)
        
        layout.addWidget(uav_name)
        layout.addSpacing(15)
        layout.addWidget(fuel)
        layout.addSpacing(15)
        layout.addWidget(target)

        group.setLayout(layout)
        group._base_stylesheet = """
            QGroupBox {{
                border: 3px solid {color};
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
        """

        group.setStyleSheet(group._base_stylesheet.format(color="gray"))
        
        group.uav_name = uav_name
        group.fuel = fuel
        group.target = target
        
        return group
    
    def UpdateUAVCard(self, uav):
        color = uav.color_hex

        self.card_uav.setStyleSheet(self.card_uav._base_stylesheet.format(color=color))

        self.card_uav.uav_name.setText(f"UAV: {uav.color_text}")
        self.card_uav.fuel.setText(f"Fuel: {int(uav.fuel)} km")
        self.card_uav.target.setText(f"Target: {uav.goal_item.idx}")

    def CreateInfoCard(self, title):
        layout = QVBoxLayout()

        group = QGroupBox(title)
        group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        group.setFixedHeight(120)  # Set fixed height for info cards
    
        title_font = QFont("Times New Roman", 14)
        title_font.setBold(True)
        group.setFont(title_font)

        font = QFont("Times New Roman", 14)

        # Use longer placeholders with consistent formatting
        distance = QLabel("Distance to target: ----- km")
        fuel = QLabel("Fuel Usage: ---%")
        warnings = QLabel("Hazard Probability: ---%")

        for label in (distance, fuel, warnings):
            label.setFont(font)
            label.setMinimumWidth(200)  # Set minimum width
            layout.addWidget(label)

        group.setLayout(layout)

        group._base_stylesheet = """
            QGroupBox {{
                border: 3px solid {color};
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
        """
        group.setStyleSheet(group._base_stylesheet.format(color="gray"))

        group.distance = distance
        group.fuel = fuel
        group.warnings = warnings
       
        return group
    
    def UpdateInfoCards(self, uav: UAVItem):
        color = uav.color_hex

        self.card_a.setStyleSheet(self.card_a._base_stylesheet.format(color=color))
        self.card_b.setStyleSheet(self.card_b._base_stylesheet.format(color=color))

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
        self.card_uav.setStyleSheet(self.card_uav._base_stylesheet.format(color="gray"))
        self.card_uav.uav_name.setText("UAV: -------")
        self.card_uav.fuel.setText("Fuel: ----- km")
        self.card_uav.target.setText("Target: -")

        self.card_a.setStyleSheet(self.card_a._base_stylesheet.format(color="gray"))
        self.card_a.distance.setText("Distance to target: ----- km")
        self.card_a.fuel.setText("Fuel Usage: ---%")
        self.card_a.warnings.setText("Hazard Probability: ---%")
        
        self.card_b.setStyleSheet(self.card_b._base_stylesheet.format(color="gray"))
        self.card_b.distance.setText("Distance to target: ----- km")
        self.card_b.fuel.setText("Fuel Usage: ---%")
        self.card_b.warnings.setText("Hazard Probability: ---%")

        self.curr_uav = None
    
    def ClickCancel(self):
        self.path_stack.setCurrentIndex(0)

        for uav in UAVs:
            uav.hyp_path.setVisible(False)
            uav.hyp_label.setVisible(False)
            uav.ra_path.setVisible(False)
            uav.ra_label.setVisible(False)

        self.ClearUAVCards()
        pass

    def ClickPathA(self):
        if not hasattr(self, "curr_uav") or self.curr_uav is None:
            return
        
        #self.curr_uav.MoveToGoalA()
        self.ClickCancel()
        

    def ClickPathB(self):
        if not hasattr(self, "curr_uav") or self.curr_uav is None:
            return
        
        #self.curr_uav.MoveToGoalB()
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
            #self.card_update_timer.start()
            #self.uav_info_stack.setCurrentWidget(self.uav_info_widgets[self.curr_uav.idx])

    def StartSummary(self):
        from DataLogging.LogNavigation import NavigationCSV

        summary = [total_correct, total_path]
        self.showSum = SumChat(summary)
        ChatBoxCSV()
        self.showSum.show()
        self.close()   

class GenerateLevel(QWidget):
    def __init__(self, color_hex: str, idx: int, color_text: str):
        super().__init__()

        self.oob = False
        self.reset = False
        height = max(10, min(240, int(random.normalvariate(singleTaskInput.gauge_mean[idx], singleTaskInput.gauge_sd[idx]))))
        #self.monitor_level = random.randint(singleTaskInput.gauge_mean[idx] - singleTaskInput.gauge_sd[idx], singleTaskInput.gauge_mean[idx] + singleTaskInput.gauge_sd[idx])
        self.monitor_level = height
        self.oob_time = None
        self.setFixedHeight(350)
        self.color_text = color_text

        #self.animation_timer = QTimer(self)
        #self.animation_timer.timeout.connect(lambda: self.Animate())
        #self.animation_duration = 500
        #self.animation_interval = 16
        self.animation_start_time = None
        self.animation_start_height = self.monitor_level
        self.animation_end_height = self.monitor_level

        #self.timer = QTimer(self)
        #self.timer.timeout.connect(lambda: self.ChangeHeight(idx))
    
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

        #self.TimerDelay()

    def ResetLevel(self, idx:int):
        
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
            #LogGauges()

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

class ChatWidget(QWidget):
    def __init__(self, context_items):
        super().__init__()
        
        # Set fixed size for the chat widget
        self.setFixedHeight(130)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        main_layout = QHBoxLayout(self)
        self.context_items = context_items
        self.setLayout(main_layout)

        left_group = QGroupBox("Chat Box")
        left_group.setFixedHeight(130)
        left_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        left_layout = QVBoxLayout(left_group)

        self.latest_message = QLabel("Waiting...")
        self.latest_message.setWordWrap(True)
        self.latest_message.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.latest_message.setFont(QFont("Times New Roman", 14))
        self.latest_message.setFixedHeight(90) 
        left_layout.addWidget(self.latest_message)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type a message...")
        self.input_box.setFont(QFont("Times New Roman", 14))
        self.input_box.setFixedHeight(30) 
        left_layout.addWidget(self.input_box)

        left_group.setLayout(left_layout)

        left_group.setStyleSheet(f"""
            QGroupBox {{
                border: 3px solid gray;
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

        title_font = QFont("Times New Roman", 14)
        title_font.setBold(True)
        left_group.setFont(title_font)

        right_group = QGroupBox("Message History")
        right_group.setFixedHeight(130)
        right_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        right_layout = QVBoxLayout(right_group)
        
        self.history_scroll = QScrollArea()
        self.history_scroll.setWidgetResizable(True)
        self.history_scroll.setFixedHeight(100)

        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout(self.history_widget)
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.history_scroll.setWidget(self.history_widget)

        right_layout.addWidget(self.history_scroll)
        right_group.setLayout(right_layout)

        right_group.setStyleSheet(f"""
            QGroupBox {{
                border: 3px solid gray;
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

        title_font = QFont("Times New Roman", 14)
        title_font.setBold(True)
        right_group.setFont(title_font)

        main_layout.addWidget(left_group, 2)
        main_layout.addWidget(right_group, 3)
        
        self.input_box.returnPressed.connect(self.handle_user_message)

        self.gauge_templates = [
            "Is {item} within the bounds?",
            "Is {item} above the bounds?",
            "Is {item} below the bounds?"
        ]

        self.uav_templates = [
            "What is the fuel level of {item}?",
            "What is the current goal of {item}?",
            "What is the length of Path A for {item}?",
            "What is the length of Path B for {item}?"
        ]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_random_message)

        #delay = random.randint(singleTaskInput.chat_timer[0]*1000, singleTaskInput.chat_timer[1]*1000)
        self.timer.start(2000)

    def handle_user_message(self):
        text = self.input_box.text().strip()
        if text:
            chat_box[1] = text

            global answer 
            answer = self.compute_answer()
            LogChat()
            self.input_box.clear()
            self.latest_message.setText("Waiting...")

    def compute_answer(self):

        if len(chat_box) < 1 or chat_box[0] == "N/A":
            return None

        question = chat_box[0]
        correct_answer = None

        if "BLUE" in question:
            color = "BLUE"
        elif "RED" in question:
            color = "RED"
        elif "YELLOW" in question:
            color = "YELLOW"
        elif "GREEN" in question:
            color = "GREEN"

        # --- Gauge questions ---
        if "GAUGE" in question:
            gauge = next((g for g in gauges if getattr(g, "color_text", "") == color), None)
            idx = {"RED": 0, "YELLOW": 1, "GREEN": 2, "BLUE": 3}.get(color)
            if gauge:
                mean, dist = singleTaskInput.gauge_mean[idx], singleTaskInput.gauge_dist[idx]
                low, high = mean - dist, mean + dist
                curr_level = getattr(gauge, "monitor_level", 0)
                q = question.lower()
                if "within" in q:
                    correct_answer = "Yes" if low <= curr_level <= high else "No"
                elif "above" in q:
                    correct_answer = "Yes" if curr_level > high else "No"
                elif "below" in q:
                    correct_answer = "Yes" if curr_level < low else "No"


        # --- UAV questions ---
        elif "UAV" in question:
            uav = next((u for u in UAVs if getattr(u, "color_text", "").upper() == color), None)
            if uav:
                q = question.lower()
                if "fuel" in q:
                    val = round(getattr(uav, "fuel", getattr(uav, "starting_fuel", 0)))
                    correct_answer = f"{val} km"
                elif "goal" in q:
                    goal = getattr(uav.goal_item, "idx", None)
                    correct_answer = f"TARGET {goal}" if goal is not None else "Unknown"
                elif "path a" in q:
                    val = round(getattr(uav, "hyp_length", 0))
                    correct_answer = f"{val} km"
                elif "path b" in q:
                    val = round(getattr(uav, "ra_length", 0))
                    correct_answer = f"{val} km"

        return correct_answer

    def add_random_message(self):
        
        self.item = random.choice(self.context_items)

        if "GAUGE" in self.item:
            template = random.choice(self.gauge_templates)

        if "UAV" in self.item:
            template = random.choice(self.uav_templates)

        msg = template.format(item=self.item)

        self.latest_message.setText(f"{msg}")
        chat_box[0] = msg
        chat_box[1] = "N/A"

        self.add_message_card(self.item)

        global msg_time, answer
        msg_time = datetime.datetime.now()
        answer = None

        LogChat()

        delay = random.randint(singleTaskInput.chat_timer[0]*1000,
                           singleTaskInput.chat_timer[1]*1000)
        self.timer.start(delay)

    def add_message_card(self, item: str):
        card = QGroupBox("")
        card.setFixedHeight(40)
        layout = QVBoxLayout()

        label = QLabel(item)
        label.setFont(QFont("Times New Roman", 12))
        label.setWordWrap(True)
        layout.addWidget(label)

        card.setLayout(layout)
        card.setStyleSheet("""
            QGroupBox {
                border: 2px solid gray;
                border-radius: 5px;
                margin-top: 5px;
                font-family: "Times New Roman";
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 5px;
                padding: 0 3px;
                font-size: 10pt;
                font-weight: bold;
            }
        """)

        self.history_layout.addWidget(card)

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

def LogChat():
    block = 1
    trial = 3
    auto = str(False)
    auto_type = "None"

    LogChatBox(block, trial, chat_box, answer, msg_time, auto, auto_type)
    pass