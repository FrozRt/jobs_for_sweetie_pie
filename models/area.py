from pydantic import BaseModel


class Area(BaseModel):
    area_id: int
    title: str
