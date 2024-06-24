from fastapi import FastAPI

from CRUD import post_image, post_tag, posts, images, tags
from Data import database
from Models import models

app = FastAPI()
app.include_router(tags.router)
app.include_router(images.router)
app.include_router(posts.router)
app.include_router(post_tag.router)
app.include_router(post_image.router)
models.Base.metadata.create_all(bind=database.engine)


@app.get("/health")
async def main():
    return {"message": "API is working"}


@app.get("/")
async def main():
    return {"message": "Personal Blog RestAPI"}
