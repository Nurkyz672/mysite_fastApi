from fastapi import APIRouter,HTTPException,Depends
from mysite.database.models import SubCategory
from mysite.database.schema import SubCategoryOutSchema, SubCategoryInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


subcategory_router = APIRouter(prefix='/subcategory',tags=['Subcategory CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@subcategory_router.post('/', response_model=SubCategoryOutSchema)
async def user_create(subcategory:SubCategoryInputSchema,db: Session = Depends(get_db)):
    user_db = SubCategory(**subcategory.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db



@subcategory_router.get('/',response_model=List[SubCategoryOutSchema])
async def subcategory_list(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()




@subcategory_router.get('/{subcategory_id}',response_model=SubCategoryOutSchema)
async def subcategory_detail(subcategory_id:int,db: Session = Depends(get_db)):
    user_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()

    if not user_db:
        raise HTTPException(detail='Мындай подкатегория  жок',status_code=404)
    return user_db


@subcategory_router.put('/{subcategory_id}', response_model=dict)
async def update_subcategory(subcategory_id: int,subcategory: SubCategoryInputSchema, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай маалымат жок')

    for subcategory_key, subcategory_value in subcategory.dict().items():
        setattr(subcategory_db,subcategory_key,subcategory_value)

    db.commit()
    db.refresh(subcategory_db)

    return {'message': 'Подкатегория озгорулду'}

@subcategory_router.delete('/{subcategory_id}/', response_model=dict)
async def delete_subcategory(subcategory_id: int,db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory_db:
        raise HTTPException( status_code=404,detail='Мындай профайл жок')

    db.delete(subcategory_db)
    db.commit()
    return {'message': 'Подкатегория  удалена'}