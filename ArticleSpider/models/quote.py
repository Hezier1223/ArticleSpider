# Created by Max on 2/11/18
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Quote(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    author = Column(String(45))
