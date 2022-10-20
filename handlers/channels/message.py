import asyncio

import models
from core.db_api.vacancies import database
from core.loader import bot


class Message:
    def run(self):
        asyncio.run(self.send_message())

    async def send_message(self):
        tasks = []
        vacancies = await database.get_new_vacancies()
        if vacancies:
            for vacancy in vacancies:
                task = asyncio.create_task(
                    bot.send_message(vacancy.channel_id, self.handle_message(vacancy))
                )
                tasks.append(task)
            tasks.append(asyncio.create_task(database.update_given_vacancies(vacancies)))
            await asyncio.gather(*tasks)

    @staticmethod
    def handle_message(vacancy: models.Vacancy):
        if vacancy.salary:
            message = (
                f"{vacancy.title}\n"
                f"{vacancy.salary}\n"
                f"\n"
                f"{vacancy.company}\n"
                f"{vacancy.description}"
            )
        else:
            message = f"{vacancy.title}\n" f"\n" f"{vacancy.company}\n" f"{vacancy.description}"
        return message


message_maker = Message()
