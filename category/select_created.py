from fastapi import APIRouter, Depends
from database import session, Engine
from schemas import CategoryModel
from model import Category, User
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

session = session(bind=Engine)

category_router = APIRouter(prefix="/category")


@category_router.get("/")
async def category_list(Authorize: AuthJWT = Depends(), status_code=status.HTTP_200_OK):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    categories = session.query(Category).all()
    context = [
        {
            "id": category.id,
            "name": category.name,
        }
        for category in categories
    ]

    return jsonable_encoder(context)


@category_router.post("/create")
async def create(category: CategoryModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    check_category = session.query(Category).filter(Category.id == category.id).first()
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        if check_category:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday ma'lumotlar mavjud")

        new_category = Category(
            id=category.id,
            name=category.name
        )
        session.add(new_category)
        session.commit()

        return category
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ma'lumotlarni faqat Admin o'zgartira oladi")
