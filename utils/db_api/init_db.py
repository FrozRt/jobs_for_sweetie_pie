from utils.db_api.connection import RawConnection


class HHDatabaseInit(RawConnection):
    @staticmethod
    async def create_city_table():
        sql = """CREATE TABLE IF NOT EXISTS Area(
                area_id INTEGER PRIMARY KEY,
                title VARCHAR(100));
                # CREATE INDEX id_index ON Area(area_id) USING HASH;          
                """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_users_table():
        sql = """CREATE TABLE IF NOT EXISTS UsersFilters (
                user_id INTEGER PRIMARY KEY,
                profession VARCHAR(120),
                area_id INTEGER,
                salary VARCHAR(20),
                active BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (area_id) REFERENCES Area(area_id) ON DELETE CASCADE);
                """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def create_vacancy_table():
        sql = """CREATE TABLE IF NOT EXISTS ShowedVacancy(
                id INTEGER PRIMARY KEY,
                vacancy_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES UsersFilters(user_id) ON DELETE CASCADE);
                # CREATE INDEX user_vac_index ON ShowedVacancy(vacancy_id, user_id) USING HASH;
                """
        await HHDatabaseInit._make_request(sql)

    @staticmethod
    async def pull_area_table():
        pass

    async def create_tables(self):
        tables = ["city", "users", "vacancy"]
        for table in tables:
            await eval(f"self.create_{table}_table()")
