from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    id_post: Optional[int] = None
    title: str
    body: str
    status: str
    has_image: bool = False
    status: str = 'ACT'
    publishing_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class ImageBase(BaseModel):
    id_image: Optional[int] = None
    url: str
    caption: str

    class Config:
        from_attributes: True


class TagBase(BaseModel):
    id_tag: Optional[int] = None
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


class PostTagBase(BaseModel):
    post_id: int
    tag_id: int
    added_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostImageBase(BaseModel):
    post_id: int
    image_id: int
    added_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreatePostImage(PostImageBase):
    class Config:
        from_attributes = True


class CreatePostTag(PostTagBase):
    class Config:
        from_attributes = True
