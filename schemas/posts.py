from pydantic import BaseModel,EmailStr, Field

from database.models import Posts
from typing import List


class CreatePost(BaseModel):

    title: str
    content: str

class PostResponse(BaseModel):

    id: int
    post_title: str
    post_content: str
    created_at: str
    username:str