from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette import status

import database
import models
import schemas
from fastapi import APIRouter
from database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=schemas.CreatePost)
async def get_random_post(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM posts ORDER BY RANDOM() LIMIT 1")).fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Couldn't retrieve data"
            )
        return result
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get('/all', response_model=List[schemas.CreatePost])
async def get_posts(db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).all()
        return post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreatePost)
async def post_post(post_posts: schemas.CreatePost, db: Session = Depends(get_db)):
    try:
        new_post = models.Post(**post_posts.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.get('/{id_post}', response_model=schemas.CreatePost, status_code=status.HTTP_200_OK)
def gest_post_by_id(id_post: int, db: Session = Depends(get_db)):
    try:
        idv_post = db.query(models.Post).filter(models.Post.id_post == id_post).first()
        if idv_post is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_post} you requested for does not exist")
        return idv_post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )

##TODO fix this
@router.delete('/{id_post}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id_post: int, db: Session = Depends(get_db)):
    try:
        deleted_post = db.query(models.Post).filter(models.Post.id_post == id_post)
        if deleted_post.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_post} you requested for does not exist")
        deleted_post.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"Deleted")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.put('/{id_post}', response_model=schemas.CreatePost)
def update_post(upd_post: schemas.PostBase, id_post: int, db: Session = Depends(get_db)):
    try:
        updated_post = db.query(models.Post).filter(models.Post.id_post == id_post)
        if updated_post.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
        updated_post.update(upd_post.dict(), synchronize_session=False)
        db.commit()
        return updated_post.first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )
