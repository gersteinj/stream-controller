from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base
from .myEnums import Weights


class Robot(Base):
    __tablename__ = 'robots'

    id = Column(Integer, primary_key=True, index=True)
    robot_name = Column(String)
    weight = Column(Enum(Weights))

    __table_args__ = (
        UniqueConstraint('robot_name', 'weight'),
    )

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Enum(Weights))
    red_id = Column(Integer, ForeignKey('robots.id'))
    blue_id = Column(Integer, ForeignKey('robots.id'))
    result = Column(String, nullable=True)