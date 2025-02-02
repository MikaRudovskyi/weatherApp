import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def plot_temperature(canvas, figure, forecasts):
    times = [datetime.strptime(f["dt_txt"], "%Y-%m-%d %H:%M:%S") for f in forecasts[:8]]
    temps = [f["main"]["temp"] for f in forecasts[:8]]

    figure.clear()
    ax = figure.add_subplot(111)

    # Градиентная линия
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(temps)))
    for i in range(len(temps) - 1):
        ax.plot(times[i:i + 2], temps[i:i + 2], marker="o", linestyle="-", color=colors[i], linewidth=3)

    # Подписи температур
    for time, temp in zip(times, temps):
        ax.text(time, temp + 0.5, f"{temp:.1f}°C", fontsize=12, ha='center', va='bottom', color="#34495e",
                fontweight="bold")

    ax.set_title("Температура (наступні 24 години)", fontsize=14, fontweight="bold", color="#2c3e50")
    ax.set_xlabel("Час", fontsize=12, color="#2c3e50")
    ax.set_ylabel("Температура (°C)", fontsize=12, color="#2c3e50")

    ax.tick_params(axis='both', which='major', labelsize=10, colors="#34495e")
    ax.grid(True, linestyle="--", alpha=0.5)

    figure.autofmt_xdate()
    canvas.draw()
