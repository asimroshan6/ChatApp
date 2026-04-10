from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Dict




app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}
    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[websocket] = username
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)
    
    async def send_message(self, websocket: WebSocket, message: str):
        for connection in self.active_connections:
            try:
                if connection == websocket:
                    await connection.send_text(f"You: {message}")
                else:
                    await connection.send_text(f"{self.active_connections[websocket]}: {message}")
            except:
                self.disconnect(connection)
        
    
connection_manager = ConnectionManager()


@app.websocket("/message")
async def websocket_endpoint(websocket: WebSocket):
    username = websocket.query_params.get("username")
    await connection_manager.connect(websocket, username)
    await connection_manager.broadcast(f"{username} joins 🚶")
    
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_message(websocket, data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"{username} left 🚶‍➡️")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

    

@app.get("/chat", name="chat")
async def chat(request: Request):
    return templates.TemplateResponse(name="chat.html", request=request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
    