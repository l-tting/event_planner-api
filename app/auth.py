from fastapi import HTTPException,Depends,Request
from jose import jwt, ExpiredSignatureError,JWTError
from datetime import datetime,timedelta,timezone
from app.database import sessionlocal,get_db
from app.models import Admin
from sqlalchemy.orm import Session


SECRET_KEY='syusjn6876'
ALGORITHM ='HS256'
ACCESS_TOKEN_EXPIRY_TIME = timedelta(days=30)


def check_admin(email):
    db = sessionlocal()
    admin = db.query(Admin).filter(Admin.admin_email==email).first()
    return admin

def create_access_token(data:dict,expires_delta:timedelta | None=None):
    # create copy to avoid modifying original data
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRY_TIME
    to_encode.update({"exp":expires})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")    
    if not token:
        print("No token")
        raise HTTPException(status_code=401, detail="Access token missing from cookies")
    return token



async def get_current_admin(access_token: str = Depends(get_token_from_cookie)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('user')
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    admin = check_admin(email)
    if not admin:
        raise HTTPException(status_code=401, detail="User does not exist")

    return admin


