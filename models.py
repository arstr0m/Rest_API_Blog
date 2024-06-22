from typing import List

from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

#pip install psycopg2

class Post(Base):
    __tablename__ = "posts"
    id_post: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String(50), nullable=False, index=True)
    body = Column(String(250), nullable=False)
    has_image = Column(Boolean, nullable=False, server_default='FALSE')
    status = Column(String(3), nullable=False, server_default='ACT')
    publishing_date = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    post_tags: Mapped[List["post_tag"]] = relationship("post_tag", back_populates="post")
    post_images: Mapped[List["post_image"]] = relationship("post_image", back_populates="post")

class Image(Base):
    __tablename__ = 'images'
    id_image: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    added_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    url = Column(String(250), nullable=False)
    caption = Column(String(250), nullable=False, server_default='lorem ipsum amazing photo, look at that!')

    post_images: Mapped[List["post_image"]] = relationship("post_image", back_populates="image")

class Tag(Base):
    __tablename__ = 'tag'
    id_tag: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title = Column(String(50), nullable=False, index=True)
    status = Column(String(3), nullable=False, server_default='ACT')

    post_tags: Mapped[List["post_tag"]] = relationship("post_tag", back_populates="tag")

class post_tag(Base):
    __tablename__ = 'post_tag'
    added_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id_post"), primary_key=True)
    tags_id: Mapped[int] = mapped_column(ForeignKey("tag.id_tag"), primary_key=True)

    post: Mapped["Post"] = relationship("Post", back_populates="post_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="post_tags")

class post_image(Base):
    __tablename__ = 'post_image'
    added_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id_post"), primary_key=True)
    tags_id: Mapped[int] = mapped_column(ForeignKey("images.id_image"), primary_key=True)

    post: Mapped["Post"] = relationship("Post", back_populates="post_images")
    image: Mapped["Image"] = relationship("Image", back_populates="post_images")