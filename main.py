
from fastapi import FastAPI, HTTPException, status, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, Any
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Base, engine
from services import get_parking_slots, get_parking_by_id, create_parking

Base.metadata.create_all(bind = engine)

app = FastAPI()

class CreateParking(BaseModel):
    slot_code: str 
    zone_name: str = Field(min_length=3)
    max_weight: int = Field(gt=0)
    is_available: bool


def to_dict(parking):
    return {
        "slot_id": parking.slot_id,
        "slot_code": parking.slot_code,
        "zone_name": parking.zone_name,
        "max_weight": parking.max_weight,
        "is_available": parking.is_available
    }

class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str
    path: str

def success_response(status_code: int, message: str, data: Any, error: str, path: str = None):
    return BaseResponse(
        status_code=status_code,
        message=message,
        data = data,
        error=error,
        timestamp=datetime.now().isoformat(),
        path= path
    )

def fail_response(status_code: int, message: str, data: Any = None, error: str = None, path: str = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code":status_code,
            "message":message,
            "data": data,
            "error":error,
            "timestamp":datetime.now().isoformat(),
            "path": path
        }
        
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return fail_response(
        status_code=exc.status_code,
        message=exc.detail,
        error="HTTPException",
        path=request.url.path
    )


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return fail_response(
        status_code=500,
        message="System error",
        error=str(exc),
        path=request.url.path
    )



@app.get("/connect")
def test_connect(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"msg": "Connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parking-slots", status_code=status.HTTP_201_CREATED)
def create_parking_slot(request: Request, parking: CreateParking, db: Session = Depends(get_db)):
    result = create_parking(
        db = db,
        slot_code=parking.slot_code,
        zone_name=parking.zone_name,
        max_weight=parking.max_weight,
        is_available=parking.is_available
    )

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Create Success!",
        data= to_dict(result),
        error=None,
        path=request.url.path
    )


@app.get("/parking-slots")
def get_all_parking(request: Request, db: Session = Depends(get_db)):
    result = get_parking_slots(
        db=db
    )
    if result == []:
        raise HTTPException(
            status_code=400,    
            detail=[]
        )
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Create Success!",
        data= (to_dict(i) for i in result),
        error=None,
        path=request.url.path
    )

@app.get("/parking-slots/{slot_id}")
def get_parking_id(request: Request, slot_id: int, db: Session = Depends(get_db)):
    result = get_parking_by_id(
        db=db,
        slot_id = slot_id
    )

    return success_response(
            status_code=status.HTTP_200_OK,
            message="Get Successful",
            data= to_dict(result),
            error=None,
            path=request.url.path
        )