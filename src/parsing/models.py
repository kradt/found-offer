import datetime
from pydantic import BaseModel


class OfferModel(BaseModel):
    """
    Модель Вакансії
    """
    title: str
    city: str | None
    salary_from: float | None
    salary_to: float | None
    company: str
    description: str
    link: str
    time_publish: datetime.datetime | None
