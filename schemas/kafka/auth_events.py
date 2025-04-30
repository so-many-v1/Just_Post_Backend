from pydantic import BaseModel, EmailStr
from datetime import datetime

class RegistrationEventSchema(BaseModel):

    event_id:str
    time:float
    username:str
    email: EmailStr

class LoginEventSchema(RegistrationEventSchema):

    pass

class DeleteEventSchema(RegistrationEventSchema):

    pass