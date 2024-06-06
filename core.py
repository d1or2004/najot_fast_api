# Download and Install FASTAPI
"""pip install fastapi uvicorn """
from fastapi import FastAPI
from auth import model_auth
from userr.created_select import user_router
from category.select_created import category_router
from order.select_created import order_router
from product.select_create import product_router
from userr.update_id import user_update
from userr.delete import user_delete
from category.update_delete_id import category
from order.update_delete_id import order
from product.update_delete_id import product
from schemas import Settings

# run fastapi
"""uvicorn main:app --reload"""

app = FastAPI()
app.include_router(model_auth)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(order_router)
app.include_router(product_router)
app.include_router(user_update)
app.include_router(user_delete)
app.include_router(category)
app.include_router(order)
app.include_router(product)
from fastapi_jwt_auth import AuthJWT


@AuthJWT.load_config
def get_cofig():
    return Settings()


@app.get("/")
async def intro():
    return {
        "message": "This is landing page!"
    }


@app.get("/test")
async def test1():
    return {
        "message": "Hello! "
    }


@app.get("/test2")
async def test2():
    return {
        "message": "Group -> N37. Hello"
    }


@app.get("/test3/{id}")
async def user_id(id: int):
    return {
        "Massage": f"This is user - {id}"
    }
