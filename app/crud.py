from sqlalchemy.orm import Session
from . import models, schemas
from .myEnums import Weights

###############################################
#                                             #
#              Utility Functions              #
#                                             #
###############################################

def convert_name(display_name: str):
    return display_name.replace(' ','-').lower()

###############################################
#                                             #
#            Get Individual Robot             #
#                                             #
###############################################

def get_robot(db: Session, robot_id: int):
    return db.query(models.Robot).filter(models.Robot.id == robot_id).first()

def get_robot_by_display_name(db: Session, display_name: str):
    converted_name = convert_name(display_name)
    print(f'Checking to see if {converted_name} already exists')
    return db.query(models.Robot).filter(models.Robot.name == converted_name).first()

def get_robot_by_name(db: Session, name: str):
    return db.query(models.Robot).filter(models.Robot.name == name).first()

###############################################
#                                             #
#             Get List of Robots              #
#                                             #
###############################################

def get_robots(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Robot).offset(skip).limit(limit).all()

def get_robots_by_weight(db: Session, weight: Weights):
    return db.query(models.Robot).filter(models.Robot.weight == weight).all()

###############################################
#                                             #
#                Create Robot                 #
#                                             #
###############################################

def create_robot(db: Session, robot: schemas.Robot):
    db_robot = models.Robot(display_name=robot.display_name, weight=robot.weight, name=convert_name(robot.display_name))
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot

###############################################
#                                             #
#                Create Match                 #
#                                             #
###############################################

def create_match(db: Session, match_in: schemas.MatchIn):
    match = schemas.Match(weight=match_in.weight, blue_bot=get_robot_by_name(db=db, name=match_in.blue_bot), red_bot = get_robot_by_name(db=db, name=match_in.red_bot))
    return match