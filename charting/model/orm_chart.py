from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Chart(Base):
    __tablename__ = 'chart'
    title = Column(String(255), primary_key=True)
    country = Column(String(255))
    category = Column(String(255))
    path = Column(String(255))
    base64 = Column(Text)
