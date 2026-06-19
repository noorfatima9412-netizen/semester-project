from pydantic import BaseModel
from datetime import date


class MedicineCreate(BaseModel):
    name: str
    category: str
    quantity: int
    price: float
    expiry_date: date


class MedicineResponse(MedicineCreate):
    id: int

    class Config:
        from_attributes = True