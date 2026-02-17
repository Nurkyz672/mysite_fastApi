from pydantic import BaseModel,EmailStr,constr
from typing import Optional
from. models import StatusChoices
from datetime import date,datetime


class UserProfileSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

class Login(BaseModel):
    username: str
    password: str


class  UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    phone_number: Optional[int]


class  UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[int]
    phone_number: Optional[int]
    status: StatusChoices
    date_registered: date


class CategoryInputSchema(BaseModel):
    category_image: str
    category_name: str


class CategoryOutSchema(BaseModel):
    id: int
    category_image: str
    category_name: str


class SubCategoryInputSchema(BaseModel):
    category_id: int
    sub_category_name: str

class SubCategoryOutSchema(BaseModel):
    id: int
    sub_category_name: str
    category_id: int


class ProductInputSchema(BaseModel):
    id : int
    subcategory_id: int
    product_name: str
    price: int
    article_number: int
    description: str
    video: Optional[str] = None
    product_type: bool



class ProductOutSchema(BaseModel):
    id: int
    subcategory_id: int
    subcategory:SubCategoryOutSchema
    product_name: str
    price: int
    article_number: int
    description: str
    video: Optional[str]
    product_type: bool
    created_date: date


class ProductImageInputSchema(BaseModel):
    product_id: int
    image: str

class ProductImageOutSchema(BaseModel):
    id: int
    image: str


class ReviewInputSchema(BaseModel):
    text: str
    stars: int
    user_id: int
    product_id: int

class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    product_id: int
    text: str
    stars: int
    created_date: datetime


