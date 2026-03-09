from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import CourierProduct
from mysite.database.schema import CourierProductOutSchema, CourierProductInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

courier_product_router = APIRouter(prefix='/courier_product', tags=['CourierProduct'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@courier_product_router.post('/', response_model=CourierProductOutSchema)
async def create_courier_product(item: CourierProductInputSchema, db: Session = Depends(get_db)):
    product_db = CourierProduct(**item.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@courier_product_router.get('/', response_model=List[CourierProductOutSchema])
async def list_courier_products(db: Session = Depends(get_db)):
    return db.query(CourierProduct).all()


@courier_product_router.get('/{product_id}', response_model=CourierProductOutSchema)
async def get_courier_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(CourierProduct).filter(CourierProduct.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Продукт курьера не найден')
    return product_db


@courier_product_router.put('/{product_id}', response_model=dict)
async def update_courier_product(product_id: int, item: CourierProductInputSchema, db: Session = Depends(get_db)):
    product_db = db.query(CourierProduct).filter(CourierProduct.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Продукт курьера не найден')

    for key, value in item.dict().items():
        setattr(product_db, key, value)

    db.commit()
    db.refresh(product_db)
    return {'message': 'Продукт курьера обновлен'}


@courier_product_router.delete('/{product_id}', response_model=dict)
async def delete_courier_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(CourierProduct).filter(CourierProduct.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Продукт курьера не найден')

    db.delete(product_db)
    db.commit()
    return {'message': 'Продукт курьера удален'}