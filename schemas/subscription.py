from pydantic import BaseModel

class CheckSubscription(BaseModel):

    following_to_username:str

class SubscribeToSchema(CheckSubscription):

    pass