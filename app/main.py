from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

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
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

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

@app.get('/robots/{weight}', response_model=list[schemas.Robot])
def read_robots_by_weight(weight: Weights, db: Session = Depends(get_db)):
    robots = crud.get_robots_by_weight(db, weight=weight)
    return robots

@app.get('/robots/{robot_id}', response_model=schemas.Robot)
def read_robot(robot_id: int, db: Session = Depends(get_db)):
    db_robot = crud.get_robot(db, robot_id=robot_id)
    if db_robot is None:
        raise HTTPException(status_code=404, detail="Robot Not Found :(")
    return db_robot

@app.get('/weight/')
def read_weights():
    return [weight for weight in Weights]

@app.get('/matches/', response_model=list[schemas.Match])
def read_matches(db: Session = Depends(get_db)):
    return crud.get_matches(db=db)

@app.post('/matches/create', response_model=schemas.Match)
async def create_match(match_in: schemas.MatchIn, db: Session = Depends(get_db)):
    match = crud.create_match(db=db, match_in=match_in)
    await manager.broadcast('refresh')
    return match

@app.get('/matches/latest', response_model=schemas.Match)
def get_latest_match(db: Session = Depends(get_db)):
    return crud.get_latest_match(db=db)

@app.websocket('/ws/{purpose}')
async def websocket_endpoint(purpose: str | None, websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if purpose:
                print(purpose)
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