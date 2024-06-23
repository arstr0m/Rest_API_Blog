from sqlalchemy import text
from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import models
import schemas
from fastapi import APIRouter
from database import get_db

router = APIRouter(
    prefix='/tags',
    tags=['Tags']
)

##TODO FIX THIS
@router.get('/',response_model=schemas.CreatePost)
async def get_random_tag(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM tag ORDER BY RANDOM() LIMIT 1")).fetchone()
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
            detail="Internal Server Error" + str(e)
        )

@router.get('/all', response_model=List[schemas.CreateTag])
async def get_all_tags(db: Session = Depends(get_db)):
    try:
        tag = db.query(models.Tag).all()
        return tag
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreateTag])
async def post_tags(tag_tag: schemas.CreateTag, db: Session = Depends(get_db)):
    try:
        new_tag = models.Tag(**tag_tag.dict())
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        return [new_tag]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.get('/{id_tag}', response_model=schemas.CreateTag, status_code=status.HTTP_200_OK)
def get_tag_by_id(id_tag: int, db: Session = Depends(get_db)):
    try:
        idv_tag = db.query(models.Tag).filter(models.Tag.id_tag == id_tag).first()
        if idv_tag is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_tag} you requested for does not exist")
        return idv_tag
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.delete('/{id_tag}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(id_tag: int, db: Session = Depends(get_db)):
    try:
        deleted_tag = db.query(models.Tag).filter(models.Tag.id_tag == id_tag)
        if deleted_tag.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_tag} you requested for does not exist")
        deleted_tag.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f"Deleted tag: #{id_tag}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )


@router.put('/{id_tag}', response_model=schemas.CreateTag)
def update_tag(upd_tag: schemas.TagBase, id_tag: int, db: Session = Depends(get_db)):
    try:
        updated_tag = db.query(models.Tag).filter(models.Tag.id_tag == id_tag)
        if updated_tag.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id_tag} does not exist")
        updated_tag.update(upd_tag.dict(), synchronize_session=False)
        db.commit()
        return updated_tag.first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error " + str(e)
        )