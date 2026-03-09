from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Store
from mysite.database.schema import StoreOutSchema, StoreInputSchema
from mysite.database.db import SessionLocal

store_router = APIRouter(prefix='/store', tags=['Store'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store_router.post('/', response_model=StoreOutSchema)
async def create_store(store: StoreInputSchema, db: Session = Depends(get_db)):
    # Проверяем, существует ли уже магазин с таким именем
    existing_store = db.query(Store).filter(Store.store_name == store.store_name).first()
    if existing_store:
        raise HTTPException(status_code=400, detail="Магазин с таким именем уже существует")

    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.get('/', response_model=List[StoreOutSchema])
async def list_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()


@store_router.get('/{store_id}', response_model=StoreOutSchema)
async def get_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    return store_db


@store_router.put('/{store_id}', response_model=StoreOutSchema)
async def update_store(store_id: int, store: StoreInputSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(status_code=404, detail="Магазин не найден")

    for key, value in store.dict().items():
        setattr(store_db, key, value)

    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.delete('/{store_id}', response_model=dict)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(status_code=404, detail="Магазин не найден")

    db.delete(store_db)
    db.commit()
    return {'message': 'Магазин удален'}