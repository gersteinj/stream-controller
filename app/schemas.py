from pydantic import BaseModel

from .myEnums import Weights

class RobotIn(BaseModel):
    robot_name: str
    weight: Weights
    
    class Config:
        orm_mode = True

class Robot(RobotIn):
    id: int | None
    
    class Config:
        orm_mode = True

class MatchIn(BaseModel):
    weight: Weights
    red_id: int
    blue_id: int

    class Config:
        orm_mode = True

class Match(MatchIn):
    id: int
    result: str | None

    class Config:
        orm_mode = True
