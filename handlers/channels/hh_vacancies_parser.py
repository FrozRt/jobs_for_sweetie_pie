import asyncio

import aiohttp
from bs4 import BeautifulSoup, Tag

import models
from core.db_api.vacancies import database

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 \
                                        Safari/537.36",
    "accept": "*/*",
}
params = {
    "text": "backend developer",
    "area": 2,  # Поиск ощуществляется по вакансиям города Санкт-Петербург
    "per_page": 10,  # Кол-во вакансий на 1 странице
}


class HHParser:
    def __init__(self):
        self.base_url = "https://hh.ru/search/vacancy"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 \
                                        Safari/537.36",
            "accept": "*/*",
        }

    def run(self):
        asyncio.run(self.get_channels())

    async def __get_response(self, session, channel):
        async with session.get(
            self.base_url + f"?area={channel.city_id}&text={channel.filter}&page=1"
        ) as response:
            await self.__parse(await response.text(), channel.channel_id)

    @staticmethod
    async def __parse(text, channel_id):
        soup = BeautifulSoup(text, "html5lib")
        vacancies_div = soup.find_all("div", class_="vacancy-serp-item__layout")
        for vacancy_div in vacancies_div:
            vacancy = models.Vacancy(
                vacancy_id=vacancy_div.find("a", attrs={"data-qa": "vacancy-serp__vacancy-title"})[
                    "href"
                ]
                .split(
                    "/",
                )[4]
                .split("?")[0],
                channel_id=channel_id,
                title=vacancy_div.find(
                    "a", attrs={"data-qa": "vacancy-serp__vacancy-title"}
                ).__str__(),
                company=HHParser._fix_href_companies(
                    vacancy_div.find("a", attrs={"data-qa": "vacancy-serp__vacancy-employer"})
                ),
                description=HHParser._union_description(vacancy_div),
                salary=HHParser._get_or_none(
                    vacancy_div.find(
                        "span",
                        attrs={"data-qa": "vacancy-serp__vacancy-compensation"},
                    )
                ),
            )
            await database.add_to_db(vacancy)

    async def get_channels(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for channel in await database.get_channels():
                tasks.append(asyncio.create_task(self.__get_response(session, channel)))
            await asyncio.gather(*tasks)

    @staticmethod
    def _get_or_none(tag: Tag):
        if tag is not None:
            return tag.text
        return ""

    @staticmethod
    def _fix_href_companies(tag: Tag):
        if tag is not None:
            href = "https://spb.hh.ru" + tag["href"]
            name = tag.text
            return f"<a href='{href}'>{name}</a>"
        return None

    @staticmethod
    def _union_description(vacancy_div: Tag):
        work_responsibilities = HHParser._get_or_none(
            vacancy_div.find(
                "div",
                attrs={"data-qa": "vacancy-serp__vacancy_snippet_responsibility"},
            )
        )
        work_requirements = HHParser._get_or_none(
            vacancy_div.find(
                "div",
                attrs={"data-qa": "vacancy-serp__vacancy_snippet_requirement"},
            )
        )

        if work_responsibilities and work_requirements:
            return f"{work_responsibilities} \n\n{work_requirements}"
        elif work_responsibilities and not work_requirements:
            return f"{work_responsibilities}"
        elif not work_responsibilities and work_requirements:
            return f"{work_requirements}"
        else:
            return ""


parser = HHParser()
