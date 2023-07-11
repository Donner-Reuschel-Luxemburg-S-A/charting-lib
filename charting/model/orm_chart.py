from sqlalchemy import Column, String, Integer, Text, Date, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Chart(Base):
    __tablename__ = 'chart'
    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    last_update = Column(DateTime)
    path = Column(String(255))
    start = Column(Date)
    end = Column(Date)
    country = Column(String(255))
    category = Column(String(255))
    base64 = Column(Text(64000))

