from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import models
import schemas
from fastapi import APIRouter
from database import get_db

router = APIRouter(
    prefix='/images',
    tags=['Images']
)


@router.get('/', response_model=List[schemas.CreateImage])
async def get_all_images(db: Session = Depends(get_db)):
    image = db.query(models.Image).all()
    return image


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreateImage])
async def post_images(image_image: schemas.CreateImage, db: Session = Depends(get_db)):
    new_image = models.Image(**image_image.dict())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return [new_image]


@router.get('/{id}', response_model=schemas.CreateImage, status_code=status.HTTP_200_OK)
def get_image(id_image: int, db: Session = Depends(get_db)):
    idv_image = db.query(models.Image).filter(models.Image.id_image == id_image).first()

    if idv_image is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id_image} you requested for does not exist")
    return idv_image


@router.delete('/{id_image}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(id_image: int, db: Session = Depends(get_db)):
    deleted_image = db.query(models.Image).filter(models.Image.id_image == id_image)

    if deleted_image.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id_image} you requested for does not exist")
    deleted_image.delete(synchronize_session=False)
    db.commit()


@router.put('/{id_image}', response_model=schemas.CreateImage)
def update_image(upd_image: schemas.ImageBase, id_image: int, db: Session = Depends(get_db)):
    updated_image = db.query(models.Image).filter(models.Image.id_image == id_image)

    if updated_image.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id_image} does not exist")
    updated_image.update(upd_image.dict(), synchronize_session=False)
    db.commit()

    return updated_image.first()
