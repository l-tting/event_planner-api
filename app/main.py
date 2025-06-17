from fastapi import FastAPI
from app.routers import admin,attendees,events,test,payment
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(admin.router, prefix='/admin',tags=['admin'])
app.include_router(attendees.router, prefix='/attendees',tags=['attendees'])
app.include_router(events.router, prefix='/events',tags=['events'])
app.include_router(test.router, prefix='/test',tags=['test'])
app.include_router(payment.router, prefix='/payment',tags=['mpesa'])

@app.get('/')
def index():
    return {"message": "Welcome to Project Harmony"}