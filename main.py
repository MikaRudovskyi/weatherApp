import sys
from PyQt5.QtWidgets import QApplication
from services.ui import WeatherApp
from services.splash import SplashScreen
from PyQt5.QtCore import QTimer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    # Створюємо головне вікно, але не показуємо його одразу
    weather_app = WeatherApp()

    # Даємо заставці показатися 3 секунди, а потім закриваємо її і показуємо головне вікно
    QTimer.singleShot(3000, lambda: (splash.close(), weather_app.show()))

    sys.exit(app.exec_())
