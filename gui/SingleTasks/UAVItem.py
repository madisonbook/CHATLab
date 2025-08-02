from PyQt6.QtWidgets import (
    QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QPlainTextEdit,
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem,
    QGraphicsTextItem, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt6.QtGui import QFont, QBrush, QPen, QColor, QPixmap, QPainter, QPolygonF, QPainterPath
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsRectItem, QStackedWidget, QGraphicsProxyWidget
import math
from .PathGoals import GoalItem, PathItem
import random
import singleTaskInput

class UAVItem():
    def __init__(self, idx, color_hex, color_text, x_pos, y_pos, curr_goal: GoalItem, goal_items, fuel, speed,
                 angle, on_click_callback, scene):
        
        pts = [QPointF(0, -25), QPointF(-25, 25), QPointF(25, 25)]
        triangle = QPolygonF(pts)

        self.scene = scene
        self.uav_item = ClickableUAV(triangle, color_hex, self.OnClick)
        self.uav_item.setPos(x_pos, y_pos)
        self.uav_item.setRotation(self.GetAngle(x_pos, y_pos, curr_goal.pos_x, curr_goal.pos_y))

        self.curr_pos = QPointF(x_pos, y_pos)
        #self.is_moving = False
        self.timer = None
        self.color_hex = color_hex
        self.idx = idx
        self.color_text = color_text
        self.angle = angle
        self.fuel = fuel
        self.speed = speed
        self.goal_item = curr_goal
        self.goal_items = goal_items
        path = PathItem(color_hex, x_pos, y_pos, curr_goal.pos_x, curr_goal.pos_y, angle)
        self.hyp_path = path.hyp
        self.hyp_label = path.hyp_label
        self.hyp_length = path.hyp_length
        self.ra_path = path.ra
        self.ra_label = path.ra_label
        self.ra_midpoint = path.ra_midpoint
        self.ra_length = path.ra_length

        self.idle_timer = QTimer()
        self.idle_timer.setInterval(1000) 
        self.idle_time = 0
        self.last_pos = QPointF(x_pos, y_pos)
        self.idle_timer.timeout.connect(self.CheckIdle)
        self.idle_timer.start()
        self.is_idle = False
        self.on_path = "NA"

        self.on_click_callback = on_click_callback

    def GetAngle(self, x_pos, y_pos, x_goal, y_goal):
        dx = x_goal - x_pos
        dy = y_goal - y_pos
        return math.degrees(math.atan2(dy, dx)) + 90
    
    def GetNewGoal(self):
        new_goals = [goal for goal in self.goal_items if goal != self.goal_item]
        new_goal = random.choice(new_goals)
        self.goal_item = new_goal
        self.uav_item.setRotation(self.GetAngle(self.curr_pos.x(), self.curr_pos.y(), new_goal.pos_x, new_goal.pos_y))
        pass

    def GetNewPath(self):
        angle = random.randint(100, 165)

        if self.hyp_path.scene():
            self.scene.removeItem(self.hyp_path)
        if self.hyp_label.scene():
            self.scene.removeItem(self.hyp_label)
        if self.ra_path.scene():
            self.scene.removeItem(self.ra_path)
        if self.ra_label.scene():
            self.scene.removeItem(self.ra_label)

        path = PathItem(self.color_hex, self.curr_pos.x(), self.curr_pos.y(), self.goal_item.pos_x, self.goal_item.pos_y, angle)
        self.hyp_path = path.hyp
        self.hyp_label = path.hyp_label
        self.hyp_length = path.hyp_length
        self.ra_path = path.ra
        self.ra_label = path.ra_label
        self.ra_midpoint = path.ra_midpoint
        self.ra_length = path.ra_length

        self.hyp_path.setZValue(0)
        self.hyp_label.setZValue(1)
        self.ra_path.setZValue(0)
        self.ra_label.setZValue(1)

        self.scene.addItem(self.hyp_path)
        self.scene.addItem(self.hyp_label)
        self.scene.addItem(self.ra_path)
        self.scene.addItem(self.ra_label)

        self.hyp_path.setVisible(False)
        self.hyp_label.setVisible(False)
        self.ra_path.setVisible(False)
        self.ra_label.setVisible(False)
        pass
    
    def OnClick(self):
        self.hyp_path.setVisible(True)
        self.hyp_label.setVisible(True)
        self.ra_path.setVisible(True)
        self.ra_label.setVisible(True)

        if self.on_click_callback:
            self.on_click_callback(self.color_text, self.idx)
        pass

    def MoveToHomeBase(self):
        start_pos = self.uav_item.pos()
        mid_pos = QPointF(730, 30)
        goal_rect = self.goal_item.rect()
        goal_pos = self.goal_item.pos() + QPointF(goal_rect.width() / 2, goal_rect.height() / 2)

        self.animation_steps = 100
        self.current_step = 0

        dx1 = (mid_pos.x() - start_pos.x()) / self.animation_steps
        dy1 = (mid_pos.y() - start_pos.y()) / self.animation_steps

        dx2 = (start_pos.x() - mid_pos.x()) / self.animation_steps
        dy2 = (start_pos.y() - mid_pos.y()) / self.animation_steps

        self.uav_item.setRotation(self.GetAngle(start_pos.x(), start_pos.y(), mid_pos.x(), mid_pos.y()))

        def AnimateP1():
            if self.current_step >= self.animation_steps:
                self.timer.stop()
                self.timer.timeout.disconnect()
                self.current_step = 0
                self.fuel = 1500

                def delayed_start():
                    self.uav_item.setRotation(self.GetAngle(mid_pos.x(), mid_pos.y(), start_pos.x(), start_pos.y()))
                    self.timer.timeout.connect(AnimateP2)
                    self.timer.start(self.speed * 5)

                QTimer.singleShot(2000, delayed_start)
                return
            
            if self.fuel > 0:
                new_x = start_pos.x() + dx1 * self.current_step
                new_y = start_pos.y() + dy1 * self.current_step

                self.uav_item.setPos(QPointF(new_x, new_y))
                self.curr_pos = QPointF(new_x, new_y)

                if self.current_step > 0 and self.fuel > 0:
                    self.fuel -= math.hypot(dx1, dy1)
                    if self.fuel < 0:
                        self.fuel = 0
                
                self.current_step += 1

        def AnimateP2():
            if self.current_step >= self.animation_steps:
                self.timer.stop()
                self.uav_item.setRotation(self.GetAngle(start_pos.x(), start_pos.y(), goal_pos.x(), goal_pos.y()))
                self.uav_item.setPos(start_pos.x(), start_pos.y())
                self.curr_pos = start_pos
                self.on_path = "NA"
                self.uav_item.is_moving = False
                return
            
            new_x = mid_pos.x() + dx2 * self.current_step
            new_y = mid_pos.y() + dy2 * self.current_step
            self.uav_item.setPos(QPointF(new_x, new_y))
            self.curr_pos = QPointF(new_x, new_y)

            if self.current_step > 0:
                self.fuel -= math.hypot(dx2, dy2)
                
            self.current_step += 1

        self.timer = QTimer()
        self.uav_item.is_moving = True
        self.on_path = "HB"
        self.is_idle = False
        self.idle_time = 0
        self.LogAction()
        self.timer.timeout.connect(AnimateP1)
        self.timer.start(self.speed*5)  

    def MoveToGoalA(self):
        start_pos = self.uav_item.pos()
        goal_rect = self.goal_item.rect()
        goal_pos = self.goal_item.pos() + QPointF(goal_rect.width() / 2, goal_rect.height() / 2)

        self.animation_steps = 100
        self.current_step = 0

        dx = (goal_pos.x() - start_pos.x()) / self.animation_steps
        dy = (goal_pos.y() - start_pos.y()) / self.animation_steps

        def Animate():
            if self.current_step >= self.animation_steps:
                self.timer.stop()
                self.uav_item.setPos(goal_pos)
                self.curr_pos = goal_pos
                self.uav_item.is_moving = False
                self.on_path = "NA"
                self.GetNewGoal()
                self.GetNewPath()
                return
            
            if self.fuel > 0:
                new_x = start_pos.x() + dx * self.current_step
                new_y = start_pos.y() + dy * self.current_step

                self.uav_item.setPos(QPointF(new_x, new_y))
                self.curr_pos = QPointF(new_x, new_y)

                if self.current_step > 0:
                    self.fuel -= math.hypot(dx, dy)
                    if self.fuel < 0:
                        self.fuel = 0

                self.current_step += 1

        self.timer = QTimer()
        self.uav_item.is_moving = True
        self.is_idle = False
        self.idle_time = 0
        self.on_path = "A"
        self.LogAction()
        self.timer.timeout.connect(Animate)
        self.timer.start(self.speed*10)

    def MoveToGoalB(self):
        self.animation_steps = 100
        self.current_step = 0

        self.start = self.uav_item.pos()
        self.end = self.goal_item.pos() + QPointF(
            self.goal_item.rect().width() / 2,
            self.goal_item.rect().height() / 2
        )

        mid_pos = QPointF(self.ra_midpoint)
        
        self.uav_item.setRotation(self.GetAngle(self.start.x(), self.start.y(), mid_pos.x(), mid_pos.y()))

        dx1 = (mid_pos.x() - self.start.x()) / self.animation_steps
        dy1 = (mid_pos.y() - self.start.y()) / self.animation_steps

        dx2 = (self.end.x() - mid_pos.x()) / self.animation_steps
        dy2 = (self.end.y() - mid_pos.y()) / self.animation_steps

        def AnimateP1():
            if self.current_step >= self.animation_steps:
                self.timer.timeout.disconnect()
                self.current_step = 0
                self.uav_item.setRotation(self.GetAngle(mid_pos.x(), mid_pos.y(), self.end.x(), self.end.y()))
                self.timer.timeout.connect(AnimateP2)
                return
            
            if self.fuel > 0:
                new_x = self.start.x() + dx1 * self.current_step
                new_y = self.start.y() + dy1 * self.current_step

                self.uav_item.setPos(QPointF(new_x, new_y))
                self.curr_pos = QPointF(new_x, new_y)

                if self.current_step > 0:
                    self.fuel -= math.hypot(dx1, dy1)
                    if self.fuel < 0:
                        self.fuel = 0
                    
                self.current_step += 1

        def AnimateP2():
            if self.current_step >= self.animation_steps:
                self.timer.stop()
                self.uav_item.is_moving = False
                self.on_path = "NA"
                self.GetNewGoal()
                self.GetNewPath()
                return
            
            if self.fuel > 0:

                new_x = mid_pos.x() + dx2 * self.current_step
                new_y = mid_pos.y() + dy2 * self.current_step

                self.uav_item.setPos(QPointF(new_x, new_y))
                self.curr_pos = QPointF(new_x, new_y)

                if self.current_step > 0:
                    self.fuel -= math.hypot(dx2, dy2)
                    if self.fuel < 0:
                        self.fuel = 0                  
                    
                self.current_step += 1

        self.timer = QTimer()
        self.uav_item.is_moving = True
        self.idle_time = 0
        self.on_path = "B"
        self.is_idle = False
        self.LogAction()
        self.timer.timeout.connect(AnimateP1)
        self.timer.start(self.speed*5)

    def CheckIdle(self):
        if not self.is_idle or self.fuel == 0:

            if not self.uav_item.is_moving or self.fuel == 0:
                self.idle_time += 1

            else:
                self.idle_time = 0

            if self.idle_time >= 10:
                self.is_idle = True
                self.LogAction()

    def LogAction(self):
        from .UAVNavigation import LogNav
        LogNav()
        pass
    
class ClickableUAV(QGraphicsPolygonItem):
    def __init__(self, polygon, color, on_click_callback):
        super().__init__(polygon)
        self.setBrush(QBrush(QColor(color)))
        self.setPen(QPen(Qt.GlobalColor.black, 3))
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.on_click_callback = on_click_callback
        self.is_moving = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.is_moving:
            self.on_click_callback()
        event.accept()