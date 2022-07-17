import asyncio
from typing import TypedDict

import aiohttp

import models
from utils.db_api.connection import RawConnection
from utils.db_api.vacancies import HHVacancy


class Region(TypedDict):
    id: int
    parent_id: int
    name: str
    areas: list


class HHArea(RawConnection):
    @staticmethod
    async def __fetch(session: aiohttp.ClientSession):
        async with session.get("https://api.hh.ru/areas/113") as response:
            json = await response.json()
            return json["areas"]

    @staticmethod
    async def fill_area():
        async with aiohttp.ClientSession() as session:
            data = await HHArea.__fetch(session)
            tasks = []
            for republic in data:
                if republic["areas"]:
                    for region in republic["areas"]:
                        tasks.append(HHArea.get_task(region))
                else:
                    tasks.append(HHArea.get_task(republic))
            await asyncio.gather(*tasks)

    @staticmethod
    def get_task(region: Region):
        return asyncio.create_task(
            HHArea.add_area_to_db(models.Area(area_id=region["id"], title=region["name"]))
        )

    @staticmethod
    async def get_area_data(area_id: int) -> models.Area:
        sql = "SELECT * FROM Area WHERE area_id = %s"
        params = (area_id,)
        return await HHVacancy._make_request(sql, params, fetch=True, model_type=models.Area)

    @staticmethod
    async def add_area_to_db(area: models.Area):
        if not (await HHArea.get_area_data(area.area_id)):
            sql = "INSERT INTO Area (area_id, title) VALUES (%s, %s)"
            params = (area.area_id, area.title)
            await HHVacancy._make_request(sql, params)
