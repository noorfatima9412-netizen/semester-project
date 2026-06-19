from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from database import Base, engine, get_db
from models import Customer, Medicine, Prescription, Sale, Supplier, User
from schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    DashboardStats,
    MedicineCreate,
    MedicineResponse,
    MedicineUpdate,
    PrescriptionCreate,
    PrescriptionResponse,
    SaleCreate,
    SaleResponse,
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
    TokenResponse,
    UserLogin,
    UserRegister,
)

app = FastAPI(
    title="Pharmacy Management System API",
    description="Full-stack pharmacy management system for UMT OSSD project",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables when app starts (also run schema.sql in Supabase)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Pharmacy Management System API is running", "docs": "/docs"}


# ==================== AUTH (2 endpoints) ====================

@app.post("/auth/register", response_model=TokenResponse)
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.username, user.role)
    return TokenResponse(access_token=token, username=user.username, role=user.role)


@app.post("/auth/login", response_model=TokenResponse)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Wrong username or password")

    token = create_access_token(user.username, user.role)
    return TokenResponse(access_token=token, username=user.username, role=user.role)


# ==================== MEDICINES (7 endpoints) ====================

@app.post("/medicines/", response_model=MedicineResponse)
def add_medicine(
    data: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = Medicine(**data.model_dump())
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    return medicine


@app.get("/medicines/", response_model=List[MedicineResponse])
def get_all_medicines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Medicine).order_by(Medicine.name).all()


@app.get("/medicines/search", response_model=List[MedicineResponse])
def search_medicines(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    keyword = f"%{q}%"
    return (
        db.query(Medicine)
        .filter(or_(Medicine.name.ilike(keyword), Medicine.category.ilike(keyword)))
        .all()
    )


@app.get("/medicines/expiring", response_model=List[MedicineResponse])
def get_expiring_medicines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    limit_date = date.today() + timedelta(days=30)
    return (
        db.query(Medicine)
        .filter(Medicine.expiry_date <= limit_date)
        .order_by(Medicine.expiry_date)
        .all()
    )


@app.get("/medicines/{medicine_id}", response_model=MedicineResponse)
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@app.put("/medicines/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: int,
    data: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(medicine, key, value)

    db.commit()
    db.refresh(medicine)
    return medicine


@app.delete("/medicines/{medicine_id}")
def delete_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    db.delete(medicine)
    db.commit()
    return {"message": "Medicine deleted successfully"}


# ==================== CUSTOMERS (5 endpoints) ====================

@app.post("/customers/", response_model=CustomerResponse)
def add_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@app.get("/customers/", response_model=List[CustomerResponse])
def get_all_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Customer).order_by(Customer.name).all()


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer


@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}


# ==================== SALES (4 endpoints) ====================

def build_sale_response(sale: Sale) -> SaleResponse:
    return SaleResponse(
        id=sale.id,
        customer_id=sale.customer_id,
        medicine_id=sale.medicine_id,
        quantity_sold=sale.quantity_sold,
        total_price=sale.total_price,
        sale_date=sale.sale_date,
        customer_name=sale.customer.name if sale.customer else None,
        medicine_name=sale.medicine.name if sale.medicine else None,
    )


@app.post("/sales/", response_model=SaleResponse)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    medicine = db.query(Medicine).filter(Medicine.id == data.medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    if medicine.quantity < data.quantity_sold:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    total_price = Decimal(str(medicine.price)) * data.quantity_sold
    medicine.quantity -= data.quantity_sold

    sale = Sale(
        customer_id=data.customer_id,
        medicine_id=data.medicine_id,
        user_id=current_user.id,
        quantity_sold=data.quantity_sold,
        total_price=total_price,
    )
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return build_sale_response(sale)


@app.get("/sales/", response_model=List[SaleResponse])
def get_all_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sales = db.query(Sale).order_by(Sale.sale_date.desc()).all()
    return [build_sale_response(sale) for sale in sales]


@app.get("/sales/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return build_sale_response(sale)


@app.delete("/sales/{sale_id}")
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    db.delete(sale)
    db.commit()
    return {"message": "Sale deleted successfully"}


# ==================== PRESCRIPTIONS (3 endpoints) ====================

def build_prescription_response(p: Prescription) -> PrescriptionResponse:
    return PrescriptionResponse(
        id=p.id,
        customer_id=p.customer_id,
        medicine_id=p.medicine_id,
        dosage=p.dosage,
        duration=p.duration,
        prescribed_by=p.prescribed_by,
        created_at=p.created_at,
        customer_name=p.customer.name if p.customer else None,
        medicine_name=p.medicine.name if p.medicine else None,
    )


@app.post("/prescriptions/", response_model=PrescriptionResponse)
def add_prescription(
    data: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    medicine = db.query(Medicine).filter(Medicine.id == data.medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    prescription = Prescription(**data.model_dump())
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return build_prescription_response(prescription)


@app.get("/prescriptions/", response_model=List[PrescriptionResponse])
def get_all_prescriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prescriptions = db.query(Prescription).order_by(Prescription.created_at.desc()).all()
    return [build_prescription_response(p) for p in prescriptions]


@app.get("/prescriptions/customer/{customer_id}", response_model=List[PrescriptionResponse])
def get_customer_prescriptions(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prescriptions = (
        db.query(Prescription)
        .filter(Prescription.customer_id == customer_id)
        .order_by(Prescription.created_at.desc())
        .all()
    )
    return [build_prescription_response(p) for p in prescriptions]


# ==================== SUPPLIERS (3 endpoints) ====================

@app.post("/suppliers/", response_model=SupplierResponse)
def add_supplier(
    data: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = Supplier(**data.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@app.get("/suppliers/", response_model=List[SupplierResponse])
def get_all_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Supplier).order_by(Supplier.name).all()


@app.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(supplier, key, value)

    db.commit()
    db.refresh(supplier)
    return supplier


# ==================== DASHBOARD (1 endpoint) ====================

@app.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_medicines = db.query(Medicine).count()
    low_stock_count = db.query(Medicine).filter(Medicine.quantity < 10).count()
    total_sales = db.query(Sale).count()
    total_customers = db.query(Customer).count()

    today = date.today()
    sales_today = (
        db.query(Sale)
        .filter(func.date(Sale.sale_date) == today)
        .count()
    )

    revenue = db.query(func.coalesce(func.sum(Sale.total_price), 0)).scalar()

    return DashboardStats(
        total_medicines=total_medicines,
        low_stock_count=low_stock_count,
        total_sales=total_sales,
        sales_today=sales_today,
        total_customers=total_customers,
        total_revenue=Decimal(str(revenue)),
    )
