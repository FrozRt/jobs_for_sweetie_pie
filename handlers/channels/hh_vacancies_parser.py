from time import time

from loader import bot
from data.config import CHANNEL
import asyncio
from aiohttp import ClientSession

# def write_data(data):
#     global count
#     with open('data_from_hh.csv', 'a') as file:
#         order = ['date', 'title', 'cost', 'company', 'url', 'responsibility', 'requirement']
#         writer = csv.DictWriter(
#             file, fieldnames=order, delimiter=';',
#             quoting=csv.QUOTE_NONNUMERIC)
#         writer.writerow(data)
#     count += 1


async def get_vacancy():
    url = 'https://api.hh.ru/vacancies'
    tasks = []
    async with ClientSession() as session:
        for page in range(10):
            task = asyncio.create_task(get_response(url, session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)
    await session.connector.close()


async def get_response(url, session, page=None):
    if page is not None:
        params['page'] = page
    async with session.get(url, params=params, headers=headers) as response:
        data = await response.json()
        if page is None:
            return data
        await get_page(data)


async def get_page(data):
    ids = []
    for item in data['items']:

        ids.append(item['id'])

        await bot.send_message(chat_id=CHANNEL, text=ids, parse_mode="HTML")


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 \
                                        Safari/537.36', 'accept': '*/*'
               }
    params = {
        'text': 'Python',
        'area': 2,  # Поиск ощуществляется по вакансиям города Санкт-Петербург
        'per_page': 100  # Кол-во вакансий на 1 странице
    }
    start_time = time()
    asyncio.run(get_vacancy())
    print(f"Passed {round(time() - start_time, 2)} sec")
