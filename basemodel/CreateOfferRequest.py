from pydantic import BaseModel
class CreateOfferRequest(BaseModel):
    name: str
    price: float
    description: str
    #seller_id: int