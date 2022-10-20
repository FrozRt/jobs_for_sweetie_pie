from typing import List

import models
from core.db_api.connection import RawConnection


class HHVacancy(RawConnection):
    @staticmethod
    async def get_vacancy_data(vacancy_id: int, channel_id: int) -> models.Vacancy:
        sql = "SELECT EXISTS (SELECT * FROM Vacancies WHERE vacancy_id = %s AND channel_id = %s)"
        params = (vacancy_id, channel_id)
        return await HHVacancy._make_request(sql, params, fetch=True)

    @staticmethod
    async def add_to_db(vacancy: models.Vacancy):
        if not (await HHVacancy.get_vacancy_data(vacancy.vacancy_id, vacancy.channel_id)):
            sql = (
                "INSERT INTO Vacancies(vacancy_id, channel_id, title, description, salary, company)"
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            params = tuple(vacancy.dict().values())
            await HHVacancy._make_request(sql, params, model_type=models.Vacancy)

    @staticmethod
    async def get_channels() -> models.Channel:
        sql = "SELECT * FROM Channels"
        return await HHVacancy._make_request(sql, fetch=True, mult=True, model_type=models.Channel)

    @staticmethod
    async def get_new_vacancies() -> models.Vacancy:
        sql = "SELECT * FROM Vacancies WHERE is_posted = 0"
        return await HHVacancy._make_request(sql, fetch=True, mult=True, model_type=models.Vacancy)

    @staticmethod
    async def update_given_vacancies(params: List[tuple]) -> None:
        sql = """UPDATE Vacancies
        SET is_posted = 1
        WHERE vacancy_id IN %s AND channel_id IN %s
        """
        params = ([v.vacancy_id for v in params], [v.channel_id for v in params])
        await HHVacancy._make_request(sql, params, mult=True, model_type=models.Vacancy)


database = HHVacancy()
