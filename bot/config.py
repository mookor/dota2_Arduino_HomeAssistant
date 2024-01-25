from dotenv import load_dotenv
from logger import Logger
import os

if load_dotenv():
    Logger.info("Loaded .env file")
else:
    Logger.error("Failed to load .env file")

bot_token = os.getenv("BOT_TOKEN")
plot_path = "graph.png"

