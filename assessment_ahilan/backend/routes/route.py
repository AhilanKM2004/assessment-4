from fastapi import APIRouter, Depends , UploadFile, File , HTTPException
from sqlalchemy.orm import Session
from models.schema import signinput,singleinput,userinput,logininput,courseinput, table_input
from models.model import users
from services.servic import attach_file_service,  delete_task_service ,edit_task_service,signup_service , task_input_service , getalltask_service , gettaskdate_service , gettaskpriority_service #, login_service
from database.deps import get_db
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from models.auth import login_user , get_current_user 
auth = OAuth2PasswordBearer(tokenUrl="login")
router33 = APIRouter()
import os
import shutil
from database.db import UPLOAD_DIR


@router33.post("/signup")
def siging(form_data: signinput,db: Session = Depends(get_db)):
    signup_service(db, form_data.username ,  form_data.email , form_data.password)


@router33.post("/login")
def login(
    form_data: logininput,
    db: Session = Depends(get_db)
):
    return login_user(db, form_data.email , form_data.password)

@router33.get("/me")
def get_me(current_user: users = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,}

@router33.post("/create_table")
def creating(data :table_input , current_user: users = Depends(get_current_user) , db : Session = Depends(get_db)):
    task_input_service(data.title , data.decription , data.due_date ,data.priority , db ) 

@router33.get("/getalltask")
def looking(current_user: users = Depends(get_current_user) , db : Session = Depends(get_db)):
    return getalltask_service( db ) 

@router33.get("/sortbydate")
def sortingbydate(current_user: users = Depends(get_current_user) , db : Session = Depends(get_db)):
    return gettaskdate_service( db ) 
@router33.get("/sortbypriority")
def sortingbypriority(current_user: users = Depends(get_current_user) , db : Session = Depends(get_db)):
    return gettaskpriority_service( db ) 
@router33.put("/editthis/{task_id}")
def edit_task(task_id: int,data: table_input,current_user: users = Depends(get_current_user), db: Session = Depends(get_db)):
    return edit_task_service(db, task_id, data)
@router33.delete("/deletethis/{x}")
def delete_task(x : int , current_user: users = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_task_service(db,x)

@router33.post("/attachfile/{task_id}")
def attach_file(task_id: int,file: UploadFile = File(...),db: Session = Depends(get_db),current_user = Depends(get_current_user)
):
    return attach_file_service(db, task_id, file)


# @router33.post("/upload_file")
# def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return {
#         "filename": file.filename,
#         "message": "File uploaded successfully"
#     }
















# @router33.get("/download/{file_name}")
# def downloader(file_name : str , token : str=Depends(auth)):
#     return download_file(data.value)
# @router33.post("/practice_quiz")
# def start(data:singleinput,db: Session = Depends(get_db)):
#     return Submit quiz(db , data.value)

# @router33.get("/check")
# def start(db: Session = Depends(get_db)):
#     return check()
# http://127.0.0.1:8000/enter_the_prompt


# @router33.post("/login")---------------------------------------------------------------------------------ai logic
# def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
#     user = db.query(Users).filter(Users.username == form_data.username).first()

#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_token({"sub": user.username})
#     return {"access_token": token, "token_type": "bearer"}


# @router33.post("/login")-------------------------------------------------------------------my simple logic , working one but old
# def start(data:logininput, db: Session = Depends(get_db)):
#     return login_service(db,data.name,data.password)