from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette import status

from Data.database import get_db
from Models import models
from Schemas import schemas

router = APIRouter(
    prefix='/images',
    tags=['Images']
)


@router.get('/', response_model=schemas.CreateImage)
async def get_random_image(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM images ORDER BY RANDOM() LIMIT 1")).fetchone()
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


@router.get('/all', response_model=List[schemas.CreateImage])
async def get_all_images(db: Session = Depends(get_db)):
    try:
        image = db.query(models.Image).all()
        return image
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


##it was removed List cast from response model
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateImage)
async def post_images(image_image: schemas.CreateImage, db: Session = Depends(get_db)):
    try:
        new_image = models.Image(**image_image.dict())
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return [new_image]
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get('/{id_image}', response_model=schemas.CreateImage, status_code=status.HTTP_200_OK)
def get_image_by_id(id_image: int, db: Session = Depends(get_db)):
    try:
        idv_image = db.query(models.Image).filter(models.Image.id_image == id_image).first()
        if idv_image is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_image} you requested for does not exist")
        return idv_image
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.delete('/{id_image}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(id_image: int, db: Session = Depends(get_db)):
    try:
        deleted_image = db.query(models.Image).filter(models.Image.id_image == id_image)
        if deleted_image.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id_image} you requested for does not exist")
        deleted_image.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.put('/{id_image}', response_model=schemas.CreateImage)
def update_image(upd_image: schemas.ImageBase, id_image: int, db: Session = Depends(get_db)):
    try:
        updated_image = db.query(models.Image).filter(models.Image.id_image == id_image)
        if updated_image.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id_image} does not exist")
        updated_image.update(upd_image.dict(), synchronize_session=False)
        db.commit()

        return updated_image.first()
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
