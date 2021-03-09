from aiogram import types

import models
from .connection import RawConnection


class HHVacancy(RawConnection):
    @staticmethod
    async def get_vacancy_data(vacancy_id: int) -> models.Vacancy:
        sql = 'SELECT * FROM vacancies WHERE vacancy_id = %s '
        params = (vacancy_id,)
        return await HHVacancy._make_request(sql, params, fetch=True, model_type=models.Vacancy)

    @staticmethod
    async def add_to_db(vacancy: types.User):
        if not (await HHVacancy.get_vacancy_data(vacancy.id)):
            sql = 'INSERT INTO vacancies (vacancy_id, name) VALUES (%s, %s)'
            params = (vacancy.id, vacancy.full_name)
            await HHVacancy._make_request(sql, params)
