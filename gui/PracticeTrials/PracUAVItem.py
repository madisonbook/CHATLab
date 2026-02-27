from PyQt6.QtWidgets import (
    QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QPlainTextEdit,
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem,
    QGraphicsTextItem, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QFont, QBrush, QPen, QColor, QPixmap, QPainter, QPolygonF, QVector2D
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsRectItem, QStackedWidget, QGraphicsProxyWidget
import math
from SingleTasks.NavItems import GoalItem, PathItem
import random

class UAVItem():
    def __init__(self, idx, color_hex, color_text, x_pos, y_pos, curr_goal: GoalItem, goal_items, storm_items, fuel, speed,
                 angle, on_click_callback, scene):
        
        pts = [QPointF(0, -25), QPointF(-25, 25), QPointF(25, 25)]
        triangle = QPolygonF(pts)

        self.scene = scene
        self.uav_item = ClickableUAV(triangle, color_hex, self.OnClick)
        self.uav_item.setPos(x_pos, y_pos)
        self.uav_item.setRotation(self.GetAngle(x_pos, y_pos, curr_goal.pos_x, curr_goal.pos_y))

        self.curr_pos = QPointF(x_pos, y_pos)
        self.idx = idx
        self.at_goal = False
        self.speed = speed
        self.timer = None
        self.color_hex = color_hex
        self.color_text = color_text
        self.angle = angle
        self.fuel = fuel
        self.starting_fuel = fuel
        self.score = 0
        self.goal_item = curr_goal
        self.goal_items = goal_items
        self.total_goal_reached = 0
        self.storm_items = storm_items
        self.storm_hit = False
        path = PathItem(color_hex, x_pos, y_pos, curr_goal.pos_x, curr_goal.pos_y, angle)
        self.hyp_path = path.hyp
        self.hyp_label = path.hyp_label
        self.hyp_midpoint = path.hyp_midpoint
        self.hyp_length = path.hyp_length
        self.ra_path = path.ra
        self.ra_label = path.ra_label
        self.ra_midpoint = path.ra_midpoint
        self.ra_length = path.ra_length

        self.GetStormHitChance()

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
        self.starting_fuel = self.fuel
        self.storm_hit = False

        fuel_buffer = 150
        hb_x, hb_y = 730, 30
        dist_to_HB = math.hypot(self.curr_pos.x() - hb_x, self.curr_pos.y() - hb_y)
        self.at_goal = False

        if self.fuel < (dist_to_HB + fuel_buffer):
            self.goal_item = GoalItem("HB", hb_x, hb_y)
            self.uav_item.setRotation(
                self.GetAngle(self.curr_pos.x(), self.curr_pos.y(), self.goal_item.pos_x, self.goal_item.pos_y)
            )
            return

        reachable_goals = []
        for goal in self.goal_items:
            if goal == self.goal_item:
                continue
            dist_to_goal = math.hypot(self.curr_pos.x() - goal.pos_x, self.curr_pos.y() - goal.pos_y)
            dist_goal_to_HB = math.hypot(goal.pos_x - hb_x, goal.pos_y - hb_y)

            if self.fuel >= (dist_to_goal + dist_goal_to_HB + fuel_buffer):
                reachable_goals.append(goal)

        if reachable_goals:
            new_goal = random.choice(reachable_goals)
            self.goal_item = new_goal
            self.uav_item.setRotation(
                self.GetAngle(self.curr_pos.x(), self.curr_pos.y(), new_goal.pos_x, new_goal.pos_y)
            )
        else:
            self.goal_item = GoalItem("HB", hb_x, hb_y)
            self.uav_item.setRotation(
                self.GetAngle(self.curr_pos.x(), self.curr_pos.y(), self.goal_item.pos_x, self.goal_item.pos_y)
            )

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
        self.hyp_midpoint = path.hyp_midpoint
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

        self.GetStormHitChance()

        pass

    def GetStormHitChance(self):     
        def linear_hit_chance(dist, max_dist, min_dist):
            if dist <= min_dist:
                return 95
            elif dist >= max_dist:
                return 0
            else:
                t = (dist - min_dist) / (max_dist - min_dist)
                scaled = (1 - t) ** 5
                #scaled = 1 - (dist - min_dist) / (max_dist - min_dist)
                return round(scaled * 100)

        min_d1 = float('inf')
        min_d2 = float('inf')

        for storm in self.storm_items:
            storm_pos = QPointF(storm.pos_x, storm.pos_y)

            d1 = QVector2D(storm_pos - self.hyp_midpoint).length()
            if d1 < min_d1:
                min_d1 = d1
                self.storm_a = storm.idx

            d2 = QVector2D(storm_pos - self.ra_midpoint).length()
            if d2 < min_d2:
                min_d2 = d2
                self.storm_b = storm.idx

        max_dist = 300
        min_dist = 50

        self.hit_chancea = linear_hit_chance(min_d1, max_dist, min_dist)
        self.hit_chanceb = linear_hit_chance(min_d2, max_dist, min_dist)

        #print(f"Min Distance to Path A: {min_d1}, Hit Chance A: {self.hit_chancea}%")
        #print(f"Min Distance to Path B: {min_d2}, Hit Chance B: {self.hit_chanceb}%")

    def PauseForStorm(self):
        if self.timer and self.timer.isActive():
            self.timer.stop()
            self.uav_item.is_moving = False
            #self.LogAction("UAV Hit Storm")
            QTimer.singleShot(2000, self.ResumeAfterStorm)

    def ResumeAfterStorm(self):
        if self.timer:
            self.timer.start(32)
            self.uav_item.is_moving = True
            #self.storm_hit = False
            self.fuel = self.fuel - 50

    def OnClick(self):
        self.hyp_path.setVisible(True)
        self.hyp_label.setVisible(True)
        self.ra_path.setVisible(True)
        self.ra_label.setVisible(True)

        if self.on_click_callback:
            self.on_click_callback(self.color_text, self.idx)
        pass 

    def MoveToGoalA(self):
        start_pos = self.uav_item.pos()
        goal_rect = self.goal_item.rect()
        goal_pos = self.goal_item.pos() + QPointF(goal_rect.width() / 2, goal_rect.height() / 2)

        self.current_step = 0

        total_dx = goal_pos.x() - start_pos.x()
        total_dy = goal_pos.y() - start_pos.y()
        total_distance = math.hypot(total_dx, total_dy)

        unit_dx = total_dx / total_distance
        unit_dy = total_dy / total_distance

        dx = unit_dx * self.speed
        dy = unit_dy * self.speed

        closest_storm = self.storm_items[self.storm_a - 1]

        def Animate(): 
            if self.fuel > 0:
                new_x = self.curr_pos.x() + dx
                new_y = self.curr_pos.y() + dy
                new_pos = QPointF(new_x, new_y)

                if self.storm_hit and math.hypot(self.hyp_midpoint.x() - new_x, self.hyp_midpoint.y() - new_y) <= self.speed:
                    self.PauseForStorm()

                if math.hypot(goal_pos.x() - new_x, goal_pos.y() - new_y) <= self.speed:
                    self.timer.stop()
                    self.uav_item.setPos(goal_pos)
                    self.curr_pos = goal_pos
                    self.uav_item.is_moving = False
                    self.on_path = "NA"
                    if self.goal_item.idx == "HB":
                        self.fuel = 2000
                        
                    self.at_goal = True
                    self.storm_hit = False
                    self.total_goal_reached += 1
                    self.score = 10 if not self.storm_hit else 5
                    #self.LogAction("UAV at Goal")
                    self.GetNewGoal()
                    self.GetNewPath()
                    self.score = 0
                    return

                self.uav_item.setPos(new_pos)
                self.curr_pos = new_pos
                self.fuel -= math.hypot(dx, dy)
                if self.fuel < 0:
                    self.fuel = 0

        self.timer = QTimer()
        self.uav_item.is_moving = True
        self.is_idle = False
        self.idle_time = 0
        self.on_path = "A"
        if random.randint(1, 101) < self.hit_chancea:
            closest_storm.AnimateToPoint(self.hyp_midpoint)
            self.storm_hit = True

        #self.LogAction("UAV Path A")
        self.timer.timeout.connect(Animate)
        self.timer.start(32)

        

    def MoveToGoalB(self):
        self.current_step = 0

        start_pos = self.uav_item.pos()
        goal_rect = self.goal_item.rect()
        goal_pos = self.goal_item.pos() + QPointF(goal_rect.width() / 2, goal_rect.height() / 2)
        mid_pos = QPointF(self.ra_midpoint)

        self.uav_item.setRotation(self.GetAngle(start_pos.x(), start_pos.y(), mid_pos.x(), mid_pos.y()))

        total_dx1 = mid_pos.x() - start_pos.x()
        total_dy1 = mid_pos.y() - start_pos.y()
        total_distance1 = math.hypot(total_dx1, total_dy1)

        unit_dx1 = total_dx1 / total_distance1
        unit_dy1 = total_dy1 / total_distance1

        dx1 = unit_dx1 * self.speed
        dy1 = unit_dy1 * self.speed

        total_dx2 = goal_pos.x() - mid_pos.x()
        total_dy2 = goal_pos.y() - mid_pos.y()
        total_distance2 = math.hypot(total_dx2, total_dy2)

        unit_dx2 = total_dx2 / total_distance2
        unit_dy2 = total_dy2 / total_distance2

        dx2 = unit_dx2 * self.speed
        dy2 = unit_dy2 * self.speed

        closest_storm = self.storm_items[self.storm_b - 1]

        def AnimateP1(): 
            if self.fuel > 0:
                new_x = self.curr_pos.x() + dx1
                new_y = self.curr_pos.y() + dy1
                new_pos = QPointF(new_x, new_y)

                if math.hypot(mid_pos.x() - new_x, mid_pos.y() - new_y) <= self.speed:
                    self.timer.timeout.disconnect()
                    self.current_step = 0
                    self.uav_item.setRotation(self.GetAngle(mid_pos.x(), mid_pos.y(), goal_pos.x(), goal_pos.y()))
                    
                    if self.storm_hit:
                        self.PauseForStorm()

                    self.timer.timeout.connect(AnimateP2)
                    return

                self.uav_item.setPos(new_pos)
                self.curr_pos = new_pos
                self.fuel -= math.hypot(dx1, dy1)
                if self.fuel < 0:
                    self.fuel = 0      

        def AnimateP2(): 
            if self.fuel > 0:
                new_x = self.curr_pos.x() + dx2
                new_y = self.curr_pos.y() + dy2
                new_pos = QPointF(new_x, new_y)

                if math.hypot(goal_pos.x() - new_x, goal_pos.y() - new_y) <= (self.speed * 2):
                    self.timer.stop()
                    self.uav_item.is_moving = False
                    self.on_path = "NA"
                    if self.goal_item.idx == "HB":
                        self.fuel = 2000

                    self.at_goal = True
                    self.total_goal_reached += 1
                    self.score = 8 if not self.storm_hit else 5
                    #self.LogAction("UAV at Goal")
                    self.GetNewGoal()
                    self.GetNewPath()
                    self.score = 0
                    return

                self.uav_item.setPos(new_pos)
                self.curr_pos = new_pos
                self.fuel -= math.hypot(dx2, dy2)
                if self.fuel < 0:
                    self.fuel = 0   

        self.timer = QTimer()
        self.uav_item.is_moving = True
        self.idle_time = 0
        self.on_path = "B"
        self.is_idle = False
        if random.randint(1, 101) < self.hit_chancea:
            closest_storm.AnimateToPoint(self.ra_midpoint)
            self.storm_hit = True

        #self.LogAction("UAV Path B")
        self.timer.timeout.connect(AnimateP1)
        self.timer.start(32)


    def CheckIdle(self):
        if not self.is_idle or self.fuel == 0:

            if not self.uav_item.is_moving or self.fuel == 0:
                self.idle_time += 1

            else:
                self.idle_time = 0

            if self.idle_time >= 10:
                self.is_idle = True
                #self.LogAction("UAV Idle")
    
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
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click_callback()
        event.accept()