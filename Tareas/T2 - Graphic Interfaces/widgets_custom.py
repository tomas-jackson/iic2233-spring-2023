from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QDrag


class BotonArrastable(QPushButton):

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = self.icon().pixmap(32, 32)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)
