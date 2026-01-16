from fastapi import FastAPI
from routes.route import router33
from database.db import base, engine
import os

app = FastAPI()
app.include_router(router33)
base.metadata.create_all(bind=engine)


