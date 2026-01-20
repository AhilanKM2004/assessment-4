from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.route import router33
from database.db import base, engine
import os

app = FastAPI()
os.makedirs("product_images", exist_ok=True)
app.mount("/product_images", StaticFiles(directory="product_images"), name="product_images")
app.include_router(router33)
base.metadata.create_all(bind=engine)
