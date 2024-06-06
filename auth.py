from fastapi import APIRouter, status, Depends
from schemas import RegisterModel, LoginModel, Settings
from database import Engine, session
from model import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
import datetime
from fastapi_jwt_auth import AuthJWT

session = session(bind=Engine)
model_auth = APIRouter(prefix="/auth")


@model_auth.get("/")
async def auth(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    return {"massage": "Auth rooter"}


@model_auth.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: RegisterModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu emaildan oldin ro'yxatdan o'tkazilgan")
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu username mavjud")

    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active

    )
    session.add(new_user)
    session.commit()
    return user


@model_auth.get('/register')
async def list(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    user = session.query(User).all()
    return jsonable_encoder(user)


@model_auth.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=60)
        refresh_lifetime = datetime.timedelta(days=2)
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_access_token(subject=db_user.username, expires_time=refresh_lifetime)
        token = {
            "access token": access_token,
            "refresh token": refresh_token
        }
        response = {
            "code": 200,
            "success": True,
            "msg": "User successfully login",
            "id": db_user.id,
            "token": token
        }
        return jsonable_encoder(response)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parol yoki username noto'g'ri ")


@model_auth.get('/login')
async def list(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    user = session.query(User).all()
    return jsonable_encoder(user)
