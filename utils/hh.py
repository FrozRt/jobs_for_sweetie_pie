
import asyncio

import aiohttp


class HH:

    def __init__(self, per_page=None):
        self.per_page = min(per_page or 100, 100)
        self.base_url = f'https://api.hh.ru/vacancies?per_page={self.per_page}'

    def run(self, q):
        data = asyncio.run(self.get_all(q))
        return data

    async def __fetch(self, session, url):
        async with session.get(url) as response:
            return await response.json()

    async def get_all(self, query):
        urls = []
        tasks = []
        async with aiohttp.ClientSession() as session:
            json_data = await self.__fetch(session, self.base_url+f'&text={query}')
            pages = json_data.get('pages')
            pages = [i+1 for i in range(pages-1)]
            for i in pages:
                urls.append(self.base_url+f'&text={query}&page={i}')
            for url in urls:
                tasks.append(self.__fetch(session, url))
            vacs = await asyncio.gather(*tasks)
            result = self.__process_data(vacs)
            data = self.__process_items(result)
            return data

    @staticmethod
    def __process_data(vacs):
        result = []
        for page in vacs:
            result += page['items']
        return result

    @staticmethod
    def __process_items(result):
        data = []
        for vac in result:
            data.append({
                'title': vac['name'],
                'description': vac['snippet']['requirement'],
                'salary': vac.get('salary', {}),
                'company': vac['employer']['name'],
                'source': 'hh',
                'source_internal_id': vac['id'],
                'link': vac['alternate_url']
            })
        return data


HHParser = HH()
