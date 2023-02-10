from datetime import datetime
from ..core.database import Base
from sqlalchemy import Column, Integer, SmallInteger, DateTime, Float, String


class Calculator(Base):
    __tablename__ = 'calculate'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    periods = Column(SmallInteger)
    amount = Column(Integer)
    rate = Column(Float)
    month_profit = Column(Float)
    final_profit = Column(Float)
    date_of_use = Column(DateTime, default=datetime.now)
