from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr


# ---------- Auth ----------
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "staff"


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str


# ---------- Supplier ----------
class SupplierCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: str
    email: Optional[str] = None


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_person: Optional[str]
    phone: str
    email: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------- Medicine ----------
class MedicineCreate(BaseModel):
    name: str
    category: str
    quantity: int
    price: Decimal
    expiry_date: date
    supplier_id: Optional[int] = None


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[Decimal] = None
    expiry_date: Optional[date] = None
    supplier_id: Optional[int] = None


class MedicineResponse(BaseModel):
    id: int
    name: str
    category: str
    quantity: int
    price: Decimal
    expiry_date: date
    supplier_id: Optional[int]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------- Customer ----------
class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    address: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------- Sale ----------
class SaleCreate(BaseModel):
    customer_id: int
    medicine_id: int
    quantity_sold: int


class SaleResponse(BaseModel):
    id: int
    customer_id: int
    medicine_id: int
    quantity_sold: int
    total_price: Decimal
    sale_date: Optional[datetime]
    customer_name: Optional[str] = None
    medicine_name: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- Prescription ----------
class PrescriptionCreate(BaseModel):
    customer_id: int
    medicine_id: int
    dosage: str
    duration: str
    prescribed_by: str


class PrescriptionResponse(BaseModel):
    id: int
    customer_id: int
    medicine_id: int
    dosage: str
    duration: str
    prescribed_by: str
    created_at: Optional[datetime]
    customer_name: Optional[str] = None
    medicine_name: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- Dashboard ----------
class DashboardStats(BaseModel):
    total_medicines: int
    low_stock_count: int
    total_sales: int
    sales_today: int
    total_customers: int
    total_revenue: Decimal
