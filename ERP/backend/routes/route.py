from fastapi import APIRouter, Depends , UploadFile, File , HTTPException
from sqlalchemy.orm import Session
from models.schema import  userinput , logininput  , orderinput ,aisearchinput
from models.model import users , products , orders
from services.servic import signup_service , generate_chart_service, view_raw_csv_service , ai_search_service
from database.deps import get_db
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from models.auth import login_user , get_current_user 
auth = OAuth2PasswordBearer(tokenUrl="login")
router33 = APIRouter()
import os
import shutil
from database.db import UPLOAD_DIR
from fastapi.responses import FileResponse

@router33.post("/signup")
def siging(form_data: userinput,db: Session = Depends(get_db)):
    return signup_service(db, form_data.username ,  form_data.email , form_data.password , form_data.role)
   
@router33.post("/login")
def login(form_data: logininput,db: Session = Depends(get_db)):
    return login_user(db, form_data.email , form_data.password)

@router33.get("/me")
def get_me(current_user: users = Depends(get_current_user)):
    return {"name": current_user.name,"email": current_user.email,"role":current_user.role}

@router33.get("/line chart/chart_view")
def line_chart_view(filename: str,current_user: users = Depends(get_current_user)):
    try:
        chart_path = generate_chart_service(filename, "line chart")
        return FileResponse(chart_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router33.get("/area chart/chart_view")
def area_chart_view(filename: str,current_user: users = Depends(get_current_user)):
    try:
        chart_path = generate_chart_service(filename, "area chart")
        return FileResponse(chart_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router33.get("/scatter chart/chart_view")
def scatter_chart_view(filename: str,current_user: users = Depends(get_current_user)):
    try:
        chart_path = generate_chart_service(filename, "scatter chart")
        return FileResponse(chart_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router33.post("/upload_file")
def uploading_file(file: UploadFile = File(...),current_user: users = Depends(get_current_user)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "filename": file.filename,
        "message": "File uploaded successfully"}
@router33.get("/to_view_raw_file")
def raw_file(filename: str,current_user: users = Depends(get_current_user)):
    try:
        return view_raw_csv_service(filename)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router33.post("/upload_file")
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully"
    }

@router33.post("/ai_search")
def ai_search(data: aisearchinput,current_user: users = Depends(get_current_user)):
    result = ai_search_service(data.search)
    return {"result": result}




@router33.get("/products")
def get_products(
    db: Session = Depends(get_db),
    current_user: users = Depends(get_current_user)
):
    items = db.query(products).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image": f"http://127.0.0.1:8000/{p.image}"
        }
        for p in items
    ]


@router33.post("/place_order")
def place_order(data: orderinput,db: Session = Depends(get_db),current_user: users = Depends(get_current_user)):
    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be zero")
    new_order = orders(
        customer_id=current_user.id,
        product_id=data.product_id,
        quantity=data.quantity
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {"message": "Order placed successfully"}


from fastapi import UploadFile, File, Form
import shutil
import os

PRODUCT_IMAGE_DIR = "product_images"
os.makedirs(PRODUCT_IMAGE_DIR, exist_ok=True)


@router33.post("/add_product")
def add_product(
    name: str = Form(...),
    price: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: users = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPG or PNG allowed")

    image_path = os.path.join(PRODUCT_IMAGE_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_product = products(
        name=name,
        price=price,
        image=image_path
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product added successfully"}








