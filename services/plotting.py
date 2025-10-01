import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.interpolate import make_interp_spline

def plot_temperature(canvas, figure, forecasts, theme="light"):
    times = [datetime.strptime(f["dt_txt"], "%Y-%m-%d %H:%M:%S") for f in forecasts[:8]]
    temps = [f["main"]["temp"] for f in forecasts[:8]]

    figure.clear()
    ax = figure.add_subplot(111)

    time_nums = np.linspace(0, len(times) - 1, 300)
    time_indices = np.arange(len(times))
    spline = make_interp_spline(time_indices, temps, k=3)
    smooth_temps = spline(time_nums)

    smooth_times = np.linspace(times[0].timestamp(), times[-1].timestamp(), 300)
    smooth_times = [datetime.fromtimestamp(t) for t in smooth_times]

    colors = plt.cm.viridis(np.linspace(0, 1, len(smooth_temps)))

    for i in range(len(smooth_temps) - 1):
        ax.plot(smooth_times[i:i + 2], smooth_temps[i:i + 2], linestyle="-", color=colors[i], linewidth=3)

    if theme == "dark":
        text_color = "#ecf0f1"
        spine_color = "#95a5a6"
        tick_color = "#bdc3c7"
        bg_color = "#2c3e50"
    else:
        text_color = "#2c3e50"
        spine_color = "#bbb"
        tick_color = "#34495e"
        bg_color = "#ffffff"

    for time, temp in zip(times, temps):
        ax.text(time, temp + 0.5, f"{temp:.1f}°C", fontsize=12, ha='center', va='bottom',
                color=text_color, fontweight="bold")

    ax.set_title("Температура (наступні 24 години)", fontsize=14, fontweight="bold", color=text_color)
    ax.set_xlabel("Час", fontsize=12, color=text_color)
    ax.set_ylabel("Температура (°C)", fontsize=12, color=text_color)

    ax.set_facecolor(bg_color)
    figure.set_facecolor(bg_color)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(spine_color)
    ax.spines["bottom"].set_color(spine_color)

    ax.tick_params(axis='both', which='major', labelsize=10, colors=tick_color)
    ax.grid(True, linestyle="--", alpha=0.3, color=spine_color)

    figure.autofmt_xdate()
    canvas.draw()