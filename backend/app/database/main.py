from fastapi import FastAPI
from app.database.database import engine

app = FastAPI(title="Pharmacy Management System")


@app.get("/")
def home():
    return {"message": "API Running Successfully"}


@app.get("/db-test")
def db_test():
    try:
        conn = engine.connect()
        conn.close()

        return {
            "status": "Database Connected Successfully"
        }

    except Exception as e:
        return {
            "error": str(e)
        }