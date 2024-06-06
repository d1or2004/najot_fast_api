from fastapi import APIRouter
from werkzeug.security import generate_password_hash

from database import session, Engine
from schemas import UserModel
from model import User
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

session = session(bind=Engine)

user_router = APIRouter(prefix="/user")


@user_router.post("/create")
async def user_create(user: UserModel):
    user_check = session.query(User).filter(User.id == user.id).first()
    if user_check:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday malumtlar ro'yxatda mavjud")

    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active,
    )

    session.add(new_user)
    session.commit()
    data = {
        "code": 200,
        "msg": "Successfully",
        "user": user

    }
    return jsonable_encoder(data)


@user_router.get("/", status_code=status.HTTP_200_OK)
async def user_c(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    users = session.query(User).all()
    context = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
        }
        for user in users
    ]
    return jsonable_encoder(context)
