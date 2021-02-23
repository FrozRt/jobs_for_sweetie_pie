import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

admins = [os.getenv("ADMIN1"), os.getenv("ADMIN2")]

CHANNEL = os.getenv("CHANNEL")
