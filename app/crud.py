from sqlalchemy.orm import Session
from . import models, schemas
from .myEnums import Weights


###############################################
#                                             #
#            Get Individual Robot             #
#                                             #
###############################################

def get_robot_by_id(db: Session, robot_id: int):
    return db.query(models.Robot).filter(models.Robot.id == robot_id).first()

def get_robot_by_name(db: Session, robot_name: str):
    print(f'Checking to see if {robot_name} exists')
    return db.query(models.Robot).filter(models.Robot.robot_name == robot_name).first()


###############################################
#                                             #
#             Get List of Robots              #
#                                             #
###############################################

def get_robots(db: Session, skip: int=0, limit: int=500):
    return db.query(models.Robot).offset(skip).limit(limit).all()

def get_robots_by_weight(db: Session, weight: Weights):
    return db.query(models.Robot).filter(models.Robot.weight == weight).all()

###############################################
#                                             #
#                Create Robot                 #
#                                             #
###############################################

def create_robot(db: Session, robot_in: schemas.RobotIn):
    db_robot = models.Robot(**robot_in.dict())
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot

###############################################
#                                             #
#                   Matches                   #
#                                             #
###############################################

def create_match(db: Session, match_in: schemas.MatchIn):
    db_match = models.Match(**match_in.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def get_matches(db: Session):
    return db.query(models.Match).all()

def get_latest_match(db: Session):
    return db.query(models.Match).order_by(models.Match.id.desc()).first()

def get_match_by_id(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()

# def get_match_details(db: Session, match_id: int):
#     db_match = get_match_by_id(db, match_id=match_id)
#     red_robot = get_robot_by_id(db, match.red_id)
#     blue_robot = get_robot_by_id(db, match.blue_id)
#     return