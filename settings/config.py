import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    CHANNEL = os.getenv("CHANNEL")
    API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

    admins = [os.getenv("ADMIN1"), os.getenv("ADMIN2")]


settings = Settings()

