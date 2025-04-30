from typing import List

from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreatePostEvent(BaseModel):

    event_id:str
    time:float
    writer_username:str