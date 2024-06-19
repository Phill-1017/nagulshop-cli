from pydantic import BaseModel
class CreateBidRequest(BaseModel):
    offer_id: int
    bidder_id: int
    bid_amount: int
