from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import StoreMenu
from mysite.database.schema import StoreMenuOutSchema, StoreMenuInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

store_menu_router = APIRouter(prefix='/store_menu', tags=['StoreMenu'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store_menu_router.post('/', response_model=StoreMenuOutSchema)
async def create_store_menu(item: StoreMenuInputSchema, db: Session = Depends(get_db)):
    menu_db = StoreMenu(**item.dict())
    db.add(menu_db)
    db.commit()
    db.refresh(menu_db)
    return menu_db


@store_menu_router.get('/', response_model=List[StoreMenuOutSchema])
async def list_store_menu(db: Session = Depends(get_db)):
    return db.query(StoreMenu).all()


@store_menu_router.get('/{menu_id}', response_model=StoreMenuOutSchema)
async def get_store_menu(menu_id: int, db: Session = Depends(get_db)):
    menu_db = db.query(StoreMenu).filter(StoreMenu.id == menu_id).first()
    if not menu_db:
        raise HTTPException(status_code=404, detail='Элемент меню не найден')
    return menu_db


@store_menu_router.put('/{menu_id}', response_model=dict)
async def update_store_menu(menu_id: int, item: StoreMenuInputSchema, db: Session = Depends(get_db)):
    menu_db = db.query(StoreMenu).filter(StoreMenu.id == menu_id).first()
    if not menu_db:
        raise HTTPException(status_code=404, detail='Элемент меню не найден')

    for key, value in item.dict().items():
        setattr(menu_db, key, value)

    db.commit()
    db.refresh(menu_db)
    return {'message': 'Элемент меню обновлен'}


@store_menu_router.delete('/{menu_id}', response_model=dict)
async def delete_store_menu(menu_id: int, db: Session = Depends(get_db)):
    menu_db = db.query(StoreMenu).filter(StoreMenu.id == menu_id).first()
    if not menu_db:
        raise HTTPException(status_code=404, detail='Элемент меню не найден')

    db.delete(menu_db)
    db.commit()
    return {'message': 'Элемент меню удален'}