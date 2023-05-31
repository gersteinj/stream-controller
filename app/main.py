from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json

from . import crud, models, schemas
from .database import SessionLocal, engine
from .myEnums import Weights

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print('New connection')
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
    
    async def event_broadcast(self, event_type, event_data):
        msg_json = {'event_type': event_type, 'data': event_data }
        for connection in self.active_connections:
            await connection.send_json(msg_json)

manager = ConnectionManager()

@app.get('/robots/', response_model=list[schemas.Robot])
def read_robots(skip: int=0, limit: int=500, db: Session = Depends(get_db)):
    robots = crud.get_robots(db=db, skip=skip, limit=limit)
    return robots

@app.get('/robots/{weight}', response_model=list[schemas.Robot])
def read_robots_by_weight(weight: Weights, db: Session = Depends(get_db)):
    robots = crud.get_robots_by_weight(db=db, weight=weight)
    return robots

@app.post('/robots/', response_model=schemas.RobotIn)
def create_robot(robot: schemas.RobotIn, db: Session = Depends(get_db)):
    # db_robot = crud.get_robot_by_display_name(db, display_name=robot.display_name)
    # if db_robot:
    #     raise HTTPException(status_code=400, detail="Name already used!")
    db_robot = crud.create_robot(db=db, robot_in=robot)
    
    return db_robot

@app.get('/robots/id/{robot_id}', response_model=schemas.Robot)
def read_robot_by_id(robot_id: int, db: Session = Depends(get_db)):
    db_robot = crud.get_robot_by_id(db=db, robot_id=robot_id)
    if db_robot is None:
        raise HTTPException(status_code=404, detail=f"Couldnt't find robot {robot_id}.")
    return db_robot

@app.get('/weight/')
def read_weights():
    return [weight for weight in Weights]

@app.get('/matches/', response_model=list[schemas.Match])
def read_matches(db: Session = Depends(get_db)):
    return crud.get_matches(db=db)

@app.post('/matches/', response_model=schemas.MatchIn)
async def create_match(match_in: schemas.MatchIn, db: Session = Depends(get_db)):
    db_match = crud.create_match(db=db, match_in=match_in)
    print(db_match.id)
    
    await manager.event_broadcast('new_match', db_match.id)
    return db_match

# @app.get('/matches/latest', response_model=schemas.Match)
# def get_latest_match(db: Session = Depends(get_db)):
#     db_match = crud.get_latest_match(db=db)
#     return db_match

@app.get('/matches/latest', response_model=int)
def get_latest_match(db: Session = Depends(get_db)):
    db_match = crud.get_latest_match(db=db)
    return db_match.id

@app.get('/matches/{match_id}/', response_model=schemas.Match)
def get_match_by_id(match_id: int, db: Session = Depends(get_db)):
    db_match = crud.get_match_by_id(db=db, match_id=match_id)
    return db_match

@app.get('/matches/{match_id}/detail', response_model=schemas.MatchDetail)
def get_match_details(match_id: int, db: Session = Depends(get_db)):
    db_match = crud.get_match_by_id(db=db, match_id=match_id)
    red_robot = crud.get_robot_by_id(db, db_match.red_id)
    blue_robot = crud.get_robot_by_id(db, db_match.blue_id)
    return schemas.MatchDetail(id=db_match.id, weight=db_match.weight, result=db_match.result, red_robot=red_robot,blue_robot=blue_robot)
    


@app.websocket('/ws/{purpose}')
async def websocket_endpoint(purpose: str | None, websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f'You wrote: {data}', websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast('Somebody disconnected')

@app.get('/', response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/view/controls', response_class=HTMLResponse)
def control_panel_view(request: Request):
    return templates.TemplateResponse('control-panel.html', {'request': request, 'title': 'Control Panel'})

@app.get('/view/robots', response_class=HTMLResponse)
def all_robots_view(request: Request):
    return templates.TemplateResponse('view-robots.html', {'request': request, 'title': 'View Robots'})

@app.get('/view/create', response_class=HTMLResponse)
def create_robot_view(request: Request):
    return templates.TemplateResponse('create-robot.html', {'request': request, 'title': 'Create a Robot'})

@app.get('/view/display', response_class=HTMLResponse)
def display_view(request: Request):
    return templates.TemplateResponse('display-test.html', {'request': request, 'title': 'Test Display'})
