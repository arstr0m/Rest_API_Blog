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
    prefix='/post_tags',
    tags=['PostTags']
)


@router.get('/', response_model=schemas.CreatePostTag)
async def get_random_post_tag(db: Session = Depends(get_db)):
    try:

        result = db.execute(text("SELECT * FROM post_tag ORDER BY RANDOM() LIMIT 1")).fetchone()
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


@router.get('/all', response_model=List[schemas.CreatePostTag])
async def get_all_post_tags(db: Session = Depends(get_db)):
    try:
        post_tag = db.query(models.PostTag).all()
        return post_tag
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


# it was removed List cast from response model

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreatePostTag)
async def post_tags(post_tag: schemas.CreatePostTag, db: Session = Depends(get_db)):
    try:
        new_post_tag = models.PostTag(**post_tag.dict())
        db.add(new_post_tag)
        print(new_post_tag)
        db.commit()
        db.refresh(new_post_tag)

        return jsonable_encoder(new_post_tag)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get('/{post_id}/{tag_id}', response_model=schemas.CreatePostTag, status_code=status.HTTP_200_OK)
def get_post_tag_by_ids(tag_id: int, post_id: int, db: Session = Depends(get_db)):
    try:
        idv_post_tag = db.query(models.PostTag).filter(
            and_(models.PostTag.tag_id == tag_id, models.PostTag.post_id == post_id)).first()
        if idv_post_tag is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {tag_id} you requested for does not exist")
        return idv_post_tag
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.delete('/{post_id}/{tag_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_tag(tag_id: int, post_id: int, db: Session = Depends(get_db)):
    try:
        deleted_post_tag = db.query(models.PostTag).filter(
            and_(models.PostTag.tag_id == tag_id, models.PostTag.post_id == post_id))
        if deleted_post_tag.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The tag_id: {tag_id} and id post{post_id} you requested for does not exist")
        deleted_post_tag.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.put('/{post_id}/{tag_id}', response_model=schemas.CreatePostTag)
def update_post_tag(
        upd_post_tag: schemas.PostTagBase,
        tag_id: int,
        post_id: int,
        db: Session = Depends(get_db)
):
    try:
        updated_post_tag = db.query(models.PostTag).filter(
            and_(
                models.PostTag.tag_id == tag_id,
                models.PostTag.post_id == post_id
            )
        )
        if updated_post_tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The image with id {tag_id} and post id {post_id} does not exist"
            )
        db.query(models.PostTag).filter(
            and_(
                models.PostTag.tag_id == tag_id,
                models.PostTag.post_id == post_id
            )
        ).update(
            {
                **upd_post_tag.dict(),
                "added_at": text("now()")
            },
            synchronize_session=False
        )
        db.commit()
        updated_post_tag = db.query(models.PostTag).filter(
            and_(
                models.PostTag.tag_id == tag_id,
                models.PostTag.post_id == post_id
            )
        ).first()

        return jsonable_encoder(updated_post_tag)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
