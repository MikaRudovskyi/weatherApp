from PyQt5.QtWidgets import QSplashScreen, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()

        # Завантажуємо фонове зображення
        pixmap = QPixmap("icons/splash.png")
        self.setPixmap(pixmap)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(pixmap.size())  # Встановлюємо розмір заставки відповідно до зображення

        # Додаємо текст "Ласкаво просимо!"
        self.label = QLabel("Ласкаво просимо!", self)
        self.label.setFont(QFont("Montserrat", 30, QFont.Bold))  # Сучасний шрифт
        self.label.setStyleSheet("color: white;")  # Білий текст
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, self.height() // 2 - 40, self.width(), 80)

        # Додаємо тінь для тексту
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(Qt.black)
        self.label.setGraphicsEffect(shadow)

        # Анімація прозорості (fade-in)
        self.opacity_animation = QPropertyAnimation(self.label, b"windowOpacity")
        self.opacity_animation.setDuration(1200)  # 1.2 секунди
        self.opacity_animation.setStartValue(0)  # Починаємо з 0 (прозорість)
        self.opacity_animation.setEndValue(1)  # Повністю видно
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Анімація масштабу (zoom-in ефект)
        self.scale_animation = QPropertyAnimation(self.label, b"geometry")
        self.scale_animation.setDuration(1200)
        self.scale_animation.setStartValue(self.label.geometry().adjusted(0, 10, 0, -10))  # Трохи менше розміром
        self.scale_animation.setEndValue(self.label.geometry())  # Повертається в нормальний розмір
        self.scale_animation.setEasingCurve(QEasingCurve.OutBounce)

        # Запускаємо анімації
        self.opacity_animation.start()
        self.scale_animation.start()

    def keyPressEvent(self, event):
        """Закриваємо заставку при натисканні будь-якої клавіші."""
        self.close()
