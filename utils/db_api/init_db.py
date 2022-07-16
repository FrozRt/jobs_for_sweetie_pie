from utils.db_api.connection import RawConnection


class HHDatabaseInit(RawConnection):
    @staticmethod
    async def create_city_table():
        sql = """CREATE TABLE IF NOT EXISTS Area(
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(50))"""
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_users_table():
        sql = """CREATE TABLE IF NOT EXISTS UsersFilters (
                    telegram_id INTEGER PRIMARY KEY,
                    profession VARCHAR(120),
                    area_id INTEGER,
                    salary VARCHAR(20),
                    active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (area_id) REFERENCES Area(id) ON DELETE CASCADE)"""
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_vacancy_table():
        sql = """CREATE TABLE IF NOT EXISTS ShowedVacancy(
                id INTEGER PRIMARY KEY,
                vacancy_id INTEGER,
                telegram_id INTEGER,
                FOREIGN KEY (telegram_id) REFERENCES UsersFilters(telegram_id) ON DELETE CASCADE)
                """
        await HHDatabaseInit._make_request(sql)

    async def create_tables(self):
        tables = ["city", "users", "vacancy"]
        for table in tables:
            await eval(f"self.create_{table}_table()")
