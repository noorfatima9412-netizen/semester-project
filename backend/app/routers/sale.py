from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse
from app.auth.dependencies import get_current_user
from sqlalchemy import func

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post("/", response_model=SaleResponse)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    new_sale = Sale(
        medicine_name=sale.medicine_name,
        quantity=sale.quantity,
        total_price=sale.total_price
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale


@router.get("/", response_model=list[SaleResponse])
def get_sales(
    db: Session = Depends(get_db)
):
    return db.query(Sale).all()

@router.get("/total-revenue")
def get_total_revenue(
db: Session = Depends(get_db)
):
    total_revenue = db.query(
    func.sum(Sale.total_price)
    ).scalar()

    return {
        "total_revenue": total_revenue or 0
    }

@router.get("/history")
def get_sales_history(
db: Session = Depends(get_db)
):
    sales = db.query(Sale).order_by(
    Sale.created_at.desc()
    ).all()

    return sales
