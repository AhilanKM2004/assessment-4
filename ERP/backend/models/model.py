from sqlalchemy import Column, Integer, String , ForeignKey
from database.db import base

class users(base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)
    role=Column(String)



class products(base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    image = Column(String)   


class orders(base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer,ForeignKey("user.id"))
    product_id = Column(Integer,ForeignKey("product.id"))
    quantity = Column(Integer)




