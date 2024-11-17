import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Пошук міста: ", self)
        self.city_input = QLineEdit(self)

        self.unit_label = QLabel("Оберіть одиницю вимірювання температури: ", self)
        self.unit_selector = QComboBox(self)
        self.unit_selector.addItems(["Цельсій", "Фаренгейт"])

        self.get_weather_button = QPushButton("Показати погоду", self)
        self.temperature_label = QLabel(self)
        self.icon_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)

        vbox.addWidget(self.unit_label)
        vbox.addWidget(self.unit_selector)

        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.icon_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)

        self.unit_label.setAlignment(Qt.AlignCenter)

        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff; /* Светло голубой фон */
            }
            QLabel, QPushButton, QComboBox {
                font-family: 'Segoe UI', Calibri, sans-serif;
                color: #2e4053; /* Тёмно-серый текст */
            }
            QLabel {
                font-size: 20px;
            }
            QLineEdit {
                font-size: 20px;
                padding: 5px;
                border: 2px solid #5dade2; /* Голубая рамка */
                border-radius: 5px;
                background-color: #ffffff; /* Белый фон */
            }
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                background-color: #5dade2; /* Голубая кнопка */
                color: white; /* Белый текст */
                border: none;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3498db; /* Более насыщенный голубой при наведении */
            }
            QPushButton:pressed {
                background-color: #2874a6; /* Темный голубой при нажатии */
            }
            QComboBox {
                font-size: 20px;
                padding: 5px;
                border: 2px solid #5dade2; /* Голубая рамка */
                border-radius: 5px;
                background-color: #ffffff; /* Белый фон */
            }
            QLabel#temperature_label {
                font-size: 50px;
                font-weight: bold;
                color: #1c2833; /* Темный текст */
            }
            QLabel#icon_label {
                font-size: 100px;
                font-family: 'Segoe UI Emoji';
            }
            QLabel#description_label {
                font-size: 25px;
                font-style: italic;
                color: #34495e; /* Темно-синий текст */
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "16c26bc8666efa2438be4753476d5a20"
        city = self.city_input.text().capitalize()

        if not city.strip():
            self.display_error("Будь ласка, введіть назву міста!")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ua"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            if 'response' in locals() and response is not None:
                match response.status_code:
                    case 400:
                        self.display_error("Поганий запит:\nперевірте введені дані")
                    case 401:
                        self.display_error("Неавторизовано:\nНедійсний ключ API")
                    case 403:
                        self.display_error("Заборонено:\nДоступ заборонено")
                    case 404:
                        self.display_error("Не знайдено:\nМісто не знайдено")
                    case 500:
                        self.display_error("Внутрішня помилка сервера:\nПовторіть спробу пізніше")
                    case 502:
                        self.display_error("Поганий шлюз:\nНевірна відповідь від сервера")
                    case 503:
                        self.display_error("Сервіс недоступний:\nСервер не працює")
                    case 504:
                        self.display_error("Час очікування шлюзу:\nНемає відповіді від сервера")
                    case _:
                        self.display_error(f"Сталася помилка HTTP:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Помилка підключення:\nПеревірте підключення до Інтернету")
        except requests.exceptions.Timeout:
            self.display_error("Помилка часу очікування:\nЧас очікування запиту минув")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Забагато перенаправлень:\nПеревірте URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Помилка запиту:\n{req_error}")

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 50px;")
        temperature_k = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        unit = self.unit_selector.currentText()
        if unit == "Цельсій":
            temperature = f"{temperature_k - 273.15:.0f} °C"
        elif unit == "Фаренгейт":
            temperature = f"{(temperature_k * 9 / 5) - 459.67:.0f} °F"

        self.temperature_label.setText(temperature)

        icon_path = self.get_weather_icon_path(weather_id)
        pixmap = QPixmap(icon_path)

        # Перевірка на правильність завантаження іконки
        if pixmap.isNull():
            print(f"Не вдалося завантажити іконку: {icon_path}")
        else:
            self.icon_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

        self.description_label.setText(weather_description.capitalize())

    @staticmethod
    def get_weather_icon_path(weather_id):
        if 200 <= weather_id <= 232:
            return "icons/thunderstorm.png"
        elif 300 <= weather_id <= 321:
            return "icons/drizzle.png"
        elif 500 <= weather_id <= 531:
            return "icons/rain.png"
        elif 600 <= weather_id <= 622:
            return "icons/snow.png"
        elif 701 <= weather_id <= 741:
            return "icons/fog.png"
        elif weather_id == 762:
            return "icons/volcano.png"
        elif weather_id == 771:
            return "icons/wind.png"
        elif weather_id == 781:
            return "icons/tornado.png"
        elif weather_id == 800:
            return "icons/sunny.png"
        elif 801 <= weather_id <= 804:
            return "icons/cloudy.png"
        else:
            return ""

    def display_error(self, message):
        self.temperature_label.setText(message)
        self.icon_label.clear()
        self.description_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())