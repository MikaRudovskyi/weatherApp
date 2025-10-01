from PyQt5.QtWidgets import QSplashScreen, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()

        pixmap = QPixmap("icons/splash.png")
        self.setPixmap(pixmap)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(pixmap.size())

        self.label = QLabel("Ласкаво просимо!", self)
        self.label.setFont(QFont("Montserrat", 30, QFont.Bold))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, self.height() // 2 - 40, self.width(), 80)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(Qt.black)
        self.label.setGraphicsEffect(shadow)

        self.opacity_animation = QPropertyAnimation(self.label, b"windowOpacity")
        self.opacity_animation.setDuration(1200)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.scale_animation = QPropertyAnimation(self.label, b"geometry")
        self.scale_animation.setDuration(1200)
        self.scale_animation.setStartValue(self.label.geometry().adjusted(0, 10, 0, -10))
        self.scale_animation.setEndValue(self.label.geometry())
        self.scale_animation.setEasingCurve(QEasingCurve.OutBounce)

        self.opacity_animation.start()
        self.scale_animation.start()

    def keyPressEvent(self, event):
        self.close()