from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.post('/robots/', response_model=schemas.Robot)
def create_robot(robot: schemas.Robot, db: Session = Depends(get_db)):
    db_robot = crud.get_robot_by_display_name(db, display_name=robot.display_name)
    if db_robot:
        raise HTTPException(status_code=400, detail="Name already used!")
    return crud.create_robot(db=db, robot=robot)

@app.get('/robots/', response_model=list[schemas.Robot])
def read_robots(skip: int=0, limit: int=50, db: Session = Depends(get_db)):
    robots = crud.get_robots(db, skip=skip, limit=limit)
    return robots

@app.get('/robots/{robot_id}', response_model=schemas.Robot)
def read_robot(robot_id: int, db: Session = Depends(get_db)):
    db_robot = crud.get_robot(db, robot_id=robot_id)
    if db_robot is None:
        raise HTTPException(status_code=404, detail="Robot Not Found :(")
    return db_robot

@app.get('/wc/{weight_class}')
def read_weight_class(weight_class: str, db: Session = Depends(get_db)):
    robots = crud.get_robots_by_weight_class(db, weight_class=weight_class)
    return robots

@app.get('/')
def homepage():
    print('get request reached the home page')
    return 'Hello'