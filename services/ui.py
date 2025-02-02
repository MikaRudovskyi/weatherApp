from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from services.api import get_weather_data
from services.plotting import plot_temperature
from services.utils import get_weather_icon_path, create_forecast_card


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = "16c26bc8666efa2438be4753476d5a20"
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Прогноз погоди")
        self.setGeometry(100, 100, 900, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
            }
            QLineEdit {
                padding: 12px;
                font-size: 16px;
                border-radius: 10px;
                border: 2px solid #1abc9c;
                background-color: white;
            }
            QPushButton {
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                background-color: #1abc9c;
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
            QLabel {
                font-size: 18px;
                color: #34495e;
            }
        """)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Введіть назву міста...")
        self.search_button = QPushButton("🔍 Пошук")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.search_button)

        self.current_weather = QLabel("Інформація про погоду з'явиться тут.")
        self.current_weather.setAlignment(Qt.AlignCenter)
        self.current_weather.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        self.forecast_area = QScrollArea()
        self.forecast_area.setWidgetResizable(True)
        self.forecast_container = QFrame()
        self.forecast_container.setStyleSheet("background-color: #ffffff; border-radius: 10px;")
        self.forecast_layout = QHBoxLayout(self.forecast_container)
        self.forecast_area.setWidget(self.forecast_container)

        self.setLayout(QVBoxLayout())
        self.layout().addLayout(input_layout)
        self.layout().addWidget(self.current_weather)
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.forecast_area)

        self.search_button.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.current_weather.setText("Введіть назву міста!")
            return

        data = get_weather_data(city, self.api_key)
        if data:
            self.update_weather(data)
        else:
            self.current_weather.setText("Помилка отримання даних!")

    def update_weather(self, data):
        city_name = data["city"]["name"]
        forecasts = data["list"]
        current = forecasts[0]

        temp = current["main"]["temp"]
        description = current["weather"][0]["description"]
        wind_speed = current["wind"]["speed"]
        humidity = current["main"]["humidity"]

        icon_path = get_weather_icon_path(current["weather"][0]["id"])

        self.current_weather.setText(
            f'<div style="text-align: center;">'
            f'  <img src="{icon_path}" width="50" height="50"><br>'
            f'  <b style="font-size: 22px; color: #2c3e50;">{city_name}</b><br>'
            f'  🌡 Температура: {temp:.0f} °C<br>'
            f'  {description.capitalize()}<br>'
            f'  💨 Вітер: {wind_speed} м/с | 💧 Вологість: {humidity}%'
            f'</div>'
        )

        plot_temperature(self.canvas, self.figure, forecasts)

        for i in reversed(range(self.forecast_layout.count())):
            widget = self.forecast_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for forecast in forecasts[::8]:
            date = forecast["dt_txt"].split(" ")[0]
            icon = get_weather_icon_path(forecast["weather"][0]["id"])
            temp = f"{forecast['main']['temp']:.0f} °C"

            card = create_forecast_card(date, icon, temp)
            self.forecast_layout.addWidget(card)
