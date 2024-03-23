import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.ipAddressRoutes import ipAddressRoutes
from routes.deviceRoutes import deviceRoutes
from routes.systemRoutes import systemRoutes
from routes.shelfRoutes import shelfRoutes
from routes.cardRoutes import cardRoutes
from routes.portRoutes import portRoutes
from routes.vlanNetRoutes import vlanNetRoutes
from routes.vlanMytvRoutes import vlanMytvRoutes
from routes.onuRoutes import onuRoutes
from routes.vlanImsRoutes import vlanImsRoutes

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# sử dụng router
app.include_router(ipAddressRoutes)
app.include_router(deviceRoutes)
app.include_router(systemRoutes)
app.include_router(shelfRoutes)
app.include_router(cardRoutes)
app.include_router(portRoutes)
app.include_router(vlanNetRoutes)
app.include_router(vlanMytvRoutes)
app.include_router(onuRoutes)
app.include_router(vlanImsRoutes)

# chỉ định cho server chạy trên cổng nào    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv('PORT')))
