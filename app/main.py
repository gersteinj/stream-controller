from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .myEnums import WeightsEnum

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

current_match = None

app.mount('/static', StaticFiles(directory='static', html=True), name='static')

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

@app.get('/weight/')
def read_weights():
    return [weight for weight in WeightsEnum]

@app.get('/weight/{weight}')
def read_robots_by_weight(weight: WeightsEnum, db: Session = Depends(get_db)):
    robots = crud.get_robots_by_weight(db, weight=weight)
    return robots

@app.get('/')
def homepage():
    print('get request reached the home page')
    return 'Hello'

@app.post('/currentmatch', response_model=schemas.Match)
def post_current_match(match_in: schemas.MatchIn, db: Session = Depends(get_db)):
    global current_match
    match = crud.create_match(db=db, match_in=match_in)
    current_match = match
    return match

@app.get('/currentmatch', response_model=schemas.Match)
def read_current_match():
    global current_match
    return current_match

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message text was: {data}')