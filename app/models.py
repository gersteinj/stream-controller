from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from .database import Base
from .myEnums import Weights


class Robot(Base):
    __tablename__ = 'robots'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    weight = Column(Enum(Weights))

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Enum(Weights))
    red_bot = Column(Integer, ForeignKey('robots.id'))
    blue_bot = Column(Integer, ForeignKey('robots.id'))