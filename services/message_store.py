from sqlalchemy.orm import Session
from typing import Dict, List
from database.models import Message


class MessageStore:
    
    def add_message(self, db: Session, room_id: int, message: Dict):
        message = Message(room_id=room_id, username=message["username"], type=message["type"], content=message["text"])
        db.add(message)
        db.commit()
                    
    def get_messages(self, db: Session, room_id: int, limit: int = 50):
        messages = db.query(Message).filter(Message.room_id == room_id).order_by(Message.created_at.desc()).limit(limit).all()
        history = []
        for message in messages:
            msg = {"type": message.type, "username": message.username, "text": message.content}
            history.append(msg)
            
        return history
    
    def delete_room(self, db: Session, room_id: int):
        messages = db.query(Message).filter(Message.room_id == room_id).all()
        for message in messages:
            db.delete(message)
        db.commit()


message_store = MessageStore()