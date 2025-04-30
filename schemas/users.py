from datetime import datetime

from pydantic import BaseModel,EmailStr, Field

from database.models import Posts
from typing import List

class LoginUser(BaseModel):

    name:str = Field(min_length=3)
    password:str = Field(min_length=5)

class RegisterUser(LoginUser):

    confirmed_password:str
    email:EmailStr

class UsersPosts(BaseModel):

    id:int
    post_title:str
    post_content:str
    created_at:str


class UserProfile(BaseModel):

    name : str
    posts : List[UsersPosts]
    followers_amount: int
    following_amount: int