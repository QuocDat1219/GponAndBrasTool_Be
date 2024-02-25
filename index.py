import uvicorn
import os

from fastapi import FastAPI
from routes.userRoutes import user

app = FastAPI()

# sử dụng router
app.include_router(user)\

# chỉ định cho server chạy trên cổng nào    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv('PORT')))
