from fastapi import APIRouter,HTTPException,Depends
from mysite.database.models import ProductImage
from mysite.database.schema import ProductImageOutSchema,ProductImageInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


product_image_router = APIRouter(prefix='/productimage',tags=['ProductImage CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_image_router.post('/', response_model=ProductImageOutSchema)
async def productimage_create(user:ProductImageInputSchema,db: Session = Depends(get_db)):
    productimage_db = ProductImage(**user.dict())
    db.add(productimage_db)
    db.commit()
    db.refresh(productimage_db)
    return productimage_db



@product_image_router.get('/',response_model=List[ProductImageOutSchema])
async def product_image_list(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()

@product_image_router.get('/{product_image_id}',response_model=ProductImageOutSchema)
async def category_detail(product_image_id:int,db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()

    if not product_image_db:
        raise HTTPException(detail='Мындай продукт картина жок',status_code=404)
    return product_image_db


@product_image_router.put('/{product_image_id}', response_model=dict)
async def update_product_image(product_image_id: int,product_image: ProductImageInputSchema, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай Продукт картина жок'
        )

    for product_image_key, product_image_value in product_image.dict().items():
        setattr(product_image_db, product_image_key, product_image_value)

    db.commit()
    db.refresh(product_image_db)

    return {'message': 'Продукт картина озгорулду'}



@product_image_router.delete('/{product_image_id}/', response_model=dict)
async def delete_product_image(product_image_id: int,db: Session = Depends(get_db)):
    productimage_db = db.query(ProductImage).filter(
        ProductImage.id == product_image_id).first()

    if not productimage_db:
        raise HTTPException(status_code=404,detail='Мындай жок')

    db.delete(productimage_db)
    db.commit()

    return {'message': 'Продукт картина удалена'}




