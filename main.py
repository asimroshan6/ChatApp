from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.session import Base, engine
from database.models import Room
from routers import websocket, room


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Anonymous Chat App", description="This is the api for anonymous chat application using fastapi", docs_url=None, redoc_url=None, openapi_url=None)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(websocket.router)
app.include_router(room.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@app.get("/health")
def health_check():
    return {"message": "Healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
    