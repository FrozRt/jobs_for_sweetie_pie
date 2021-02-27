import re
from dateutil.parser import parse
from datetime import datetime, timedelta


from core.loader import bot
from settings.config import settings
import asyncio
from aiohttp import ClientSession


# def write_data(settings):
#     global count
#     with open('data_from_hh.csv', 'a') as file:
#         order = ['date', 'title', 'cost', 'company', 'url', 'responsibility', 'requirement']
#         writer = csv.DictWriter(
#             file, fieldnames=order, delimiter=';',
#             quoting=csv.QUOTE_NONNUMERIC)
#         writer.writerow(settings)
#     count += 1


async def get_vacancy():
    url = 'https://api.hh.ru/vacancies'
    tasks = []
    async with ClientSession() as session:
        for page in range(10):
            task = asyncio.create_task(get_response(url, session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)
    # await session.connector.close()


async def get_response(url, session, page=None):
    if page is not None:
        params['page'] = page
    async with session.get(url, params=params, headers=headers) as response:
        data = await response.json()
        if page is None:
            return data
        await get_page(data)


async def get_page(data):
    jobs = []
    for item in data['items']:
        if parse(item['published_at'], ignoretz=True) < (datetime.now() - timedelta(days=1)):
            continue

        name = item['name']
        if item['snippet']['requirement'] and item['snippet']['responsibility']:
            dirty_description = item['snippet']['requirement'] + '\n' + item['snippet']['responsibility']
        else:
            dirty_description = ''
        description = re.sub('<[^<]+?>', '', dirty_description)
        url = item['alternate_url']
        job_item = f'{name}\n{description}\n{url}'
        jobs.append(job_item)

    await bot.send_message(chat_id=settings.CHANNEL, text=jobs, parse_mode="HTML")


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 \
                                        Safari/537.36', 'accept': '*/*'
               }
    params = {
        'name': '3d artist',
        'area': 2,  # Поиск ощуществляется по вакансиям города Санкт-Петербург
        'per_page': 10  # Кол-во вакансий на 1 странице
    }
    asyncio.run(get_vacancy())
