from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AdminCreate(BaseModel):
    admin_name: str
    admin_email: str
    admin_phone: str
    password: str
  
class AdminLogin(BaseModel):
    admin_email:str
    admin_password:str

class AdminRemove(BaseModel):
    admin_email:str

class EventCreate(BaseModel):
    event_name: str
    event_location: str
    event_datetime: datetime
    event_image_url: str

class EventUpdate(BaseModel):
    event_name: Optional[str]
    event_location: Optional[str]
    event_datetime: Optional[datetime]
    event_image_url: Optional[str]


class STK_PushResponse(BaseModel):
    merchant_request_id:str
    checkout_request_id:str
    status:str
    response_code:str='0'
    response_desc:str='Success. Request accepted for processing'
    customer_message: str = "Please check your phone to complete the payment" 


class MpesaCallback(BaseModel):
    merchant_request_id: str
    checkout_request_id: str
    result_code: str
    result_desc: str


class STK_PushCreate(BaseModel):
    phone_number:str
    amount: float

class STKPushCheckResponse(BaseModel):
    success: bool
    message: str
    status: Optional[str] = None