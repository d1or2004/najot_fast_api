from model import Orders, User, Product
from schemas import OrderModel, UserOrder
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from database import session, Engine
from fastapi_jwt_auth import AuthJWT

session = session(bind=Engine)

order_router = APIRouter(prefix="/orders")


@order_router.get('/')
async def select(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    orders = session.query(Orders).all()
    context = [
        {
            "id": order.id,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            },
            "count": order.count,
            "product": {
                "id": order.product.id,
                "name": order.product.name,
                "price": order.product.price
            },
        }
        for order in orders
    ]
    return jsonable_encoder(context)


@order_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(orders: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    check_order = session.query(Orders).filter(Orders.id == orders.id).first()
    check_user_id = session.query(User).filter(User.id == orders.user_id).first()
    check_product_id = session.query(Product).filter(Product.id == orders.product_id).first()

    if check_order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order with this ID already exists")

    if not check_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id does not exist")

    if not check_product_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_id does not exist")

    new_order = Orders(
        id=orders.id,
        user_id=orders.user_id,
        count=orders.count,
        order_status=orders.order_status,
        product_id=orders.product_id
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    data = {
        "code": 201,
        "msg": "Success",
        "order": {
            "id": new_order.id,
            "user": {
                "id": new_order.user.id,
                "username": new_order.user.username,
                "email": new_order.user.email
            },
            "count": new_order.count,
            "product": {
                "id": new_order.product.id,
                "name": new_order.product.name,
                "price": new_order.product.price
            },
        }
    }
    return jsonable_encoder(data)


@order_router.post('/user/order')
async def user_order(user_order: UserOrder, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    check_user = session.query(User).filter(User.username == user_order.username).first()
    if check_user.is_staff:
        check_order = session.query(Orders).filter(Orders.user_id == check_user.id)
        if check_order:
            context = [
                {
                    "id": order.id,
                    "user": {
                        "id": order.user.id,
                        "username": order.user.username,
                        "email": order.user.email
                    },
                    "count": order.count,
                    "product": {
                        "id": order.product.id,
                        "name": order.product.name,
                        "price": order.product.price
                    },
                    "status": order.order_status,
                    "Jami summa": order.count * order.product.price
                }
                for order in check_order
            ]
            return jsonable_encoder(context)
        else:
            return HTTPException(status_code=status.HTTP_200_OK, detail="Savat bosh")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ma'lumotlarni faqat admin ko'rish mumkin")


@order_router.post('/user/order/savat')
async def user_order(user_order: UserOrder, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    check_user = session.query(User).filter(User.username == user_order.username).first()
    if check_user:
        check_order = session.query(Orders).filter(Orders.user_id == check_user.id)
        if check_order:
            total_balance = 0
            product_count = 0
            for order in check_order:
                total_balance += order.count * order.product.price
                product_count += order.count
                context = {
                    "product": {
                        "price": order.product.price,
                        "count": product_count,
                        "Jami summa": total_balance
                    }
                }
            return jsonable_encoder(context)
