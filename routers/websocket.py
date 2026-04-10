from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import Dict, List
from database.session import get_db
from database.models import User, Message, Room
from services.message_store import message_store
from services.auth import get_current_user
from services.ai_service import get_ai_response


class Connection:
    def __init__(self, websocket: WebSocket, username: str):
        self.websocket: WebSocket = websocket
        self.username: str = username

class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[int, List[Connection]] = {}
        
    async def connect(self, room_id: int, websocket: WebSocket, username: str):
        await websocket.accept()
        connection = Connection(websocket=websocket, username=username)
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(connection)
    
    def disconnect(self, room_id: int, websocket: WebSocket):
        for connection in list(self.rooms[room_id]):
            if connection.websocket == websocket:
                self.rooms[room_id].remove(connection)
                break
            
        if not self.rooms[room_id]:
            del self.rooms[room_id]
        
    async def broadcast(self, room_id: int, message: str):
        if room_id not in self.rooms:
            return
        for connection in list(self.rooms[room_id]):
            try:
                await connection.websocket.send_text(message)
            except:
                self.disconnect(room_id, connection.websocket)
        
        
    async def send_message(self, room_id: int, websocket: WebSocket, message: str):
        if room_id not in self.rooms:
            return
        
        sender = "Unknown"
        
        for connection in self.rooms[room_id]:
            if connection.websocket == websocket:
                sender = connection.username
                break
        
        for connection in list(self.rooms[room_id]):
            try:
                if connection.websocket == websocket:
                    await connection.websocket.send_text(f"You: {message}")
                else:
                    await connection.websocket.send_text(f"{sender}: {message}")
            except:
                self.disconnect(room_id, connection.websocket)
                
    def check_room(self, room_id):
        if room_id not in self.rooms:
            return False
        return True
    
    def show_activate_connections(self, room_id):
        return [conn.username for conn in self.rooms[room_id]]
                
websocket_manager = ConnectionManager()

router = APIRouter(tags=["Websocket"])

@router.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, db: Session = Depends(get_db)):
    token = websocket.query_params.get("token")
    user = get_current_user(token)
    username = user.get("username")
    room_id = user.get("room_id")
    await websocket_manager.connect(room_id=room_id, websocket=websocket, username=username)
    history = message_store.get_messages(db=db, room_id=room_id)
    await websocket.send_json({"type": "history", "history": history})
    await websocket_manager.broadcast(room_id=room_id, message=f"{username} joined")
    message_store.add_message(db=db, room_id=room_id, message={"type": "join", "username": username, "text": "joined"})
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                import json
                data = json.loads(data)
            except:
                data = {"type": "chat", "message": data}
            if data["type"] == "chat":
                await websocket_manager.send_message(room_id=room_id, websocket=websocket, message=data["message"])
                message_store.add_message(db=db, room_id=room_id, message={"type": "message", "username": username, "text": data["message"]})
                if "/ai" in data["message"]:
                    query = data["message"].split("/ai")[1]
                    ai_response = await get_ai_response(query)
                    await websocket_manager.broadcast(
                        room_id,
                        f"🤖 AI: {ai_response}"
                    )
                    message_store.add_message(db=db, room_id=room_id, message={"type": "message", "username": "🤖 AI", "text": ai_response})
                    
            else:
                num_users = websocket_manager.show_activate_connections(room_id=room_id)
                await websocket.send_json({"type": "online_users", "users": num_users})
    except WebSocketDisconnect:
        websocket_manager.disconnect(room_id=room_id, websocket=websocket)
        db.query(User).filter(User.room_id == room_id).delete()
        await websocket_manager.broadcast(room_id=room_id, message=f"{username} left")
        message_store.add_message(db=db, room_id=room_id, message={"type": "left", "username": username, "text": "left"})
        room_exists = websocket_manager.check_room(room_id)
        if not room_exists:
            db.query(Message).filter(Message.room_id == room_id).delete(synchronize_session=False)
            db.query(User).filter(User.room_id == room_id).delete(synchronize_session=False)
            db.query(Room).filter(Room.id == room_id).delete(synchronize_session=False)
            db.commit()