from model import Product, Category, User
from schemas import ProductModel
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from database import session, Engine
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from database import SessionLocal


session = session(bind=Engine)

product_router = APIRouter(prefix="/product")


@product_router.get('/')
async def select(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    products = session.query(Product).all()
    context = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
        }
        for product in products
    ]
    return jsonable_encoder(context)


@product_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(product: ProductModel, Authorize: AuthJWT = Depends(), db: Session = Depends(SessionLocal)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        check_product = session.query(Product).filter(Product.id == product.id).first()
        check_category_id = session.query(Category).filter(Category.id == product.category_id).first()
        if check_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this ID already exists")
        if not check_category_id:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category_id does not exist")
        new_product = Product(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category_id=product.category_id
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        data = {
            "code": 201,
            "msg": "Success",
            "Product": new_product
        }

        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ma'lumotlarni faqat ADMIN o'zgartira oladi")
