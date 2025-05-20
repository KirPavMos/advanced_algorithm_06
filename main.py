# Необходимо на языке Python реализовать
# API на FastAPI для получения данных из базы данных.

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBSeller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

Base.metadata.create_all(bind=engine)

class Seller(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        from_attributes = True

class SellerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/sellers", response_model=List[Seller])
def get_all_sellers(db: Session = Depends(get_db)):
    sellers = db.query(DBSeller).all()
    return sellers

@app.put("/sellers/{seller_id}/update", response_model=Seller)
def update_seller(seller_id: int, seller_update: SellerUpdate, db: Session = Depends(get_db)):
    db_seller = db.query(DBSeller).filter(DBSeller.id == seller_id).first()
    if not db_seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    update_data = seller_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_seller, key, value)

    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

@app.get("/sellers/{seller_id}", response_model=Seller)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(DBSeller).filter(DBSeller.id == seller_id).first()
    if seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller