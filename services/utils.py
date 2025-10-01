from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def get_weather_icon_path(weather_id):
    base_path = "icons/"
    if 200 <= weather_id <= 232:
        return base_path + "thunderstorm.png"
    elif 300 <= weather_id <= 321:
        return base_path + "drizzle.png"
    elif 500 <= weather_id <= 531:
        return base_path + "rain.png"
    elif 600 <= weather_id <= 622:
        return base_path + "snow.png"
    elif 701 <= weather_id <= 781:
        return base_path + "fog.png"
    elif weather_id == 800:
        return base_path + "sunny.png"
    elif 801 <= weather_id <= 804:
        return base_path + "cloudy.png"
    else:
        return base_path + "unknown.png"

def create_forecast_card(date, icon_path, temp):
    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #ddd;
        }
    """)

    layout = QVBoxLayout(card)

    date_label = QLabel(date)
    date_label.setAlignment(Qt.AlignCenter)
    date_label.setStyleSheet("font-size: 14px;")

    icon_label = QLabel()
    icon_pixmap = QPixmap(icon_path)
    icon_label.setPixmap(icon_pixmap.scaled(50, 50, Qt.KeepAspectRatio))
    icon_label.setAlignment(Qt.AlignCenter)

    temp_label = QLabel(temp)
    temp_label.setAlignment(Qt.AlignCenter)
    temp_label.setStyleSheet("font-size: 16px; font-weight: bold;")

    layout.addWidget(date_label)
    layout.addWidget(icon_label)
    layout.addWidget(temp_label)

    return card