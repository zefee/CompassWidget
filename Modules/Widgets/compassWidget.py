import math

from PySide2.QtWidgets import QWidget, QHBoxLayout
from PySide2.QtGui import QPainter, QBrush, QColor, QPen, QPainterPath
from PySide2.QtCore import Qt, QPointF, QSizeF, QRectF, QSize, QPoint, QLineF, QLine

class CompassWidget(QWidget):
    def __init__(self, parent=None):
        super(CompassWidget, self).__init__(parent)
        self.setMouseTracking(True)
        self._dragging = False
        self._last_pos = None
        self._angle = 0.0
        self.snap_angle = 10

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        size = self.size()
        center = QPointF(size.width() / 2, size.height() / 2)
        self.sWidth = size.width()
        self.sHeight = size.height()
        radius = min(size.width(), size.height()) / 2 - 5

        # Draw background
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, radius, radius)

        # Draw arrow
        painter.setPen(QPen(Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black))
        painter.drawEllipse(center, radius * 0.03, radius * 0.03)
        painter.translate(center)
        painter.rotate(self._angle)
        self._arrowTip = QPointF(0, -radius)
        tailLine = QLineF(QPointF(0, 0), self._arrowTip)
        arrowLeft = QLineF(self._arrowTip, QPointF(-radius * 0.3, -radius * 0.7))
        arrowRight = QLineF(self._arrowTip, QPointF(radius * 0.3, -radius * 0.7))
        painter.drawLine(tailLine)
        painter.drawLine(arrowLeft)
        painter.drawLine(arrowRight)

        self._arrowTip = painter.transform().map(self._arrowTip)
        self._arrowTip -= center
        self._arrowTip /= radius

        # Calculate direction vector
        direction_vector = QPointF(0, -1)
        direction_vector = painter.transform().map(direction_vector)
        direction_vector -= center
        direction_vector /= radius

    def sizeHint(self):
        return QSize(100, 100)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if not self._dragging:
            return

        size = self.size()
        center = QPoint(size.width() / 2, size.height() / 2)

        # Calculate the angle between the center of the compass and the mouse position
        mouse_position = event.pos()
        direction_vector = mouse_position - center
        angle = math.atan2(direction_vector.y(), direction_vector.x()) * 180 / math.pi

        # Update the angle of the compass

        if event.modifiers() & Qt.ShiftModifier:
            angle = round(angle / self.snap_angle) * self.snap_angle

        self.angle = angle + 90

        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self.direction_vector_changed.emit(self._arrowTip.x(), self._arrowTip.y() * -1)
            self.size_changed.emit(self.sWidth, self.sHeight)
            self.angle_changed.emit(self.angle)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    from PySide2.QtCore import Signal
    direction_vector_changed = Signal(float, float)
    size_changed = Signal(float, float)
    angle_changed = Signal(float)