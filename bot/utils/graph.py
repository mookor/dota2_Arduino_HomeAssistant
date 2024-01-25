import matplotlib.pyplot as plt
import seaborn as sns
from bot.config import plot_path
from logger import Logger


def draw_graph(flatten_data, dates, meassure_type):
    
    Logger.info("Drawing graph")
    sns.set(style="whitegrid")
    if len(flatten_data) == 0:
        Logger.info("not enough data to draw graph")
        return False
    
    fig = plt.figure(figsize=(10, 6))
    label = "Влажность" if meassure_type == "humidity" else "Температура"

    dates_len = len(dates)


    sns.lineplot(x=dates, y=flatten_data, marker='o', color='b', label=label)

    plt.xlabel('Date')
    plt.ylabel(label)
    
    if dates_len > 60:
        dates = dates[::int(dates_len / 60)]
    plt.xticks(dates, rotation=65)
    plt.tight_layout()

    # Добавляем сетку на задний фон
    plt.grid(True, linestyle='--', alpha=0.6)

    # Отображаем легенду
    plt.legend()

    fig.savefig(plot_path, format='png')
    Logger.info("graph was drawn")
    return True
