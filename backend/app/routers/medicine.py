from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.medicine import Medicine
from app.schemas.medicine import MedicineCreate, MedicineResponse
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/medicines",
    tags=["Medicines"]
)


@router.post("/", response_model=MedicineResponse)
def add_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    new_medicine = Medicine(
        name=medicine.name,
        category=medicine.category,
        quantity=medicine.quantity,
        price=medicine.price,
        expiry_date=medicine.expiry_date
    )

    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)

    return new_medicine


@router.get("/", response_model=list[MedicineResponse])
def get_all_medicines(
    db: Session = Depends(get_db)
):
    medicines = db.query(Medicine).all()
    return medicines


@router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine_by_id(
    medicine_id: int,
    db: Session = Depends(get_db)
):
    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id
    ).first()

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    return medicine


@router.put("/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: int,
    medicine_data: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id
    ).first()

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    medicine.name = medicine_data.name
    medicine.category = medicine_data.category
    medicine.quantity = medicine_data.quantity
    medicine.price = medicine_data.price
    medicine.expiry_date = medicine_data.expiry_date

    db.commit()
    db.refresh(medicine)

    return medicine


@router.delete("/{medicine_id}")
def delete_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id
    ).first()

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    db.delete(medicine)
    db.commit()

    return {
        "message": "Medicine deleted successfully"
    }

@router.get("/search/{name}")
def search_medicine(
name: str,
db: Session = Depends(get_db)
):
    medicines = db.query(Medicine).filter(
    Medicine.name.ilike(f"%{name}%")
    ).all()

    return medicines

@router.patch("/{medicine_id}/stock")
def update_stock(
medicine_id: int,
quantity: int,
db: Session = Depends(get_db)
):
    medicine = db.query(Medicine).filter(
    Medicine.id == medicine_id
    ).first()

    if not medicine:
      raise HTTPException(
        status_code=404,
        detail="Medicine not found"
    )

    medicine.quantity += quantity

    db.commit()
    db.refresh(medicine)

    return {
        "message": "Stock updated successfully",
        "new_quantity": medicine.quantity
    }

