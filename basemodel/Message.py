from pydantic import BaseModel
class MessageModel(BaseModel):
    message: str
    sender: str
    receiver: str
