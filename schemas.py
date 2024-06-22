from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class PostBase(BaseModel):
    title:str
    body: str
    status: str
    has_image: bool = False
    status: str = 'ACT'
    publishing_date: Optional[datetime] = None
    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    url: str
    caption: str
    class Config:
        orm_mode: True

class TagBase(BaseModel):
    title: str
    status: str

    class Config:
        orm_mode: True
class CreatePost(PostBase):
    class Config:
        orm_mode = True

class CreateImage(ImageBase):
    class Config:
        orm_mode = True

class CreateTag(TagBase):
    class Config:
        orm_mode = True