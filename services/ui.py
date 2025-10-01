import json
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QScrollArea, QFrame, QComboBox, QApplication
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from services.api import get_weather_data
from services.plotting import plot_temperature
from services.utils import get_weather_icon_path, create_forecast_card

class WeatherApp(QWidget):
    FAVORITES_FILE = "favorites.json"
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        super().__init__()
        self.api_key = "16c26bc8666efa2438be4753476d5a20"
        self.last_weather_data = None

        self.themes = {
            "light": {
                "style": """
                    QWidget {
                        background-color: #f5f7fa;
                    }
                    QLineEdit, QComboBox {
                        padding: 12px;
                        font-size: 16px;
                        border-radius: 10px;
                        border: 2px solid #1abc9c;
                        background-color: white;
                        color: #2c3e50;
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
                """,
                "weather_color": "#2c3e50"
            },
            "dark": {
                "style": """
                    QWidget {
                        background-color: #2c3e50;
                    }
                    QLineEdit, QComboBox {
                        padding: 12px;
                        font-size: 16px;
                        border-radius: 10px;
                        border: 2px solid #3498db;
                        background-color: #34495e;
                        color: white;
                    }
                    QPushButton {
                        padding: 12px;
                        font-size: 16px;
                        font-weight: bold;
                        background-color: #3498db;
                        color: white;
                        border-radius: 10px;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                    QLabel {
                        font-size: 18px;
                        color: #ecf0f1;
                    }
                """,
                "weather_color": "#ecf0f1"
            }
        }

        self.current_theme = self.load_theme()
        self.initUI()
        self.load_favorites()

    def initUI(self):
        self.setWindowTitle("Прогноз погоди")
        self.resize(1280, 720)
        self.center_window()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Введіть назву міста...")
        self.search_button = QPushButton("🔍 Пошук")
        self.favorites_button = QPushButton("⭐ Додати в обране")
        self.delete_favorite_button = QPushButton("🗑 Видалити з обраного")
        self.reset_button = QPushButton("🔄 Скинути")
        self.theme_button = QPushButton("🌗 Тема")

        self.favorites_combo = QComboBox()
        self.favorites_combo.setPlaceholderText("Виберіть місто з обраного")
        self.favorites_combo.currentIndexChanged.connect(self.select_favorite)

        self.favorites_label = QLabel("Обрані міста:")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.search_button)
        input_layout.addWidget(self.favorites_button)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.favorites_label)
        buttons_layout.addWidget(self.favorites_combo)
        buttons_layout.addWidget(self.delete_favorite_button)
        buttons_layout.addWidget(self.reset_button)
        buttons_layout.addWidget(self.theme_button)

        self.current_weather = QLabel()
        self.current_weather.setAlignment(Qt.AlignCenter)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        self.forecast_area = QScrollArea()
        self.forecast_area.setWidgetResizable(True)
        self.forecast_container = QFrame()
        self.forecast_container.setStyleSheet("border-radius: 10px;")
        self.forecast_layout = QHBoxLayout(self.forecast_container)
        self.forecast_area.setWidget(self.forecast_container)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.current_weather)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self.forecast_area)

        self.setLayout(main_layout)

        self.search_button.clicked.connect(self.get_weather)
        self.favorites_button.clicked.connect(self.add_to_favorites)
        self.delete_favorite_button.clicked.connect(self.remove_from_favorites)
        self.reset_button.clicked.connect(self.reset_app)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.city_input.returnPressed.connect(self.get_weather)

        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(self.themes[self.current_theme]["style"])
        text_color = self.themes[self.current_theme]["weather_color"]

        if self.last_weather_data:
            self.update_weather(self.last_weather_data)
        else:
            self.current_weather.setText(
                f'<div style="text-align: center; font-size: 22px; font-weight: bold; color: {text_color};">'
                f'Інформація про погоду з\'явиться тут.'
                f'</div>'
            )
            self.update_chart_background()

    def update_chart_background(self):
        bg_color = "#ffffff" if self.current_theme == "light" else "#2c3e50"
        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        self.canvas.draw()

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        self.save_theme()

    def save_theme(self):
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"theme": self.current_theme}, f, ensure_ascii=False, indent=4)

    def load_theme(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
            return settings.get("theme", "light")
        return "light"

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.current_weather.setText(
                f'<div style="text-align: center; font-size: 22px; font-weight: bold; color: {self.themes[self.current_theme]["weather_color"]};">'
                f'Введіть назву міста!'
                f'</div>'
            )
            return
        data = get_weather_data(city, self.api_key)
        if data:
            self.update_weather(data)
        else:
            self.current_weather.setText(
                f'<div style="text-align: center; font-size: 22px; font-weight: bold; color: {self.themes[self.current_theme]["weather_color"]};">'
                f'Помилка отримання даних!'
                f'</div>'
            )

    def update_weather(self, data):
        self.last_weather_data = data
        city_name = data["city"]["name"]
        forecasts = data["list"]
        current = forecasts[0]

        temp = current["main"]["temp"]
        description = current["weather"][0]["description"]
        wind_speed = current["wind"]["speed"]
        humidity = current["main"]["humidity"]

        icon_path = get_weather_icon_path(current["weather"][0]["id"])
        text_color = self.themes[self.current_theme]["weather_color"]

        self.current_weather.setText(
            f'<div style="text-align: center; color: {text_color};">'
            f'  <img src="{icon_path}" width="50" height="50"><br>'
            f'  <b style="font-size: 22px;">{city_name}</b><br>'
            f'  🌡 Температура: {temp:.0f} °C<br>'
            f'  {description.capitalize()}<br>'
            f'  💨 Вітер: {wind_speed} м/с | 💧 Вологість: {humidity}%'
            f'</div>'
        )

        plot_temperature(self.canvas, self.figure, forecasts, self.current_theme)

        for i in reversed(range(self.forecast_layout.count())):
            widget = self.forecast_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for forecast in forecasts[::8]:
            date = forecast["dt_txt"].split(" ")[0]
            icon = get_weather_icon_path(forecast["weather"][0]["id"])
            temp = f"{forecast['main']['temp']:.0f} °C"
            card = create_forecast_card(date, icon, temp, self.current_theme)
            self.forecast_layout.addWidget(card)

    def add_to_favorites(self):
        city = self.city_input.text().strip()
        if not city:
            return
        favorites = self.load_favorites()
        if city not in favorites:
            favorites.append(city)
            self.save_favorites(favorites)
            self.favorites_combo.clear()
            self.favorites_combo.addItems(favorites)

    def remove_from_favorites(self):
        city = self.favorites_combo.currentText()
        if not city:
            return
        favorites = self.load_favorites()
        if city in favorites:
            favorites.remove(city)
            self.save_favorites(favorites)
            self.favorites_combo.removeItem(self.favorites_combo.currentIndex())

    def reset_app(self):
        self.city_input.clear()
        self.last_weather_data = None
        self.apply_theme()
        self.figure.clear()
        self.canvas.draw()
        for i in reversed(range(self.forecast_layout.count())):
            widget = self.forecast_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def load_favorites(self):
        if os.path.exists(self.FAVORITES_FILE):
            with open(self.FAVORITES_FILE, "r", encoding="utf-8") as f:
                favorites = json.load(f)
        else:
            favorites = []
        self.favorites_combo.clear()
        self.favorites_combo.addItems(favorites)
        return favorites

    def save_favorites(self, favorites):
        with open(self.FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(favorites, f, ensure_ascii=False, indent=4)

    def select_favorite(self):
        city = self.favorites_combo.currentText()
        if city:
            self.city_input.setText(city)
            self.get_weather()