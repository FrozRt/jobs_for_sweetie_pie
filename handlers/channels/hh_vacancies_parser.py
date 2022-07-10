import asyncio

import aiohttp
from bs4 import BeautifulSoup, Tag

if __name__ == "__main__":
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
    def __init__(self, query: dict):
        self.base_url = "https://hh.ru/search/vacancy"
        self.query = f"?{'&'.join(f'{k}={v}' for k, v in query.items())}"
        self.url = self.base_url + self.query
        self.success_status = 200

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 \
                                        Safari/537.36",
            "accept": "*/*",
        }

    def run(self):
        data = asyncio.run(self.get_data())
        return data

    async def __get_soup(self, session: aiohttp.ClientSession, page_num=None) -> BeautifulSoup:
        async with session.get(self.url + f"&page={page_num}", headers=self.headers) as response:
            text = await response.text(encoding="utf-8")
        return BeautifulSoup(text, "html5lib")

    async def get_data(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            soup = await self.__get_soup(session)
            pages = int(soup.find_all("span", {"class": "pager-item-not-in-short-range"})[-1].text)

            for i in range(pages):
                tasks.append(self.__get_soup(session, i))

            soups = await asyncio.gather(*tasks)
            return self.__parse(soups)

    def __parse(self, soups):
        data = []
        for soup in soups:
            vacancies_div = soup.find_all("div", class_="vacancy-serp-item__layout")
            for vacancy_div in vacancies_div:
                data.append(
                    {
                        "link_title": vacancy_div.find(
                            "a", attrs={"data-qa": "vacancy-serp__vacancy-title"}
                        ),
                        "salary": self.__get_or_none(
                            vacancy_div.find(
                                "span",
                                attrs={"data-qa": "vacancy-serp__vacancy-compensation"},
                            )
                        ),
                        "company_link_title": self.__fix_href_companies(
                            vacancy_div.find(
                                "a", attrs={"data-qa": "vacancy-serp__vacancy-employer"}
                            )
                        ),
                        "company_location": vacancy_div.find(
                            "div", attrs={"data-qa": "vacancy-serp__vacancy-address"}
                        ).text,
                        "work_responsibilities": self.__get_or_none(
                            vacancy_div.find(
                                "div",
                                attrs={"data-qa": "vacancy-serp__vacancy_snippet_responsibility"},
                            )
                        ),
                        "work_requirements": self.__get_or_none(
                            vacancy_div.find(
                                "div",
                                attrs={"data-qa": "vacancy-serp__vacancy_snippet_requirement"},
                            )
                        ),
                    }
                )
        return data

    @staticmethod
    def __get_or_none(tag: Tag):
        if tag is not None:
            return tag.text
        return "Не указано"

    @staticmethod
    def __fix_href_companies(tag: Tag):
        if tag is not None:
            href = "https://spb.hh.ru" + tag["href"]
            name = tag.text
            return f"<a href='{href}'>{name}</a>"
        return "Не указано"


parser = HHParser(
    {
        "text": "backend developer",
        "area": 2,
    }
)
