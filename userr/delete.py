from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from model import User
from database import SessionLocal
from schemas import UserModel
from fastapi_jwt_auth import AuthJWT

user_delete = APIRouter(prefix="/user")


@user_delete.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(SessionLocal)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        db.delete(db_user)
        db.commit()

        return {"msg": "User deleted successfully"}
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ma'lumotlarni faqat ADMIN o'zgartira oladi")
