from core.db_api.connection import RawConnection
from core.db_api.vacancies import HHVacancy


class HHDatabaseInit(RawConnection):
    @staticmethod
    async def create_city_table():
        sql = """CREATE TABLE IF NOT EXISTS Cities(
            city_id INTEGER PRIMARY KEY,
            title VARCHAR(100));
            # CREATE INDEX id_index ON Cities(city_id) USING HASH;
            """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_channels_table():
        sql = """CREATE TABLE IF NOT EXISTS Channels(
            channel_id BIGINT PRIMARY KEY,
            city_id INTEGER,
            filter TEXT,
            FOREIGN KEY (city_id) REFERENCES
            Cities(city_id) ON DELETE CASCADE);
            """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_vacancy_table():
        sql = """CREATE TABLE IF NOT EXISTS Vacancies(
            vacancy_id BIGINT,
            channel_id BIGINT,
            company TEXT,
            salary CHAR(50),
            title TEXT,
            description TEXT,
            is_posted BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (vacancy_id, channel_id),
            FOREIGN KEY (channel_id) REFERENCES
            Channels(channel_id));
            """
        await HHDatabaseInit._make_request(sql)

    async def create_tables(self):
        tables = (
            "city",
            "channels",
            "vacancy",
        )
        for table in tables:
            await eval(f"self.create_{table}_table()")

    @staticmethod
    async def fill_cities_table():
        sql = "INSERT INTO Cities(city_id, title) VALUES (%s, %s)"
        params = [
            (1, "Москва"),
            (2, "Санкт-Петербург"),
            (3, "Екатеринбург"),
            (4, "Новосибирск"),
            (88, "Казань"),
        ]
        await HHVacancy._make_request(sql, params)

    async def expand_database(self):
        await self.create_tables()
        # await self.fill_cities_table()
