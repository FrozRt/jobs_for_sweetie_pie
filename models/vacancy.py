from typing import Optional

from pydantic import BaseModel


class Vacancy(BaseModel):
    vacancy_id: int
    channel_id: int
    title: str
    description: Optional[str]
    salary: Optional[str]
    company: str


class Channel(BaseModel):
    channel_id: int
    city_id: int
    filter: str
