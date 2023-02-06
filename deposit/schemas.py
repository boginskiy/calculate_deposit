from pydantic import BaseModel, validator, Field
import datetime


class DataCalculate_IN(BaseModel):
    date: str = Field(...,
                      description="Дата заявки")
    periods: int = Field(...,
                         ge=1, le=60,
                         description="Количество месяцев по вкладу")
    amount: int = Field(...,
                        ge=10_000, le=3_000_000,
                        description="Сумма вклада")
    rate: float = Field(...,
                        ge=1, le=8, description="Процент по вкладу")

    @validator("date")
    def check_date(cls, values):
        return datetime.datetime.strptime(values, "%d.%m.%Y").date()

    @validator("rate")
    def check_rate(cls, values):
        return values / 100
