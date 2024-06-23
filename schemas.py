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
        from_attributes = True

class ImageBase(BaseModel):
    url: str
    caption: str
    class Config:
        from_attributes: True

class TagBase(BaseModel):
    title: str
    status: str

    class Config:
        from_attributes: True
class CreatePost(PostBase):
    class Config:
        from_attributes = True

class CreateImage(ImageBase):
    class Config:
        from_attributes = True

class CreateTag(TagBase):
    class Config:
        from_attributes = True