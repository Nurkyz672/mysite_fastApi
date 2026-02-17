
from fastapi import FastAPI

import mysite
from mysite.api import users, subcategory, review, product_image, product, category, auth
import uvicorn
from mysite.admin.setup import setup_admin


shop_app = FastAPI(title='Store Project')
shop_app.include_router(users.user_router)
shop_app.include_router(subcategory.subcategory_router)
shop_app.include_router(review.review_router)
shop_app.include_router(product_image.product_image_router)
shop_app.include_router(product.product_router)
shop_app.include_router(category.category_router)
shop_app.include_router(auth.auth_router)
setup_admin(shop_app)

if __name__ == '__main__':
    uvicorn.run(shop_app,host='127.0.0.1',port=8002)
