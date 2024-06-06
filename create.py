from database import Engine, Base
from model import User, Category, Orders, Product

Base.metadata.create_all(bind=Engine)
