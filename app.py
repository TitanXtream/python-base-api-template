from fastapi import FastAPI,HTTPException,Request,Depends
import socketio
from contextlib import asynccontextmanager
import uvicorn
import os

from services import UserService
from repos.user_repo import UserRepo
from utils.app_state import AppState
from typing import cast

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("-- Intitialising App resources --")
        
        app_state = cast(AppState,app.state)
        
        app_state.user_service = UserService(UserRepo())
        
        print("-- Initialization successfull --")
        
        yield # Application runs here
    except Exception as e:
        print("Lifespan Error: " + str(e))
        raise HTTPException(500,"Something went wrong please try again later")
    finally: 
        print("-- Terminating app --")
        print("-- Termination successful --")


# Create FastAPI and Socket.IO ASGI app
app = FastAPI(lifespan=lifespan)
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "FastAPI + SocketIO Server Running"}

def get_user_service(request:Request):
    return cast(AppState,request.app.state).user_service

# Example HTTP route
@app.get("/users")
def get_users(user_service:UserService = Depends(get_user_service)):
    
    return {"result": user_service.get_user_profile("u1")}


# Socket.IO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("message", "Welcome!", to=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")



if __name__ == "__main__":
    # Run the app
    port = int(os.environ.get("PORT", 10000))  # fallback for local dev
    is_dev = os.environ.get("ENV", "development") == "development"
    
    uvicorn.run(
        "app:socket_app", 
        host="0.0.0.0", 
        port=port, 
        reload=is_dev
    )
    
