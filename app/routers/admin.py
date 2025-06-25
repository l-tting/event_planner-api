from fastapi import APIRouter,status,Depends,HTTPException,Request,Response
from app.schemas import AdminCreate,AdminLogin,AdminRemove
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin
from functools import wraps
from fastapi.responses import JSONResponse
from werkzeug.security import generate_password_hash
from app import schemas,auth
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash


router = APIRouter()


def superadmin_required(current_admin: Admin = Depends(auth.get_current_admin)):
    if current_admin.role != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can perform this action")
    return current_admin




@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db),
    # current_admin:Admin=Depends(superadmin_required)
):
    existing = db.query(Admin).filter(Admin.admin_email == admin.admin_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")

    hashed_password = generate_password_hash(admin.password)
    new_admin = Admin(
        admin_name=admin.admin_name,
        admin_email=admin.admin_email,
        admin_phone=admin.admin_phone,
        password=hashed_password,
      
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin created successfully"}


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user: schemas.AdminLogin, db: Session = Depends(get_db)):
    valid_admin = db.query(Admin).filter(Admin.admin_email == user.admin_email).first()
    
    if valid_admin is None or not check_password_hash(valid_admin.password, user.admin_password):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    
    access_token = auth.create_access_token(
        data={"user": user.admin_email}, 
        expires_delta=timedelta(days=30)
    )
    print("Access token:", access_token)
    
    response = JSONResponse(
        content={"message": "Login successful", "current_user": valid_admin.admin_name}
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=30 * 24 * 60 * 60, 
        expires=30 * 24 * 60 * 60,
        samesite="Lax",             
        secure=False                
    )
    return response

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="Lax",  
        secure=False     # Set to True for HTTPS
    )
    return {"message": "Successfully logged out"}

@router.post('/remove',status_code=status.HTTP_200_OK)
def remove_admin(admin:AdminRemove,current_admin:Admin = Depends(superadmin_required),db:Session=Depends(get_db)):
    admin = db.query(Admin).filter(Admin.admin_email==admin.admin_email).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Admin not found")
    
    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted successfully"}


