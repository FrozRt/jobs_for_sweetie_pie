import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    CHANNEL = os.getenv("CHANNEL")
    API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

    admins = [os.getenv("ADMIN1"), os.getenv("ADMIN2")]

    MY_DB = os.getenv("DB_NAME")
    MY_HOST = os.getenv("DB_HOST")
    MY_PORT = os.getenv("DB_PORT")
    MY_USER = os.getenv("DB_USER")
    MY_PASSWORD = os.getenv("DB_PASSWORD")

    @classmethod
    def get_db_connection_data(cls):
        return {k[3:].lower(): v for k, v in cls.__dict__.items() if k[:3] == 'MY_'}


settings = Settings()
print(settings.get_db_connection_data())
