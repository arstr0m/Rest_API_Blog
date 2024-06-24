from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text, and_
from sqlalchemy.orm import Session
from starlette import status

from Data.database import get_db
from Models import models
from Schemas import schemas

router = APIRouter(
    prefix='/post_images',
    tags=['PostImages']
)


@router.get('/', response_model=schemas.CreatePostImage)
async def get_random_post_image(db: Session = Depends(get_db)):
    try:

        result = db.execute(text("SELECT * FROM post_image ORDER BY RANDOM() LIMIT 1")).fetchone()
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


@router.get('/all', response_model=List[schemas.CreatePostImage])
async def get_all_post_images(db: Session = Depends(get_db)):
    try:
        post_image = db.query(models.PostImage).all()
        return post_image
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


# it was removed List cast from response model

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreatePostImage)
async def post_images(post_image: schemas.CreatePostImage, db: Session = Depends(get_db)):
    try:
        new_post_image = models.PostImage(**post_image.dict())
        db.add(new_post_image)
        print(new_post_image)
        db.commit()
        db.refresh(new_post_image)

        return jsonable_encoder(new_post_image)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get('/{post_id}/{image_id}', response_model=schemas.CreatePostImage, status_code=status.HTTP_200_OK)
def get_post_image_by_ids(image_id: int, post_id: int, db: Session = Depends(get_db)):
    try:
        idv_post_image = db.query(models.PostImage).filter(
            and_(models.PostImage.image_id == image_id, models.PostImage.post_id == post_id)).first()
        if idv_post_image is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {image_id} you requested for does not exist")
        return idv_post_image
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.delete('/{post_id}/{image_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_image(image_id: int, post_id: int, db: Session = Depends(get_db)):
    try:
        deleted_post_image = db.query(models.PostImage).filter(
            and_(models.PostImage.image_id == image_id, models.PostImage.post_id == post_id))
        if deleted_post_image.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The image_id: {image_id} and id post{post_id} you requested for does not exist")
        deleted_post_image.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.put('/{post_id}/{image_id}', response_model=schemas.CreatePostImage)
def update_post_image(
        upd_image: schemas.PostImageBase,
        image_id: int,
        post_id: int,
        db: Session = Depends(get_db)
):
    try:
        updated_post_image = db.query(models.PostImage).filter(
            and_(
                models.PostImage.image_id == image_id,
                models.PostImage.post_id == post_id
            )
        )
        if updated_post_image is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The image with id {image_id} and post id {post_id} does not exist"
            )
        db.query(models.PostImage).filter(
            and_(
                models.PostImage.image_id == image_id,
                models.PostImage.post_id == post_id
            )
        ).update(
            {
                **upd_image.dict(),
                "added_at": text("now()")
            },
            synchronize_session=False
        )
        db.commit()
        updated_post_image = db.query(models.PostImage).filter(
            and_(
                models.PostImage.image_id == image_id,
                models.PostImage.post_id == post_id
            )
        ).first()

        return jsonable_encoder(updated_post_image)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
