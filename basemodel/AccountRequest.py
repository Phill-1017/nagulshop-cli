from pydantic import BaseModel
class AccountRequest(BaseModel):
    username: str
    password: str
    role: str