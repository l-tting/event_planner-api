from fastapi import APIRouter,status,Depends,HTTPException,File,Form,UploadFile
from app.models import Admin,Event
from app.auth import get_current_admin
from app.database import get_db
from app.schemas import EventCreate,EventUpdate
from sqlalchemy.orm import Session
from sqlalchemy import func
import shutil
import os
from datetime import datetime

router = APIRouter()

@router.post('/add', status_code=status.HTTP_201_CREATED)
def add_event(
    event_name: str = Form(...),
    event_location: str = Form(...),
    event_datetime: str = Form(...),  # send as ISO string from frontend
    event_image: UploadFile = File(...),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # Convert string to datetime object
    try:
        parsed_datetime = datetime.fromisoformat(event_datetime)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")

    # Check for duplicates on same date
    event_date = parsed_datetime.date()
    existing_event = db.query(Event).filter(
        Event.event_name == event_name,
        Event.event_location == event_location,
        func.date(Event.event_datetime) == event_date
    ).first()

    if existing_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event with same name, location, and datetime already exists"
        )

    # Save image
    image_dir = "static/images"
    os.makedirs(image_dir, exist_ok=True)
    image_path = os.path.join(image_dir, event_image.filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(event_image.file, buffer)

    image_url = f"/static/images/{event_image.filename}"

    # Create new event
    new_event = Event(
        event_name=event_name,
        event_location=event_location,
        event_datetime=parsed_datetime,
        event_image_url=image_url
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {"new_event": new_event}

@router.get('/fetch',status_code=status.HTTP_200_OK)
def get_events(current_admin:Admin=Depends(get_current_admin),db:Session=Depends(get_db)):
    events = db.query(Event).all()
    return {"events":events}


@router.put("/{event_id}", response_model=EventCreate)
def update_event(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Extract only explicitly provided values (Pydantic v2)
    raw_data = event_update.model_dump(exclude_unset=True)

    # Clean out undesired placeholder or empty values
    clean_data = {
        k: v for k, v in raw_data.items()
        if v not in ("string", "", None)
    }

    for key, value in clean_data.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event



@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    db.refresh()
    return {"Message":"Event deleted succesfully"}