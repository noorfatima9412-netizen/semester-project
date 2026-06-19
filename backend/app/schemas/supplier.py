from pydantic import BaseModel

class SupplierCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str


class SupplierResponse(SupplierCreate):
    id: int

    class Config:
        from_attributes = True