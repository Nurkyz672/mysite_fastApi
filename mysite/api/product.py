from itertools import product
from fastapi import APIRouter,HTTPException,Depends
from mysite.database.models import Product
from mysite.database.schema import ProductOutSchema,ProductInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


product_router = APIRouter(prefix='/product',tags=['Product CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/', response_model=ProductOutSchema)
async def create_product(user:ProductInputSchema,db: Session = Depends(get_db)):
    product_db = Product(**user.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db



@product_router.get('/',response_model=List[ProductOutSchema])
async def product_list(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/{product_id}',response_model=ProductOutSchema)
async def product_detail(product_id:int,db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()

    if not product_db:
        raise HTTPException(detail='Мындай маалымат жок',status_code=404)
    return product_db


@product_router.put('/{product_id}', response_model=dict)
async def update_category(product_id: int,product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай продукт жок'
        )

    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value)

    db.commit()
    db.refresh(product_db)

    return {'message': 'Продукт озгорулду'}



@product_router.delete('/{product_id}/', response_model=dict)
async def delete_product(product_id: int,db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException( status_code=404,detail='Мындай продукт жок')

    db.delete(product_db)
    db.commit()
    return {'message': 'Продукт удалена'}




