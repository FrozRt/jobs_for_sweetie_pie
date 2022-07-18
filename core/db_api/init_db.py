from core.db_api.connection import RawConnection
from core.db_api.vacancies import HHVacancy


class HHDatabaseInit(RawConnection):
    @staticmethod
    async def create_city_table():
        sql = """CREATE TABLE IF NOT EXISTS Cities(
            city_id INTEGER PRIMARY KEY,
            title VARCHAR(100));
            CREATE INDEX id_index ON Cities(city_id) USING HASH;
            """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_technology_stack_table():
        sql = """CREATE TABLE IF NOT EXISTS TechnologyStacks(
            technology_stack_id INTEGER PRIMARY KEY,
            title VARCHAR(120));
            CREATE INDEX id_index ON TechnologyStacks(technology_stack_id) USING HASH;
            """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_channels_table():
        sql = """CREATE TABLE IF NOT EXISTS Channels(
            channel_id INTEGER PRIMARY KEY,
            technology_stack_id INTEGER,
            city_id INTEGER,
            salary VARCHAR(20),
            active BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (city_id) REFERENCES
            Cities(city_id) ON DELETE CASCADE,
            FOREIGN KEY (technology_stack_id) REFERENCES
            TechnologyStacks(technology_stack_id) ON DELETE CASCADE);
            """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_vacancy_table():
        sql = """CREATE TABLE IF NOT EXISTS Vacancies(
            vacancy_id INTEGER PRIMARY KEY,
            city_id INTEGER,
            salary VARCHAR(20),
            title TEXT,
            description TEXT,
            FOREIGN KEY (city_id) REFERENCES
            Cities(city_id) ON DELETE CASCADE);
            """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_vacancy_channel_table():
        sql = """CREATE TABLE IF NOT EXISTS VacancyChannel(
            id INTEGER PRIMARY KEY,
            vacancy_id INTEGER,
            channel_id INTEGER,
            FOREIGN KEY (vacancy_id) REFERENCES Vacancies(vacancy_id) ON DELETE CASCADE,
            FOREIGN KEY (channel_id) REFERENCES Channels(channel_id) ON DELETE CASCADE);
            CREATE INDEX channel_vac_index ON VacancyChannel(vacancy_id, channel_id) USING HASH;
            """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_vacancy_stack_table():
        sql = """CREATE TABLE IF NOT EXISTS VacancyTechnologyStack(
            id INTEGER PRIMARY KEY,
            vacancy_id INTEGER,
            technology_stack_id INTEGER,
            FOREIGN KEY (vacancy_id) REFERENCES Vacancies(vacancy_id) ON DELETE CASCADE,
            FOREIGN KEY (technology_stack_id) REFERENCES
            TechnologyStacks(technology_stack_id) ON DELETE CASCADE);
            CREATE INDEX channel_vac_index ON
            VacancyTechnologyStack(vacancy_id, technology_stack_id) USING HASH;
            """
        await HHDatabaseInit._make_request(sql)

    async def create_tables(self):
        tables = (
            "city",
            "technology_stack",
            "channels",
            "vacancy",
            "vacancy_channel",
            "vacancy_stack",
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
        await self.fill_cities_table()
