from fastapi import APIRouter, status, Depends, HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from model import Category, User
from database import SessionLocal
from schemas import CategoryModel
from database import session, Engine
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

category = APIRouter(prefix="/category")


@category.put('/{id}')
async def update(id: int, data: CategoryModel, Authorize: AuthJWT = Depends(), db: Session = Depends(SessionLocal)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday category_id mavjud emas")
        category.name = data.name
        db.commit()
        db.refresh(category)

        return {
            "code": 200,
            "msg": "User update Seccessfully",
            "Category": category
        }
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumotlarni faqat Admin o'zgartirish mumkin")
    # if category:
    #     for key, value in data.dict(exclude_unset=True).items():
    #         setattr(category, key, value)
    #     session.commit()
    #     data = {
    #         "code": 200,
    #         "msg": "Update category"
    #     }
    #     return jsonable_encoder(data)
    # return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday id mavjud emas")


@category.delete('/{category_id}', status_code=status.HTTP_200_OK)
async def delete(category_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(SessionLocal)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        db.delete(db_category)
        db.commit()

        return {
            "msg": "Category deleted successfully"
        }

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumotlarni faqat Admin o'zgartirish mumkin")


@category.get('/{id}')
async def category_id(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(SessionLocal)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        check_category = db.query(Category).filter(Category.id == id).first()
        if check_category:
            return jsonable_encoder(check_category)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday id ga ega category yo'q")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumotlarni faqat Admin o'zgartirish mumkin")
