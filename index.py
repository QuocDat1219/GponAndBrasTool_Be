import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from routes.ipAddressRoutes import ipAddressRoutes
from routes.shelfRoutes import shelfRoutes
from routes.vlanNetRoutes import vlanNetRoutes
from routes.vlanMytvRoutes import vlanMytvRoutes
from routes.vlanImsRoutes import vlanImsRoutes
from routes.thietbiRoutes import thietbiRoutes
from routes.controlDeviceRoutes import controlDeviceRoutes
from routes.userRoutes import userRoutes
from routes.visaRoutes import visaRoutes
from routes.ctsRoutes import ctsRouter
from routes.googleSheetsRoutes import googleSheetRouter
from routes.controlManyGponRoutes import controlManyGponRouter
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ipAddressRoutes)
app.include_router(shelfRoutes)
app.include_router(thietbiRoutes)
app.include_router(vlanNetRoutes)
app.include_router(vlanMytvRoutes)
app.include_router(vlanImsRoutes)
app.include_router(controlDeviceRoutes)
app.include_router(userRoutes)
app.include_router(visaRoutes)
app.include_router(ctsRouter)
app.include_router(googleSheetRouter)
app.include_router(controlManyGponRouter)

# Tạo SocketManager
manager = SocketManager(app)

#Xác định xử lý các xự kiện
@manager.on("connect")
async def connect(sid, environ):
    print(f"Client {sid} connected")

@manager.on("disconnect")
async def disconnect(sid):
    print(f"Client {sid} disconnected")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('PORT')), reload=True)

