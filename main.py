from fastapi import FastAPI
import models
import database
import schemas
import images
import posts
import tags

app = FastAPI()
app.include_router(tags.router)
app.include_router(images.router)
app.include_router(posts.router)
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def main():
    return {"message": "Hello world"}

