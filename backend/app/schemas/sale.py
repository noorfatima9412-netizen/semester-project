from pydantic import BaseModel
from datetime import datetime

class SaleCreate(BaseModel):
    medicine_name: str
    quantity: int
    total_price: float


class SaleResponse(SaleCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True