from sqlalchemy_utils import ChoiceType

from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(27), nullable=True)
    last_name = Column(String(27), nullable=True)
    username = Column(String(27), unique=True)
    email = Column(String(40), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Orders", back_populates="user")

    def __repr__(self):
        return f"< User {self.username}"


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(23))
    product = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"< Category {self.name}"


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(23))
    description = Column(String(233))
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="product")
    orders = relationship("Orders", back_populates="product")

    def __repr__(self):
        return f"< Product {self.name}"


class Orders(Base):
    __tablename__ = 'orders'
    OrderChoices = (
        ("PENDING", "pending"),
        ("TRANSIT", "transit"),
        ("DELIVERED", "delivered")
    )
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    count = Column(Integer)
    order_status = Column(ChoiceType(choices=OrderChoices), default="PENDING")
    product = relationship("Product", back_populates="orders")
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Orders {self.user_id}"
