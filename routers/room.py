from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
from services.schemas import RoomRequest
from services.auth import hash_password, verify_password, create_access_token
from database.models import Room, User, Message
from database.session import get_db
from routers.websocket import websocket_manager


router = APIRouter(tags=["Room"])
templates = Jinja2Templates(directory="templates")



@router.get("/chat")
def chat(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")

@router.get("/create-room", name="create-room")
def create_room(request: Request):
    return templates.TemplateResponse(request=request, name="create-room.html")

@router.post("/create-room")
def create_room(room_body: RoomRequest, db: Session=Depends(get_db)):
    
    dupe_room = db.query(Room).filter(Room.room_name == room_body.room_name).first()
    if dupe_room:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="room already exists")
    
    room = Room(room_name=room_body.room_name, hashed_password=hash_password(room_body.password))
    db.add(room)
    db.flush()
    
    dupe_user = db.query(User).filter(User.username == room_body.username, User.room_id == room.id).first()
    if dupe_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")

    user = User(username=room_body.username, room_id=room.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token(user.username, room.id, room_body.password, timedelta(minutes=20))
    
    return {"room_name": room.room_name, "user_id": user.id, "username": user.username, "room_id": room.id, "token": token}

@router.post("/join-room")
def join_room(room_body: RoomRequest, db: Session=Depends(get_db)):
    room = db.query(Room).filter(Room.room_name == room_body.room_name).first()
    if not room or not verify_password(room_body.password, room.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="room not found")
    room_exists = websocket_manager.check_room(room.id)
    if not room_exists:
        db.query(Message).filter(Message.room_id == room.id).delete(synchronize_session=False)
        db.query(User).filter(User.room_id == room.id).delete(synchronize_session=False)
        db.query(Room).filter(Room.id == room.id).delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="room not found")
    
    dupe_user = db.query(User).filter(User.username == room_body.username, User.room_id == room.id).first()
    if dupe_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")

    user = User(username=room_body.username, room_id=room.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token(user.username, room.id, room_body.password, timedelta(hours=24))
    
    return {"room_name": room.room_name, "user_id": user.id, "username": user.username, "room_id": room.id, "token": token}
