from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(50), default="staff")
    created_at = Column(DateTime, server_default=func.now())

    sales = relationship("Sale", back_populates="user")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(150))
    phone = Column(String(20), nullable=False)
    email = Column(String(150))
    created_at = Column(DateTime, server_default=func.now())

    medicines = relationship("Medicine", back_populates="supplier")


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    expiry_date = Column(Date, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    created_at = Column(DateTime, server_default=func.now())

    supplier = relationship("Supplier", back_populates="medicines")
    sales = relationship("Sale", back_populates="medicine")
    prescriptions = relationship("Prescription", back_populates="medicine")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(150), unique=True)
    address = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    sales = relationship("Sale", back_populates="customer")
    prescriptions = relationship("Prescription", back_populates="customer")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    quantity_sold = Column(Integer, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    sale_date = Column(DateTime, server_default=func.now())

    customer = relationship("Customer", back_populates="sales")
    medicine = relationship("Medicine", back_populates="sales")
    user = relationship("User", back_populates="sales")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    dosage = Column(String(100), nullable=False)
    duration = Column(String(100), nullable=False)
    prescribed_by = Column(String(150), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    customer = relationship("Customer", back_populates="prescriptions")
    medicine = relationship("Medicine", back_populates="prescriptions")
