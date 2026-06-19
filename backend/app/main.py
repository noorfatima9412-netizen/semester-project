from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

from app.routers.dashboard import router as dashboard_router

# Models
from app.models.user import User
from app.models.medicine import Medicine
from app.models.supplier import Supplier
from app.models.sale import Sale

# Routers
from app.routers.auth import router as auth_router
from app.routers.medicine import router as medicine_router
from app.routers.supplier import router as supplier_router
from app.routers.sale import router as sale_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pharmacy Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Routes
app.include_router(auth_router)

# Medicine Routes
app.include_router(medicine_router)

# Supplier Routes
app.include_router(supplier_router)

# Sales Routes
app.include_router(sale_router)

app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "message": "Pharmacy Management System API Running"
    }