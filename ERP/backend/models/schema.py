from pydantic import BaseModel

class logininput(BaseModel):
    email: str
    password: str

class userinput(BaseModel):
    username : str
    password : str
    email : str
    role : str
        
class aisearchinput(BaseModel):
    search: str
class productinput(BaseModel):
    product : str
    price : int

class orderinput(BaseModel):
    product_id: int
    quantity: int


class stringinput(BaseModel):
    value : str


    







