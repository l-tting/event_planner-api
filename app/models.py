from sqlalchemy import Column,String,ForeignKey,Integer,func, DateTime,Enum
from app.database import Base
from sqlalchemy.orm import relationship
import enum


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False)
    event_name = Column(String(255), nullable=False)
    event_location = Column(String(255), nullable=False)
    event_datetime = Column(DateTime, nullable=False)
    event_image_url = Column(String(2083), nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    transactions = relationship("STK_Push", back_populates="event", cascade="all, delete")
    admin = relationship("Admin", back_populates="events")
    tickets = relationship("Ticket", back_populates="event", cascade="all, delete")



class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer,primary_key=True,nullable=False)
    admin_name = Column(String(255),nullable=False)
    admin_email = Column(String(255),unique=True,nullable=False)
    admin_phone = Column(String(255),nullable=False)
    password = Column(String(255),nullable=False)
    role = Column(String(50), nullable=False, default='admin') 
    events = relationship("Event", back_populates="admin", cascade="all, delete")



class Attendee(Base):
    __tablename__ = 'attendees'
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    phone_number = Column(String(100),nullable=False)
    email = Column(String(255),nullable=False)
    created_at = Column(DateTime,server_default=func.now())
    tickets = relationship("Ticket", back_populates="attendee", cascade="all, delete")


class TicketStatus(str, enum.Enum):
    PAID ='paid'
    FAILED = 'failed'
    PENDING = 'pending'


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey("attendees.id"),nullable=False)
    event_id = Column(Integer,ForeignKey('events.id'),nullable=False)
    qr_code_url = Column(String,nullable=False)
    status = Column(Enum(TicketStatus, name='ticket_status_enum'),default=TicketStatus.PENDING,nullable=False)
    purchased_at = Column(DateTime,server_default=func.now())
    attendee = relationship("Attendee", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")

class MPESAStatus(str, enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    TIMEOUT = 'timeout'



class STK_Push(Base):
    __tablename__= 'stk_push'
    stk_id = Column(Integer,primary_key=True)
    merchant_request_id = Column(String,nullable=False)
    checkout_request_id = Column(String,nullable=False)
    phone = Column(String,nullable=False)
    amount = Column(Integer,nullable=False)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False)
    event = relationship("Event", back_populates="transactions") 
    status = Column(Enum(MPESAStatus, name='mpesa_status_enum', create_type=False),
        default=MPESAStatus.PENDING,
        nullable=False
    )
    result_code = Column(String,nullable=True)
    result_desc = Column(String,nullable=True)
    created_at = Column(DateTime,server_default=func.now())