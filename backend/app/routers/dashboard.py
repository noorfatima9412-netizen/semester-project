from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.medicine import Medicine
from app.models.supplier import Supplier
from app.models.sale import Sale
from datetime import date, timedelta
from sqlalchemy import func

router = APIRouter(
prefix="/dashboard",
tags=["Dashboard"]
)

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_medicines = db.query(Medicine).count()
    total_suppliers = db.query(Supplier).count()
    total_sales = db.query(Sale).count()

    total_revenue = db.query(
        func.sum(Sale.total_price)
    ).scalar() or 0

    return {
    "total_medicines": total_medicines,
    "total_suppliers": total_suppliers,
    "total_sales": total_sales,
    "total_revenue": total_revenue
}

@router.get("/low-stock")
def get_low_stock_medicines(
db: Session = Depends(get_db)
):
 medicines = db.query(Medicine).filter(
 Medicine.quantity < 20
 ).all()

 return medicines

@router.get("/expiring-soon")
def get_expiring_medicines(
db: Session = Depends(get_db)
):
    next_30_days = date.today() + timedelta(days=30)

    medicines = db.query(Medicine).filter(
    Medicine.expiry_date <= next_30_days
    ).all()

    return medicines