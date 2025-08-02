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

class GoalItem(QGraphicsEllipseItem):
    def __init__(self, idx, x_goal, y_goal):
        super().__init__()

        self.setRect(QRectF(0, 0, 30, 30))
        self.setBrush(Qt.GlobalColor.white)
        self.setPen(QPen(Qt.GlobalColor.black, 3))
        self.setPos(x_goal, y_goal)

        self.text_item = QGraphicsTextItem(str(idx), self)
        font = QFont("Times New Roman", 14, QFont.Weight.Bold)
        self.text_item.setFont(font)

        text_rect = self.text_item.boundingRect()
        ellipse_rect = self.rect()
        x = (ellipse_rect.width() - text_rect.width()) / 2
        y = (ellipse_rect.height() - text_rect.height()) / 2
        self.text_item.setPos(x, y)

        self.pos_x = x_goal
        self.pos_y = y_goal
        self.idx = idx
        
class PathItem():
    def __init__(self, color, x_pos, y_pos, x_goal, y_goal, angle):
        super().__init__()

        self.color = QColor(color)
        self.start = QPointF(x_pos, y_pos)
        self.end = QPointF(x_goal + 15, y_goal + 15)

        self.hyp, self.hyp_label, self.hyp_length = self.CreateHyp()
        self.ra, self.ra_label, self.ra_midpoint, self.ra_length = self.CreateRA(angle)

    def CreateHyp(self):
        path = QPainterPath()
        path.moveTo(self.start)
        path.lineTo(self.end)
        
        path_length = int(math.hypot(self.end.x() - self.start.x(), self.end.y() - self.start.y()))

        path_item = QGraphicsPathItem(path)

        pen = QPen(self.color)
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setWidth(4)
        path_item.setPen(pen)

        x_mid = (self.start.x() + self.end.x()) / 2
        y_mid = (self.start.y() + self.end.y()) / 2
        mid_point = QPointF(x_mid, y_mid)
        path_label = self.GenLabel("A", mid_point)
        return path_item, path_label, path_length
    
    def CreateRA(self, angle):
        path = QPainterPath()
        path.moveTo(self.start)
        theta = math.radians(angle)

        dx = self.end.x() - self.start.x()
        dy = self.end.y() - self.start.y()
        c = math.hypot(dx, dy)

        if c == 0:
            bend = self.start
        else:
            a = c / (2 * math.sin(theta / 2))

            mx = (self.start.x() + self.end.x()) / 2
            my = (self.start.y() + self.end.y()) / 2
            #midpoint = QPointF(mx, my)

            ux = -dy / c
            uy = dx / c
            h = math.sqrt(a**2 - (c / 2)**2)

            bx = mx + h * ux
            by = my + h * uy
            bend = QPointF(bx, by)

        path.lineTo(bend)
        path.lineTo(self.end)
        path_length = int(math.hypot(bend.x() - self.start.x(), bend.y() - self.start.y()) + math.hypot(self.end.x() - bend.x(), self.end.y() - bend.y()))

        path_item = QGraphicsPathItem(path)
        pen = QPen(self.color)
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setWidth(4)
        path_item.setPen(pen)

        path_label = self.GenLabel("B", bend)
        return path_item, path_label, bend, path_length

    def GenLabel(self, name: str, point):
        label = QGraphicsEllipseItem()

        label.setRect(QRectF(0, 0, 32, 24))
        label.setBrush(Qt.GlobalColor.white)
        label.setPen(QPen(Qt.GlobalColor.black, 2))

        x_pos = point.x()
        y_pos = point.y()
        label.setPos(x_pos - 16, y_pos - 12)

        text_item = QGraphicsTextItem(str(name), label)
        font = QFont("Times New Roman", 14, QFont.Weight.Bold)
        text_item.setFont(font)

        text_rect = text_item.boundingRect()
        ellipse_rect = label.rect()
        x = (ellipse_rect.width() - text_rect.width()) / 2
        y = (ellipse_rect.height() - text_rect.height()) / 2
        text_item.setPos(x, y)

        return label