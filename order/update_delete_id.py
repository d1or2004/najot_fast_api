from fastapi import APIRouter, status, Depends, HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from model import Orders, User, Product
from database import SessionLocal
from schemas import OrderModel
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

order = APIRouter(prefix="/orders")


@order.put("/{order_id}", status_code=status.HTTP_200_OK)
async def update(order_id: int, order: OrderModel, Authorize: AuthJWT = Depends(), db: Session = Depends(SessionLocal)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    db_order = db.query(Orders).filter(Orders.id == order_id).first()
    db_user_id = db.query(User).filter(User.id == order.user_id).first()
    db_product_id = db.query(Product).filter(Product.id == order.product_id).first()
    if db_order:
        if db_product_id and db_user_id:
            db_order.user_id = order.user_id
            db_order.product_id = order.product_id

            db.commit()
            db.refresh(db_order)
            return {
                "code": 200,
                "msg": "Order update successfully",
                "Order": db_order
            }
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id yoki product_id mavjud emas")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="order_id mavjud emas")


@order.delete('/{order_id}', status_code=status.HTTP_200_OK)
async def delete(order_id: int, db: Session = Depends(SessionLocal), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    db_order = db.query(Orders).filter(Orders.id == order_id).first()

    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orders not found")
    db.delete(db_order)
    db.commit()

    return {
        "msg": "Orders deleted successfully"
    }


@order.get('/{id}')
async def category_id(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(SessionLocal)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    check_order = db.query(Orders).filter(Orders.id == id).first()
    if check_order:
        data = {
            "code": 201,
            "msg": "Success",
            "order": {
                "id": check_order.id,
                "user": {
                    "id": check_order.user.id,
                    "username": check_order.user.username,
                    "email": check_order.user.email
                },
                "count": check_order.count,
                "product": {
                    "id": check_order.product.id,
                    "name": check_order.product.name,
                    "price": check_order.product.price
                },
                "Total balance : ": check_order.product.price * check_order.count,
                "10 % chegirma, -> uzum promo kodidan foydalanganingiz uchun": (
                        check_order.product.price * check_order.count)
            }
        }
        kod = "uzum"
        if kod == "uzum":
            data["order"]["10 % chegirma, -> uzum promo kodidan foydalanganingiz uchun"] *= 0.9
            return jsonable_encoder(data)
        else:
            jsonable_encoder(f"10 % chegirmaga ega bo'lmoqchi bolsangiz "
                             f"uzum promo kodidan foydalaning  {data}")
            return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday id ga ega Order yo'q")
