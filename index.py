from fastapi import FastAPI
from routes.userRoutes import user
app = FastAPI()
app.include_router(user)
