from pydantic import BaseModel
from datetime import date

class signinput(BaseModel):
    username : str
    email: str
    password: str
class table_input(BaseModel):
    title: str
    decription: str
    due_date: date
    priority:int


class logininput(BaseModel):
    email: str
    password: str

class userinput(BaseModel):
    name : str
    password : str
    email : str
    role : str
        
class singleinput(BaseModel):
    value : str

class quizinput(BaseModel):
    student_id : int
    course_name : str

class chatinput(BaseModel):
    response : str

class courseinput(BaseModel):
    course_name : str
    student_id : int
    module_id : int


    







