from time import sleep

from celery import current_task
from celery.schedules import crontab
from loguru import logger

from core.celery_app import celery_app
from handlers.channels.hh_vacancies_parser import parser
from handlers.channels.message import message_maker


@celery_app.task(acks_late=True)
def test_data_celery(word: str) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state="PROGRESS", meta={"process_percent": i * 10})
    return f"test task return {word}"


@celery_app.task(name="parser")
def parse_vacancies_into_db():
    parser.run()
    logger.success("Parser started...")


@celery_app.task(name="sender")
def send_vacancies_into_channels():
    message_maker.run()
    logger.success("Send messages in channels...")


celery_app.conf.beat_schedule = {
    "run_parser_worker": {"task": "parser", "schedule": crontab(minute="*/3")},
    "run_message_maker": {"task": "sender", "schedule": crontab(minute="*/5")},
}
