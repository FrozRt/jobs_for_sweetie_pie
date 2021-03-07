from datetime import datetime

from pydantic import BaseModel


class Vacancy(BaseModel):
    vacancy_id: int
    title: str
    description: str
    salary: float
    company: str
    uri: str

    created_at: datetime
